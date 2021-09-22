import bpy

class SlideTransitionOperator(bpy.types.Operator):
    """ Create a Slide transition, sliding in one direction """
    bl_idname = "sequencer.slide_transition_operator"
    bl_label = "slide transition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if len(context.selected_sequences) != 2:
            print("TEST")
            return {'FINISHED'}

        bpy.ops.sequencer.effect_strip_add(
            type="ADD",
            frame_start=context.selected_sequences[-1].frame_final_start,
            frame_end=context.selected_sequences[0].frame_final_end)

        return {'FINISHED'}
