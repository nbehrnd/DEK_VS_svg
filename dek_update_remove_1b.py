#!/usr/bin/python3
# name:    dek_update_remove_1b.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-09-08 (YYYY-MM-DD)
# edit:
#
"""Remove .svg no longer used from the project.

Among the 20k+ .svg about the DEK, the development of the DEK project
will drop some of them; for example because an earlier version was
empty (i.e., contained only the line system).  The criterion for this
action is the comparison of the file names of .svg provided by

https://tools.wmflabs.org/wikilovesdownloads/

for files with the tag of

SVG Deutsche Einheitskurzschrift

deposited in a new text file as reference, then compared with the .svg
in folders raw_data and dek_workshop.

Use:
+ Fetch the new file list from wikimedia.

+ Checkout the git branch svg_data, then deposit both this script,
  dek_update_remove_1b.py, as well as the new (Wikimedia generated)
  file list one level above the folders raw_data and dek_workshop.

+ Because file names contain non-ASCII characters, the launch of the
  script is constrained to the CLI of Python 3 by

  python dek_update_remove_1b.py [file_list.txt]

  with [file_list.txt] the newly Wikimedia generated file list.

This will create a new text file, file_remove.txt which will list all
files to be removed."""

import os
import shutil
import sys
from urllib.parse import unquote

address_register = []
raw_data = []
raw_data_to_remove = []


def check_python():
    """Assure the script is used with Python 3, only."""
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def check_deposit_folder():
    """Check the presence of folder raw_data; if absent, create it."""
    for element in os.listdir("."):
        create = True
        if (str(element) == str("raw_data")) and os.path.isdir(element):
            create = False
            break

    if create:
        try:
            os.mkdir("raw_data")
        except IOError:
            print("Error to create folder 'raw_data'.  Exit.")
            sys.exit()


def read_input_list():
    """Retrieve the .svg files listed on Wikimedia's list.

    Read-out of the files' addresses on Wikimedia's servers, relay the
    decoded string to wget to store local copies.  Report if a string
    conversion failed in log 'failed_string_conversion.txt'. """
    try:
        if len(sys.argv[1]) > 1:
            try:
                input_file = str(sys.argv[1])
            except:
                print("The file was not found.")
    except:
        print("\nThe expected input instruction is: \n")
        print(
            "    python dek_update_remove_1b.py YYYY-MM-DD_DEK_input_list.txt \n"
        )
        sys.exit()

    # work on decoding the addresses (back) into UTF-8:
    with open(input_file, mode="r") as source:
        for line in source:
            url = unquote(str(line).strip())
            reference = url.split("_-_")[-1]
            address_register.append(reference)
        address_register.sort()


def record_present_raw_files():
    """Retrieve the .svg still locally present as raw file."""
    root = os.getcwd()
    os.chdir("raw_data")

    for file in os.listdir("."):
        if file.endswith(".svg"):
            raw_data.append(file)

    set_raw_data = set(raw_data)
    set_address_register = set(address_register)

    set_raw_to_remove = set_address_register - set_raw_data
    for entry in set_raw_to_remove:
        raw_data_to_remove.append(entry)
    raw_data_to_remove.sort()

    with open("remove_raw_files.txt", mode="w") as newfile:
        for entry in raw_data_to_remove:
            newfile.write("{}\n".format(entry))

    shutil.move("remove_raw_files.txt",
                os.path.join(root, "remove_raw_files.txt"))
    os.chdir(root)


def record_dek_workshop_files():
    """Retrieve the (already simplified) .svg files."""
    root = os.getcwd()
    os.chdir("dek_workshop")

    dek_workshop = []
    dek_workshop_to_remove = []

    for file in os.listdir("."):
        if file.endswith(".svg"):
            dek_workshop.append(file)

    set_dek_workshop = set(dek_workshop)
    set_address_register = set(address_register)

    set_dek_workshop_to_remove = set_address_register - set_dek_workshop
    for entry in set_dek_workshop_to_remove:
        dek_workshop_to_remove.append(entry)
    dek_workshop_to_remove.sort()

    with open("remove_workshop_files.txt", mode="w") as newfile:
        for entry in dek_workshop_to_remove:
            newfile.write("{}\n".format(entry))
    os.chdir(root)


def difference_view():
    """Identify the files no longer needed."""
    # Check the difference with


def main():
    """ Join the functions. """
    check_python()
    check_deposit_folder()
    read_input_list()
    record_present_raw_files()
    record_dek_workshop_files()


if __name__ == "__main__":
    main()
