# Introduction to the Layer File Format

openEarthWorks stores projects in a file with an extension of `*.lyr`. This is a _layer file_.

At its core, this file is a SQLite database, consisting of multiple tables. In theory, you can open this in SQLiteBrowser or similar tools and edit it, though this is not recommended due to potential corruption, and the difficulty navigating the tables by UUID.

There are several types of tables.

- **Index Tables** are used to store basic information about layer tables. In a default layer file, there are typically two or more index tables, depending on which plugins are in use.
  
  - `LAYERS` catalogues all the data layers, usually consisting of elevation and latitude/longitude points
  
  - `PROJECT` contains basic information about the project, including project-specific preferences.

- __Layer Tables__ are usually filled with point data, often containing 3 or more types of data per point, though this is determined by their `Type` as defined in `LAYERS` index table. The names of these tables are their corresponding UUID, effectively allowing an unlimited number of layers without risk of collision.

- __Stake Table__ There is only one stake table (`STAKES`). It lists all stake points for the project. Stakes can be one of two types: Physical or virtual. Stakes can be converted between types.

  - Stakes require some information: Type (`PHYS` or `VIRT`), Location (`LAT`, `LONG`, `ALT`), Task (`PRIMARY_REF`, `REFERENCE`, `MARKER`, `FLAG`, `BOUNDARY`, etc.), UUID, and Name

  - It is recommended to create a physical primary reference stake on the jobsite. This is analagous to a master benchmark. This could be set as a virtual primary reference stake in Engineer and then converted to a phsyical stake later in in Operator, however, care must be taken to ensure that the location is set properly so the design isn't offset by error.

- __Base Table__ is used to manage base stations set up as part of a project. It stores the data necessary to restore a base.

  - Each entry includes a `Name`, `LAT`, `LONG`, and `ALT`.
