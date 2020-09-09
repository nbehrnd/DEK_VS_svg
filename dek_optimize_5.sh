#!/bin/bash

# name:    dek_optimize_5.sh
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-31 (YYYY-MM-DD)
# edit:    2020-09-09 (YYYY-MM-DD)
#
#
# The DEK .svg fetched from Wikimedia contain much more information,
# than building an Anki deck requires.  Removing e.g. commentary lines
# and simplifying the paths to draw the illustrations thus reduces the
# individual file size, and globally the Anki deck (20k+ entries).
#
# This bash script moderates the Linux executable of svgcleaner,[1]
# included as a copy in this project, too.  Deposit both this bash
# script dek_optimize_5.sh and svgcleaner as copies in the folder one
# level above folder "raw_data" (present since working for the first
# time with the .svg) and "antechamber" (visible while preparing an
# update of the Anki deck).  Add the executable bit and run the script
# from the CLI by
#
# ./dek_optimize_5.sh
#
# Depending on the explicit choice (initial work / updating work), the
# location where the script simplifies the .svg is adjusted.  Often,
# the apparent size is about 20...25% of the originally submitted .svg.
#
# At any time, a "Ctrl + C" command will stop the script's action.
#
# [1] https://github.com/RazrFalcon/svgcleaner, v0.9.5 / Apr 10, 2018."""

# Explicitly choose between initial work, or update.
#
# The case-wise design is inspired by an answer at
# https://stackoverflow.com/questions/5542016/bash-user-input-if
read -n1 -p "Choose between [1] initial work, [2] update, or [q]uit. " doit
case $doit in
    1) choice=10 ;;
    2) choice=20 ;;
    q) choice=0 ;;
esac


# Feedback to the user:
if [ $choice = 10 ]
then
    printf "\n[1]    Processing of initial data copied from 'raw_data'.\n";
elif [ $choice = 20 ]
then
    printf "\n[2]    Processing of update data copied from 'antechamber'.\n";
elif [ $choice = 0 ]
then
    printf "\n[q]    Closing of the script.\n";
fi

# Simplification of the .svg:
if [ $choice = 10 ]
then
    cp ./svgcleaner ./raw_data/dek_workshop;
    cd ./raw_data/dek_workshop;
    chmod u+x ./svgcleaner;
elif [ $choice = 20 ]
then
    cp ./svgcleaner ./antechamber/dek_workshop;
    cd ./antechamber/dek_workshop;
    chmod u+x ./svgcleaner;
fi

for num in {1..5}
do
    
    for file in *.svg; do
        echo ""
        echo "cycle $num of 5, processing $input_file"  # CLI reporter

        input_file=$file
        extent_intermediate='_inter.svg'
        intermediate_file=$input_file$extent_intermediate

        ./svgcleaner $input_file $intermediate_file --indent 1 --remove-comments --remove-unused-defs --convert-shapes --remove-metadata --remove-nonsvg-attributes --remove-unreferenced-ids --remove-text-attributes --trim-colors --simplify-transforms --paths-coordinates-precision 1
        mv $intermediate_file $input_file
    done

done

# Finalize the work:
rm svgcleaner  # space cleaning

echo ""
echo "Number of .svg files in folder 'dek_workshop':"
ls *.svg | wc -l
echo "Number of all files in folder 'dek_workshop':"
ls *.* | wc -l
echo "Apparent file size of all files in folder 'dek_workshop':"
du -h --apparent-size
