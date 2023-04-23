
from . import StringModifier


class SynonymResolver(StringModifier):

    @classmethod
    def from_config_file(cls, file_path, preference, glossary="Global"):
        pass

    @classmethod
    def from_config_content(cls, content, preference, glossary="Global"):
        pass

    def __init__(self, glossary, preferences=None):
        super(SynonymResolver, self).__init__()
        self.__glossary = glossary.copy()
        for glossary_key, glossary_value in glossary:
            for pref_key, pref_value in preferences:
                for pref in reversed(pref_value):
                    if pref in glossary_value:
                        glossary_value.remove(pref)
                        glossary_value.prepend(pref)

    def modify(self, n):
        for key, val in self.__glossary:
            if n in val:
                return val[0]
        return n
