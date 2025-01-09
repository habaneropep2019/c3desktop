# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

from PySide6.QtWidgets import QApplication, QLabel, QDialog, QHBoxLayout
from globals import *


class aboutDialog(QDialog):
	def __init__(self):
		super().__init__()
		
		layout = QHBoxLayout()
		
		self.setWindowTitle("About openEarthCAD")
		
		aboutContents = QLabel(f"This is openEarthCAD Engineer, version {oe_version}")
		
		layout.addWidget(aboutContents)
		
		self.setLayout(layout)
		
def helpAbout():
	OEapplication()
	
	helpAboutDialog = aboutDialog()
	
	helpAboutDialog.exec()
	
