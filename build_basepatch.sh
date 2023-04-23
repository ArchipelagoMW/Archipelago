#!/bin/sh

cd `dirname $0`
armips asm/basepatch.asm -sym data/basepatch.sym &&
bsdiff '../../Wario Land 4 (UE) [!].gba' data/basepatch.gba data/basepatch.bsdiff
