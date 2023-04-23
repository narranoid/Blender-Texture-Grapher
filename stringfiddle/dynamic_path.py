
import os
import os.path
from enum import Enum


class PathFormat(Enum):
    RUNNING_SYSTEM = 1
    POSIX = 2
    NT = 4
    MAC = 8
    OS_2_EMX = 16

def get_module_name(path_format, default_module_prefix="path"):
    mapping = {
        PathFormat.RUNNING_SYSTEM: default_module_prefix,
        PathFormat.POSIX: "posixpath",
        PathFormat.NT: "ntpath",
        PathFormat.MAC: "macpath",
        PathFormat.OS_2_EMX: "os2emxpath"
    }
    return mapping.get(path_format, default_module_prefix)


def get_full_module_name(path_format, default_module_prefix="path"):
    mod_name = get_module_name(path_format)
    if mod_name is not None and len(mod_name) > 0:
        mod_name = "." + mod_name

    return "os" + mod_name


def get_module(path_format, default_module_prefix="path"):
    return __import__("os")
    #return __import__(get_full_module_name(path_format))

def get_full_function_name(function_name, path_format, default_module_prefix="path"):
    prefix = get_module_name(path_format, default_module_prefix)
    if prefix is not None and len(prefix) > 0:
        prefix += "."
    return prefix + function_name

def get_object(function_name, path_format, default_module_prefix="path"):
    mod_name = get_full_module_name(path_format, default_module_prefix)
    mod = __import__(mod_name, globals(), locals(), [function_name], 0)
    return getattr(mod, function_name)


def call(path, function_name, path_format, default_module_prefix="path"):
    func = get_object(function_name, path_format, default_module_prefix)
    return func(path)


def splitdrive(path, path_format=PathFormat.RUNNING_SYSTEM):
    return call(path, "splitdrive", path_format)


def splitext(path, path_format=PathFormat.RUNNING_SYSTEM):
    return call(path, "splitext", path_format)


def split(path, path_format=PathFormat.RUNNING_SYSTEM):
    return call(path, "split", path_format)


def sep(path_format=PathFormat.RUNNING_SYSTEM):
    return get_object("sep", path_format, "")


def altsep(path_format=PathFormat.RUNNING_SYSTEM):
    return get_object("altsep", path_format, "")


def pathsep(path_format=PathFormat.RUNNING_SYSTEM):
    return get_object("pathsep", path_format, "")


def join(paths, path_format=PathFormat.RUNNING_SYSTEM):
    return call(paths, "join", path_format)
