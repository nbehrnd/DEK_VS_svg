#!/usr/bin/python3
# name:    dek_fetch.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-06-02 (YYYY-MM-DD)
# edit:    2020-09-08 (YYYY-MM-DD)
#
"""Collect the original .svg about DEK from Wikimedia.

There are 21k+ of .svg files on Wikimedia sharing the tag

SVG Deutsche Einheitskurzschrift

created by Wikimedia user Thirunavukkarasye-Raveendran, who is not the
author of this project, and published as public domain.  The addresses
of these .svg files may be obtained with these tags as a zipped .txt
file from

https://tools.wmflabs.org/wikilovesdownloads/

After decompressing, this text file is used as sole parameter for the
current script, dek_fetch_1.py, to collect the .svg with wget while
preserving the time stamp of their upload to Wikimedia when running

python dek_fetch_1.py [addresslist.txt]

Lines preceded by the octohorpe # will be treated as comment to skip,
these may contain e.g. a time stamp.

The addresses in [addresslist.txt] frequently encode characters like
umlauts and accents which are not part of the ASCII table.  This is
one of the reasons why this script's use is restricted to Python 3.

Initially, the script was written to obtain local copies of the .svg
stored in folder 'raw_data'; this prepared further processing of these
with the other scripts of this project eventually yielding the Anki
deck.  To ease updating the Anki deck, the script now allows to direct
the .svg listed in [addresslist.txt] into folder 'antechamber' instead
of default folder 'raw_data' to focus the inspection and curation on
either new, or revised .svg."""

import os
import shutil
import subprocess as sub
import sys
from urllib.parse import unquote

root = os.getcwd()
intermediate_register = []
address_register = []

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


def check_antechamber_folder():
    """Check the presence of folder antechamber; if absent, create it."""
    for element in os.listdir("."):
        create = True
        if (str(element) == str("antechamber")) and os.path.isdir(element):
            create = False
            break

    if create:
        try:
            os.mkdir("antechamber")
        except IOError:
            print("Error to create folder 'antechamber'.  Exit.")
            sys.exit()


def read_input_list():
    """ Retrieve the .svg files listed on Wikimedia's list.

    Read-out of the files' addresses on Wikimedia's servers, relay the
    decoded string to wget to store local copies.  Report if a string
    conversion failed in log 'failed_string_conversion.txt'.  It is
    considered more efficient if Wikimedia's address list is edited to
    contain two leading comment lines (starting by #) stating the date
    of their creation rather than their individual storage within the
    git-managed project."""
    try:
        if len(sys.argv[1]) > 1:
            try:
                input_file = str(sys.argv[1])
            except:
                print("The file was not found.")
    except:
        print("\nThe expected input instruction is: \n")
        print("    python dek_fetch.py [addresslist.txt] \n")
        sys.exit()

    try:
        with open(input_file, mode="r") as source:
            for line in source:
                intermediate_register.append(str(line).strip())
    except IOError:
        print("Unable to read file '{}'.  Exit.".format(input_file))
        sys.exit()

    # Decode the addresses (back) into UTF-8.
    for line in intermediate_register:
        if line.startswith("#") is False:
            url = unquote(str(line).strip())
            address_register.append("{}\n".format(url))
        address_register.sort()

    try:
        with open("addresslist.txto", mode="w") as newfile:
            newfile.writelines(address_register)
    except IOError:
        print("Error writing intermediate 'addresslist.txto' file.")
        sys.exit()


def processing_for_windows():
    """Fetch the .svg sequentially with wget in linear fashion.

    The wget tool is available for Windows, too.  As a fallback, its
    use is restricted to the already known, previously used linear
    approach; fetching one file at a time.  The Linux analogue of this
    function, processing_for_linux, will strive for an approach with
    multiple simultaneous downloads."""
    with open("addresslist.txto", mode="r") as source:
        for entry in source:
            try:
                command = str("wget -t 21 {}".format(str(entry).strip()))
                sub.call(command, shell=True)
            except IOError:
                print("\nCheck if wget was installed in your system.")
                print("See, for example, https://en.wikipedia.org/wiki/Wget")
                print("The script stops here.  Exit.")
                sys.exit()

    os.remove("addresslist.txto")


def processing_for_linux():
    """Fetch the .svg with multiple simultaneous instances of wget.

    With xargs, Linux offers to use multiple simultaneous instances of
    wget which may reduce the time to harvest the data substantially.
    To prevent a system freeze, a conservative approach is taken using
    either the one processor is, or one less than the total count of
    processors available are used."""

    use_processors = 0
    processors_available = int(len(os.sched_getaffinity(0)))
    if processors_available == 1:
        use_processors = 1
    if processors_available > 1:
        use_processors = processors_available - 1
    else:
        print("Error determining the number of processors available.  Exit.")
        sys.exit()

    # The instruction is based on
    # https://stackoverflow.com/questions/5546694/parallel-wget-download-url-list-and-rename
    #
    # with the model pattern: cat test.txt | xargs -P 4 wget -nv -t 21
    #
    # xargs -P 4: work with up to four simultaneous processes.
    # wget -nv -t 21: use wget's non-verbose report to the CLI (lists
    #    only date, time, address, file name of fetched file) and try
    #    up to 21 times to fetch the .svg currently in question.
    #
    # For efficiency, Linux' first attempt is to call wget2.  If this
    # fails, wget serves as fallback.

#    try:
#        command = str(
#            "cat addresslist.txto | xargs -0 -P {} wget2 -nv -t 21".format(use_processors))
#        sub.call(command, shell=True)
#    except IOError:
#        print("Problem using wget2; attempt using slower wget instead.")
#        try:
#            command = str(
#                "cat addresslist.txto | xargs -0 -P {} wget2 -nv -t 21".format(
#                    use_processors))
#            sub.call(command, shell=True)
#        except IOError:
#            print("Linux based xargs/wget fetch of the data failed.  Exit.")
#            sys.exit()
#
#    os.remove("addresslist.txto")

# known to work -- faster, start:
    try:
        command = str("cat addresslist.txto | parallel -j4 'wget2 {}'")
        sub.call(command, shell=True)
    except IOError:
        print("parallel/wget2 failed.  Exit")
    # known to work, end.
    
        # known to work, not as fast, start:
        try:
            command = str("cat addresslist.txto | parallel -j4 'wget {}'")
            sub.call(command, shell=True)
        except IOError:
            print("parallel/wget failed.  Exit")
        # exit method not as fast.

            # the linear method / slow:
            # known to work, start:
            with open("addresslist.txto", mode="r") as source:
                for entry in source:
                    try:
                        command = str("wget2 -t 21 {}".format(str(entry).strip()))
                        sub.call(command, shell=True)
                    except IOError:
                        print("\nCheck if wget was installed in your system.")
                        print("See, for example, https://en.wikipedia.org/wiki/Wget")
                        print("The script stops here.  Exit.")
                        sys.exit()
                    # known to work, end.

def define_svg_harvest():
    """Select Windows/Linux and type of .svg deposit.

    It is preferred to use the script in Linux, where fetching the
    data is eased by wget2 (fallback: wget) to retrieve the data, and
    xargs to parallelize this.  For Windows and MacOS (not tested),
    wget is available, too but its call is not parallelized here.

    Fetching the data discerns between either the initial harvest (->
    folder 'raw_data', generated on the fly) and an eventually update
    of the data (-> folder antechamber)."""

    print("\nSelect if fetching the data either is")
    print("[1]    the initial collection of the .svg, or")
    print("[2]    intends an update of the raw .svg.")
    print("[q]    Exit the script whatsoever.")
    choice = input("\nyour choice: ")

    if str(choice) == str(1):
        check_raw_data_folder()
        shutil.copy("addresslist.txto", "raw_data")
        os.chdir("raw_data")

        if str(sys.platform).lower().startswith("lin"):
            processing_for_linux()
        elif str(sys.platform).lower().startswith("win") or str(
                sys.platform).lower().startswith("darwin"):
            processing_for_windows()
        else:
            print("This operating system is currently not supported.")

    if str(choice) == str(2):
        check_antechamber_folder()
        shutil.copy("addresslist.txto", "antechamber")
        os.chdir("antechamber")

        if str(sys.platform).lower().startswith("lin"):
            processing_for_linux()
        elif str(sys.platform).lower().startswith("win") or str(
                sys.platform).lower().startswith("darwin"):
            processing_for_windows()
        else:
            pass

    if (str(choice).lower() == str("q")) or (str(choice) not in ["1", "2"]):
        print("\nThe script stops here.  Exit.\n")
        sys.exit()


def cleaning():
    """Remove the intermediate 'adresslist.txto' file."""
    os.chdir(root)

    try:
        os.remove('addresslist.txto')
    except IOError:
        pass


def main():
    """ Join the functions. """
    check_python()
    read_input_list()
    define_svg_harvest()

    cleaning()

if __name__ == "__main__":
    main()
