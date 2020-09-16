#!/usr/bin/python3
# -*- coding: utf-8 -*-

# name:    dek_delta
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-15 (YYYY-MM-DD)
# edit:    2020-05-16 (YYYY-MM-DD)
#
"""Ease to trace changes between updates for .svg about DEK.

    This script stands after collecting .svg intended for an update
    of an already existing data, and before further processing of the
    illustrations by renaming, svg path optimization, and any form
    of writing a relational .csv table.

    Place the script one level above folders raw_data (about previous
    harvests) and antechamber (the current harvest to update the Anki
    deck).  The script is called from the CLI by Python 3 by

    python dek_delta.py [-n | -m | -r | -R]

    to narrow subsequent work on .svg either identified as new (toggle
    -n), or as modified (toggle -m) when comparing the raw_data of
    previous harvests with the ones currently deposit in the dedicated
    folder antechamber.

    -n  identifies files which appear for the first time in folder
        antechamber, but not in folder raw_data.  Criterion is the
        file name.  They will be moved into a new sub-folder, new_svg.
        Perform this as first action.

    -m  identifies in folder antechamber files which differ from the
        files in raw_data.  Because files in antechamber are fetched
        more recently, than files in raw_data, the difference is read
        as the file being modified.  Criterion to establish the file's
        difference is the string of md5sum and file name.  Modified
        files will be moved into a new folder, modified_svg.  Perform
        this as second action.

    -r  By now the number of remaining .svg in folder antechamber may
        be less than the number of .svg in folder raw_data.  This is
        plausible if .svg fetched earlier are now retracted entirely.
        For example, there were empty symbolizations containing only
        the line system used in DEK, and the stamps "LEER" (German for
        "empty") the author of the symbolizations no longer considered
        useful.  By toggle -r, obsolete .svg are identified and copied
        for visual inspection from folder raw_data into antechamber's
        sub-folder retract_svg.  In addition, file svg_to_retract.txt
        is written as permanent record into the root of the project,
        i.e., at the level of folders raw_data and antechamber.  This
        file is accessed again by option -R.

    -R  The scripts, documentation, as well as the .svg (both in raw,
        as well as in simplified form) of this script are managed with
        git.  For all files listed in file svg_to_retract.txt (written
        by -r), the subsequent call for parameter -R will issue the
        deletion of this file from this monitoring in a pattern of

        git rm example.svg

        for folder's raw_data files in question.  As a safety guard,
        this rinse has to be completed manually by an explicit commit
        of this change and the manual remove of the folder retract_svg
        in antechamber.

    The use of the parameters -n, -m, -r, and -R is mutually exclusive.

    Upon approval, the remaining raw data are then copy-pasted into
    folder raw_data.  Copies of these new raw data are to be renamed,
    svg optimized, and tagged "as usual"; this allows both a creation
    of a "delta-Anki deck" restricted to .svg in any way different to
    those previously considered, or to merge them fully with the .svg
    retained from a previous harvest.  Note for this, the other Python
    and bash scripts expect the location of the new data directly in
    folder antechamber, however do not reach out for neither new_svg,
    nor modified_svg."""

import argparse
import hashlib
import os
import subprocess
import shutil
import sys


def check_python():
    """Assure the script is used with Python 3, only."""
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def identify_new_svg():
    """Identify the new files present in the update branch."""
    svg_previous_sessions = []
    svg_updating_session = []
    svg_new = []
    root = os.getcwd()

    # learn about the already existing data:
    os.chdir("raw_data")
    for file in os.listdir("."):
        if file.endswith(".svg"):
            svg_previous_sessions.append(file)
    os.chdir(root)

    # learn about the data containing the update:
    os.chdir("antechamber")
    for file in os.listdir("."):
        if file.endswith(".svg"):
            svg_updating_session.append(file)

    # discern of the files:
    set_svg_previous_sessions = set(svg_previous_sessions)
    set_svg_updating_session = set(svg_updating_session)
    set_svg_new = set_svg_updating_session - set_svg_previous_sessions

    # act accordingly:
    try:
        os.mkdir("new_svg")
    except IOError:
        print("Creation of folder 'new_svg' failed.  Exit.")
        sys.exit()

    for new in set_svg_new:
        svg_new.append(new)
        old_path = os.path.join(os.getcwd(), str(new))
        new_path = os.path.join(os.getcwd(), str("new_svg"), str(new))
        shutil.move(old_path, new_path)

    print("By name, there are {} new .svg files.".format(len(svg_new)))
    os.chdir(root)


def identify_modified_svg():
    """Identify .svg changed in antechamber vz. already curated .svg."""
    svg_previous_sessions = []
    register_modified = []
    root = os.getcwd()

    # learn about the already existing data:
    os.chdir("raw_data")
    for file in os.listdir("."):
        if file.endswith(".svg"):

            # compute a checksum:
            with open(file, mode="rb") as reference:
                data = reference.read()
                md5sum_reference = hashlib.md5(data).hexdigest()
                retain = str("{} {}".format(str(md5sum_reference), str(file)))
            svg_previous_sessions.append(retain)
    os.chdir(root)

    # learn about the data containing the update:
    os.chdir("antechamber")
    try:
        os.mkdir("modified_svg")
    except IOError:
        print("Creation of folder 'modified' failed.  Exit.")
        sys.exit()

    for file in os.listdir("."):
        if file.endswith(".svg"):

            # compute a checksum:
            with open(file, mode="rb") as to_test:
                data = to_test.read()
                md5sum_reference = hashlib.md5(data).hexdigest()
                retain = str("{} {}".format(str(md5sum_reference), str(file)))

            # now compare with the already known:
            if str(retain) not in svg_previous_sessions:
                register_modified.append(file)

                old_path = os.path.join(os.getcwd(), file)
                new_path = os.path.join(os.getcwd(), str("modified_svg"), file)
                shutil.move(old_path, new_path)

    if len(register_modified) == 0:
        print("There are no modified .svg data.")
        shutil.rmtree("modified_svg")
    else:
        print("There is / are {} altered .svg moved to folder 'modified'.".
              format(len(register_modified)))
    os.chdir(root)


def retracted_svg():
    """The .svg only present in raw_data are those deemed 'retracted'."""
    register_antechamber = []
    register_retract = []
    root = os.getcwd()

    # learn about the data containing the update:
    os.chdir("antechamber")

    try:
        os.mkdir("retract_svg")
    except IOError:
        print("Creation of folder 'retract_svg' failed.  Exit.")
        sys.exit()

    for file in os.listdir("."):
        if file.endswith(".svg"):
            register_antechamber.append(file)
    os.chdir(root)

    # learn about the already existing data:
    os.chdir("raw_data")
    for file in os.listdir("."):
        if file.endswith(".svg") and (str(file) not in register_antechamber):
            register_retract.append(file)

            old_path = os.path.join(os.getcwd(), file)
            new_path = os.path.join(root, str("antechamber"),
                                    str("retract_svg"), str(file))
            try:
                shutil.copy(old_path, new_path)
            except IOError:
                print("Copy of file '{}' into folder 'retracted_svg' failed.".
                      format(file))
                continue

    register_retract.sort()
    os.chdir(root)

    # report the results:
    if len(register_retract) == 0:
        os.chdir("antechamber")
        shutil.rmtree("retracted_svg")
        print("There are no .svg files to remove from folder 'raw_data'.")
    else:
        print(
            "There is / are {} .svg to remove from folder 'raw_data'.".format(
                len(register_retract)))
        print("A copy of them is stored in folder 'retacted_svg'.")

        try:
            with open("svg_to_retract.txt", mode="w") as newfile:
                for entry in register_retract:
                    newfile.write("{}\n".format(entry))
            print("File 'svg_to_retract.txt' lists them, too.")
        except IOError:
            print("Error writing 'svg_to_retract.txt' listing.  Exit.")
            sys.exit()


def rinse_raw_data():
    """Run git rm example.svg for .svg identified as retracted."""
    register = []

    # identify the files in question:
    try:
        with open("svg_to_retract.txt", mode="r") as source:
            for line in source:
                line = str(line).strip()
                register.append(line)
        register.sort()
    except IOError:
        print("File 'svg_to_retract.txt' is not accessible.  Exit.")
        sys.exit()

    # act accordingly:
    os.chdir("raw_data")
    print("The following instructions will be sent to git")
    for entry in register:
        command = str("git rm {}".format(entry))
        print("\n{}".format(command))
        try:
            subprocess.call(command, shell=True)
        except IOError:
            print("Error removing file '{}'".format(entry))
            continue

    print("\nComplete the rinsing of folder 'raw_data' by a commit.")
    print("Remove then folder 'retract_svg' in folder 'antechamber'.")


# clarifications for argparse, start:
parser = argparse.ArgumentParser(
    description='Identify changes in the DEK .svg data since the last update')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    '-n',
    '--new',
    action='store_true',
    help='to start, move apparently new .svg into a separate folder')
group.add_argument(
    '-m',
    '--modified',
    action='store_true',
    help='in second place, move modified.svg into a separate folder')
group.add_argument('-r',
                   '--retracted',
                   action='store_true',
                   help='third, copy .svg to retract into a separate folder')
group.add_argument(
    '-R',
    '--rinse',
    action='store_true',
    help='lastly, remove .svg identified as retracted from raw_data')

args = parser.parse_args()
# clarifications for argparse, end.

if __name__ == "__main__":
    check_python()
    if args.new:
        identify_new_svg()
    elif args.modified:
        identify_modified_svg()
    elif args.retracted:
        retracted_svg()
    elif args.rinse:
        rinse_raw_data()
