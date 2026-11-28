# (C) Copyright 2024 Informed Technology Solutions, LLC
# (C) Copyright 2024, 2026 Alec Bloss
# SPDX-License-Identifier: MPL-2.0

import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QMessageBox


class C3Globals:
    c3_version = "1.0"
    debug_mode = 1  # 0 is disabled, 1 is enabled


class C3App:
    # True indicates saved (default). False indicates unsaved changes.
    SaveStatus = True
    projectName = None
    projectCRS = None
    projectUnits = None
    projectPtDensity = None
    projectFileName = None

    @staticmethod
    def checkIfSaved() -> bool:
        """Returns True if the project is clean, False if dirty."""
        return C3App.SaveStatus is True

    @staticmethod
    def notSavedWarning(parent=None) -> QMessageBox.StandardButton:
        """
        Prompts the user with Save, Discard, or Cancel options.
        Returns the QMessageBox StandardButton selected by the user.
        """
        box = QMessageBox(
            QMessageBox.Warning,
            "Unsaved Changes",
            "The currently open project has unsaved changes.\nWould you like to save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            parent
        )
        box.setDefaultButton(QMessageBox.Save)
        return box.exec()
