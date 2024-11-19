#!/bin/bash

# (C) Copyright 2024 Informed Technology Solutions, LLC
# SPDX-License-Identifier: BSD-3-Clause

pyside6-uic window.ui -o window.py

pyside6-rcc resources.qrc -o rc_resources.py

pyside6-rcc resources.qrc -o resources_rc.py

rm config.ini
