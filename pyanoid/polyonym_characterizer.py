
from ..stringfiddle.affinity.acronym_affinity_evaluator import AcronymAffinityEvaluator
from ..stringfiddle.affinity.combined_affinity_evaluator import CombinedAffinityEvaluator
from ..stringfiddle.affinity.match_affinity_evaluator import MatchAffinityEvaluator
from ..stringfiddle.affinity.initialism_affinity_evaluator import InitialismAffinityEvaluator
from ..stringfiddle.format import CombinedFormatter
from ..stringfiddle.format.split import SeparatorSplitter
from ..stringfiddle.term import Terminology
from .characterizer import Characterizer


class PolyonymCharacterizer(Characterizer):

    def __init__(self, characterization_context, characteristic_group_type, characteristic_groups):
        super(PolyonymCharacterizer, self).__init__(characterization_context, characteristic_group_type, characteristic_groups)
        self._terminology = Terminology(sub_sources=characteristic_groups)

    @property
    def terminology(self):
        return self._terminology

    def get_characteristic_group_by_affinity(self, input_data, input_pre_formatter=None):
        highest_affinity = 0.000001
        highest_affinity_characteristic_group = None
        for characteristic_group in self._characteristic_groups:
            affinity_evaluator = self.get_characteristic_group_affinity_evaluator(characteristic_group, self.characteristic_names_formatter)
            affinity = affinity_evaluator.get_affinity(input_data, input_pre_formatter)
            # print("Affinity: "+str(affinity))
            if affinity > highest_affinity:
                highest_affinity = affinity
                highest_affinity_characteristic_group = characteristic_group

        return highest_affinity_characteristic_group

    def get_characteristic_group_by_name(self, name, ignore_case=False):
        for characteristic_group in self._characteristic_groups:
            if characteristic_group.contains_name(name, ignore_case=ignore_case):
                return characteristic_group
        return None

    def get_characteristic_group_safe(self, name, input_pre_formatter=None):
        characteristic_group = self.get_characteristic_group_by_name(name, ignore_case=False)
        if characteristic_group is None:
            characteristic_group = self.get_characteristic_group_by_name(name, ignore_case=True)
        if characteristic_group is None:
            characteristic_group = self.get_characteristic_group_by_affinity(name, input_pre_formatter)
        return characteristic_group

    def get_characteristic_group_by_identifier(self, identifier):
        for characteristic_group in self._characteristic_groups:
            if characteristic_group.identifier == identifier:
                return characteristic_group
        return None

    def get_characteristic_group_affinity_evaluator(self, characteristic_group, pre_formatter=None):
        return CombinedAffinityEvaluator(
            characteristic_group.names,
            [MatchAffinityEvaluator, InitialismAffinityEvaluator, AcronymAffinityEvaluator],
            pre_formatter
        )

    @property
    def characteristic_names_formatter(self):
        return CombinedFormatter([
            SeparatorSplitter([" "])
        ])
