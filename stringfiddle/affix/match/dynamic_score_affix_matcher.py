
from abc import abstractmethod

from .. import AffixAspect, AffixedGroup
from . import ScoreAffixMatcher


class DynamicScoreAffixMatcher(ScoreAffixMatcher):

    def __init__(self, affix_aspects=AffixAspect.ALL):
        super(DynamicScoreAffixMatcher, self).__init__()
        self._affix_aspects = affix_aspects

    @property
    def score_criteria(self):
        return self._affix_aspects

    def calculate_score(self, affixable):
        score = self.init_score()
        if bool(self._affix_aspects & AffixAspect.PREFIX):
            score = self.consider_prefix(score, affixable)
        if bool(self._affix_aspects & AffixAspect.STEM) > 0:
            score = self.consider_stem(score, affixable)
        if bool(self._affix_aspects & AffixAspect.POSTFIX) > 0:
            score = self.consider_postfix(score, affixable)
        if bool(self._affix_aspects & AffixAspect.GROUP_LENGTH) > 0 and isinstance(affixable, AffixedGroup):
            score = self.consider_group_length(score, affixable)
        return score

    @abstractmethod
    def init_score(self):
        pass

    @abstractmethod
    def consider_prefix(self, score, item):
        pass

    @abstractmethod
    def consider_stem(self, score, item):
        pass

    @abstractmethod
    def consider_postfix(self, score, item):
        pass

    @abstractmethod
    def consider_group_length(self, score, group):
        pass
