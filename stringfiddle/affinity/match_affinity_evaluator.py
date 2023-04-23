
from .affinity_evaluator import AffinityEvaluator
from ..util import plain_join


class MatchAffinityEvaluator(AffinityEvaluator):

    def __init__(self, evaluation_data, pre_formatter=None):
        super(MatchAffinityEvaluator, self).__init__(evaluation_data, pre_formatter)

    def get_affinity_from_string_to_string(self, input_string, word):
        if len(word) <= 0 or len(input_string) <= 0:
            return 0.0

        index = 0
        match_count = 0.0
        while index < len(input_string) and index < len(word):
            if word[index] == input_string[index]:
                match_count += 1.0
            index += 1

        return match_count / float(len(input_string))

    def get_affinity_from_string_to_list(self, input_string, match_data_list):
        return self.get_affinity_from_string_to_string(input_string, plain_join(match_data_list))

    def get_affinity_from_list_to_list(self, input_list, match_data_list):
        match_ratio = 0.0
        index = 0

        while index < len(input_list) and index < len(match_data_list):
            match_ratio += self.get_affinity_from_string_to_string(input_list[index], match_data_list[index])

        return match_ratio / float(len(input_list))


    def get_affinity_from_list_to_string(self, input_list, match_data_string):
        return self.get_affinity_from_string_to_string(plain_join(input_list), match_data_string)
