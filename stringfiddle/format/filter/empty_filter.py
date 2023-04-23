
from . import ListFilter


class EmptyFilter(ListFilter):

    def __init__(self, whitelist=False):
        super(EmptyFilter, self).__init__(whitelist)

    def filter(self, items):
        copy = items.copy()
        index = len(items)-1

        while index >= 0:
            item = items[index]
            if self.whitelist and len(item) > 0 or not self.whitelist and len(item) <= 0:
                del copy[index]
            index -= 1

        return copy
