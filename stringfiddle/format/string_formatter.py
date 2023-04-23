
from abc import ABC, abstractmethod
from .. import util as str_util


class StringFormatter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def format(self, string_obj):
        pass

    @abstractmethod
    def format_to_string(self, string_obj):
        pass

    @abstractmethod
    def format_to_list(self, string_seq, without_empty=True):
        pass

    @staticmethod
    def prepare_list(prep_list, without_empty=True):
        if without_empty:
            return str_util.without_empty(prep_list)
        return prep_list
