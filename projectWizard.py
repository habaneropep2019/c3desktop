# (C) Copyright 2024 Informed Technology Solutions, LLC
# (C) Copyright 2024, 2026 Alec Bloss
# SPDX-License-Identifier: MPL-2.0

import os
from PySide6.QtWidgets import (
    QDialog, QGridLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt

from c3globals import C3Globals, C3App
from layerfile import LayerFile


class NewProjectWizard(QDialog):
    def __init__(self, parent=None):
        # Guard against non-QWidget types
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)

        self.setWindowTitle("C3Desktop Engineer - New Project Wizard")
        self.setMinimumWidth(480)

        layout = QGridLayout()
        layout.setColumnMinimumWidth(0, 140)
        layout.setColumnMinimumWidth(1, 260)

        # Info header
        info_label = QLabel(
            "Welcome to the new project wizard. Enter the basic parameters below, "
            "then click 'Next' to choose where to save the project file."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label, 0, 0, 1, 2)

        # Project Name
        layout.addWidget(QLabel("Project Name:"), 1, 0)
        self.form_projectName = QLineEdit()
        self.form_projectName.setPlaceholderText("Untitled Project")
        layout.addWidget(self.form_projectName, 1, 1)

        # Project CRS
        layout.addWidget(QLabel("Coordinate System (CRS):"), 2, 0)
        self.form_projectCRS = QComboBox()
        # Retain order: parsed by index
        self.form_projectCRS.addItems(["WGS84", "Undefined"])
        layout.addWidget(self.form_projectCRS, 2, 1)

        # Unit of Measure
        layout.addWidget(QLabel("Unit of Measure:"), 3, 0)
        self.form_projectUnits = QComboBox()
        # Retain order: parsed by index
        self.form_projectUnits.addItems(["feet/inches, acres, cubic yards", "Undefined"])
        layout.addWidget(self.form_projectUnits, 3, 1)

        # Point Density
        layout.addWidget(QLabel("Default Point Density (ft):"), 4, 0)
        self.form_projectPtDensity = QLineEdit()
        self.form_projectPtDensity.setText("1")
        self.form_projectPtDensity.setValidator(QIntValidator(1, 10000, self))
        layout.addWidget(self.form_projectPtDensity, 4, 1)

        # Action Buttons
        self.btn_next = QPushButton("Next")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_next.clicked.connect(self._on_accept)
        self.btn_cancel.clicked.connect(self.reject)

        layout.addWidget(self.btn_cancel, 6, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.btn_next, 6, 1, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def _on_accept(self):
        """Validates inputs, prompts for file location, and initializes the project."""
        name = self.form_projectName.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter a project name.")
            self.form_projectName.setFocus()
            return

        # Prompt for target project file
        default_file = f"{name}.lyr" if name else "project.lyr"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save New Project", default_file, "Layer Files (*.lyr);;All Files (*)"
        )

        # If user cancelled file selection, abort and stay in wizard
        if not file_path:
            return

        # Commit attributes to global context
        C3App.projectName = name
        C3App.projectCRS = self.form_projectCRS.currentIndex()
        C3App.projectUnits = self.form_projectUnits.currentIndex()
        C3App.projectPtDensity = self.form_projectPtDensity.text()
        C3App.projectFileName = file_path

        if C3Globals.debug_mode:
            print(f"Project Name: {C3App.projectName}")
            print(f"Project CRS index: {C3App.projectCRS}")
            print(f"Project Units index: {C3App.projectUnits}")
            print(f"Project Point Density: {C3App.projectPtDensity}")
            print(f"Project File: {C3App.projectFileName}")

        # Initialize project file on disk
        try:
            LayerFile.create()
            C3App.SaveStatus = True
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Creation Failed", f"Could not create project file:\n{e}")


def newProject_Wizard(*args, **kwargs):
    """
    Slot for actionPrjNew.triggered.
    Safely absorbs the Qt `checked: bool` signal parameter.
    """
    parent = kwargs.get("parent", None)
    if args and isinstance(args[0], QWidget):
        parent = args[0]

    wizard = NewProjectWizard(parent)
    return wizard.exec()
