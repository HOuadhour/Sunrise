# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designUiFiles/resetDatabaseDlg.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_resetDatabaseDlg(object):
    def setupUi(self, resetDatabaseDlg):
        resetDatabaseDlg.setObjectName("resetDatabaseDlg")
        resetDatabaseDlg.resize(421, 287)
        self.gridLayout = QtWidgets.QGridLayout(resetDatabaseDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(resetDatabaseDlg)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 4)
        self.acceptingCondition = QtWidgets.QCheckBox(resetDatabaseDlg)
        self.acceptingCondition.setObjectName("acceptingCondition")
        self.gridLayout.addWidget(self.acceptingCondition, 1, 0, 1, 1)
        self.closeButton = QtWidgets.QPushButton(resetDatabaseDlg)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 1, 2, 1, 1)
        self.acceptButton = QtWidgets.QPushButton(resetDatabaseDlg)
        self.acceptButton.setDefault(True)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout.addWidget(self.acceptButton, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)

        self.retranslateUi(resetDatabaseDlg)
        self.closeButton.clicked.connect(resetDatabaseDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(resetDatabaseDlg)

    def retranslateUi(self, resetDatabaseDlg):
        _translate = QtCore.QCoreApplication.translate
        resetDatabaseDlg.setWindowTitle(_translate("resetDatabaseDlg", "Reset Database"))
        self.textBrowser.setHtml(_translate("resetDatabaseDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">By Accepting this you agree to:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">1) Delete all you tasks that belong to all the years, past or future.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">2) Delete all the tasks that shown as an autocomplete when you type a new task.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">3) Delete all the history details and your progress data including the charts.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ef2929;\">4) This process is irreversible, even if the autosave of the database is disabled, the database will be deleted.</span><span style=\" font-weight:600;\"><br /></span></p></body></html>"))
        self.acceptingCondition.setText(_translate("resetDatabaseDlg", "I read it and I accept"))
        self.closeButton.setText(_translate("resetDatabaseDlg", "&Close"))
        self.acceptButton.setText(_translate("resetDatabaseDlg", "&Accept"))

