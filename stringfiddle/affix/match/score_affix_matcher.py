
from abc import abstractmethod

from . import AffixMatcher


class ScoreAffixMatcher(AffixMatcher):

    def __init__(self):
        super(ScoreAffixMatcher, self).__init__()

    def get_best_match(self, matching_items):
        best_score = 0
        best_match = None
        for item in matching_items:
            item_score = self.calculate_score(item)
            if best_match is None or item_score > best_score:
                best_score = item_score
                best_match = item
        return best_match

    def is_match(self, affixable):
        return self.calculate_score(affixable) <= 0

    @abstractmethod
    def calculate_score(self, affixable):
        pass
