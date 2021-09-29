import bpy


def preprocess_transition(context):
    """
    Check that the number of strip is appropriate and extract relevant
    information
    """
    if len(context.selected_sequences) != 2:
        return (None, None, None, None)

    seq1 = context.selected_sequences[0]
    seq2 = context.selected_sequences[1]

    frame_start = seq1.frame_final_start
    frame_end = seq2.frame_final_end

    return (seq1, seq2, frame_start, frame_end)


class BlurryTransitionOperator(bpy.types.Operator):

    """
    Create a blurry transition, smoothly changing from one strip to the
    other.
    """
    bl_idname = "sequencer.blurry_transition_operator"
    bl_label = "blurry transition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        seq1, seq2, frame_start, frame_end = preprocess_transition(context)

        if not (seq1 and seq2 and frame_start and frame_end):
            return {'FINISHED'}

        bpy.ops.sequencer.effect_strip_add(
            type='GAMMA_CROSS', frame_start=frame_start, frame_end=frame_end)

        gamma_cross = bpy.context.scene.sequence_editor.sequences.new_effect(
            name=seq2.name + ".gm",
            type='GAMMA_CROSS',
            channel=seq2.channel + 1,
            frame_start=frame_start,
            frame_end=frame_end,
            seq1=seq2,
            seq2=seq1)
        blur = bpy.context.scene.sequence_editor.sequences.new_effect(
            name=seq2.name + ".bl",
            type='GAUSSIAN_BLUR',
            channel=seq2.channel + 2,
            frame_start=frame_start,
            frame_end=frame_end,
            seq1=gamma_cross)

        blur.keyframe_insert("size_x", -1, frame_start)
        blur.keyframe_insert("size_y", -1, frame_start)
        blur.keyframe_insert("size_x", -1, frame_end)
        blur.keyframe_insert("size_y", -1, frame_end)

        blur.size_x = 100
        blur.size_y = 100

        blur.keyframe_insert("size_x", -1, (frame_start + frame_end) / 2)
        blur.keyframe_insert("size_y", -1, (frame_start + frame_end) / 2)

        return {'FINISHED'}
