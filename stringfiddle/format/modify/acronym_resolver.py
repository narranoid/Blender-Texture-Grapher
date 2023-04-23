
from . import StringModifier
from ...util import is_abbreviation_of


class AcronymResolver(StringModifier):

    def __init__(self, glossary):
        super(AcronymResolver, self).__init__()
        self.__glossary = glossary

    def modify(self, acronym):
        for word in self.__glossary:
            if is_abbreviation_of(acronym, word):
                return word
        return acronym
