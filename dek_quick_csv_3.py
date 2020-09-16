#!/usr/bin/python3
# -*- coding: utf-8 -*-

# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-31 (YYYY-MM-DD)
# edit:    2020-09-15 (YYYY-MM-DD)
#
"""Quick generation of a minimal relational .csv table for Anki.

The programmatic generation of an Anki deck requires a text file to
relate the file names of the DEK .svg to consider with a keyword.  By
this script, this minimal information is stored in a permanent record.

Deposit this script one level above the folder 'raw_data' (working to
create the Anki deck for the first time) and 'antechamber' (present if
eventually updating an already existing Anki deck).  From the CLI of
Python 3, launch the script by

python deck_quick_csv.py [-i | -u]

with mandatory provision of either parameter -i (for an initial fetch
of .svg) or -u (to update an already existing set of .svg / Anki deck).

The newly written file 'csv2anki.csv' retains for each file a 'key'
and a 'file name', separated by a semicolon in the pattern of

A-Saite; <img src="DEK_VS_steno_svg_-_A-Saite.svg">

Anki permits only UTF-8 encoded relational tables and some file names
contain special characters (e.g., umlauts).  Thus, the script's action
is constrained to Python 3.

Because file 'csv2anki.csv' actually is used as mandatory parameter by
script dek_csv4.py to extend the file indexing, file 'csv2anki.csv' is
deposited both in the folder of 'raw_data' / 'antechamber' as well as
their sub-subfolders 'dek_workshop' where it will be accessed again."""

import argparse
import os
import shutil
import sys

from datetime import date


def check_python():
    """Assure the script is used with Python 3, only."""
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def only_check_presence_workshop():
    """Probe the presence of folder 'dek_workshop'."""
    presence_raw_data = False
    for element in os.listdir("."):
        if (str(element) == str("dek_workshop")) and os.path.isdir(element):
            presence_raw_data = True
            break
    if presence_raw_data is False:
        print("Folder 'dek_workshop' is missing.  Exit.")
        sys.exit()


def create_csv():
    """Write relational table csv2anki.csv about keys and images."""
    file_register = []
    csv_register = []
    root = str(os.getcwd())
    os.chdir("dek_workshop")

    for file in os.listdir("."):
        if file.endswith(".svg"):
            file_register.append(file)
    file_register.sort(key=str.lower)

    for entry in file_register:
        file_name = str(entry)

        keyword = str(entry).split("_-_")[-1]
        keyword = str(keyword)[:-4]

        retain = str('{}; <img src="{}">'.format(keyword, file_name))
        csv_register.append(retain)

    try:
        with open("dek2anki.csv", mode="w") as newfile:
            today = date.today()
            header = str("# file: dek2anki.csv\n")
            header += str("# date: {} (YYYY-MM-DD)\n".format(today))
            header += str("# data: {}\n#\n".format(len(csv_register)))
            newfile.write(header)

            for record in csv_register:
                keep = str("{}\n".format(record))
                newfile.write(keep)
    except IOError:
        print("Error writing file 'dek2anki.csv'.  Exit.")
        sys.exit()

    try:
        table_old_place = os.path.join(str(os.getcwd()), str("dek2anki.csv"))
        table_new_place = os.path.join(root, str("dek2anki.csv"))
        shutil.copy(table_old_place, table_new_place)
    except IOError:
        print("Error copying file 'dek2anki.csv' from 'dek_workshop'.")
        sys.exit()

    print("File 'dek2anki.csv' was written.")


# clarifications for argparse, start:
parser = argparse.ArgumentParser(
    description='Write an initial dek2Anki.csv for Wikimedia .svg about DEK (no tags)')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i',
                   '--initial',
                   action='store_true',
                   help='on all, including initial fetch of the .svg data')
group.add_argument('-u',
                   '--update',
                   action='store_true',
                   help='only on data contributing to an update of the .svg')

args = parser.parse_args()
# clarifications for argparse, end.

if __name__ == "__main__":
    check_python()
    if args.initial:
        print("work on the earlier / initial fetch of the .svg data")
        only_check_presence_workshop()
        create_csv()

    elif args.update:
        print("work only on data contributing to an update of the .svg")
        os.chdir("antechamber")
        only_check_presence_workshop()
        create_csv()
