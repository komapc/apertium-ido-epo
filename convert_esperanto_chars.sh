#!/bin/bash
# Postprocessor to convert Esperanto special characters to Ido equivalents
# Usage: echo "text" | apertium epo-ido | ./convert_esperanto_chars.sh

sed -e 's/ĉ/ch/g' \
    -e 's/Ĉ/Ch/g' \
    -e 's/ĝ/g/g' \
    -e 's/Ĝ/G/g' \
    -e 's/ĥ/h/g' \
    -e 's/Ĥ/H/g' \
    -e 's/ĵ/j/g' \
    -e 's/Ĵ/J/g' \
    -e 's/ŝ/sh/g' \
    -e 's/Ŝ/Sh/g' \
    -e 's/ŭ/u/g' \
    -e 's/Ŭ/U/g'
