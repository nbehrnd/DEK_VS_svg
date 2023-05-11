#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    dek_rename.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-31 (YYYY-MM-DD)
# edit:    [2023-05-11 Thu]
#
"""Rename the .svg for an Anki deck.

This is the second script in the sequence to work with the .svg files
about the DEK.  At present, both the file names include the verbose
and uniform string of

```
_Deutsche_Einheitskurzschrift_-_Verkehrsschrift_-_
```

For the creation of the Anki deck, the short `DEK` about the topic,
and -- where assigned -- tag like `G_` (as in `G_DEK_Aachen.svg`)
about symbolizations relevant to geography suffice.  The intended
assignment of new file names is a question of regular expressions
equally provided by a module of the Python standard library."""

import argparse
import os
import re
import shutil
import sys


def check_python():
    """assure the script is used with Python 3 only.

    This is not only because of the transition of Python2 to Python3,
    but at least equally because of the (better) support for utf-8
    and hence umlauts, and other special characters."""
    if sys.version_info[0] != 3:
        print("\nThe script is set up to work with Python 3, only.\n")
        exit()


def create_new_name(input_string):
    """define a new file name"""
    to_replace = str("_Deutsche_Einheitskurzschrift_-_Verkehrsschrift_-_")
    substitute = "+"
    new_name = re.sub(to_replace, substitute, input_string)

    return new_name


def main():
    """join the actions"""
    check_python()

    for file in os.listdir("."):
        if str(file).endswith(".svg"):
            try:
                print(f"Work on: {file}")
                shutil.move(file, create_new_name(file))
            except OSError:
                print(f"Error while working on {file}.")


# clarifications for argparse, start:
parser = argparse.ArgumentParser(
    description="Shorten the .svg file names about DEK symbolizations")

args = parser.parse_args()
# clarifications for argparse, end.

if __name__ == "__main__":
    main()
