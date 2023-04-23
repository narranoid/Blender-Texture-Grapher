
from . import StringFormatter


class NoneFormatter(StringFormatter):

    def __init__(self):
        super(NoneFormatter, self).__init__()

    def format(self, string_obj):
        return string_obj

    def format_to_string(self, string_obj):
        return string_obj

    def format_to_list(self, string_seq, without_empty=True):
        return string_seq
