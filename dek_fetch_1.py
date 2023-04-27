#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    dek_fetch.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-06-02 (YYYY-MM-DD)
# edit:    [2023-04-27 Thu]
#
"""Collect the original .svg about DEK from Wikimedia.

There are 39k+ of .svg files on Wikimedia sharing the tag

SVG Deutsche Einheitskurzschrift

created by Wikimedia user Thirunavukkarasye-Raveendran, who is not the author of
this project, and published as public domain.  The open site

https://tools.wmflabs.org/wikilovesdownloads/

generates a list of the relevant addresses for the files in question with the
keywords "SVG Deutsche Einheitskurzschrift" as zip-compressed text file, used in
the project

https://github.com/nbehrnd/dek_wikimedia

to eventually generate an Anki deck for training DEK.  To start, the compilation
o the addresses of the .svg on Wikimedia requires about 1:45 min:s on the server
of Wikimedia.  Then, this script is launched from the CLI of Python 3 by a call
in pattern of

python3 dek_fetch_1.py wikimedia_addresss.txt

where `wikimedia_addresses.txt` is the file with Wikimedia's addresses, which
however may be of any name or file extension.  This command causes the script to

+ remove entries which are not about .svg
+ rewrite the remaining addresses into a form safer for download (no umlauts and
  other characters which could confuse a web browser or a computer shell as an
  instruction) into an intermediate file `list_accessed.txt` which is used in
  the next step of this sequence.
+ launch `wget2` to download the .svg files in question.  In case the script is
  used in an environment other than Linux (e.g. Windows), then this requires to
  add `wget2` into the system's PATH variable.

  Home repository of `wget2`: https://gitlab.com/gnuwget/wget2
  Documentation: https://rockdaboot.github.io/wget2/md_wget2_manual.html
  Entry in Linux Debian's repostories: https://tracker.debian.org/pkg/wget2
"""

import argparse
import os
import shutil
import subprocess as sub
import sys
import urllib.parse

root = os.getcwd()
intermediate_register = []
address_register = []
register = []  # stores the content of 'wikimedia_addresses.txt'


def file_read():
    """Transfer content of the input file into a register."""
    new_list = []
    try:
        with args.inputfile as source:
            for line in source:
                new_list.append(str(line).strip())

    # except Exception:
    except IOError:
        print("File not accessible, exit.")
        sys.exit()

    return new_list


def check_raw_data_folder():
    """Check the presence of folder raw_data; if absent, create it."""
    remove = False

    for element in os.listdir("."):
        if (str(element) == str("raw_data")) and os.path.isdir(element):
            print('There already is a folder "raw_data" -- what to do now?')
            print("[O]verwrite old folder, or [c]ancel further processing.")

            check = input()
            if str(check) in ['o', 'O']:
                remove = True
            elif str(check) in ['c', 'C']:
                sys.exit()
            else:
                print("Invalid input, exit.")
                sys.exit()

    if remove:
        shutil.rmtree("raw_data")
    os.mkdir("raw_data")


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


def safe_addresses(listing=None):
    """replace umlauts, parentheses, etc by safer encoding

    Some of the addresses include umlauts, parentheses and other special
    characters which either may be misinterpreted by the shell as (part
    of) an instruction, or/and are not reliably transmitted as an address
    of a web page.  This translation requires Python's standard library
    `urllib.parse`."""
    old_list = listing
    new_list = []

    for entry in old_list:
        parsed = urllib.parse.urlparse(entry.strip())
        new_url = urllib.parse.urlunparse(
            parsed._replace(path=urllib.parse.quote(parsed.path)))
        new_list.append(new_url)

    return new_list


def list2file(listing=None, name=""):
    """write a list into a permanent record"""

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
        command = str(f"wget2 --input-file {name} --continue -nv \
            --input-encoding utf-8")
        print(f"\ncommand issued:\n   {command}")
        sub.call(command, shell=True)
    except IOError:
        print("Check if `wget2` was properly installed.  Exit.")
        sys.exit()


# clarifications for argparse, start:
parser = argparse.ArgumentParser(
    description='file fetcher for Wikimedia .svg about DEK')
parser.add_argument(
    'inputfile',
    type=argparse.FileType('r'),
    help='Input text file, typically "wikimedia_addresses.txt"')
args = parser.parse_args()
# clarifications for argparse, end.

if __name__ == "__main__":
    #    check_raw_data_folder()
    raw_data = file_read()
    only_svg = retain_only_svg(listing=raw_data)

    #    reencoded = safe_addresses(listing=only_svg)

    list2file(listing=only_svg, name="list_accessed.txt")
    fetch_svg(name="list_accessed.txt")
