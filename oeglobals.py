# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QMessageBox

class OeGlobals:
	oe_version = "1.0"
	debug_mode = 0 # 0 is disabled, 1 is enabled

class OeApp:
	SaveStatus = True # True indicates it is saved, and is the default. False (or 0) indicates it is not saved. This should NEVER be directly accessed by a plugin. Use OeApp.checkIfSaved
	projectName = None
	projectCRS = None
	projectUnits = None
	projectPtDensity = None
	projectFileName = None

	def notSavedWarning():
		notSavedDialog = QMessageBox.question(None, "Unsaved Work", "The currently open project is not saved. Would you like to save it before exiting?", QMessageBox.Yes | QMessageBox.No)
		if notSavedDialog == QMessageBox.Yes:
			return True
		else:
			return False

	def checkIfSaved():
		if OeApp.SaveStatus is True:
			return True
		else:
			return False
