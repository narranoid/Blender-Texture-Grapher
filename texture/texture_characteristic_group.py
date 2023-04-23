
from ..pyanoid.polyonym_characteristic_group import PolyonymCharacteristicGroup
from ..pyanoid.characteristic import characteristic


class TextureCharacteristicGroup(PolyonymCharacteristicGroup):

    def __init__(self, names, raw_characteristics, identifier=None, sub_groups=None):
        super(TextureCharacteristicGroup, self).__init__(names, raw_characteristics, identifier, sub_groups)

    @property
    @characteristic("Order", none_safe=True, default_result=9999999999)
    def order(self, raw_value):
        return int(raw_value)
