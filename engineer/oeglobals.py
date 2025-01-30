# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

class OeGlobals:
	oe_version = "1.0"
	debug_mode = 0 # 0 is disabled, 1 is enabled

class OeApp:
	SaveStatus = 1 # True indicates it is saved. False (or 0) indicates it is not saved. This should NEVER be directly written by a plugin, though it can be read directly.
	projectName = None
	projectCRS = None
	projectUnits = None
	projectPtDensity = None
	projectFileName = None

	def notSavedWarning():
		notSavedDialog = QErrorMessage()
		notSavedDialog.showMessage("The currently open project has not been saved. Please save the project before opening a new one.")
