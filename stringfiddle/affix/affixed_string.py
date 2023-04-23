
from . import Affixable


class AffixedString(Affixable):

    def __init__(self, full_string, prefix_index, postfix_index):
        super(AffixedString, self).__init__()
        self._full_string = full_string
        self._prefix_index = prefix_index
        self._postfix_index = postfix_index

    def __str__(self):
        return self._full_string

    @property
    def full_string(self):
        return self._full_string

    @property
    def stem(self):
        if self._postfix_index >= 0 > self._prefix_index:
            return self._full_string
        elif self._postfix_index == 0:
            return self._full_string[self._prefix_index:]
        elif self._prefix_index < 0:
            return self._full_string[:self._postfix_index]
        return self._full_string[self._prefix_index:self._postfix_index]

    @property
    def prefix(self):
        if self._prefix_index < 0:
            return ""
        return self._full_string[0:self._prefix_index]

    @property
    def postfix(self):
        if self._postfix_index == 0:
            return ""
        return self._full_string[self._postfix_index:]

    @property
    def prefix_length(self):
        return self._prefix_index + 1

    @property
    def postfix_length(self):
        return self._postfix_index * -1

    @property
    def prefix_index(self):
        return self._prefix_index

    @property
    def postfix_index(self):
        return self._postfix_index

    @property
    def affixes(self):
        return [self.prefix, self.postfix]
