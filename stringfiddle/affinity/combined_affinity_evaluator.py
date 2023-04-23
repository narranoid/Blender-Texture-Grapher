
from .affinity_evaluator import AffinityEvaluator


class CombinedAffinityEvaluator(AffinityEvaluator):

    def __init__(self, evaluation_data, matcher_types, pre_formatter=None, matcher_ratio=0.9):
        super(CombinedAffinityEvaluator, self).__init__(evaluation_data, pre_formatter)
        self._matchers = list()
        self._matcher_ratio = matcher_ratio
        for t in matcher_types:
            self._matchers.append(t(evaluation_data, pre_formatter))

    def get_affinity_from_string_to_string(self, input_string, match_data_string):
        highest_ratio = 0.0
        ratio_multiplier = 1.0
        for m in self._matchers:
            current_ratio = m.get_affinity_from_string_to_string(input_string, match_data_string) * ratio_multiplier
            if current_ratio >= 1.0:
                return current_ratio
            elif current_ratio > highest_ratio:
                highest_ratio = current_ratio
            ratio_multiplier *= self._matcher_ratio
        return highest_ratio

    def get_affinity_from_string_to_list(self, input_string, match_data_list):
        highest_ratio = 0.0
        ratio_multiplier = 1.0
        for m in self._matchers:
            current_ratio = m.get_affinity_from_string_to_list(input_string, match_data_list) * ratio_multiplier
            if current_ratio >= 1.0:
                return current_ratio
            elif current_ratio > highest_ratio:
                highest_ratio = current_ratio
            ratio_multiplier *= self._matcher_ratio
        return highest_ratio

    def get_affinity_from_list_to_list(self, input_list, match_data_list):
        highest_ratio = 0.0
        ratio_multiplier = 1.0
        for m in self._matchers:
            current_ratio = m.get_affinity_from_list_to_list(input_list, match_data_list) * ratio_multiplier
            if current_ratio >= 1.0:
                return current_ratio
            elif current_ratio > highest_ratio:
                highest_ratio = current_ratio
            ratio_multiplier *= self._matcher_ratio
        return highest_ratio

    def get_affinity_from_list_to_string(self, input_list, match_data_string):
        highest_ratio = 0.0
        ratio_multiplier = 1.0
        for m in self._matchers:
            current_ratio = m.get_affinity_from_list_to_string(input_list, match_data_string) * ratio_multiplier
            if current_ratio >= 1.0:
                return current_ratio
            elif current_ratio > highest_ratio:
                highest_ratio = current_ratio
            ratio_multiplier *= self._matcher_ratio
        return highest_ratio
