
from enum import Enum, auto
from ..mix import ShaderMathOperation


class MathOperation(Enum):
    # Functions
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    POWER = auto()
    LOGARITHM = auto()

    # Comparison
    MINIMUM = auto()
    MAXIMUM = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()

    # Rounding
    MODULO = auto()
    SNAP = auto()
    PING_PONG = auto()

    @staticmethod
    def get_two_input_operations():
        return [
            MathOperation.ADD,
            MathOperation.SUBTRACT,
            MathOperation.MULTIPLY,
            MathOperation.DIVIDE,

            MathOperation.POWER,
            MathOperation.LOGARITHM,

            MathOperation.MINIMUM,
            MathOperation.MAXIMUM,
            MathOperation.LESS_THAN,
            MathOperation.GREATER_THAN,

            MathOperation.MODULO,
            MathOperation.SNAP,
            MathOperation.PING_PONG
        ]
