
from ..pyanoid.affix_characterization import AffixCharacterization

from ..stringfiddle.affix import AffixedString
from ..stringfiddle.affix import file_util as affix_f


class TextureCharacterization(AffixCharacterization):

    def __init__(self, characterization_context, characteristic_group, affixable, file_path=None):
        super(TextureCharacterization, self).__init__(characterization_context, characteristic_group, affixable)
        self._texture_set_characterization = None
        self._file_path = file_path

    @property
    def texture_set_characterization(self):
        return self._texture_set_characterization

    @texture_set_characterization.setter
    def texture_set_characterization(self, texture_set_characterization):
        self._texture_set_characterization = texture_set_characterization

    @property
    def file_path(self):
        if self._file_path is not None:
            return self._file_path
        elif isinstance(self.affixable, AffixedString):
            if self.texture_set_characterization is not None:
                file_paths = self.texture_set_characterization.file_paths
                return affix_f.resolve_extension(self.affixable, file_paths)
            else:
                return self.affixable.full_string
        return None

