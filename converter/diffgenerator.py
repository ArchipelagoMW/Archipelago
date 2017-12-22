import shutil
import struct
import json
import os
import sys

DIR_ORIGINAL_MAPS = './s1_original_maps'
DIR_EDITABLE_MAPS = './s2_editable_maps'
DIR_FINAL_MAPS = './s3_final_maps'

MAP_SIZE = 100000
MAP_HEIGHT = 200

MINIMAP_SIZE = 450
MINIMAP_HEIGHT = 18

# List of tuples used to maintain sorted order
ARRAYS_MAP = [
    ('map', 0),
    ('event', 200000),
    ('items', 402700),
    ('tiles0', 602704),
    ('tiles1', 802704),
    ('tiles2', 1002704),
    ('tiles3', 1202704),
    ('tiles4', 1402704),
    ('tiles5', 1602704),
    ('tiles6', 1802704),
]

ARRAYS_MINIMAP = [
    ('roomtype', 400000),
    ('roomcolor', 400900),
    ('roombg', 401800),
]

INTS = [
    ('area', 602700),
    ('version', 2602704),
]

class MapData(object):
    def __init__(self, sourcefile):
        f = open(sourcefile, "rb")

        self.data_map = []
        for name, offset in ARRAYS_MAP:
            f.seek(offset)
            tiledata = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
            self.data_map.append((name, tiledata))

        self.data_minimap = []
        for name, offset in ARRAYS_MINIMAP:
            f.seek(offset)
            tiledata = list(struct.unpack('%dh' % MINIMAP_SIZE, f.read(MINIMAP_SIZE*2)))
            self.data_map.append((name, tiledata))

        self.data_int = []
        for name, offset in ARRAYS_INT:
            f.seek(offset)
            metadata = list(struct.unpack('i', f.read(4)))[0]
            self.data_map.append((name, metadata))

        f.close()


def list_diff(original_arr, modified_arr):
    return [(index, value[1]) for index, value in enumerate(zip(original_arr, modified_arr)) if value[0] != value[1]]

def map_coords(index):
    return '%d,%d' % (index//MAP_HEIGHT, index%MAP_HEIGHT)

def minimap_coords(index):
    return '%d,%d' % (index//MINIMAP_HEIGHT, index%MINIMAP_HEIGHT)

def diff_maps(original_file, modified_file):

    original = MapData(original_file)
    modified = MapData(modified_file)

    sb = []

    for name, _ in ARRAYS_MAP:
        sb.append('===%s===' % name)
        diff = list_diff(original.data_map[name], modified.data_map[name])
        sb += ['%s:%s' % (map_coords(index), value) for index, value in diff]

    for name, _ in ARRAYS_MINIMAP:
        sb.append('===%s===' % name)
        diff = list_diff(original.data_minimap[name], modified.data_minimap[name])
        sb += ['%s:%s' % (minimap_coords(index), value) for index, value in diff]

    return '\n'.join(sb)    




if __name__ == '__main__':
    main()
