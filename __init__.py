import bpy

from .strip_move_operator import MoveStripOperator
from .slide_transition import (VerticalSlideTransitionOperator,
                               HorizontalSlideTransitionOperator)
from .proxy_25_operator import Proxy25Operator

bl_info = {
    "name": "Sequencer transitions",
    "blender": (2, 83, 0),
    "category": "Sequencer",
}

LIST_TRANSITION_OPERATORS = [
    MoveStripOperator,
    VerticalSlideTransitionOperator,
    HorizontalSlideTransitionOperator,
    Proxy25Operator
]


def menu_func(self, context):
    for transition in LIST_TRANSITION_OPERATORS:
        self.layout.operator(transition.bl_idname)


def register():
    for transition in LIST_TRANSITION_OPERATORS:
        bpy.utils.register_class(transition)

    bpy.types.SEQUENCER_MT_add.append(menu_func)


def unregister():
    for transition in LIST_TRANSITION_OPERATORS:
        bpy.utils.unregister_class(transition)
