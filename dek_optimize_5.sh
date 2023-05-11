#!/bin/bash

# name:    dek_optimize_5.sh
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-31 (YYYY-MM-DD)
# edit:    [2023-05-11 Thu]
#
#
# For the display of .svg in an Anki deck about DEK, the files carry
# more details of information, than necessary.  Because the slides
# in the Anki deck are not intended to be processed further, it is
# assumed safe to remove many of the (meta) data, to trim the levels
# of indentation, reduce the precision of coordinates of Bezier 
# curves and vector strokes.  For this, this bash script moderates
# the action of svgcleaner.[1]  In comparison to the initial .svg,
# the newly written files are typically are 25 to 20% of the original
# file size which is significant for a corpus of close to 40k files.
#
# Deposit both this bash script dek_optimize_5.sh and svgcleaner as
# copies in the folder containing the "raw_data".  After provision of
# the executable bit to both run
#
# ./dek_optimize_5.sh
#
# At any time, a "Ctrl + C" command will stop the script's action.
#
# [1] https://github.com/RazrFalcon/svgcleaner in version 0.9.5 by
#     Apr 10, 2018."""

# Explicitly choose between initial work, or update.
#
# The case-wise design is inspired by an answer at
# https://stackoverflow.com/questions/5542016/bash-user-input-if
read -n1 -p "Choose between [1] initial work, or [q]uit. " doit
case $doit in
    1) choice=10 ;;
    q) choice=0 ;;
esac


# Feedback to the user:
if [ "$choice" = 10 ]
then
    printf "\n[1] Process the original data by overwrite";
elif [ "$choice" = 0 ]
then
    printf "\n[q] Close the script.\n";
fi

# Simplification of the .svg:
if [ "$choice" = 10 ]
then
    mkdir prior_optimization;
    cp ./*.svg ./prior_optimization;
    chmod u+x ./svgcleaner;
elif [ "$choice" = 0 ]
then
    exit
fi

for num in {1..5}
do

    for file in *.svg; do
        echo ""
        echo "cycle $num of 5, processing $input_file"  # CLI reporter

        input_file="$file"
        extent_intermediate='_inter.svg'
        intermediate_file=$input_file$extent_intermediate

        ./svgcleaner "$input_file" "$intermediate_file" --indent 1 \
            --remove-comments --remove-unused-defs --convert-shapes \
            --remove-metadata --remove-nonsvg-attributes \
            --remove-unreferenced-ids --remove-text-attributes \
            --trim-colors --simplify-transforms \
            --paths-coordinates-precision 1
        mv "$intermediate_file" "$input_file"
    done

done

# Finalize the work:
# rm svgcleaner  # space cleaning

echo ""
echo "----"
printf "Number of .svg prior optimization:"; \
    find ./prior_optimization/*.svg | wc -l
printf "Number of .svg after optimization:"; \
    find ./*.svg | wc -l

# EOF
