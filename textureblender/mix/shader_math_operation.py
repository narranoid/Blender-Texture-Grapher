
from ..enums import MathOperation
from .internal_node_mix_operation import InternalNodeMixOperation


class ShaderMathOperation(InternalNodeMixOperation):

    @staticmethod
    def get_all_operations():
        return [
            ShaderMathOperation(MathOperation.ADD, "Add", "A + B."),
            ShaderMathOperation(MathOperation.SUBTRACT, "Subtract", "A - B."),
            ShaderMathOperation(MathOperation.MULTIPLY, "Multiply", "A * B."),
            ShaderMathOperation(MathOperation.DIVIDE, "Divide", "A / B."),

            ShaderMathOperation(MathOperation.POWER, "Power", "A power B."),
            ShaderMathOperation(MathOperation.LOGARITHM, "Logarithm", "Logarithm A base B."),

            ShaderMathOperation(MathOperation.MINIMUM, "Minimum", "The minimum from A and B."),
            ShaderMathOperation(MathOperation.MAXIMUM, "Maximum", "The maximum from A and B."),
            ShaderMathOperation(MathOperation.LESS_THAN, "Less Than", "1 if A < B else 0."),
            ShaderMathOperation(MathOperation.GREATER_THAN, "Greater Than", "1 if A > B else 0."),

            ShaderMathOperation(MathOperation.MODULO, "Modulo", "Modulo using fmod(A,B)."),
            ShaderMathOperation(MathOperation.SNAP, "Snap", "Snap to increment, snap(A,B)."),
            ShaderMathOperation(MathOperation.PING_PONG, "Ping Pong", "Wraps a value and reverses every other cycle (A,B).")
        ]

    def __init__(self, math_operation, name, description):
        super(ShaderMathOperation, self).__init__(math_operation.name, name, description, "ShaderNodeMath")

    @property
    def math_operation(self):
        return MathOperation[self.identifier]

    @property
    def is_two_input_operation(self):
        return self.math_operation in [
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

    @property
    def is_recommended_for_blending(self):
        return self.math_operation in [
            MathOperation.ADD,
            MathOperation.SUBTRACT,
            MathOperation.MULTIPLY,
            MathOperation.DIVIDE,

            #MathOperation.POWER,
            #MathOperation.LOGARITHM,

            MathOperation.MINIMUM,
            MathOperation.MAXIMUM
            #MathOperation.LESS_THAN,
            #MathOperation.GREATER_THAN,

            #MathOperation.MODULO,
            #MathOperation.SNAP,
            #MathOperation.PING_PONG
        ]

    def create_mixing_node(self, node_tree):
        mixing_node = super(ShaderMathOperation, self).create_mixing_node(node_tree)
        mixing_node.operation = self.identifier
        return mixing_node
