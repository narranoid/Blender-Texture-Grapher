
from ..enums import VectorMathOperation
from .internal_node_mix_operation import InternalNodeMixOperation


class ShaderVectorMathOperation(InternalNodeMixOperation):

    @staticmethod
    def get_all_operations():
        return [
            ShaderVectorMathOperation(VectorMathOperation.ADD, "Add", "A + B."),
            ShaderVectorMathOperation(VectorMathOperation.SUBTRACT, "Subtract", "A - B."),
            ShaderVectorMathOperation(VectorMathOperation.MULTIPLY, "Multiply", "Entry-wise multiply."),
            ShaderVectorMathOperation(VectorMathOperation.DIVIDE, "Divide", "Entry-wise divide."),

            ShaderVectorMathOperation(VectorMathOperation.CROSS_PRODUCT, "Cross Product", "A cross B."),
            ShaderVectorMathOperation(VectorMathOperation.PROJECT, "Project", "Project A onto B."),
            ShaderVectorMathOperation(VectorMathOperation.REFLECT, "Reflect", "Reflect A around the normal B. B doesn't need to be normalized."),
            ShaderVectorMathOperation(VectorMathOperation.DOT_PRODUCT, "Dot Product", "A dot B."),

            ShaderVectorMathOperation(VectorMathOperation.DISTANCE, "Distance", "Distance between A and B."),

            ShaderVectorMathOperation(VectorMathOperation.MINIMUM, "Minimum", "Entry-wise minimum."),
            ShaderVectorMathOperation(VectorMathOperation.MAXIMUM, "Maximum", "Entry-wise maximum."),
            ShaderVectorMathOperation(VectorMathOperation.MODULO, "Modulo", "Entry-wise modulo using fmod(A,B)."),
            ShaderVectorMathOperation(VectorMathOperation.SNAP, "Snap", "Round A to the largest integer multiple of B less than or equal A.")
        ]

    def __init__(self, vector_math_operation, name, description):
        super(ShaderVectorMathOperation, self).__init__(vector_math_operation.name, name, description, "ShaderNodeVectorMath")

    @property
    def vector_math_operation(self):
        return VectorMathOperation[self.identifier]

    @property
    def is_two_input_operation(self):
        return self.vector_math_operation in [
            VectorMathOperation.ADD,
            VectorMathOperation.SUBTRACT,
            VectorMathOperation.MULTIPLY,
            VectorMathOperation.DIVIDE,

            VectorMathOperation.CROSS_PRODUCT,
            VectorMathOperation.PROJECT,
            VectorMathOperation.REFLECT,
            VectorMathOperation.DOT_PRODUCT,

            VectorMathOperation.DISTANCE,

            VectorMathOperation.MINIMUM,
            VectorMathOperation.MAXIMUM,
            VectorMathOperation.MODULO,
            VectorMathOperation.SNAP
        ]

    @property
    def is_recommended_for_blending(self):
        return self.vector_math_operation in [
            VectorMathOperation.ADD,
            VectorMathOperation.SUBTRACT,
            VectorMathOperation.MULTIPLY,
            VectorMathOperation.DIVIDE,

            #VectorMathOperation.CROSS_PRODUCT,
            #VectorMathOperation.PROJECT,
            #VectorMathOperation.REFLECT,
            #VectorMathOperation.DOT_PRODUCT,

            #VectorMathOperation.DISTANCE,

            VectorMathOperation.MINIMUM,
            VectorMathOperation.MAXIMUM
            #VectorMathOperation.MODULO,
            #VectorMathOperation.SNAP,
        ]

    def create_mixing_node(self, node_tree):
        mixing_node = super(ShaderVectorMathOperation, self).create_mixing_node(node_tree)
        mixing_node.operation = self.identifier
        return mixing_node
