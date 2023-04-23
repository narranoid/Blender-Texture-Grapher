
from abc import abstractmethod

from ... import util as str_util
from ...dynamic_path import PathFormat
from ... import dynamic_path as dynamic_path
from .. import StringFormatter


class StringJoiner(StringFormatter):

    def __init__(self):
        super(StringJoiner, self).__init__()

    def format_to_string(self, formattable):
        if str_util.is_string(formattable):
            return formattable
        return self.format(formattable)

    def format_to_list(self, formattable, without_empty=True):
        working_list = [formattable] if str_util.is_string(formattable) else formattable
        return self.prepare_list(working_list, without_empty)

    def format(self, formattable):
        if str_util.is_string(formattable):
            return formattable
        return self.join(formattable)

    @abstractmethod
    def join(self, formattable):
        pass


class SeparatorJoiner(StringJoiner):

    def __init__(self, join_separator):
        super(SeparatorJoiner, self).__init__()
        self.__join_separator = join_separator

    def join(self, formattable):
        return self.__join_separator.join(formattable)


class PathJoiner(StringJoiner):

    def __init__(self, path_format=PathFormat.RUNNING_SYSTEM):
        super(PathJoiner, self).__init__()
        self.__path_format = path_format

    def join(self, formattable):
        return dynamic_path.join(formattable, self.__path_format)
