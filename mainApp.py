# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import sys
from multiprocessing import cpu_count

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QWidget, QApplication, QMainWindow

from AbsCor import JOB_LOCAL, PARAM_DET_X, PARAM_DET_Y, \
    PARAM_DET_OFFSET_X, PARAM_DET_OFFSET_Y, PARAM_SAM_LENGHT, PARAM_SAM_RADIUS, \
    PARAM_SIM_SDD, PARAM_SIM_PHOTONS, PARAM_SIM_MAX_RUNNING_TIME, PARAM_SIM_NODES, \
    PARAM_SIM_PROCESSES
from AbsCor.gui.mainTemplate import Ui_Form
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
        tabIndex = self.jobTabs.addTab(jobWidget, u"Job {0} [Init]".format(self.jobCount))
        self.jobs[self.jobCount] = jobWidget
        self.showJobGroup(True)
        self.jobTabs.setCurrentIndex(tabIndex)
        jobWidget.sigCloseJob.connect(lambda jobIndex=self.jobCount: self.closeJob(jobIndex))
        jobWidget.sigJobStatusChanged.connect(lambda status, jobIndex=self.jobCount: self.setJobStatus(status, jobIndex))
        jobWidget.sigStartJob.emit()

    def setJobStatus(self, status, jobIndex):
        jobWidget = self.jobs[jobIndex]
        tabIndex = self.jobTabs.indexOf(jobWidget)
        self.jobTabs.setTabText(tabIndex, u"Job {0} [{1}]".format(jobIndex, status))


    def closeJob(self, jobIndex):
        jobWidget = self.jobs[jobIndex]
        self.jobTabs.removeTab(self.jobTabs.indexOf(jobWidget))
        del self.jobs[jobIndex]

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
