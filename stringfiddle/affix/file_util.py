
from . import util as affix_util
import os


def find_affixed_files(files, trim_extensions=None, norm_paths=False, norm_case=False):
    file_names = []
    for file_or_file_name in files:
        file_name = get_file_name_checked(file_or_file_name)
        if trim_extensions:
            file_name = remove_extension(file_name, trim_extensions)
        if norm_paths:
            file_name = os.path.normpath(file_name)
        if norm_case:
            file_name = os.path.normcase(file_name)
        file_names.append(file_name)
    return affix_util.find_affixed_groups(file_names)


def remove_extension(file_name, extensions):
    for ext in extensions:
        if file_name.lower().endswith("." + ext.lower()):
            trim_index = (len(ext) + 1) * -1
            return file_name[:trim_index]
    return file_name


def remove_extensions(file_names, extensions):
    names_wo_extensions = []
    for file_name in file_names:
        names_wo_extensions.append(remove_extension(file_name, extensions))
    return names_wo_extensions


def resolve_extension(target, files_w_extension):
    target_str = affix_util.get_string_checked(target)
    for file_or_file_name in files_w_extension:
        file_name = get_file_name_checked(file_or_file_name)
        if file_name.startswith(target_str):
            return file_or_file_name
    return None


def resolve_extensions(targets, files_w_extension):
    targets_iter = affix_util.get_string_iterator(targets)
    ext_dict = dict()

    for target in targets_iter:
        resolved = resolve_extension(target, files_w_extension)
        if resolved:
            ext_dict[target] = resolved
    return ext_dict


def resolve_supported_extension(target, supported_extensions):
    target_str = affix_util.get_string_checked(target)
    for ext in supported_extensions:
        try_path = target_str + "." + ext
        if os.path.exists(try_path):
            return try_path
    return None


def resolve_supported_extensions(targets, supported_extensions):
    resolved = list()
    for target in targets:
        resolved.append(resolve_supported_extension(target, supported_extensions))
    return resolved


def get_file_name_checked(file_or_file_name):
    return file_or_file_name if isinstance(file_or_file_name, str) else file_or_file_name.name
