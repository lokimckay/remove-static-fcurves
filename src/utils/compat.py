"""
API compatibility functions for handling differences between Blender versions.
"""

import bpy
from . import version


def get_action_fcurves(action):
    """
    Get the fcurves collection from an action, handling version differences.
    
    In Blender 4.x: action.fcurves
    In Blender 5.0+: action.animation_data.fcurves or action.groups
    
    Args:
        action: The action object
    
    Returns:
        Collection of fcurves, or None if not available
    """
    # Blender 5.0+ uses animation_data or groups
    if version.is_version_at_least(5, 0, 0):
        # Try animation_data first
        if hasattr(action, 'animation_data') and action.animation_data:
            if hasattr(action.animation_data, 'fcurves'):
                return action.animation_data.fcurves
        # Fallback to groups
        if hasattr(action, 'groups'):
            # In 5.0, fcurves may be accessed through groups
            # Collect fcurves from all groups
            fcurves = []
            for group in action.groups:
                if hasattr(group, 'channels'):
                    fcurves.extend(group.channels)
            return fcurves if fcurves else None
    else:
        # Blender 4.x uses direct fcurves attribute
        if hasattr(action, 'fcurves'):
            return action.fcurves
    
    return None


def remove_action_fcurve(action, fcurve):
    """
    Remove an fcurve from an action, handling version differences.
    
    Args:
        action: The action object
        fcurve: The fcurve to remove
    
    Returns:
        bool: True if removal succeeded, False otherwise
    """
    # Blender 5.0+ uses animation_data or groups
    if version.is_version_at_least(5, 0, 0):
        # Try animation_data first
        if hasattr(action, 'animation_data') and action.animation_data:
            if hasattr(action.animation_data, 'fcurves'):
                try:
                    action.animation_data.fcurves.remove(fcurve)
                    return True
                except (ValueError, AttributeError):
                    pass
        # Fallback to groups
        if hasattr(action, 'groups'):
            for group in action.groups:
                if hasattr(group, 'channels'):
                    try:
                        group.channels.remove(fcurve)
                        return True
                    except (ValueError, AttributeError):
                        continue
    else:
        # Blender 4.x uses direct fcurves attribute
        if hasattr(action, 'fcurves'):
            try:
                action.fcurves.remove(fcurve)
                return True
            except (ValueError, AttributeError):
                pass
    
    return False


