# name:    dek_rename.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-31 (YYYY-MM-DD)
# edit:    2020-09-08 (YYYY-MM-DD)
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

The presence of umlauts requires the script called by

python dek_rename.py

to use Python 3 one level above folder "raw_data" (initial work) and
possibly "antechamber".  During an initial work with the data, a blank
folder 'dek_workshop' will be created, retaining the original .svg as
fetched from Wikimedia.  If the work targets an update of already .svg
files, this script's action is to be redirected accordingly to
'antechamber', which depends on the user's explicit input."""

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


def populate_workshop():
    """Populate 'dek_workshop' with copies of the .svg from 'raw_data'."""
    root = os.getcwd()
    deposit = os.path.join(root, 'dek_workshop')
    os.chdir("raw_data")

    register = []
    for file in os.listdir("."):
        if file.endswith(".svg"):
            register.append(file)
    register.sort()

    for entry in register:
        original = os.path.join(str(os.getcwd()), str(entry))
        copy = os.path.join(str(deposit), str(entry))
        try:
            shutil.copy(original, copy)
        except IOError:
            print("Problem copying file '{}'.".format(entry))
            continue

    os.chdir(root)


def file_renamer():
    """Shorten the file names used for the copied .svg."""
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
            #            shutil.copy(entry, os.path.join(deposit, new_filename))
            shutil.copy(entry, new_filename)

        except OSError:
            print("PROBLEM: {}".format(new_filename))


def initial_or_update():
    """Choose between initial or updating work."""
    print("\nChoose if the current work is about")
    print("[1]    creating the Anki deck for the first time,")
    print("[2]    eventually updates an already existing set, or")
    print("[q]    Exit the script whatsoever.")
    choice = input("\nyour choice: ")

    if str(choice) == str(1):
        try:
            check_workshop_folder()
            only_check_presence_raw_data()
            populate_workshop()
            os.chdir(os.path.join(str(os.getcwd()), str("workshop")))
            file_renamer()
        except IOError:
            print("Folder 'workshop' for 'raw_data' inaccessible.  Exit.")
            sys.exit()

    elif str(choice) == str(2):
        try:
            os.chdir("antechamber")
            check_workshop_folder()
            populate_workshop()
            os.chdir(os.path.join(str(os.getcwd()), str("workshop")))
            file_renamer()
        except IOError:
            print("Folder 'workshop' for 'antechamber' inaccessible.  Exit.")
            sys.exit()

    elif (str(choice).lower() == str("q")) or (str(choice) not in ["1", "2"]):
        print("\nThe script stops here.  Exit.")
        sys.exit()


def main():
    """ Join the functions. """
    check_python()
    initial_or_update()


#    check_workshop_folder()
#    populate_workshop()

if __name__ == "__main__":
    main()
