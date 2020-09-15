#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    dek_rename.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-31 (YYYY-MM-DD)
# edit:    2020-09-15 (YYYY-MM-DD)
#
"""Rename the .svg for an Anki deck.

There already is an Anki deck about steno / DEK using .png.  At present,
its coverage is differs and there is overlap to the one when accessing
the ones drawn and filed by Thirunavukkarasye-Raveendran as .svg on
Wikimedia.  There is no reason to create an Anki deck which would
overwrite the former.  Thus, .svg of this project will be renamed in a
pattern of

DEK_VS_steno_svg_-_name.svg

where "DEK_vs_steno" reflects the content briefly (and separates this
deck from decks related to DEK's work) about the system (Deutsche
Einheitskurzschrift, Verkehrsschrift / first level of simplification),
and what seems to be short enough (steno) to ring a bell even for non-
specialists about the deck's purpose.  Even if not this popular like
"Gregg" or "shorthand", a colloquial "steno" equally may be understood
in other languages of the Latin script, too.

Because the file names may contain umlauts, the script's action is
constrained to Python 3.  It is launched from the CLI by

python dek_rename.py [-i | -u]

to either work on data of an initial fetch (parameter -i), or on data
leading to an update (parameter -u).  Folders 'dek_workshop' will be
populated, to preserve the original data from further processing."""

import argparse
import os
import shutil
import sys


def check_python():
    """ Assure the script is used with Python 3, only. """
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def only_check_presence_raw_data():
    """ This time, only probe if there is folder raw_data. """
    presence_raw_data = False
    for element in os.listdir("."):
        if (str(element) == str("raw_data")) and os.path.isdir(element):
            presence_raw_data = True
            break
    if presence_raw_data is False:
        print("Folder 'raw_data' is missing.  Exit.")
        sys.exit()


def only_check_presence_antechamber():
    """ This time, only probe if there is folder antechamber. """
    presence_raw_data = False
    for element in os.listdir("."):
        if (str(element) == str("antechamber")) and os.path.isdir(element):
            presence_raw_data = True
            break
    if presence_raw_data is False:
        print("Folder 'antechamber' is missing.  Exit.")
        sys.exit()


def check_workshop_folder():
    """Work on the files should take place in a dedicated folder."""
    create = True
    for element in os.listdir("."):
        if (str(element) == str("dek_workshop")) and os.path.isdir(element):
            try:
                shutil.rmtree("dek_workshop")
                os.mkdir("dek_workshop")
            except IOError:
                print("Creation of folder 'dek_workshop' failed.  Exit.")
            break

    if create:
        try:
            os.mkdir("dek_workshop")
        except IOError:
            print("Creation of folder 'dek_workshop' failed.  Exit.")
            sys.exit()


def inital_copy():
    """Provide 'dek_workshop' with copies about the initally fetched .svg."""
    root = os.getcwd()
    register = []

    os.chdir("raw_data")
    for file in os.listdir("."):
        if file.endswith(".svg"):
            register.append(file)
    register.sort()

    for entry in register:
        print(entry)
        old_path = os.path.join(os.getcwd(), str(entry))

        key = str(entry).split("_-_")[-1]
        new_file_name = ''.join(["DEK_VS_steno_svg_-_", str(key)])

        new_path = os.path.join(root, str("dek_workshop"), str(new_file_name))
        try:
            shutil.copy(old_path, new_path)
        except IOError:
            print("Error copying file '{}' into folder 'dek_worksop'.".format(
                entry))
            continue


def updating_copy():
    """Populate 'dek_workshop' for the updating branch."""
    root = os.getcwd()
    register = []

    for file in os.listdir("."):
        if file.endswith(".svg"):
            register.append(file)
    register.sort()

    for entry in register:
        print(entry)
        old_path = os.path.join(root, str(entry))

        key = str(entry).split("_-_")[-1]
        new_file_name = ''.join(["DEK_VS_steno_svg_-_", str(key)])

        new_path = os.path.join(root, str("dek_workshop"), str(new_file_name))
        try:
            shutil.copy(old_path, new_path)
        except IOError:
            print("Error copying file '{}' into folder 'dek_worksop'.".format(
                entry))
            continue


# clarifications for argparse, start:
parser = argparse.ArgumentParser(
    description='.svg file renamer for Wikimedia .svg about DEK')

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
    check_python()
    if args.initial:
        print("aim for an initial fetch of the data.")
        only_check_presence_raw_data()

        check_workshop_folder()
        inital_copy()

    elif args.update:
        print("aim to update already existing data.")
        only_check_presence_antechamber()
        os.chdir("antechamber")
        check_workshop_folder()
        updating_copy()
