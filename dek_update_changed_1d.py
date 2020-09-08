#!/usr/bin/python3
# name:    dek_update_changed_1d.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-09-08 (YYYY-MM-DD)
# edit:
#
"""Indicate the modified (rewritten) DEK .svg for a visual inspection.

Wikimedia user Thirunavukkarasye-Raveendran, who is not author of this
project, constantly generates new .svg files about the first degree of
simplification within the DEK.  He equally welcomes suggestions to
improve .svg already in existence.

Prior to processing and inclusion of the revised .svg into the already
existing Anki deck, which will overwrite the earlier version of the
.svg file in question, this script shall assist their inspection.  To
identify a changed .svg file, the md5sum of all unprocessed .svg files
in folder raw_data are computed which then are compared with those of
the newly fetched data in folder antechamber.  For portability reasons
this script relies on Python's standard library hashlib*) and does not
use the (much faster) md5sum of GNU coreutils.

Expecting file names with non-ASCII characters (e.g., umlauts), launch
the script from the CLI of Python 3 one level above folders raw_data
and antechamber by

python dek_update_changed_1d.py

without provision of parameter.  In case of a mismatch of the checksum
the script will create a copy of the .svg of folder antechamber into a
newly created folder, modified_svg.

*) The implementation is based on
https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python
"""
import hashlib
import os
import shutil
import sys

raw_data = []
raw_data_checksums = []
antechamber_modified = []


def check_python():
    """Assure the script is used with Python 3, only."""
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def check_raw_data_folder():
    """Check the presence of folder raw_data."""
    for element in os.listdir("."):
        check = False
        if (str(element) == str("raw_data")) and os.path.isdir(element):
            check = True
            break

    if check is False:
        print("Folder 'raw_data' is missing.  Exit.")
        sys.exit()


def check_antechamber_folder():
    """Check the presence of folder antechamber."""
    for element in os.listdir("."):
        check = False
        if (str(element) == str("antechamber")) and os.path.isdir(element):
            check = True
            break

    if check is False:
        print("Folder 'antechamber' is missing.  Exit.")
        sys.exit()


def record_present_raw_files():
    """Identify the .svg in folder raw_data and their checksum."""
    root = os.getcwd()
    os.chdir("raw_data")

    for file in os.listdir("."):
        if file.endswith(".svg"):
            raw_data.append(file)

            # Compute the checksum in raw_data."""
            try:
                with open(file, mode='rb') as file_to_check:
                    data = file_to_check.read()
                    md5sum_returned = hashlib.md5(data).hexdigest()
                    raw_data_checksums.append(md5sum_returned)
            except IOError:
                print("Problem computing md5sum for '{}'.".format(file))
                continue

    raw_data.sort()
    raw_data_checksums.sort()
    os.chdir(root)


def record_antechamber_files():
    """Identify the modified .svg in folder antechamber.

    Only files of same file name as in folder raw_data are considered
    for a computation of and subsequent comparison by checksums."""
    root = os.getcwd()
    os.chdir("antechamber")

    for file in raw_data:
        # Compute the checksum in antechamber.
        try:
            with open(file, mode='rb') as file_to_check:
                data = file_to_check.read()
                md5sum_returned = hashlib.md5(data).hexdigest()

                # Compare the checksums.
                if str(md5sum_returned) not in raw_data_checksums:
                    antechamber_modified.append(file)
        except IOError:
            print("Problem scrutinizing file '{}' in antechamber.  Continue.".
                  format(file))

    antechamber_modified.sort()
    os.chdir(root)


def copy_modified_files():
    """Copy the modified files into folder modified_svg."""
    try:
        os.mkdir("modified_svg")
    except IOError:
        print("Error creating a separate folder 'modified_svg'.  Exit.")
        sys.exit()

    for entry in antechamber_modified:
        source = os.path.join(str(os.getcwd()), str("antechamber"), str(entry))
        deposit = os.path.join(str(os.getcwd()), str("modified_svg"),
                               str(entry))
        try:
            shutil.copy(source, deposit)
        except IOError:
            print("Problem to copy file {}.  Script continues to work.".format(
                entry))
            continue


def main():
    """Join the functions."""
    check_python()
    check_raw_data_folder()
    check_antechamber_folder()
    record_present_raw_files()
    record_antechamber_files()
    copy_modified_files()


if __name__ == "__main__":
    main()
