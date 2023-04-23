import bpy
import os
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

from .util import get_strings, get_by_string, is_external, get_filepath
from .string_source import StringSource
from . import node_util as nu
from .blender_texture_characterization_context import BlenderTextureCharacterizationContext

def init_characterizer():

    characterizer_ini_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "global.ini")
    # print(characterizer_ini_path)
    file_names = [
        characterizer_ini_path
    ]

    characteristic_groups = read_texture_characteristic_groups(file_names, BlenderTextureCharacteristicGroup)
    return BlenderTextureCharacterizer(BlenderTextureCharacterizationContext(), characteristic_groups)


class BlenderTextureCharacterizer(TextureCharacterizer):

    def __init__(self, texture_characterization_context, texture_characteristic_groups):
        super(BlenderTextureCharacterizer, self).__init__(texture_characterization_context, BlenderTextureCharacteristicGroup, texture_characteristic_groups)

    def select_by_number(self, select_mode, check_group, all_groups, affix_matcher=None, custom_number=0):
        if affix_matcher is None:
            affix_matcher = VarianceAffixMatcher()

        number_matches = affix_matcher.get_matches(all_groups)

        for number_group in number_matches:
            for affixed_string in number_group:
                if check_group.contains_string(affixed_string):
                    current_num = int(affixed_string.stem)
                    if select_mode == 2 and current_num == custom_number:
                        pass



    def select_by_bitdepth(self, select_mode, check_group, all_groups, affix_matcher=None, custom_depth=0):
        if affix_matcher is None:
            affix_matcher = BitdepthAffixMatcher()

        bitdepth_matches = affix_matcher.get_matches(all_groups)
        match_length = len(bitdepth_matches)

        if match_length <= 0:
            return None

        bitdepth_selection = set()

        for bitdepth_group in bitdepth_matches:
            bitdepth_selection_entry = None
            highest_depth_select = None
            highest_depth = affix_matcher.start_depth
            lowest_depth_select = None
            lowest_depth = affix_matcher.end_depth

            for affixed_string in bitdepth_group:
                if check_group.contains_string(affixed_string):
                    current_depth = int(affixed_string.stem)
                    if current_depth >= highest_depth:
                        highest_depth = current_depth
                        highest_depth_select = affixed_string
                    if current_depth <= lowest_depth:
                        lowest_depth = current_depth
                        lowest_depth_select = affixed_string
                    if select_mode == 4 and 0 < custom_depth == current_depth:
                        bitdepth_selection_entry = affixed_string
                        break

            if bitdepth_selection_entry is None:
                if select_mode == 2:
                    bitdepth_selection_entry = highest_depth_select
                else:
                    bitdepth_selection_entry = lowest_depth_select

            if bitdepth_selection_entry is not None:
                bitdepth_selection.add(bitdepth_selection_entry)

        for bitdepth_entry in bitdepth_selection:
            check_group.remove(bitdepth_entry)

        return bitdepth_selection

    def create_texture_images_from_files(self, nodes_context, file_paths, hide=False, preffered_bitdpeth=0):
        characterizations = list()
        affix_matcher = ArithmeticScoreAffixMatcher(AffixAspect.GROUP_LENGTH)
        #bitdepth_evaluator = BitdepthAffixMatcher()
        #variance_evaluator = VarianceAffixMatcher()

        affixed_groups = affix_f.find_affixed_files(file_paths, trim_extensions=self.supported_extensions)
        best_match = affix_matcher.get_best_match(affixed_groups)

        tex_nodes = []
        #formattables = affix_u.remove_evaluated_stems_from(best_match, [bitdepth_evaluator, variance_evaluator])

        for affixed_string in best_match:

            stem = affixed_string.stem
            file_path = affix_f.resolve_extension(affixed_string, file_paths)
            name_str = self.node_name_formatter.format_to_string(stem)

            tex_node = nodes_context.new(type='ShaderNodeTexImage')
            #tex_node.label = self.node_label_formatter.format_to_string(stem)
            #tex_node.name = self.node_name_formatter.format_to_string(stem)
            tex_node.image = bpy.data.images.load(file_path)

            characteristic_group = self.get_characteristic_group_safe(name_str)
            if characteristic_group:
                tex_node.label = characteristic_group.first_name
                tex_node.image.colorspace_settings.name = characteristic_group.color_space
                tex_node.image.name = characteristic_group.first_name
            else:
                pass
                #tex_node.label = self.node_label_formatter.format_to_string(stem)
                #tex_node.image.name = self.image_name_formatter.format_to_string(stem)

            characterization = BlenderTextureCharacterization(self, [characteristic_group], affixed_string)
            characterization.add_shader_texture_node(tex_node, add_image=True)
            characterizations.append(characterization)

            tex_node.hide = hide
            tex_nodes.append(tex_node)
        return characterizations

    def load_image_from_file(self, file_path, custom_name=None):
        img = bpy.data.images.load(file_path)
        if custom_name is None:
            img.name = self.image_name_formatter.format_to_string(file_path)
        else:
            img.name = custom_name
        return img

    def characterize(self, file_paths, affix_matcher=None):
        characterizations = list()
        if affix_matcher is None:
            affix_matcher = ArithmeticScoreAffixMatcher(AffixAspect.GROUP_LENGTH)

        affixed_groups = affix_f.find_affixed_files(file_paths, trim_extensions=self.context.image_extensions)
        best_match = affix_matcher.get_best_match(affixed_groups)

        for affixed_string in best_match:
            stem = affixed_string.stem
            file_path = affix_f.resolve_extension(affixed_string, file_paths)
            name_str = self.context.format_characterizable_texture_string(stem)

            characteristic_group = self.get_characteristic_group_safe(name_str)

            characterization = BlenderTextureCharacterization(self.context, characteristic_group, affixed_string, file_path)
            characterizations.append(characterization)

        set_characterization = BlenderTextureSetCharacterization(self.context, None, characterizations)
        return set_characterization

    def characterize_image_nodes(self, nodes, string_source, affix_matcher=None):
        characterizations = list()
        if affix_matcher is None:
            affix_matcher = ArithmeticScoreAffixMatcher(AffixAspect.GROUP_LENGTH)

        search_for_images = (string_source == StringSource.IMAGE_NAME or string_source == StringSource.FILEPATH
                             or string_source == StringSource.RAW_FILEPATH)
        strings = get_strings(nodes, string_source)

        affixed_groups = affix_u.find_affixed_groups(strings)
        best_match = affix_matcher.get_best_match(affixed_groups)

        for affixed_string in best_match:
            stem = affixed_string.stem
            img = None
            image_nodes = None
            file_path = ""

            if search_for_images:
                img = get_by_string(bpy.data.images, affixed_string.full_string, string_source)
                if img:
                    image_nodes = nu.get_nodes_with_image(nodes, img)
            else:
                found_node = get_by_string(nodes, affixed_string.full_string, string_source)
                img = found_node.image
                image_nodes = [found_node]

            if img:
                file_path = get_filepath(img, string_source == StringSource.RAW_FILEPATH)
            name_str = self.context.format_characterizable_texture_string(stem)

            characteristic_group = self.get_characteristic_group_safe(name_str)
            characterization = BlenderTextureCharacterization(self.context, characteristic_group, affixed_string, file_path)

            if img:
                # print(name_str)
                characterization.add_image(img)
            if image_nodes:
                # print("Node Found " + name_str)
                for n in image_nodes:
                    characterization.add_shader_texture_node(n, add_image=False)

            characterizations.append(characterization)

        set_characterization = BlenderTextureSetCharacterization(self.context, None, characterizations)
        return set_characterization

    def characterize_images(self, images, affix_matcher=None, prefer_raw_filepath=False):
        characterizations = list()
        if affix_matcher is None:
            affix_matcher = ArithmeticScoreAffixMatcher(AffixAspect.GROUP_LENGTH)

        image_names = list()
        for img in images:
            image_names.append(img.name)

        affixed_groups = affix_u.find_affixed_groups(image_names)
        best_match = affix_matcher.get_best_match(affixed_groups)

        for affixed_string in best_match:
            stem = affixed_string.stem
            img = bpy.data.images[affixed_string.full_string]
            file_path = get_filepath(img, prefer_raw_filepath)
            name_str = self.context.format_characterizable_texture_string(stem)

            characteristic_group = self.get_characteristic_group_safe(name_str)
            characterization = BlenderTextureCharacterization(self.context, characteristic_group, affixed_string, file_path)
            characterizations.append(characterization)

        set_characterization = BlenderTextureSetCharacterization(self.context, None, characterizations)
        return set_characterization
