from . import TermSource


class Terminology(TermSource):

    def __init__(self, terms=None, sub_sources=None):
        super(Terminology, self).__init__()
        self._terms = terms if terms is not None else []
        self._sub_sources = sub_sources if sub_sources is not None else []

    @property
    def sub_sources(self):
        return self._sub_sources

    def get_sub_sources_of_type(self, sub_source_type):
        result = []
        for sub_source in self._sub_sources:
            if isinstance(sub_source, sub_source_type):
                result.append(sub_source)
        return result

    @property
    def terms(self):
        all_terms = []
        for t in self._terms:
            all_terms.append(t)
        for sub_termin in self._sub_sources:
            for t in sub_termin.terms:
                all_terms.append(t)
        return all_terms
