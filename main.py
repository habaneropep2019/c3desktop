# (C) Copyright 2024 Informed Technology Solutions, LLC
# (C) Copyright 2024, 2026 Alec Bloss
# SPDX-License-Identifier: MPL-2.0

import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QLabel, QDockWidget,
    QListWidget, QDialog, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from plugins import *
from about_help import *
from c3globals import C3Globals, C3App
from projectWizard import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("C3Desktop Engineer")
        self.setMinimumSize(1280, 900)

        self.dock_windows()

        EnabledPlugins()

        # Main Central Widget
        centralLabel = QLabel("This is the main widget")
        centralLabel.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(centralLabel)

        # Create Main Menubar
        menubar = self.menuBar()

        # --- File menu ---
        filemenu = menubar.addMenu("&File")

        actionPrjNew = QAction("New Project", self)
        actionPrjNew.setStatusTip("Create a new Project")
        actionPrjNew.triggered.connect(newProject_Wizard)
        filemenu.addAction(actionPrjNew)

        actionPrjOpen = QAction("Open Project", self)
        actionPrjOpen.setStatusTip("Open a project")
        actionPrjOpen.triggered.connect(self.openProjectFile)
        filemenu.addAction(actionPrjOpen)

        actionPrjExport = QAction("Export Project", self)
        actionPrjExport.setStatusTip("Export a project")
        filemenu.addAction(actionPrjExport)

        filemenu.addSeparator()

        actionPrjSave = QAction("Save Project", self)
        actionPrjSave.setStatusTip("Save project to disk")
        actionPrjSave.triggered.connect(self.saveProject)
        filemenu.addAction(actionPrjSave)

        filemenu.addSeparator()

        actionExit = QAction("Exit", self)
        actionExit.setStatusTip("Exit the program")
        actionExit.triggered.connect(self.close)
        filemenu.addAction(actionExit)

        # --- Edit menu ---
        editmenu = menubar.addMenu("&Edit")

        actionEditCopy = QAction("Copy", self)
        actionEditCopy.setStatusTip("Copy Selection")
        editmenu.addAction(actionEditCopy)

        editmenu.addSeparator()

        actionEditPreferences = QAction("Preferences", self)
        actionEditPreferences.setStatusTip("Configure program preferences")
        editmenu.addAction(actionEditPreferences)

        # --- Layers menu ---
        layersmenu = menubar.addMenu("&Layers")

        actionLayerEditor = QAction("Layer Editor", self)
        actionLayerEditor.setStatusTip("Layer Editor")
        layersmenu.addAction(actionLayerEditor)

        layersmenu.addSeparator()

        actionLayerImport = QAction("Import Layer", self)
        actionLayerImport.setStatusTip("Import Layer from various formats")
        layersmenu.addAction(actionLayerImport)

        # --- Help menu ---
        helpmenu = menubar.addMenu("&Help")

        actionHelpAbout = QAction("About C3Desktop", self)
        actionHelpAbout.setStatusTip("Information about C3Desktop")
        actionHelpAbout.triggered.connect(helpAbout)
        helpmenu.addAction(actionHelpAbout)

        actionQtAbout = QAction("About Qt", self)
        actionQtAbout.setStatusTip("Information about the Qt Toolkit")
        actionQtAbout.triggered.connect(QApplication.aboutQt)
        helpmenu.addAction(actionQtAbout)

        helpmenu.addSeparator()

        actionHelpManual = QAction("Manual", self)
        actionHelpManual.setStatusTip("Help Documentation")
        helpmenu.addAction(actionHelpManual)

    def dock_windows(self):
        # Docked window: Plugins list
        pluginDock = QDockWidget("Plugins", self)
        pluginDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._plugins_list_ = QListWidget(pluginDock)
        self._plugins_list_.addItems((
            "Waterway Feature",
            "Ditch Feature",
            "Pad Feature",
            "Surface Feature"
        ))
        pluginDock.setWidget(self._plugins_list_)
        self.addDockWidget(Qt.LeftDockWidgetArea, pluginDock)

        # Docked window: Attributes Editor
        attrDock = QDockWidget("Attribute Editor", self)
        attrDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._attribute_editor_ = QLabel("No feature selected!")
        attrDock.setWidget(self._attribute_editor_)
        self.addDockWidget(Qt.LeftDockWidgetArea, attrDock)

        # Docked window: Layers list
        layerDock = QDockWidget("Layers", self)
        layerDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._layer_list_ = QListWidget(layerDock)
        self._layer_list_.addItems((
            "Project Layer",
            "Main Benchmark",
            "Design Topo",
            "Measured Topo"
        ))
        layerDock.setWidget(self._layer_list_)
        self.addDockWidget(Qt.RightDockWidgetArea, layerDock)

        # Docked window: Legend
        legendDock = QDockWidget("Legend", self)
        legendDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._legend_ = QLabel("No legend available")
        legendDock.setWidget(self._legend_)
        self.addDockWidget(Qt.RightDockWidgetArea, legendDock)

    def openProjectFile(self):
        # If current project has unsaved changes, prompt before opening a new one
        if not C3App.checkIfSaved():
            choice = C3App.notSavedWarning(self)
            if choice == QMessageBox.Save:
                if not self.saveProject():
                    return  # Save failed or was cancelled; abort opening
            elif choice == QMessageBox.Cancel:
                return  # Abort opening

        selected_file, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Layer Files (*.lyr);;All Files (*)"
        )
        if not selected_file:
            return

        if C3Globals.debug_mode:
            print("openProjectFile: Project File Name:", selected_file)

        C3App.projectFileName = selected_file
        # Load project information from layerfile
        try:
            from layerfile import LayerFile
            LayerFile.loadProjectInfo('All')
            C3App.SaveStatus = True
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load project:\n{e}")

    def saveProject(self) -> bool:
        """
        Saves current project. Prompts for a filename if not yet named.
        Returns True on success, False on cancellation or failure.
        """
        if not C3App.projectFileName:
            selected_file, _ = QFileDialog.getSaveFileName(
                self, "Save Project", "", "Layer Files (*.lyr);;All Files (*)"
            )
            if not selected_file:
                return False  # User cancelled the save dialog
            C3App.projectFileName = selected_file

        try:
            # Connect your actual layer/project serialization here:
            # LayerFile.saveProject(C3App.projectFileName)
            C3App.SaveStatus = True
            if C3Globals.debug_mode:
                print(f"Project saved to: {C3App.projectFileName}")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save project:\n{e}")
            return False

    def closeEvent(self, event):
        """Intercepts application close and enforces save checks."""
        if C3App.checkIfSaved():
            event.accept()
            return

        user_choice = C3App.notSavedWarning(self)
        if user_choice == QMessageBox.Save:
            if self.saveProject():
                event.accept()
            else:
                # If save was cancelled or failed, stay in the application
                event.ignore()
        elif user_choice == QMessageBox.Discard:
            event.accept()  # Exit without saving
        else:
            # QMessageBox.Cancel
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
