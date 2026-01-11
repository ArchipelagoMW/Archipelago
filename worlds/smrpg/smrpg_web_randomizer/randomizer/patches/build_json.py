#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys

# Build static JSON versions of all the IPS patches and put them in a static folder.


def parse_ips(ips):
    f = open(ips, 'rb')
    if f.read(5) != b'PATCH':
        raise ValueError("File does not begin with PATCH header")

    patch = []

    while True:
        offset = f.read(3)
        if offset == b'EOF':
            break
        offset = int(offset.hex(), 16)
        size = int(f.read(2).hex(), 16)

        # Check for RLE
        if not size:
            rle_size = int(f.read(2).hex(), 16)
            value = f.read(1)
            patch.append({offset: list(value) * rle_size})
        else:
            data = f.read(size)
            patch.append({offset: list(data)})

    return patch


thisdir = os.path.split(os.path.abspath(sys.argv[0]))[0]
files = [f for f in os.listdir(thisdir) if f.lower().endswith('.ips')]

static_dir = os.path.normpath(os.path.join(thisdir, '../static/randomizer/patches'))
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

for f in files:
    print("Building patch for: {}".format(f))
    patch = parse_ips(os.path.join(thisdir, f))
    json_file = os.path.join(static_dir, os.path.splitext(f)[0] + '.json')
    with open(json_file, 'w') as file_obj:
        json.dump(patch, file_obj)
