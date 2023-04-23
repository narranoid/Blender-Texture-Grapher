
from . import ListFilter


class IndexFilter(ListFilter):

    def __init__(self, indices, whitelist=False):
        super(IndexFilter, self).__init__(whitelist)
        self.__indices = list(indices)

    def filter(self, items):
        items_copy = list(items)
        indices = list()
        for index in self.__indices:
            normalized_index = index if index >= 0 else len(items_copy) + index
            indices.append(normalized_index)
        indices.sort(reverse=True)

        if self.whitelist:
            index = len(items)-1
            while index >= 0:
                if index not in indices:
                    del items_copy[index]
                index -= 1
        else:
            for index in indices:
                if index < len(items_copy):
                    del items_copy[index]

        return items_copy
