# (C) Copyright 2025 Informed Technology Solutions, LLC
# SPDX-License-Identifier: BSD-3-Clause

import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QLabel, QDockWidget, QListWidget, QDialog, QPushButton, QFileDialog, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from oeglobals import *


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.setWindowTitle("openEarthCAD Operator")
		
		self.setMinimumSize(1280, 800)

		# Main Central Widget
		centralLabel = QLabel("This is the main widget")
		centralLabel.setAlignment(Qt.AlignCenter)
		
		self.setCentralWidget(centralLabel)
		
# TODO - This should be changed to automatically save any open projects.
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
