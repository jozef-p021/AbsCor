# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import os
import re
import subprocess
import tempfile
import time
from signal import SIGTERM
from threading import Thread

import fabio
import matplotlib.pyplot as plt
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QString
from PyQt4.QtGui import QWidget, QMessageBox
from PySide.QtCore import QTimer
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from AbsCor import JOB_LOCAL, PARAM_DET_X, PARAM_DET_Y, \
    PARAM_DET_OFFSET_X, PARAM_DET_OFFSET_Y, PARAM_SAM_LENGHT, PARAM_SAM_RADIUS, \
    PARAM_SIM_SDD, PARAM_SIM_PHOTONS, PARAM_SIM_PROCESSES, PARAM_SIM_MAX_RUNNING_TIME, PARAM_JOB_TYPE, STATUS_INIT, \
    STATUS_ERROR, STATUS_CANCELLED, STATUS_RUNNING, STATUS_FINISHED, PARAM_REMOTE_JOB_CONFIG, \
    PARAM_SIM_NODES, JOB_REMOTE, SIMULATION_SCRIPT_PATH
from AbsCor.gui.jobTemplate import Ui_Form
from detector import Detector
from snippets import getScaledTimeHumanReadable
from pexpect import pxssh
from mpl_toolkits.mplot3d import Axes3D, axes3d
from paramiko import SSHClient
from scp import SCPClient
import datetime


class JobWidget(QWidget, Ui_Form):
    sigCloseJob = pyqtSignal()
    sigFinishJob = pyqtSignal()
    sigStartJob = pyqtSignal()
    sigJobStatusChanged = pyqtSignal(QString)
    jobCancelCountDown = 0
    outputFile = None
    status = STATUS_INIT
    remoteJobId = None
    jobStartTime = None
    jobEndTime = None

    def __init__(self, jobParams, parent=None):
        super(JobWidget, self).__init__(parent)
        self.logger = logging.getLogger(u"Gui")
        self.jobParams = jobParams
        self.jobTimeCounter = QTimer()
        self.jobTimeCounter.setInterval(1000)
        self.jobTimeCounter.timeout.connect(self.jobTimerTick)

        self.sigFinishJob.connect(self._finishJob)
        self.sigStartJob.connect(self.startJob)
        self.setupUi(self)

    def _startLocalJob(self):
        try:
            cmd = self._getMpiCommand()
            self.localJobProc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                                 shell=True, preexec_fn=os.setsid)
            self.status = STATUS_RUNNING
            self.sigJobStatusChanged.emit(self.status)

            self.logger.debug(u"Local job started")

            if self.localJobProc.wait() != 0:
                self.logger.debug(u"Local job finished with error")
                self.status = STATUS_ERROR
                self.sigJobStatusChanged.emit(self.status)
            else:
                self.logger.debug(u"Local job successfully finished")
                self.status = STATUS_FINISHED
                self.sigJobStatusChanged.emit(self.status)

        except Exception as e:
            self.logger.error(u"Exception: {0}".format(e))
            self.status = STATUS_ERROR
            self.sigJobStatusChanged.emit(self.status)
        finally:
            self.sigFinishJob.emit()

    def _startRemoteJob(self):
        try:
            cmd = self._getMpiCommand()
            remoteConfig = self.jobParams[PARAM_REMOTE_JOB_CONFIG]
            remoteWorkingDir = remoteConfig[u"repo"]
            remoteHost = remoteConfig[u"host"]
            remoteUser = remoteConfig[u"user"]
            remotePass = remoteConfig[u"pass"]

            if self.jobParams[PARAM_SIM_MAX_RUNNING_TIME] > 0:
                maxRuntime = datetime.timedelta(minutes=self.jobParams[PARAM_SIM_MAX_RUNNING_TIME])
            else:
                maxRuntime = u"99-00:00:00"

            template = remoteConfig[u"template"]
            template = template.replace(u"{PARAM_SIM_MAX_RUNNING_TIME}", unicode(maxRuntime))
            template = template.replace(u"{PARAM_SIM_NODES}", unicode(self.jobParams[PARAM_SIM_NODES]))
            template = template.replace(u"{PARAM_REMOTE_WORKING_DIR}", unicode(remoteWorkingDir))
            template = template.replace(u"{PARAM_JOB_COMMAND}", cmd)

            self.logger.debug(u"Remote job started")

            fd, path = tempfile.mkstemp()
            with os.fdopen(fd, 'w') as tmp:
                # do stuff with temp file
                tmp.write(template)

            from paramiko import SSHClient
            from scp import SCPClient
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname=remoteHost, username=remoteUser, password=remotePass)

            with SCPClient(ssh.get_transport()) as scp:
                scp.put(path, '{0}/remoteSbatchJob.sh'.format(remoteWorkingDir))

            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sbatch {0}/remoteSbatchJob.sh'.format(remoteWorkingDir))
            self.remoteJobId = int(re.search("[0-9]*$", ssh_stdout.readlines()[0]).group(0))

            while True:
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
                    'scontrol show jobid -dd {0}'.format(self.remoteJobId))
                line = ssh_stdout.readlines()[3]
                jobStatus = re.search(u"JobState=(\w*)", line).group(1)
                if jobStatus == "PENDING":
                    self.status = STATUS_INIT
                elif jobStatus == "RUNNING":
                    self.status = STATUS_RUNNING
                elif jobStatus == "CANCELLED":
                    self.status = STATUS_ERROR
                    break
                elif jobStatus == "ERROR":
                    self.status = STATUS_ERROR
                    break
                elif jobStatus == "COMPLETED":
                    self.status = STATUS_FINISHED
                    scp.get('{0}/{1}'.format(remoteWorkingDir, self.outputFile.replace("./","")), self.outputFile)
                    break

                self.sigJobStatusChanged.emit(self.status)
                time.sleep(1)

            self.sigJobStatusChanged.emit(self.status)

        except Exception as e:
            self.logger.error(u"Exception: {0}".format(e))
            self.status = STATUS_ERROR

            self.sigJobStatusChanged.emit(self.status)
        finally:
            self.sigFinishJob.emit()

    def _cancelLocalJob(self):
        if self.status in (STATUS_RUNNING, STATUS_INIT) and self.localJobProc is not None:
            os.killpg(os.getpgid(self.localJobProc.pid), SIGTERM)
            self.localJobProc = None

    def _cancelRemoteJob(self):
        remoteConfig = self.jobParams[PARAM_REMOTE_JOB_CONFIG]
        remoteHost = remoteConfig[u"host"]
        remoteUser = remoteConfig[u"user"]
        remotePass = remoteConfig[u"pass"]

        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(hostname=remoteHost, username=remoteUser, password=remotePass)

        ssh.exec_command('scancel {0}'.format(self.remoteJobId))

    def _finishJob(self):
        if os.path.isfile(self.outputFile):
            self.displayOutput(self.outputFile)

        self.jobEndTime = time.time()
        self.jobTimeCounter.stop()
        self.jobProgressWidget.hide()

    def _getMpiCommand(self):
        cmd = ["mpirun", "-n", self.jobParams[PARAM_SIM_PROCESSES],
               "python", SIMULATION_SCRIPT_PATH,
               "--o", self.outputFile,
               "--detX", self.jobParams[PARAM_DET_X],
               "--detY", self.jobParams[PARAM_DET_Y],
               "--detOffsetX", self.jobParams[PARAM_DET_OFFSET_X],
               "--detOffsetY", self.jobParams[PARAM_DET_OFFSET_Y],
               "--sdd", self.jobParams[PARAM_SIM_SDD],
               "--samLength", self.jobParams[PARAM_SAM_LENGHT],
               "--samRadius", self.jobParams[PARAM_SAM_RADIUS],
               "--N", self.jobParams[PARAM_SIM_PHOTONS],
               ]
        return " ".join([str(part) for part in cmd])

    def _getSlurmJobFile(self):
        pass

    @pyqtSlot()
    def cancelJob(self):
        if self.jobParams[PARAM_JOB_TYPE] == JOB_LOCAL:
            self._cancelLocalJob()
        elif self.jobParams[PARAM_JOB_TYPE] == JOB_REMOTE:
            self._cancelRemoteJob()
        self.status = STATUS_CANCELLED
        self.sigJobStatusChanged.emit(self.status)

    @pyqtSlot()
    def closeJob(self):
        if self.status in (STATUS_RUNNING, STATUS_INIT):
            message = QMessageBox()
            ret = message.question(self, u'', u"Job is still running, do You want to cancel it?",
                                   message.Yes | message.No)
            if ret == message.No:
                return
            else:
                self.cancelJob()

        self.sigCloseJob.emit()

    @pyqtSlot()
    def jobTimerTick(self):
        if self.jobParams[PARAM_SIM_MAX_RUNNING_TIME] > 0:
            self.jobCancelCountDown -= 1
            interval = self.jobParams[PARAM_SIM_MAX_RUNNING_TIME] * 60
            self.progressBar.setFormat(u'{0}'.format(getScaledTimeHumanReadable(self.jobCancelCountDown)))
            self.progressBar.setValue((100. / interval) * self.jobCancelCountDown)

            if self.jobCancelCountDown <= 0:
                self.cancelJob()

        if self.jobStartTime is not None:
            runtime = int(time.time() - self.jobStartTime)
            self.runTimeLabel.setText(u'{0}'.format(getScaledTimeHumanReadable(runtime)))

    def startJob(self):
        self.outputFile = self.getOutputName()

        if self.jobParams[PARAM_JOB_TYPE] == JOB_LOCAL:
            Thread(target=self._startLocalJob).start()
        else:
            Thread(target=self._startRemoteJob).start()

        if self.jobParams[PARAM_SIM_MAX_RUNNING_TIME] > 0:
            self.jobCancelCountDown = self.jobParams[PARAM_SIM_MAX_RUNNING_TIME] * 60 + 1
            self.jobTimerTick()
        else:
            self.progressBar.setFormat(u'Unlimited')
            self.progressBar.setValue(100)

        self.jobStartTime = time.time()
        p = time.localtime()
        datestring = u'{0:d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour,
                                                                             p.tm_min, p.tm_sec)
        self.jobTimeCounter.start()
        self.initTimeLabel.setText(datestring)
        self.jobProgressWidget.show()

    def getOutputName(self):
        p = time.localtime()
        datestring = u'{0:d}-{1:02d}-{2:02d}_{3:02d}-{4:02d}-{5:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour,
                                                                             p.tm_min, p.tm_sec)
        fileName = u"{0}.{1}".format(datestring, u"edf")
        return os.path.join(u"./output", fileName)

    def displayOutput(self, edfFile):
        output = fabio.openimage.openimage(edfFile)
        det = Detector(self.jobParams[PARAM_DET_X], self.jobParams[PARAM_DET_Y])
        det.SDD = self.jobParams[PARAM_SIM_SDD]
        det.detector_offset(self.jobParams[PARAM_DET_OFFSET_X], self.jobParams[PARAM_DET_OFFSET_Y])

        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(1, 1, 1, projection=u'3d')
        ax.plot_surface(det.xd, det.yd, output.data, cmap=u'jet')
        self.jobPlotFrame.layout().addWidget(canvas)
        fig.subplots_adjust(left=0, bottom=0, right=0.1, top=0.1)
        fig.tight_layout(pad=0.5)
        canvas.draw()
