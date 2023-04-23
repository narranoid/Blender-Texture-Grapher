
from abc import ABC, abstractmethod
from ..util import is_string


class AffinityEvaluator(ABC):

    def __init__(self, evaluation_data, pre_formatter=None):
        self._evaluation_data = list(evaluation_data)
        self.pre_format(pre_formatter)

    def pre_format(self, pre_formatter):
        if pre_formatter is not None:
            for i in range(0, len(self._evaluation_data)):
                self._evaluation_data[i] = pre_formatter.format(self._evaluation_data[i])

    def get_affinity(self, input_data, pre_formatter=None):
        self.pre_format(pre_formatter)
        highest_affinity = 0.0
        for entry in self._evaluation_data:
            affinity = 0.0
            if is_string(input_data) and is_string(entry):
                affinity = self.get_affinity_from_string_to_string(input_data, entry)
            elif is_string(input_data):
                affinity = self.get_affinity_from_string_to_list(input_data, entry)
            elif is_string(entry):
                affinity = self.get_affinity_from_list_to_string(input_data, entry)
            else:
                affinity = self.get_affinity_from_list_to_list(input_data, entry)

            if affinity > highest_affinity:
                highest_affinity = affinity
                if highest_affinity >= 1.0:
                    return highest_affinity

        return highest_affinity

    @abstractmethod
    def get_affinity_from_string_to_string(self, input_string, match_data_string):
        pass

    @abstractmethod
    def get_affinity_from_string_to_list(self, input_string, match_data_list):
        pass

    @abstractmethod
    def get_affinity_from_list_to_list(self, input_list, match_data_list):
        pass

    @abstractmethod
    def get_affinity_from_list_to_string(self, input_list, match_data_string):
        pass
