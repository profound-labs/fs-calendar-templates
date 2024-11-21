#!/bin/bash

if [ "$#" != "2" ]; then
    echo "Pass two arguments: source dir and destination dir."
    exit 2
fi

SRC="$1"
DST="$2"

echo "Converting jpg to 92dpi..."

for i in "$SRC"/*.jpg; do
    name=`basename -s .jpg $i`
    echo -n "$name.jpg ... "
    convert "$i" -compress jpeg -quality 90 -density 300 -resample 92 "$DST/$name.jpg"
    if [ "$?" != "0" ]; then
        echo "ERROR"
        exit 2
    fi
    echo "OK"
done

echo -n "Replacing thumbs with original resolution... "

cp "$SRC"/*-thumb.jpg "$DST"

if [ "$?" != "0" ]; then
    echo "ERROR"
    exit 2
fi
echo "OK"
