# (C) Copyright 2021, 2022 Alec Bloss
# (C) Copyright 2024 Informed Technology Solutions, LLC
# SPDX-License-Identifier: BSD-3-Clause

import sys
from PySide6 import QtWidgets, QtGui, Qt, QtCore
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QIcon, QPixmap, QFont
from window import Ui_MainWindow
import rc_resources
import time
import os
from os.path import exists
import configparser
from serial import Serial
from pynmeagps import NMEAReader
import io

MachineList = None

def readSerialGPS(serialdevice, baudrate):
    stream = Serial(serialdevice, baudrate, timeout = 3)
    nmr = NMEAReader(stream)
    (raw_data, parsed_data) = nmr.read()
    print(parsed_data)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # This function is used for diagnostics - enables us to check the raw data coming from the receiver. Needs updated at some point to choose which receiver - it's kinda useless right now.
        def dstream():
            self.dstream = self.datastreamStart.isChecked()
            while self.dstream:
                self.datastreamBrowser.appendPlainText()
                QApplication.processEvents()
        self.datastreamStart.clicked.connect(dstream)

        # Calling this function reads the configuration file each time it's called and creates an implement list.
        def configImplementList():
            config = configparser.ConfigParser()
            config.sections()
            config.read('config.ini')
            config.sections()
            global MachineList
            global MachineListNew
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            print(list(config['Machines'].keys()))
            MachineList = new_stdout.getvalue()
            sys.stdout = old_stdout

            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            print(MachineList.replace("[", ""))
            MachineList = new_stdout.getvalue()
            sys.stdout = old_stdout

            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            print(MachineList.replace("]", ""))
            MachineList = new_stdout.getvalue()
            sys.stdout = old_stdout

            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            print(MachineList.replace("'", ""))
            MachineList = new_stdout.getvalue()
            sys.stdout = old_stdout

            MachineList = MachineList.strip()
            MachineList.replace('\n\n','\n')

            MachineListNew = MachineList.split(',')
        configImplementList()

        # On startup, we want to populate the implement lists.
        self.settingsImplementList.insertItems(1, MachineListNew)
        self.g1d_ImplementList.insertItems(1, MachineListNew)

        # Add ability to add new implement configurations. Just adds an item to the list and adds default values.
        def AddImplement():
            open('config.ini', 'w')
            config = configparser.ConfigParser()
            config['Information'] = {'LGNSSVersion': '1.0', 'CopyrightYears': '2021, 2022', 'config.file.version': '01'}
            config['Machines'] = {'Generic':'Generic'}
            config['generic'] = {'id': 'generic', 'display-name': 'Generic', 'implement.type': 'Survey Only', 'rcvrconfig': 'Single', 'rcvr1.device': '/dev/ttyACM0', 'rcvr1.baudrate': '9600', 'rcvr1.corrections.source': 'Disabled', 'rcvr1.send.corrections.to': 'dev/ttyACM1',
                             'rcvr1.baudrate.2': '9600', 'rcvr1.input.type': 'Disabled', 'rcvr1.receiver.type': 'Generic', 'rcvr1.antenna.height': '0.0', 'rcvr1.dualhead': 'Disabled', 'rcvr1.antenna.type': 'Generic', 'rcvr1.enabled': 'false'}
            config['generic'].update({'rcvr2.device': '/dev/ttyACM2', 'rcvr2.baudrate': '9600', 'rcvr2.corrections.source': 'Disabled', 'rcvr2.send.corrections.to': 'dev/ttyACM3',
                             'rcvr2.baudrate.2': '9600', 'rcvr2.input.type': 'Disabled', 'rcvr2.receiver.type': 'Generic', 'rcvr2.antenna.height': '0.0', 'rcvr2.dualhead': 'Disabled', 'rcvr2.antenna.type': 'Generic', 'rcvr2.enabled': 'false'})
            config['generic'].update({'rcvr3.device': '/dev/ttyACM4', 'rcvr3.baudrate': '9600', 'rcvr3.corrections.source': 'Disabled', 'rcvr3.send.corrections.to': 'dev/ttyACM5',
                             'rcvr3.baudrate.2': '9600', 'rcvr3.input.type': 'Disabled', 'rcvr3.receiver.type': 'Generic', 'rcvr3.antenna.height': '0.0', 'rcvr3.dualhead': 'Disabled', 'rcvr3.antenna.type': 'Generic', 'rcvr3.enabled': 'false'})
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        self.newImplCreate.clicked.connect(AddImplement)

app = QtWidgets.QApplication(sys.argv)

if __name__ == "__main__":

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    pixmap = QPixmap(":/Images/overhead-satellite.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    font = splash.font()
    font.setPixelSize(24)
    font.setWeight(QFont.Bold)
    splash.setFont(font)
    time.sleep(1)
    splash.showMessage("Loading...", alignment=QtCore.Qt.AlignCenter)
    QApplication.processEvents()
    time.sleep(2)
    splash.showMessage("Checking configuration", alignment=QtCore.Qt.AlignCenter)
    QApplication.processEvents()
    time.sleep(2)
    if not os.path.exists('config.ini'):
        splash.showMessage("First run, creating base configuration", alignment=QtCore.Qt.AlignCenter)
        QApplication.processEvents()
        open('config.ini', 'w')
        config = configparser.ConfigParser()
        config['Information'] = {'LGNSSVersion': '1.0', 'CopyrightYears': '2021, 2022', 'config.file.version': '01'}
        config['Machines'] = {'Generic':'Generic'}
        config['generic'] = {'id': 'generic', 'display-name': 'Generic', 'implement.type': 'Survey Only', 'rcvrconfig': 'Single', 'rcvr1.device': '/dev/ttyACM0', 'rcvr1.baudrate': '9600', 'rcvr1.corrections.source': 'Disabled', 'rcvr1.send.corrections.to': 'dev/ttyACM1',
                             'rcvr1.baudrate.2': '9600', 'rcvr1.input.type': 'Disabled', 'rcvr1.receiver.type': 'Generic', 'rcvr1.antenna.height': '0.0', 'rcvr1.dualhead': 'Disabled', 'rcvr1.antenna.type': 'Generic', 'rcvr1.enabled': 'false'}
        config['generic'].update({'rcvr2.device': '/dev/ttyACM2', 'rcvr2.baudrate': '9600', 'rcvr2.corrections.source': 'Disabled', 'rcvr2.send.corrections.to': 'dev/ttyACM3',
                             'rcvr2.baudrate.2': '9600', 'rcvr2.input.type': 'Disabled', 'rcvr2.receiver.type': 'Generic', 'rcvr2.antenna.height': '0.0', 'rcvr2.dualhead': 'Disabled', 'rcvr2.antenna.type': 'Generic', 'rcvr2.enabled': 'false'})
        config['generic'].update({'rcvr3.device': '/dev/ttyACM4', 'rcvr3.baudrate': '9600', 'rcvr3.corrections.source': 'Disabled', 'rcvr3.send.corrections.to': 'dev/ttyACM5',
                             'rcvr3.baudrate.2': '9600', 'rcvr3.input.type': 'Disabled', 'rcvr3.receiver.type': 'Generic', 'rcvr3.antenna.height': '0.0', 'rcvr3.dualhead': 'Disabled', 'rcvr3.antenna.type': 'Generic', 'rcvr3.enabled': 'false'})
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        time.sleep(1)
    splash.showMessage("Loading Events", alignment=QtCore.Qt.AlignCenter)
    QApplication.processEvents()
    time.sleep(1)
    app.processEvents()

window = MainWindow()
window.show()
splash.finish(window)
app.exec()
