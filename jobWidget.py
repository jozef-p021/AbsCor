# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import os
import subprocess
from signal import SIGTERM
from threading import Thread

import time
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QString
from PyQt4.QtGui import QWidget, QMessageBox
from PySide.QtCore import QTimer

from AbsCor import JOB_LOCAL, PARAM_DET_X, PARAM_DET_Y, \
    PARAM_DET_OFFSET_X, PARAM_DET_OFFSET_Y, PARAM_SAM_LENGHT, PARAM_SAM_RADIUS, \
    PARAM_SIM_SDD, PARAM_SIM_PHOTONS, PARAM_SIM_PROCESSES, PARAM_SIM_MAX_RUNNING_TIME
from AbsCor.gui.jobTemplate import Ui_Form
from detector import Detector

import fabio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D, axes3d

from snippets import getScaledTimeHumanReadable


class JobWidget(QWidget, Ui_Form):
    sigCloseJob = pyqtSignal()
    sigFinishJob = pyqtSignal()
    sigStartJob = pyqtSignal()
    sigJobStatusChanged = pyqtSignal(QString)
    jobCancelCountDown = 0

    def __init__(self, jobParams, parent=None):
        super(JobWidget, self).__init__(parent)
        self.logger = logging.getLogger(u"Gui")
        self.jobParams = jobParams
        self.jobTimeCounter = QTimer()
        self.jobTimeCounter.timeout.connect(self.jobTimerTick)

        self.sigFinishJob.connect(self._finishJob)
        self.sigStartJob.connect(self.startJob)
        self.setupUi(self)

    def _startLocalJob(self):
        try:
            params = self.jobParams
            outputFile = self.getOutputName()
            cmd = ["mpirun", "-n", params[PARAM_SIM_PROCESSES],
                   "python", "bmg_raytrace_mpi_distr.py",
                   "--o", outputFile,
                   "--detX", params[PARAM_DET_X],
                   "--detY", params[PARAM_DET_Y],
                   "--detOffsetX", params[PARAM_DET_OFFSET_X],
                   "--detOffsetY", params[PARAM_DET_OFFSET_Y],
                   "--sdd", params[PARAM_SIM_SDD],
                   "--samLength", params[PARAM_SAM_LENGHT],
                   "--samRadius", params[PARAM_SAM_RADIUS],
                   "--N", params[PARAM_SIM_PHOTONS],
                   ]
            cmd = " ".join([str(part) for part in cmd])
            self.localJobProc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                                 shell=True, preexec_fn=os.setsid)
            self.logger.debug(u"Local job started")
            self.runningJob = (JOB_LOCAL, outputFile)

            if self.localJobProc.wait() != 0:
                self.logger.debug(u"Local job finished with error")
                self.sigJobStatusChanged.emit("E")
            else:
                self.logger.debug(u"Local job successfully finished")
                self.sigJobStatusChanged.emit(u"F")

        except Exception as e:
            self.logger.error(u"Exception: {0}".format(e))
            self.sigJobStatusChanged.emit(u"E")
        finally:
            self.sigFinishJob.emit()

    def _cancelLocalJob(self):
        if self.localJobProc is not None:
            os.killpg(os.getpgid(self.localJobProc.pid), SIGTERM)
            self.runningJob = None
            self.localJobProc = None

    def _finishJob(self):
        if self.runningJob is not None:
            outputFile = self.runningJob[1]
            self.displayOutput(outputFile)

        p = time.localtime()
        datestring = u'{0:d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour,
                                                                             p.tm_min, p.tm_sec)
        self.endTimeLabel.setText(datestring)
        self.jobTimeCounter.stop()
        self.jobProgressWidget.hide()
        self.runningJob = None
        self.localJobProc = None

    @pyqtSlot()
    def cancelJob(self):
        if self.runningJob is None: return

        if self.runningJob[0] == JOB_LOCAL:
            self._cancelLocalJob()
            self.sigJobStatusChanged.emit(u"C")

    @pyqtSlot()
    def closeJob(self):
        if self.runningJob is not None:
            message = QMessageBox()
            ret = message.question(self, u'', u"Job is still running, do You want to cancel it?", message.Yes | message.No)
            if ret == message.No:
                return
            else:
                self.cancelJob()

        self.sigCloseJob.emit()

    @pyqtSlot()
    def jobTimerTick(self):
        self.jobCancelCountDown -= 1
        interval = self.jobParams[PARAM_SIM_MAX_RUNNING_TIME] * 60
        self.progressBar.setFormat(u'{0}'.format(getScaledTimeHumanReadable(self.jobCancelCountDown)))
        self.progressBar.setValue((100. / interval) * self.jobCancelCountDown)

        if self.jobCancelCountDown <= 0:
            self.cancelJob()

    def startJob(self):
        Thread(target=self._startLocalJob).start()
        self.sigJobStatusChanged.emit(u"R")
        self.jobTimeCounter.setInterval(1000)
        self.jobCancelCountDown = self.jobParams[PARAM_SIM_MAX_RUNNING_TIME] * 60 + 1
        self.jobTimerTick()
        p = time.localtime()
        datestring = u'{0:d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour,
                                                                             p.tm_min, p.tm_sec)
        self.initTimeLabel.setText(datestring)
        self.jobTimeCounter.start()
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
        canvas.draw()