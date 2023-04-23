
from abc import ABC
import functools


def characteristic(characteristic_key, none_safe=True, default_raw_value=None, default_result=None):
    def decorator_characteristic(characteristic_func):
        @functools.wraps(characteristic_func)
        def wrapper_characteristic(data_container):
            prop = data_container.get_raw_characteristic(characteristic_key, default_raw_value)
            if not none_safe or prop is not None:
                return characteristic_func(data_container, prop)
            return default_result

        return wrapper_characteristic

    return decorator_characteristic


class CharacteristicGroup(ABC):

    def __init__(self, raw_characteristics, identifier=None, sub_groups=None):
        self._identifier = identifier
        self._raw_characteristics = None

        if raw_characteristics is None:
            self._raw_characteristics = dict()
        else:
            # Consider making a copy here as this is the raw section proxy of config file.
            # There is no copy made yet, because SectionProxy is case insensitive while dict copy is not
            # Fix ideas?
            self._raw_characteristics = raw_characteristics
            #self._raw_characteristics = dict(raw_characteristics)

        if sub_groups is None:
            self._sub_groups = list()
        else:
            self._sub_groups = list(sub_groups)

    def get_raw_characteristic(self, characteristics_key, default_value=None):
        return self._raw_characteristics.get(characteristics_key, default_value)

    @property
    def raw_characteristics(self):
        return dict(self._raw_characteristics)

    @property
    def identifier(self):
        return self._identifier

    @property
    def has_identifier(self):
        return self._identifier is not None

    @property
    def sub_groups(self):
        return list(self._sub_groups)

    @property
    def sub_group_len(self):
        return len(self._sub_groups)
