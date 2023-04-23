
from .characteristic import CharacteristicGroup
from ..stringfiddle.format.modify import AcronymResolver
from ..stringfiddle.term import Polyonym


class PolyonymCharacteristicGroup(CharacteristicGroup, Polyonym):

    def __init__(self, names, raw_characteristics, identifier=None, sub_groups=None):
        Polyonym.__init__(self)
        CharacteristicGroup.__init__(self, raw_characteristics, identifier, sub_groups)
        self._names = list(names)

    @property
    def identifier(self):
        if self._identifier is not None:
            return self._identifier
        return self.first_name

    @property
    def first_name(self):
        if len(self._names) > 0:
            first_name = self._names[0]
            if first_name is not None:
                return first_name
        return self._identifier

    @property
    def names(self):
        return list(self._names)

    @property
    def name_formatter(self):
        return AcronymResolver(self.names)
