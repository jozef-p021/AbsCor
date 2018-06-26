# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainTemplate.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1059, 571)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.detectorGroup = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detectorGroup.sizePolicy().hasHeightForWidth())
        self.detectorGroup.setSizePolicy(sizePolicy)
        self.detectorGroup.setMaximumSize(QtCore.QSize(500, 16777215))
        self.detectorGroup.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    margin-top: 0.5em;\n"
" font-weight:bold\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
" font-weight:bold;\n"
"background-color:#f6b442;\n"
"   \n"
"}"))
        self.detectorGroup.setObjectName(_fromUtf8("detectorGroup"))
        self.gridLayout_4 = QtGui.QGridLayout(self.detectorGroup)
        self.gridLayout_4.setContentsMargins(9, 13, 9, 9)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label = QtGui.QLabel(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 1)
        self.detectorPresetSelect = QtGui.QComboBox(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detectorPresetSelect.sizePolicy().hasHeightForWidth())
        self.detectorPresetSelect.setSizePolicy(sizePolicy)
        self.detectorPresetSelect.setObjectName(_fromUtf8("detectorPresetSelect"))
        self.gridLayout_4.addWidget(self.detectorPresetSelect, 1, 1, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.detectorWidthInput = QtGui.QSpinBox(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detectorWidthInput.sizePolicy().hasHeightForWidth())
        self.detectorWidthInput.setSizePolicy(sizePolicy)
        self.detectorWidthInput.setMaximum(999999999)
        self.detectorWidthInput.setObjectName(_fromUtf8("detectorWidthInput"))
        self.gridLayout_2.addWidget(self.detectorWidthInput, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)
        self.detectorHeightInput = QtGui.QSpinBox(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detectorHeightInput.sizePolicy().hasHeightForWidth())
        self.detectorHeightInput.setSizePolicy(sizePolicy)
        self.detectorHeightInput.setMaximum(999999999)
        self.detectorHeightInput.setObjectName(_fromUtf8("detectorHeightInput"))
        self.gridLayout_2.addWidget(self.detectorHeightInput, 0, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 1, 2, 1, 1)
        self.detectorOffsetXInput = QtGui.QDoubleSpinBox(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detectorOffsetXInput.sizePolicy().hasHeightForWidth())
        self.detectorOffsetXInput.setSizePolicy(sizePolicy)
        self.detectorOffsetXInput.setDecimals(3)
        self.detectorOffsetXInput.setMinimum(-999999999.0)
        self.detectorOffsetXInput.setMaximum(999999999.0)
        self.detectorOffsetXInput.setObjectName(_fromUtf8("detectorOffsetXInput"))
        self.gridLayout_2.addWidget(self.detectorOffsetXInput, 1, 1, 1, 1)
        self.detectorOffsetYInput = QtGui.QDoubleSpinBox(self.detectorGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detectorOffsetYInput.sizePolicy().hasHeightForWidth())
        self.detectorOffsetYInput.setSizePolicy(sizePolicy)
        self.detectorOffsetYInput.setDecimals(3)
        self.detectorOffsetYInput.setMinimum(-999999999.0)
        self.detectorOffsetYInput.setMaximum(999999999.0)
        self.detectorOffsetYInput.setObjectName(_fromUtf8("detectorOffsetYInput"))
        self.gridLayout_2.addWidget(self.detectorOffsetYInput, 1, 3, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.detectorGroup, 0, 0, 1, 1)
        self.simulationGroup = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.simulationGroup.sizePolicy().hasHeightForWidth())
        self.simulationGroup.setSizePolicy(sizePolicy)
        self.simulationGroup.setMaximumSize(QtCore.QSize(500, 16777215))
        self.simulationGroup.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    margin-top: 0.5em;\n"
" font-weight:bold\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
" font-weight:bold;\n"
"background-color:#f6b442;\n"
"   \n"
"}"))
        self.simulationGroup.setObjectName(_fromUtf8("simulationGroup"))
        self.gridLayout_6 = QtGui.QGridLayout(self.simulationGroup)
        self.gridLayout_6.setContentsMargins(9, 13, 9, 9)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_9 = QtGui.QLabel(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_6.addWidget(self.label_9, 0, 0, 1, 1)
        self.simulationPresetSelect = QtGui.QComboBox(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.simulationPresetSelect.sizePolicy().hasHeightForWidth())
        self.simulationPresetSelect.setSizePolicy(sizePolicy)
        self.simulationPresetSelect.setObjectName(_fromUtf8("simulationPresetSelect"))
        self.gridLayout_6.addWidget(self.simulationPresetSelect, 0, 1, 1, 1)
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.label_13 = QtGui.QLabel(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_7.addWidget(self.label_13, 1, 2, 1, 1)
        self.simulationNodesInput = QtGui.QSpinBox(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.simulationNodesInput.sizePolicy().hasHeightForWidth())
        self.simulationNodesInput.setSizePolicy(sizePolicy)
        self.simulationNodesInput.setSuffix(_fromUtf8(""))
        self.simulationNodesInput.setMinimum(1)
        self.simulationNodesInput.setObjectName(_fromUtf8("simulationNodesInput"))
        self.gridLayout_7.addWidget(self.simulationNodesInput, 1, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_7.addWidget(self.label_14, 1, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_7.addWidget(self.label_12, 0, 0, 1, 1)
        self.simulationPhotonsInput = QtGui.QSpinBox(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.simulationPhotonsInput.sizePolicy().hasHeightForWidth())
        self.simulationPhotonsInput.setSizePolicy(sizePolicy)
        self.simulationPhotonsInput.setSuffix(_fromUtf8(""))
        self.simulationPhotonsInput.setMaximum(999999999)
        self.simulationPhotonsInput.setProperty("value", 1000)
        self.simulationPhotonsInput.setObjectName(_fromUtf8("simulationPhotonsInput"))
        self.gridLayout_7.addWidget(self.simulationPhotonsInput, 0, 1, 1, 1)
        self.simulationProcessesInput = QtGui.QSpinBox(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.simulationProcessesInput.sizePolicy().hasHeightForWidth())
        self.simulationProcessesInput.setSizePolicy(sizePolicy)
        self.simulationProcessesInput.setSpecialValueText(_fromUtf8(""))
        self.simulationProcessesInput.setSuffix(_fromUtf8(""))
        self.simulationProcessesInput.setMinimum(2)
        self.simulationProcessesInput.setMaximum(999999999)
        self.simulationProcessesInput.setProperty("value", 2)
        self.simulationProcessesInput.setObjectName(_fromUtf8("simulationProcessesInput"))
        self.gridLayout_7.addWidget(self.simulationProcessesInput, 1, 3, 1, 1)
        self.label_15 = QtGui.QLabel(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_7.addWidget(self.label_15, 2, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_7.addWidget(self.label_11, 0, 2, 1, 1)
        self.sampleSddhInput = QtGui.QDoubleSpinBox(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleSddhInput.sizePolicy().hasHeightForWidth())
        self.sampleSddhInput.setSizePolicy(sizePolicy)
        self.sampleSddhInput.setDecimals(3)
        self.sampleSddhInput.setMaximum(999999999.0)
        self.sampleSddhInput.setObjectName(_fromUtf8("sampleSddhInput"))
        self.gridLayout_7.addWidget(self.sampleSddhInput, 0, 3, 1, 1)
        self.simulationRunningTimeInput = QtGui.QSpinBox(self.simulationGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.simulationRunningTimeInput.sizePolicy().hasHeightForWidth())
        self.simulationRunningTimeInput.setSizePolicy(sizePolicy)
        self.simulationRunningTimeInput.setMinimum(0)
        self.simulationRunningTimeInput.setMaximum(999999999)
        self.simulationRunningTimeInput.setProperty("value", 0)
        self.simulationRunningTimeInput.setObjectName(_fromUtf8("simulationRunningTimeInput"))
        self.gridLayout_7.addWidget(self.simulationRunningTimeInput, 2, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_7, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.simulationGroup, 2, 0, 3, 1)
        self.jobGroup = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobGroup.sizePolicy().hasHeightForWidth())
        self.jobGroup.setSizePolicy(sizePolicy)
        self.jobGroup.setMaximumSize(QtCore.QSize(500, 16777215))
        self.jobGroup.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    margin-top: 0.5em;\n"
" font-weight:bold\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
" font-weight:bold;\n"
"background-color:#f6b442;\n"
"   \n"
"}"))
        self.jobGroup.setObjectName(_fromUtf8("jobGroup"))
        self.gridLayout_9 = QtGui.QGridLayout(self.jobGroup)
        self.gridLayout_9.setContentsMargins(9, 13, 9, 9)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.startJobButton = QtGui.QPushButton(self.jobGroup)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startJobButton.setIcon(icon)
        self.startJobButton.setObjectName(_fromUtf8("startJobButton"))
        self.gridLayout_9.addWidget(self.startJobButton, 0, 4, 1, 1)
        self.jobMaxRadio = QtGui.QRadioButton(self.jobGroup)
        self.jobMaxRadio.setObjectName(_fromUtf8("jobMaxRadio"))
        self.gridLayout_9.addWidget(self.jobMaxRadio, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem, 0, 2, 1, 1)
        self.jobLocalRadio = QtGui.QRadioButton(self.jobGroup)
        self.jobLocalRadio.setChecked(True)
        self.jobLocalRadio.setObjectName(_fromUtf8("jobLocalRadio"))
        self.gridLayout_9.addWidget(self.jobLocalRadio, 0, 0, 1, 1)
        self.openEdfButton = QtGui.QPushButton(self.jobGroup)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/open-folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openEdfButton.setIcon(icon1)
        self.openEdfButton.setObjectName(_fromUtf8("openEdfButton"))
        self.gridLayout_9.addWidget(self.openEdfButton, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.jobGroup, 5, 0, 1, 1)
        self.currentJobGroup = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currentJobGroup.sizePolicy().hasHeightForWidth())
        self.currentJobGroup.setSizePolicy(sizePolicy)
        self.currentJobGroup.setMinimumSize(QtCore.QSize(552, 500))
        self.currentJobGroup.setSizeIncrement(QtCore.QSize(0, 0))
        self.currentJobGroup.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    margin-top: 0.5em;\n"
" font-weight:bold\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
" font-weight:bold;\n"
"background-color:#f6b442;\n"
"   \n"
"}"))
        self.currentJobGroup.setObjectName(_fromUtf8("currentJobGroup"))
        self.gridLayout_8 = QtGui.QGridLayout(self.currentJobGroup)
        self.gridLayout_8.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout_8.setContentsMargins(0, 13, 0, 0)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.jobTabs = QtGui.QTabWidget(self.currentJobGroup)
        self.jobTabs.setMinimumSize(QtCore.QSize(550, 0))
        self.jobTabs.setIconSize(QtCore.QSize(16, 16))
        self.jobTabs.setElideMode(QtCore.Qt.ElideNone)
        self.jobTabs.setTabsClosable(True)
        self.jobTabs.setMovable(True)
        self.jobTabs.setObjectName(_fromUtf8("jobTabs"))
        self.gridLayout_8.addWidget(self.jobTabs, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.currentJobGroup, 0, 1, 7, 1)
        spacerItem1 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        self.sampleGroup = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleGroup.sizePolicy().hasHeightForWidth())
        self.sampleGroup.setSizePolicy(sizePolicy)
        self.sampleGroup.setMaximumSize(QtCore.QSize(500, 16777215))
        self.sampleGroup.setStyleSheet(_fromUtf8("QGroupBox {\n"
"    border: 1px solid gray;\n"
"    margin-top: 0.5em;\n"
" font-weight:bold\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
" font-weight:bold;\n"
"background-color:#f6b442;\n"
"   \n"
"}"))
        self.sampleGroup.setObjectName(_fromUtf8("sampleGroup"))
        self.gridLayout_5 = QtGui.QGridLayout(self.sampleGroup)
        self.gridLayout_5.setContentsMargins(9, 13, 9, 9)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.sampleRadiusInput = QtGui.QDoubleSpinBox(self.sampleGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleRadiusInput.sizePolicy().hasHeightForWidth())
        self.sampleRadiusInput.setSizePolicy(sizePolicy)
        self.sampleRadiusInput.setDecimals(3)
        self.sampleRadiusInput.setMaximum(999999999.0)
        self.sampleRadiusInput.setObjectName(_fromUtf8("sampleRadiusInput"))
        self.gridLayout_3.addWidget(self.sampleRadiusInput, 0, 3, 1, 1)
        self.label_7 = QtGui.QLabel(self.sampleGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.sampleGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 0, 2, 1, 1)
        self.sampleLengthInput = QtGui.QDoubleSpinBox(self.sampleGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleLengthInput.sizePolicy().hasHeightForWidth())
        self.sampleLengthInput.setSizePolicy(sizePolicy)
        self.sampleLengthInput.setDecimals(3)
        self.sampleLengthInput.setMaximum(999999999.0)
        self.sampleLengthInput.setObjectName(_fromUtf8("sampleLengthInput"))
        self.gridLayout_3.addWidget(self.sampleLengthInput, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.sampleGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)
        self.sampleAbsorptionLengthInput = QtGui.QDoubleSpinBox(self.sampleGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleAbsorptionLengthInput.sizePolicy().hasHeightForWidth())
        self.sampleAbsorptionLengthInput.setSizePolicy(sizePolicy)
        self.sampleAbsorptionLengthInput.setDecimals(3)
        self.sampleAbsorptionLengthInput.setMaximum(999999999.0)
        self.sampleAbsorptionLengthInput.setObjectName(_fromUtf8("sampleAbsorptionLengthInput"))
        self.gridLayout_3.addWidget(self.sampleAbsorptionLengthInput, 1, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 2, 0, 1, 2)
        self.label_6 = QtGui.QLabel(self.sampleGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_5.addWidget(self.label_6, 1, 0, 1, 1)
        self.samplePresetSelect = QtGui.QComboBox(self.sampleGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.samplePresetSelect.sizePolicy().hasHeightForWidth())
        self.samplePresetSelect.setSizePolicy(sizePolicy)
        self.samplePresetSelect.setObjectName(_fromUtf8("samplePresetSelect"))
        self.gridLayout_5.addWidget(self.samplePresetSelect, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.sampleGroup, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.jobTabs.setCurrentIndex(-1)
        QtCore.QObject.connect(self.startJobButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.startJob)
        QtCore.QObject.connect(self.detectorPresetSelect, QtCore.SIGNAL(_fromUtf8("activated(int)")), Form.setDetectorPreset)
        QtCore.QObject.connect(self.samplePresetSelect, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), Form.setSamplePreset)
        QtCore.QObject.connect(self.simulationPresetSelect, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), Form.setSimulationPreset)
        QtCore.QObject.connect(self.jobLocalRadio, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), Form.setLocalJob)
        QtCore.QObject.connect(self.jobMaxRadio, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), Form.setRemoteJob)
        QtCore.QObject.connect(self.openEdfButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.loadEdfFile)
        QtCore.QObject.connect(self.jobTabs, QtCore.SIGNAL(_fromUtf8("tabCloseRequested(int)")), Form.tabCloseRequest)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.detectorPresetSelect, self.detectorWidthInput)
        Form.setTabOrder(self.detectorWidthInput, self.detectorHeightInput)
        Form.setTabOrder(self.detectorHeightInput, self.detectorOffsetXInput)
        Form.setTabOrder(self.detectorOffsetXInput, self.detectorOffsetYInput)
        Form.setTabOrder(self.detectorOffsetYInput, self.samplePresetSelect)
        Form.setTabOrder(self.samplePresetSelect, self.sampleLengthInput)
        Form.setTabOrder(self.sampleLengthInput, self.sampleRadiusInput)
        Form.setTabOrder(self.sampleRadiusInput, self.simulationPresetSelect)
        Form.setTabOrder(self.simulationPresetSelect, self.simulationPhotonsInput)
        Form.setTabOrder(self.simulationPhotonsInput, self.sampleSddhInput)
        Form.setTabOrder(self.sampleSddhInput, self.simulationNodesInput)
        Form.setTabOrder(self.simulationNodesInput, self.simulationProcessesInput)
        Form.setTabOrder(self.simulationProcessesInput, self.simulationRunningTimeInput)
        Form.setTabOrder(self.simulationRunningTimeInput, self.jobLocalRadio)
        Form.setTabOrder(self.jobLocalRadio, self.jobMaxRadio)
        Form.setTabOrder(self.jobMaxRadio, self.startJobButton)
        Form.setTabOrder(self.startJobButton, self.jobTabs)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.detectorGroup.setTitle(_translate("Form", "    Detector    ", None))
        self.label.setText(_translate("Form", "Preset:", None))
        self.label_2.setText(_translate("Form", "Width:", None))
        self.detectorWidthInput.setSuffix(_translate("Form", " px", None))
        self.label_3.setText(_translate("Form", "Height:", None))
        self.detectorHeightInput.setSuffix(_translate("Form", " px", None))
        self.label_4.setText(_translate("Form", "Offset X:", None))
        self.label_5.setText(_translate("Form", "Offset Y:", None))
        self.detectorOffsetXInput.setSuffix(_translate("Form", " mm", None))
        self.detectorOffsetYInput.setSuffix(_translate("Form", " mm", None))
        self.simulationGroup.setTitle(_translate("Form", "    Simulation    ", None))
        self.label_9.setText(_translate("Form", "Preset:", None))
        self.label_13.setText(_translate("Form", "Processes:", None))
        self.label_14.setText(_translate("Form", "Nodes:", None))
        self.label_12.setText(_translate("Form", "Photons:", None))
        self.label_15.setText(_translate("Form", "Max. runtime:", None))
        self.label_11.setText(_translate("Form", "SDD:", None))
        self.sampleSddhInput.setSuffix(_translate("Form", " mm", None))
        self.simulationRunningTimeInput.setSpecialValueText(_translate("Form", "No limit", None))
        self.simulationRunningTimeInput.setSuffix(_translate("Form", " min", None))
        self.jobGroup.setTitle(_translate("Form", "    Job    ", None))
        self.startJobButton.setToolTip(_translate("Form", "Start new job", None))
        self.startJobButton.setText(_translate("Form", "Start job", None))
        self.jobMaxRadio.setText(_translate("Form", "Remote", None))
        self.jobLocalRadio.setText(_translate("Form", "Local", None))
        self.openEdfButton.setToolTip(_translate("Form", "Open edf file from local disk", None))
        self.openEdfButton.setText(_translate("Form", "Open edf", None))
        self.currentJobGroup.setTitle(_translate("Form", "    Current jobs    ", None))
        self.sampleGroup.setTitle(_translate("Form", "    Sample    ", None))
        self.sampleRadiusInput.setSuffix(_translate("Form", " mm", None))
        self.label_7.setText(_translate("Form", "Length:", None))
        self.label_8.setText(_translate("Form", "Radius:", None))
        self.sampleLengthInput.setSuffix(_translate("Form", " mm", None))
        self.label_10.setText(_translate("Form", "Absorption length:", None))
        self.sampleAbsorptionLengthInput.setSuffix(_translate("Form", " mm", None))
        self.label_6.setText(_translate("Form", "Preset:", None))

import resources_rc
