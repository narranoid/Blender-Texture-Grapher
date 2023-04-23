
from abc import abstractmethod

from ... import util as str_util
from .. import StringFormatter


class ListFilter(StringFormatter):

    def __init__(self, whitelist=False):
        super(ListFilter, self).__init__()
        self.__whitelist = whitelist

    def format(self, formattable):
        if str_util.is_string(formattable):
            return self.filter([formattable])
        return self.filter(formattable)

    def format_to_string(self, formattable):
        result = self.format(formattable)
        if not str_util.is_string(result):
            return str_util.plain_join(result)
        return result

    def format_to_list(self, formattable, without_empty=True):
        result = self.format(formattable)
        if str_util.is_string(result):
            return [result]
        return self.prepare_list(result, without_empty)

    @abstractmethod
    def filter(self, items):
        pass

    @property
    def whitelist(self):
        return self.__whitelist

    @whitelist.setter
    def whitelist(self, value):
        self.__whitelist = value
