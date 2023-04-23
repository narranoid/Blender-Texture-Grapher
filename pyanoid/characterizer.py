
from abc import ABC


class Characterizer(ABC):

    def __init__(self, characterization_context, characteristic_group_type, characteristic_groups):
        self._characterization_context = characterization_context
        self._characteristic_groups = list(characteristic_groups)
        self._characteristic_group_type = characteristic_group_type

    @property
    def context(self):
        return self._characterization_context

    @property
    def characteristic_groups(self):
        return list(self._characteristic_groups)

    @property
    def identifiers(self):
        identifier_list = list()
        for characteristic_group in self._characteristic_groups:
            identifier_list.append(characteristic_group)
        return identifier_list

