#!/usr/bin/bash

# name:    dek_optimize_5c.sh
# author:  nbehrnd@yahoo.com
# license: MIT, 2023
# date:    <2023-06-13 Wed>
# edit:    <2023-06-29 Thu>
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
# until changes of the file size underpass a critical threshold.  Command
# options selected are in the sequence of the now archived documentation of
# the project, see
#
# https://github.com/RazrFalcon/svgcleaner
# https://github.com/RazrFalcon/svgcleaner/blob/master/docs/svgcleaner.adoc
#
# for additional background and typical processing of motifs.

# parameters applicable:
parameters="--quiet --indent none \
  --remove-comments --remove-declarations --remove-nonsvg-elements \
  --remove-unused-defs --convert-shapes --remove-title --remove-desc \
  --remove-metadata --remove-nonsvg-attributes --remove-dupl-lineargradient \
  --remove-dupl-radialgradient --remove-dupl-fegaussianblur --ungroup-groups \
  --ungroup-defs --merge-gradients --regroup-gradient-stops \
  --remove-invisible-elements --resolve-use --remove-version \
  --remove-unreferenced-ids --trim-ids \
  --remove-text-attributes --remove-unused-coordinates \
  --remove-default-attributes --remove-xmlns-xlink-attribute \
  --remove-needless-attributes --remove-gradient-attributes \
  --apply-transform-to-gradients --apply-transform-to-shapes \
  --remove-unresolved-classes --paths-to-relative --remove-unused-segments\
  --convert-segments --apply-transform-to-paths --trim-paths \
  --join-arcto-flags --remove-dupl-cmd-in-paths --use-implicit-cmds \
  --trim-colors --simplify-transforms \
  --coordinates-precision 1 ----properties-precision 1 \
  --paths-coordinates-precision 1 --list-separator space \
  --multipass"


for file in *.svg
  do
  echo "$file"
  ./svgcleaner $parameters $file -c > "$file".out.svg
  rm "$file"
done


# restore the file names
file-rename -- 's/\.out\.svg$//' *.svg

# EOF
