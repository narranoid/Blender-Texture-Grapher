import bpy
from bpy.props import StringProperty

from ..texture.texture_characterizer import TextureCharacterizer
from ..stringfiddle.affix import file_util as affix_f
from ..stringfiddle.affix import util as affix_u
from ..stringfiddle.affix import AffixAspect
from ..stringfiddle.affix.match import ArithmeticScoreAffixMatcher, BitdepthAffixMatcher, VarianceAffixMatcher
from ..texture.conf_util import read_texture_characteristic_groups

from ..textureblender.blender_texture_characteristic_group import BlenderTextureCharacteristicGroup
from .blender_texture_characterization import BlenderTextureCharacterization
from .blender_texture_set_characterization import BlenderTextureSetCharacterization

from ..stringfiddle.format.join import SeparatorJoiner
from ..stringfiddle.format import CombinedFormatter, NoneFormatter
from ..stringfiddle.format.split import SeparatorSplitter, CamelCaseSplitter, CamelCaseFilter, PathSplitter, PathFormat, SplitOption
from ..stringfiddle.format.filter import EmptyFilter, IndexFilter
from ..stringfiddle.format.modify import CaseModifier, CaseOption, AcronymResolver
from .util import get_strings, get_by_string, is_external, get_filepath
from .string_source import StringSource
from . import node_util as nu
from ..texture.texture_characterization_context import TextureCharacterizationContext


class BlenderTextureCharacterizationContext(TextureCharacterizationContext):

    def __init__(self):
        super(BlenderTextureCharacterizationContext, self).__init__()

    def format_string(self, string, string_source, formatter_dict):
        result_string = string
        formatter = formatter_dict.get(string_source, None)
        if formatter is not None:
            result_string = formatter.format_to_string(string)
        return result_string


    # region Base Source Formatters

    @property
    def base_name_source_formatter(self):
        return CombinedFormatter([
            SeparatorSplitter(["/", "_", "-", ".", " ", "|", ";", "\"", "\\", "'"]),
            CamelCaseSplitter(CamelCaseFilter.SINGLES)
        ])

    @property
    def base_label_source_formatter(self):
        return CombinedFormatter([
            SeparatorSplitter(["/", "_", "-", ".", " ", "|", ";", "\"", "\\", "'"]),
            CamelCaseSplitter(CamelCaseFilter.SINGLES)
        ])

    # endregion

    # region Base Destination Formatters

    @property
    def base_name_destination_formatter(self):
        return CombinedFormatter([
            CaseModifier(CaseOption.UC_FIRST),
            SeparatorJoiner(".")
        ])

    @property
    def base_label_destination_formatter(self):
        return CombinedFormatter([
            CaseModifier(CaseOption.UC_FIRST),
            SeparatorJoiner(" ")
        ])

    # endregion



    # region Texture Node

    # region Texture Node Name

    @property
    def texture_node_name_format_string(self):
        return "{texture_set}.{texture}"

    def get_texture_node_name(self, texture, texture_source, texture_set=None, texture_set_source=None):
        texture_name = self.format_string(texture, texture_source, {
            StringSource.FILEPATH: self.texture_node_name_from_filepath_formatter,
            StringSource.NAME: self.texture_node_name_from_name_formatter,
            StringSource.LABEL: self.texture_node_name_from_label_formatter
        })

        if texture_set is not None and texture_set_source is not None:
            texture_set_name = self.format_string(texture_set, texture_set_source, {
                StringSource.FILEPATH: self.texture_node_set_name_from_filepath_formatter,
                StringSource.NAME: self.texture_node_set_name_from_name_formatter,
                StringSource.LABEL: self.texture_node_set_name_from_label_formatter
            })
            return self.texture_node_name_format_string.format(texture_set=texture_set_name, texture=texture_name)
        return texture_name

    @property
    def texture_node_name_from_filepath_formatter(self):
        #return self.base_name_destination_formatter
        return CombinedFormatter([
            self.base_filepath_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_node_set_name_from_filepath_formatter(self):
        return self.texture_node_name_from_filepath_formatter

    @property
    def texture_node_name_from_name_formatter(self):
        return CombinedFormatter([
            self.base_name_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_node_set_name_from_name_formatter(self):
        return self.texture_node_name_from_name_formatter

    @property
    def texture_node_name_from_label_formatter(self):
        return CombinedFormatter([
            self.base_label_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_node_set_name_from_label_formatter(self):
        return self.texture_node_name_from_label_formatter

    # endregion

    # region Texture Node Label

    @property
    def texture_node_label_format_string(self):
        return "{texture_set} {texture}"

    def get_texture_node_label(self, texture, texture_source, texture_set=None, texture_set_source=None):
        texture_label = self.format_string(texture, texture_source, {
            StringSource.FILEPATH: self.texture_node_label_from_filepath_formatter,
            StringSource.NAME: self.texture_node_label_from_name_formatter,
            StringSource.LABEL: self.texture_node_label_from_label_formatter
        })

        if texture_set is not None and texture_set_source is not None:
            texture_set_label = self.format_string(texture_set, texture_set_source, {
                StringSource.FILEPATH: self.texture_node_set_label_from_filepath_formatter,
                StringSource.NAME: self.texture_node_set_label_from_name_formatter,
                StringSource.LABEL: self.texture_node_set_label_from_label_formatter
            })
            return self.texture_node_label_format_string.format(texture_set=texture_set_label, texture=texture_label)
        return texture_label

    @property
    def texture_node_label_from_filepath_formatter(self):
        return CombinedFormatter([
            self.base_filepath_source_formatter,
            self.base_label_destination_formatter
        ])

    @property
    def texture_node_set_label_from_filepath_formatter(self):
        return self.texture_node_label_from_filepath_formatter

    @property
    def texture_node_label_from_name_formatter(self):
        return CombinedFormatter([
            self.base_name_source_formatter,
            self.base_label_destination_formatter
        ])

    @property
    def texture_node_set_label_from_name_formatter(self):
        return self.texture_node_label_from_name_formatter

    @property
    def texture_node_label_from_label_formatter(self):
        return CombinedFormatter([
            self.base_label_source_formatter,
            self.base_label_destination_formatter
        ])

    @property
    def texture_node_set_label_from_label_formatter(self):
        return self.texture_node_label_from_label_formatter

    # endregion

    # endregion


    # region Texture Set Node

    # region Texture Set Node Name

    @property
    def texture_set_node_name_format_string(self):
        return "{texture_set}"

    def get_texture_set_node_name(self, texture_set, texture_set_source):
        texture_set_name = self.format_string(texture_set, texture_set_source, {
            StringSource.FILEPATH: self.texture_set_node_name_from_filepath_formatter,
            StringSource.NAME: self.texture_set_node_name_from_name_formatter,
            StringSource.LABEL: self.texture_set_node_name_from_label_formatter
        })

        return self.texture_set_node_name_format_string.format(texture_set=texture_set_name)

    @property
    def texture_set_node_name_from_filepath_formatter(self):
        return CombinedFormatter([
            self.base_filepath_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_set_node_name_from_name_formatter(self):
        return CombinedFormatter([
            self.base_name_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_set_node_name_from_label_formatter(self):
        return CombinedFormatter([
            self.base_label_source_formatter,
            self.base_name_destination_formatter
        ])

    # endregion

    # region Texture Node Label

    @property
    def texture_set_node_label_format_string(self):
        return "{texture_set}"

    def get_texture_set_node_label(self, texture_set, texture_set_source):
        texture_set_label = self.format_string(texture_set, texture_set_source, {
            StringSource.FILEPATH: self.texture_set_node_label_from_filepath_formatter,
            StringSource.NAME: self.texture_set_node_label_from_name_formatter,
            StringSource.LABEL: self.texture_set_node_label_from_label_formatter
        })

        return self.texture_set_node_name_format_string.format(texture_set=texture_set_label)

    @property
    def texture_set_node_label_from_filepath_formatter(self):
        return CombinedFormatter([
            self.base_filepath_source_formatter,
            self.base_label_destination_formatter
        ])

    @property
    def texture_set_node_label_from_name_formatter(self):
        return CombinedFormatter([
            self.base_name_source_formatter,
            self.base_label_destination_formatter
        ])

    @property
    def texture_set_node_label_from_label_formatter(self):
        return CombinedFormatter([
            self.base_label_source_formatter,
            self.base_label_destination_formatter
        ])

    # endregion

    # endregion



    # region Texture Set Node Group Name

    @property
    def texture_set_node_group_name_format_string(self):
        return "{texture_set}"

    def get_texture_set_node_group_name(self, texture_set, texture_set_source):
        texture_set_name = self.format_string(texture_set, texture_set_source, {
            StringSource.FILEPATH: self.texture_set_node_group_name_from_filepath_formatter,
            StringSource.NAME: self.texture_set_node_group_name_from_name_formatter,
            StringSource.LABEL: self.texture_set_node_group_name_from_label_formatter
        })

        return self.texture_set_node_group_name_format_string.format(texture_set=texture_set_name)

    @property
    def texture_set_node_group_name_from_filepath_formatter(self):
        return CombinedFormatter([
            self.base_filepath_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_set_node_group_name_from_name_formatter(self):
        return CombinedFormatter([
            self.base_name_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_set_node_group_name_from_label_formatter(self):
        return CombinedFormatter([
            self.base_label_source_formatter,
            self.base_name_destination_formatter
        ])

    # endregion


    # region Texture Image Name

    @property
    def texture_image_name_format_string(self):
        return "{texture_set}.{texture}"

    def get_texture_image_name(self, texture, texture_source, texture_set=None, texture_set_source=None):
        texture_name = self.format_string(texture, texture_source, {
            StringSource.FILEPATH: self.texture_image_name_from_filepath_formatter,
            StringSource.NAME: self.texture_image_name_from_name_formatter,
            StringSource.LABEL: self.texture_image_name_from_label_formatter
        })

        if texture_set is not None and texture_set_source is not None:
            texture_set_name = self.format_string(texture_set, texture_set_source, {
                StringSource.FILEPATH: self.texture_image_set_name_from_filepath_formatter,
                StringSource.NAME: self.texture_image_set_name_from_name_formatter,
                StringSource.LABEL: self.texture_image_set_name_from_label_formatter
            })
            return self.texture_image_name_format_string.format(texture_set=texture_set_name, texture=texture_name)
        return texture_name

    @property
    def texture_image_name_from_filepath_formatter(self):
        return CombinedFormatter([
            self.base_filepath_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_image_set_name_from_filepath_formatter(self):
        return self.texture_image_name_from_filepath_formatter

    @property
    def texture_image_name_from_name_formatter(self):
        return CombinedFormatter([
            self.base_name_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_image_set_name_from_name_formatter(self):
        return self.texture_image_name_from_name_formatter

    @property
    def texture_image_name_from_label_formatter(self):
        return CombinedFormatter([
            self.base_label_source_formatter,
            self.base_name_destination_formatter
        ])

    @property
    def texture_image_set_name_from_label_formatter(self):
        return self.texture_image_name_from_label_formatter

    # endregion




    # region Texture Set Image Name (EXR/Layered)

    # endregion

    # UDIM = Texture Sub Set ?


    @property
    def node_label_formatter(self):
        return self.file_stem_formatter

    @property
    def node_name_formatter(self):
        return NoneFormatter()

    @property
    def node_group_name_formatter(self):
        return self.image_name_formatter

    @property
    def image_name_formatter(self):
        return CombinedFormatter([
            PathSplitter(path_format=PathFormat.RUNNING_SYSTEM,
                         split_options=SplitOption.DRIVE | SplitOption.ALT_SEP | SplitOption.SEP),
            EmptyFilter(),
            IndexFilter([-1], whitelist=True),
            SeparatorSplitter(["_", "-", ".", " "]),
            CamelCaseSplitter(CamelCaseFilter.SINGLES),
            CaseModifier(CaseOption.UC_FIRST),
        ])

    @property
    def image_texture_set_name_formatter(self):
        pass

    @property
    def image_texture_name_formater(self):
        pass

    @property
    def image_texture_set_to_texture_name_separator(self):
        return "_"


    @property
    def image_node_texture_set_name_formatter(self):
        pass

    @property
    def image_node_texture_name_formatter(self):
        pass

    @property
    def image_node_texture_set_to_texture_name_separator(self):
        return "."

    @property
    def image_node_texture_set_label_formatter(self):
        pass

    @property
    def image_node_texture_label_formatter(self):
        pass

    @property
    def image_node_texture_set_to_texture_label_separator(self):
        return " "


    @property
    def affinity_evaluator(self):
        return None

    @property
    def node_group_socket_input_name_formatter(self):
        return self.file_stem_formatter

    @property
    def node_group_socket_output_name_formatter(self):
        return self.file_stem_formatter

    @property
    def texture_node_frame_name_formatter(self):
        return self.file_stem_formatter

    @property
    def texture_node_frame_label_formatter(self):
        return self.file_stem_formatter

    @property
    def socket_link_detection_formatter(self):
        return self.file_stem_formatter

    # region Image Extensions

    @property
    def image_extensions(self):
        return ["png", "jpg", "jpeg", "tif", "tiff", "bmp", "exr"]

    @property
    def image_extension_filter_pattern(self):
        ext_patterns = []
        for ext in self.image_extensions:
            ext_patterns.append("*." + ext)
        return ";".join(ext_patterns)

    @property
    def image_extension_filter(self):
        return StringProperty(
            default=self.image_extension_filter_pattern,
            options={'HIDDEN'}
        )

    # endregion
