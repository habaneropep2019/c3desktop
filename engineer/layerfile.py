# (C) Copyright 2025 Informed Technology Solutions, LLC
# SPDX-License-Identifier: BSD-3-Clause

from oeglobals import *
import sqlite3
import datetime

class LayerFile:

    # LayerFile.create - creates a new layerfile, including all the basic tables required.
    # project(Name, CRS, Units, PtDensity, FileName are all gotten from OeApp)
    def create():
        connection = sqlite3.connect(OeApp.projectFileName)

        today = datetime.date.today()

        cursor = connection.cursor()
        cursor.execute("CREATE TABLE LAYERS (UUID TEXT, Type TEXT, Name TEXT, Qualification TEXT)")
        cursor.execute("CREATE TABLE PROJECT ('Project Name' TEXT, 'Creation Date' INTEGER, Plugins TEXT, OE_VERSION INTEGER)")
        cursor.execute(
            "INSERT INTO PROJECT VALUES (?, ?, ?, ?)",
            (OeApp.projectName, today, None, OeGlobals.oe_version)
        )

        connection.commit()
        connection.close()
