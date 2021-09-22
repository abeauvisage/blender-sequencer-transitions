import bpy

class MoveStripOperator(bpy.types.Operator):
    """ Simple operator moving a strip """
    bl_idname = "sequencer.move_strip_operator"
    bl_label = "move strip"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        window = context.window
        with open("/home/macha/blender.log", "w") as f:

            f.write("nb sequences: " + str(type(context.selected_sequences)))
            for s in context.selected_sequences:
                s.frame_start += 10

                f.write(str(s))

        return {'FINISHED'}
