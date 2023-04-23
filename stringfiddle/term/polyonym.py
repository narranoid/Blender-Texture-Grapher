from . import TermSource
from abc import ABC, abstractmethod


class Polyonym(TermSource):

    def __init__(self):
        super(Polyonym, self).__init__()

    # Term functions

    @property
    def terms(self):
        return self.names

    @property
    def first_term(self):
        return self.first_name

    def contains_term(self, term):
        return self.contains_name(term)

    # Name functions

    @property
    @abstractmethod
    def names(self):
        pass

    @property
    def first_name(self):
        return self.names[0]

    def contains_name(self, name, ignore_case=False):
        if not ignore_case:
            return name in self.names

        for self_name in self.names:
            if self_name.lower() == name.lower():
                return True
        return False
