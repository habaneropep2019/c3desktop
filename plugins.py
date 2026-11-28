# (C) Copyright 2024 Informed Technology Solutions, LLC
# (C) Copyright 2024, 2026 Alec Bloss
# SPDX-License-Identifier: MPL-2.0

from c3globals import C3Globals


def EnabledPlugins():
    """Returns the list of core plugins enabled at startup."""
    enabled_plugins = ["waterway", "ditch", "pad", "surface"]
    if C3Globals.debug_mode:
        print(f"Enabled plugins: {', '.join(enabled_plugins)}")
    return enabled_plugins


def pluginInfo(name, data=None):
    """
    Query metadata from a plugin.
    Pass just the name, or pass name and <data> for a specific field.
    """
    # Placeholder for plugin registry metadata queries
    implemented = "no"
    return implemented
