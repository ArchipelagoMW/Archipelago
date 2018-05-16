import shutil
import struct
import json
import os
import sys

DIR_ORIGINAL_MAPS = './original'
DIR_MODIFIED_MAPS = './modified'
DIR_GENERATED_MAPS = './generated'

MAP_SIZE = 100000
MAP_HEIGHT = 200

MINIMAP_SIZE = 450
MINIMAP_HEIGHT = 18

# List of tuples used to maintain sorted order
ARRAYS_MAP = [
    ('collision', 0),
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
    def __init__(self, source_file=None):
        self.data_map = {}
        self.data_minimap = {}
        self.data_int = {}
        if source_file == None: return
        
        f = open(source_file, "rb")

        for name, offset in ARRAYS_MAP:
            f.seek(offset)
            tiledata = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
            self.data_map[name] = tiledata

        for name, offset in ARRAYS_MINIMAP:
            f.seek(offset)
            tiledata = list(struct.unpack('%dh' % MINIMAP_SIZE, f.read(MINIMAP_SIZE*2)))
            self.data_minimap[name] = tiledata

        for name, offset in INTS:
            f.seek(offset)
            metadata = list(struct.unpack('i', f.read(4)))[0]
            self.data_int[name] = metadata

        f.close()

    def copy(self):
        clone = MapData()
        clone.data_map = dict((name, list(tiledata)) for name, tiledata in self.data_map.items())
        clone.data_minimap = dict((name, list(tiledata)) for name, tiledata in self.data_minimap.items())
        clone.data_int = dict((name, metadata) for name, metadata in self.data_int.items())
        return clone

    def apply_diff(self, diffs):
        for layer_name, diff in diffs.items():
            if layer_name in (x[0] for x in ARRAYS_MINIMAP):
                array = self.data_minimap[layer_name]
            else:
                array = self.data_map[layer_name]

            for index, coords, value in diff:
                array[index] = value

    def save_to_file(self, file_name):
        f = open(file_name, "wb+")

        for name, offset in ARRAYS_MAP:
            f.seek(offset)
            f.write(struct.pack('%dh' % MAP_SIZE, *self.data_map[name]))

        for name, offset in ARRAYS_MINIMAP:
            f.seek(offset)
            f.write(struct.pack('%dh' % MINIMAP_SIZE, *self.data_minimap[name]))

        for name, offset in INTS:
            f.seek(offset)
            f.write(struct.pack('i', self.data_int[name]))

        f.close()


class DiffData(object):
    def __init__(self, diff_file):
        f = open(diff_file)
        lines = f.read().split('\n')
        f.close()

        area_diffs = {}

        areaid = None
        area_lines = []
        for line in lines:
            if line.startswith('=='):
                if areaid != None:
                    area_diffs[areaid] = self._parse_area_diff(area_lines)
                    area_lines.clear()
                areaid = int(line.strip('=').split(':')[-1])
            else:
                area_lines.append(line)
        if areaid != None:
            area_diffs[areaid] = self._parse_area_diff(area_lines)
            area_lines.clear()

        self.area_diffs = area_diffs

    def get_areaids(self):
        return sorted(self.area_diffs.keys())

    def _parse_area_diff(self, lines):
        diffs = {}

        layer_name = None
        format_type = None
        layer_lines = []
        for line in lines:
            if line.startswith('@'):
                if layer_name != None:
                    diffs[layer_name] = self._parse_diff(layer_name, layer_lines, format_type)
                    layer_lines.clear()
                layer_name, format_type = line.strip('@').split(':')
            else:
                layer_lines.append(line)
        if layer_name != None:
            diffs[layer_name] = self._parse_diff(layer_name, layer_lines, format_type)
            layer_lines.clear()

        return diffs

    def _parse_diff(self, layer_name, layer_lines, format_type):
        if layer_name in (x[0] for x in ARRAYS_MINIMAP):
            index_function = minimap_index
        else:
            index_function = map_index

        if format_type.startswith('L'):
            return self._parse_line_diff(layer_lines, index_function)
        elif format_type.startswith('B'):
            x1, y1 = map(int, format_type[format_type.find('(')+1:format_type.rfind(')')].split(','))
            return self._parse_box_diff(layer_lines, index_function, x1, y1)

    def _parse_line_diff(self, lines, index_function):
        diff = []
        for line in lines:
            coords, value = line.split(':')
            x, y = coords.split(',')
            x, y, value = map(int, (x, y, value))
            diff.append((index_function(x, y), (x, y), value))
        return diff

    def _parse_box_diff(self, lines, index_function, x1, y1):
        diff = []
        for dy, line in enumerate(lines):
            values = line.split(',')
            for dx, value in enumerate(values):
                if value == '': continue
                x, y = x1+dx, y1+dy
                diff.append((index_function(x, y), (x, y), int(value)))
        return diff


def apply_diff_to_maps(maps_by_area, diff_data):
    new_maps = {}
    for areaid, map_data in maps_by_area.items():
        new_map = map_data.copy()
        diffs = diff_data.area_diffs[areaid]
        new_map.apply_diff(diffs)
        new_maps[areaid] = new_map
    return new_maps


def list_diff(original_arr, modified_arr, coordinate_function):
    return [(index, coordinate_function(index), value[1]) for index, value in enumerate(zip(original_arr, modified_arr)) if value[0] != value[1]]

def compute_bounding_box(coordinate_list):
    x1 = min(x for x,y in coordinate_list)
    y1 = min(y for x,y in coordinate_list)
    x2 = max(x for x,y in coordinate_list) + 1
    y2 = max(y for x,y in coordinate_list) + 1
    return x1, y1, (x2-x1), (y2-y1)

def box_format(x1, y1, w, h, layer_name, diff):
    sb = ['@%s:B(%d,%d)' % (layer_name, x1, y1)]
    sorted_diff = [(c[0],c[1],v) for i,c,v in diff]
    sorted_diff.sort(key=lambda p : (p[1],p[0]))
    box = [['']*w for i in range(h)]
    for i, c, value in diff:
        x, y = c
        box[y-y1][x-x1] = str(value)
    box = [row[:max(i for i,v in enumerate([1]+row) if v != '')] for row in box]
    sb += [','.join(row) for row in box]
    return sb


def line_format(layer_name, diff):
    sb = ['@%s:L' % layer_name]
    sb += ['%d,%d:%d' % (c[0], c[1], v) for i,c,v in diff]
    return sb

def format_diff(layer_name, diff):
    coordinate_list = [(coords[0], coords[1]) for index,coords,value in diff]
    x1,y1,w,h = compute_bounding_box(coordinate_list)

    size_box_format = (w-1)*h
    size_line_format = len(coordinate_list)*8

    if size_box_format < size_line_format:
        return box_format(x1, y1, w, h, layer_name, diff)
    else:
        return line_format(layer_name, diff)

def map_coords(index):
    return (index//MAP_HEIGHT, index%MAP_HEIGHT)

def minimap_coords(index):
    return (index//MINIMAP_HEIGHT, index%MINIMAP_HEIGHT)

def map_index(x, y):
    return x*MAP_HEIGHT + y

def minimap_index(x, y):
    return x*MINIMAP_HEIGHT + y

def xy_to_minimaptileid(x, y):
    mini_x = x//20
    mini_y = (y//45)*4
    if y%45 >= 12: mini_y += (y%45-1)//11
    return mini_x, mini_y

def bounding_box_filter(diff, bbox, minimap=False):
    x1, y1, w, h = bbox
    x2, y2 = x1+w, y1+h
    if minimap:
        x1, y1 = xy_to_minimaptileid(x1, y1)
        x2, y2 = xy_to_minimaptileid(x2, y2)
    return [(i, c, v) for i, c, v in diff if (x1 <= c[0] and y1 <= c[1] and c[0] < x2 and c[1] < y2)]


def diff_maps(original_file, modified_file, bbox=None):
    original = MapData(original_file)
    modified = MapData(modified_file)

    diffs = {}

    for name, _ in ARRAYS_MAP:
        diffs[name] = list_diff(original.data_map[name], modified.data_map[name], map_coords)
        if bbox != None: diffs[name] = bounding_box_filter(diffs[name], bbox, minimap=False)

    for name, _ in ARRAYS_MINIMAP:
        diffs[name] = list_diff(original.data_minimap[name], modified.data_minimap[name], minimap_coords)
        if bbox != None: diffs[name] = bounding_box_filter(diffs[name], bbox, minimap=True)

    return diffs


def generate_diff_file(diff_file_name='output.txt', bboxes=None):
    sb = []
    for areaid in range(10):
        filename = 'area%d.map' % areaid
        files_original = os.listdir(DIR_ORIGINAL_MAPS)
        files_modified = os.listdir(DIR_MODIFIED_MAPS)

        if filename in files_modified:
            if not filename in files_original:
                print_ln('ERROR! MISSING FILE - %s' % filename)
                return

            #if areaid == 2: bbox = 254, 182, 2, 2
            #else: bbox = 456, 157, 26, 14
            bbox = None
            if bboxes != None: bbox = bboxes[areaid]

            diffs = diff_maps('%s/%s' % (DIR_ORIGINAL_MAPS, filename), '%s/%s' % (DIR_MODIFIED_MAPS, filename), bbox)
            if all(len(changes) == 0 for name, changes in diffs.items()):
                continue

            sb.append('==area:%d==' % areaid)
            for name in sorted(diffs.keys()):
                changes = diffs[name]
                if len(diffs[name]) == 0: continue
                sb += format_diff(name, diffs[name])

    f = open(diff_file_name, 'w+')
    f.write('\n'.join(sb))
    f.close()

def generate_maps_from_diff_file(diff_file_name='output.txt'):
    diff_data = DiffData(diff_file_name)

    maps_by_area = {}
    for areaid in diff_data.get_areaids():
        maps_by_area[areaid] = MapData('%s/area%d.map' % (DIR_ORIGINAL_MAPS, areaid))

    new_maps = apply_diff_to_maps(maps_by_area, diff_data)

    for areaid, map_data in new_maps.items():
        map_data.save_to_file('%s/area%d.map' % (DIR_GENERATED_MAPS, areaid))

if __name__ == '__main__':
    generate_diff_file()
    #generate_maps_from_diff_file()

