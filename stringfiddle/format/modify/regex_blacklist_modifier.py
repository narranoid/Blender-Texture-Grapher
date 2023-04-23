
import re

from . import StringModifier
from ... import util as str_util


class RegexBlacklistModifier(StringModifier):

    def __init__(self, regular_expressions, flags=0, remove_count=0):
        super(RegexBlacklistModifier, self).__init__()
        if str_util.is_string(regular_expressions):
            regular_expressions = [regular_expressions]
        self.__regex_list = regular_expressions
        self.__flags = flags
        self.__remove_count = remove_count

    def modify(self, n):
        beautified = n
        for r in self.__regex_list:
            replace_regex = re.compile(r, self.__flags)
            beautified = replace_regex.sub("", beautified, count=self.__remove_count)
        return beautified
