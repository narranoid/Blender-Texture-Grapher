
from ..texture.texture_characteristic_group import TextureCharacteristicGroup
from ..pyanoid.characteristic import characteristic


class BlenderTextureCharacteristicGroup(TextureCharacteristicGroup):

    def __init__(self, names, raw_characteristics=None, identifier=None, sub_groups=None):
        super(BlenderTextureCharacteristicGroup, self).__init__(names, raw_characteristics, identifier, sub_groups)

    @property
    @characteristic("ColorSpace", none_safe=True, default_result="Linear")
    def color_space(self, raw_value):
        return raw_value

    @property
    @characteristic("Channels", none_safe=True, default_result=3)
    def channels(self, raw_value):
        return int(raw_value)
