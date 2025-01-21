# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

from oeglobals import *

def EnabledPlugins():
	enabledPlugins = ["waterway", "ditch", "pad", "surface"]
	
def pluginInfo(name, data):
	# You can pass just the name, or you can pass name and <data>, where data is the field you want returned
	implemented = "no"
	
