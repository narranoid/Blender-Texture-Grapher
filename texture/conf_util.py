
from ..stringfiddle.term.conf_util import *


def read_texture_characteristic_groups(file_names, handler_func):
    # cp = merge_parsers_of_files(file_names)
    cp = ConfigParser()
    cp.read(file_names[0])

    characteristic_groups = []
    for section_name in cp.sections():
        identifier = section_name
        names = parse_terms(cp[section_name]["Names"])
        raw_characteristics = cp[section_name]
        characteristic_groups.append(handler_func(names, raw_characteristics, identifier))
    return characteristic_groups
