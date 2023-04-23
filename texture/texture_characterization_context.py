
from ..texture.texture_characterizer import TextureCharacterizer
from ..stringfiddle.affix import file_util as affix_f
from ..stringfiddle.affix import util as affix_u
from ..stringfiddle.affix import AffixAspect
from ..stringfiddle.affix.match import ArithmeticScoreAffixMatcher, BitdepthAffixMatcher, VarianceAffixMatcher
from ..texture.conf_util import read_texture_characteristic_groups

from ..textureblender.blender_texture_characteristic_group import BlenderTextureCharacteristicGroup

from ..stringfiddle.format.join import SeparatorJoiner
from ..stringfiddle.format import CombinedFormatter, NoneFormatter
from ..stringfiddle.format.split import SeparatorSplitter, CamelCaseSplitter, CamelCaseFilter, PathSplitter, PathFormat, SplitOption
from ..stringfiddle.format.filter import EmptyFilter, IndexFilter
from ..stringfiddle.format.modify import CaseModifier, CaseOption, AcronymResolver


class TextureCharacterizationContext:

    def __init__(self):
        pass

    def format_default(self, input_string):
        pass

    def format_characterizable_texture_string(self, texture_string):
        return self.characterizable_texture_string_formatter.format_to_string(texture_string)

    @property
    def base_filepath_source_formatter(self):
        return CombinedFormatter([
            PathSplitter(path_format=PathFormat.RUNNING_SYSTEM,
                         split_options=SplitOption.DRIVE | SplitOption.ALT_SEP | SplitOption.SEP),
            EmptyFilter(),
            IndexFilter([-1], whitelist=True),
            SeparatorSplitter(["/", "_", "-", ".", " "]),
            CamelCaseSplitter(CamelCaseFilter.SINGLES)
        ])

    @property
    def base_destination_formatter(self):
        return CombinedFormatter([
            CaseModifier(CaseOption.UC_FIRST),
            SeparatorJoiner("")
        ])

    @property
    def characterizable_texture_string_formatter(self):
        return CombinedFormatter([
            self.base_filepath_source_formatter,
            self.base_destination_formatter
        ])
