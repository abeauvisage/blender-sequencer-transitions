import bpy

from .slide_transition import (VerticalSlideTransitionOperator,
                               HorizontalSlideTransitionOperator)
from .blurry_transition import BlurryTransitionOperator
from .blurry_slide_transition import BlurrySlideTransitionOperator
from .proxy_25_operator import Proxy25Operator

bl_info = {
    "name": "Sequencer transitions",
    "blender": (2, 83, 0),
    "category": "Sequencer",
}

LIST_TRANSITION_OPERATORS = [
    VerticalSlideTransitionOperator,
    HorizontalSlideTransitionOperator,
    BlurryTransitionOperator,
    BlurrySlideTransitionOperator,
]

OTHER_OPERATORS = [
    Proxy25Operator
]


def menu_func(self, context):
    self.layout.separator()
    for transition in LIST_TRANSITION_OPERATORS:
        self.layout.operator(transition.bl_idname)


def register():
    for transition in LIST_TRANSITION_OPERATORS:
        bpy.utils.register_class(transition)

    bpy.types.SEQUENCER_MT_add_transitions.append(menu_func)

    for op in OTHER_OPERATORS:
        bpy.utils.register_class(op)


def unregister():
    for transition in LIST_TRANSITION_OPERATORS:
        bpy.utils.unregister_class(transition)

    bpy.types.SEQUENCER_MT_add_transitions.remove(menu_func)

    for op in OTHER_OPERATORS:
        bpy.utils.register_class(op)
