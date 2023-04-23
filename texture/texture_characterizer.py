
from ..pyanoid.polyonym_characterizer import PolyonymCharacterizer
from ..stringfiddle.format import CombinedFormatter
from ..stringfiddle.format.split import SeparatorSplitter, CamelCaseSplitter, CamelCaseFilter
from ..stringfiddle.format.join import SeparatorJoiner
from ..stringfiddle.format.modify import CaseModifier, CaseOption, AcronymResolver


class TextureCharacterizer(PolyonymCharacterizer):

    def __init__(self, texture_characterization_context, texture_characteristic_group_type,
                 texture_characteristic_groups):
        super(TextureCharacterizer, self).__init__(texture_characterization_context, texture_characteristic_group_type,
                                                   texture_characteristic_groups)

    @property
    def min_match_affinity(self):
        return 0.8

    @property
    def display_name_joiner(self):
        return SeparatorJoiner(" ")

    @property
    def technical_name_joiner(self):
        return SeparatorJoiner("_")

    @property
    def file_affix_formatter(self):
        return CombinedFormatter([
            SeparatorSplitter(["_", "-", ".", " "]),
            CamelCaseSplitter(CamelCaseFilter.SINGLES),
            CaseModifier(CaseOption.UC_FIRST),
        ])

    @property
    def file_stem_formatter(self):
        return CombinedFormatter([
            SeparatorSplitter(["_", "-", ".", " "]),
            CamelCaseSplitter(CamelCaseFilter.SINGLES),
            CaseModifier(CaseOption.UC_FIRST),
        ])


