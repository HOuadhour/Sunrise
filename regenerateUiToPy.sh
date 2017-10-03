#!/usr/bin/bash

pyuic5 designUiFiles/mainDesign.ui -o designPyFiles/mainDesign.py
pyuic5 designUiFiles/addTaskDlg.ui -o designPyFiles/addTaskDlg.py
pyuic5 designUiFiles/preferencesDlg.ui -o designPyFiles/preferencesDlg.py
pyuic5 designUiFiles/resetDatabaseDlg.ui -o designPyFiles/resetDatabaseDlg.py
pyuic5 designUiFiles/editTaskDlg.ui -o designPyFiles/editTaskDlg.py
pyuic5 designUiFiles/taskCompletedMsg.ui -o designPyFiles/taskCompletedMsg.py
pyuic5 designUiFiles/copyTasksDlg.ui -o designPyFiles/copyTasksDlg.py
pyuic5 designUiFiles/taskCompletedDlg.ui -o designPyFiles/taskCompletedDlg.py
