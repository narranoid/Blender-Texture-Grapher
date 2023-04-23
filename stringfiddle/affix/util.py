
from . import AffixedString
from .. import util as str_util


def remove_matching_stems_from(group, affix_matchers):
    full_string_dict = dict()

    for fs in group.full_strings:
        full_string_dict[fs] = fs

    for matcher in affix_matchers:
        matches = matcher.get_matches(group)
        for match_group in matches:
            for key, val in full_string_dict:
                for match_str in match_group:
                    if match_str.full_string == val:
                        full_string_dict[key] = str_util.plain_join(match_str.affixes)
    return full_string_dict


def contains(contained_object, container):
    str_object = get_string_checked(contained_object)
    for item in container:
        if isinstance(item, AffixedString) and item.full_string == str_object:
            return True
        elif str_util.is_string(item) and item == contained_object:
            return True
        elif contains(contained_object, item):
            return True

    return False


def iter_affixed_strings(container):
    for item in container:
        if isinstance(item, AffixedString):
            yield item
        else:
            for sub_item in iter_affixed_strings(item):
                yield sub_item

    return False


def get_string_checked(string_or_name_identity):
    if isinstance(string_or_name_identity, AffixedString):
        return string_or_name_identity.full_string
    elif isinstance(string_or_name_identity, str):
        return string_or_name_identity
    return str(string_or_name_identity)


def get_string_iterator(name_string_container):
    from . import AffixedGroup
    if isinstance(name_string_container, AffixedGroup):
        return name_string_container.iter_strings()
    return iter(name_string_container)


def find_affixed_groups(strings):
    from . import AffixedGroup
    identity_groups = set()
    index_outer = 0
    if len(strings) == 1:
        identity_groups.add(AffixedGroup(strings, -1, 0))
    elif len(strings) > 1:
        while index_outer < len(strings)-1:
            index_inner = 1
            while index_inner < len(strings):
                pre_id_helper = get_prefix_index(strings[index_outer], strings[index_inner])
                post_id_helper = get_postfix_index(strings[index_outer], strings[index_inner])
                if pre_id_helper >= 0 or post_id_helper <= -1:
                    add_to_group(strings[index_outer], strings[index_inner], pre_id_helper, post_id_helper, identity_groups)
                index_inner += 1
            index_outer += 1
    return identity_groups


def find_affixed_group(strings, affix_matcher):
    pass


def add_to_group(string1, string2, prefix_index, postfix_index, groups):
    from . import AffixedGroup
    for group in groups:
        if group.prefix_index == prefix_index and group.postfix_index == postfix_index:
            group.add(string1)
            group.add(string2)
            return
    groups.add(AffixedGroup([string1, string2], prefix_index, postfix_index))


def get_identity_index(name1, name2, incrementor, start_index, default_index):
    index = start_index
    while index < len(name1) and index < len(name2):
        if name1[index] is not name2[index]:
            return index
        index += incrementor
    return default_index


def get_prefix_index(string1, string2):
    index = 0
    while index < len(string1) and index < len(string2):
        if string1[index] is not string2[index]:
            return index
        index += 1
    return -1


def get_postfix_index(string1, string2):
    reverse_index = -1
    index = 0
    reversed_name1 = string1[::-1]
    reversed_name2 = string2[::-1]

    while index < len(string1) and index < len(string2):
        if reversed_name1[index] is not reversed_name2[index]:
            return reverse_index+1
        reverse_index -= 1
        index += 1
    return 0
