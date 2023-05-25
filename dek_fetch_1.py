#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name:    dek_fetch_1.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    <2020-06-02 Tue>
# edit:    <2023-05-25 Thu>
#
"""Collect the original .svg about DEK from Wikimedia.

There are 39k+ of .svg files on Wikimedia sharing the tag

SVG Deutsche Einheitskurzschrift

created by Wikimedia user Thirunavukkarasye-Raveendran, who is not the
author of this project, and published as public domain.  The open site

https://tools.wmflabs.org/wikilovesdownloads/

generates a list of the relevant addresses for the files in question
with the keywords "SVG Deutsche Einheitskurzschrift" as zip-compressed
text files, used in the project

https://github.com/nbehrnd/dek_wikimedia

to eventually generate an Anki deck for training DEK.  To start, the
compilation of the addresses of the .svg on Wikimedia requires about
1:45 min:s on the server of Wikimedia.  Then, this script is launched
from the CLI of Python 3 by a call in pattern of

python3 dek_fetch_1.py addresses01.txt

where `addresses01.txt` is the file with Wikimedia's addresses, which
however may be of any name or file extension.  This command causes
the script to

+ access the list of addresses the Wikimedia download portal provided
+ remove entries which are not about .svg
+ launch `wget2` to download the .svg files in question.  In case the
  script is used in an environment other than Linux (e.g. Windows),
  then this requires to add `wget2` into the system's PATH variable.

Note: The download includes a default constraint of to 5k .svg per
      run.  Experience shows this is a safer approach to collect the
      files, than all at once.

Home repository of `wget2`: https://gitlab.com/gnuwget/wget2
Documentation: https://rockdaboot.github.io/wget2/md_wget2_manual.html
Entry in Linux Debian's repositories: https://tracker.debian.org/pkg/wget2
"""

import argparse
import os
import shutil
import subprocess as sub
import sys


def get_args():
    """collect instructions from the CLI"""
    parser = argparse.ArgumentParser(
        description="fetch .svg about DEK from Wikimedia with get2",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "file",
        type=argparse.FileType("rt"),
        help="text file with the addresses on Wikimedia's servers")

    parser.add_argument(
        "-n",
        "--number",
        metavar="",
        type=int,
        default=5000,
        help="specify the number of .svg to fetch from Wikimedia's servers")

    return parser.parse_args()


def file_read_2(raw_data, entries=0):
    """read the addresses into the program"""
    register = []
    for line in raw_data:
        register.append(str(line).strip())
    register = register[:entries]

    raw_data.close()

    return register


def retain_only_svg(listing=None):
    """retain only addresses about .svg files

    On occasion, other file types than .svg are tagged with 'DEK' - .mp3
    about languages classes already were observed in the past.  There is
    no intent to eventually include these into the Anki deck."""
    old_list = listing
    new_list = []
    bad_list = []

    for entry in old_list:
        if str(entry).endswith(".svg"):
            new_list.append(entry)
        else:
            bad_list.append(entry)

    if bad_list:
        try:
            with open(file="bad_list.txt", mode="wt", encoding="utf-8") as new:
                for entry in bad_list:
                    new.write(f"{entry} \n")
            print(f"See `bad_list.txt` for {len(bad_list)} entries removed.")
        except OSError:
            print("Error writing file `bad_list.txt`.")

    return new_list


def list2file(listing=None, name=""):
    """record list of files of interest in a file"""

    try:
        with open(file=name, mode="wt", encoding="utf-8") as newfile:
            for entry in listing:
                newfile.write("".join([str(entry), "\n"]))
    except IOError:
        print(f"Impossible to write to new file {name}.  Exit.")
        sys.exit()


def fetch_svg(name=""):
    """copy svg from Wikimedia's serves into the local repository

    The action depends on wget2, which is advertised as a successor
    of higher efficiency of the more senior wget.  If the script is
    used in an other environment than Linux, then wget2 must be once
    added to the system's PATH variable."""

    try:
        command = str(
            f"wget2 --input-file {name} --continue -nv --input-encoding utf-8")
        print(f"\ncommand issued:\n   {command}")
        sub.call(command, shell=True)
    except IOError:
        print("Check if `wget2` was properly installed.  Exit.")
        sys.exit()


def check_progress():
    """report how many .svg were saved"""
    counter = 0
    for file in os.listdir("."):
        if str(file).endswith(".svg"):
            counter += 1
    print(f"\nIn total, {counter} .svg files were collected.")


def tidy_up(name=""):
    """clear the space for next batch of .svg data"""

    depot = "_".join(["depot", name[:-4]])
    try:
        os.mkdir(depot)
    except OSError:
        print(f"\nStop: check first if folder {depot} already exists -- exit.")
        sys.exit()

    for file in os.listdir("."):
        if file.endswith(".svg"):
            try:
                shutil.move(file, depot)
            except OSError:
                print(f"transfer of {file} to {depot} failed")

    try:
        shutil.move("svg_of_interest.txt", depot)
    except OSError:
        print("Failed to secure file 'svg_of_interest.txt'")


def main():
    """join functionalities"""
    args = get_args()

    raw_list = file_read_2(args.file, args.number)
    filtered_list = retain_only_svg(raw_list)
    list2file(filtered_list, "svg_of_interest.txt")

    fetch_svg("svg_of_interest.txt")
    check_progress()

    tidy_up(args.file.name)


if __name__ == "__main__":
    main()
