# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designUiFiles/mainDesign.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1011, 832)
        MainWindow.setMinimumSize(QtCore.QSize(703, 832))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabWidgetPage1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.taskTable = QtWidgets.QTableWidget(self.tabWidgetPage1)
        self.taskTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.taskTable.setObjectName("taskTable")
        self.taskTable.setColumnCount(0)
        self.taskTable.setRowCount(0)
        self.gridLayout_2.addWidget(self.taskTable, 1, 1, 1, 3)
        self.completedTaskTable = QtWidgets.QTableWidget(self.tabWidgetPage1)
        self.completedTaskTable.setMaximumSize(QtCore.QSize(16777215, 250))
        self.completedTaskTable.setObjectName("completedTaskTable")
        self.completedTaskTable.setColumnCount(0)
        self.completedTaskTable.setRowCount(0)
        self.gridLayout_2.addWidget(self.completedTaskTable, 2, 1, 1, 3)
        self.scrollArea = QtWidgets.QScrollArea(self.tabWidgetPage1)
        self.scrollArea.setMinimumSize(QtCore.QSize(200, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(200, 16777215))
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 198, 739))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.dateTaskFilter = QtWidgets.QDateEdit(self.scrollAreaWidgetContents)
        self.dateTaskFilter.setCalendarPopup(True)
        self.dateTaskFilter.setObjectName("dateTaskFilter")
        self.verticalLayout_3.addWidget(self.dateTaskFilter)
        self.addTaskButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.addTaskButton.setObjectName("addTaskButton")
        self.verticalLayout_3.addWidget(self.addTaskButton)
        self.copyTaskButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.copyTaskButton.setCheckable(True)
        self.copyTaskButton.setObjectName("copyTaskButton")
        self.verticalLayout_3.addWidget(self.copyTaskButton)
        self.editTaskButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.editTaskButton.setObjectName("editTaskButton")
        self.verticalLayout_3.addWidget(self.editTaskButton)
        self.deleteTaskButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.deleteTaskButton.setObjectName("deleteTaskButton")
        self.verticalLayout_3.addWidget(self.deleteTaskButton)
        self.resetDataButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.resetDataButton.setObjectName("resetDataButton")
        self.verticalLayout_3.addWidget(self.resetDataButton)
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.sortTaskTableOption = QtWidgets.QComboBox(self.groupBox)
        self.sortTaskTableOption.setObjectName("sortTaskTableOption")
        self.sortTaskTableOption.addItem("")
        self.sortTaskTableOption.addItem("")
        self.sortTaskTableOption.addItem("")
        self.sortTaskTableOption.addItem("")
        self.gridLayout_4.addWidget(self.sortTaskTableOption, 1, 0, 1, 1)
        self.reverseTaskTableSorting = QtWidgets.QCheckBox(self.groupBox)
        self.reverseTaskTableSorting.setObjectName("reverseTaskTableSorting")
        self.gridLayout_4.addWidget(self.reverseTaskTableSorting, 2, 0, 1, 1)
        self.sortTaskTableButton = QtWidgets.QPushButton(self.groupBox)
        self.sortTaskTableButton.setObjectName("sortTaskTableButton")
        self.gridLayout_4.addWidget(self.sortTaskTableButton, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.startTaskButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.startTaskButton.setObjectName("startTaskButton")
        self.verticalLayout_3.addWidget(self.startTaskButton)
        self.stopTaskButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.stopTaskButton.setObjectName("stopTaskButton")
        self.verticalLayout_3.addWidget(self.stopTaskButton)
        self.iFinishedItButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.iFinishedItButton.setObjectName("iFinishedItButton")
        self.verticalLayout_3.addWidget(self.iFinishedItButton)
        self.iCompletedButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.iCompletedButton.setObjectName("iCompletedButton")
        self.verticalLayout_3.addWidget(self.iCompletedButton)
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.elapsedProgressBar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.elapsedProgressBar.setProperty("value", 0)
        self.elapsedProgressBar.setTextVisible(True)
        self.elapsedProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.elapsedProgressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.elapsedProgressBar.setObjectName("elapsedProgressBar")
        self.verticalLayout_3.addWidget(self.elapsedProgressBar)
        self.remainingProgressBar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.remainingProgressBar.setProperty("value", 0)
        self.remainingProgressBar.setObjectName("remainingProgressBar")
        self.verticalLayout_3.addWidget(self.remainingProgressBar)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 2, 1)
        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QtWidgets.QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabWidgetPage2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.graphicWidget = QtWidgets.QWidget(self.tabWidgetPage2)
        self.graphicWidget.setMinimumSize(QtCore.QSize(0, 250))
        self.graphicWidget.setMaximumSize(QtCore.QSize(16777215, 250))
        self.graphicWidget.setObjectName("graphicWidget")
        self.gridLayout_3.addWidget(self.graphicWidget, 4, 4, 1, 7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.analysisTable = QtWidgets.QTableWidget(self.tabWidgetPage2)
        self.analysisTable.setObjectName("analysisTable")
        self.analysisTable.setColumnCount(0)
        self.analysisTable.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.analysisTable)
        self.taskDetailsTree = QtWidgets.QTreeWidget(self.tabWidgetPage2)
        self.taskDetailsTree.setMinimumSize(QtCore.QSize(500, 0))
        self.taskDetailsTree.setLineWidth(2)
        self.taskDetailsTree.setAnimated(True)
        self.taskDetailsTree.setWordWrap(True)
        self.taskDetailsTree.setHeaderHidden(True)
        self.taskDetailsTree.setObjectName("taskDetailsTree")
        self.horizontalLayout_2.addWidget(self.taskDetailsTree)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 3, 4, 1, 7)
        self.analysisView = QtWidgets.QComboBox(self.tabWidgetPage2)
        self.analysisView.setObjectName("analysisView")
        self.analysisView.addItem("")
        self.analysisView.addItem("")
        self.gridLayout_3.addWidget(self.analysisView, 2, 4, 1, 1)
        self.monthAnalysisFilter = QtWidgets.QComboBox(self.tabWidgetPage2)
        self.monthAnalysisFilter.setObjectName("monthAnalysisFilter")
        self.gridLayout_3.addWidget(self.monthAnalysisFilter, 2, 5, 1, 1)
        self.yearAnalysisFilter = QtWidgets.QComboBox(self.tabWidgetPage2)
        self.yearAnalysisFilter.setObjectName("yearAnalysisFilter")
        self.gridLayout_3.addWidget(self.yearAnalysisFilter, 2, 6, 1, 1)
        self.tabWidget.addTab(self.tabWidgetPage2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSaveAs)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreferences)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sunsite - Control Your Life Not Reacting"))
        self.dateTaskFilter.setDisplayFormat(_translate("MainWindow", "ddd MMMM dd yyyy"))
        self.addTaskButton.setText(_translate("MainWindow", "&Add Task"))
        self.copyTaskButton.setText(_translate("MainWindow", "&Copy Task"))
        self.editTaskButton.setText(_translate("MainWindow", "&Edit Task"))
        self.deleteTaskButton.setText(_translate("MainWindow", "&Delete Task"))
        self.deleteTaskButton.setShortcut(_translate("MainWindow", "Del"))
        self.resetDataButton.setText(_translate("MainWindow", "&Reset Database"))
        self.groupBox.setTitle(_translate("MainWindow", "Sort options"))
        self.sortTaskTableOption.setItemText(0, _translate("MainWindow", "Duration"))
        self.sortTaskTableOption.setItemText(1, _translate("MainWindow", "Elapsed Time"))
        self.sortTaskTableOption.setItemText(2, _translate("MainWindow", "Remaining Time"))
        self.sortTaskTableOption.setItemText(3, _translate("MainWindow", "Task Name"))
        self.reverseTaskTableSorting.setText(_translate("MainWindow", "Reverse Sorting"))
        self.sortTaskTableButton.setText(_translate("MainWindow", "Sort Table"))
        self.startTaskButton.setText(_translate("MainWindow", "&Start Doing Task"))
        self.startTaskButton.setShortcut(_translate("MainWindow", "Space"))
        self.stopTaskButton.setText(_translate("MainWindow", "S&top Doing Task"))
        self.stopTaskButton.setShortcut(_translate("MainWindow", "Space"))
        self.iFinishedItButton.setText(_translate("MainWindow", "I &Finished It"))
        self.iFinishedItButton.setShortcut(_translate("MainWindow", "Ctrl+Space"))
        self.iCompletedButton.setText(_translate("MainWindow", "&I Completed It Outside"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), _translate("MainWindow", "Task List"))
        self.taskDetailsTree.headerItem().setText(0, _translate("MainWindow", "Task Details"))
        self.analysisView.setItemText(0, _translate("MainWindow", "Monthly View"))
        self.analysisView.setItemText(1, _translate("MainWindow", "Yearly View"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), _translate("MainWindow", "Task Analysis"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSaveAs.setText(_translate("MainWindow", "Save As"))
        self.actionSaveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionPreferences.setShortcut(_translate("MainWindow", "Ctrl+P"))

