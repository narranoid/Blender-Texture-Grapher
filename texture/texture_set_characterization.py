
from ..pyanoid.characterization import Characterization
from ..stringfiddle.affix import AffixedGroup


class TextureSetCharacterization(Characterization):

    def __init__(self, characterization_context, characteristic_group, texture_characterizations, file_path=None):
        def get_order(x):
            if x.characteristic_group is None:
                return 1000000000

            return x.characteristic_group.order

        texture_characterizations.sort(key=lambda x: get_order(x), reverse=False)
        super(TextureSetCharacterization, self).__init__(characterization_context, characteristic_group)
        self._texture_characterizations = list(texture_characterizations)
        self._file_path = file_path
        for tc in self._texture_characterizations:
            tc.texture_set_characterization = self

    @property
    def texture_characterizations(self):
        return list(self._texture_characterizations)

    # filepath only exists eg for EXR where everything is packed in one file
    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path

    @property
    def affixed_group(self):
        string_set = set()
        prefix_index = -1
        postfix_index = 0

        for tex_char in self._texture_characterizations:
            affixed_string = tex_char.affixable
            prefix_index = affixed_string.prefix_index
            postfix_index = affixed_string.postfix_index
            string_set.add(affixed_string.full_string)

        return AffixedGroup(string_set, prefix_index, postfix_index)



