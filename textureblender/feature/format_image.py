
from bpy.props import BoolProperty


class FormatImageFeature:
    format_image_names: BoolProperty(
        name='Format Image Name',
        description='Automatically set image names.',
        default=True
    )

    def format_images(self, texture_characterization, string_source, images=None):
        texture_characterization.format_images(self, string_source, names=self.format_image_names,
                                               images=images)

    def format_image_names_to_set(self, texture_set_characterization, string_source):
        for tex_char in texture_set_characterization.texture_characterizations:
            self.format_images(tex_char, string_source)
