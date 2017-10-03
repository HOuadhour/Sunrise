# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designUiFiles/copyTasksDlg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_copyTasksDlg(object):
    def setupUi(self, copyTasksDlg):
        copyTasksDlg.setObjectName("copyTasksDlg")
        copyTasksDlg.resize(387, 462)
        copyTasksDlg.setMinimumSize(QtCore.QSize(387, 462))
        copyTasksDlg.setMaximumSize(QtCore.QSize(387, 462))
        self.gridLayout_3 = QtWidgets.QGridLayout(copyTasksDlg)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 4, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(copyTasksDlg)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_3.addWidget(self.progressBar, 3, 0, 1, 3)
        self.closeButton = QtWidgets.QPushButton(copyTasksDlg)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout_3.addWidget(self.closeButton, 4, 1, 1, 1)
        self.startCopyButton = QtWidgets.QPushButton(copyTasksDlg)
        self.startCopyButton.setObjectName("startCopyButton")
        self.gridLayout_3.addWidget(self.startCopyButton, 4, 2, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(copyTasksDlg)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.destinationDateList = QtWidgets.QListWidget(self.groupBox_2)
        self.destinationDateList.setObjectName("destinationDateList")
        self.gridLayout_2.addWidget(self.destinationDateList, 1, 0, 1, 2)
        self.addDateButton = QtWidgets.QPushButton(self.groupBox_2)
        self.addDateButton.setMinimumSize(QtCore.QSize(100, 0))
        self.addDateButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.addDateButton.setObjectName("addDateButton")
        self.gridLayout_2.addWidget(self.addDateButton, 0, 1, 1, 1)
        self.destinationDate = QtWidgets.QDateEdit(self.groupBox_2)
        self.destinationDate.setCalendarPopup(True)
        self.destinationDate.setObjectName("destinationDate")
        self.gridLayout_2.addWidget(self.destinationDate, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 3)
        self.groupBox = QtWidgets.QGroupBox(copyTasksDlg)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.sourceDate = QtWidgets.QLineEdit(self.groupBox)
        self.sourceDate.setReadOnly(True)
        self.sourceDate.setObjectName("sourceDate")
        self.gridLayout.addWidget(self.sourceDate, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 3)
        self.groupBox_3 = QtWidgets.QGroupBox(copyTasksDlg)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.overwriteCopy = QtWidgets.QRadioButton(self.groupBox_3)
        self.overwriteCopy.setObjectName("overwriteCopy")
        self.horizontalLayout.addWidget(self.overwriteCopy)
        self.skipCopy = QtWidgets.QRadioButton(self.groupBox_3)
        self.skipCopy.setChecked(True)
        self.skipCopy.setObjectName("skipCopy")
        self.horizontalLayout.addWidget(self.skipCopy)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_3, 2, 0, 1, 3)

        self.retranslateUi(copyTasksDlg)
        self.closeButton.clicked.connect(copyTasksDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(copyTasksDlg)

    def retranslateUi(self, copyTasksDlg):
        _translate = QtCore.QCoreApplication.translate
        copyTasksDlg.setWindowTitle(_translate("copyTasksDlg", "Copy Tasks"))
        self.closeButton.setText(_translate("copyTasksDlg", "&Close"))
        self.startCopyButton.setText(_translate("copyTasksDlg", "&Start"))
        self.groupBox_2.setTitle(_translate("copyTasksDlg", "Destination"))
        self.addDateButton.setText(_translate("copyTasksDlg", "&Add"))
        self.destinationDate.setDisplayFormat(_translate("copyTasksDlg", "ddd MMMM dd yyyy"))
        self.groupBox.setTitle(_translate("copyTasksDlg", "Source"))
        self.groupBox_3.setTitle(_translate("copyTasksDlg", "If Task Exists "))
        self.overwriteCopy.setText(_translate("copyTasksDlg", "Overwrite it"))
        self.skipCopy.setText(_translate("copyTasksDlg", "Skip it"))

