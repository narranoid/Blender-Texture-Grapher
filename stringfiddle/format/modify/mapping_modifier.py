
import re

from . import StringModifier


class MappingModifier(StringModifier):

    def __init__(self, mapping_dict, ignore_key_case=True, replace_count=0):
        super(MappingModifier, self).__init__()
        self.__mapping_dict = mapping_dict
        self.__ignore_key_case = ignore_key_case
        self.__replace_count = replace_count

    def modify(self, n):
        beautified = n
        case_flag = re.IGNORECASE if self.__ignore_key_case else 0
        for key, value in self.__mapping_dict:
            replace_regex = re.compile(re.escape(key), case_flag)
            beautified = replace_regex.sub(value, beautified, count=self.__replace_count)
        return beautified
