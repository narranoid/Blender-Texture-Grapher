
from .affinity_evaluator import AffinityEvaluator
from ..util import plain_join


class AcronymAffinityEvaluator(AffinityEvaluator):

    def __init__(self, evaluation_data, pre_formatter=None):
        super(AcronymAffinityEvaluator, self).__init__(evaluation_data, pre_formatter)

    def get_affinity_from_string_to_string(self, acronym, word):
        if len(word) <= 0 or len(acronym) <= 0 or word[0] != acronym[0]:
            return 0.0

        word_index = 1
        acronym_index = 1
        while acronym_index < len(acronym) and word_index < len(word):
            if word[word_index] == acronym[acronym_index]:
                acronym_index += 1
            word_index += 1

        return float(acronym_index) / float(len(acronym))

    def get_affinity_from_string_to_list(self, input_string, match_data_list):
        return self.get_affinity_from_string_to_string(input_string, plain_join(match_data_list))

    def get_affinity_from_list_to_list(self, input_list, match_data_list):
        return self.get_affinity_from_string_to_string(plain_join(input_list), plain_join(match_data_list))

    def get_affinity_from_list_to_string(self, input_list, match_data_string):
        return self.get_affinity_from_string_to_string(plain_join(input_list), match_data_string)
