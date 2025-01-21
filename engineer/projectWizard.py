# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

from globals import *

from PySide6.QtWidgets import QApplication, QLabel, QDialog, QGridLayout, QLineEdit, QComboBox, QPushButton, QFileDialog

class newProjectWizard(QDialog):
	def __init__(self):
		super().__init__()
		
		layout = QGridLayout()
		
		layout.setColumnMinimumWidth(1, 150)
		layout.setColumnMinimumWidth(0, 50)
		
		self.setWindowTitle("openEarthCAD Engineer - New Project Wizard")
		
		nP_label_info = QLabel("Welcome to the new project wizard. Some information is required about the project. On the next screen, you will be prompted to choose a location to save the project to.")
		nP_label_info.setWordWrap(1)
		
		nP_label_projectName = QLabel("Enter the project name:")
		nP_form_projectName = QLineEdit()
		
		nP_label_projectCRS = QLabel("Choose a CRS:")
		nP_form_projectCRS = QComboBox()
		nP_form_projectCRS.addItems(["WGS84", "Undefined"])
		
		nP_label_projectUnits = QLabel("Choose a unit of measure system:")
		nP_form_projectUnits = QComboBox()
		nP_form_projectUnits.addItems(["feet/inches, acres, cubic yards", "Undefined"])
		
		nP_form_okButton = QPushButton("Next", self)
		
		layout.addWidget(nP_label_info, 0, 1)
		layout.addWidget(nP_label_projectName, 1, 0)
		layout.addWidget(nP_form_projectName, 1, 1)
		layout.addWidget(nP_label_projectCRS, 2, 0)
		layout.addWidget(nP_form_projectCRS, 2, 1)
		layout.addWidget(nP_label_projectUnits, 3, 0)
		layout.addWidget(nP_form_projectUnits, 3, 1)
		layout.addWidget(nP_form_okButton, 6, 3)
		
		#nP_form_okButton.clicked.connect(nPW_SaveDialog)
		
		
		self.setLayout(layout)
		
def newProject_Wizard():
	OEapplication()
	
	projectWizardDialog = newProjectWizard()
	
	projectWizardDialog.exec()
	
	print(nP_form_projectName)
