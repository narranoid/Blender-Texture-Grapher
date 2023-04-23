
from abc import abstractmethod

from .. import StringFormatter
from ... import util as str_util


class StringModifier(StringFormatter):

    def __init__(self):
        super(StringModifier, self).__init__()
    
    def format(self, formattable):
        if str_util.is_string(formattable):
            return self.modify(formattable)
        result = []
        for s in formattable:
            result.append(self.modify(s))
        return result

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
    def modify(self, formattable):
        pass
