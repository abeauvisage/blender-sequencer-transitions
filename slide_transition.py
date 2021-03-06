import bpy


def preprocess_transition(context):
    """
    Check that the number of strip is appropriate and extract relevant
    information
    """
    if len(context.selected_sequences) != 2:
        return None

    seq1 = context.selected_sequences[0]
    seq2 = context.selected_sequences[1]

    frame_start = seq1.frame_final_start
    frame_end = seq2.frame_final_end

    return (seq1, seq2, frame_start, frame_end)


def createTransition(context, axis="x"):

    seq1, seq2, frame_start, frame_end = preprocess_transition(context)

    if not (seq1 and seq2 and frame_start and frame_end):
        return {'FINISHED'}

    transform = bpy.context.scene.sequence_editor.sequences.new_effect(
        name=seq2.name + ".tr",
        type='TRANSFORM',
        channel=seq2.channel + 1,
        frame_start=frame_start,
        frame_end=frame_end,
        seq1=seq2)

    transform.keyframe_insert("translate_start_" + axis, -1, frame_start)
    transform.translate_start_y = -100
    transform.keyframe_insert("translate_start_" + axis, -1, frame_end)

    alpa_under = bpy.context.scene.sequence_editor.sequences.new_effect(
        name=seq2.name + ".au",
        type='ALPHA_UNDER',
        channel=seq2.channel + 2,
        frame_start=frame_start,
        frame_end=frame_end,
        seq1=transform,
        seq2=seq1)

    bpy.ops.sequencer.meta_make()


class VerticalSlideTransitionOperator(bpy.types.Operator):
    """ Create a vertical Slide transition, sliding in one direction """
    bl_idname = "sequencer.v_slide_transition_operator"
    bl_label = "vertical slide transition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        createTransition(context=context, axis="y")

        return {'FINISHED'}


class HorizontalSlideTransitionOperator(bpy.types.Operator):
    """ Create an horizontal Slide transition, sliding in one direction """
    bl_idname = "sequencer.h_slide_transition_operator"
    bl_label = "horizontal slide transition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        createTransition(context=context, axis="x")

        return {'FINISHED'}
