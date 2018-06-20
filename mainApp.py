# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import os
import sys
import time
from multiprocessing import cpu_count

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QWidget, QApplication, QMainWindow

from AbsCor import JOB_LOCAL, PARAM_DET_X, PARAM_DET_Y, \
    PARAM_DET_OFFSET_X, PARAM_DET_OFFSET_Y, PARAM_SAM_LENGHT, PARAM_SAM_RADIUS, \
    PARAM_SIM_SDD, PARAM_SIM_PHOTONS, PARAM_SIM_MAX_RUNNING_TIME, PARAM_SIM_NODES, \
    PARAM_SIM_PROCESSES
from AbsCor.gui.mainTemplate import Ui_Form
from bmg_raytrace import Detector
from detector import Detector
from jobWidget import JobWidget


class MainWidget(QWidget, Ui_Form):
    localJobProc = None
    jobCount = 0

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.jobs = {}
        self.logger = logging.getLogger("Gui")
        self.logger.setLevel(logging.DEBUG)
        logFormat = '%(asctime)s, %(name)s, %(levelname)s, %(message)s'
        formatter = logging.Formatter(logFormat, datefmt='%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler("./gui.log")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.setupUi(self)

    def setupUi(self, Form):
        Ui_Form.setupUi(self, Form)

        self.simulationProcessesInput.setValue(cpu_count())
        self.showJobGroup(False)

    def uiFinishWait(self):
        for _ in range(0, 100):
            QApplication.processEvents()

    def showJobGroup(self, flag=True):
        if flag:
            self.currentJobGroup.show()
        else:
            self.currentJobGroup.hide()
        self.uiFinishWait()
        self.adjustSize()

    @pyqtSlot()
    def startJob(self):
        self.jobCount += 1
        jobWidget = JobWidget(self.getParams())
        tabIndex = self.jobTabs.addTab(jobWidget, u"Job {0}".format(self.jobCount))
        self.jobs[self.jobCount] = (jobWidget, tabIndex)
        self.showJobGroup(True)
        self.jobTabs.setCurrentIndex(tabIndex)
        jobWidget.sigCloseJob.connect(lambda jobIndex=self.jobCount: self.closeJob(jobIndex))
        jobWidget.sigStartJob.emit()

    def closeJob(self, jobIndex):
        _, tabIndex = self.jobs[jobIndex]
        self.jobTabs.removeTab(self.jobTabs.currentIndex())
        del self.jobs[jobIndex]

    @pyqtSlot()
    def cancelJob(self):
        if self.runningJob is None: return

        if self.runningJob[0] == JOB_LOCAL:
            self._cancelLocalJob()

    def getParams(self):
        return {
            PARAM_DET_X: int(self.detectorWidthInput.value()),
            PARAM_DET_Y: int(self.detectorHeightInput.value()),
            PARAM_DET_OFFSET_X: int(self.detectorOffsetXInput.value()),
            PARAM_DET_OFFSET_Y: int(self.detectorOffsetYInput.value()),
            PARAM_SAM_LENGHT: int(self.sampleLengthInput.value()),
            PARAM_SAM_RADIUS: int(self.sampleRadiusInput.value()),
            PARAM_SIM_PHOTONS: int(self.simulationPhotonsInput.value()),
            PARAM_SIM_MAX_RUNNING_TIME: int(self.simulationRunningTimeInput.value()),
            PARAM_SIM_NODES: int(self.simulationNodesInput.value()),
            PARAM_SIM_PROCESSES: int(self.simulationProcessesInput.value()),
            PARAM_SIM_SDD: int(self.sampleSddhInput.value()),
        }


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = QMainWindow()
    win.setWindowTitle(u"AbsCor")
    widget = MainWidget()
    win.setCentralWidget(widget)

    win.show()
    app.exec_()
