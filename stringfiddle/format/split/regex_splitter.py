
from . import StringSplitter
import re


class RegexSplitter(StringSplitter):

    def __init__(self, regex, flags=0):
        super(RegexSplitter, self).__init__()
        self.__regex = regex
        self.__flags = flags

    def split(self, split_string):
        split_regex = re.compile(self.__regex, self.__flags)
        return split_regex.split(split_string)

    @property
    def regex(self):
        return self.__regex
