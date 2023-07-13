#!/bin/sh

cd `dirname $0`
armips asm/basepatch.asm -sym data/basepatch_ext.sym &&
bsdiff '../../Wario Land 4 (UE) [!].gba' data/basepatch.gba data/basepatch.bsdiff
grep -Ev '[0-9A-F]{8} [@.].*' data/basepatch_ext.sym > data/basepatch.sym
if [ $1 -z ]; then rm -f data/basepatch_ext.sym; fi
