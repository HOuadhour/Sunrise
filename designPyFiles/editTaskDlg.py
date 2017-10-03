# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designUiFiles/editTaskDlg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_editTaskDlg(object):
    def setupUi(self, editTaskDlg):
        editTaskDlg.setObjectName("editTaskDlg")
        editTaskDlg.resize(410, 176)
        editTaskDlg.setMinimumSize(QtCore.QSize(410, 176))
        editTaskDlg.setMaximumSize(QtCore.QSize(410, 176))
        self.gridLayout = QtWidgets.QGridLayout(editTaskDlg)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.closeButton = QtWidgets.QPushButton(editTaskDlg)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 3, 2, 1, 1)
        self.durationEditedEntry = QtWidgets.QSpinBox(editTaskDlg)
        self.durationEditedEntry.setWrapping(True)
        self.durationEditedEntry.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.durationEditedEntry.setAccelerated(True)
        self.durationEditedEntry.setMinimum(1)
        self.durationEditedEntry.setMaximum(1440)
        self.durationEditedEntry.setProperty("value", 5)
        self.durationEditedEntry.setObjectName("durationEditedEntry")
        self.gridLayout.addWidget(self.durationEditedEntry, 1, 1, 1, 3)
        self.label_3 = QtWidgets.QLabel(editTaskDlg)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(editTaskDlg)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 2, 1, 1)
        self.noDurationButton = QtWidgets.QPushButton(editTaskDlg)
        self.noDurationButton.setCheckable(True)
        self.noDurationButton.setObjectName("noDurationButton")
        self.gridLayout.addWidget(self.noDurationButton, 1, 4, 1, 1)
        self.editTaskButton = QtWidgets.QPushButton(editTaskDlg)
        self.editTaskButton.setDefault(True)
        self.editTaskButton.setObjectName("editTaskButton")
        self.gridLayout.addWidget(self.editTaskButton, 3, 4, 1, 1)
        self.taskEditedEntry = QtWidgets.QLineEdit(editTaskDlg)
        self.taskEditedEntry.setObjectName("taskEditedEntry")
        self.gridLayout.addWidget(self.taskEditedEntry, 0, 1, 1, 4)

        self.retranslateUi(editTaskDlg)
        self.closeButton.clicked.connect(editTaskDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(editTaskDlg)
        editTaskDlg.setTabOrder(self.taskEditedEntry, self.durationEditedEntry)
        editTaskDlg.setTabOrder(self.durationEditedEntry, self.noDurationButton)
        editTaskDlg.setTabOrder(self.noDurationButton, self.editTaskButton)
        editTaskDlg.setTabOrder(self.editTaskButton, self.closeButton)

    def retranslateUi(self, editTaskDlg):
        _translate = QtCore.QCoreApplication.translate
        editTaskDlg.setWindowTitle(_translate("editTaskDlg", "Edit Task"))
        self.closeButton.setText(_translate("editTaskDlg", "&Close"))
        self.durationEditedEntry.setSuffix(_translate("editTaskDlg", " Minutes"))
        self.label_3.setText(_translate("editTaskDlg", "Duration"))
        self.label.setText(_translate("editTaskDlg", "Task"))
        self.noDurationButton.setText(_translate("editTaskDlg", "No Duration"))
        self.editTaskButton.setText(_translate("editTaskDlg", "&Edit"))

