
from .characterization import Characterization
from ..stringfiddle.affix import AffixedGroup


class AffixCharacterization(Characterization):

    def __init__(self, characterization_context, characteristic_group, affixable):
        super(AffixCharacterization, self).__init__(characterization_context, characteristic_group)
        self._affixable = affixable

    @property
    def affixable(self):
        return self._affixable

    @property
    def affixables(self):
        if isinstance(self.affixable, AffixedGroup):
            return
