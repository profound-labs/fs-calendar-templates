#!/bin/bash

if [ "$#" != "2" ]; then
    echo "Pass in two arguments: source dir and destination dir."
    exit 2
fi

SRC="$1"
DST="$2"

echo "Converting jpg..."

for i in "$SRC"/*.jpg; do
    name=`basename -s .jpg "$i"`
    echo -n "$name.jpg ... "
    img2pdf --output "$DST/$name.pdf" "$i"
    if [ "$?" != "0" ]; then
        echo "ERROR"
        exit 2
    fi
    echo "OK"
done
