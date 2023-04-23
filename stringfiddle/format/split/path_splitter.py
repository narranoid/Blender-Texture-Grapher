
from enum import Flag

from . import StringSplitter
from ... import dynamic_path as dynamic_path
from ...dynamic_path import PathFormat


class SplitOption(Flag):
    NONE = 0
    DRIVE = 1
    EXT = 2
    SEP = 4
    ALT_SEP = 8
    PATH_SEP = 16


class PathSplitter(StringSplitter):

    def __init__(self, path_format=PathFormat.RUNNING_SYSTEM, split_options=SplitOption.SEP):
        super(PathSplitter, self).__init__()
        self.__path_format = path_format
        self.__split_options = split_options

    def split(self, split_string):
        result_list = []
        if bool(self.__split_options & SplitOption.PATH_SEP):
            path_sep_list = split_string.split(dynamic_path.pathsep(self.__path_format))
            for path_sep_item in path_sep_list:
                result_list += self.split_path(path_sep_item)
        else:
            result_list += self.split_path(split_string)
        return result_list

    def split_path(self, split_string):
        working_string = split_string
        result_list = []
        ext = None
        drive = None

        if bool(self.__split_options & SplitOption.DRIVE):
            drive_split = dynamic_path.splitdrive(working_string)
            working_string = drive_split[1]
            drive = drive_split[0]

        if bool(self.__split_options & SplitOption.EXT):
            ext_split = dynamic_path.splitext(working_string, self.__path_format)
            working_string = ext_split[0]
            ext = ext_split[1]

        if bool(self.__split_options & SplitOption.SEP):
            sep = dynamic_path.sep(self.__path_format)
            split_list = working_string.split(sep)
            result_list += split_list

        if bool(self.__split_options & SplitOption.ALT_SEP):
            altsep = dynamic_path.altsep(self.__path_format)
            if altsep is not None:
                if bool(self.__split_options & SplitOption.SEP):
                    old_result_list = result_list
                    result_list = list()
                    for o in old_result_list:
                        split_list = o.split(altsep)
                        result_list += split_list
                else:
                    split_list = working_string.split(altsep)
                    result_list += split_list

        if len(result_list) <= 0:
            result_list.append(working_string)

        if ext:
            result_list.append(ext)

        if drive:
            result_list.insert(0, drive)

        return result_list
