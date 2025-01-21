# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

from oeglobals import *
import os

from PySide6.QtWidgets import QApplication, QLabel, QDialog, QGridLayout, QLineEdit, QComboBox, QPushButton, QFileDialog
from PySide6.QtGui import QIntValidator


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
		nP_form_projectCRS.addItems(["WGS84", "Undefined"]) # IMPORTANT: Retain order of items! These are parsed by index, not text!
		
		nP_label_projectUnits = QLabel("Choose a unit of measure system:")
		nP_form_projectUnits = QComboBox()
		nP_form_projectUnits.addItems(["feet/inches, acres, cubic yards", "Undefined"])  # IMPORTANT: Retain order of items! These are parsed by index, not text!

		nP_label_projectPtDensity = QLabel("Project default point density (in feet):")
		nP_form_projectPtDensity = QLineEdit()
		nP_form_projectPtDensity.setText("1")
		nP_form_projectPtDensity.setValidator(QIntValidator())
		
		nP_form_okButton = QPushButton("Next", self)

		
		layout.addWidget(nP_label_info, 0, 1)
		layout.addWidget(nP_label_projectName, 1, 0)
		layout.addWidget(nP_form_projectName, 1, 1)
		layout.addWidget(nP_label_projectCRS, 2, 0)
		layout.addWidget(nP_form_projectCRS, 2, 1)
		layout.addWidget(nP_label_projectUnits, 3, 0)
		layout.addWidget(nP_form_projectUnits, 3, 1)
		layout.addWidget(nP_label_projectPtDensity, 4, 0)
		layout.addWidget(nP_form_projectPtDensity, 4, 1)
		layout.addWidget(nP_form_okButton, 6, 3)

		def printForms():
			OeApp.projectName = nP_form_projectName.text()
			OeApp.projectCRS = nP_form_projectCRS.currentIndex()
			OeApp.projectUnits = nP_form_projectUnits.currentIndex()
			OeApp.projectPtDensity = nP_form_projectPtDensity.text()

			if OeGlobals.debug_mode:
				print("Project name:", OeApp.projectName)
				print("Project CRS:", OeApp.projectCRS)
				print("Project Unit of Measure:", OeApp.projectUnits)
				print("Project Point Density:", OeApp.projectPtDensity)

		def nPSaveDialog() :
			nPFileDialog = QFileDialog.getSaveFileName(None, "Save Project", "", "Layer Files (*.lyr)")
			OeApp.projectFileName = nPFileDialog[0]
			if OeGlobals.debug_mode:
				print("New Project Filename:", OeApp.projectFileName)
		
		nP_form_okButton.clicked.connect(printForms)
		nP_form_okButton.clicked.connect(nPSaveDialog)
		nP_form_okButton.clicked.connect(self.close)
		
		
		self.setLayout(layout)
		
def newProject_Wizard():
	
	projectWizardDialog = newProjectWizard()
	
	projectWizardDialog.exec()
	
