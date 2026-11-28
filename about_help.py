# (C) Copyright 2024 Informed Technology Solutions, LLC
# (C) Copyright 2024, 2026 Alec Bloss
# SPDX-License-Identifier: MPL-2.0

from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QWidget
from c3globals import C3Globals


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        # Guard against non-QWidget types (like bool passed from signals)
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)

        self.setWindowTitle("About C3Desktop")

        layout = QHBoxLayout()
        aboutContents = QLabel(
            f"<b>C3Desktop Engineer</b><br>"
            f"Version: {C3Globals.c3_version}<br><br>"
            f"(C) 2024 Informed Technology Solutions, LLC<br>"
            f"(C) 2024, 2026 Alec Bloss<br>"
            f"Licensed under the MPL-2.0"
        )
        layout.addWidget(aboutContents)
        self.setLayout(layout)


def helpAbout(*args, **kwargs):
    """
    Slot for actionHelpAbout.triggered.
    Safely absorbs the Qt `checked: bool` signal parameter.
    """
    parent = kwargs.get("parent", None)
    # If a QWidget was passed positionally, use it as parent
    if args and isinstance(args[0], QWidget):
        parent = args[0]

    dialog = AboutDialog(parent)
    dialog.exec()
