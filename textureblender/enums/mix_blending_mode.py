
from enum import Enum, auto


class MixBlendingMode(Enum):
    MIX = auto()

    DARKEN = auto()
    MULTIPLY = auto()
    COLOR_BURN = auto()

    LIGHTEN = auto()
    SCREEN = auto()
    COLOR_DODGE = auto()
    ADD = auto()

    OVERLAY = auto()
    SOFT_LIGHT = auto()
    LINEAR_LIGHT = auto()

    DIFFERENCE = auto()
    SUBTRACT = auto()
    DIVIDE = auto()

    HUE = auto()
    SATURATION = auto()
    COLOR = auto()
    VALUE = auto()
