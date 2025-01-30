# (C) Copyright 2024 Informed Technology Solutions, LLC 
# SPDX-License-Identifier: BSD-3-Clause

import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QLabel, QDockWidget, QListWidget, QDialog, QPushButton, QFileDialog, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from plugins import *
from about_help import *
from oeglobals import *
from projectWizard import *

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.setWindowTitle("openEarthCAD Engineer")
		
		self.setMinimumSize(1280, 900)
		
		self.dock_windows()
		
		EnabledPlugins()
		
		def openProjectFile(self):
			global project_name
			project_name = QFileDialog.getOpenFileName(None, "Open Project", "", "Layer Files (*.lyr)")
			if OeGlobals.debug_mode:
				print("openProjectFile: Project File Name:", project_name[0])
			if project_name != OeApp.projectFileName: # If a project is already opened
				if OeApp.SaveStatus: # If currently open project is saved
					OeApp.ProjectFileName = project_name[0] # Update currently open project
					# Need to close currently open project
				else:
					OeGlobals.NotSavedWarning() # Display error that current project is not saved. Do nothing.

		# Main Central Widget
		centralLabel = QLabel("This is the main widget")
		centralLabel.setAlignment(Qt.AlignCenter)
		
		self.setCentralWidget(centralLabel)
		
		# Create Main Menubar
		
		menubar = self.menuBar()
		
		# Main Menubar - File menu
		filemenu = menubar.addMenu("&File")
		
		actionPrjNew = QAction("New Project", self)
		actionPrjNew.setStatusTip("Create a new Project")
		actionPrjNew.triggered.connect(newProject_Wizard)
		filemenu.addAction(actionPrjNew)
		
		actionPrjOpen = QAction("Open Project", self)
		actionPrjOpen.setStatusTip("Open a project")
		actionPrjOpen.triggered.connect(openProjectFile)
		filemenu.addAction(actionPrjOpen)
		
		actionPrjExport = QAction("Export Project", self)
		actionPrjExport.setStatusTip("Export a project")
		filemenu.addAction(actionPrjExport)
		
		filemenu.addSeparator()
		
		actionPrjSave = QAction("Save Project", self)
		actionPrjSave.setStatusTip("Save project to disk")
		filemenu.addAction(actionPrjSave)
		
		filemenu.addSeparator()
		
		actionExit = QAction("Exit", self)
		actionExit.setStatusTip("Exit the program")
		filemenu.addAction(actionExit)
		actionExit.triggered.connect(self.close)
		
		# Main Menubar - Edit menu
		filemenu = menubar.addMenu("&Edit")
		
		actionEditCopy = QAction("Copy", self)
		actionEditCopy.setStatusTip("Copy Selection")
		filemenu.addAction(actionEditCopy)
		
		filemenu.addSeparator()
		
		actionEditPreferences = QAction("Preferences", self)
		actionEditPreferences.setStatusTip("Configure program preferences")
		filemenu.addAction(actionEditPreferences)
		
		# Main Menubar - Layers menu
		
		filemenu = menubar.addMenu("&Layers")
		
		actionLayerEditor = QAction("Layer Editor", self)
		actionLayerEditor.setStatusTip("Layer Editor")
		filemenu.addAction(actionLayerEditor)
		
		filemenu.addSeparator()
		
		actionLayerImport = QAction("Import Layer", self)
		actionLayerImport.setStatusTip("Import Layer from various formats")
		filemenu.addAction(actionLayerImport)
		
		# Main Menubar - Help menu
		
		filemenu = menubar.addMenu("&Help")
		
		actionHelpAbout = QAction("About openEarthCAD", self)
		actionHelpAbout.setStatusTip("Information about openEarthCAD")
		actionHelpAbout.triggered.connect(helpAbout)
		filemenu.addAction(actionHelpAbout)
		
		actionQtAbout = QAction("About Qt", self)
		actionQtAbout.setStatusTip("Information about the Qt Toolkit")
		actionQtAbout.triggered.connect(QApplication.aboutQt)
		filemenu.addAction(actionQtAbout)
		
		filemenu.addSeparator()
		
		actionHelpManual = QAction("Manual", self)
		actionHelpManual.setStatusTip("Help Documentation")
		filemenu.addAction(actionHelpManual)
		
	def dock_windows(self):
		# Docked window: Plugins list
		pluginDock = QDockWidget("Plugins", self)
		pluginDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
		self._plugins_list_ = QListWidget(pluginDock)
		self._plugins_list_.addItems((
			"Waterway Feature",
			"Ditch Feature",
			"Pad Feature",
			"Surface Feature"))
		pluginDock.setWidget(self._plugins_list_)
		self.addDockWidget(Qt.LeftDockWidgetArea, pluginDock)
		
		# Docked window: Attributes Editor
		pluginDock = QDockWidget("Attribute Editor", self)
		pluginDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
		self._attribute_editor_ = QLabel("No feature selected!")
		pluginDock.setWidget(self._attribute_editor_)
		self.addDockWidget(Qt.LeftDockWidgetArea, pluginDock)
		
		# Docked window: Layers list
		pluginDock = QDockWidget("Layers", self)
		pluginDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
		self._layer_list_ = QListWidget(pluginDock)
		self._layer_list_.addItems((
			"Project Layer",
			"Main Benchmark",
			"Design Topo",
			"Measured Topo"))
		pluginDock.setWidget(self._layer_list_)
		self.addDockWidget(Qt.RightDockWidgetArea, pluginDock)
		
		# Docked window: Legend
		pluginDock = QDockWidget("Legend", self)
		pluginDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
		self._legend_ = QLabel("No legend available")
		pluginDock.setWidget(self._legend_)
		self.addDockWidget(Qt.RightDockWidgetArea, pluginDock)
		
		def openProjectFile(self):
			project_name, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "All Files (*);;Layer Files (*.lyr)")

	def closeEvent(self, event):
		if OeApp.checkIfSaved is True:
			event.accept()
		else:
			shouldISave = OeApp.notSavedWarning()
			if shouldISave is True:
				event.ignore()
				# Insert save logic here
			else:
				event.accept() # Accept the close event because user doesn't care if they lost work

		
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
