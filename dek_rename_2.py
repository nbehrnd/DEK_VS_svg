#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name:    dek_rename.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    <2020-05-31 Sun>
# edit:    <2023-05-25 Thu>
#
"""Rename the .svg for an Anki deck.

This is the second script in the sequence to work with the .svg files
about the DEK.  At present, both the file names include the verbose
and uniform string of

```
_Deutsche_Einheitskurzschrift_-_Verkehrsschrift_-_
```

which is going to be replaced by `+`.  Contrasting to underscore,
hyphen, colon, it is less likely one of the DEK examples is going
to use the plus sign as a separator (sub) string.

For the creation of the Anki deck, the short `DEK` about the topic,
and -- where assigned -- tag like `G_` (as in `G_DEK_Aachen.svg`)
about symbolizations relevant to geography suffice.  The intended
assignment of new file names is a question of regular expressions
equally provided by a module of the Python standard library."""

import argparse
import os
import re
import shutil


def get_args():
    """ read the command line arguments """
    parser = argparse.ArgumentParser(
        description="Shorten the .svg file names about DEK symbolizations")

    return parser.parse_args()


def create_new_name(input_string):
    """define a new file name"""
    to_replace = str("_Deutsche_Einheitskurzschrift_-_Verkehrsschrift_-_")
    substitute = "+"
    new_name = re.sub(to_replace, substitute, input_string)

    return new_name


def main():
    """join the actions"""
    get_args()

    for file in os.listdir("."):
        if str(file).endswith(".svg"):
            try:
                print(f"Work on: {file}")
                shutil.move(file, create_new_name(file))
            except OSError:
                print(f"Error while working on {file}.")


if __name__ == "__main__":
    main()
