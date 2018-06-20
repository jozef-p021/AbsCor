# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import os
import subprocess
from signal import SIGTERM
from threading import Thread

import fabio
import time
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QWidget

from AbsCor import JOB_LOCAL, PARAM_DET_X, PARAM_DET_Y, \
    PARAM_DET_OFFSET_X, PARAM_DET_OFFSET_Y, PARAM_SAM_LENGHT, PARAM_SAM_RADIUS, \
    PARAM_SIM_SDD, PARAM_SIM_PHOTONS, PARAM_SIM_PROCESSES
from AbsCor.gui.jobTemplate import Ui_Form
from detector import Detector

import fabio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class JobWidget(QWidget, Ui_Form):
    sigCloseJob = pyqtSignal()
    sigFinishJob = pyqtSignal()
    sigStartJob = pyqtSignal()

    def __init__(self, jobParams, parent=None):
        super(JobWidget, self).__init__(parent)
        self.logger = logging.getLogger("Gui")
        self.jobParams = jobParams
        self.sigFinishJob.connect(self._finishJob)
        self.sigStartJob.connect(self.startJob)
        self.setupUi(self)

    @pyqtSlot()
    def cancelJob(self):
        pass

    @pyqtSlot()
    def closeJob(self):
        self.sigCloseJob.emit()

    def startJob(self):
        Thread(target=self._startLocalJob).start()
        self.jobProgressWidget.show()

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
            else:
                self.logger.debug(u"Local job successfully finished")

        except Exception as e:
            self.logger.error(u"Exception: {0}".format(e))
        finally:
            self.sigFinishJob.emit()

    def _cancelLocalJob(self):
        if self.localJobProc is not None:
            os.killpg(os.getpgid(self.localJobProc.pid), SIGTERM)

    def _finishJob(self):
        outputFile = self.runningJob[1]
        self.runningJob = None
        self.localJobProc = None
        self.jobProgressWidget.hide()
        self.displayOutput(outputFile)

    def getOutputName(self):
        p = time.localtime()
        datestring = u'{0:d}-{1:02d}-{2:02d}_{3:02d}-{4:02d}-{5:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour,
                                                                             p.tm_min, p.tm_sec)
        fileName = u"{0}.{1}".format(datestring, u"edf")
        return os.path.join(u"./output", fileName)

    def displayOutput(self, edfFile):
        output = fabio.openimage.openimage(edfFile)
        detX, detY = output.data.shape
        det = Detector(detX, detY)

        fig = plt.figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        cset = ax.plot_surface(det.xd, det.yd, output.data, cmap='jet')
        self.jobPlotFrame.layout().addWidget(canvas)
        canvas.draw()
        # plt.show()
