
from abc import ABC, abstractmethod


class Affixable(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def prefix(self):
        pass

    @property
    @abstractmethod
    def postfix(self):
        pass

    @property
    @abstractmethod
    def prefix_length(self):
        pass

    @property
    @abstractmethod
    def postfix_length(self):
        pass

    @property
    @abstractmethod
    def prefix_index(self):
        pass

    @property
    @abstractmethod
    def postfix_index(self):
        pass

    @property
    @abstractmethod
    def affixes(self):
        pass
