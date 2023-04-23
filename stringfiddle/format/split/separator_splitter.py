
from . import StringSplitter
import re


class SeparatorSplitter(StringSplitter):

    def __init__(self, split_separators=["_", "-", ".", " "]):
        super(SeparatorSplitter, self).__init__()
        self.__split_separators = split_separators

    def split(self, split_string):
        regex_str = "("
        for sep in self.__split_separators:
            regex_str += re.escape(sep) + "|"
        regex_str = regex_str[:-1] + ")"
        regex_result = re.compile(regex_str).split(split_string)
        index = 0
        while index < len(regex_result):
            if regex_result[index] in self.__split_separators:
                del regex_result[index]
            index += 1
        return regex_result
