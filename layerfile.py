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

        cursor.execute("CREATE TABLE PROJECT (Project_Name TEXT, 'Creation_Date' INTEGER, Plugins TEXT, OE_VERSION INTEGER)")
        cursor.execute(
            "INSERT INTO PROJECT VALUES (?, ?, ?, ?)",
            (OeApp.projectName, today, None, OeGlobals.oe_version)
        )

        cursor.execute("CREATE TABLE STAKES (UUID TEXT, Name TEXT, Type TEXT, LAT TEXT, LONG TEXT, ALT TEXT, TASK TEXT)")

        connection.commit()
        connection.close()

    def loadProjectInfo(attribute):
        connection = sqlite3.connect(OeApp.projectFileName)
        if OeGlobals.debug_mode:
            print("Value of Attribute:", attribute)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM PROJECT")

        projectInfo = cursor.fetchone()

        match attribute:
            case "Project_Name":
                OeGlobals.projectName = projectInfo[0]
                print("Project Name as loaded:", projectInfo[0])
            case "Creation_Date":
                if OeGlobals.debug_mode:
                    print("Selected Project Attribute:", attribute)
                    print("Attribute Value:", projectInfo[1])
                return projectInfo[1]
            case "Plugins":
                if OeGlobals.debug_mode:
                    print("Selected Project Attribute:", attribute)
                    print("Attribute Value:", projectInfo[2])
                return projectInfo[2]
            case "OE_VERSION":
                if OeGlobals.debug_mode:
                    print("Selected Project Attribute:", attribute)
                    print("Attribute Value:", projectInfo[3])
                return projectInfo[3]

        connection.commit()
        connection.close()
