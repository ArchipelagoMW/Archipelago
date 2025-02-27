#!/bin/sh

set -u
set -e

APWORLD_NAME=wl4
FILES="
    LICENSE
    data
    *.py
"

WORLD_DIR="build/$APWORLD_NAME"

mkdir -p build
rm -rf build/*
mkdir "$WORLD_DIR"
cp -r $FILES "$WORLD_DIR"

cd build
zip -r "$APWORLD_NAME.apworld" "$APWORLD_NAME"
