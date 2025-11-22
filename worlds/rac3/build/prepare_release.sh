#!/bin/bash

SCRIPT_DIR=$(cd `dirname $0` && pwd)
cd $SCRIPT_DIR
zip -qo -r ./rac3.apworld ./rac3

OUTPUT=rac3jp_ap
rm -rf $OUTPUT $OUTPUT.zip
mkdir -p $OUTPUT
cp -f ./rac3.apworld ${OUTPUT}
zip -r $OUTPUT{.zip,}

