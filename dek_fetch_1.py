#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    dek_fetch.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-06-02 (YYYY-MM-DD)
# edit:    [2023-04-28 Fri]
#
"""Collect the original .svg about DEK from Wikimedia.

There are 39k+ of .svg files on Wikimedia sharing the tag

SVG Deutsche Einheitskurzschrift

created by Wikimedia user Thirunavukkarasye-Raveendran, who is not the
author of this project, and published as public domain.  The open site

https://tools.wmflabs.org/wikilovesdownloads/

generates a list of the relevant addresses for the files in question
with the keywords "SVG Deutsche Einheitskurzschrift" as zip-compressed
text file, used in the project

https://github.com/nbehrnd/dek_wikimedia

to eventually generate an Anki deck for training DEK.  To start, the
compilation o the addresses of the .svg on Wikimedia requires about
1:45 min:s on the server of Wikimedia.  Then, this script is launched
from the CLI of Python 3 by a call in pattern of

python3 dek_fetch_1.py addresss.txt

where `addresses.txt` is the file with Wikimedia's addresses, which
however may be of any name or file extension.  This command causes
the script to

+ remove entries which are not about .svg
+ rewrite the remaining addresses into a form safer for download (no
  umlauts and other characters which could confuse a web browser or a 
  computer shell as an instruction) into an intermediate file
  `list_accessed.txt` which is used in   the next step of this
  sequence.
+ launch `wget2` to download the .svg files in question.  In case the
  script is used in an environment other than Linux (e.g. Windows),
  then this requires to add `wget2` into the system's PATH variable.

Note: The download includes a default constraint of to 5k .svg per
      run.  Experience shows this is a safer approach to collect the
      files, than all at once.

Home repository of `wget2`: https://gitlab.com/gnuwget/wget2
Documentation: https://rockdaboot.github.io/wget2/md_wget2_manual.html
Entry in Linux Debian's repostories: https://tracker.debian.org/pkg/wget2
"""

import argparse
import os
import subprocess as sub
import sys
# import urllib.parse


def get_args():
    """collect instructions from the CLI"""
    parser = argparse.ArgumentParser(
        description='file fetcher for Wikimedia .svg about DEK',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "file",
        type=argparse.FileType('r'),
        help='Input text file, typically "wikimedia_addresses.txt"')
    parser.add_argument(
        "-n",
        "--number",
        metavar="",
        type=int,
        default=5000,
        help="specify the number of .svg to fetch from Wikimedia's servers.")
    return parser.parse_args()


def file_read(raw_data="", entries=0):
    """Transfer content of the input file into a register."""
    new_list = []
    try:
        with raw_data as source:
            new_list = [line.strip() for line in source]

    # except Exception:
    except IOError:
        print("File not accessible, exit.")
        sys.exit()

    new_list = new_list[:entries]
    return new_list


def retain_only_svg(listing=None):
    """ascertain to fetch only .svg files

    On occasion, other file types than .svg are tagged with 'DEK' - .mp3
    about languages classes already were observed in the past.  There is
    no intent to eventually include these into the Anki deck."""
    old_list = listing
    new_list = []

    for entry in old_list:
        if str(entry).endswith(".svg"):
            new_list.append(entry)

    return new_list


# def safe_addresses(listing=None):
#     """replace umlauts, parentheses, etc by safer encoding
#
#     Some of the addresses include umlauts, parentheses and other special
#     characters which either may be misinterpreted by the shell as (part
#     of) an instruction, or/and are not reliably transmitted as an address
#     of a web page.  This translation requires Python's standard library
#     `urllib.parse`."""
#     old_list = listing
#     new_list = []
#
#     for entry in old_list:
#         parsed = urllib.parse.urlparse(entry.strip())
#         new_url = urllib.parse.urlunparse(
#             parsed._replace(path=urllib.parse.quote(parsed.path)))
#         new_list.append(new_url)
#
#     return new_list


def list2file(listing=None, name=""):
    """record list of files of interes in a file"""

    try:
        with open(file=name, mode="w", encoding="utf-8") as newfile:
            for entry in listing:
                newfile.write("".join([str(entry), "\n"]))
    except IOError:
        print(f"Impossible to write to new file {name}.  Exit.")
        sys.exit()


def fetch_svg(name=""):
    """copy svg from wikimedia's serves into the local repository

    The action depends on wget2, which is advertised as a successor
    of higher efficiency of the more senior wget.  If the script is
    used in an other environment than Linux, then wget must be once
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
    print(f"The folder contains {counter} .svg files.")


def main():
    """join functionalities"""
    args = get_args()

    raw_data = file_read(args.file, args.number)
    filtered_list = retain_only_svg(raw_data)
    list2file(filtered_list, "svg_of_interest.txt")

    fetch_svg("svg_of_interest.txt")
    check_progress()

if __name__ == "__main__":
    main()
