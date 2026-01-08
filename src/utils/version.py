"""
Version detection and comparison utilities for multi-version Blender support.
"""

import bpy


def get_blender_version():
    """
    Returns the current Blender version as a tuple (major, minor, patch).
    
    Returns:
        tuple: (major, minor, patch) version numbers
    """
    return bpy.app.version


def get_version_string():
    """
    Returns the current Blender version as a string (e.g., "4.2.0").
    
    Returns:
        str: Version string in format "major.minor.patch"
    """
    version = get_blender_version()
    return f"{version[0]}.{version[1]}.{version[2]}"


def is_version_at_least(major, minor=0, patch=0):
    """
    Check if the current Blender version is at least the specified version.
    
    Args:
        major (int): Major version number
        minor (int): Minor version number (default: 0)
        patch (int): Patch version number (default: 0)
    
    Returns:
        bool: True if current version >= specified version
    """
    current = get_blender_version()
    target = (major, minor, patch)
    
    if current[0] != target[0]:
        return current[0] > target[0]
    if current[1] != target[1]:
        return current[1] > target[1]
    return current[2] >= target[2]


def is_version_less_than(major, minor=0, patch=0):
    """
    Check if the current Blender version is less than the specified version.
    
    Args:
        major (int): Major version number
        minor (int): Minor version number (default: 0)
        patch (int): Patch version number (default: 0)
    
    Returns:
        bool: True if current version < specified version
    """
    return not is_version_at_least(major, minor, patch)


def is_version_5_0():
    """Check if running Blender 5.0 or later."""
    return is_version_at_least(5, 0, 0)


