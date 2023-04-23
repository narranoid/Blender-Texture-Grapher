
from .. import util as str_util
from . import StringFormatter


class CombinedFormatter(StringFormatter):

    def __init__(self, formatting_objects):
        super(CombinedFormatter, self).__init__()
        self.__formatting_objects = formatting_objects

    def iter_strings(self, formattable):
        for current in self.iter_raw(formattable):
            if not str_util.is_string(current):
                yield str_util.plain_join(current)
            else:
                yield current

    def iter_lists(self, formattable):
        for current in self.iter_raw(formattable):
            if str_util.is_string(current):
                yield [current]
            else:
                yield current

    def iter_raw(self, formattable):
        current = formattable if str_util.is_string(formattable) else formattable.copy()
        for formatter in self.__formatting_objects:
            current = formatter.format(current)
            yield current

    def format_to_string(self, formattable):
        raw = self.format(formattable)
        if str_util.is_string(raw):
            return raw
        return str_util.plain_join(raw)

    def format_to_list(self, formattable, without_empty=True):
        raw = self.format(formattable)
        if str_util.is_string(raw):
            return self.prepare_list([raw], without_empty)
        return self.prepare_list(raw, without_empty)
    
    def format(self, formattable):
        current = formattable #if str_util.is_string(formattable) else formattable.copy()
        for formatter in self.__formatting_objects:
            current = formatter.format(current)
        return current
