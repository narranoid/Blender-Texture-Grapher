from abc import ABC, abstractmethod


class TermSource(ABC):

    def __init__(self):
        pass

    @property
    @abstractmethod
    def terms(self):
        pass

    @property
    def first_term(self):
        return self.terms[0]

    def contains_term(self, term):
        return term in self.terms

