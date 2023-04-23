
from .affinity_evaluator import AffinityEvaluator
from ..util import plain_join


class InitialismAffinityEvaluator(AffinityEvaluator):

    def __init__(self, evaluation_data, pre_formatter=None):
        super(InitialismAffinityEvaluator, self).__init__(evaluation_data, pre_formatter)

    def get_affinity_from_string_to_string(self, input_string, match_data_string):
        return self.get_affinity_from_string_to_list(input_string, [match_data_string])

    def get_affinity_from_string_to_list(self, input_string, match_data_list):
        if len(input_string) == 0 or len(match_data_list) == 0:
            return 0.0

        input_len = float(len(input_string))
        data_len = float(len(match_data_list))
        match_count = 0.0

        index = 0
        if data_len < input_len:
            for entry in match_data_list:
                if input_string[index] == entry[0]:
                    match_count += 1.0
                index += 1
            return match_count / data_len * (data_len / input_len)

        for initialism_char in input_string:
            if initialism_char == match_data_list[index][0]:
                match_count += 1.0
            index += 1
        return match_count / input_len * (input_len / data_len)

    def get_affinity_from_list_to_list(self, input_list, match_data_list):
        return self.get_affinity_from_string_to_list(plain_join(input_list), match_data_list)

    def get_affinity_from_list_to_string(self, input_list, match_data_string):
        return self.get_affinity_from_string_to_list(plain_join(input_list), [match_data_string])

