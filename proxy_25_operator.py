import bpy

class Proxy25Operator(bpy.types.Operator):
    """ Operator to enable proxy 25 for the Sequencer and rebuilt it """
    bl_idname = "sequencer.set_proxy_25"
    bl_label = "set proxy 25 and rebuild"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.sequencer.enable_proxies(proxy_25=True)
        bpy.ops.sequencer.rebuild_proxy()
        return {'FINISHED'}
