#!/usr/bin/python3

# Email: HOuadhour@yandex.com
# Twitter: @HOuadhour
# LinkedIn: linkedin.com/in/HOuadhour
# Telegram: @HOuadhour

# The QtCore module contains the core non GUI functionality.  The QtGui
# contains classes for windowing system integration, event handling, 2D
# graphics, basic imaging, fonts and text.  The QtWidgets module contains
# classes that provide a set of UI elements to create classic desktop-style
# user interfaces.
# The QtCharts module provides a set of easy to use chart components.
from PyQt5 import QtWidgets, QtCore, QtGui, QtChart
# the mainDesign file converted from ui to py using pyuic5
import designPyFiles.mainDesign as gui
# the add task  dialog converted from ui to py using pyuic5
import designPyFiles.addTaskDlg as atd
# the prefrences dialog converted from ui to py using pyuic4
import designPyFiles.preferencesDlg as pd
# the reseting database dialog converted from ui to py using pyuic5
import designPyFiles.resetDatabaseDlg as rdd
# the edit task dialog converted from ui to py using pyuic5
import designPyFiles.editTaskDlg as etd
# the task completed message converted from ui to py using pyuic5
import designPyFiles.taskCompletedMsg as tcm
# the task completed dialog converted from ui to py using pyuic5
import designPyFiles.taskCompletedDlg as tcd
# the copy task dialog converted from ui to py using pyuic5
import designPyFiles.copyTasksDlg as ctd
import sys
import os
# To save objects as a file then load them to a variable
import pickle
from datetime import datetime, timedelta
import calendar


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWindow = gui.Ui_MainWindow()
        self.mainWindow.setupUi(self)
        self.mainWindow.retranslateUi(self)
        self.currentTaskIndex = 0

        # initiating other dialogs belonging to the main window

        # addTaskDlg
        self.addTaskDlg = QtWidgets.QDialog()
        self.addTaskDlg.ui = atd.Ui_addTaskDlg()
        self.addTaskDlg.ui.setupUi(self.addTaskDlg)
        self.addTaskDlg.setStyleSheet(open("style.css", "r").read())
        # editTaskDlg
        self.editTaskDlg = QtWidgets.QDialog()
        self.editTaskDlg.ui = etd.Ui_editTaskDlg()
        self.editTaskDlg.ui.setupUi(self.editTaskDlg)
        self.editTaskDlg.setStyleSheet(open("style.css", "r").read())
        # preferencesDlg
        self.preferencesDlg = QtWidgets.QDialog()
        self.preferencesDlg.ui = pd.Ui_preferencesDlg()
        self.preferencesDlg.ui.setupUi(self.preferencesDlg)
        self.preferencesDlg.setStyleSheet(open("style.css", "r").read())
        # resetDatabaseDlg
        self.resetDatabaseDlg = QtWidgets.QDialog()
        self.resetDatabaseDlg.ui = rdd.Ui_resetDatabaseDlg()
        self.resetDatabaseDlg.ui.setupUi(self.resetDatabaseDlg)
        self.resetDatabaseDlg.setStyleSheet(open("style.css", "r").read())
        # taskCompletedMsg
        self.taskCompletedMsg = QtWidgets.QDialog()
        self.taskCompletedMsg.ui = tcm.Ui_taskCompletedMsg()
        self.taskCompletedMsg.ui.setupUi(self.taskCompletedMsg)
        self.taskCompletedMsg.setStyleSheet(open("style.css", "r").read())
        # taskCompletedDlg
        self.taskCompletedDlg = QtWidgets.QDialog()
        self.taskCompletedDlg.ui = tcd.Ui_taskCompletedDlg()
        self.taskCompletedDlg.ui.setupUi(self.taskCompletedDlg)
        self.taskCompletedDlg.setStyleSheet(open("style.css", "r").read())
        # copyTasksDlg
        self.copyTasksDlg = QtWidgets.QDialog()
        self.copyTasksDlg.ui = ctd.Ui_copyTasksDlg()
        self.copyTasksDlg.ui.setupUi(self.copyTasksDlg)
        self.copyTasksDlg.setStyleSheet(open("style.css", "r").read())

        # setting the toolbar icons
        self.mainWindow.actionNew.setIcon(QtGui.QIcon("icons/toolbar/new.png"))
        self.mainWindow.actionOpen.setIcon(
            QtGui.QIcon("icons/toolbar/open.png"))
        self.mainWindow.actionSave.setIcon(
            QtGui.QIcon("icons/toolbar/save.png"))
        self.mainWindow.actionSaveAs.setIcon(
            QtGui.QIcon("icons/toolbar/save-as.png"))
        self.mainWindow.actionPreferences.setIcon(
            QtGui.QIcon("icons/toolbar/preferences.png"))
        self.mainWindow.actionQuit.setIcon(
            QtGui.QIcon("icons/toolbar/quit.png"))

        # setting the icon of the program
        self.setWindowIcon(QtGui.QIcon("icons/sunrise.svg"))
        self.addTaskDlg.setWindowIcon(QtGui.QIcon("icons/sunrise.svg"))
        self.editTaskDlg.setWindowIcon(QtGui.QIcon("icons/sunrise.svg"))
        self.copyTasksDlg.setWindowIcon(QtGui.QIcon("icons/sunrise.svg"))
        self.preferencesDlg.setWindowIcon(QtGui.QIcon("icons/sunrise.svg"))

        # declare our chart
        self.chart = QtChart.QChart()
        # hide the legend from the graphic
        self.chart.legend().hide()
        # set the margins to zero for all sides
        self.chart.setMargins(QtCore.QMargins(0, 0, 0, 0))
        # declare our chartView and improve the render view
        self.chartView = QtChart.QChartView(self.chart)
        self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        # create layout for the graphicWidget
        layout = QtWidgets.QVBoxLayout()
        # add the chart view to the layout
        layout.addWidget(self.chartView)
        # set the layout for the graphicWidget
        self.mainWindow.graphicWidget.setLayout(layout)

        # create our timer for getting the remaining time of our working task
        self.timer = QtCore.QTimer()
        # create the second timer to capture the time elapsed before the user
        # hit the delete task
        self.timer2 = QtCore.QTimer()
        # this timer will be update it every 1 second to calculate the
        # elapsedTime and the remainingTime of the task and we print the value
        # to the progressBar
        self.timer3 = QtCore.QTimer()

        # set the current and the minimum date to dateTaskFilter
        self.mainWindow.dateTaskFilter.setDate(QtCore.QDate.currentDate())
        self.mainWindow.dateTaskFilter.setMinimumDate(
            QtCore.QDate.currentDate())

        # Table Properties

        # Setting the default column numbers.
        self.mainWindow.taskTable.setColumnCount(4)
        self.mainWindow.completedTaskTable.setColumnCount(1)
        self.mainWindow.analysisTable.setColumnCount(6)
        # Setting the column header titles.
        self.mainWindow.taskTable.setHorizontalHeaderLabels(
            ["Duration", "Elapsed Time", "Remaining Time", "Task"])
        self.mainWindow.completedTaskTable.setHorizontalHeaderLabels(["Task"])
        self.mainWindow.analysisTable.setHorizontalHeaderLabels(
            ["Date", "Total Tasks", "UnCompleted Tasks", "Completed Tasks",
             "Deleted Tasks", "Average Score"])
        # set the columns width
        self.mainWindow.taskTable.setColumnWidth(0, 150)
        self.mainWindow.taskTable.setColumnWidth(1, 150)
        self.mainWindow.taskTable.setColumnWidth(2, 150)
        self.mainWindow.analysisTable.setColumnWidth(0, 170)
        self.mainWindow.analysisTable.setColumnWidth(1, 150)
        self.mainWindow.analysisTable.setColumnWidth(2, 150)
        self.mainWindow.analysisTable.setColumnWidth(3, 150)
        self.mainWindow.analysisTable.setColumnWidth(4, 150)
        # Set the selection mode and behavior to multiple or single rows at a
        # time and selecting rows instead of items.
        self.mainWindow.taskTable.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.mainWindow.taskTable.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        # Set the selection mode and behavior to single row at a time and
        # selecting rows instead of items.
        self.mainWindow.completedTaskTable.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.mainWindow.completedTaskTable.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        # set the selection mode and behavior to single item at a time and
        # selecting items not rows
        self.mainWindow.analysisTable.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.mainWindow.analysisTable.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems)
        # Try to adjust the table area to the contents
        self.mainWindow.taskTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.mainWindow.completedTaskTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.mainWindow.analysisTable.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        # set no edit key or double click to edit the contents of the table
        self.mainWindow.taskTable.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.mainWindow.completedTaskTable.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.mainWindow.analysisTable.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        # Setting the last column to stretch to the end of the table
        self.mainWindow.taskTable.horizontalHeader().\
            setStretchLastSection(True)
        self.mainWindow.completedTaskTable.horizontalHeader().\
            setStretchLastSection(True)
        self.mainWindow.analysisTable.horizontalHeader().\
            setStretchLastSection(True)
        # when resize a column resize the other one
        self.mainWindow.taskTable.horizontalHeader().\
            setCascadingSectionResizes(True)
        self.mainWindow.completedTaskTable.horizontalHeader().\
            setCascadingSectionResizes(True)
        self.mainWindow.analysisTable.horizontalHeader().\
            setCascadingSectionResizes(True)
        # align the header labes to be alligned to the left not the
        # center(default)
        self.mainWindow.taskTable.horizontalHeader().\
            setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.mainWindow.completedTaskTable.horizontalHeader().\
            setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.mainWindow.analysisTable.horizontalHeader().\
            setDefaultAlignment(QtCore.Qt.AlignLeft)
        # disable the save button by default
        self.mainWindow.actionSave.setEnabled(False)
        # disable the stop task button
        self.mainWindow.stopTaskButton.setEnabled(False)

        # SIGNALS

        # mainWindow Signals
        self.mainWindow.addTaskButton.clicked.connect(self.showAddTaskDlg)
        self.mainWindow.deleteTaskButton.clicked.connect(
            self.deleteTaskFunction)
        self.mainWindow.resetDataButton.clicked.connect(
            self.showResetDatabseDlg)
        self.mainWindow.taskTable.currentCellChanged.connect(
            self.changeButtonsStatus)
        self.mainWindow.dateTaskFilter.dateChanged.connect(
            self.updateTaskTable)
        self.mainWindow.editTaskButton.clicked.connect(
            self.showEditTaskDlg)
        self.mainWindow.startTaskButton.clicked.connect(
            self.startDoingTaskFunction)
        self.mainWindow.stopTaskButton.clicked.connect(
            self.stopDoingTaskFunction)
        self.mainWindow.taskTable.currentCellChanged.connect(
            self.changeButtonsStatus)
        self.timer.timeout.connect(self.taskCompletedFunction)
        self.mainWindow.analysisView.currentIndexChanged.connect(
            self.updateAnalysisTable)
        self.mainWindow.yearAnalysisFilter.currentIndexChanged.connect(
            self.updateAnalysisTable)
        self.mainWindow.monthAnalysisFilter.currentIndexChanged.connect(
            self.updateAnalysisTable)
        self.mainWindow.copyTaskButton.clicked.connect(
            self.showCopyTasksDlg)
        self.mainWindow.iCompletedButton.clicked.connect(
            self.showTaskCompletedDlg)
        self.mainWindow.analysisTable.currentCellChanged.connect(
            self.updateTaskDetails)
        self.mainWindow.sortTaskTableButton.clicked.connect(self.sortTaskTable)
        self.timer3.timeout.connect(self.updateProgressBar)
        self.mainWindow.iFinishedItButton.clicked.connect(
            self.taskCompletedFunction)
        self.mainWindow.taskTable.cellDoubleClicked.connect(
            self.showEditTaskDlg)
        self.mainWindow.completedTaskTable.cellDoubleClicked.connect(
            self.reviveTaskFunction)

        # toolbar Signals
        self.mainWindow.actionPreferences.triggered.connect(
            self.showPreferencesDlg)
        self.mainWindow.actionQuit.triggered.connect(self.close)
        self.mainWindow.actionSave.triggered.connect(self.saveDatabase)
        self.mainWindow.actionNew.triggered.connect(self.createNewDatabase)
        self.mainWindow.actionOpen.triggered.connect(self.openAnotherDatabase)
        self.mainWindow.actionSaveAs.triggered.connect(self.saveDatabaseCopy)

        # addTaskDlg Signals
        self.addTaskDlg.ui.addTaskButton.clicked.connect(self.addTaskFunction)
        self.addTaskDlg.ui.taskEntry.currentTextChanged.connect(
            self.updatePreviewFont)
        self.addTaskDlg.ui.taskEntry.currentTextChanged.connect(
            self.changeAddTaskButtonStatus)
        self.addTaskDlg.ui.fontName.currentFontChanged.connect(
            self.updatePreviewFont)
        self.addTaskDlg.ui.fontSize.valueChanged.connect(self.updatePreviewFont)
        self.addTaskDlg.ui.fontStyle.currentIndexChanged.connect(
            self.updatePreviewFont)
        self.addTaskDlg.ui.fontWeight.currentIndexChanged.connect(
            self.updatePreviewFont)
        self.addTaskDlg.ui.fontSetting.stateChanged.connect(
            self.saveLastFontSetting)
        self.addTaskDlg.ui.noDurationButton.toggled.connect(self.setNoDuration)

        # preferencesDlg Signals
        self.preferencesDlg.ui.resetCurrentDirectoryButton.clicked.connect(
            self.resetCurrentPathFunction)
        self.preferencesDlg.ui.browseButton.clicked.connect(
            self.changeCurrentPathDlg)
        self.preferencesDlg.ui.acceptButton.clicked.connect(
            self.acceptPreferencesDlgChanges)
        self.preferencesDlg.ui.selectedTable.currentIndexChanged.connect(
            self.setTableProperties)
        self.preferencesDlg.ui.applyButton.clicked.connect(
            self.acceptTableChanges)
        self.preferencesDlg.ui.changeButton1.clicked.connect(
            self.changeBgColor1)
        self.preferencesDlg.ui.changeButton2.clicked.connect(
            self.changeBgColor2)
        self.preferencesDlg.ui.changeButton3.clicked.connect(
            self.changeBgColor3)
        self.preferencesDlg.ui.changeButton4.clicked.connect(
            self.changeBgColor4)
        self.preferencesDlg.ui.changeButton5.clicked.connect(
            self.changeBgColor5)
        self.preferencesDlg.ui.changeButton6.clicked.connect(
            self.changeFgColor1)
        self.preferencesDlg.ui.changeButton7.clicked.connect(
            self.changeFgColor2)
        self.preferencesDlg.ui.changeButton8.clicked.connect(
            self.changeFgColor3)
        self.preferencesDlg.ui.changeButton9.clicked.connect
        (self.changeFgColor4)
        self.preferencesDlg.ui.changeButton10.clicked.connect(
            self.changeFgColor5)
        self.preferencesDlg.ui.bgRedNumber1.valueChanged.connect(
            self.setBgColorLabel1)
        self.preferencesDlg.ui.bgGreenNumber1.valueChanged.connect(
            self.setBgColorLabel1)
        self.preferencesDlg.ui.bgBlueNumber1.valueChanged.connect(
            self.setBgColorLabel1)
        self.preferencesDlg.ui.bgRedNumber2.valueChanged.connect(
            self.setBgColorLabel2)
        self.preferencesDlg.ui.bgGreenNumber2.valueChanged.connect(
            self.setBgColorLabel2)
        self.preferencesDlg.ui.bgBlueNumber2.valueChanged.connect(
            self.setBgColorLabel2)
        self.preferencesDlg.ui.bgRedNumber3.valueChanged.connect(
            self.setBgColorLabel3)
        self.preferencesDlg.ui.bgGreenNumber3.valueChanged.connect(
            self.setBgColorLabel3)
        self.preferencesDlg.ui.bgBlueNumber3.valueChanged.connect(
            self.setBgColorLabel3)
        self.preferencesDlg.ui.bgRedNumber4.valueChanged.connect(
            self.setBgColorLabel4)
        self.preferencesDlg.ui.bgGreenNumber4.valueChanged.connect(
            self.setBgColorLabel4)
        self.preferencesDlg.ui.bgBlueNumber4.valueChanged.connect(
            self.setBgColorLabel4)
        self.preferencesDlg.ui.bgRedNumber5.valueChanged.connect(
            self.setBgColorLabel5)
        self.preferencesDlg.ui.bgGreenNumber5.valueChanged.connect(
            self.setBgColorLabel5)
        self.preferencesDlg.ui.bgBlueNumber5.valueChanged.connect(
            self.setBgColorLabel5)
        self.preferencesDlg.ui.gLineRedNumber.valueChanged.connect(
            self.setGLineColorLabel)
        self.preferencesDlg.ui.gLineGreenNumber.valueChanged.connect(
            self.setGLineColorLabel)
        self.preferencesDlg.ui.gLineBlueNumber.valueChanged.connect(
            self.setGLineColorLabel)
        self.preferencesDlg.ui.changeGLineColor.clicked.connect(
            self.changeGLineColor)
        self.preferencesDlg.ui.cTitleRedNumber.valueChanged.connect(
            self.setCTitleColorLabel)
        self.preferencesDlg.ui.cTitleGreenNumber.valueChanged.connect(
            self.setCTitleColorLabel)
        self.preferencesDlg.ui.cTitleBlueNumber.valueChanged.connect(
            self.setCTitleColorLabel)
        self.preferencesDlg.ui.changeCTitleColor.clicked.connect(
            self.changeCTitleColor)
        self.preferencesDlg.ui.fgRedNumber1.valueChanged.connect(
            self.setFgColorLabel1)

        self.preferencesDlg.ui.fgGreenNumber1.valueChanged.connect(
            self.setFgColorLabel1)
        self.preferencesDlg.ui.fgBlueNumber1.valueChanged.connect(
            self.setFgColorLabel1)
        self.preferencesDlg.ui.fgRedNumber2.valueChanged.connect(
            self.setFgColorLabel2)
        self.preferencesDlg.ui.fgGreenNumber2.valueChanged.connect(
            self.setFgColorLabel2)
        self.preferencesDlg.ui.fgBlueNumber2.valueChanged.connect(
            self.setFgColorLabel2)
        self.preferencesDlg.ui.fgRedNumber3.valueChanged.connect(
            self.setFgColorLabel3)
        self.preferencesDlg.ui.fgGreenNumber3.valueChanged.connect(
            self.setFgColorLabel3)
        self.preferencesDlg.ui.fgBlueNumber3.valueChanged.connect(
            self.setFgColorLabel3)
        self.preferencesDlg.ui.fgRedNumber4.valueChanged.connect(
            self.setFgColorLabel4)
        self.preferencesDlg.ui.fgGreenNumber4.valueChanged.connect(
            self.setFgColorLabel4)
        self.preferencesDlg.ui.fgBlueNumber4.valueChanged.connect(
            self.setFgColorLabel4)
        self.preferencesDlg.ui.fgRedNumber5.valueChanged.connect(
            self.setFgColorLabel5)
        self.preferencesDlg.ui.fgGreenNumber5.valueChanged.connect(
            self.setFgColorLabel5)
        self.preferencesDlg.ui.fgBlueNumber5.valueChanged.connect(
            self.setFgColorLabel5)

        # resetDatabaseDlg Signals
        self.resetDatabaseDlg.ui.acceptingCondition.stateChanged.connect(
            self.acceptResetCondition)
        self.resetDatabaseDlg.ui.acceptButton.clicked.connect(
            self.resetDatabaseFunction)

        # editTaskDlg Signals
        self.editTaskDlg.ui.editTaskButton.clicked.connect(
            self.editTaskFunction)
        self.editTaskDlg.ui.noDurationButton.toggled.connect(self.setNoDuration)

        # copyTasksDlg Signals
        self.copyTasksDlg.ui.addDateButton.clicked.connect(
            self.addDestinationDate)
        self.copyTasksDlg.ui.startCopyButton.clicked.connect(
            self.startCopyTasks)

        # taskCompletedDlg Signals
        self.taskCompletedDlg.ui.startTime.timeChanged.connect(
            self.checkCompletedTime)
        self.taskCompletedDlg.ui.completeTime.timeChanged.connect(
            self.checkCompletedTime)
        self.taskCompletedDlg.ui.acceptButton.clicked.connect(
            self.taskCompletedOutside)

        # Initiate the Database and the configFile
        self.initiateDatabaseAndConf()
        # Check for the existance for the configFile and the database
        # save the current written variables or load the current file to the
        # variables configFile and database
        self.checkDatabaseAndConfig()
        # set the title of the mainWindow
        self.setWindowTitle("Sunrise - {}".format(self.currentPath))
        # check if we have years and months available as a keys or no
        # if not we create it
        today = datetime.today().strftime("%Y")
        if self.database["tasks"].get(today, -1) == -1:
            self.createTaskDaysData(datetime.today().strftime("%Y"), reset=True)
        # we call this function to set the filters of the analysisTable
        self.setAnalysisFilters()
        # set the monthAnalysisFilter to the current month
        self.mainWindow.monthAnalysisFilter.setCurrentText(
            datetime.today().strftime("%B"))
        # set the yearAnalysisFilter to the current year
        self.mainWindow.yearAnalysisFilter.setCurrentText(
            datetime.today().strftime("%Y"))
        # we call this function to show our Uncompleted tasks in the table
        self.updateTaskTable()
        # show/hide the completed task table
        self.mainWindow.completedTaskTable.setVisible(
            self.configFile["showCompletedTasks"])
        self.showHeaders()
        self.setTableGrid()
        self.setTableAlternatingRowC()
        self.mainWindow.remainingProgressBar.setVisible(False)
        self.mainWindow.elapsedProgressBar.setVisible(False)
        # disable/enable some buttons
        self.changeButtonsStatus()

    def reviveTaskFunction(self):
        # We call this function when the user double clicked a completedTask
        # this function will put the completed task again to the uncompleted
        # task so the user can add more time to it ...etc.

        row = self.mainWindow.completedTaskTable.currentRow()
        if row != -1:
            dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
            selectedTask = self.database["tasks"][yearFilter][monthFilter][
                dayFilter][1].pop(row)
            revivedTime = datetime.today()
            selectedTask.append(revivedTime)
            # the task has duration
            if selectedTask[1] != -1:
                selectedTask[12] = 1*60*1000
                # convert the duration from minute to ms
                selectedTask[13] = selectedTask[1]*60*1000
                # add 1 minute at least to the task
                selectedTask[1] += 1
            # change the remaining and elapsed Time
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0].\
                append(selectedTask)
            self.updateTaskTable()
            # check the autoSave option is True or no, True we save otherwise We
            # let the user press on the save button
            if self.autoSaveDatabase:
                # saving our database
                self.saveDatabase()
            else:
                # after we change something in the database we enable the save
                # button and add a star to the titlebar
                self.mainWindow.actionSave.setEnabled(True)
                self.setWindowTitle("Sunrise - {}*".format(self.currentPath))

    def updateProgressBar(self):
        # call this function every second after the user started a task

        row = self.mainWindow.taskTable.currentRow()
        if row != -1:
            dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
            # get the last started Time
            startedTime = self.database["tasks"][yearFilter][monthFilter][
                dayFilter][0][row][10][-1]
            oldElapsedTime = self.database["tasks"][yearFilter][monthFilter][
                dayFilter][0][row][13]//1000
            elapsedTime = (datetime.today() - startedTime).seconds
            remainingTime = self.timer.remainingTime()//1000
            # get the duration of the task and check if the task has duration or
            # not
            duration = self.database["tasks"][yearFilter][monthFilter][
                dayFilter][0][row][1]
            if duration != -1:
                elapsedTime += oldElapsedTime
            self.mainWindow.elapsedProgressBar.setFormat(
                "Elapsed Time is {:02d}:{:02d}:{:02d}".format(
                    elapsedTime//60//60, elapsedTime//60 % 60, elapsedTime % 60)
            )
            self.mainWindow.elapsedProgressBar.setValue(elapsedTime)
            self.mainWindow.remainingProgressBar.setFormat(
                "Remaining Time is {:02d}:{:02d}:{:02d}".format(
                    remainingTime//60//60,
                    remainingTime//60 % 60, remainingTime % 60))
            self.mainWindow.remainingProgressBar.setValue(remainingTime)

    def sortTaskTable(self):
        # when the user click the sort button we sort the taskTable depends on
        # the options

        # we need this function to sort depending on something we choose it
        from operator import itemgetter
        reverseSorting = self.mainWindow.reverseTaskTableSorting.isChecked()
        sortOption = self.mainWindow.sortTaskTableOption.currentText()
        day, month, year = self.getTaskDateFilter()
        if sortOption == "Duration":
            self.database["tasks"][year][month][day][0].sort(
                key=itemgetter(1), reverse=reverseSorting)
        if sortOption == "Elapsed Time":
            self.database["tasks"][year][month][day][0].sort(
                key=itemgetter(13), reverse=reverseSorting)
        if sortOption == "Remaining Time":
            self.database["tasks"][year][month][day][0].sort(
                key=itemgetter(12), reverse=reverseSorting)
        if sortOption == "Task Name":
            self.database["tasks"][year][month][day][0].sort(
                key=itemgetter(0), reverse=reverseSorting)
        self.updateTaskTable()
        # check the autoSave option is True or no, True we save otherwise We let
        # the user press on the save button
        if self.autoSaveDatabase:
            # saving our database
            self.saveDatabase()
        else:
            # after we change something in the database we enable the save
            # button and add a star to the titlebar
            self.mainWindow.actionSave.setEnabled(True)
            self.setWindowTitle("Sunrise - {}*".format(self.currentPath))

    def checkTaskStatus(self):
        # when we start a task that has no duration, and we stopped after a time
        # and we want to come back later but we didn't come back so this task
        # will stay at the uncompletedTask list so we have to move that task to
        # the completed one if 1 day passed without returning to the task

        # if the taskDay not exist yet so it will become equal to today
        today = datetime.today().strftime("%a %B %d %Y")
        taskDay = self.database.get("lastWorkingDay", datetime.today()
                                    ).strftime("%a %B %d %Y")
        # this means that the lastDayWorking it's not today and not a future day
        # of course so now we search for thet tasks and check the elapsed time
        if taskDay != today:
            month = taskDay.split()[1]
            year = taskDay.split()[3]
            taskIndex = []
            tasks = len(self.database["tasks"][year][month][taskDay][0])
            for task in range(tasks):
                # we need only the task that has no duration
                duration = self.database[
                    "tasks"][year][month][taskDay][0][task][1]
                if duration == -1:
                    # as long as you can't get point for less than 1 minute so
                    # we see if the task has 1 minute or more as an elapsedTime
                    # we convert the time from milliseconds to minutes
                    elapsedTime = self.database["tasks"][year][month][
                        taskDay][0][task][13]
                    if elapsedTime//1000//60 >= 1:
                        taskIndex.append(task)
            # if we start removing the task form the least to the greatest we
            # will get a problem so we will reverse the order of the taskIndex
            taskIndex.sort(reverse=True)
            for index in taskIndex:
                completedTask = self.database["tasks"][
                    year][month][taskDay][0].pop(index)
                # set the completedTime equal to the last stoppedTime
                completedTime = completedTask[11][-1]
                completedTask[2] = completedTime
                self.database["tasks"][year][month][taskDay][1].append(
                    completedTask)
            self.saveDatabase()

    def changeCTitleColor(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["chartTitleColor"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.cTitleRedNumber.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.cTitleGreenNumber.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.cTitleBlueNumber.setValue(color.getRgb()[2])

    def changeGLineColor(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["gLineColor"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.gLineRedNumber.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.gLineGreenNumber.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.gLineBlueNumber.setValue(color.getRgb()[2])

    def changeBgColor1(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["bgColor1"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.bgRedNumber1.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.bgGreenNumber1.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.bgBlueNumber1.setValue(color.getRgb()[2])

    def changeFgColor1(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["fgColor1"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.fgRedNumber1.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.fgGreenNumber1.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.fgBlueNumber1.setValue(color.getRgb()[2])

    def changeBgColor2(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["bgColor2"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.bgRedNumber2.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.bgGreenNumber2.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.bgBlueNumber2.setValue(color.getRgb()[2])

    def changeFgColor2(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["fgColor2"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.fgRedNumber2.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.fgGreenNumber2.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.fgBlueNumber2.setValue(color.getRgb()[2])

    def changeBgColor3(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["bgColor3"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.bgRedNumber3.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.bgGreenNumber3.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.bgBlueNumber3.setValue(color.getRgb()[2])

    def changeFgColor3(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["fgColor3"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.fgRedNumber3.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.fgGreenNumber3.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.fgBlueNumber3.setValue(color.getRgb()[2])

    def changeBgColor4(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["bgColor4"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.bgRedNumber4.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.bgGreenNumber4.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.bgBlueNumber4.setValue(color.getRgb()[2])

    def changeFgColor4(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["fgColor4"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.fgRedNumber4.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.fgGreenNumber4.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.fgBlueNumber4.setValue(color.getRgb()[2])

    def changeBgColor5(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["bgColor5"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.bgRedNumber5.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.bgGreenNumber5.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.bgBlueNumber5.setValue(color.getRgb()[2])

    def changeFgColor5(self):
        # everytime we click on the change button we execute this function to
        # change the color this function will open a color dialog to choose a
        # color from it

        initialColor = self.configFile["fgColor5"]
        color = QtWidgets.QColorDialog.getColor(
            initialColor, options=QtWidgets.QColorDialog.ColorDialogOption(
                QtWidgets.QColorDialog.DontUseNativeDialog))
        if color.isValid():
            self.preferencesDlg.ui.fgRedNumber5.setValue(color.getRgb()[0])
            self.preferencesDlg.ui.fgGreenNumber5.setValue(color.getRgb()[1])
            self.preferencesDlg.ui.fgBlueNumber5.setValue(color.getRgb()[2])

    def setCTitleColorLabel(self):
        # everytime we change the spinboxes of the gLinecolor we call this
        # function to update the gLineColorLabel

        red = self.preferencesDlg.ui.cTitleRedNumber.value()
        green = self.preferencesDlg.ui.cTitleGreenNumber.value()
        blue = self.preferencesDlg.ui.cTitleBlueNumber.value()
        self.preferencesDlg.ui.cTitleColorLabel.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setGLineColorLabel(self):
        # everytime we change the spinboxes of the gLinecolor we call this
        # function to update the gLineColorLabel

        red = self.preferencesDlg.ui.gLineRedNumber.value()
        green = self.preferencesDlg.ui.gLineGreenNumber.value()
        blue = self.preferencesDlg.ui.gLineBlueNumber.value()
        self.preferencesDlg.ui.gLineColorLabel.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setBgColorLabel1(self):
        # everytime we change the spinboxes of the background color1 we call
        # this function to update the background color label1

        red = self.preferencesDlg.ui.bgRedNumber1.value()
        green = self.preferencesDlg.ui.bgGreenNumber1.value()
        blue = self.preferencesDlg.ui.bgBlueNumber1.value()
        self.preferencesDlg.ui.bgColorLabel1.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setFgColorLabel1(self):
        # everytime we change the spinboxes of the foreground color1 we call
        # this function to update the foreground color label1

        red = self.preferencesDlg.ui.fgRedNumber1.value()
        green = self.preferencesDlg.ui.fgGreenNumber1.value()
        blue = self.preferencesDlg.ui.fgBlueNumber1.value()
        self.preferencesDlg.ui.fgColorLabel1.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setBgColorLabel2(self):
        # everytime we change the spinboxes of the background color2 we call
        # this function to update the background color label2

        red = self.preferencesDlg.ui.bgRedNumber2.value()
        green = self.preferencesDlg.ui.bgGreenNumber2.value()
        blue = self.preferencesDlg.ui.bgBlueNumber2.value()
        self.preferencesDlg.ui.bgColorLabel2.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setFgColorLabel2(self):
        # everytime we change the spinboxes of the foreground color2 we call
        # this function to update the foreground color label2

        red = self.preferencesDlg.ui.fgRedNumber2.value()
        green = self.preferencesDlg.ui.fgGreenNumber2.value()
        blue = self.preferencesDlg.ui.fgBlueNumber2.value()
        self.preferencesDlg.ui.fgColorLabel2.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setBgColorLabel3(self):
        # everytime we change the spinboxes of the background color3 we call
        # this function to update the background color label3

        red = self.preferencesDlg.ui.bgRedNumber3.value()
        green = self.preferencesDlg.ui.bgGreenNumber3.value()
        blue = self.preferencesDlg.ui.bgBlueNumber3.value()
        self.preferencesDlg.ui.bgColorLabel3.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setFgColorLabel3(self):
        # everytime we change the spinboxes of the foreground color3 we call
        # this function to update the foreground color label3

        red = self.preferencesDlg.ui.fgRedNumber3.value()
        green = self.preferencesDlg.ui.fgGreenNumber3.value()
        blue = self.preferencesDlg.ui.fgBlueNumber3.value()
        self.preferencesDlg.ui.fgColorLabel3.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setBgColorLabel4(self):
        # everytime we change the spinboxes of the background color4 we call
        # this function to update the background color label4

        red = self.preferencesDlg.ui.bgRedNumber4.value()
        green = self.preferencesDlg.ui.bgGreenNumber4.value()
        blue = self.preferencesDlg.ui.bgBlueNumber4.value()
        self.preferencesDlg.ui.bgColorLabel4.setStyleSheet("\
        QLabel{background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setFgColorLabel4(self):
        # everytime we change the spinboxes of the foreground color4 we call
        # this function to update the foreground color label4

        red = self.preferencesDlg.ui.fgRedNumber4.value()
        green = self.preferencesDlg.ui.fgGreenNumber4.value()
        blue = self.preferencesDlg.ui.fgBlueNumber4.value()
        self.preferencesDlg.ui.fgColorLabel4.setStyleSheet("\
        QLabel{ background-color: %s }" % QtGui.QColor(red, green, blue).name())

    def setBgColorLabel5(self):
        # everytime we change the spinboxes of the background color5 we call
        # this function to update the background color label5

        red = self.preferencesDlg.ui.bgRedNumber5.value()
        green = self.preferencesDlg.ui.bgGreenNumber5.value()
        blue = self.preferencesDlg.ui.bgBlueNumber5.value()
        self.preferencesDlg.ui.bgColorLabel5.setStyleSheet(
            "QLabel{ background-color: %s }" % QtGui.QColor(
                red, green, blue).name())

    def setFgColorLabel5(self):
        # everytime we change the spinboxes of the foreground color5 we call
        # this function to update the foreground color label5

        red = self.preferencesDlg.ui.fgRedNumber5.value()
        green = self.preferencesDlg.ui.fgGreenNumber5.value()
        blue = self.preferencesDlg.ui.fgBlueNumber5.value()
        self.preferencesDlg.ui.fgColorLabel5.setStyleSheet(
            "QLabel{ background-color: %s }" % QtGui.QColor(
                red, green, blue).name())

    def acceptTableChanges(self):
        # when the user click on the apply button
        # we save the table changes to the selected Table

        # get the current index of the selectedTable
        index = self.preferencesDlg.ui.selectedTable.currentIndex()
        # get the value of showing the grid table
        # to stop the line going over 80 characters we will use a temp variable
        temp = self.preferencesDlg.ui.showTableGrid.isChecked()
        self.configFile["showTableGrid"][index] = temp
        # get the value of the grid style
        temp = self.preferencesDlg.ui.tableGridStyle.currentText()
        self.configFile["tableGridStyle"][index] = temp
        # get the value of set alternating row colors
        temp = self.preferencesDlg.ui.tableAlternatingRowC.isChecked()
        self.configFile["alternatingRowColors"][index] = temp
        # get the value of show the horizontal and vertical headers
        temp = self.preferencesDlg.ui.showHorizontalHeaders.isChecked()
        self.configFile["showHorizontalHeaders"][index] = temp
        temp = self.preferencesDlg.ui.showVerticalHeaders.isChecked()
        self.configFile["showVerticalHeaders"][index] = temp
        # get the current status of use bold style on positive numbers
        temp = self.preferencesDlg.ui.useBoldAnalysisT.isChecked()
        self.configFile["useBoldAnalysisTable"] = temp
        self.saveConfigFile()
        self.setTableAlternatingRowC()
        self.setTableGrid()
        self.showHeaders()
        self.updateAnalysisTable()

    def setTableProperties(self):
        # when the user change the selected Table set the correct properties
        # according to the table

        # hide the use bold of positive numbers
        self.preferencesDlg.ui.useBoldAnalysisT.setVisible(False)
        # get the current index of the selectedTable
        index = self.preferencesDlg.ui.selectedTable.currentIndex()
        if index == 2:
            # unhide the use bold of positive numbers
            self.preferencesDlg.ui.useBoldAnalysisT.setVisible(True)
        # set the current value of show table grid
        self.preferencesDlg.ui.showTableGrid.setChecked(
            self.configFile["showTableGrid"][index])
        # set the current value of the grid style
        self.preferencesDlg.ui.tableGridStyle.setCurrentText(
            self.configFile["tableGridStyle"][index])
        # set the current value of show alternatic row colors
        self.preferencesDlg.ui.tableAlternatingRowC.setChecked(
            self.configFile["alternatingRowColors"][index])
        # set the current value of show the horizontal and vertical headers
        self.preferencesDlg.ui.showHorizontalHeaders.setChecked(
            self.configFile["showHorizontalHeaders"][index])
        self.preferencesDlg.ui.showVerticalHeaders.setChecked(
            self.configFile["showVerticalHeaders"][index])

    def addDestinationDate(self):
        # when the user select a date and click the add button
        # we exectue this function

        destinationDate = self.copyTasksDlg.ui.destinationDate.date()
        destinationDate = datetime(
            destinationDate.year(),
            destinationDate.month(),
            destinationDate.day()).strftime("%a %B %d %Y")
        if destinationDate not in self.destinationDateList:
            self.destinationDateList.append(destinationDate)
        self.copyTasksDlg.ui.destinationDateList.clear()
        self.copyTasksDlg.ui.destinationDateList.addItems(
            self.destinationDateList)

    def setAnalysisFilters(self):
        # Set the the months and years list of the analysis table

        # set the yearAnalysisFilter and the monthAnalysisFilter
        yearList = list(self.database["tasks"].keys())
        # remove the addedTasks from the list
        yearList.remove("addedTasks")
        monthList = list(self.database["tasks"]
                         [datetime.today().strftime("%Y")].keys())
        self.mainWindow.monthAnalysisFilter.clear()
        self.mainWindow.yearAnalysisFilter.clear()
        self.mainWindow.yearAnalysisFilter.addItems(yearList)
        self.mainWindow.monthAnalysisFilter.addItems(monthList)

    def setNoDuration(self):
        # when we check the no duraiton button we disable the duration spinbox
        # entry if we uncheck the button we activate the duration again

        # we have two button have the same objectName and same rules but in
        # different dialogs so we get the objectName of the parent (dialog) and
        # do our work
        sender = self.sender().parent().objectName()
        if sender == "addTaskDlg":
            if self.addTaskDlg.ui.noDurationButton.isChecked():
                self.addTaskDlg.ui.durationEntry.setEnabled(False)
            else:
                self.addTaskDlg.ui.durationEntry.setEnabled(True)
        elif sender == "editTaskDlg":
            if self.editTaskDlg.ui.noDurationButton.isChecked():
                self.editTaskDlg.ui.durationEditedEntry.setEnabled(False)
            else:
                self.editTaskDlg.ui.durationEditedEntry.setEnabled(True)

    def taskCompletedFunction(self):
        # We call this function when we complete a task either by timeout or a
        # task without duration

        self.mainWindow.startTaskButton.setEnabled(True)
        self.mainWindow.stopTaskButton.setEnabled(False)
        self.mainWindow.addTaskButton.setEnabled(True)
        self.mainWindow.editTaskButton.setEnabled(True)
        self.mainWindow.copyTaskButton.setEnabled(True)
        self.mainWindow.deleteTaskButton.setEnabled(True)
        self.mainWindow.resetDataButton.setEnabled(True)
        self.mainWindow.taskTable.setEnabled(True)
        self.mainWindow.toolBar.setEnabled(True)
        self.mainWindow.iCompletedButton.setEnabled(True)
        self.mainWindow.sortTaskTableButton.setEnabled(True)
        self.mainWindow.remainingProgressBar.setVisible(False)
        self.mainWindow.elapsedProgressBar.setVisible(False)
        self.showTaskCompletedMsg()
        taskNotes = self.taskCompletedMsg.ui.taskNotes.toPlainText()
        # I use variable to avoid E501 PEP8 Error (more than 80 characters line)
        temp = self.taskCompletedMsg.ui.groupBox.isChecked()
        if len(taskNotes) == 0 or not temp:
            taskNotes = "N/A"
        # stop the timer3
        self.timer.stop()  # general timer
        self.timer3.stop()  # progressBar timer
        row = self.mainWindow.taskTable.currentRow()
        dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
        # add the stoppedTime  and the completedTime of the task to the task
        # properties there is a difference between the stoppedTime when we press
        # the stop button and when the timer ends
        stoppedTime = datetime.today()
        if self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][1] == -1:
            startedTime = self.database["tasks"][yearFilter][monthFilter][
                dayFilter][0][row][10][-1]
            try:
                stoppedTime = self.database["tasks"][yearFilter][monthFilter][
                    dayFilter][0][row][11][-1]
                self.database["tasks"][yearFilter][monthFilter][dayFilter][
                    0][row][2] = stoppedTime  # completedTime
                # elapsedTime
                self.database["tasks"][yearFilter][monthFilter][dayFilter][
                    0][row][13] += (stoppedTime - startedTime).seconds * 1000
            except IndexError:
                self.database["tasks"][yearFilter][monthFilter][dayFilter][
                    0][row][2] = stoppedTime  # completedTime
                # elapsedTime
                self.database["tasks"][yearFilter][monthFilter][dayFilter][
                    0][row][13] += (stoppedTime - startedTime).seconds * 1000
        else:
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][2] = stoppedTime
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][13] = -1
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][14] = taskNotes
        # add the remaining and elapsed time to the task properties
        # as long as the task has been completed so we don't need a remaining
        # time anymore
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][12] = -1
        # remove the completed task from the Uncompleted tasks and add it to the
        # completedTask
        completedTask = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0].pop(row)
        self.database["tasks"][yearFilter][monthFilter][dayFilter][1].append(
            completedTask)
        if self.autoSaveDatabase:
            self.saveDatabase()
        else:
            # after we change something in the database we enable the save
            # button and add a star to the titlebar
            self.mainWindow.actionSave.setEnabled(True)
            self.setWindowTitle("Sunrise - {}*".format(self.currentPath))
        self.updateTaskTable()
        # set the focus to the table
        self.mainWindow.completedTaskTable.setFocus(True)
        # select the last completed task of the list
        totalTasks = len(self.database["tasks"]
                         [yearFilter][monthFilter][dayFilter][1])
        self.mainWindow.completedTaskTable.setCurrentCell(totalTasks-1, 0)

    def startDoingTaskFunction(self):
        # execute this function when the user select a task and choosed to start
        # doing the task disable the start task button and enable the stop task
        # button if the user starts a task can't start another one until he
        # stops the current working task the user can't delete, edit, add or
        # copy tasks while he starts doing tasks he can't even reset database or
        # interact with the table anymore also we disable the toolbar and
        # prevent the user from quiting the application while the task is
        # started it's time for working why wasting time on the program :)

        self.currentWorkingTask = self.mainWindow.taskTable.currentRow()
        self.mainWindow.startTaskButton.setEnabled(False)
        self.mainWindow.stopTaskButton.setEnabled(True)
        self.mainWindow.addTaskButton.setEnabled(False)
        self.mainWindow.editTaskButton.setEnabled(False)
        self.mainWindow.copyTaskButton.setEnabled(False)
        self.mainWindow.deleteTaskButton.setEnabled(False)
        self.mainWindow.resetDataButton.setEnabled(False)
        self.mainWindow.taskTable.setEnabled(False)
        self.mainWindow.toolBar.setEnabled(False)
        self.mainWindow.iCompletedButton.setEnabled(False)
        self.mainWindow.sortTaskTableButton.setEnabled(False)
        self.mainWindow.elapsedProgressBar.setVisible(True)
        self.mainWindow.remainingProgressBar.setVisible(True)
        row = self.mainWindow.taskTable.currentRow()
        dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
        self.currentTaskIndex = row
        startedTime = datetime.today()
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][10].append(startedTime)
        # get the remaining time in ms
        remainingTime = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][12]
        # check if the task has a duration or not
        duration = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][1]
        # if this condition is True, that means this task has no duration so we
        # start the timer with the remaining time until tomorrow converted to
        # ms
        if duration == -1:
            tomorrow = (datetime.today()+timedelta(days=1))
            tomorrow = tomorrow.replace(
                hour=0, minute=0, second=0, microsecond=0)
            # may be you ask why we multiply it by 1000 then we divided, because
            # we need the value in ms for the timer
            remainingTime = (tomorrow-startedTime).seconds*1000
            self.mainWindow.elapsedProgressBar.setMaximum(remainingTime//1000)
            self.mainWindow.remainingProgressBar.setMaximum(remainingTime//1000)
            # activate the I Finished It  button only for the unlimited task
            self.mainWindow.iFinishedItButton.setVisible(True)
        else:
            self.mainWindow.elapsedProgressBar.setMaximum(duration*60)
            self.mainWindow.remainingProgressBar.setMaximum(duration*60)
            self.mainWindow.iFinishedItButton.setVisible(False)
        # start our timer and set it to run only once
        self.timer.setSingleShot(True)
        self.timer.start(remainingTime)
        self.timer3.start(1000)
        self.saveDatabase()

    def stopDoingTaskFunction(self):
        # execute this function when the user choose to stop doing a task
        # enable the start task button
        # disable the stop task button
        # reEnable the add, copy, edit, delete  and reset database buttons
        # reEnable the taskTable and the toolbar

        self.mainWindow.startTaskButton.setEnabled(True)
        self.mainWindow.stopTaskButton.setEnabled(False)
        self.mainWindow.addTaskButton.setEnabled(True)
        self.mainWindow.editTaskButton.setEnabled(True)
        self.mainWindow.copyTaskButton.setEnabled(True)
        self.mainWindow.deleteTaskButton.setEnabled(True)
        self.mainWindow.resetDataButton.setEnabled(True)
        self.mainWindow.taskTable.setEnabled(True)
        self.mainWindow.toolBar.setEnabled(True)
        self.mainWindow.iCompletedButton.setEnabled(True)
        self.mainWindow.sortTaskTableButton.setEnabled(True)
        self.mainWindow.remainingProgressBar.setVisible(False)
        self.mainWindow.elapsedProgressBar.setVisible(False)
        # stop the timers
        # general timer for counting the elapsedTime and remainingTime for the
        # task
        self.timer.stop()
        # timer to count the elapsedTime and remainingTime for the progressBar
        self.timer3.stop()
        row = self.mainWindow.taskTable.currentRow()
        dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
        # get the duration of the task by default in minutes so we convert later
        # to ms
        duration = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][1]
        # add the stoppedTime of the task to the task properties
        stoppedTime = datetime.today()

        # add the current day to database["lastWorkingDay"]
        self.database["lastWorkingDay"] = stoppedTime
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][11].append(stoppedTime)
        oldElapsedTime = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][13]
        startedTime = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][10][-1]
        # get the elapsed time in milliseconds
        elapsedTime = (stoppedTime - startedTime).seconds*1000
        # create the remainingTime variable
        remainingTime = -1
        # check if the task has a duration or no
        if duration != -1:
            # calculate the remaining time, the origin duration - the elapsed
            remainingTime = (duration*60*1000) - (elapsedTime+oldElapsedTime)
            # note we add the elapsed time to the previous one only if it's a
            # task without duration
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][13] += elapsedTime
        else:
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][13] += elapsedTime
        # add the remaining and elapsed time to the task properties
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][12] = remainingTime
        if self.autoSaveDatabase:
            self.saveDatabase()
        else:
            # after we change something in the database we enable the save
            # button and add a star to the titlebar
            self.mainWindow.actionSave.setEnabled(True)
            self.setWindowTitle("Sunrise - {}*".format(self.currentPath))
        self.updateTaskTable()

    def getTaskDateFilter(self):
        # get the dateTaskFilter and return 3 values
        # dayFilter, monthFilter, yearFilter

        # get the dateTaskFilter and convert it to a datetime object
        dateTaskFilter = self.mainWindow.dateTaskFilter.date()
        dateTaskFilter = datetime(
            dateTaskFilter.year(),
            dateTaskFilter.month(),
            dateTaskFilter.day())
        # format the datetime object to a string
        dayFilter = dateTaskFilter.strftime("%a %B %d %Y")
        monthFilter = dateTaskFilter.strftime("%B")
        yearFilter = dateTaskFilter.strftime("%Y")
        return dayFilter, monthFilter, yearFilter

    def outputTaskDetails(self):
        # Show the created, modified datetime

        try:
            # get the current row number
            row = self.mainWindow.taskTable.currentRow()
            dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
            # get the created time, saved as a datetime object
            createdTime = self.database["tasks"][yearFilter][monthFilter][
                dayFilter][0][row][7].strftime("%m/%d/%Y %H:%M:%S")
            # get the modified time, saved as a datetime object
            modifiedTime = self.database["tasks"][yearFilter][monthFilter][
                dayFilter][0][row][8].strftime("%m/%d/%Y %H:%M:%S")
            self.mainWindow.creationDateLabel.setText(createdTime)
            self.mainWindow.modificationDateLabel.setText(modifiedTime)
        except IndexError:
            # after deleting tasks or changing the dateFilter to none tasks we
            # delete the labels
            self.mainWindow.creationDateLabel.clear()
            self.mainWindow.modificationDateLabel.clear()

    def showHeaders(self):
        # When the user select to show or to hide the horizontal and vertical
        # headers we call this function

        self.mainWindow.taskTable.verticalHeader().setVisible(
            self.configFile["showVerticalHeaders"][0])
        self.mainWindow.completedTaskTable.verticalHeader().setVisible(
            self.configFile["showVerticalHeaders"][1])
        self.mainWindow.analysisTable.verticalHeader().setVisible(
            self.configFile["showVerticalHeaders"][2])
        self.mainWindow.taskTable.horizontalHeader().setVisible(
            self.configFile["showHorizontalHeaders"][0])
        self.mainWindow.completedTaskTable.horizontalHeader().setVisible(
            self.configFile["showHorizontalHeaders"][1])
        self.mainWindow.analysisTable.horizontalHeader().setVisible(
            self.configFile["showHorizontalHeaders"][2])

    def setTableAlternatingRowC(self):
        # when user checked the alternating row color the table will alternating
        # row colors

        self.mainWindow.taskTable.setAlternatingRowColors(
            self.configFile["alternatingRowColors"][0])
        self.mainWindow.completedTaskTable.setAlternatingRowColors(
            self.configFile["alternatingRowColors"][1])
        self.mainWindow.analysisTable.setAlternatingRowColors(
            self.configFile["alternatingRowColors"][2])

    def setTableGrid(self):
        # every time we check or uncheck show table's grid, we call this
        # function

        self.mainWindow.taskTable.setShowGrid(
            self.configFile["showTableGrid"][0])
        self.mainWindow.completedTaskTable.setShowGrid(
            self.configFile["showTableGrid"][1])
        self.mainWindow.analysisTable.setShowGrid(
            self.configFile["showTableGrid"][2])
        self.mainWindow.taskTable.setGridStyle(
            self.configFile["tableGridStyles"]
            [self.configFile["tableGridStyle"][0]])
        self.mainWindow.completedTaskTable.setGridStyle(
            self.configFile["tableGridStyles"]
            [self.configFile["tableGridStyle"][1]])
        self.mainWindow.analysisTable.setGridStyle(
            self.configFile["tableGridStyles"]
            [self.configFile["tableGridStyle"][2]])

    def acceptResetCondition(self):
        # Change the status of the accept button to enabled so the user can
        # accept and reset the database

        if self.resetDatabaseDlg.ui.acceptingCondition.isChecked():
            self.resetDatabaseDlg.ui.acceptButton.setEnabled(True)
        else:
            self.resetDatabaseDlg.ui.acceptButton.setEnabled(False)

    def openAnotherDatabase(self):
        # if the user has pressed the Open button or Ctrl+O
        # a new database will be opened and loaded
        # change the currentPath but without saving it

        path = QtWidgets.QFileDialog.getOpenFileName(
            self.preferencesDlg, "Open another database",
            directory=self.currentPath,
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if path[0]:
            # change current path to the new database path
            self.currentPath = path[0]
            self.setWindowTitle("Sunrise - {}".format(self.currentPath))
            # load the database
            self.loadDatabase()
            # update the tasktable
            self.updateTaskTable()

    def createNewDatabase(self):
        # if the user has pressed the New button or Ctrl+N
        # a new database will be created
        # with the chosen path and name

        path = QtWidgets.QFileDialog.getSaveFileName(
            self.preferencesDlg,
            "Create a new file",
            directory=self.currentPath,
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if path[0]:
            # change current path to the new database path
            self.currentPath = path[0]
            # create a new database
            self.createTaskDaysData(datetime.today().strftime("%Y"), reset=True)
            # save the database file
            self.saveDatabase()
            # load the database
            self.loadDatabase()
            # update the tasktable
            self.updateTaskTable()

    def saveDatabaseCopy(self):
        # if the user has pressed the New button or Ctrl+Shit+S
        # a copy of the current database will be created
        # with the chosen path and name

        path = QtWidgets.QFileDialog.getSaveFileName(
            self.preferencesDlg,
            "Create a new file",
            directory=self.currentPath,
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if path[0]:
            # change current path to the new database path
            self.currentPath = path[0]
            # save the database file
            self.saveDatabase()
            # load the database
            self.loadDatabase()
            # update the tasktable
            self.updateTaskTable()

    def changeAddTaskButtonStatus(self):
        # change the status of the addTaskButton of addTaskDlg
        # if no task the button will be disabled

        if self.addTaskDlg.ui.taskEntry.currentText():
            self.addTaskDlg.ui.addTaskButton.setEnabled(True)
        else:
            self.addTaskDlg.ui.addTaskButton.setEnabled(False)

    def changeButtonsStatus(self):
        # we call this function to enable the delete and edit buttons if the
        # current row of the table has been changed

        row = self.mainWindow.taskTable.currentRow()
        today = datetime.today().strftime("%a %B %d %Y")
        taskDay, month, year = self.getTaskDateFilter()
        if row != -1:
            # get duration of the task and show/hide the I Finished It Button
            duration = self.database["tasks"][year][month][taskDay][0][row][1]
            startedTime = self.database["tasks"][year][month][taskDay][0][
                row][10]
            self.mainWindow.editTaskButton.setEnabled(True)
            self.mainWindow.deleteTaskButton.setEnabled(True)
            self.mainWindow.copyTaskButton.setEnabled(True)
            if duration == -1 and len(startedTime) > 0:
                self.mainWindow.iFinishedItButton.setVisible(True)
            else:
                self.mainWindow.iFinishedItButton.setVisible(False)
            if today == taskDay:
                self.mainWindow.startTaskButton.setEnabled(True)
                self.mainWindow.iCompletedButton.setEnabled(True)
            else:
                self.mainWindow.startTaskButton.setEnabled(False)
                self.mainWindow.iCompletedButton.setEnabled(False)
        else:
            self.mainWindow.deleteTaskButton.setEnabled(False)
            self.mainWindow.editTaskButton.setEnabled(False)
            self.mainWindow.copyTaskButton.setEnabled(False)
            self.mainWindow.startTaskButton.setEnabled(False)
            self.mainWindow.iCompletedButton.setEnabled(False)
            self.mainWindow.iFinishedItButton.setVisible(False)

    def checkDatabaseAndConfig(self):

        # we call this function to check if we have a saved database and a
        # configFile or no if yes we load it and overwrite the current one or we
        # save ours to a new file

        # checking for the configFile existance
        if os.path.exists(self.defaultConfigPath):
            self.loadConfigFile()  # load the configFile
            # get the default path of the configFile
            self.defaultConfigPath = self.configFile["defaultConfigPath"]
            # get the current path of the database
            self.currentPath = self.configFile["currentPath"]
            # get the autoSave option of the database
            self.autoSaveDatabase = self.configFile["autoSaveDatabase"]
            # checking for the database existance
            if os.path.exists(self.currentPath):
                self.loadDatabase()  # load the database
            else:
                # we extract the directory from the full path
                # and we create the directory even if some directory is exist
                os.makedirs(os.path.dirname(self.currentPath), exist_ok=True)
                self.saveDatabase()  # Save the current database to a file
        else:
            os.makedirs(os.path.dirname(self.defaultConfigPath), exist_ok=True)
            os.makedirs(os.path.dirname(self.currentPath), exist_ok=True)
            self.saveConfigFile()  # Save the current configFile to a file
            self.saveDatabase()  # save the current database to a file

    def createTaskDaysData(self, year, reset=False):
        # get months list and add it to the database file
        # reset variable for reseting the database or initiating the file for
        # the first time

        if reset:
            # reset the database by creating the dictionary from the beginning
            self.database["tasks"] = {year: {}}
            # we create a set to save all the tasks added,
            # and when the user is typing a text he will get an autocompletion
            # from this list, we choose set to prevent duplicate tasks.
            self.database["tasks"]["addedTasks"] = set()
        else:
            self.database["tasks"][year] = {}
        for month in range(1, 13):
            # current month on text format
            cMonth = datetime(int(year), month, 1).strftime("%B")
            self.database["tasks"][year][cMonth] = {}
        # Get dates of every month and add it to the self.database file
        c = calendar.TextCalendar()
        # we iterate from 1 to 12 (month numbers) create out iterable object
        # that contains our dates that belongs to this month
        for month in range(1, 13):
            days = c.itermonthdates(int(year), month)
            for day in days:
                # the result will contain some other days that belongs to other
                # months, so we filter the result to our month only.
                if day.month == month:
                    self.database["tasks"][year][
                        day.strftime("%B")][
                        day.strftime("%a %B %d %Y")] = [[], [], []]
        # after we change something in the database we enable the save button
        # and add a star to the titlebar
        self.mainWindow.actionSave.setEnabled(True)
        self.setWindowTitle("Sunrise - {}*".format(self.currentPath))
        if self.autoSaveDatabase:
            self.saveDatabase()

    def saveDatabase(self):
        # Save the file as object for example lists, dicts etc ... (Not saving
        # as a text).

        with open(self.currentPath, "wb") as data:
            myFile = pickle.Pickler(data)
            myFile.dump(self.database)
        # after saving the database file
        # we have to restore the titlebar text and disable the save button again
        self.mainWindow.actionSave.setEnabled(False)
        self.setWindowTitle("Sunrise - {}".format(self.currentPath))

    def loadDatabase(self):
        # Load the file as object to the variable without the need to use the
        # open() method or read() ...etc

        try:
            with open(self.currentPath, "rb") as data:
                myFile = pickle.Unpickler(data)
                self.database = myFile.load()
        # prevent crashing the program when the user try to open a bad file
        except pickle.UnpicklingError:
            QtWidgets.QMessageBox.warning(self, "Warning Message", "Please \
                select a legitimate database file, \
                that has been created with this program.")
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Warning Message", "Please \
                select a legitimate database file, \
                that has been created with this program.")

    def saveConfigFile(self):
        # Save the file as object for example lists, dicts etc ... (Not saving
        # as a text).

        with open(self.defaultConfigPath, "wb") as data:
            myFile = pickle.Pickler(data)
            myFile.dump(self.configFile)

    def loadConfigFile(self):
        # Load the file as object to the variable without the need to use the
        # open() method or read() ...etc

        with open(self.defaultConfigPath, "rb") as data:
            myFile = pickle.Unpickler(data)
            self.configFile = myFile.load()

    def updateTaskAdded(self):
        # We add every task added before to the dropdown list as an autocomplete
        # for the taskEntry

        self.addTaskDlg.ui.taskEntry.clear()
        # check for addedTasks if it's there or no
        if self.database["tasks"].get("addedTasks", -1) != -1:
            for task in self.database["tasks"]["addedTasks"]:
                self.addTaskDlg.ui.taskEntry.addItem(task)
        # add the key addedTasks to the database
        else:
            self.database["tasks"]["addedTasks"] = set()
        self.addTaskDlg.ui.taskEntry.setCurrentText("")

    def saveLastFontSetting(self):
        # every time we create a task we save the font setting, if the user has
        # checked the CheckBox or we call this function every time the state of
        # the checkbox is changing

        if self.addTaskDlg.ui.fontSetting.isChecked():
            fontFamily = self.addTaskDlg.ui.fontName.currentFont().family()
            fontSize = self.addTaskDlg.ui.fontSize.value()
            fontStyle = self.addTaskDlg.ui.fontStyle.currentText()
            fontWeight = self.addTaskDlg.ui.fontWeight.currentText()
            self.configFile["lastFontSetting"] = (
                fontFamily,
                fontSize,
                fontStyle,
                fontWeight,
                True)  # True to save the state of the checkBox
        else:
            self.configFile["lastFontSetting"] = (
                "Ubuntu", 10, "Normal", "Normal", False)
        self.saveConfigFile()

    def updatePreviewFont(self):
        # this function will update the preview font text, when we change font
        # setting or typing the task

        taskText = self.addTaskDlg.ui.taskEntry.currentText()
        fontFamily = self.addTaskDlg.ui.fontName.currentFont().family()
        fontSize = self.addTaskDlg.ui.fontSize.value()
        fontStyle = self.addTaskDlg.ui.fontStyle.currentText()
        fontWeight = self.addTaskDlg.ui.fontWeight.currentText()
        font = QtGui.QFont()  # create our font object
        # setting our font family (Ubuntu, Arial ...etc)
        font.setFamily(fontFamily)
        # setting the point size (10 pt, 14 pt ..etc)
        font.setPointSize(fontSize)
        # setting the style
        if fontStyle == "Italic":
            font.setStyle(QtGui.QFont.StyleItalic)
        elif fontStyle == "Oblique":
            font.setStyle(QtGui.QFont.StyleOblique)
        else:
            font.setStyle(QtGui.QFont.StyleNormal)
        # setting the weight
        if fontWeight == "Bold":
            font.setWeight(QtGui.QFont.Bold)
        else:
            font.setWeight(QtGui.QFont.Normal)
        self.addTaskDlg.ui.previewText.setText(taskText)
        self.addTaskDlg.ui.previewText.setFont(font)

    def updateTaskTable(self):
        # After we add a task we call this function to update the tableWidget
        # and the task in it also we call it after we deleted a task or we edit
        # a task

        try:
            dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
            # check for tasks that has no duration but has elapsedtime
            # move it to the completedList
            self.checkTaskStatus()
            self.mainWindow.taskTable.clearContents()  # Clear the contents
            # (task,duration,status) of the table to update it without the
            # touching of the title of the columns.
            rowIndex = 0  # a count variable
            # Getting the current number of Uncompleted tasks
            rowNumber = len(
                self.database["tasks"][yearFilter][monthFilter][dayFilter][0])
            # Setting the current number of rows depending on the number of
            # tasks
            self.mainWindow.taskTable.setRowCount(rowNumber)
            for task in self.database["tasks"][yearFilter][monthFilter][
                    dayFilter][0]:  # Iterates uncompleted tasks
                font = QtGui.QFont()
                font.setFamily(task[3])
                font.setPointSize(task[4])
                fontStyle = task[5]
                if fontStyle == "Italic":
                    font.setStyle(QtGui.QFont.StyleItalic)
                elif fontStyle == "Oblique":
                    font.setStyle(QtGui.QFont.StyleOblique)
                else:
                    font.setStyle(QtGui.QFont.StyleNormal)
                fontWeight = task[6]
                if fontWeight == "Bold":
                    font.setWeight(QtGui.QFont.Bold)
                else:
                    font.setWeight(QtGui.QFont.Normal)
                taskText = QtWidgets.QTableWidgetItem(task[0])
                durationText = QtWidgets.QTableWidgetItem(
                    "{} Minutes".format(task[1]))
                if task[1] == -1:
                    durationText = QtWidgets.QTableWidgetItem(
                        "{}".format(task[1]))
                if task[12] == -1:
                    remainingTime = QtWidgets.QTableWidgetItem(
                        "{}".format(task[12]))  # Minute:Seconds
                else:
                    # the default time is in milliseconds so we convert it to
                    # minutes and seconds
                    remainingTime = QtWidgets.QTableWidgetItem(
                        "{} Min {} Sec".format(
                            task[12]//1000//60, task[12]//1000 %
                            60))  # Minute:Seconds
                elapsedTime = QtWidgets.QTableWidgetItem(
                    "{} Min {} Sec".format(
                        task[13]//1000//60, task[13]//1000 %
                        60))  # Minute:Seconds
                taskText.setFont(font)
                durationText.setFont(font)
                remainingTime.setFont(font)
                elapsedTime.setFont(font)
                # Set the duration of the task.
                self.mainWindow.taskTable.setItem(rowIndex, 0, durationText)
                # Set the elapsed time of the task
                self.mainWindow.taskTable.setItem(
                    rowIndex, 1, elapsedTime)
                # Set the remaining time of the task
                self.mainWindow.taskTable.setItem(
                    rowIndex, 2, remainingTime)
                # Set the task name
                self.mainWindow.taskTable.setItem(
                    rowIndex, 3, taskText)
                # Increasing the row variable to assign the next task to the
                # next row
                rowIndex += 1
            # set the focus to the table
            self.mainWindow.taskTable.setFocus(True)
            # select the first task of the list
            self.mainWindow.taskTable.setCurrentCell(self.currentTaskIndex, 0)
            # refresh the analysis table
            self.updateAnalysisTable()
            # refresh the completedTaskTable
            self.updateCompletedTaskTable()
        # The first time we open the application we have no key for today so we
        # get  error when we try to show the content to the table
        except KeyError:
            # Setting the current number of rows to zero because we get KeyError
            # which means no tasks for today
            self.mainWindow.taskTable.setRowCount(0)

    def updateCompletedTaskTable(self):
        # after we complete a task we call this function to refresh the
        # completed task table

        try:
            dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
            # Clear the contents (task,duration) of the table to update it
            # without the touching of the title of the columns.
            self.mainWindow.completedTaskTable.clearContents()
            rowIndex = 0  # a count variable
            # Getting the current number of completed tasks
            rowNumber = len(
                self.database["tasks"][yearFilter][monthFilter][dayFilter][1])
            # Setting the current number of rows depending on the number of
            # tasks
            self.mainWindow.completedTaskTable.setRowCount(rowNumber)
            for task in self.database["tasks"][yearFilter][monthFilter][
                    dayFilter][1]:  # Iterates completed tasks
                font = QtGui.QFont()
                font.setFamily(task[3])
                font.setPointSize(task[4])
                fontStyle = task[5]
                if fontStyle == "Italic":
                    font.setStyle(QtGui.QFont.StyleItalic)
                elif fontStyle == "Oblique":
                    font.setStyle(QtGui.QFont.StyleOblique)
                else:
                    font.setStyle(QtGui.QFont.StyleNormal)
                fontWeight = task[6]
                if fontWeight == "Bold":
                    font.setWeight(QtGui.QFont.Bold)
                else:
                    font.setWeight(QtGui.QFont.Normal)
                taskText = QtWidgets.QTableWidgetItem(task[0])
                taskText.setFont(font)
                # Set the current task to the specified column and row
                self.mainWindow.completedTaskTable.setItem(
                    rowIndex, 0, taskText)
                # Increasing the row variable to assign the next task to the
                # next row
                rowIndex += 1
        # The first time we open the application we have no key for today so we
        # get  error when we try to show the content to the table
        except KeyError:
            # Setting the current number of rows to zero because we get KeyError
            # which means no completed tasks for today
            self.mainWindow.completedTaskTable.setRowCount(0)

    def updateAnalysisTable(self):
        # we call this function everytime we add, edit, delete, complete a task
        # everytime we chnage the view from monthly to yearly or change the year
        # or the month we call this function also

        try:
            monthFilter = self.mainWindow.monthAnalysisFilter.currentText()
            yearFilter = self.mainWindow.yearAnalysisFilter.currentText()
            positiveFont = QtGui.QFont()
            positiveFont.setBold(self.configFile["useBoldAnalysisTable"])
            # Clear the contents (task,duration) of the table to update it
            # without the touching of the title of the columns.
            self.mainWindow.analysisTable.clearContents()
            rowIndex = 0  # a count variable
            # Getting the current number of days or months depends on the
            # selection (yearly,monthly)
            if self.mainWindow.analysisView.currentText() == "Monthly View":
                rowNumber = len(
                    self.database["tasks"][yearFilter][monthFilter].keys())
            else:
                rowNumber = len(self.database["tasks"][yearFilter].keys())
            # Setting the current number of rows depending on the number of days
            # or months
            self.mainWindow.analysisTable.setRowCount(rowNumber)
            if self.mainWindow.analysisView.currentText() == "Monthly View":
                self.mainWindow.monthAnalysisFilter.setEnabled(True)
                self.mainWindow.analysisTable.setHorizontalHeaderLabels(
                    ["Date", "Total Tasks", "UnCompleted Tasks",
                     "Completed Tasks", "Deleted Tasks", "Points"])
                for date in self.database["tasks"][yearFilter][monthFilter]:
                    # returned value is a list, UnCompleted-Completed-Deleted
                    tasksNumber = self.totalTasks(date)
                    totalTasks = QtWidgets.QTableWidgetItem(
                        "{}".format(sum(tasksNumber)))
                    uncompletedTasks = QtWidgets.QTableWidgetItem(
                        "{}".format(tasksNumber[0]))
                    completedTasks = QtWidgets.QTableWidgetItem(
                        "{}".format(tasksNumber[1]))
                    deletedTasks = QtWidgets.QTableWidgetItem(
                        "{}".format(tasksNumber[2]))
                    totalPoints = QtWidgets.QTableWidgetItem("{}".format(0))
                    tasks = self.database["tasks"][yearFilter][monthFilter][
                        date]
                    # we go through the uncompleted and completed task only
                    points = 0
                    for i in range(2):
                        for task in tasks[i]:
                            # this is the uncompleted tasks
                            if i == 0:
                                # current value in elapsed time is in
                                # milliseconds so we need to convert it to
                                # minutes the elapsed time only the minutes
                                temp = task[13]//1000//60
                                # multiply number of minutes by 5 because it's
                                # still uncompleted task
                                temp *= 5
                                # add the score to the total points
                                points += temp
                            # the completedTasks
                            elif i == 1:
                                # if this task has no duration so sure will have
                                # an elapsed time
                                if task[1] == -1:
                                    temp = task[13]//1000//60
                                    # we multiply by 10 because the task has
                                    # been completed successfully
                                    temp *= 10
                                    # add the score to the total points + 100
                                    # points for every completed Task
                                    points += temp + 100
                                # this task has a duration so the elapsed time
                                # equal the duration
                                else:
                                    # the default value in duration is in minute
                                    # so no need to convert
                                    temp = task[1] * 10
                                    points += temp
                    # subtract 50 points for every uncompleted or deleted Task
                    points -= 50 * (tasksNumber[0] + tasksNumber[2])
                    totalPoints = QtWidgets.QTableWidgetItem(
                        "{}".format(points))
                    date = QtWidgets.QTableWidgetItem("{}".format(date))
                    totalPointsValue = int(totalPoints.text())
                    if self.configFile["bgColor"]:
                        if totalPointsValue == 3000:
                            totalPoints.setBackground(
                                self.configFile["bgColor1"])
                        elif totalPointsValue >= 2400:
                            totalPoints.setBackground(
                                self.configFile["bgColor2"])
                        elif totalPointsValue >= 1800:
                            totalPoints.setBackground(
                                self.configFile["bgColor3"])
                        elif totalPointsValue >= 1200:
                            totalPoints.setBackground(
                                self.configFile["bgColor4"])
                        elif totalPointsValue >= 600:
                            totalPoints.setBackground(
                                self.configFile["bgColor5"])
                    if self.configFile["fgColor"]:
                        if totalPointsValue == 3000:
                            totalPoints.setForeground(
                                self.configFile["fgColor1"])
                        elif totalPointsValue >= 2400:
                            totalPoints.setForeground(
                                self.configFile["fgColor2"])
                        elif totalPointsValue >= 1800:
                            totalPoints.setForeground(
                                self.configFile["fgColor3"])
                        elif totalPointsValue >= 1200:
                            totalPoints.setForeground(
                                self.configFile["fgColor4"])
                        elif totalPointsValue >= 600:
                            totalPoints.setForeground(
                                self.configFile["fgColor5"])
                    # set/unset bold font style on positive numbers
                    if int(totalTasks.text()) > 0:
                        totalTasks.setFont(positiveFont)
                    if int(uncompletedTasks.text()) > 0:
                        uncompletedTasks.setFont(positiveFont)
                    if int(completedTasks.text()) > 0:
                        completedTasks.setFont(positiveFont)
                    if int(deletedTasks.text()) > 0:
                        deletedTasks.setFont(positiveFont)
                    if totalPointsValue > 0:
                        totalPoints.setFont(positiveFont)
                    self.mainWindow.analysisTable.setItem(rowIndex, 0, date)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 1, totalTasks)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 2, uncompletedTasks)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 3, completedTasks)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 4, deletedTasks)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 5, totalPoints)
                    rowIndex += 1
                # select the current date in the table
                self.mainWindow.analysisTable.setCurrentCell(
                    datetime.today().day - 1, 0)
            else:
                self.mainWindow.monthAnalysisFilter.setEnabled(False)
                self.mainWindow.analysisTable.setHorizontalHeaderLabels(
                    ["Month", "Total Tasks", "UnCompleted Tasks",
                     "Completed Tasks", "Deleted Tasks", "Points"])
                rowIndex = 0
                for key in self.database["tasks"][yearFilter].keys():
                    month = QtWidgets.QTableWidgetItem("{}".format(key))
                    self.mainWindow.analysisTable.setItem(rowIndex, 0, month)
                    # returned value is a list contained three values,
                    # uncompleted,completed,deleted tasks
                    tasksNumber = self.totalTasks(None, key, yearFilter)
                    totalTasks = QtWidgets.QTableWidgetItem(
                        "{}".format(sum(tasksNumber)))
                    uncompletedTasks = QtWidgets.QTableWidgetItem(
                        "{}".format(tasksNumber[0]))
                    completedTasks = QtWidgets.QTableWidgetItem(
                        "{}".format(tasksNumber[1]))
                    deletedTasks = QtWidgets.QTableWidgetItem(
                        "{}".format(tasksNumber[2]))
                    totalPoints = QtWidgets.QTableWidgetItem("{}".format(0))
                    monthPoints = 0
                    for date in self.database["tasks"][yearFilter][key].keys():
                        tasks = self.database["tasks"][yearFilter][key][date]
                        dayPoints = 0
                        for i in range(2):
                            for task in tasks[i]:
                                # this is the uncompleted tasks
                                if i == 0:
                                    # current value in elapsed time is in
                                    # milliseconds so we need to convert it to
                                    # minutes
                                    # the elapsed time only the minutes
                                    temp = task[13]//1000//60
                                    # multiply number of minutes by 5 because
                                    # it's still uncompleted task
                                    temp *= 5
                                    # add the score to the day points
                                    dayPoints += temp
                                # the completedTasks
                                elif i == 1:
                                    # if this task has no duration so sure will
                                    # have an elapsed time
                                    if task[1] == -1:
                                        temp = task[13]//1000//60
                                        # we multiply by 10 because the task has
                                        # been completed successfully
                                        temp *= 10
                                        # add the score to the total points
                                        dayPoints += temp
                                    # this task has a duration so the elapsed
                                    # time equal the duration
                                    else:
                                        # the default value in duration is in
                                        # minute so no need to convert
                                        temp = task[1] * 10
                                        dayPoints += temp
                        # subtract 50 points for every uncompleted or deleted
                        dayPoints -= 50 * len(tasks[0]+tasks[2])
                        monthPoints += dayPoints
                    totalPoints = QtWidgets.QTableWidgetItem(
                        "{}".format(monthPoints))
                    totalPointsValue = int(totalPoints.text())
                    if self.configFile["bgColor"]:
                        if totalPointsValue >= 90000:
                            totalPoints.setBackground(
                                self.configFile["bgColor1"])
                        elif totalPointsValue >= 72000:
                            totalPoints.setBackground(
                                self.configFile["bgColor2"])
                        elif totalPointsValue >= 54000:
                            totalPoints.setBackground(
                                self.configFile["bgColor3"])
                        elif totalPointsValue >= 36000:
                            totalPoints.setBackground(
                                self.configFile["bgColor4"])
                        elif totalPointsValue >= 18000:
                            totalPoints.setBackground(
                                self.configFile["bgColor5"])
                    if self.configFile["fgColor"]:
                        if totalPointsValue >= 90000:
                            totalPoints.setForeground(
                                self.configFile["fgColor1"])
                        elif totalPointsValue >= 72000:
                            totalPoints.setForeground(
                                self.configFile["fgColor2"])
                        elif totalPointsValue >= 54000:
                            totalPoints.setForeground(
                                self.configFile["fgColor3"])
                        elif totalPointsValue >= 36000:
                            totalPoints.setForeground(
                                self.configFile["fgColor4"])
                        elif totalPointsValue >= 18000:
                            totalPoints.setForeground(
                                self.configFile["fgColor5"])
                    # set/unset bold font style on positive numbers
                    if int(totalTasks.text()) > 0:
                        totalTasks.setFont(positiveFont)
                    if int(uncompletedTasks.text()) > 0:
                        uncompletedTasks.setFont(positiveFont)
                    if int(completedTasks.text()) > 0:
                        completedTasks.setFont(positiveFont)
                    if int(deletedTasks.text()) > 0:
                        deletedTasks.setFont(positiveFont)
                    if totalPointsValue > 0:
                        totalPoints.setFont(positiveFont)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 1, totalTasks)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 2, uncompletedTasks)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 3, completedTasks)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 4, deletedTasks)
                    self.mainWindow.analysisTable.setItem(
                        rowIndex, 5, totalPoints)
                    rowIndex += 1
                row = datetime.today().month - 1
                self.mainWindow.analysisTable.setCurrentCell(row, 0)
            self.updateTheChart()
        # The first time we open the application we have no key for today so we
        # get  error when we try to show the content to the table
        except KeyError:
            # Setting the current number of rows to zero, because we don't have
            # data yet
            self.mainWindow.analysisTable.setRowCount(0)

    def updateTheChart(self):
        # Everytime we change something in the analysis table we call this
        # function

        analysisFilter = self.mainWindow.analysisView.currentText()
        # remove all series
        self.chart.removeAllSeries()
        # create our x axis
        self.axisX = QtChart.QValueAxis()
        # create the y axis
        self.axisY = QtChart.QValueAxis()
        # hide/unhide the x axis labels
        self.axisX.setLabelsVisible(self.configFile["showXaxis"])
        # hide/unhide the y axis labels
        self.axisY.setLabelsVisible(self.configFile["showYaxis"])
        # hide the title
        self.chart.setTitle("")
        # add title to the chart if it's available
        if self.configFile["showChartTitle"]:
            self.chart.setTitle(self.configFile["chartTitle"])
            font = QtGui.QFont()
            font.setFamily(self.configFile["chartTitleFont"])
            font.setPointSize(self.configFile["chartTitleSize"])
            font.setBold(self.configFile["chartTitleStyle"][0])
            font.setItalic(self.configFile["chartTitleStyle"][1])
            self.chart.setTitleFont(font)
            self.chart.setTitleBrush(self.configFile["chartTitleColor"])
        # set/unset the zoom options
        self.chartView.setRubberBand(
            QtChart.QChartView().RubberBands(
                self.configFile["chartZoomOption"]))
        # set/unset the animation
        self.chart.setAnimationOptions(
            QtChart.QChart.AnimationOptions(
                self.configFile["chartAnimation"]))
        totalXAxis = 0
        # set the chart theme
        self.chart.setTheme(
            self.configFile["chartThemes"][self.configFile["chartTheme"]])
        if analysisFilter == "Monthly View":
            totalXAxis = len(self.database["tasks"][
                self.mainWindow.yearAnalysisFilter.currentText()][
                    self.mainWindow.monthAnalysisFilter.currentText()].keys())
            self.axisX.setLabelFormat("Day %d")
        else:
            totalXAxis = len(
                self.database["tasks"][
                    self.mainWindow.yearAnalysisFilter.currentText()].keys())
            self.axisX.setLabelFormat("Month %d")
        # initiate the total x axis count
        self.axisX.setTickCount(totalXAxis)
        # add the x axis
        self.chart.setAxisX(self.axisX)
        pen = QtGui.QPen()
        pen.setWidth(self.configFile["gLineWidth"])
        pen.setColor(self.configFile["gLineColor"])
        # create our series data
        self.series = QtChart.QLineSeries()
        self.series.setPointsVisible(True)
        self.series.setPen(pen)
        totalPointsList = list()
        for row in range(totalXAxis):
            # get the average score from the table
            # convert it to an integer after we delete the percent sign from the
            # text
            totalPointsList.append(
                float(
                    self.mainWindow.analysisTable.item(
                        row, 5).text()))
        # append the result of the day and the average score to the series
        for count in range(len(totalPointsList)):
            self.series.append(count+1, totalPointsList[count])
        self.axisY.setLabelFormat("%d Pt")
        # add the self.series to chart
        self.chart.addSeries(self.series)
        # add the y axis to the chart
        self.chart.setAxisY(self.axisY)
        # attach the axis to the self.series
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

    def updateTaskDetails(self):
        # Everytime we change something in the tasks we call this function to
        # refresh the treeWidget

        self.mainWindow.taskDetailsTree.clear()
        column = self.mainWindow.analysisTable.currentColumn()
        # *[0] Uncompleted tasks
        # *[1] completed tasks
        # *[2] deleted tasks
        # *[*][0] Task
        # *[*][1] Duration
        # *[*][2] Completed Time
        # *[*][3] Font Family
        # *[*][4] Font Point Size
        # *[*][5] Font Style
        # *[*][6] Font Weight
        # *[*][7] Created Time
        # *[*][8] Modified Time
        # *[*][9] Deleted Time
        # *[*][10] Task Start Time
        # *[*][11] Task Stop Time
        # *[*][12] Remaining Task Time in ms
        # *[*][13] Elapsed Task Time in ms
        # *[*][14] Task Notes when we complete a task
        # *[*][15] Revived Time when we complet a task and we revive it again
        # hide the task Details by default
        self.mainWindow.taskDetailsTree.setVisible(False)
        analysisView = self.mainWindow.analysisView.currentText()
        if analysisView.startswith("Mo"):
            # we need only the uncompleted,completed,deleted tasks
            if column >= 2 and column <= 4:
                # Unhide the task details
                self.mainWindow.taskDetailsTree.setVisible(True)
                row = self.mainWindow.analysisTable.currentRow()
                selectedItem = int(
                    self.mainWindow.analysisTable.item(
                        row, column).text())
                if selectedItem == 0:
                    # hide the task details if the current number is zero
                    self.mainWindow.taskDetailsTree.setVisible(False)
                date = self.mainWindow.analysisTable.item(row, 0).text()
                month = self.mainWindow.monthAnalysisFilter.currentText()
                year = self.mainWindow.yearAnalysisFilter.currentText()
                # check what list the user wants, uncompleted,completed,deleted
                # tasks column 2 -> uncompleted but in the database uncompleted
                # in the index 0 so we take two from the column to get the right
                # number
                column -= 2
                for task in self.database["tasks"][year][month][date][column]:
                    taskName = QtWidgets.QTreeWidgetItem(
                        self.mainWindow.taskDetailsTree)
                    taskName.setText(0, task[0])
                    # child of parent
                    item1 = QtWidgets.QTreeWidgetItem()
                    item1.setText(0, "Created Datetime")
                    item2 = QtWidgets.QTreeWidgetItem()
                    item2.setText(0, "Modified Datetime")
                    item3 = QtWidgets.QTreeWidgetItem()
                    item3.setText(0, "Deleted Datetime")
                    item4 = QtWidgets.QTreeWidgetItem()
                    item4.setText(0, "Duration")
                    item5 = QtWidgets.QTreeWidgetItem()
                    item5.setText(0, "Started Time")
                    item6 = QtWidgets.QTreeWidgetItem()
                    item6.setText(0, "Stopped Time")
                    item7 = QtWidgets.QTreeWidgetItem()
                    item7.setText(0, "Completed Time")
                    item8 = QtWidgets.QTreeWidgetItem()
                    item8.setText(0, "Elapsed Time")
                    item9 = QtWidgets.QTreeWidgetItem()
                    item9.setText(0, "Remaining Time")
                    item11 = QtWidgets.QTreeWidgetItem()
                    item11.setText(0, "Notes")
                    item12 = QtWidgets.QTreeWidgetItem()
                    item12.setText(0, "Revived Datetime")

                    # child of children
                    item10 = QtWidgets.QTreeWidgetItem()
                    item10.setText(0, task[7].strftime("%Y-%m-%d, %H:%M:%S %p"))
                    # if the modified time equal to the created time don't show
                    # it
                    item20 = QtWidgets.QTreeWidgetItem()
                    if task[7] != task[8]:
                        item20.setText(
                            0, task[8].strftime("%Y-%m-%d, %I:%M:%S %p"))
                    # we add the value only if the task has been deleted
                    item30 = QtWidgets.QTreeWidgetItem()
                    if task[9] != "N/A":
                        item30.setText(
                            0, task[9].strftime("%Y-%m-%d, %I:%M:%S %p"))
                    # we add the value only if we have duration
                    item40 = QtWidgets.QTreeWidgetItem()
                    if task[1] != -1:
                        item40.setText(0, "{} Minute".format(task[1]))
                    # we add the value only if we started the task
                    item50 = []
                    if len(task[10]) > 0:
                        for time in task[10]:
                            temp = QtWidgets.QTreeWidgetItem()
                            temp.setText(0, time.strftime("%I:%M:%S %p"))
                            item50.append(temp)
                    # we add the value ony if we have started the task and
                    # stopped it
                    item60 = []
                    if len(task[11]) > 0:
                        for time in task[11]:
                            temp = QtWidgets.QTreeWidgetItem()
                            temp.setText(0, time.strftime("%I:%M:%S %p"))
                            item60.append(temp)
                    # we add the value only if we have completed the task
                    item70 = QtWidgets.QTreeWidgetItem()
                    if task[2] != "N/A":
                        item70.setText(0, task[2].strftime("%I:%M:%S %p"))
                    # we add the value only if we have an elapsed time
                    item80 = QtWidgets.QTreeWidgetItem()
                    if task[13] != -1 and task[13] != 0:
                        item80.setText(
                            0, "{} Minute, {} Second".format(
                                task[13]//1000//60, task[13]//1000 %
                                60))
                    # we add the value only if we have a remaining time
                    item90 = QtWidgets.QTreeWidgetItem()
                    if task[12] != -1 and task[12] != 0:
                        item90.setText(
                            0, "{} Minute, {} Second".format(
                                task[12]//1000//60, task[12]//1000 %
                                60))
                    # we add the text only if we have a note
                    item110 = QtWidgets.QTreeWidgetItem()
                    if task[14] != "N/A":
                        item110.setText(0, task[14])
                    # not all tasks has revived value so we have to check first
                    # normal task has 15 properties 16 will the revived time
                    item120 = QtWidgets.QTreeWidgetItem()
                    if len(task) > 15:
                        item120.setText(0, task[15].strftime("%I:%M:%S %p"))

                    # adding child to the parent
                    taskName.addChild(item1)
                    if task[7] != task[8]:
                        taskName.addChild(item2)
                    # add it only if the task has been deleted
                    if task[9] != "N/A":
                        taskName.addChild(item3)
                    # add it only if the task has duration
                    if task[1] != -1:
                        taskName.addChild(item4)
                    # add it only if we have a started time
                    if len(task[10]) > 0:
                        taskName.addChild(item5)
                    # add it only if we have a stopped time
                    if len(task[11]) > 0:
                        taskName.addChild(item6)
                    # add it only if we have completed the task
                    if task[2] != "N/A":
                        taskName.addChild(item7)
                    # we add it only if we have an elapsed time
                    if task[13] != -1 and task[13] != 0:
                        taskName.addChild(item8)
                    # we add it only if we have a remaining time
                    if task[12] != -1 and task[12] != 0:
                        taskName.addChild(item9)
                    # we add it only if we have a note
                    if task[14] != "N/A":
                        taskName.addChild(item11)
                    # we add only if we have a revived time otherwise we get
                    # IndexError insert the task rather than append it to the
                    # end
                    if len(task) > 15:
                        taskName.insertChild(1, item12)

                    # adding child to the children
                    item1.addChild(item10)
                    if task[7] != task[8]:
                        item2.addChild(item20)
                    if task[9] != "N/A":
                        item3.addChild(item30)
                    if task[1] != "N/A":
                        item4.addChild(item40)
                    if len(task[10]) > 0:
                        for item in item50:
                            item5.addChild(item)
                    if len(task[11]) > 0:
                        for item in item60:
                            item6.addChild(item)
                    if task[2] != "N/A":
                        item7.addChild(item70)
                    if task[13] != -1 and task[13] != 0:
                        item8.addChild(item80)
                    if task[12] != -1 and task[12] != 0:
                        item9.addChild(item90)
                    if task[14] != "N/A":
                        item11.addChild(item110)
                    if len(task) > 15:
                        item12.addChild(item120)

    def hasTask(self, taskText, yearFilter, monthFilter, dayFilter):
        # Check if a task is already in the list
        # we return True with the index of the existing task, and the index of
        # the list, otherwise False and -1

        try:
            count = 0
            for taskList in self.database["tasks"][yearFilter][monthFilter][
                    dayFilter]:

                # our tasklist contains 3 lists 1 for the Uncompleted tasks
                # which is the default list for the new task 2 for the completed
                # tasks and the last one for the deleted tasks we add a counter
                # to count until 3, if we did not found the task in the first 2
                # lists we stop the loop and return False because we don't want
                # to stop the user from adding a task that he already added
                # before but he deleted it also

                count += 1
                index = -1
                if count == 3:
                    break
                for task in taskList:
                    index += 1
                    if task[0] == taskText:
                        return True, index, count
            return False, -1
        # when we try to look for a future year that is not already written in
        # the self.database file, we return False also
        except KeyError:
            return False, -1

    def resetCurrentPathFunction(self):
        # reset the current path to the default one and output the path in
        # current path lineEdit

        self.preferencesDlg.ui.currentPathEntry.setText(
            self.defaultDatabasePath)
        # enable the button if we press on reset
        self.preferencesDlg.ui.acceptButton.setEnabled(True)

    def changeCurrentPathDlg(self):
        # Open a dialog window to let the user to select a new file path
        # and load that file

        # returned value is a tuple our path is in the first place
        self.path = QtWidgets.QFileDialog.getOpenFileName(
            self.preferencesDlg,
            "Open another file",
            directory=self.currentPath,
            options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if self.path[0]:
            self.preferencesDlg.ui.currentPathEntry.setText(self.path[0])

    def acceptPreferencesDlgChanges(self):
        # if the user presses the accept button
        # we call this function to accept the changes

        # changing the current path of the database with copying the same
        # database to the new path
        self.currentPath = self.preferencesDlg.ui.currentPathEntry.text()
        self.configFile["currentPath"] = self.currentPath
        # get the current status of the autosave option
        autoSave = self.preferencesDlg.ui.autosaveDatabase.isChecked()
        # save the current status of the autosave to the configFile
        self.configFile["autoSaveDatabase"] = autoSave
        self.autoSaveDatabase = self.configFile["autoSaveDatabase"]
        # get the current index of the selectedTable
        index = self.preferencesDlg.ui.selectedTable.currentIndex()
        # get the show completedTaskTable value
        temp = self.preferencesDlg.ui.showCompletedTasks.isChecked()
        self.configFile["showCompletedTasks"] = temp
        self.mainWindow.completedTaskTable.setVisible(
            self.configFile["showCompletedTasks"])
        # get the value of showing the grid table
        self.configFile["showTableGrid"][
            index] = self.preferencesDlg.ui.showTableGrid.isChecked()
        # get the value of the grid style
        self.configFile["tableGridStyle"][
            index] = self.preferencesDlg.ui.tableGridStyle.currentText()
        # get the value of set alternating row colors
        self.configFile["alternatingRowColors"][
            index] = self.preferencesDlg.ui.tableAlternatingRowC.isChecked()
        # get the value of show the horizontal and vertical headers
        self.configFile["showHorizontalHeaders"][
            index] = self.preferencesDlg.ui.showHorizontalHeaders.isChecked()
        self.configFile["showVerticalHeaders"][
            index] = self.preferencesDlg.ui.showVerticalHeaders.isChecked()
        self.showHeaders()
        self.setTableGrid()
        self.setTableAlternatingRowC()
        # get the status of the background color of the average score
        self.configFile[
            "bgColor"] = self.preferencesDlg.ui.useBgColors.isChecked()
        # get the background color of the average score
        self.configFile["bgColor1"] = QtGui.QColor(
            self.preferencesDlg.ui.bgRedNumber1.value(),
            self.preferencesDlg.ui.bgGreenNumber1.value(),
            self.preferencesDlg.ui.bgBlueNumber1.value())
        self.configFile["bgColor2"] = QtGui.QColor(
            self.preferencesDlg.ui.bgRedNumber2.value(),
            self.preferencesDlg.ui.bgGreenNumber2.value(),
            self.preferencesDlg.ui.bgBlueNumber2.value())
        self.configFile["bgColor3"] = QtGui.QColor(
            self.preferencesDlg.ui.bgRedNumber3.value(),
            self.preferencesDlg.ui.bgGreenNumber3.value(),
            self.preferencesDlg.ui.bgBlueNumber3.value())
        self.configFile["bgColor4"] = QtGui.QColor(
            self.preferencesDlg.ui.bgRedNumber4.value(),
            self.preferencesDlg.ui.bgGreenNumber4.value(),
            self.preferencesDlg.ui.bgBlueNumber4.value())
        self.configFile["bgColor5"] = QtGui.QColor(
            self.preferencesDlg.ui.bgRedNumber5.value(),
            self.preferencesDlg.ui.bgGreenNumber5.value(),
            self.preferencesDlg.ui.bgBlueNumber5.value())
        # get the status of the foreground color of the average score
        self.configFile[
            "fgColor"] = self.preferencesDlg.ui.useFgColors.isChecked()
        # get the background color of the average score
        self.configFile["fgColor1"] = QtGui.QColor(
            self.preferencesDlg.ui.fgRedNumber1.value(),
            self.preferencesDlg.ui.fgGreenNumber1.value(),
            self.preferencesDlg.ui.fgBlueNumber1.value())
        self.configFile["fgColor2"] = QtGui.QColor(
            self.preferencesDlg.ui.fgRedNumber2.value(),
            self.preferencesDlg.ui.fgGreenNumber2.value(),
            self.preferencesDlg.ui.fgBlueNumber2.value())
        self.configFile["fgColor3"] = QtGui.QColor(
            self.preferencesDlg.ui.fgRedNumber3.value(),
            self.preferencesDlg.ui.fgGreenNumber3.value(),
            self.preferencesDlg.ui.fgBlueNumber3.value())
        self.configFile["fgColor4"] = QtGui.QColor(
            self.preferencesDlg.ui.fgRedNumber4.value(),
            self.preferencesDlg.ui.fgGreenNumber4.value(),
            self.preferencesDlg.ui.fgBlueNumber4.value())
        self.configFile["fgColor5"] = QtGui.QColor(
            self.preferencesDlg.ui.fgRedNumber5.value(),
            self.preferencesDlg.ui.fgGreenNumber5.value(),
            self.preferencesDlg.ui.fgBlueNumber5.value())
        # get the gLineColor and gLineWidth
        self.configFile["gLineColor"] = QtGui.QColor(
            self.preferencesDlg.ui.gLineRedNumber.value(),
            self.preferencesDlg.ui.gLineGreenNumber.value(),
            self.preferencesDlg.ui.gLineBlueNumber.value())
        self.configFile[
            "gLineWidth"] = self.preferencesDlg.ui.gLineWidth.value()
        # get the default chart settings
        self.configFile["showXaxis"] = self.preferencesDlg.ui.showX.isChecked()
        self.configFile["showYaxis"] = self.preferencesDlg.ui.showY.isChecked()
        # get the current chart title settings
        self.configFile[
            "showChartTitle"] = self.preferencesDlg.ui.addTitle.isChecked()
        self.configFile["chartTitle"] = self.preferencesDlg.ui.chartTitle.text()
        temp = self.preferencesDlg.ui.chartTitleFont.currentFont().family()
        self.configFile["chartTitleFont"] = temp
        self.configFile[
            "chartTitleSize"] = self.preferencesDlg.ui.chartTitleSize.value()
        self.configFile["chartTitleStyle"][
            0] = self.preferencesDlg.ui.chartBoldFont.isChecked()
        self.configFile["chartTitleStyle"][
            1] = self.preferencesDlg.ui.chartItalicFont.isChecked()
        self.configFile["chartTitleColor"] = QtGui.QColor(
            self.preferencesDlg.ui.cTitleRedNumber.value(),
            self.preferencesDlg.ui.cTitleGreenNumber.value(),
            self.preferencesDlg.ui.cTitleBlueNumber.value())
        # get the chart zoom option
        temp = self.preferencesDlg.ui.chartZoomOption.currentIndex()
        self.configFile["chartZoomOption"] = temp
        # get the chart animation style
        temp = self.preferencesDlg.ui.chartAnimation.currentIndex()
        self.configFile["chartAnimation"] = temp
        # get the current chart theme
        self.configFile[
            "chartTheme"] = self.preferencesDlg.ui.chartTheme.currentIndex()
        # get the current status of use bold style on positive numbers
        temp = self.preferencesDlg.ui.useBoldAnalysisT.isChecked()
        self.configFile["useBoldAnalysisTable"] = temp
        # saving the configFile
        self.saveConfigFile()
        self.updateTaskTable()
        self.preferencesDlg.accept()

    def startCopyTasks(self):
        # when the user selects tasks and choose the destination date and
        # presses the start button
        # when we copy a task we reset the creation and modified time we reset
        # the elapsed and the remaining time

        # *[0] Uncompleted tasks
        # *[1] completed tasks
        # *[2] deleted tasks
        # *[*][0] Task
        # *[*][1] Duration
        # *[*][2] Completed Time
        # *[*][3] Font Family
        # *[*][4] Font Point Size
        # *[*][5] Font Style
        # *[*][6] Font Weight
        # *[*][7] Created Time
        # *[*][8] Modified Time
        # *[*][9] Deleted Time
        # *[*][10] Task Start Time
        # *[*][11] Task Stop Time
        # *[*][12] Remaining Task Time in ms
        # *[*][13] Elapsed Task Time in ms
        # *[*][14] Task Notes when we complete a task
        # *[*][15] Revived Time when we complete a task and we revive it
        sourceTasks = self.mainWindow.taskTable.selectedIndexes()
        # we will get only the first number of every 4 numbers
        sourceTasks = sorted([i.row() for i in sourceTasks][::4])
        # how many tasks to copy
        totalTasks = len(sourceTasks)
        # how many copy to make
        totalCopies = len(self.destinationDateList)
        sourceDate = self.copyTasksDlg.ui.sourceDate.text()
        sourceMonth = sourceDate.split()[1]
        sourceYear = sourceDate.split()[-1]
        progressPercent = totalCopies * totalTasks
        elapsedTime = 0
        # before we start copy we have to check if the destination dates is
        # available in our database (year Key)
        years = [year.split()[-1] for year in self.destinationDateList]
        # remove duplicate years
        for year in list(years):
            if years.count(year) > 1:
                years.remove(year)
        for year in years:
            # the destination year is not available as a key so we create the
            # database for the year first
            if self.database["tasks"].get(year, -1) == -1:
                self.createTaskDaysData(year, reset=False)
        self.copyTasksDlg.ui.progressBar.setValue(0)
        for copy in range(totalCopies):
            for task in range(totalTasks):
                createdTime = datetime.today()
                modifiedTime = createdTime
                sourceTask = self.database["tasks"][sourceYear][sourceMonth][
                    sourceDate][0][sourceTasks[task]].copy()
                # remaining time equal to the duration
                sourceTask[12] = sourceTask[1]
                if sourceTask[1] != -1:
                    # convert the duration to ms
                    sourceTask[12] = sourceTask[1] * 60 * 1000
                sourceTask[7] = createdTime
                sourceTask[8] = modifiedTime
                sourceTask[10] = []  # startedTime
                sourceTask[11] = []  # stoppedTime
                sourceTask[13] = elapsedTime
                destinationDate = self.destinationDateList[copy]
                destinationMonth = destinationDate.split()[1]
                destinationYear = destinationDate.split()[-1]
                taskExistance = self.hasTask(
                    sourceTask[0],
                    destinationYear,
                    destinationMonth,
                    destinationDate)
                if taskExistance[0]:
                    if self.copyTasksDlg.ui.skipCopy.isChecked():
                        pass
                    elif self.copyTasksDlg.ui.overwriteCopy.isChecked():
                        # we don't want to overwrite a completed task
                        if taskExistance[2] != 2:
                            self.database["tasks"][destinationYear][
                                destinationMonth][destinationDate][0][
                                taskExistance[1]][1] = sourceTask[1]
                            self.database["tasks"][destinationYear][
                                destinationMonth][destinationDate][0][
                                taskExistance[1]][7] = sourceTask[7]
                            self.database["tasks"][destinationYear][
                                destinationMonth][destinationDate][0][
                                taskExistance[1]][8] = sourceTask[8]
                            self.database["tasks"][destinationYear][
                                destinationMonth][destinationDate][0][
                                taskExistance[1]][12] = sourceTask[12]
                            self.database["tasks"][destinationYear][
                                destinationMonth][destinationDate][0][
                                taskExistance[1]][13] = sourceTask[13]
                else:
                    self.database["tasks"][destinationYear][destinationMonth][
                        destinationDate][0].append(sourceTask)
                progressBarValue = (task+1)*(copy+1) * 100 // progressPercent
                self.copyTasksDlg.ui.progressBar.setValue(progressBarValue)
        if self.autoSaveDatabase:
            self.saveDatabase()
        else:
            # after we change something in the database we enable the save
            # button and add a star to the titlebar
            self.mainWindow.actionSave.setEnabled(True)
            self.setWindowTitle("Sunrise - {}*".format(self.currentPath))
        self.updateTaskTable()
        self.updateCompletedTaskTable()

    def taskCompletedOutside(self):
        # we call this function if the user has completed a task outside

        taskNotes = self.taskCompletedDlg.ui.taskNotes.toPlainText()
        temp = self.taskCompletedDlg.ui.groupBox.isChecked()
        if len(taskNotes) == 0 or not temp:
            taskNotes = "N/A"
        row = self.mainWindow.taskTable.currentRow()
        dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
        startTime = self.taskCompletedDlg.ui.startTime.time()
        startTime = datetime(
            datetime.today().year,
            datetime.today().month,
            datetime.today().day,
            startTime.hour(),
            startTime.minute(),
            0)
        # add the stoppedTime and the completedTime of the task to the task
        # properties
        stoppedTime = self.taskCompletedDlg.ui.completeTime.time()
        stoppedTime = datetime(
            datetime.today().year,
            datetime.today().month,
            datetime.today().day,
            stoppedTime.hour(),
            stoppedTime.minute(),
            0)
        # get the difference between the complete time and the start time
        # (elapsedTime) convert it to milliseconds
        elapsedTime = (stoppedTime - startTime).seconds * 1000
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][10].append(startTime)
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][11].append(stoppedTime)
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][2] = stoppedTime
        # the remaining time
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][12] = -1
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][13] = elapsedTime
        if taskNotes != "N/A":
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][14] = taskNotes + "\nThis task has been completed outside."
        else:
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][14] = "This task has been completed outside."
        # add the remaining time to the task properties
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][12] = 0
        # remove the completed task from the Uncompleted tasks and add it to the
        # completedTask
        completedTask = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0].pop(row)
        self.database["tasks"][yearFilter][monthFilter][
            dayFilter][1].append(completedTask)
        # stop the timer
        self.timer.stop()
        if self.autoSaveDatabase:
            self.saveDatabase()
        else:
            # after we change something in the database we enable the save
            # button and add a star to the titlebar
            self.mainWindow.actionSave.setEnabled(True)
            self.setWindowTitle("Sunrise - {}*".format(self.currentPath))
        self.updateTaskTable()
        # set the focus to the table
        self.mainWindow.completedTaskTable.setFocus(True)
        # select the last completed task of the list
        totalTasks = len(self.database["tasks"]
                         [yearFilter][monthFilter][dayFilter][1])
        self.mainWindow.completedTaskTable.setCurrentCell(totalTasks-1, 0)
        self.taskCompletedDlg.accept()

    def checkCompletedTime(self):
        # Check if the time is legitimate or not, if yes enable the accept
        # button disable it otherwise

        startTime = self.taskCompletedDlg.ui.startTime.time()
        completeTime = self.taskCompletedDlg.ui.completeTime.time()
        # disable the button and activate if the condition is True
        self.taskCompletedDlg.ui.acceptButton.setEnabled(False)
        # check if the time setting is legitimate or no
        # is there a duration between them or no, and can't the task start after
        # the complete time
        if startTime < completeTime:
            self.taskCompletedDlg.ui.acceptButton.setEnabled(True)

    def showCopyTasksDlg(self):
        # when the user selects a task or many tasks and presses the copy
        # button, we execute this function

        # date is a tuple contains 3 value date,month,year
        date = self.getTaskDateFilter()
        # this variable will be shared with the addDestinationDate function
        # when we add a list we add it here first so we can check later that the
        # user can't add the same date twice
        self.destinationDateList = list()
        # set the source date
        self.copyTasksDlg.ui.sourceDate.setText(date[0])
        # set the current and the minimum date of the destination date
        self.copyTasksDlg.ui.destinationDate.setDate(QtCore.QDate.currentDate())
        self.copyTasksDlg.ui.destinationDate.setMinimumDate(
            QtCore.QDate.currentDate())
        # clear the destination date list
        self.copyTasksDlg.ui.destinationDateList.clear()
        # set the progressbar to 0
        self.copyTasksDlg.ui.progressBar.setValue(0)
        self.copyTasksDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        self.copyTasksDlg.exec_()

    def showTaskCompletedMsg(self):
        # after the user finishes a task will execute this function
        # to open a message dialog
        self.taskCompletedMsg.ui.taskNotes.clear()
        self.taskCompletedMsg.setWindowModality(QtCore.Qt.ApplicationModal)
        self.taskCompletedMsg.exec_()

    def showTaskCompletedDlg(self):
        self.taskCompletedDlg.ui.taskNotes.clear()
        currentHour = datetime.today().hour
        currentMinute = datetime.today().minute
        # can't finish tasks in a future time
        self.taskCompletedDlg.ui.startTime.setTime(
            QtCore.QTime(currentHour, currentMinute))
        self.taskCompletedDlg.ui.startTime.setMaximumTime(
            QtCore.QTime(currentHour, currentMinute))
        self.taskCompletedDlg.ui.completeTime.setTime(
            QtCore.QTime(currentHour, currentMinute))
        self.taskCompletedDlg.ui.completeTime.setMaximumTime(
            QtCore.QTime(currentHour, currentMinute))
        # disable the accept button by default until the user change the times
        # to a legitimate one legitimate time start time is less than the
        # complete time
        self.taskCompletedDlg.ui.acceptButton.setEnabled(False)
        self.taskCompletedDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        self.taskCompletedDlg.exec_()

    def showPreferencesDlg(self):
        # Open the preferences dialog if the prefrences button in the toolbar or
        # Ctrl + p have been activated

        # set the current index of the prefrencesList to 0
        self.preferencesDlg.ui.preferencesList.setCurrentRow(0)
        # set the status of the autosave option
        self.preferencesDlg.ui.autosaveDatabase.setChecked(
            self.autoSaveDatabase)
        # set the current path of the database file
        self.preferencesDlg.ui.currentPathEntry.setText(
            self.configFile["currentPath"])
        # set the current value for showing the completedTask
        self.preferencesDlg.ui.showCompletedTasks.setChecked(
            self.configFile["showCompletedTasks"])
        # set the current index of the selectedTable
        self.preferencesDlg.ui.selectedTable.setCurrentIndex(0)
        # set the current value of show table grid
        self.preferencesDlg.ui.showTableGrid.setChecked(
            self.configFile["showTableGrid"][0])
        # set the current value of the grid style
        self.preferencesDlg.ui.tableGridStyle.setCurrentText(
            self.configFile["tableGridStyle"][0])
        # set the current value of show alternatic row colors
        self.preferencesDlg.ui.tableAlternatingRowC.setChecked(
            self.configFile["alternatingRowColors"][0])
        # set the current value of show the horizontal and vertical headers
        self.preferencesDlg.ui.showHorizontalHeaders.setChecked(
            self.configFile["showHorizontalHeaders"][0])
        self.preferencesDlg.ui.showVerticalHeaders.setChecked(
            self.configFile["showVerticalHeaders"][0])
        # check/uncheck the background color groupbox of the average score
        self.preferencesDlg.ui.useBgColors.setChecked(
            self.configFile["bgColor"])
        # set the background colors of the average score
        self.preferencesDlg.ui.bgRedNumber1.setValue(
            self.configFile["bgColor1"].getRgb()[0])
        self.preferencesDlg.ui.bgGreenNumber1.setValue(
            self.configFile["bgColor1"].getRgb()[1])
        self.preferencesDlg.ui.bgBlueNumber1.setValue(
            self.configFile["bgColor1"].getRgb()[2])
        self.preferencesDlg.ui.bgColorLabel1.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["bgColor1"].name())
        self.preferencesDlg.ui.bgRedNumber2.setValue(
            self.configFile["bgColor2"].getRgb()[0])
        self.preferencesDlg.ui.bgGreenNumber2.setValue(
            self.configFile["bgColor2"].getRgb()[1])
        self.preferencesDlg.ui.bgBlueNumber2.setValue(
            self.configFile["bgColor2"].getRgb()[2])
        self.preferencesDlg.ui.bgColorLabel2.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["bgColor2"].name())
        self.preferencesDlg.ui.bgRedNumber3.setValue(
            self.configFile["bgColor3"].getRgb()[0])
        self.preferencesDlg.ui.bgGreenNumber3.setValue(
            self.configFile["bgColor3"].getRgb()[1])
        self.preferencesDlg.ui.bgBlueNumber3.setValue(
            self.configFile["bgColor3"].getRgb()[2])
        self.preferencesDlg.ui.bgColorLabel3.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["bgColor3"].name())
        self.preferencesDlg.ui.bgRedNumber4.setValue(
            self.configFile["bgColor4"].getRgb()[0])
        self.preferencesDlg.ui.bgGreenNumber4.setValue(
            self.configFile["bgColor4"].getRgb()[1])
        self.preferencesDlg.ui.bgBlueNumber4.setValue(
            self.configFile["bgColor4"].getRgb()[2])
        self.preferencesDlg.ui.bgColorLabel4.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["bgColor4"].name())
        self.preferencesDlg.ui.bgRedNumber5.setValue(
            self.configFile["bgColor5"].getRgb()[0])
        self.preferencesDlg.ui.bgGreenNumber5.setValue(
            self.configFile["bgColor5"].getRgb()[1])
        self.preferencesDlg.ui.bgBlueNumber5.setValue(
            self.configFile["bgColor5"].getRgb()[2])
        self.preferencesDlg.ui.bgColorLabel5.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["bgColor5"].name())
        # check/uncheck the foreground color groupbox of the average score
        self.preferencesDlg.ui.useFgColors.setChecked(
            self.configFile["fgColor"])
        # set the background colors of the average score
        self.preferencesDlg.ui.fgRedNumber1.setValue(
            self.configFile["fgColor1"].getRgb()[0])
        self.preferencesDlg.ui.fgGreenNumber1.setValue(
            self.configFile["fgColor1"].getRgb()[1])
        self.preferencesDlg.ui.fgBlueNumber1.setValue(
            self.configFile["fgColor1"].getRgb()[2])
        self.preferencesDlg.ui.fgColorLabel1.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["fgColor1"].name())
        self.preferencesDlg.ui.fgRedNumber2.setValue(
            self.configFile["fgColor2"].getRgb()[0])
        self.preferencesDlg.ui.fgGreenNumber2.setValue(
            self.configFile["fgColor2"].getRgb()[1])
        self.preferencesDlg.ui.fgBlueNumber2.setValue(
            self.configFile["fgColor2"].getRgb()[2])
        self.preferencesDlg.ui.fgColorLabel2.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["fgColor2"].name())
        self.preferencesDlg.ui.fgRedNumber3.setValue(
            self.configFile["fgColor3"].getRgb()[0])
        self.preferencesDlg.ui.fgGreenNumber3.setValue(
            self.configFile["fgColor3"].getRgb()[1])
        self.preferencesDlg.ui.fgBlueNumber3.setValue(
            self.configFile["fgColor3"].getRgb()[2])
        self.preferencesDlg.ui.fgColorLabel3.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["fgColor3"].name())
        self.preferencesDlg.ui.fgRedNumber4.setValue(
            self.configFile["fgColor4"].getRgb()[0])
        self.preferencesDlg.ui.fgGreenNumber4.setValue(
            self.configFile["fgColor4"].getRgb()[1])
        self.preferencesDlg.ui.fgBlueNumber4.setValue(
            self.configFile["fgColor4"].getRgb()[2])
        self.preferencesDlg.ui.fgColorLabel4.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["fgColor4"].name())
        self.preferencesDlg.ui.fgRedNumber5.setValue(
            self.configFile["fgColor5"].getRgb()[0])
        self.preferencesDlg.ui.fgGreenNumber5.setValue(
            self.configFile["fgColor5"].getRgb()[1])
        self.preferencesDlg.ui.fgBlueNumber5.setValue(
            self.configFile["fgColor5"].getRgb()[2])
        self.preferencesDlg.ui.fgColorLabel5.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["fgColor5"].name())
        # set the current gLineWidth and gLineColor
        self.preferencesDlg.ui.gLineWidth.setValue(
            self.configFile["gLineWidth"])
        self.preferencesDlg.ui.gLineRedNumber.setValue(
            self.configFile["gLineColor"].getRgb()[0])
        self.preferencesDlg.ui.gLineGreenNumber.setValue(
            self.configFile["gLineColor"].getRgb()[1])
        self.preferencesDlg.ui.gLineBlueNumber.setValue(
            self.configFile["gLineColor"].getRgb()[2])
        self.preferencesDlg.ui.gLineColorLabel.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["gLineColor"].name())
        # set the current chart settings
        self.preferencesDlg.ui.showX.setChecked(self.configFile["showXaxis"])
        self.preferencesDlg.ui.showY.setChecked(self.configFile["showYaxis"])
        # set the current chart title settings
        self.preferencesDlg.ui.addTitle.setChecked(
            self.configFile["showChartTitle"])
        self.preferencesDlg.ui.chartTitle.setText(self.configFile["chartTitle"])
        font = QtGui.QFont()
        font.setFamily(self.configFile["chartTitleFont"])
        self.preferencesDlg.ui.chartTitleFont.setCurrentFont(font)
        self.preferencesDlg.ui.chartTitleSize.setValue(
            self.configFile["chartTitleSize"])
        self.preferencesDlg.ui.chartBoldFont.setChecked(
            self.configFile["chartTitleStyle"][0])
        self.preferencesDlg.ui.chartItalicFont.setChecked(
            self.configFile["chartTitleStyle"][1])
        self.preferencesDlg.ui.cTitleRedNumber.setValue(
            self.configFile["chartTitleColor"].getRgb()[0])
        self.preferencesDlg.ui.cTitleGreenNumber.setValue(
            self.configFile["chartTitleColor"].getRgb()[1])
        self.preferencesDlg.ui.cTitleBlueNumber.setValue(
            self.configFile["chartTitleColor"].getRgb()[2])
        self.preferencesDlg.ui.cTitleColorLabel.setStyleSheet(
            "QLabel{ background-color: %s }" %
            self.configFile["chartTitleColor"].name())
        # set the current option of zooming the chart
        self.preferencesDlg.ui.chartZoomOption.setCurrentIndex(
            self.configFile["chartZoomOption"])
        # set the default chart animation option
        self.preferencesDlg.ui.chartAnimation.setCurrentIndex(
            self.configFile["chartAnimation"])
        # set the default chart theme option
        self.preferencesDlg.ui.chartTheme.setCurrentIndex(
            self.configFile["chartTheme"])
        # hide use bold style on positive numbers
        self.preferencesDlg.ui.useBoldAnalysisT.setVisible(False)
        # set the current status of use bold style on positive numbers
        self.preferencesDlg.ui.useBoldAnalysisT.setChecked(
            self.configFile["useBoldAnalysisTable"])
        self.preferencesDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        self.preferencesDlg.exec_()

    def showResetDatabseDlg(self):
        # Show the reset database dialog if the user press the reset database
        # button

        # set the default status of the accept button to disabled
        self.resetDatabaseDlg.ui.acceptButton.setEnabled(False)
        # set the default state of the I read it and I accept to unchecked
        self.resetDatabaseDlg.ui.acceptingCondition.setChecked(False)
        self.resetDatabaseDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resetDatabaseDlg.exec_()

    def showAddTaskDlg(self):
        #  Open the addTask Dialog if the add button is pressed

        self.test = self.timer2.remainingTime()
        # set the current day to date entry
        self.addTaskDlg.ui.dateEntry.setDate(QtCore.QDate.currentDate())
        self.addTaskDlg.ui.dateEntry.setMinimumDate(QtCore.QDate.currentDate())
        # set the focus to the task entry every time we open the add task dialog
        self.addTaskDlg.ui.taskEntry.setFocus(True)
        # clear the last typed task duration
        self.addTaskDlg.ui.durationEntry.setValue(1)
        # add tasks to the dropdown list
        self.updateTaskAdded()
        # set the addTaskButton to disabled by default
        self.addTaskDlg.ui.addTaskButton.setEnabled(False)
        # get the lastFontSetting and set it to the dialog
        fontFamily = self.configFile["lastFontSetting"][0]
        fontSize = self.configFile["lastFontSetting"][1]
        fontStyle = self.configFile["lastFontSetting"][2]
        fontWeight = self.configFile["lastFontSetting"][3]
        rememberFont = self.configFile["lastFontSetting"][4]
        font = QtGui.QFont()
        font.setFamily(fontFamily)
        self.addTaskDlg.ui.fontName.setCurrentFont(font)
        self.addTaskDlg.ui.fontSize.setValue(fontSize)
        self.addTaskDlg.ui.fontStyle.setCurrentText(fontStyle)
        self.addTaskDlg.ui.fontWeight.setCurrentText(fontWeight)
        self.addTaskDlg.ui.fontSetting.setChecked(rememberFont)
        self.addTaskDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        self.addTaskDlg.exec_()

    def showEditTaskDlg(self):
        # by choosing the task and clicking on the edit task button open this
        # dialog we can edit the task name and the duration only

        dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
        row = self.mainWindow.taskTable.currentRow()
        # by default we uncheck the noDurationButton
        self.editTaskDlg.ui.noDurationButton.setChecked(False)
        task = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][0]
        duration = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][1]
        # convert from ms to minute
        elapsedTime = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][13] // 1000 // 60
        # to prevent the program from crashing when it tries to set a value for
        # the spinBox and it founds a string we change the duration to 5 which
        # is the default value
        if duration == -1:
            duration = 1
            self.editTaskDlg.ui.noDurationButton.setChecked(True)
        self.editTaskDlg.ui.taskEditedEntry.setText(task)
        self.editTaskDlg.ui.durationEditedEntry.setValue(duration)
        if elapsedTime > 0:
            self.editTaskDlg.ui.durationEditedEntry.setMinimum(elapsedTime+1)
        else:
            self.editTaskDlg.ui.durationEditedEntry.setMinimum(1)
        self.editTaskDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        self.editTaskDlg.exec_()

    def addTaskFunction(self):
        # We Execute this function if the add button of the addTask dialog is
        # pressed this function will add a task to the chosen legitimate day
        # day can't be in the past like yesterday
        # can't add a task that has been added before to the same day

        task = self.addTaskDlg.ui.taskEntry.currentText()
        # Get the duration value
        duration = self.addTaskDlg.ui.durationEntry.value()
        # Get the day of the task as a QDate object
        date = self.addTaskDlg.ui.dateEntry.date()
        dayFilter = datetime(date.year(), date.month(), date.day()).strftime(
            "%a %B %d %Y")  # format the date object to a string
        monthFilter = datetime(
            date.year(),
            date.month(),
            date.day()).strftime("%B")  # get the month name
        yearFilter = datetime(
            date.year(),
            date.month(),
            date.day()).strftime("%Y")  # get the year
        fontFamily = self.addTaskDlg.ui.fontName.currentFont().family()
        fontSize = self.addTaskDlg.ui.fontSize.value()
        fontStyle = self.addTaskDlg.ui.fontStyle.currentText()
        fontWeight = self.addTaskDlg.ui.fontWeight.currentText()
        createdDatetime = datetime.today()
        modifiedDatetime = createdDatetime
        deletedDatetime = "N/A"
        completedDatetime = "N/A"
        remainingTime = duration*60*1000
        # we will use it to close the dialog if the task has been added
        # succesfully
        taskAdded = False
        # checking if the task is already there or no
        if self.hasTask(task, yearFilter, monthFilter, dayFilter)[0]:
            QtWidgets.QMessageBox.warning(
                self.addTaskDlg, "Warning Message", "Duplicate Tasks Is Not \
                Allowed.\nYou have 3 Solutions to solve that problem.\n1) \
                Delete the existing task.\n2) Change the name of task.\n3) \
                Change the date of the task.")
            taskAdded = False
        # task does not exist in the database
        else:
            # this year does not exist in the self.database file so we have to
            # create the days for this year
            if self.database["tasks"].get(yearFilter, -1) == -1:
                # passing reset as False because we don't want to erase our
                # database and create it from the beginning
                self.createTaskDaysData(yearFilter, reset=False)
            # *[0] Uncompleted tasks
            # *[1] completed tasks
            # *[2] deleted tasks
            # *[*][0] Task
            # *[*][1] Duration
            # *[*][2] Completed Time
            # *[*][3] Font Family
            # *[*][4] Font Point Size
            # *[*][5] Font Style
            # *[*][6] Font Weight
            # *[*][7] Created Time
            # *[*][8] Modified Time
            # *[*][9] Deleted Time
            # *[*][10] Task Start Time
            # *[*][11] Task Stop Time
            # *[*][12] Remaining Task Time in ms
            # *[*][13] Elapsed Task Time in ms
            # *[*][14] Task Notes when we complete a task
            # *[*][15] Revived Time when we complete a task and we revive it
            # check for the noDurationButton if it's check we change the
            # duration variable to N/A
            if self.addTaskDlg.ui.noDurationButton.isChecked():
                duration = -1
                remainingTime = -1
            self.database["tasks"][yearFilter][monthFilter][
                dayFilter][0].append([
                    task,
                    duration,
                    completedDatetime,
                    fontFamily,
                    fontSize,
                    fontStyle,
                    fontWeight,
                    createdDatetime,
                    modifiedDatetime,
                    deletedDatetime,
                    [],
                    [],
                    remainingTime,
                    0,
                    "N/A"])
            # add the current task to the dropdown task list
            self.database["tasks"]["addedTasks"].add(task)
            taskAdded = True
        # we check if the task has been added successfully to close the dialog
        # or we let the dialog open
        if taskAdded:
            # We call this function to update the contents of the table
            self.updateTaskTable()
            # save the last font setting
            self.saveLastFontSetting()
            # check the autoSave option is True or no, True we save otherwise We
            # let the user press on the save button
            if self.autoSaveDatabase:
                # saving our database
                self.saveDatabase()
            else:
                # after we change something in the database we enable the save
                # button and add a star to the titlebar
                self.mainWindow.actionSave.setEnabled(True)
                self.setWindowTitle("Sunrise - {}*".format(self.currentPath))
            # set the focus to the table
            self.mainWindow.taskTable.setFocus(True)
            # get total tasks for that day
            UncompletedTasks = self.totalTasks(dayFilter)
            # select the last item added to the list
            self.mainWindow.taskTable.setCurrentCell(UncompletedTasks[0]-1, 0)
            # start the timer and after 30 seconds the user if he deletes the
            # task, it will affect the average score
            self.timer2.setSingleShot(True)
            self.timer2.start(30000)
            # at the end we close the dialog with accept mode
            self.addTaskDlg.accept()

    def editTaskFunction(self):
        # when clicking on the editTaskButton of the editTaskDlg
        # we change the taskname and the duration
        # and also we change the task name in the autocomplete task list

        dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
        row = self.mainWindow.taskTable.currentRow()
        oldTask = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][0]
        elapsedTime = self.database["tasks"][yearFilter][monthFilter][
            dayFilter][0][row][13]
        newTask = self.editTaskDlg.ui.taskEditedEntry.text()
        newDuration = self.editTaskDlg.ui.durationEditedEntry.value()
        # check if the user has checked the noDurationButton or not
        if self.editTaskDlg.ui.noDurationButton.isChecked():
            newDuration = -1
        modifiedDatetime = datetime.today()
        if not self.hasTask(newTask, yearFilter, monthFilter, dayFilter)[
                            0] or oldTask == newTask:
            # change the task in the dropdown list of the autocomplete task list
            try:
                self.database["tasks"]["addedTasks"].remove(oldTask)
            except KeyError:
                pass
            self.database["tasks"]["addedTasks"].add(newTask)
            # change the old task with the new one in the database
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][0] = newTask
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][1] = newDuration
            # set the modifiedDatetime for the task
            self.database["tasks"][yearFilter][monthFilter][dayFilter][0][
                row][8] = modifiedDatetime
            # change the remaining time
            if newDuration == -1:
                self.database["tasks"][yearFilter][monthFilter][dayFilter][
                    0][row][12] = newDuration
            else:
                # calculate the new remaining time duration - elapsedTime
                self.database["tasks"][yearFilter][monthFilter][dayFilter][
                    0][row][12] = (newDuration * 60 * 1000) - elapsedTime
            # check if the autosave is enabled to save the databas eotehrwise
            # let the user save by pressing the save button
            if self.autoSaveDatabase:
                self.saveDatabase()
            else:
                # after we change something in the database we enable the save
                # button and add a star to the titlebar
                self.mainWindow.actionSave.setEnabled(True)
                self.setWindowTitle("Sunrise - {}*".format(self.currentPath))
            # refreshing the taskTable
            self.updateTaskTable()
            # set the focus to the table
            self.mainWindow.taskTable.setFocus(True)
            # after changing select the same task in the table
            self.mainWindow.taskTable.setCurrentCell(row, 0)
            # closing the dialog after changing
            self.editTaskDlg.accept()
        else:
            QtWidgets.QMessageBox.information(
                self.editTaskDlg, "Information Message",
                "Task already exists with this name.")

    def totalTasks(self, day=None, month=None, year=None):
        # count the numbers of all tasks (completed,Uncompleted,deleted) in the
        # selected day, month, year and return the total tasks as a list
        # no arguments passed the result will be zero
        # you have to pass day only or month with year or year alone, otherwise
        # the result will be zero

        total = list()
        totalUncompleted = list()
        totalCompleted = list()
        totalDeleted = list()
        if day:
            monthFilter = day.split()[1]
            yearFilter = day.split()[-1]  # last item means -1 and it's the year
            for taskList in self.database["tasks"][yearFilter][monthFilter][
                    day]:
                total.append(len(taskList))
        elif month and year:
            # we have three lists inside every date key ucompleted, completed,
            # deleted tasks
            for i in range(3):
                for date in self.database["tasks"][year][month].keys():
                    total.append(
                        len(self.database["tasks"][year][month][date][i]))
                if i == 0:
                    totalUncompleted = total.copy()
                elif i == 1:
                    totalCompleted = total.copy()
                else:
                    totalDeleted = total.copy()
                total.clear()
            total.append(sum(totalUncompleted))
            total.append(sum(totalCompleted))
            total.append(sum(totalDeleted))
        elif year:
            for month in self.database["tasks"][year]:
                for day in month:
                    for taskList in day:
                        total.append(len(taskList))
        else:
            total = 0
        return total

    def resetDatabaseFunction(self):

        # this function will reset the database to the current year
        # it will delete all the tasks for all the years

        self.createTaskDaysData(
            datetime.today().strftime("%Y"),
            reset=True)  # Resetting database tasks
        # saving our database
        self.saveDatabase()
        # upadating the taskTable and the completedTaskTable
        self.updateTaskTable()
        # close the dialog
        self.resetDatabaseDlg.accept()

    def deleteTaskFunction(self):
        # we call this function to delete a task from the list
        # can't delete a completed task

        # this variables contains row and column of the selected items but we
        # need only the row number, the original result it will be like this
        # let's say two items selected
        # row,column,row,column
        selectedRows = self.mainWindow.taskTable.selectedIndexes()
        # we will get only the first number of every 4 numbers
        selectedRows = [i.row() for i in selectedRows][::4]
        # now we have to sort the row numbers from high to lowest one because if
        # we have 4 tasks and we want to delete just 3 of them like this
        # 0 2 3 we can delete the first one but the index 2 will be the item 1
        # and 3 no more exists so we get IndexError
        selectedRows.sort(reverse=True)
        dayFilter, monthFilter, yearFilter = self.getTaskDateFilter()
        try:
            for row in selectedRows:
                deletedDatetime = datetime.today()
                self.database["tasks"][yearFilter][monthFilter][dayFilter][
                    0][row][9] = deletedDatetime
                deletedTask = self.database["tasks"][yearFilter][monthFilter][
                    dayFilter][0].pop(row)
                # check if the task has been added recently or not
                # if yes check the elapsed time if less than 30 seconds just
                # delete it without adding the task to the deletedList
                if row == len(
                        self.database["tasks"][yearFilter][monthFilter]
                        [dayFilter][0]):
                    if self.timer2.remainingTime() > -1:
                        self.timer2.stop()
                    else:
                        self.database["tasks"][yearFilter][monthFilter][
                            dayFilter][2].append(deletedTask)
                else:
                    self.database["tasks"][yearFilter][monthFilter][
                        dayFilter][2].append(deletedTask)
                self.updateTaskTable()
        except IndexError:
            pass
        if self.autoSaveDatabase:
            self.saveDatabase()
        else:
            # after we change something in the database we enable the save
            # button and add a star to the titlebar
            self.mainWindow.actionSave.setEnabled(True)
            self.setWindowTitle("Sunrise - {}*".format(self.currentPath))
        # set the focus to the table
        self.mainWindow.taskTable.setFocus(True)
        # select the first task of the list
        self.mainWindow.taskTable.setCurrentCell(0, 0)

    def closeEvent(self, event):
        # Override the closeEvent of QtWidgets.QMainWindow
        # when the user wants to exit the application has some data not saved
        # warns him or when the user wants to quit the pplication when he starts
        # doing a task stop him

        # the user starts a task means the stop button will be enabled
        # stop him from exiting
        if self.mainWindow.stopTaskButton.isEnabled():
            QtWidgets.QMessageBox.warning(
                self, "Warning Message",
                "Can't close application while working on task.")
            event.ignore()
        else:
            if self.mainWindow.actionSave.isEnabled():
                result = QtWidgets.QMessageBox.question(
                    self, "Quitting Application",
                    "Are you sure you want to quit \
                    the application without saving?")
                if result == QtWidgets.QMessageBox.Yes:
                    self.close()
                else:
                    event.ignore()

    def initiateDatabaseAndConf(self):
        # Initiate the database variables and keys ...etc
        # Initiate the necessary and default configuration parameters

        # get the user home directory
        self.homeDirectory = os.path.expanduser("~")
        # initiating our database variable
        self.database = {"tasks": {}}
        # initiating our config variable
        self.configFile = {}

        # Setting the default config values

        # add the default autosave option of the database
        self.configFile["autoSaveDatabase"] = True
        # get the autoSave option of the database
        self.autoSaveDatabase = self.configFile["autoSaveDatabase"]
        # add the default font settings to the configFile
        # font family, font point size, font style, font weight, remember last
        # font used
        self.configFile["lastFontSetting"] = (
            "Ubuntu", 10, "Normal", "Normal", False)
        # set the default value for the alternating row color
        self.configFile["alternatingRowColors"] = [True, True, True]
        # set the default value for showing the grid of the tables
        self.configFile["showTableGrid"] = [True, True, True]
        # set the default grid style of all the available tables
        self.configFile["tableGridStyle"] = [
            "SolidLine", "SolidLine", "SolidLine"]
        self.configFile["tableGridStyles"] = {
            "SolidLine": QtCore.Qt.SolidLine,
            "DashLine": QtCore.Qt.DashLine,
            "DotLine": QtCore.Qt.DotLine,
            "DashDotLine": QtCore.Qt.DashDotLine,
            "DashDotDotLine": QtCore.Qt.DashDotDotLine}
        # set the current value to show the completed tasks or no
        self.configFile["showCompletedTasks"] = False
        # set the default value for showing the horizontal and vertical headers
        self.configFile["showHorizontalHeaders"] = [True, True, True]
        self.configFile["showVerticalHeaders"] = [False, False, False]
        # set/unset the background color of the average score
        self.configFile["bgColor"] = True
        # set the default background color of the average score
        self.configFile["bgColor1"] = QtGui.QColor(
            0x00, 0x80, 0xFF)  # equivalent to #0080FF Blue variant
        self.configFile["bgColor2"] = QtGui.QColor(
            0x2E, 0xFE, 0x2E)  # equivalent to #2EFE2E Green variant
        # equivalent to #9AFE2E Yellow Green variant
        self.configFile["bgColor3"] = QtGui.QColor(0x9A, 0xFE, 0x2E)
        # equivalent to #FACC2E Orange Yellow Variant
        self.configFile["bgColor4"] = QtGui.QColor(0xFA, 0xCC, 0x2E)
        self.configFile["bgColor5"] = QtGui.QColor(
            0xFE, 0x2E, 0x2E)  # equivalent to #FE2E2E Red Variant
        # set/unset the foreground color of the average score
        self.configFile["fgColor"] = False
        # set the default foreground color of the average score
        self.configFile["fgColor1"] = QtGui.QColor(
            0x00, 0x00, 0x00)  # equivalent to #000000 Black
        self.configFile["fgColor2"] = QtGui.QColor(
            0x00, 0x00, 0x00)  # equivalent to #000000 Black
        self.configFile["fgColor3"] = QtGui.QColor(
            0x00, 0x00, 0x00)  # equivalent to #000000 Black
        self.configFile["fgColor4"] = QtGui.QColor(
            0x00, 0x00, 0x00)  # equivalent to #000000 Black
        self.configFile["fgColor5"] = QtGui.QColor(
            0x00, 0x00, 0x00)  # equivalent to #000000 Black
        # set the default color for the graphic Line
        self.configFile["gLineColor"] = QtGui.QColor(
            0x00, 0x00, 0x00)  # equivalent to #000000 Black
        # set the default graphic Line Width
        self.configFile["gLineWidth"] = 2.5
        # set the default chart settings
        self.configFile["showXaxis"] = True
        self.configFile["showYaxis"] = True
        # set the default chart title settings
        self.configFile["showChartTitle"] = False
        self.configFile["chartTitle"] = ""
        self.configFile["chartTitleFont"] = "Ubuntu"
        self.configFile["chartTitleSize"] = 12
        self.configFile["chartTitleStyle"] = [False, False]  # Bold, Italic
        self.configFile["chartTitleColor"] = QtGui.QColor(
            0x00, 0x00, 0x00)  # equivalent to #000000 Black
        # set the default option for zooming the chart
        self.configFile["chartZoomOption"] = 0
        # set the default chart animation style
        self.configFile["chartAnimation"] = 0  # No animation
        # set the default chart theme
        self.configFile["chartTheme"] = 0  # Light Theme default one
        self.configFile["chartThemes"] = {
            0: QtChart.QChart.ChartThemeLight,
            1: QtChart.QChart.ChartThemeBlueCerulean,
            2: QtChart.QChart.ChartThemeDark,
            3: QtChart.QChart.ChartThemeBrownSand,
            4: QtChart.QChart.ChartThemeBlueNcs,
            5: QtChart.QChart.ChartThemeHighContrast,
            6: QtChart.QChart.ChartThemeBlueIcy,
            7: QtChart.QChart.ChartThemeQt}
        # set the default value for using bold style for positive numbers in the
        # analysisTable
        self.configFile["useBoldAnalysisTable"] = True

        # Setting the file paths for the database and the configFile depending
        # on the operating system

        # we check for windows because windows folder delimiter is a backslash \
        # not a slash / like Linux
        if sys.platform.startswith("win"):
            # add default path of the configFile
            self.configFile["defaultConfigPath"] = self.homeDirectory + \
                "\AppData\Local\HOuadhour\Sunrise\.configFile"
            # add default path of the database
            self.configFile["defaultDatabasePath"] = self.homeDirectory + \
                "\Documents\HOuadhour\Sunrise\database"
            # add the current path of the database
            self.configFile["currentPath"] = self.homeDirectory + \
                "\Documents\HOuadhour\Sunrise\database"
        else:
            # add default path of the configFile
            self.configFile["defaultConfigPath"] = self.homeDirectory + \
                "/.config/HOuadhour/Sunrise/.configFile"
            # add default path of the database
            self.configFile["defaultDatabasePath"] = self.homeDirectory + \
                "/Documents/HOuadhour/Sunrise/database"
            # add the current path of the database
            self.configFile["currentPath"] = self.homeDirectory + \
                "/Documents/HOuadhour/Sunrise/database"
        # get the default path of the configFile
        self.defaultConfigPath = self.configFile["defaultConfigPath"]
        # get the default path of the database
        self.defaultDatabasePath = self.configFile["defaultDatabasePath"]
        # get the current path of the database
        self.currentPath = self.configFile["currentPath"]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyApp()
    myapp.setStyleSheet(open("style.css", "r").read())
    myapp.showMaximized()
    sys.exit(app.exec_())
