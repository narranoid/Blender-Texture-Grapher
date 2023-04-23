
import re

from . import StringModifier


class BlacklistModifier(StringModifier):

    def __init__(self, filter_list, ignore_case=True, filter_count=0):
        super(BlacklistModifier, self).__init__()
        self.__filter_list = filter_list
        self.__ignore_case = ignore_case
        self.__filter_count = filter_count

    def modify(self, n):
        beautified = n
        case_flag = re.IGNORECASE if self.__ignore_case else 0
        for filter_value in self.__filter_list:
            replace_regex = re.compile(re.escape(filter_value), case_flag)
            beautified = replace_regex.sub("", beautified, count=self.__filter_count)
        return beautified
