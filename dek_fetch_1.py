#!/usr/bin/python3
# name:    dek_fetch.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-06-02 (YYYY-MM-DD)
# edit:
#
""" Collect the original .svg about DEK on Wikimedia.

There are multiple thousands of .svg files on Wikimedia sharing the tag

SVG Deutsche Einheitskurzschrift

This script automates the download of them.  It is possible to create
a list about all relevant data for free with this tag line on the page

https://tools.wmflabs.org/wikilovesdownloads/

The then provided archive should be unzipped.  The included text file
should be renamed in a pattern like

YYYY-MM-DD_DEK_input_list.txt

to reflect additions to this collection expected to growth further (at
present, 21k+ entries).  This text file is the sole expected parameter
when running this script by

python dek_fetch.py YYYY-MM-DD_DEK_input_list.txt

on the CLI of Python 3.  The script's use is constrained to Python 3
because the original file names contains chars like umlauts encoded in
UTF-8.  The script decodes the addresses given in the input list, and
deposit .svg file with help by Linux tool wget into folder raw_data.
If the folder is missing (initial download), the script will create
this folder.

Here, wget is considered as safer than alternatives because wget's
action will retain the public timestamp of the upload of the .svg to
the servers of Wikimedia rather than the timestamp when downloading
them to create a local copy. """

import os
import subprocess as sub
import sys
from urllib.parse import unquote


def check_python():
    """ Assure the script is used with Python 3, only. """
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def check_deposit_folder():
    """ Check the presence of folder raw_data; if absent, create it. """
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


def read_input_list():
    """ Retrieve the .svg files listed on Wikimedia's list.

        Read-out of the files' addresses on Wikimedia's servers, relay the
    decoded string to wget to store local copies.  Report if a string
    conversion failed in log 'failed_string_conversion.txt'. """
    try:
        if len(sys.argv[1]) > 1:
            try:
                input_file = str(sys.argv[1])
            except:
                print("The file was not found.")
    except:
        print("\nThe expected input instruction is: \n")
        print("    python dek_fetch.py YYYY-MM-DD_DEK_input_list.txt \n")
        sys.exit()

    address_register = []
    missed_data = []

    # work on decoding the addresses (back) into UTF-8:
    with open(input_file, mode="r") as source:
        for line in source:
            url = unquote(str(line).strip())
            address_register.append(url)
    address_register.sort()

    # fetch the .svg files by help of wget:
    root = os.getcwd()
    os.chdir("raw_data")

    for entry in address_register:
        print("{}".format(entry))
        try:
            command = str("wget -t 21 {}".format(entry))
            sub.call(command, shell=True)
        except IOError:
            missed_data.append(entry)
    os.chdir(root)

    # create the error log (string conversion) if neccessary:
    if len(missed_data) >= 1:
        with open("missed_data.txt", mode="w") as newfile:
            for missed in missed_data:
                retain = str("{}\n".format(missed))
                newfile.write(retain)


def main():
    """ Join the functions. """
    check_python()
    check_deposit_folder()
    read_input_list()


main()
