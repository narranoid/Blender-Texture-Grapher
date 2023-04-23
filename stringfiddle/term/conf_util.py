import json
from configparser import ConfigParser


def format_names(names, omit_square_brackets=True):
    stringified = json.dumps(names)
    if omit_square_brackets:
        pass
    return stringified


def parse_config_files(filenames, section_handler):
    # Gather all names
    merged_parser = merge_parsers_of_files(filenames)
    objects = []
    for section_name in merged_parser.sections():
        objects.append(section_handler(merged_parser[section_name], section_name))
    return objects


def parse_terms(names_string):
    if not names_string.startswith("["):
        names_string = "[" + names_string
    if not names_string.endswith("]"):
        names_string += "]"
    return json.loads(names_string)

# not working currently
def merge_term_keys_of_files(filenames, term_keys=["Names"]):
    # Gather all names
    name_dict = dict()
    for f in filenames:
        file_parser = ConfigParser()
        file_parser.read(f)
        for section_name in file_parser.sections():
            saved_names = name_dict.get(section_name, [])
            for name_key in term_keys:
                for n in reversed(parse_terms(file_parser[section_name][name_key])):
                    saved_names.remove(n)
                    saved_names.insert(0, n)
                name_dict[section_name] = saved_names

    merged_parser = ConfigParser()
    merged_parser.read(filenames)
    for section_name in merged_parser.sections():
        names = name_dict.get(section_name, False)
        for name_key in term_keys:
            if names:
                merged_parser[section_name][name_key] = format_names(names)

    return merged_parser


def merge_parsers_of_files(filenames, name_key="Names"):
    # Gather all names
    name_dict = dict()
    for f in filenames:
        file_parser = ConfigParser()
        file_parser.read(f)
        for section_name in file_parser.sections():
            saved_names = name_dict.get(section_name, [])
            for n in reversed(parse_terms(file_parser[section_name][name_key])):
                saved_names.remove(n)
                saved_names.insert(0, n)
            name_dict[section_name] = saved_names

    merged_parser = ConfigParser()
    merged_parser.read(filenames)
    for section_name in merged_parser.sections():
        names = name_dict.get(section_name, False)
        if names:
            merged_parser[section_name][name_key] = format_names(names)

    return merged_parser


