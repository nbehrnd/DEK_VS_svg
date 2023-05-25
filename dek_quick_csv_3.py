#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    <2020-05-31 Thu>
# edit:    <2023-05-25 Thu>
#
"""Quick generation of a minimal relational .csv table for Anki.

The programmatic generation of an Anki deck requires a text file to
relate the file names of the DEK .svg to consider with a keyword.  By
this script, this minimal information is stored in a permanent record.

From the CLI of Python 3, launch the script by

python deck_quick_csv.py

The newly written file 'csv2anki.csv' retains for each file a 'key'
and a 'file name', separated by a semicolon in the pattern of

A-Saite; <img src="DEK_VS_steno_svg_-_A-Saite.svg">

Anki permits only UTF-8 encoded relational tables and some file names
contain special characters (e.g., umlauts).  Thus, the script's action
is constrained to Python 3.

Note, file 'csv2anki.csv' actually is used as mandatory parameter by
script dek_csv4.py to extend the file indexing to be accessed again."""

import argparse
import os
import sys

from datetime import date


def get_args():
    """read the arguments by the CLI"""
    parser = argparse.ArgumentParser(
        description="Write an initial dek2Anki.csv about Wikimedia DEK .svg")

    return parser.parse_args()


def tally_files():
    """identify the files the preliminary Anki deck could cover"""
    register = []

    for file in os.listdir("."):
        if file.endswith(".svg"):
            register.append(file)

    register.sort(key=str.lower)
    return register


def create_csv(file_register):
    """Write relational table csv2anki.csv about keys and images."""
    csv_register = []

    for entry in file_register:
        file_name = str(entry)

        keyword = str(entry).rsplit('+', maxsplit=1)[-1]
        keyword = str(keyword)[:-4]

        retain = str(f'{keyword}; <img src="{file_name}">')
        csv_register.append(retain)

    try:
        with open("dek2anki.csv", mode="w", encoding="utf-8") as newfile:
            header = ""
            header = str("# file: dek2anki.csv\n")
            header += str(f"# date: {date.today()} (YYYY-MM-DD)\n")
            header += str(f"# data: {len(csv_register)}\n#\n")
            newfile.write(header)

            for record in csv_register:
                keep = str(f"{record}\n")
                newfile.write(keep)
            print("File 'dek2anki.csv' was written.")
    except IOError:
        print("Error writing file 'dek2anki.csv'.  Exit.")
        sys.exit()


def main():
    """join the functionalites"""
    get_args()
    register = tally_files()
    create_csv(register)


if __name__ == "__main__":
    main()
