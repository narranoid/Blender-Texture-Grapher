
from .. import AffixAspect
from . import DynamicScoreAffixMatcher


class ArithmeticScoreAffixMatcher(DynamicScoreAffixMatcher):

    def __init__(self, affix_aspects=AffixAspect.ALL):
        super(ArithmeticScoreAffixMatcher, self).__init__(affix_aspects)

    def init_score(self):
        return 1

    def consider_prefix(self, score, item):
        return score * (item.prefix_length + 1)

    def consider_stem(self, score, item):
        return score * (len(item.stem) + 1)

    def consider_postfix(self, score, item):
        return score * (item.postfix_length + 1)

    def consider_group_length(self, score, group):
        return score * len(group)
