# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jobTemplate.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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
        Form.resize(426, 207)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.jobPlotFrame = QtGui.QFrame(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobPlotFrame.sizePolicy().hasHeightForWidth())
        self.jobPlotFrame.setSizePolicy(sizePolicy)
        self.jobPlotFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.jobPlotFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.jobPlotFrame.setObjectName(_fromUtf8("jobPlotFrame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.jobPlotFrame)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout.addWidget(self.jobPlotFrame, 2, 0, 1, 2)
        self.jobProgressWidget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jobProgressWidget.sizePolicy().hasHeightForWidth())
        self.jobProgressWidget.setSizePolicy(sizePolicy)
        self.jobProgressWidget.setObjectName(_fromUtf8("jobProgressWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.jobProgressWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.progressBar = QtGui.QProgressBar(self.jobProgressWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 1, 1, 1, 1)
        self.cancelJobButton = QtGui.QPushButton(self.jobProgressWidget)
        self.cancelJobButton.setObjectName(_fromUtf8("cancelJobButton"))
        self.gridLayout_2.addWidget(self.cancelJobButton, 1, 2, 1, 1)
        self.label_10 = QtGui.QLabel(self.jobProgressWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.jobProgressWidget, 0, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.initTimeLabel = QtGui.QLabel(Form)
        self.initTimeLabel.setObjectName(_fromUtf8("initTimeLabel"))
        self.horizontalLayout.addWidget(self.initTimeLabel)
        self.label_6 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.endTimeLabel = QtGui.QLabel(Form)
        self.endTimeLabel.setObjectName(_fromUtf8("endTimeLabel"))
        self.horizontalLayout.addWidget(self.endTimeLabel)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.cancelJobButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.cancelJob)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.closeJob)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "Close job", None))
        self.cancelJobButton.setText(_translate("Form", "Cancel job", None))
        self.label_10.setText(_translate("Form", "Runtime:", None))
        self.label_2.setText(_translate("Form", "Init time:", None))
        self.initTimeLabel.setText(_translate("Form", "xxxx-xx-xx xx:xx:xx", None))
        self.label_6.setText(_translate("Form", "End time:", None))
        self.endTimeLabel.setText(_translate("Form", "xxxx-xx-xx xx:xx:xx", None))

