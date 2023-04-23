
from enum import Enum, auto


class VectorMathOperation(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    CROSS_PRODUCT = auto()
    PROJECT = auto()
    REFLECT = auto()
    DOT_PRODUCT = auto()

    DISTANCE = auto()

    MINIMUM = auto()
    MAXIMUM = auto()
    MODULO = auto()
    SNAP = auto()
