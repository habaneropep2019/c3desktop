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

        cursor.execute("CREATE TABLE PROJECT (Project_Name TEXT, Creation_Date INTEGER, Plugins TEXT, OE_VERSION INTEGER, CRS TEXT, Units TEXT, PtDensity INTEGER)")
        cursor.execute(
            "INSERT INTO PROJECT VALUES (?, ?, ?, ?, ?, ?, ?)",
            (OeApp.projectName, today, None, OeGlobals.oe_version, OeApp.projectCRS, OeApp.projectUnits, OeApp.projectPtDensity)
        )

        cursor.execute("CREATE TABLE STAKES (UUID TEXT, Name TEXT, Type TEXT, LAT TEXT, LONG TEXT, ALT TEXT, TASK TEXT)")

        cursor.execute("CREATE TABLE BASES (Name TEXT, LAT TEXT, LONG TEXT, ALT TEXT)")

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
                if OeGlobals.debug_mode:
                    print("Project Name as loaded:", projectInfo[0])
            case "Creation_Date":
                # We don't really use this right now but it's here to be used in the future
                if OeGlobals.debug_mode:
                    print("Project Creation Date as loaded:", projectInfo[1])
            case "Plugins":
                # We're not using this right now but we will be soon.
                if OeGlobals.debug_mode:
                    print("Project Plugins as loaded:", projectInfo[2])
            case "OE_VERSION":
                # This isn't implemented anywhere yet but once the format is stablized it'll be used to check for version incompatibilities.
                if OeGlobals.debug_mode:
                    print("Project OE_VERSION as loaded:", projectInfo[3])
            case "CRS":
                OeApp.projectCRS = projectInfo[4]
                if OeGlobals.debug_mode:
                    print("Project CRS as loaded:", projectInfo[4])
            case "Units":
                OeApp.projectUnits = projectInfo[5]
                if OeGlobals.debug_mode:
                    print("Project Units as loaded:", projectInfo[5])
            case "PtDensity":
                OeApp.projectPtDensity = projectInfo[6]
                if OeGlobals.debug_mode:
                    print("Project Default Point Density as loaded:", projectInfo[6])
            case "All":
                OeGlobals.projectName = projectInfo[0]
                if OeGlobals.debug_mode:
                    print("Project Name as loaded:", projectInfo[0])
                # We don't really use this right now but it's here to be used in the future
                if OeGlobals.debug_mode:
                    print("Project Creation Date as loaded:", projectInfo[1])
                # We're not using this right now but we will be soon.
                if OeGlobals.debug_mode:
                    print("Project Plugins as loaded:", projectInfo[2])
                 # This isn't implemented anywhere yet but once the format is stablized it'll be used to check for version incompatibilities.
                if OeGlobals.debug_mode:
                    print("Project OE_VERSION as loaded:", projectInfo[3])
                OeApp.projectCRS = projectInfo[4]
                if OeGlobals.debug_mode:
                    print("Project CRS as loaded:", projectInfo[4])
                OeApp.projectUnits = projectInfo[5]
                if OeGlobals.debug_mode:
                    print("Project Units as loaded:", projectInfo[5])
                OeApp.projectPtDensity = projectInfo[6]
                if OeGlobals.debug_mode:
                    print("Project Default Point Density as loaded:", projectInfo[6])

        connection.commit()
        connection.close()

    # Add a new table. This is used to add stake and layer tables. It will generate a new table with appropriate entries, and in the case of layers, will return a UUID. Stake tables return nothing.
    def addTable(tableType):

        connection = sqlite3.connect(OeApp.projectFileName)
        if OeGlobals.debug_mode:
            print("Value of tableType:", tableType)

        cursor = connection.cursor()

        match tableType:
            case "Stake":
                cursor.execute("CREATE TABLE LAYERS (UUID TEXT, Type TEXT, Name TEXT, Qualification TEXT)")
            case "Layer":
                cursor.execute("CREATE TABLE LAYERS (UUID TEXT, Type TEXT, Name TEXT, Qualification TEXT)")

        connection.commit()
        connection.close()

class StakeLayer:

    def newStake(UUID, Name, Type, LAT, LONG, ALT, TASK):

        connection = sqlite3.connect(OeApp.projectFileName)

        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO STAKES VALUES (?, ?, ?, ?, ?, ?, ?)",
            (UUID, Name, Type, LAT, LONG, ALT, TASK)
        )

        connection.commit()
        connection.close()

class BaseLayer:

    def newBase(Name, LAT, LONG, ALT):

        connection = sqlite3.connect(OeApp.projectFileName)

        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO BASES VALUES (?, ?, ?, ?)",
            (Name, LAT, LONG, ALT)
        )

        connection.commit()
        connection.close()
