
from bpy.props import BoolProperty

from .. import node_util as nu


class ApplyImageSettingsFeature:
    apply_color_space: BoolProperty(
        name='Color Space',
        description='Automatically set the color space according to the texture.',
        default=True
    )

    def apply_image_settings(self, texture_characterization):
        if self.apply_color_space:
            texture_characterization.apply_image_settings()

    def apply_image_settings_to_set(self, texture_set_characterization):
        if self.apply_color_space:
            texture_set_characterization.apply_image_settings()
