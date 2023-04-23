
import re
from enum import Flag

from .import StringSplitter


class CamelCaseFilter(Flag):
    NONE = 0

    ONE_LETTER_WORDS = 1 #DONE
    UPPER_CASE_WORDS = 2  # DONE
    LOWER_CASE_LEADING = 4  # DONE

    NUMBERS = 24 #DONE
    NUMBERS_LEADING = 8 #DONE

    SINGLES = 96
    SINGLE_WORDS = 32 #DONE
    SINGLE_NUMBERS = 64 #DONE


class CamelCaseSplitter(StringSplitter):

    def __init__(self, filter=CamelCaseFilter.NONE):
        super(CamelCaseSplitter, self).__init__()
        self.__filter = filter

    def split(self, formattable):
        return camel_case_search_split(formattable, self.__filter)


def camel_case_search_split(word, filter=CamelCaseFilter.NONE):
    split_indices = []
    start_indices = get_potential_camel_case_indices(word, 0, filter)
    split_indices += start_indices
    for index in start_indices:
        next_index_check = index
        next_index = next_camel_case_index(word, index, filter)
        if next_index is next_index_check \
                and (word[next_index].isnumeric() and bool(filter & CamelCaseFilter.SINGLE_NUMBERS)
                or (word[next_index].islower() or word[next_index].isupper()) and bool(filter & CamelCaseFilter.SINGLE_WORDS)):
            continue

        while next_index is not next_index_check and next_index is not len(word):
            split_indices.append(next_index)
            next_index_check = next_index
            next_index = next_camel_case_index(word, next_index, filter)

    if len(split_indices) > 0:
        split_indices.sort()
        return [word[i:j] for i, j in zip(split_indices, split_indices[1:]+[None])]
    return word


def next_camel_case_index(word, index, cc_filter):
    if index >= len(word):
        return index

    if word[index].isnumeric() and not bool(cc_filter & CamelCaseFilter.NUMBERS):
        return next_index_after_number(word, index, cc_filter)
    else:
        uc_word_valid = is_uc_word_valid(word, index, cc_filter)
        # if one digit numbers leading or one letter words and they are banned
        if is_one_letter_valid(word, index, cc_filter):
            if word[index].isupper() and uc_word_valid:
                return next_index_after_upper_case_word(word, index, cc_filter)
            elif word[index].islower():
                return next_index_after_lower_case_word(word, index, cc_filter)
        elif word[index].islower() and uc_word_valid:
            return next_index_after_lower_case_word(word, index, cc_filter)
    return index


def next_index_after_upper_case_word(word, index, filter):
    working_index = index
    working_index += 1
    while working_index < len(word):
        if not word[working_index].isupper():
            if working_index < len(word)-1 and word[working_index+1].islower():
                return working_index-1
            else:
                return working_index
        working_index += 1
    return index


def next_index_after_lower_case_word(word, index, filter):
    backup_index = index
    index += 1
    while index < len(word):
        if not word[index].islower():
            return index
        index += 1
    return backup_index


def next_index_after_number(word, index, filter):
    backup_index = index
    index += 1
    while index < len(word):
        if not word[index].isnumeric():
            return index
        index += 1
    return backup_index


def is_uc_word_valid(word, index, filter):
    return not is_uc_word(word, index) or not bool(filter & CamelCaseFilter.UPPER_CASE_WORDS)


def is_uc_word(word, index):
    return word[index].isupper() and (index == len(word) - 1 or not word[index + 1].isupper())


def is_one_letter_valid(word, index, filter):
    return not (is_last_letter_in_lc_word(word, index) and bool(filter & CamelCaseFilter.ONE_LETTER_WORDS)
                or is_last_letter_in_uc_word(word, index) and bool(filter & CamelCaseFilter.ONE_LETTER_WORDS))


def is_last_digit(word, index):
    return word[index].isnumeric() \
           and (index == len(word) - 1 or not word[index + 1].isnumeric())


def is_last_letter_in_word(word, index):
    return is_last_letter_in_lc_word(word, index) or is_last_letter_in_uc_word(word, index)


def is_last_letter_in_lc_word(word, index):
    return (word[index].isupper() or word[index].islower()) \
           and (index == len(word) - 1 or not word[index + 1].islower())


def is_last_letter_in_uc_word(word, index):
    return word[index].isupper() \
           and (index == len(word) - 1 or not word[index + 1].islower())


def get_potential_camel_case_indices(lookup_string, start_index=0, filter=CamelCaseFilter.NONE):
    indices = []
    char_list_regex = "A-Z"

    if not bool(filter & CamelCaseFilter.NUMBERS_LEADING):
        char_list_regex += "0-9"
    if not bool(filter & CamelCaseFilter.LOWER_CASE_LEADING):
        char_list_regex += "a-z"

    start_pattern = "(^[{0}])|((?![{0}]).[{0}])".format(char_list_regex)
    for m in re.finditer(start_pattern, lookup_string[start_index:]):
        index = m.start()
        if len(m.group(0)) > 1:
            index += 1
        indices.append(index)

    return indices



