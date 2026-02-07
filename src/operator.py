"""
Operators for removing static FCurves
"""

import bpy
from . import utils


class RemoveStaticFcurvesOperator(bpy.types.Operator):
    """Operator to remove static FCurves"""
    bl_idname = "graph.remove_static_fcurves"
    bl_label = "Remove Static FCurves"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Get objects with animation data
        objects_to_check = set()

        # Add selected objects
        objects_to_check.update(
            obj for obj in context.selected_objects if obj.animation_data)

        # Add visible objects from Graph Editor if we're in that context
        if context.area and context.area.type == 'GRAPH_EDITOR':
            for obj in context.scene.objects:
                if obj.animation_data and obj.animation_data.action:
                    objects_to_check.add(obj)

        # Also check the active object specifically
        if context.active_object and context.active_object.animation_data:
            objects_to_check.add(context.active_object)

        if not objects_to_check:
            self.report({'WARNING'}, "No objects with animation data found.")
            return {'CANCELLED'}

        print(f"\n=== Remove Static FCurves ===")
        print(f"Checking {len(objects_to_check)} object(s)")

        removed_count = self.remove_static_fcurves(objects_to_check)

        if removed_count > 0:
            self.report(
                {'INFO'}, f"Removed {removed_count} static animation channel(s).")
        else:
            self.report({'INFO'}, "No static FCurves found to remove.")

        return {'FINISHED'}

    @staticmethod
    def is_static_fcurve(fcurve):
        # NEW CONDITION: If the curve has modifiers, keep it
        if fcurve.modifiers and len(fcurve.modifiers) > 0:
            return False

        """Check if an FCurve is static (all keyframes have the same value)."""
        keyframes = fcurve.keyframe_points
        if len(keyframes) < 2:
            return True  # A single keyframe is considered static

        first_value = keyframes[0].co[1]
        tolerance = 0.0001  # Small tolerance for floating point comparison
        return all(abs(kf.co[1] - first_value) < tolerance for kf in keyframes)

    @staticmethod
    def remove_static_fcurves(objects):
        """Remove static FCurves from the given objects."""
        removed_count = 0

        for obj in objects:
            if not obj.animation_data or not obj.animation_data.action:
                continue

            print(f"\nProcessing object: {obj.name}")
            action = obj.animation_data.action
            print(f"  Action: {action.name}")

            # Get FCurves using the compatibility function
            fcurves_data = utils.compat.get_fcurves_from_object(obj)

            if not fcurves_data:
                print(f"  No FCurves found")
                continue

            print(f"  Found {len(fcurves_data)} FCurve(s)")

            # Check each FCurve
            for action, fcurve, slot in fcurves_data:
                is_static = RemoveStaticFcurvesOperator.is_static_fcurve(
                    fcurve)

                if is_static:
                    data_path = fcurve.data_path
                    array_idx = fcurve.array_index
                    print(
                        f"  Removing static FCurve: {data_path}[{array_idx}]")

                    # Remove using the compatibility function
                    if utils.compat.remove_action_fcurve(action, fcurve, slot):
                        removed_count += 1
                    else:
                        print(f"    Failed to remove FCurve")
                else:
                    print(
                        f"  Keeping animated FCurve: {fcurve.data_path}[{fcurve.array_index}]")

        return removed_count


def menu_func(self, context):
    self.layout.operator(RemoveStaticFcurvesOperator.bl_idname)


def register():
    bpy.utils.register_class(RemoveStaticFcurvesOperator)
    bpy.types.GRAPH_MT_channel.append(menu_func)
    bpy.types.DOPESHEET_MT_channel.append(menu_func)
    print("[RemoveStaticFcurvesOperator] registered")


def unregister():
    bpy.utils.unregister_class(RemoveStaticFcurvesOperator)
    bpy.types.GRAPH_MT_channel.remove(menu_func)
    bpy.types.DOPESHEET_MT_channel.remove(menu_func)
    print("[RemoveStaticFcurvesOperator] unregistered")


if __name__ == "__main__":
    register()

