# name:    dek_quick_csv.py
# author:  nbehrnd@yahoo.com
# license:
# date:    2020-05-31 (YYYY-MM-DD)
# edit:
#
""" A quick generation of an Anki compatible relational .csv table.

This script creates a minimal form of the relational table between the
keys and the corresponding images Anki must read once to build its own
database.  Thus, by action of

python deck_quick_csv.py

with Python 3 (Anki allows only UTF-8 encoded relational tables, and
there are special characters like umlauts, too), file csv2anki.csv is
written.  The two columns are separated by semi-colon in a pattern of

A-Saite; <img src="DEK_VS_steno_svg_-_A-Saite.svg">

This file is processed further by dek_csv_4 because it is possible to
add tags to the entries allowing a more specific training in an Anki
session, too. """

import os
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


def only_check_presence_workshop():
    """ This time, only probe if there is folder dek_workshop. """
    presence_raw_data = False
    for element in os.listdir("."):
        if (str(element) == str("dek_workshop")) and os.path.isdir(element):
            presence_raw_data = True
            break
    if presence_raw_data is False:
        print("Folder 'dek_workshop' is missing.  Exit.")
        sys.exit()


def create_csv():
    """ Write relational table csv2anki.csv about keys and images. """
    file_register = []
    csv_register = []
    os.chdir("dek_workshop")

    for file in os.listdir("."):
        if file.endswith(".svg"):
            file_register.append(file)
    file_register.sort()

    for entry in file_register:
        file_name = str(entry)

        keyword = str(entry).split("_-_")[-1]
        keyword = str(keyword)[:-4]

        retain = str('{}; <img src="{}">'.format(keyword, file_name))
        csv_register.append(retain)

    with open("dek2anki.csv", mode="w") as newfile:
        for record in csv_register:
            keep = str("{}\n".format(record))
            newfile.write(keep)


def main():
    """ Joining the functions. """
    check_python()
    only_check_presence_workshop()
    create_csv()


main()
