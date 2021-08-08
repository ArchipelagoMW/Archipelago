#!/usr/bin/env python
import sys
import os
import struct

if sys.argv[1] == "":
	print("merge_ips.py <new_ips> <orig_ips>")
	sys.exit()
else:
	new_name = sys.argv[1]
	org_name = sys.argv[2]

fn = open(os.path.dirname(os.path.realpath(__file__)) + "/" + new_name, "rb")
fo = open(os.path.dirname(os.path.realpath(__file__)) + "/" + org_name, "rb+")

print("Merging %s into %s" % (new_name, org_name))

fo.seek(-3, 2)
fn.seek(5)

offset = fn.read(3)
while offset != b'EOF':
    length_data = fn.read(2)
    length = struct.unpack(">H", length_data)[0]
    if length > 0:
        patch_data = fn.read(length)
    else:
        patch_data = fn.read(3)
    
    fo.write(offset)
    fo.write(length_data)
    fo.write(patch_data)
    offset = fn.read(3)

fo.write(b'EOF')
fo.close()
fn.close()