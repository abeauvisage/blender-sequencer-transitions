import bpy

bl_info = {
    "name": "Move strip",
    "blender": (2, 83, 0),
    "category": "Sequencer",
}

class MoveStripOperator(bpy.types.Operator):
    """ Simple operator moving a strip """
    bl_idname = "sequencer.move_strip_operator"
    bl_label = "move strip"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        window = context.window
        with open("/home/macha/blender.log", "w") as f:

            for s in context.selected_sequences:
                s.frame_start += 10

                f.write(str(s))

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SimpleTestOperator.bl_idname)

def register():
    bpy.utils.register_class(MoveStripOperator)
    bpy.types.SEQUENCER_MT_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MoveStripOperator)

if __name__ == "__main__":
    register()
