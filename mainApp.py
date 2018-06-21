# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import logging
import sys

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QWidget, QApplication, QMainWindow

from AbsCor import PARAM_DET_X, PARAM_DET_Y, \
    PARAM_DET_OFFSET_X, PARAM_DET_OFFSET_Y, PARAM_SAM_LENGHT, PARAM_SAM_RADIUS, \
    PARAM_SIM_SDD, PARAM_SIM_PHOTONS, PARAM_SIM_MAX_RUNNING_TIME, PARAM_SIM_NODES, \
    PARAM_SIM_PROCESSES
from AbsCor.gui.mainTemplate import Ui_Form
from jobWidget import JobWidget
from snippets import parseXMLFile, parseXMLTags

PRESET_DETECTOR = u"detector"
PRESET_SAMPLE = u"sample"
PRESET_SIMULATION = u"simulation"


class MainWidget(QWidget, Ui_Form):
    localJobProc = None
    jobCount = 0
    xmlConfigFile = None

    def __init__(self, xmlConfigFile=None, parent=None):
        super(MainWidget, self).__init__(parent)
        self.jobs = {}
        self.presets = {PRESET_DETECTOR: [], PRESET_SAMPLE: [], PRESET_SIMULATION: []}
        self.logger = logging.getLogger(u"Gui")
        self.logger.setLevel(logging.DEBUG)
        logFormat = u'%(asctime)s, %(name)s, %(levelname)s, %(message)s'
        formatter = logging.Formatter(logFormat, datefmt=u'%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler(u"./gui.log")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        if xmlConfigFile is not None:
            self.xmlConfigFile = xmlConfigFile
            self.parseXmlConfig(xmlConfigFile)

        self.setupUi(self)

    def setupUi(self, Form):
        Ui_Form.setupUi(self, Form)

        for presetGroup, presets in self.presets.items():
            for label, presetConfig in presets:
                if presetGroup == PRESET_DETECTOR:
                    self.detectorPresetSelect.addItem(label)
                elif presetGroup == PRESET_SAMPLE:
                    self.samplePresetSelect.addItem(label)
                elif presetGroup == PRESET_SIMULATION:
                    self.simulationPresetSelect.addItem(label)

        self.setDetectorPreset(0)
        self.setSamplePreset(0)
        self.setSimulationPreset(0)

        self.showJobGroup(False)

    def uiFinishWait(self):
        for _ in range(0, 100):
            QApplication.processEvents()

    def parseXmlConfig(self, configFile=None):
        if configFile is None: return
        config = parseXMLFile(configFile)
        for presetGroup in self.presets.keys():
            detectorPresets = config.getElementsByTagName(presetGroup)
            for detectorPreset in detectorPresets:
                label = detectorPreset.getAttribute("label")
                self.presets[presetGroup].append((label, parseXMLTags(detectorPreset.childNodes)))

    def showJobGroup(self, flag=True):
        if flag:
            self.currentJobGroup.show()
        else:
            self.currentJobGroup.hide()
        self.uiFinishWait()
        self.adjustSize()

    @pyqtSlot()
    def setDetectorPreset(self, index):
        label, config = self.presets[PRESET_DETECTOR][index]
        self.detectorWidthInput.setValue(config[u"Width"])
        self.detectorHeightInput.setValue(config[u"Height"])
        self.detectorOffsetXInput.setValue(config[u"Offset X"])
        self.detectorOffsetYInput.setValue(config[u"Offset Y"])

    @pyqtSlot()
    def setSamplePreset(self, index):
        label, config = self.presets[PRESET_SAMPLE][index]
        self.sampleLengthInput.setValue(config[u"Length"])
        self.sampleRadiusInput.setValue(config[u"Radius"])

    @pyqtSlot()
    def setSimulationPreset(self, index):
        label, config = self.presets[PRESET_SIMULATION][index]
        self.simulationPhotonsInput.setValue(config[u"Photons"])
        self.sampleSddhInput.setValue(config[u"SDD"])
        self.simulationNodesInput.setValue(config[u"Nodes"])
        self.simulationProcessesInput.setValue(config[u"Processes"])
        self.simulationRunningTimeInput.setValue(config[u"Max. runtime"])

    @pyqtSlot()
    def startJob(self):
        self.jobCount += 1
        jobWidget = JobWidget(self.getParams())
        tabIndex = self.jobTabs.addTab(jobWidget, u"Job {0} [ I ]".format(self.jobCount))
        self.jobs[self.jobCount] = jobWidget
        self.showJobGroup(True)
        self.jobTabs.setCurrentIndex(tabIndex)
        jobWidget.sigCloseJob.connect(lambda jobIndex=self.jobCount: self.closeJob(jobIndex))
        jobWidget.sigJobStatusChanged.connect(
            lambda status, jobIndex=self.jobCount: self.setJobStatus(status, jobIndex))
        jobWidget.sigStartJob.emit()

    def setJobStatus(self, status, jobIndex):
        jobWidget = self.jobs[jobIndex]
        tabIndex = self.jobTabs.indexOf(jobWidget)
        self.jobTabs.setTabText(tabIndex, u"Job {0} [ {1} ]".format(jobIndex, status))

    def closeJob(self, jobIndex):
        jobWidget = self.jobs[jobIndex]
        self.jobTabs.removeTab(self.jobTabs.indexOf(jobWidget))
        del self.jobs[jobIndex]

    def getParams(self):
        return {
            PARAM_DET_X: int(self.detectorWidthInput.value()),
            PARAM_DET_Y: int(self.detectorHeightInput.value()),
            PARAM_DET_OFFSET_X: float(self.detectorOffsetXInput.value()),
            PARAM_DET_OFFSET_Y: float(self.detectorOffsetYInput.value()),
            PARAM_SAM_LENGHT: float(self.sampleLengthInput.value()),
            PARAM_SAM_RADIUS: float(self.sampleRadiusInput.value()),
            PARAM_SIM_PHOTONS: int(self.simulationPhotonsInput.value()),
            PARAM_SIM_MAX_RUNNING_TIME: int(self.simulationRunningTimeInput.value()),
            PARAM_SIM_NODES: int(self.simulationNodesInput.value()),
            PARAM_SIM_PROCESSES: int(self.simulationProcessesInput.value()),
            PARAM_SIM_SDD: int(self.sampleSddhInput.value()),
        }


if __name__ == "__main__":
    app = QApplication(sys.argv)

    p = argparse.ArgumentParser()
    p.add_argument(u"--xmlConfig", default=u"./config.xml")
    args = p.parse_args()

    win = QMainWindow()
    win.setWindowTitle(u"AbsCor")
    widget = MainWidget(args.xmlConfig)
    win.setCentralWidget(widget)

    win.show()
    app.exec_()
