#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
name   : dek_clearance.py
author : nbehrnd@yahoo.com
license: GPLv2
date   : <2023-06-04 Sun>
edit   :
"""

import argparse
import os
import shutil
import sys


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""The optimization with svgcleaner may yield empty .svg,
and the .csv still may contain entries (now) irrelevant to the Anki deck to
assemble.  This script lints the .csv and working directory accordingly.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='the already once revised listing of addresses',
                        type=argparse.FileType('rt'),
                        default=None)

    return parser.parse_args()


def remove_empty_files():
    """remove .svg which, after optimization, are empty

    Overall, the optimization with `dek_optimize_5b.sh` proceeds faster, than
    the one by `dek_optimize_5a.sh`, but sometimes yields an empty .svg.  Move
    these files into a separate folder."""
    deposit = str("empty_svg")
    empty = []  # files where optimization lead to be empty

    try:
        os.mkdir(deposit)
    except IOError:
        print(f"Folder {deposit} already exist, hence exit.")
        sys.exit()

    for file in os.listdir("."):
        if file.endswith(".svg"):
            if os.path.getsize(file) == 0:
                shutil.move(file, deposit)
                empty.append(file)

    if empty:
        print(f"Check {deposit} for {len(empty)} empty files.")
    else:
        os.rmdir(deposit)


def remove_entries_without_file(reference):
    """remove entries from the .csv without corresponding .svg

    The .csv file may contain entries to .svg which do not exist (anymore).
    To prevent presence of an Anki card with long hand form, but lacking a
    short hand symbolization, remove these entries."""
    new_list = []

    with open(file=reference, mode="rt", encoding="utf-8") as source:
        for line in source:
            line = str(line).strip()
            address = line.split("; ")[1]
            address = address[10:-2]
            if os.path.isfile(address):
                new_list.append(line)

    os.remove(reference)

    with open(file=reference, mode="wt", encoding="utf-8") as new:
        for entry in new_list:
            new.write(f"{entry}\n")


def remove_files_without_reference(reference):
    """remove .svg files without entry in the .csv

    There still may be .svg files in the current working directory which per
    the listing in the .csv no longer are of interest.  For now, these files
    should be removed.  This function aims to complement the one earlier."""
    checklist = []

    with open(file=reference, mode="rt", encoding="utf-8") as source:
        for line in source:
            line = str(line).strip()
            address = line.split("; ")[1]
            address = address[10:-2]
            checklist.append(address)

    check_set = set(checklist)

    for file in os.listdir("."):
        if str(file).endswith(".svg"):
            if str(file) not in check_set:
                os.remove(file)


def main():
    """Join the functionalities"""

    args = get_args()
    remove_empty_files()
    remove_entries_without_file(args.file.name)
    remove_files_without_reference(args.file.name)


# --------------------------------------------------
if __name__ == '__main__':
    main()
