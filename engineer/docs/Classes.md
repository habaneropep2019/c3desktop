# OpenEarthCAD Classes

This document is mainly of interest to developers of the core app or plugins for OECad.

# Import: `oeglobals`

## `OeGlobals`

This class only contains informational variables. They should never be overwritten by any part of the application or plugins.

### `oe_version`

Self explanatory, the version of OpenEarthCAD

### `debug_mode`

Enables debug mode. This generally means a lot of variables are printed to console.

## `OeApp`

This class contains variables and functions that are useful application-wide.

### Variables

- `SaveStatus`: This variable should __never__ be directly written to. A separate class/function will be made available to track all open plugins and files.
- `projectName`: The descriptive name read from the layerfile. Not the filename.
- `projectCRS`: The coordinate reference system chosen for use. Read from the layerfile.
- `projectUnits`: The units of measure system in use. Read from the layerfile.
- `projectPtDensity`: The default point density of the project. Read from the layerfile. This is _not_ a minimum, rather the defaul resolution. Data can be in higher or lower resolutions.
- `projectFileName`: The full path to the layerfile. Gotten from either the command line, the open project menu action, or the new project menu action.

### Classes

#### `notSavedWarning()`

Accepts no arguments. Displays a error message box that says the current project is not saved.



# Import: `layerfile`

This provides functions for working with layerfiles. A connection object, `layerfile`, is provided for access to the database.

## Classes

### `LayerFile`

This class provides functions for creating, opening, and closing layerfiles. It also provides functions for creating and deleting layers, reference points, etc. in the layerfile (creates appropriate tables with UUID names).

#### `create()`

Creates a new layerfile and prepopulates it with required default information. Information is obtained from the `project`.* variables in OeApp, rather than being passed as string arguments. This function will open a connection to the layerfile, populate it, and then immediately commit and close the connection. You will need to call `open()` to actually open the layerfile for use after calling `create`.

#### `open()`

Opens an existing layerfile and loads the basic project information from it into `OeApp.project*` variables.

#### `close()`
