#!/usr/bin/bash

# name:    dek_optimize_5a.sh
# author:  nbehrnd@yahoo.com
# license: MIT, 2023
# date:    <2023-05-25 Thu>
# edit:
#
# Concept study to moderate svgcleaner.  Deposit both this bash script
# and the svgcleaner (with provision of the executable bit), and run
#
# ```shell
# ./dek_optimize_5.sh
#```
# for a comparison with sibling `dek_optimize_5b.sh` in terms of robust
# reduction of the file sizes and overall processing time.

for num in {1..5}
do

    for file in *.svg; do

        input_file="$file"
        extent_intermediate='_inter.svg'
        intermediate_file=$input_file$extent_intermediate

        ./svgcleaner "$input_file" "$intermediate_file" --quiet --indent 1 \
            --remove-comments --remove-unused-defs --convert-shapes \
            --remove-metadata --remove-nonsvg-attributes \
            --remove-unreferenced-ids --remove-text-attributes \
            --trim-colors --simplify-transforms \
            --paths-coordinates-precision 1
        mv "$intermediate_file" "$input_file"
    done

done

# EOF
