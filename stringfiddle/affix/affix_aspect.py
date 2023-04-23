
from enum import Flag


class AffixAspect(Flag):
    PREFIX = 1
    POSTFIX = 2
    STEM = 4
    GROUP_LENGTH = 8
    ALL = 15
