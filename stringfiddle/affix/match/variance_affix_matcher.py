
from .. import AffixedGroup
from . import AffixMatcher


class VarianceAffixMatcher(AffixMatcher):

    def __init__(self, start_num=0, end_num=-1):
        super(VarianceAffixMatcher, self).__init__()
        self._start_number = start_num
        self._end_number = end_num

    def is_match(self, affixable):
        if isinstance(affixable, AffixedGroup):
            return self.calculate_affixed_group_score(affixable)
        return self.calculate_affixed_string_score(affixable)

    def calculate_affixed_string_score(self, affixed_string):
        stem = affixed_string.stem
        if stem.isdigit():
            stem_num = int(stem)
            if self._start_number >= stem_num and \
                    (self._end_number < stem_num or self._end_number < 0):
                return True
        return False

    def calculate_affixed_group_score(self, affixed_group):
        #group_numbers = list()
        for affixed_string in affixed_group:
            if self.calculate_affixed_string_score(affixed_string) <= 0:
                return False
            #else:
            #    group_numbers.append(int(affixed_string.stem))


        #for group_num in group_numbers:

        return True
