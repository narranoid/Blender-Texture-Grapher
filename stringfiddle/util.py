
def without_empty(string_iterable):
    return [value for value in string_iterable if value != "" and value is not None]


def is_string(potential_string):
    return isinstance(potential_string, str)


def plain_join(strings):
    return "".join(strings)


def is_abbreviation_of(abbreviation, word):
    if len(word) <= 0 or len(abbreviation) <= 0 or word[0] != abbreviation[0]:
        return False

    word_index = 1
    abbreviation_index = 1
    while abbreviation_index < len(abbreviation) and word_index < len(word):
        if word[word_index] == abbreviation[abbreviation_index]:
            abbreviation_index += 1
        word_index += 1
    return abbreviation_index == len(abbreviation)
