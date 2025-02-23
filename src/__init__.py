import bpy


class RemoveStaticFcurvesOperator(bpy.types.Operator):
    """Operator to remove static FCurves"""
    bl_idname = "graph.remove_static_fcurves"
    bl_label = "Remove Static FCurves"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        has_selection = any(obj.select_get()
                            for obj in bpy.context.selected_objects)

        if not has_selection:
            self.report({'ERROR_INVALID_INPUT'}, "Please select objects.")
        else:
            self.remove_static_fcurves()
            self.report({'INFO'}, "Removed static animation channels.")
        return {'FINISHED'}

    @staticmethod
    def is_static_fcurve(fcurve):
        """Check if an FCurve is static (all keyframes have the same value)."""
        keyframes = fcurve.keyframe_points
        if len(keyframes) < 2:
            return True  # A single keyframe is considered static

        first_value = keyframes[0].co[1]
        return all(kf.co[1] == first_value for kf in keyframes)

    @staticmethod
    def remove_static_fcurves():
        """Remove static FCurves that have no data."""
        for obj in bpy.context.selected_objects:
            if obj.animation_data and obj.animation_data.action:
                action = obj.animation_data.action
                fcurves_to_remove = [
                    fcurve for fcurve in action.fcurves if RemoveStaticFcurvesOperator.is_static_fcurve(fcurve)]

                for fcurve in fcurves_to_remove:
                    action.fcurves.remove(fcurve)


def menu_func(self, context):
    self.layout.operator(RemoveStaticFcurvesOperator.bl_idname)


def register():
    bpy.utils.register_class(RemoveStaticFcurvesOperator)
    bpy.types.GRAPH_MT_channel.append(menu_func)
    bpy.types.DOPESHEET_MT_channel.append(menu_func)
    print("[Remove Static FCurves] registered")


def unregister():
    bpy.utils.unregister_class(RemoveStaticFcurvesOperator)
    bpy.types.GRAPH_MT_channel.remove(menu_func)
    bpy.types.DOPESHEET_MT_channel.remove(menu_func)
    print("[Remove Static FCurves] unregistered")


if __name__ == "__main__":
    register()
