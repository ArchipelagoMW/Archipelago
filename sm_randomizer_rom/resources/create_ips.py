#!/usr/bin/env python
import sys
import os

if sys.argv[1] == "":
	print("ips.py <00_file> <ff_file> <output>")
	sys.exit()
else:
	zero_name = sys.argv[1]
	ff_name = sys.argv[2]
	output_name = sys.argv[3]

f_zero = open(os.path.dirname(os.path.realpath(__file__)) + "/" + zero_name, "rb")
f_ff = open(os.path.dirname(os.path.realpath(__file__)) + "/" + ff_name, "rb")
fo = open(os.path.dirname(os.path.realpath(__file__)) + "/" + output_name, "wb")

d_zero = f_zero.read()
d_ff = f_ff.read()
patches = {}

for i in range(0, len(d_zero), 1):
    if d_zero[i] == d_ff[i]:
        patches[i] = [d_zero[i]]

base_m = -100
prev_m = -100
for m in list(patches.keys()):
    if prev_m == m - 1:
        if len(patches[base_m]) < 0xFFFF:
            patches[base_m] += patches[m]
            del patches[m]
            prev_m = m
        else:
            base_m = m
            prev_m = m
    else:
        base_m = m
        prev_m = m

d_patch = []
for k in patches:
    l = len(patches[k])
    d_patch += [(k >> 16) & 0xff, (k >> 8) & 0xFF, k & 0xFF, (l >> 8) & 0xFF, l & 0xFF] + patches[k]


d_patch = [0x50, 0x41, 0x54, 0x43, 0x48] + d_patch + [0x45, 0x4f, 0x46]
fo.write(bytes(d_patch))
fo.close()
f_ff.close()
f_zero.close()
