"""
Remove Static FCurves - Blender Extension
Removes animation channels with static (unchanging) values
"""

bl_info = {
    "name": "Remove Static FCurves",
    "author": "lokimckay",
    "version": (0, 3, 0),
    "blender": (5, 0, 0),
    "location": "Graph Editor > Channel > Remove Static FCurves",
    "description": "Remove animation channels with static (unchanging) values",
    "category": "Animation",
}

# Handle module reloading
if "bpy" in locals():
    import importlib
    if "operator" in locals():
        importlib.reload(operator)
    if "utils" in locals():
        importlib.reload(utils)
    print("[Remove Static FCurves] Reloading modules...")
else:
    from . import operator
    from . import utils


def register():
    """Register all classes and handlers"""
    operator.register()
    print("[Remove Static FCurves] Registered")


def unregister():
    """Unregister all classes and handlers"""
    operator.unregister()
    print("[Remove Static FCurves] Unregistered")


if __name__ == "__main__":
    register()
