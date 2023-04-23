import tkinter as tk
from tkinter import filedialog

from stringfiddle.affix.file_util import *
from stringfiddle.affix import AffixAspect
from stringfiddle.affix.match import ArithmeticScoreAffixMatcher
from stringfiddle.format import CombinedFormatter
from stringfiddle.format.split import SeparatorSplitter, CamelCaseSplitter, CamelCaseFilter, PathSplitter, SplitOption, PathFormat
from stringfiddle.format.join import SeparatorJoiner
from stringfiddle.format.modify import CaseModifier, CaseOption
from stringfiddle.format.filter import IndexFilter


def test_affix_matching():
    root = tk.Tk()
    root.withdraw()

    affix_matcher = ArithmeticScoreAffixMatcher(AffixAspect.GROUP_LENGTH)

    file_paths_joined = filedialog.askopenfilenames()
    file_paths = list(file_paths_joined)

    name_groups = find_affixed_files(file_paths, trim_extensions=["png", "jpg", "tif"])
    best_match = affix_matcher.get_best_match(name_groups)
    index = 1

    best_ids = best_match.stems
    formatter = CombinedFormatter([
        SeparatorSplitter(["_", "-", ".", " "]),
        CamelCaseSplitter(CamelCaseFilter.SINGLES),
        CaseModifier(CaseOption.UC_FIRST),
        IndexFilter([1]),
        SeparatorJoiner(" ")
    ])
    # best_ids = formatter.format(best_ids)

    # formatting:
    # split by separators
    # split by camel case
    # remove unwanted values
    #
    # upper case first letter for each word, lower case everything else
    # join by space

    print("Best Match:")
    for n in best_match:
        # print("")
        # print(resolve_extension(n, file_paths))
        print(n.prefix + "     " + n.stem + "     " + n.postfix)

    print("")
    for g in name_groups:
        print("Group "+str(index))
        index += 1
        for n in g:
            #print("")
            print(resolve_extension(n, file_paths))
            print(n.prefix + "     " + n.stem + "     " + n.postfix)

    print("Best IDs:")
    for n in best_ids:
        # print("")
        # print(resolve_extension(n, file_paths))
        #for n2 in formatter.format_to_string(n):
        #   print(n2)
        print(formatter.format_to_string(n))

def test_path_splitter():
    splitter = PathSplitter(path_format=PathFormat.RUNNING_SYSTEM, split_options=SplitOption.DRIVE | SplitOption.ALT_SEP | SplitOption.SEP | SplitOption.EXT)
    test_str = r"A://VERY/ALTERNATIVE/\PATH.txt"
    split_result = splitter.format(test_str)
    for s in split_result:
        print(s)

if __name__ == "__main__":
    test_path_splitter()
    #test_affix_matching()
