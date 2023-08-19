#!/bin/bash
set -e
rm -rf WoL_build
mkdir -p WoL_build
for map in WoL/*.SC2Map ; do
    mpqfile=WoL_build/$(sed 's/^WoL\///g' <<< "$map")
    smpq -c $mpqfile
    pushd $map
        for file in $(find . -type f) ; do
            file=$(cut -c 3- <<< "$file")
            smpq -a ../../$mpqfile $file
        done
    popd
done
