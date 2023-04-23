
from enum import Enum


class StringSource(Enum):
    NAME = 1
    LABEL = 2

    # Always image name, even if its a texture, looks up the image below
    IMAGE_NAME = 3

    # Data for objects, Layer name for Vertex Color Node, Texture name for texture node
    DATA_NAME = 4

    FILEPATH = 5

    RAW_FILEPATH = 6
