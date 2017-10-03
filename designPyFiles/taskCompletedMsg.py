# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designUiFiles/taskCompletedMsg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_taskCompletedMsg(object):
    def setupUi(self, taskCompletedMsg):
        taskCompletedMsg.setObjectName("taskCompletedMsg")
        taskCompletedMsg.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(taskCompletedMsg)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(taskCompletedMsg)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.groupBox = QtWidgets.QGroupBox(taskCompletedMsg)
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(True)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.taskNotes = QtWidgets.QTextEdit(self.groupBox)
        self.taskNotes.setObjectName("taskNotes")
        self.gridLayout_2.addWidget(self.taskNotes, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 3)
        self.closeButton = QtWidgets.QPushButton(taskCompletedMsg)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 2, 1, 1, 2)

        self.retranslateUi(taskCompletedMsg)
        self.closeButton.clicked.connect(taskCompletedMsg.reject)
        QtCore.QMetaObject.connectSlotsByName(taskCompletedMsg)

    def retranslateUi(self, taskCompletedMsg):
        _translate = QtCore.QCoreApplication.translate
        taskCompletedMsg.setWindowTitle(_translate("taskCompletedMsg", "Task Notes"))
        self.label.setText(_translate("taskCompletedMsg", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Congratulations!</span></p><p align=\"center\">Your Task Has Been Completed Sucessfully</p></body></html>"))
        self.groupBox.setTitle(_translate("taskCompletedMsg", "Notes"))
        self.taskNotes.setPlaceholderText(_translate("taskCompletedMsg", "You can take some notes that belongs to your task."))
        self.closeButton.setText(_translate("taskCompletedMsg", "Close"))

