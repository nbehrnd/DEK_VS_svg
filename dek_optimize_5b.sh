#!/usr/bin/bash

# name:    dek_optimize_5b.sh
# author:  nbehrnd@yahoo.com
# license: MIT, 2023
# date:    <2023-05-25 Thu>
# edit:    <2023-06-05 Mon>
#
# Concept study to moderate svgcleaner.  Deposit both this bash script
# and the svgcleaner (with provision of the executable bit), and run
#
# ```shell
# ./dek_optimize_5.sh
#```
# for a comparison with sibling `dek_optimize_5a.sh` in terms of robust
# reduction of the file sizes and overall processing time.  This time,
# a file already read into the RAM is retained for multiple iterations
# to reduce the file size until the result eventually is written as a
# new permanent record.


# parameters applicable to each iteration, in absence of problem to run
# without a note back to the CLI:
parameters="--quiet --indent 1 \
    --remove-comments --remove-unused-defs --convert-shapes \
    --remove-metadata --remove-nonsvg-attributes \
    --remove-unreferenced-ids --remove-text-attributes \
    --trim-colors --simplify-transforms \
    --paths-coordinates-precision 1"


for file in *.svg
  do
  echo "$file"
  ./svgcleaner $parameters $file -c | ./svgcleaner $parameters - -c | \
    ./svgcleaner $parameters - -c | ./svgcleaner $parameters - -c | \
    ./svgcleaner $parameters - -c > "$file".out.svg
  rm "$file"
done


# restore the file names
file-rename -- 's/\.out\.svg$//' *.svg

# EOF
