# (C) Copyright 2025 Informed Technology Solutions, LLC
# (C) Copyright 2025, 2026 Alec Bloss
# SPDX-License-Identifier: MPL-2.0

import sqlite3
import datetime
import uuid
from c3globals import C3Globals, C3App


class LayerFile:

    @staticmethod
    def _get_connection():
        """Helper to get a database connection with row access by column name."""
        if not C3App.projectFileName:
            raise ValueError("Cannot access database: C3App.projectFileName is not set.")
        conn = sqlite3.connect(C3App.projectFileName)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def create():
        """
        Creates a new layerfile on disk with the core C3 tables.
        Uses attributes populated on C3App.
        """
        if not C3App.projectFileName:
            raise ValueError("No file path specified in C3App.projectFileName")

        conn = sqlite3.connect(C3App.projectFileName)
        try:
            cursor = conn.cursor()
            today = datetime.date.today().isoformat()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS LAYERS (
                    UUID TEXT PRIMARY KEY,
                    Type TEXT,
                    Name TEXT,
                    Qualification TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PROJECT (
                    Project_Name TEXT,
                    Creation_Date TEXT,
                    Plugins TEXT,
                    C3_VERSION TEXT,
                    CRS TEXT,
                    Units TEXT,
                    PtDensity INTEGER
                )
            """)

            cursor.execute(
                """
                INSERT INTO PROJECT (
                    Project_Name, Creation_Date, Plugins,
                    C3_VERSION, CRS, Units, PtDensity
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    C3App.projectName,
                    today,
                    None,
                    C3Globals.c3_version,
                    C3App.projectCRS,
                    C3App.projectUnits,
                    C3App.projectPtDensity
                )
            )

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS STAKES (
                    UUID TEXT PRIMARY KEY,
                    Name TEXT,
                    Type TEXT,
                    LAT TEXT,
                    LONG TEXT,
                    ALT TEXT,
                    TASK TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS BASES (
                    Name TEXT PRIMARY KEY,
                    LAT TEXT,
                    LONG TEXT,
                    ALT TEXT
                )
            """)

            conn.commit()
            if C3Globals.debug_mode:
                print(f"Project database created at: {C3App.projectFileName}")
        finally:
            conn.close()

    @staticmethod
    def loadProjectInfo(attribute="All"):
        """
        Reads project metadata from the PROJECT table and updates C3App attributes.
        """
        conn = LayerFile._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PROJECT LIMIT 1")
            row = cursor.fetchone()

            if row is None:
                raise ValueError("Project file is empty or corrupted: no PROJECT records found.")

            # Support both new C3_VERSION and legacy OE_VERSION column names
            version_col = "C3_VERSION" if "C3_VERSION" in row.keys() else "OE_VERSION"

            if attribute in ("Project_Name", "All"):
                C3App.projectName = row["Project_Name"]
                if C3Globals.debug_mode:
                    print("Loaded Project Name:", C3App.projectName)

            if attribute in ("Creation_Date", "All"):
                if C3Globals.debug_mode:
                    print("Loaded Creation Date:", row["Creation_Date"])

            if attribute in ("Plugins", "All"):
                if C3Globals.debug_mode:
                    print("Loaded Plugins:", row["Plugins"])

            if attribute in ("C3_VERSION", "OE_VERSION", "All"):
                if C3Globals.debug_mode and version_col in row.keys():
                    print("Loaded Version:", row[version_col])

            if attribute in ("CRS", "All"):
                C3App.projectCRS = row["CRS"]
                if C3Globals.debug_mode:
                    print("Loaded CRS:", C3App.projectCRS)

            if attribute in ("Units", "All"):
                C3App.projectUnits = row["Units"]
                if C3Globals.debug_mode:
                    print("Loaded Units:", C3App.projectUnits)

            if attribute in ("PtDensity", "All"):
                C3App.projectPtDensity = row["PtDensity"]
                if C3Globals.debug_mode:
                    print("Loaded PtDensity:", C3App.projectPtDensity)

        finally:
            conn.close()

    @staticmethod
    def addTable(tableType: str, name: str = "", qualification: str = "") -> str:
        """
        Registers a new layer entry in the LAYERS table and returns its UUID.
        """
        new_uuid = str(uuid.uuid4())
        conn = LayerFile._get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS LAYERS (
                    UUID TEXT PRIMARY KEY,
                    Type TEXT,
                    Name TEXT,
                    Qualification TEXT
                )
            """)

            cursor.execute(
                "INSERT INTO LAYERS (UUID, Type, Name, Qualification) VALUES (?, ?, ?, ?)",
                (new_uuid, tableType, name, qualification)
            )

            conn.commit()
            if C3Globals.debug_mode:
                print(f"Added layer {tableType} ({new_uuid})")
            return new_uuid
        finally:
            conn.close()


class StakeLayer:

    @staticmethod
    def newStake(UUID=None, Name="", Type="", LAT="", LONG="", ALT="", TASK=""):
        """Adds a new stake entry to the STAKES table."""
        if not UUID:
            UUID = str(uuid.uuid4())

        conn = LayerFile._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO STAKES (UUID, Name, Type, LAT, LONG, ALT, TASK) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (UUID, Name, Type, LAT, LONG, ALT, TASK)
            )
            conn.commit()
            return UUID
        finally:
            conn.close()


class BaseLayer:

    @staticmethod
    def newBase(Name, LAT="", LONG="", ALT=""):
        """Adds a new base station entry to the BASES table."""
        conn = LayerFile._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO BASES (Name, LAT, LONG, ALT) VALUES (?, ?, ?, ?)",
                (Name, LAT, LONG, ALT)
            )
            conn.commit()
        finally:
            conn.close()
