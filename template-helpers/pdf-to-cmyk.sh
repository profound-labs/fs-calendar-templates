#!/bin/sh

# http://stackoverflow.com/questions/6241282/converting-pdf-to-cmyk-with-identify-recognizing-cmyk

# http://zeroset.mnim.org/2014/07/24/change-image-compression-in-pdf-files-with-ghostscript/

# http://tex.stackexchange.com/questions/9961/pdf-colour-model-and-latex

# http://tex.stackexchange.com/questions/13071/option-cmyk-for-xcolor-package-does-not-produce-a-cmyk-pdf

if [ "$#" != "2" ]; then
    echo "Pass in two arguments: source dir and destination dir."
    exit 2
fi

SRC="$1"
DST="$2"

echo "Converting pdf..."

for i in "$SRC"/*.pdf; do
    name=`basename -s .pdf "$i"`
    echo -n "$name.pdf ... "

    gs \
        -o "$DST/$name.pdf" \
        -sDEVICE=pdfwrite \
        -sProcessColorModel=DeviceCMYK \
        -sColorConversionStrategy=CMYK \
        -sColorConversionStrategyForImages=CMYK \
        -dDownsampleColorImages=false \
        -dAutoFilterColorImages=false \
        -dColorImageFilter=/FlateEncode \
        "$i"

    if [ "$?" != "0" ]; then
        echo "ERROR"
        exit 2
    fi
    echo "OK"
done
