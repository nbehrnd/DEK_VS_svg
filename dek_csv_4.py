#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name:    dek_csv_4.py
# author:  nbehrnd@yahoo.com
# license: GPLv2
# date:    2020-05-31 (YYYY-MM-DD)
# edit:    <2023-06-12 Mon>
#
""" Consolidation of dek_quick_csv.py's dek2anki.csv relational table.

The content of file dek2anki.csv, written by script dek_quick_csv.py,
is extended by this script with tags in a third column.  Eventually,
the lines in this relational table follow a pattern of

Aufstand; <img src="DEK_VS_steno_svg_-_Aufstand.svg">; DEK

to relate a key (here, "Auftstand"), with the address of the .svg file
(second column), and tags about this entry (third column).  Here, the
string `DEK` provides a label specific to the Anki deck.  Future versions
of the Anki deck are going to permit labels like e.g., `DEK_A` about
abbreviations, or `DEK_G` about geography (cities, counties, rivers, etc).

Previously, the script attempted to identify the use of Kuerzel (`der`,
`die`, `das`) and symbolizations of consonant groups (`mp` vs `mpf`) for
additional tags written into the third column of the .csv to build an Anki
deck.  Though the function to provide (some) of these tags aiming a focussed
review still is retained in this script, the script does not use it."""

import argparse
import os
import shutil
import sys

# from hyphen import Hyphenator  # this is outside of Python's standard library
# h_de = Hyphenator('de_DE')


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='second level consolidation of the .csv',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='the preliminary e.g. dek2anki.csv to work on',
                        type=argparse.FileType('rt'),
                        default=None)

    return parser.parse_args()


def read_current_listing(data):
    """read the .csv file to process"""
    old_list = []
    old_list = data.read().splitlines()

    header = old_list[:4]
    list_proper = old_list[4:]

    return header, list_proper


def whitelist_categories(old_list):
    """retain entries by category deemed suitable for the Anki deck

    Meanwhile, the DEK tables were categorized.  Some of these sets however
    are considered not useful for the deck to build; for example `T` (longer
    texts).  I would like to gradually open  the deck by white listing the
    sub sets."""
    tags_white_list = [
        "DEK", "A_DEK", "B_DEK", "C_DEK", "E_DEK", "F_DEK", "G_DEK", "K_DEK",
        "N_DEK", "O_DEK", "P_DEK", "L_DEK", "U_DEK", "V_DEK", "Z_DEK"
    ]
    new_list = []

    for entry in old_list:
        image_source = entry.split("img src=")[1]
        image_source = image_source[1:-2]
        tag = image_source.split("+")[0]

        if tag in tags_white_list:
            new_list.append(entry)

    return new_list


def dimension_filter(old_listing):
    """remove plates too large in dimension

    Most of the plates share the same dimensions, however not all.  Anki would
    compensate for this by variation of the scale of display, at expense of
    detail visible while working with the deck to build.  The .svg fetched from
    wikimedia are henced checked if they contain both a string `width="297mm"`
    and `height="210mm"`; else, they are not considered for now.

    Because this can remove too many plates (which perhaps can be adjusted), a
    report of plates passing the test, as well as plates not passing the test
    is installed."""
    list_pass, list_skip, list_inaccessible = [], [], []

    to_check = str("svg_skipped")
    try:
        os.mkdir(to_check)
    except IOError:
        if os.path.isdir(to_check):
            print(f"\nNote, folder `{to_check}` already exists.")
            print(
                "To prevent unwarranted overwrite, the script's action stops.")
            sys.exit()
        else:
            print(f"error to create {to_check}")

    for entry in old_listing:
        image_source = entry.split("img src=")[1]
        image_source = image_source[1:-2]
        content = []

        try:
            with open(image_source, mode="rt", encoding="utf-8") as source:
                for line in source:
                    content.append(str(line).strip())

            if (str('width="297mm"') in content) and (str('height="210mm"')
                                                      in content):
                list_pass.append(entry)
            else:
                list_skip.append(entry)
                shutil.move(image_source, to_check)

        except IOError:
            list_inaccessible.append(entry)

    # check if an intermediate folder can be removed:
    if len(list_skip) == 0:
        os.rmdir("svg_skipped")

    return list_pass, list_skip, list_inaccessible


def tag_entries(old_list):
    """provide the entries the set dependent tag"""
    new_list = []

    for entry in old_list:
        image_source = entry.split("img src=")[1]
        image_source = image_source[1:-2]
        tag = image_source.split("+")[0]

        entry = "; ".join([entry, tag])
        new_list.append(entry)

    print(f"\n{len(new_list)} entries retained in `revised_anki4dek.csv`.")
    try:
        with open(file="revised_anki4dek.csv", mode="wt",
                  encoding="utf-8") as new:
            for entry in new_list:
                new.write(f"{entry}\n")
    except IOError:
        print("Error while writing the new .csv file")


def analysator():
    """ Provide meaningful tags for column #3 in file 'csv2anki.csv'. """
    global tag_line
    tag_line = str("DEK_b")

    # rule contrasting illustrations:
    if str("ABER") in check:
        tag_line += str(" Vergleich")

    # Identification of 17 non-ambigous symbolizations -- a concept.
    #
    # It is plausible that these lists are incomplete.
    # It is complemented by later rules discerning e.g., 'st' from 'str'.
    test = str(check).lower()
    grouped_consonants = [
        'br', 'cr', 'fr', 'gr', 'kr', 'mpf', 'ndr', 'pfr', 'rdr', 'schl',
        'schm', 'schn', 'schr', 'spr', 'str', 'wr', 'zw'
    ]

    # Incomplete list of 59, apparently easier to retrieve, kuerzel.
    # Again, there are some for this simple string-based approach is
    # not working well enough (e.g., 'wo' vs. 'woll' or 'worden'; or
    # 'in' vs. 'meine', 'deine'. 'hint', 'keine', 'seine' or 'sind';
    # or 'un' vs. 'unter'; or reserved symbolizations like 'dem' which
    # is not used in 'demokratisch') thus not yet considered here.
    kuerzel = [
        'also', 'ander', 'ant', 'auf', 'aus', 'besonder', 'bis', 'dar',
        'deine', 'dessen', 'deutsch', 'dies', 'doch', 'durch', 'fort', 'für',
        'gegen', 'heit', 'hint', 'ion', 'keine', 'konnt', 'lich', 'lung',
        'meine', 'mit', 'nichts', 'noch', 'nur', 'ohne', 'rung', 'schaft',
        'schon', 'seine', 'selbst', 'sich', 'sind', 'solch', 'soll', 'sonder',
        'über', 'unter', 'vielleicht', 'voll', 'vom', 'von', 'völl', 'wenn',
        'will', 'wird', 'woll', 'worden', 'wurd', 'zer', 'zum', 'zurück',
        'zurück', 'zusammen', 'zwischen'
    ]
    check_list = grouped_consonants + kuerzel

    for element in check_list:
        if element in test:  # check:
            tag_line += str(" {}".format(element))

    # specialty rules, complementing the simpler ones above:
    #
    # "ge" at the beginning of the word, but not as "gegen"
    #
    # Pro:  Identifies, e.g. "Gebiet", excludes entries like "Gegend",
    #       or "gegenüber", and conjunctions to "ei" ("Geige").
    #
    # Con:  Detection of plausible matches like "Angebot", "angeboren"
    #       is missed.  Neither pure string comparison, or a syllable
    #       based approach so far prevent collisions with false-positives
    #       like "Türangel", or "Enge"; beside an open identification
    #       of "ng" != ["lung", "rung"].
    #
    if (test.startswith("ge")) and (test.startswith("gegen") is
                                    False) and (str(test[2]) is not str("i")):
        tag_line += str(" ge")

    # identification of "sch" as different from groups "schl", "schm",
    # "schn", "schr", and separate from kuerzel "schaft" and "deutsch"
    #
    if str("sch") in test:
        start = test.find("sch")
        try:
            if (str(test)[start + 3] in ["l", "m", "n", "r"]) or \
            (str(test)[start : start + 6] == str("schaft")) or \
            (str(test)[start - 4 : start + 3] == str("deutsch")):
                pass
            else:
                tag_line += str(" sch")
        except:
            pass

    # identification and discern of "st" from "str"
    #
    if str("st") in test:
        syllables = h_de.syllables(test)
        match = False
        for syllable in syllables:
            if (syllable.startswith("st")) and \
                (syllable.startswith("str") is False):
                match = True
                break
        if match:
            tag_line += str(" st")

    # identification and discern of "tr" from "str"
    #
    if str("tr") in test:
        start = test.find("tr")
        try:
            if str(test)[start - 1] is not str("s"):
                tag_line += str(" tr")
        except:
            pass

    # identification of "un" besider "unter" as start of a word
    #
    if (test.startswith("un")) and (test.startswith("unter") is False):
        tag_line += str(" un")


def main():
    """Join the functionalities"""
    args = get_args()

    header, old_list = read_current_listing(args.file)
    print(f"entries in old list:       {len(old_list)}")

    tag_filtered = whitelist_categories(old_list)
    print(f"permitted by tag:          {len(tag_filtered)}")

    list_pass, list_skip, list_inaccessible = dimension_filter(tag_filtered)
    print("----")
    print("check plates by their dimension:")
    print(f"plate passes test:         {len(list_pass):>5}")
    print(f"plate in different size:   {len(list_skip):>5}")
    print(f"information inaccessible:  {len(list_inaccessible):>5}")

    if list_skip:
        print("\nconsult folder `svg_skipped`")

    tag_entries(list_pass)


# --------------------------------------------------
if __name__ == '__main__':
    main()
