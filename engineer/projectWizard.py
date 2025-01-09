# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

from globals import *

from PySide6.QtWidgets import QApplication, QLabel, QDialog, QGridLayout, QLineEdit

class newProjectWizard(QDialog):
	def __init__(self):
		super().__init__()
		
		layout = QGridLayout()
		
		self.setWindowTitle("openEarthCAD Engineer - New Project Wizard")
		
		nP_label_info = QLabel("Welcome to the new project wizard. Please fill out the form below.")
		
		nP_label_projectName = QLabel("Enter the project name:")
		
		nP_form_projectName = QLineEdit()
		
		layout.addWidget(nP_label_info, 0, 0)
		layout.addWidget(nP_label_projectName, 1, 0)
		layout.addWidget(nP_form_projectName, 1, 1)
		
		
		self.setLayout(layout)
		
def newProject_Wizard():
	OEapplication()
	
	projectWizardDialog = newProjectWizard()
	
	projectWizardDialog.exec()
