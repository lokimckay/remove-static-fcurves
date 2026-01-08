"""
Utility modules for Remove Static FCurves extension
"""

# Handle module reloading
if "bpy" in locals():
    import importlib
    if "compat" in locals():
        importlib.reload(compat)
    if "version" in locals():
        importlib.reload(version)
else:
    from . import compat
    from . import version

import bpy

__all__ = ["compat", "version"]
