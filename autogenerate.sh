#!/bin/bash

# (C) Copyright 2026 Alec Bloss
# SPDX-License-Identifier: MPL-2.0

pyside6-uic window.ui -o window.py

pyside6-rcc resources.qrc -o rc_resources.py

pyside6-rcc resources.qrc -o resources_rc.py

rm config.ini
