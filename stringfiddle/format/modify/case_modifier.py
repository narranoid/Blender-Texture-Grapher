
from enum import Flag
from . import StringModifier


class CaseOption(Flag):
    UC_ALL = 5
    LC_ALL = 10

    UC_FIRST = 1
    LC_AFTER_FIRST = 2


class CaseModifier(StringModifier):

    def __init__(self, case_options):
        super(CaseModifier, self).__init__()
        self.__case_options = case_options

    def modify(self, n):
        result = n

        if bool(self.__case_options.value & (CaseOption.UC_ALL.value ^ CaseOption.UC_FIRST.value)):
            result = result.upper()
        elif bool(self.__case_options & CaseOption.UC_FIRST):
            result = result.title()

        if bool(self.__case_options.value & (CaseOption.LC_ALL.value ^ CaseOption.LC_AFTER_FIRST.value)):
            result = result.lower()
        elif bool(self.__case_options & CaseOption.LC_AFTER_FIRST) and len(result) > 1:
            result = result[0] + result[1:].lower()

        return result
