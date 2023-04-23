
from enum import Flag
from .. import AffixedGroup
from . import AffixMatcher


class BitdepthPreference(Flag):
    HIGHEST = 1
    LOWEST = 2
    ALL = 3
    CUSTOM = 4


class BitdepthAffixMatcher(AffixMatcher):

    def __init__(self, start_depth=8, end_depth=32, preference=BitdepthPreference.HIGHEST, custom_depth=0):
        super(BitdepthAffixMatcher, self).__init__()
        self._start_depth = start_depth
        self._end_depth = end_depth
        self._preference = preference
        self._custom_depth = custom_depth

    def is_match(self, affixable):
        if isinstance(affixable, AffixedGroup):
            return self.check_affixed_group(affixable)
        return self.check_affixed_string(affixable)

    def check_affixed_string(self, affixed_string):
        stem = affixed_string.stem
        if stem.isdigit():
            stem_num = int(stem)
            current_depth = self._start_depth
            while current_depth < self._end_depth:
                if current_depth == stem_num:
                    return True
                current_depth *= 2
            if current_depth == self._end_depth:
                return True
        return False

    def check_affixed_group(self, affixed_group):
        for affixed_string in affixed_group:
            if self.check_affixed_string(affixed_string) <= 0:
                return False
        return True

    @property
    def start_depth(self):
        return self._start_depth

    @property
    def end_depth(self):
        return self._end_depth
