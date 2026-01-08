"""
API compatibility functions for handling differences between Blender versions.
"""
import bpy
from bpy_extras import anim_utils
from . import version


def get_action_fcurves(action):
    """
    Get the fcurves collection from an action, handling version differences.

    In Blender 4.x: action.fcurves
    In Blender 5.0+: Uses channelbag.fcurves via action slots

    Args:
        action: The action object

    Returns:
        Collection of fcurves, or None if not available
    """
    if version.is_version_at_least(5, 0, 0):
        # Blender 5.0+ uses channelbags and slots
        # Try to get fcurves from all slots in the action
        all_fcurves = []

        # Iterate through all slots in the action
        if hasattr(action, 'slots') and action.slots:
            for slot in action.slots:
                try:
                    channelbag = anim_utils.action_get_channelbag_for_slot(
                        action, slot)
                    if channelbag and hasattr(channelbag, 'fcurves'):
                        all_fcurves.extend(channelbag.fcurves)
                except (AttributeError, RuntimeError):
                    continue

        return all_fcurves if all_fcurves else None
    else:
        # Blender 4.x uses direct fcurves attribute
        if hasattr(action, 'fcurves'):
            return action.fcurves

    return None


def get_fcurves_from_object(obj):
    """
    Get FCurves from an object's animation data, handling version differences.

    Args:
        obj: The object with animation data

    Returns:
        List of (action, fcurve, slot) tuples, or empty list
    """
    if not obj.animation_data or not obj.animation_data.action:
        return []

    action = obj.animation_data.action
    fcurves_list = []

    if version.is_version_at_least(5, 0, 0):
        # Blender 5.0+: Get the channelbag for the object's current action slot
        if hasattr(obj.animation_data, 'action_slot') and obj.animation_data.action_slot:
            try:
                channelbag = anim_utils.action_get_channelbag_for_slot(
                    action,
                    obj.animation_data.action_slot
                )
                if channelbag and hasattr(channelbag, 'fcurves'):
                    for fcurve in channelbag.fcurves:
                        fcurves_list.append(
                            (action, fcurve, obj.animation_data.action_slot))
            except (AttributeError, RuntimeError) as e:
                print(f"Error getting channelbag for {obj.name}: {e}")
        else:
            # Fallback: try all slots if no specific slot is set
            if hasattr(action, 'slots') and action.slots:
                for slot in action.slots:
                    try:
                        channelbag = anim_utils.action_get_channelbag_for_slot(
                            action, slot)
                        if channelbag and hasattr(channelbag, 'fcurves'):
                            for fcurve in channelbag.fcurves:
                                fcurves_list.append((action, fcurve, slot))
                    except (AttributeError, RuntimeError):
                        continue
    else:
        # Blender 4.x: Direct access to fcurves
        if hasattr(action, 'fcurves'):
            for fcurve in action.fcurves:
                fcurves_list.append((action, fcurve, None))

    return fcurves_list


def remove_action_fcurve(action, fcurve, slot=None):
    """
    Remove an fcurve from an action, handling version differences.

    Args:
        action: The action object
        fcurve: The fcurve to remove
        slot: (Blender 5.0+) The action slot containing the fcurve

    Returns:
        bool: True if removal succeeded, False otherwise
    """
    if version.is_version_at_least(5, 0, 0):
        # Blender 5.0+: Need to remove from the channelbag
        if slot is None:
            # Try to find which slot contains this fcurve
            if hasattr(action, 'slots'):
                for try_slot in action.slots:
                    try:
                        channelbag = anim_utils.action_get_channelbag_for_slot(
                            action, try_slot)
                        if channelbag and hasattr(channelbag, 'fcurves'):
                            if fcurve in channelbag.fcurves:
                                channelbag.fcurves.remove(fcurve)
                                return True
                    except (ValueError, AttributeError, RuntimeError):
                        continue
        else:
            # We know which slot to use
            try:
                channelbag = anim_utils.action_get_channelbag_for_slot(
                    action, slot)
                if channelbag and hasattr(channelbag, 'fcurves'):
                    channelbag.fcurves.remove(fcurve)
                    return True
            except (ValueError, AttributeError, RuntimeError) as e:
                print(f"Error removing fcurve: {e}")
    else:
        # Blender 4.x: Direct removal
        if hasattr(action, 'fcurves'):
            try:
                action.fcurves.remove(fcurve)
                return True
            except (ValueError, AttributeError):
                pass

    return False
