#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    dek_fetch.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-06-02 (YYYY-MM-DD)
# edit:    2020-09-15 (YYYY-MM-DD)
#
"""Collect the original .svg about DEK from Wikimedia.

There are 21k+ of .svg files on Wikimedia sharing the tag

SVG Deutsche Einheitskurzschrift

created by Wikimedia user Thirunavukkarasye-Raveendran, who is not the
author of this project, and published as public domain.  The open site

https://tools.wmflabs.org/wikilovesdownloads/

generates a list of the relevant addresses for the files in question
with the keywords "SVG Deutsche Einheitskurzschrift" as zip-compressed
text file, or to use a recent version of wikimedia_addresses.txt from

https://github.com/nbehrnd/dek_wikimedia

The script is launched from the CLI of Python 3 by a call in pattern of

python dek_fetch_1.py wikimedia_addresss.txt [-i | -u]

The text file is used as input file.  Either -i, or -u as mutually
exclusive parameters discern between an initial collection of the data,
deposit in folder 'raw_data', or one to eventually update the already
curated earlier.  In the later case, data will be written into folder
'antechamber'.  Like in Python, lines starting by # in the address file
are skipped like comments.

If running Windows, the script will relay work to the wget program
(see https://en.wikipedia.org/wiki/Wget).  In Linux, the script aims
for the more efficient wget2 in first place, and wget as fall back; in
both cases GNU parallel shall improve the performance by using multiple
simultaneous download threads."""


import argparse
import os
import shutil
import subprocess as sub
import sys
from urllib.parse import unquote

root = os.getcwd()
intermediate_register = []
address_register = []
register = []  # stores the content of 'wikimedia_addresses.txt'


def check_python():
    """Assure the script is used with Python 3, only."""
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def file_read():
    """Transfer content of the input file into a register."""
    try:
        with args.inputfile as source:
            for line in source:
                register.append(str(line).strip())

    # except Exception:
    except IOError:
        print("File not accessible, exit.")
        sys.exit()
        #        print(parser.print_usage())


def check_raw_data_folder():
    """Check the presence of folder raw_data; if absent, create it."""
    for element in os.listdir("."):
        create = True
        if (str(element) == str("raw_data")) and os.path.isdir(element):
            create = False
            break

    if create:
        try:
            os.mkdir("raw_data")
        except IOError:
            print("Error to create folder 'raw_data'.  Exit.")
            sys.exit()


def check_antechamber_folder():
    """Ensure the presence of an empty folder antechamber."""
    for element in os.listdir("."):
        create = True
        if (str(element) == str("antechamber")) and os.path.isdir(element):
            create = False
            try:
                shutil.rmtree(element)
                os.mkdir("antechamber")
            except IOError:
                print("Error to empty folder 'antechamber'.  Exit.")
                sys.exit()
            break

    if create:
        try:
            os.mkdir("antechamber")
        except IOError:
            print("Error to create folder 'antechamber'.  Exit.")
            sys.exit()


def identify_addresses():
    """Identify the url addresses for the .svg to fetch."""
    for line in register: #[:20]:  # LIMITED ONLY TO CHECK IF IT WORKS
        if str(line).startswith("#") is False:
            url = unquote(str(line).strip())
            address_register.append("{}\n".format(url))
    address_register.sort()


def processing_for_windows():  # TODO: CHECK IF THIS IS WORKING!
    """Fetch the .svg sequentially with wget in linear fashion.

    The wget tool is available for Windows, too.  As a fallback, its
    use is restricted to the already known, previously used linear
    approach; fetching one file at a time.  The Linux analogue of this
    function, processing_for_linux, aims to fetch the data by multiple
    simultaneous download threads which overall may be faster."""

    for address in address_register:
        try:
            command = str("wget -t 21 {}".format(str(address).strip()))
            sub.call(command, shell=True)
        except IOError:
            print("\nCheck if wget was installed in your system.")
            print("See, for example, https://en.wikipedia.org/wiki/Wget")
            print("The script stops here.  Exit.")
            sys.exit()


def processing_for_linux():  # known to work in Linux Debian 10/sid
    """Fetch the .svg with multiple simultaneous instances of wget.

    The initial thought to use Linux' xargs -- following an example on

    https://stackoverflow.com/questions/5546694/parallel-wget-download-url-list-and-rename

    in a pattern like

    cat test.txt | xargs -P 4 wget -nv -t 21

    to pipe the content of file test.txt to run up to four concurrent
    instances of wget (itself in the non-verbose mode, up to 21 trials
    to fetch the .svg currently in question) was dropped.  With 21k+,
    sometimes long addresses might require particular xargs parameters
    still unfamiliar to mine.

    RegioSQM however showcases "GNU parallel" as an alternative and
    hence used used instead.  For efficiency in the data transfer, the
    first attempt is to use wget2, and wget as a fallback.  Note, GNU
    parallel, wget2, and get may require an explicit installation from
    the repositories, e.g., Debian 10."""

    use_processors = 0
    processors_available = int(len(os.sched_getaffinity(0)))
    if processors_available == 1:
        use_processors = 1
    if processors_available > 1:
        use_processors = processors_available - 1
    else:
        print("Error determining the number of processors available.  Exit.")
        sys.exit()

    try:
        with open("addresslist.txto", mode="w") as newfile:
            for address in address_register:
                retain = str(address).strip()
                newfile.write("{}\n".format(retain))
    except IOError:
        print("Error writing intermediate 'addresslist.txto'.  Exit.")
        sys.exit()


# known to work -- faster, start:
    try:
        command = str("cat addresslist.txto | parallel -j4 'wget2 {}'")
        sub.call(command, shell=True)
    except IOError:
        print("parallel/wget2 failed.  Exit")
        # known to work, end.

        # known to work, not as fast, start:
        try:
            command = str("cat addresslist.txto | parallel -j4 'wget {}'")
            sub.call(command, shell=True)
        except IOError:
            print("parallel/wget failed.  Exit")
            # exit method not as fast.

            # the linear method / slow:
            # known to work, start:
            with open("addresslist.txto", mode="r") as source:
                for entry in source:
                    try:
                        command = str("wget2 -t 21 {}".format(
                            str(entry).strip()))
                        sub.call(command, shell=True)
                    except IOError:
                        print("\nCheck if wget was installed in your system.")
                        print(
                            "See, for example, https://en.wikipedia.org/wiki/Wget"
                        )
                        print("The script stops here.  Exit.")
                        sys.exit()
                    # known to work, end.


def cleaning():
    """Remove the intermediate 'adresslist.txto' file."""
    os.chdir(root)

    try:
        os.remove('addresslist.txto')
    except IOError:
        pass


# clarifications for argparse, start:
parser = argparse.ArgumentParser(
    description='file fetcher for Wikimedia .svg about DEK')
parser.add_argument(
    'inputfile',
    type=argparse.FileType('r'),
    help='Input text file, typically "wikimedia_addresses.txt"')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i',
                   '--initial',
                   action='store_true',
                   help='initial fetch of the .svg data')
group.add_argument('-u',
                   '--update',
                   action='store_true',
                   help='update fetch of the .svg data')

args = parser.parse_args()
# clarifications for argparse, end.

if __name__ == "__main__":
    file_read()
    if args.initial:
        print("aim for an initial fetch of the data.")
        check_raw_data_folder()
    elif args.update:
        print("aim to update already existing data.")
        check_antechamber_folder()
    identify_addresses()

    if args.initial:
        os.chdir("raw_data")
        if sys.platform.startswith("win"):
            processing_for_windows()
        elif sys.platform.startswith("lin"):
            processing_for_linux()
        else:
            print(
                "Currently, your OS is not supported.  Try Linux or Windows.")
            sys.exit()

    if args.update:
        os.chdir("antechamber")
        if sys.platform.startswith("win"):
            processing_for_windows()
        elif sys.platform.startswith("lin"):
            processing_for_linux()
        else:
            print(
                "Currently, your OS is not supported.  Try Linux or Windows.")
            sys.exit()
