#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    dek_update_new_1c.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-09-08 (YYYY-MM-DD)
# edit:    2020-09-11 (YYYY-MM-DD)
#
"""Indicate the newly written DEK .svg for a visual inspection.

Wikimedia user Thirunavukkarasye-Raveendran, who is not author of this
project, constantly generates new .svg files about the first degree of
simplification within the DEK.  Prior to processing and inclusion of
the new .svg into the already existing Anki deck, their inspection may
spur feedback to him, such as a suggest to draw examples previously
not considered.

The identification of "new .svg files" relies on a comparison of file
names of previously fetched .svg (stored in folder raw_data) with the
newly fetched .svg data deposit in folder antechamber.  Thus, this
script is to be placed one level above the two folders.  Because file
names are expected to contain non-ASCII characters (e.g., umlauts),
the script's action is restricted to work with Python3.  Launch it
from the CLI by

python dek_update_new_1c.py

without the provision of parameters.  The script will create a folder
new_svg next to folder antechamber with copies of these newly created
.svg data."""

import os
import shutil
import sys

raw_data = []
antechamber_data = []


def check_python():
    """Assure the script is used with Python 3, only."""
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def check_raw_data_folder():
    """Check the presence of folder raw_data."""
    for element in os.listdir("."):
        check = False
        if (str(element) == str("raw_data")) and os.path.isdir(element):
            check = True
            break

    if check is False:
        print("Folder 'raw_data' is missing.  Exit.")
        sys.exit()


def check_antechamber_folder():
    """Check the presence of folder antechamber."""
    for element in os.listdir("."):
        check = False
        if (str(element) == str("antechamber")) and os.path.isdir(element):
            check = True
            break

    if check is False:
        print("Folder 'antechamber' is missing.  Exit.")
        sys.exit()


def record_present_raw_files():
    """Identify the .svg in folder raw_data."""
    root = os.getcwd()
    os.chdir("raw_data")

    for file in os.listdir("."):
        if file.endswith(".svg"):
            raw_data.append(file)

    os.chdir(root)


def record_antechamber_files():
    """Identify the .svg in folder antechamber"""
    root = os.getcwd()
    os.chdir("antechamber")

    for file in os.listdir("."):
        if file.endswith(".svg"):
            antechamber_data.append(file)

    os.chdir(root)


def copy_new_files():
    """Identify the new files and copy them into folder new_svg."""
    try:
        os.mkdir("new_svg")
    except IOError:
        print("Error creating a separate folder 'new_svg'.  Exit.")
        sys.exit()

    set_raw_data = set(raw_data)
    set_antechamber_data = set(antechamber_data)
    set_new_data = set_antechamber_data - set_raw_data

    for entry in set_new_data:
        source = os.path.join(str(os.getcwd()), str("antechamber"), str(entry))
        deposit = os.path.join(str(os.getcwd()), str("new_svg"), str(entry))
        try:
            shutil.copy(source, deposit)
        except IOError:
            print("Problem to copy file {}.  Script continues to work.".format(
                entry))
            continue


def main():
    """Join the functions."""
    check_python()
    check_raw_data_folder()
    check_antechamber_folder()
    record_present_raw_files()
    record_antechamber_files()
    copy_new_files()


if __name__ == "__main__":
    main()

