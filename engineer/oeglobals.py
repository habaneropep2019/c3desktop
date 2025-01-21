# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

class OeGlobals:
	printGlobal = "Global String Test"
	oe_version = "1.0"
	debug_mode = 0 # 0 is disabled, 1 is enabled

class OeApp:
	SaveStatus = 1 # True indicates it is saved. False (or 0) indicates it is not saved.
	projectName = None
	projectCRS = None
	projectUnits = None
	projectPtDensity = None
	projectFileName = None
