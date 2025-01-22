# Introduction to the Layer File Format

openEarthWorks stores projects in a file with an extension of `*.lyr`. This is a _layer file_.

At its core, this file is a SQLite database, consisting of multiple tables. In theory, you can open this in SQLiteBrowser or similar tools and edit it, though this is not recommended due to potential corruption, and the difficulty navigating the tables by UUID.

There are two types of tables: Index tables, and layer tables.

- **Index Tables** are used to store basic information about layer tables. In a default layer file, there are typically two or more index tables, depending on which plugins are in use.
  
  - `REFERENCE_POINTS` lists all tables that contain a reference point.
  
  - `LAYERS` catalogues all the data layers, usually consisting of elevation and latitude/longitude points
  
  - `PROJECT` contains basic information about the project, including project-specific preferences.

- __Layer Tables__ are usually filled with point data, often containing 3 or more types of data per point, though this is determined by their `Type` as defined in `LAYERS` index table. The names of these tables are their corresponding UUID, effectively allowing an unlimited number of layers without risk of collision.
