
from .format_node import FormatNodeFeature
from .format_image import FormatImageFeature


class FormatImageNodeFeature(FormatNodeFeature, FormatImageFeature):

    def format_image_nodes(self, texture_characterization, string_source, nodes=None, omit_characteristic_names=False):
        texture_characterization.format_texture_nodes(string_source,
                                                      names=self.format_node_names,
                                                      labels=self.format_node_labels,
                                                      image_names=self.format_image_names,
                                                      nodes=nodes,
                                                      short_label=self.short_labels,
                                                      omit_characteristic_names=False)

    def format_image_nodes_of_set(self, texture_set_characterization, string_source, omit_characteristic_names=False):
        for tex_char in texture_set_characterization.texture_characterizations:
            self.format_image_nodes(tex_char, string_source, omit_characteristic_names=omit_characteristic_names)
