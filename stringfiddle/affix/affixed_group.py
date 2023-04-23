
from . import Affixable
from . import AffixedString
from . import util as affix_util


class AffixedGroup(Affixable):

    def __init__(self, strings, prefix_index, postfix_index):
        super(AffixedGroup, self).__init__()
        self._strings = set()
        for s in strings:
            self._strings.add(s)
        self._prefix_index = prefix_index
        self._postfix_index = postfix_index

    def iter_strings(self):
        return iter(self._strings)

    @property
    def full_strings(self):
        return set(self._strings)

    @property
    def stems(self):
        id_array = []
        for n in self:
            id_array.append(n.stem)
        return id_array

    @property
    def sample_stem(self):
        if len(self._strings) > 0:
            return next(iter(self._strings))[self._prefix_index:self._postfix_index]
        return ""

    @property
    def prefix(self):
        if len(self._strings) > 0:
            return next(iter(self._strings))[0:self._prefix_index]
        return ""

    @property
    def postfix(self):
        if len(self._strings) > 0 > self._postfix_index:
            return next(iter(self._strings))[self._postfix_index:]
        return ""

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

    def contains_string(self, string):
        checked_string = affix_util.get_string_checked(string)
        for item in self.iter_strings():
            if checked_string is item:
                return True
        return False

    def discard_string(self, string):
        self._strings.remove(string)

    def __iter__(self):
        return AffixedGroupIterator(self)

    def __len__(self):
        return len(self._strings)

    def __contains__(self, affixed_string):
        for item in self:
            if affixed_string is item:
                return True
        return False
    
    def add(self, affixed_string):
        self._strings.add(affixed_string)

    def discard(self, affixed_string):
        if affixed_string.prefix_index == self.prefix_index and affixed_string.postfix_index == self.postfix_index:
            self._strings.discard(affixed_string.full_string)

    @property
    def affixes(self):
        return [self.prefix, self.postfix]


class AffixedGroupIterator:

    def __init__(self, affixed_group):
        self._affixed_group = affixed_group
        self._string_iter = affixed_group.iter_strings()

    def __next__(self):
        next_string = next(self._string_iter)
        affixed_string = AffixedString(next_string, self._affixed_group.prefix_index, self._affixed_group.postfix_index)
        return affixed_string
