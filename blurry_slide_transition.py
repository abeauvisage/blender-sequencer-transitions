import bpy


def preprocess_transition(context):
    """
    Check that the number of strip is appropriate and extract relevant
    information
    """
    if len(context.selected_sequences) != 2:
        return (None, None, None, None)

    if (context.selected_sequences[0].frame_final_start <
            context.selected_sequences[1].frame_final_start):
        seq1 = context.selected_sequences[0]
        seq2 = context.selected_sequences[1]
    else:
        seq1 = context.selected_sequences[1]
        seq2 = context.selected_sequences[0]

    frame_start = seq2.frame_final_start
    frame_end = seq1.frame_final_end

    return (seq1, seq2, frame_start, frame_end)


class BlurrySlideTransitionOperator(bpy.types.Operator):

    """
    Create a blurry slide transition.
    """
    bl_idname = "sequencer.blurry_slide_transition_operator"
    bl_label = "blurry _slide_transition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        seq1, seq2, frame_start, frame_end = preprocess_transition(context)

        if not (seq1 and seq2 and frame_start and frame_end):
            return {'FINISHED'}

        top_channel = max(seq1.channel, seq2.channel)

        seq1_tf = bpy.context.scene.sequence_editor.sequences.new_effect(
            name=seq1.name + ".gb",
            type='TRANSFORM',
            channel=top_channel + 3,
            frame_start=seq1.frame_final_start,
            frame_end=seq1.frame_final_end,
            seq1=seq1)

        seq2_tf = bpy.context.scene.sequence_editor.sequences.new_effect(
            name=seq2.name + ".gb",
            type='TRANSFORM',
            channel=top_channel + 1,
            frame_start=seq2.frame_final_start,
            frame_end=seq2.frame_final_end,
            seq1=seq2)

        seq1_tf.keyframe_insert("translate_start_x", -1, frame_start)
        seq2_tf.keyframe_insert("translate_start_x", -1, frame_end)
        seq1_tf.keyframe_insert("scale_start_x", -1, frame_start)
        seq2_tf.keyframe_insert("scale_start_x", -1, frame_end)
        seq1_tf.keyframe_insert("scale_start_y", -1, frame_start)
        seq2_tf.keyframe_insert("scale_start_y", -1, frame_end)

        seq1_tf.translate_start_x = -100
        seq2_tf.translate_start_x = 30
        seq1_tf.scale_start_x = 1.0
        seq2_tf.scale_start_x = 1.0
        seq1_tf.scale_start_y = 1.5
        seq2_tf.scale_start_y = 1.5

        seq1_tf.keyframe_insert("translate_start_x", -1, frame_end)
        seq2_tf.keyframe_insert("translate_start_x", -1, frame_start)
        seq1_tf.keyframe_insert("scale_start_x", -1, frame_end)
        seq2_tf.keyframe_insert("scale_start_x", -1, frame_start)
        seq1_tf.keyframe_insert("scale_start_y", -1, frame_end)
        seq2_tf.keyframe_insert("scale_start_y", -1, frame_start)

        seq1_gblur = bpy.context.scene.sequence_editor.sequences.new_effect(
            name=seq1.name + ".gb",
            type='GAUSSIAN_BLUR',
            channel=top_channel + 4,
            frame_start=seq1.frame_final_start,
            frame_end=seq1.frame_final_end,
            seq1=seq1_tf)

        seq2_gblur = bpy.context.scene.sequence_editor.sequences.new_effect(
            name=seq2.name + ".gb",
            type='GAUSSIAN_BLUR',
            channel=top_channel + 2,
            frame_start=seq2.frame_final_start,
            frame_end=seq2.frame_final_end,
            seq1=seq2_tf)

        seq1_gblur.keyframe_insert("size_x", -1, frame_start)
        seq2_gblur.keyframe_insert("size_x", -1, frame_end)

        seq1_gblur.size_x = 100
        seq2_gblur.size_x = 100

        diff_frame = frame_end - frame_start
        seq1_gblur.keyframe_insert(
            "size_x", -1, frame_start + int(diff_frame * 0.1))
        seq2_gblur.keyframe_insert(
            "size_x", -1, frame_end - int(diff_frame * 0.1))

        bpy.context.scene.sequence_editor.sequences.new_effect(
            name=seq2.name + ".ao",
            type='ALPHA_OVER',
            channel=top_channel + 5,
            frame_start=frame_start + int(diff_frame * 0.1),
            frame_end=frame_end - int(diff_frame * 0.1),
            seq1=seq2_gblur,
            seq2=seq1_gblur)

        bpy.ops.sequencer.meta_make()

        return {'FINISHED'}
