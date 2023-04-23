
from abc import abstractmethod
from ... import util as str_util
from .. import StringFormatter


class StringSplitter(StringFormatter):

    def __init__(self):
        super(StringSplitter, self).__init__()

    def format(self, formattable):
        if str_util.is_string(formattable):
            return self.split(formattable)
        result = []
        for s in formattable:
            sub_split = self.split(s)
            for sub in sub_split:
                result.append(sub)
        return result

    def format_to_string(self, formattable):
        return str_util.plain_join(self.format(formattable))

    def format_to_list(self, formattable, without_empty=True):
        return self.prepare_list(self.format(formattable), without_empty)

    @abstractmethod
    def split(self, split_string):
        pass
