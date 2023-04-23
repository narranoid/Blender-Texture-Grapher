
from abc import ABC


class Characterization(ABC):

    def __init__(self, characterization_context, characteristic_group):
        self._characteristic_group = characteristic_group
        self._characterization_context = characterization_context

    @property
    def context(self):
        return self._characterization_context

    @property
    def characteristic_group(self):
        return self._characteristic_group

