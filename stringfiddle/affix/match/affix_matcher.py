
from abc import ABC, abstractmethod

from .. import util as affix_util


class AffixMatcher(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def is_match(self, affixable):
        pass

    def get_best_match(self, matching_items):
        for item in matching_items:
            if self.is_match(item):
                return item
        return None

    def get_matches(self, matching_items):
        matches = list()
        for item in matching_items:
            if self.is_match(item):
                matches.append(item)
        return matches

    def filter_matches(self, filter_items, readonly=False):
        removed_items = set()
        for item in filter_items:
            if self.is_match(item):
                removed_items.add(item)
                if not readonly:
                    filter_items.remove(item)
        return removed_items

    def filter_matches_in_group(self, group, readonly=False):
        matches = self.get_matches(affix_util.find_affixed_groups(group.full_strings))
        removed_items = set()
        for match_group in matches:
            for item in match_group:
                if self.is_match(item):
                    removed_items.add(item)
                    if not readonly:
                        group.discard_string(item.full_string)
        return removed_items
