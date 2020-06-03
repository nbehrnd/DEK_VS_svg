#!/bin/bash

# name:    dek_optimize_5.sh
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-31 (YYYY-MM-DD)
# edit:
#
# With a copy of the Linux' executable of svgcleaner in the same
# directory as this bash script, just one level above the folder
# 'dek_workshop', the .svg files are significantly simplified.  This
# reduces individual file sizes, and of the intended Anki deck.
#
# By experience, while the first cycle of simplification offers the
# most savings of individual file sizes, multiple passes may offer a
# better "globally converged" file size optimization.  After five
# cycles of simplification, the file size reduction seems to be "good
# enough" here, the apparent global size of all .svg files then is
# about 20..25% of the original files.
#
# At any time, a "Ctrl + C" command will stop the script's action.


cp svgcleaner ./dek_workshop/
cd dek_workshop
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

rm svgcleaner  # space cleaning

echo ""
echo "Number of .svg files in folder 'dek_workshop':"
ls *.svg | wc -l
echo "Number of all files in folder 'dek_workshop':"
ls *.* | wc -l
echo "Apparent file size of all files in folder 'dek_workshop':"
du -h --apparent-size

# END
