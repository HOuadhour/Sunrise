# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designUiFiles/taskCompletedDlg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_taskCompletedDlg(object):
    def setupUi(self, taskCompletedDlg):
        taskCompletedDlg.setObjectName("taskCompletedDlg")
        taskCompletedDlg.resize(399, 319)
        self.gridLayout = QtWidgets.QGridLayout(taskCompletedDlg)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.closeButton = QtWidgets.QPushButton(taskCompletedDlg)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 4, 2, 2, 2)
        self.label_2 = QtWidgets.QLabel(taskCompletedDlg)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        self.acceptButton = QtWidgets.QPushButton(taskCompletedDlg)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout.addWidget(self.acceptButton, 4, 4, 2, 1)
        self.label = QtWidgets.QLabel(taskCompletedDlg)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(taskCompletedDlg)
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(True)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.taskNotes = QtWidgets.QTextEdit(self.groupBox)
        self.taskNotes.setObjectName("taskNotes")
        self.gridLayout_2.addWidget(self.taskNotes, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 5)
        self.completeTime = QtWidgets.QTimeEdit(taskCompletedDlg)
        self.completeTime.setObjectName("completeTime")
        self.gridLayout.addWidget(self.completeTime, 1, 1, 1, 4)
        self.startTime = QtWidgets.QTimeEdit(taskCompletedDlg)
        self.startTime.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.startTime.setAccelerated(False)
        self.startTime.setObjectName("startTime")
        self.gridLayout.addWidget(self.startTime, 0, 1, 1, 4)

        self.retranslateUi(taskCompletedDlg)
        self.closeButton.clicked.connect(taskCompletedDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(taskCompletedDlg)

    def retranslateUi(self, taskCompletedDlg):
        _translate = QtCore.QCoreApplication.translate
        taskCompletedDlg.setWindowTitle(_translate("taskCompletedDlg", "Task Completed"))
        self.closeButton.setText(_translate("taskCompletedDlg", "&Close"))
        self.label_2.setText(_translate("taskCompletedDlg", "Complete Time"))
        self.acceptButton.setText(_translate("taskCompletedDlg", "&Accept"))
        self.label.setText(_translate("taskCompletedDlg", "Start Time"))
        self.groupBox.setTitle(_translate("taskCompletedDlg", "Notes"))
        self.taskNotes.setPlaceholderText(_translate("taskCompletedDlg", "You can take some notes that belongs to your task."))
        self.completeTime.setDisplayFormat(_translate("taskCompletedDlg", "HH:mm"))
        self.startTime.setDisplayFormat(_translate("taskCompletedDlg", "HH:mm"))

