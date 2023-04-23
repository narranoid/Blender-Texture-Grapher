
from .import ListFilter
import re


class RegexFilter(ListFilter):

    def __init__(self, pattern, flags=0, pos=0, endpos=0, whitelist=False):
        super(RegexFilter, self).__init__(whitelist)
        self.__pattern = pattern
        self.__flags = flags
        self.__pos = pos
        self.__endpos = endpos

    def filter(self, items):
        copy = items.copy()
        regex = re.compile(self.__pattern, self.__flags)
        index = len(items)-1

        while index >= 0:
            endpos = self.__endpos if self.__endpos > 0 else len(items[index])
            search_result = regex.search(items[index], self.__pos, endpos)
            if self.whitelist and search_result is None or not self.whitelist and search_result is not None:
                del copy[index]
            index -= 1

        return copy
