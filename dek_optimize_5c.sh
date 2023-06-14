#!/usr/bin/bash

# name:    dek_optimize_5c.sh
# author:  nbehrnd@yahoo.com
# license: MIT, 2023
# date:    <2023-06-13 Wed>
# edit:
#
# Concept study to moderate svgcleaner.  Deposit both this bash script
# and the svgcleaner (with provision of the executable bit), and run
#
# ```shell
# ./dek_optimize_5c.sh
#```
# for a comparison with sibling `dek_optimize_5b.sh`.  Instead of piping
# an intermediate file (stream) across bash anew into the svgcleaner, the
# discovered `--multipass`, the svgcleaner possibly processes the .svg
# until changes of the file size underpass a critical threshold.  Because
# there is little explicit documentation about this option on the project's
# (now archived) GitHub page, this is a speculation.
# In comparison to `dek_optimize_5b.sh` and a set of 3936 DEK .svg, now 
# all files submitted yield a usable file (script 5b yielded 22 empty files,
# a failure rate of about 0.6%).  Second, the reduction of file size of the
# set is very much comparable with the one obtained with script 5b with the
# additional benefit of a overall processing time of only about 60% of the
# one with script 5b.

# parameters applicable:
parameters="--quiet --indent 1 \
    --remove-comments --remove-unused-defs --convert-shapes \
    --remove-metadata --remove-nonsvg-attributes \
    --remove-unreferenced-ids --remove-text-attributes \
    --trim-colors --simplify-transforms \
    --paths-coordinates-precision 1 --multipass"


for file in *.svg
  do
  echo "$file"
  ./svgcleaner $parameters $file -c > "$file".out.svg
  rm "$file"
done


# restore the file names
file-rename -- 's/\.out\.svg$//' *.svg

# EOF
