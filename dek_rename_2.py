# name:    dek_rename.py
# author:  nbehrnd@yahoo.com
# date:    2020-05-31 (YYYY-MM-DD)
# edit:
#
#
""" Rename the .svg for an Anki deck.

There already is an Anki deck about steno / DEK using .png.  At present,
its coverage is quite different and with little overlap to the one when
accessing Wikimedia's category of DEK from scratch.  There is no reason
to create a deck which would overwrite the former.  Thus, .svg will be
renamed differently in a pattern of

DEK_VS_steno_svg_-_name.svg

where "DEK_vs_steno" reflects the content briefly (and separates this
deck from decks related to DEK's work) about the system (Deutsche
Einheitskurzschrift, Verkehrsschrift / first level of simplification),
and what seems to be short enough (steno) to ring a bell even for non-
specialists about the deck's purpose.  Even if not this popular like
"Gregg" or "shorthand", a colloquial "steno" equally may be understood
in other languages of the Latin script, too.

The presence of umlauts requires the script called by

python dek_rename.py

to use Python 3.  It will create a folder 'dek_workshop' with otherwise
copies of Wikimedia's .svg deposit in sub-folder 'raw_data'. """

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


def check_workshop_folder():
    """ Work on the files should take place in a dedicated folder. """
    create = True
    for element in os.listdir("."):
        if (str(element) == str("dek_workshop")) and os.path.isdir(element):
            create = False

    if create:
        try:
            os.mkdir("dek_workshop")
        except IOError:
            print("Creation of folder 'dek_workshop' failed.  Exit.")
            sys.exit()


def populate_workshop():
    """ Populate 'dek_workshop' with copies of the .svg from 'raw_data'. """
    root = os.getcwd()
    deposit = os.path.join(root, 'dek_workshop')
    os.chdir("raw_data")

    # identify the relevant files:
    register = []
    for file in os.listdir("."):
        if file.endswith(".svg"):
            register.append(file)
    register.sort()

    # build new names for the files eventually copied to dek_workshop:
    print("\nWork on:")
    for entry in register:
        try:
            # remove old prefix:
            content = str(entry).split("_-_")[-1]
            # specialty for a small group of entries
            if str("Verkehrsschrift_") in str(content):
                content = str(content)[17:]

            # define a new prefix:
            prefix = str("DEK_VS_steno_svg_-_")

            # build the new file name:
            new_filename = ''.join([prefix, content])

            # file operations:
            print(new_filename)
            shutil.copy(entry, os.path.join(deposit, new_filename))

        except OSError:
            print("PROBLEM: {}".format(new_filename))


def main():
    """ Join the functions. """
    check_python()
    only_check_presence_raw_data()
    check_workshop_folder()
    populate_workshop()


main()
# END
