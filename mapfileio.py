import struct
from utility import *

MAP_SIZE = 100000
MINIMAP_SIZE = 450
MAP_COLLISION_OFFSET = 0
MAP_EVENTS_OFFSET = 200000
MAP_ROOMTYPE_OFFSET = 400000
MAP_ROOMCOLOR_OFFSET = 400900
MAP_ROOMBG_OFFSET = 401800
MAP_ITEMS_OFFSET = 402700
MAP_TILES1_OFFSET = 802704
MAP_TILES3_OFFSET = 1202704
MAP_TILES4_OFFSET = 1402704
MAP_TILES5_OFFSET = 1602704
EGG_EVENT_ID = 250
EGG_ID = -250
NORMAL_BOMB_BLOCK_ID = 2
CHAIN_BOMB_BLOCK_ID = 3
BOMB_BLOCK_IDS = (NORMAL_BOMB_BLOCK_ID, CHAIN_BOMB_BLOCK_ID)

def write_all(areaid, items, stored_data, path='.'):
    tiledata_map = list(stored_data.tiledata_map)
    tiledata_event = list(stored_data.tiledata_event)
    tiledata_items = list(stored_data.tiledata_items)
    tiledata_roomtype = list(stored_data.tiledata_roomtype)
    tiledata_roomcolor = list(stored_data.tiledata_roomcolor)
    tiledata_roombg = list(stored_data.tiledata_roombg)
    tiledata_tiles3 = list(stored_data.tiledata_tiles3)
    tiledata_tiles4 = list(stored_data.tiledata_tiles4)
    tiledata_tiles1 = list(stored_data.tiledata_tiles1)
    tiledata_tiles5 = list(stored_data.tiledata_tiles5)
    
    # Note: read from stored data, write to actual data
    for item in items:
        if item.areaid != areaid: continue
        index = to_index(item.position)
        if item.itemid == EGG_ID:
            # place egg
            x, y = item.position
            if stored_data.tiledata_map[index] != 0:
                if has_neighboring_bomb_block(stored_data.tiledata_event, x, y):
                    ensure_neighboring_chain_bomb_block(tiledata_event, x, y)
                else:
                    tiledata_map[index] = 0
                    tiledata_tiles1[index] = 0
            else:
                tiledata_tiles1[index] = 0
            tiledata_event[index] = EGG_EVENT_ID
            tiledata_tiles3[index] = 0
            tiledata_tiles4[index] = 0
            tiledata_tiles5[index] = 0

        else:
            # place item
            tiledata_items[index] = item.itemid

    f = open(map_filename(areaid, path) , "r+b")
    f.seek(MAP_COLLISION_OFFSET)
    f.write(struct.pack('%dh' % MAP_SIZE, *tiledata_map))
    f.seek(MAP_EVENTS_OFFSET)
    f.write(struct.pack('%dh' % MAP_SIZE, *tiledata_event))
    f.seek(MAP_ITEMS_OFFSET)
    f.write(struct.pack('%dh' % MAP_SIZE, *tiledata_items))
    f.seek(MAP_ROOMTYPE_OFFSET)
    f.write(struct.pack('%dh' % MINIMAP_SIZE, *tiledata_roomtype))
    f.seek(MAP_ROOMCOLOR_OFFSET)
    f.write(struct.pack('%dh' % MINIMAP_SIZE, *tiledata_roomcolor))
    f.seek(MAP_ROOMBG_OFFSET)
    f.write(struct.pack('%dh' % MINIMAP_SIZE, *tiledata_roombg))
    f.seek(MAP_TILES3_OFFSET)
    f.write(struct.pack('%dh' % MAP_SIZE, *tiledata_tiles3))
    f.seek(MAP_TILES4_OFFSET)
    f.write(struct.pack('%dh' % MAP_SIZE, *tiledata_tiles4))
    f.seek(MAP_TILES1_OFFSET)
    f.write(struct.pack('%dh' % MAP_SIZE, *tiledata_tiles1))
    f.seek(MAP_TILES5_OFFSET)
    f.write(struct.pack('%dh' % MAP_SIZE, *tiledata_tiles5))
    f.close()
    

def write_items(areaid, items, path='.'):
    tiledata = [b'\x00\x00' for i in range(MAP_SIZE)]
    for item in items:
        if item.areaid != areaid: continue
        if item.itemid == EGG_ID: continue
        index = to_index(item.position)
        tiledata[index] = struct.pack('h', item.itemid)

    f = open(map_filename(areaid, path), 'r+b')
    f.seek(MAP_ITEMS_OFFSET)
    f.write(b''.join(tiledata))
    f.close()

def map_filename(areaid, path='.'):
    return '%s/area%d.map' % (path, areaid)

def print_all_items(path='.'):
    sb = []
    for areaid in range(0,10):
        continue
        items = load_items(areaid, path)
        sb.append('Area %d: NAME' % areaid)
        for item in items:
            sb.append(str(item))
    for areaid in range(0,10):
        items = load_eggs(areaid, path)
        for item in items:
            item.name = 'EGG_'
        sb.append('Area %d: NAME' % areaid)
        for item in items:
            sb.append(str(item))
    print('\n'.join(sb))

def has_neighboring_bomb_block(tiledata_event, x, y):
    px, py = x-1, y
    if px >= 0 and tiledata_event[xy_to_index(px,py)] in BOMB_BLOCK_IDS:
        return True
    px, py = x+1, y
    if px < 500 and tiledata_event[xy_to_index(px,py)] in BOMB_BLOCK_IDS:
        return True
    px, py = x, y-1
    if py >= 0 and tiledata_event[xy_to_index(px,py)] in BOMB_BLOCK_IDS:
        return True
    px, py = x, y+1
    if py < 200 and tiledata_event[xy_to_index(px,py)] in BOMB_BLOCK_IDS:
        return True
    return False

def ensure_neighboring_chain_bomb_block(tiledata_event, x, y):
    px, py = x-1, y
    if px >= 0 and tiledata_event[xy_to_index(px,py)] == CHAIN_BOMB_BLOCK_ID:
        return
    px, py = x+1, y
    if px < 500 and tiledata_event[xy_to_index(px,py)] == CHAIN_BOMB_BLOCK_ID:
        return
    px, py = x, y-1
    if py >= 0 and tiledata_event[xy_to_index(px,py)] == CHAIN_BOMB_BLOCK_ID:
        return
    px, py = x, y+1
    if py < 200 and tiledata_event[xy_to_index(px,py)] == CHAIN_BOMB_BLOCK_ID:
        return

    # No neighboring chain block. convert one to it
    px, py = x-1, y
    if px >= 0 and tiledata_event[xy_to_index(px,py)] == NORMAL_BOMB_BLOCK_ID:
        tiledata_event[xy_to_index(px,py)] = CHAIN_BOMB_BLOCK_ID
        return
    px, py = x+1, y
    if px < 500 and tiledata_event[xy_to_index(px,py)] == NORMAL_BOMB_BLOCK_ID:
        tiledata_event[xy_to_index(px,py)] = CHAIN_BOMB_BLOCK_ID
        return
    px, py = x, y-1
    if py >= 0 and tiledata_event[xy_to_index(px,py)] == NORMAL_BOMB_BLOCK_ID:
        tiledata_event[xy_to_index(px,py)] = CHAIN_BOMB_BLOCK_ID
        return
    px, py = x, y+1
    if py < 200 and tiledata_event[xy_to_index(px,py)] == NORMAL_BOMB_BLOCK_ID:
        tiledata_event[xy_to_index(px,py)] = CHAIN_BOMB_BLOCK_ID
        return
    print('ERROR ENSURING NEIGHBORING CHAIN BLOCK: (%d, %d)' % (x,y))


class StoredMapData(object):
    def __init__(self, filename):
        f = open(filename, "rb")
        f.seek(MAP_COLLISION_OFFSET)
        self.tiledata_map = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
        f.seek(MAP_EVENTS_OFFSET)
        self.tiledata_event = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
        f.seek(MAP_ROOMTYPE_OFFSET)
        self.tiledata_roomtype = list(struct.unpack('%dh' % MINIMAP_SIZE, f.read(MINIMAP_SIZE*2)))
        f.seek(MAP_ROOMCOLOR_OFFSET)
        self.tiledata_roomcolor = list(struct.unpack('%dh' % MINIMAP_SIZE, f.read(MINIMAP_SIZE*2)))
        f.seek(MAP_ROOMBG_OFFSET)
        self.tiledata_roombg = list(struct.unpack('%dh' % MINIMAP_SIZE, f.read(MINIMAP_SIZE*2)))
        f.seek(MAP_ITEMS_OFFSET)
        self.tiledata_items = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
        f.seek(MAP_TILES3_OFFSET)
        self.tiledata_tiles3 = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
        f.seek(MAP_TILES4_OFFSET)
        self.tiledata_tiles4 = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
        f.seek(MAP_TILES1_OFFSET)
        self.tiledata_tiles1 = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
        f.seek(MAP_TILES5_OFFSET)
        self.tiledata_tiles5 = list(struct.unpack('%dh' % MAP_SIZE, f.read(MAP_SIZE*2)))
        f.close()

    def clear_items(self):
        self.tiledata_items = [0]*MAP_SIZE

    def clear_eggs(self):
        to_set_to_bomb_block = set()
        for i in range(MAP_SIZE):
            x, y = to_position(i)
            if self.tiledata_event[i] == EGG_EVENT_ID and self.tiledata_map[i] != 0 and \
                    has_neighboring_bomb_block(self.tiledata_event, x, y):
                to_set_to_bomb_block.add(i)
        self.tiledata_event = [(0 if x == EGG_EVENT_ID else x) for x in self.tiledata_event]
        for i in to_set_to_bomb_block:
            self.tiledata_event[i] = CHAIN_BOMB_BLOCK_ID

    def clear_items_and_eggs(self):
        self.clear_items()
        self.clear_eggs()


class ItemModifier(object):
    def __init__(self, areaids, source_dir='.', no_load=False):
        self.areaids = list(areaids)
        self.items = dict((areaid, {}) for areaid in areaids)

        if no_load:
            self._set_all_dirty_flags(True)
        else:
            # Load items from maps
            for areaid in areaids:
                for item in load_items(areaid, source_dir):
                    self.items[item.areaid][item.position] = item
            self._set_all_dirty_flags(False)

        self.stored_datas = {}
        for areaid in self.areaids:
            stored_data = StoredMapData(map_filename(areaid, source_dir))
            stored_data.clear_items_and_eggs()
            self.stored_datas[areaid] = stored_data

    def _set_all_dirty_flags(self, value):
        self.modified = dict((areaid, value) for areaid in self.areaids)

    def _dirty(self, areaid):
        self.modified[areaid] = True

    def clear_items(self):
        self.items = dict((areaid, {}) for areaid in self.areaids)
        self._set_all_dirty_flags(True)

    def add_item(self, item):
        self.items[item.areaid][item.position] = item
        self._dirty(item.areaid)

    def delete_item(self, item):
        try: del self.items[item.areaid][item.position]
        except KeyError:
            print('item [%s] does not exist!' % item)
        self._dirty(item.areaid)

    def delete_position(self, areaid, position):
        try: del self.items[areaid][position]
        except KeyError:
            print('position [%d, %s] does not exist!' % areaid, position)
        self._dirty(item.areaid)

    def save(self, output_dir='.'):
        for areaid, modified in self.modified.items():
            if not modified: continue
            #write_items(areaid, self.items[areaid].values(), output_dir)
            write_all(areaid, self.items[areaid].values(), self.stored_datas[areaid], path=output_dir)

        # Reset dirty flags
        self._set_all_dirty_flags(False)

def exists_map_files(areaids, path='.'):
    import os
    for areaid in areaids:
        if not os.path.isfile(map_filename(areaid, path)):
            return False
    return True

def grab_original_maps(source_dir='original_maps', output_dir='.'):
    areaids = list(range(10))
    import shutil
    import os
    BACKUP_DIR = source_dir.rstrip('/')
    for f in filter(lambda s : s.endswith('.map'), os.listdir(BACKUP_DIR)):
        shutil.copyfile('%s/%s' % (BACKUP_DIR, f), '%s/%s' % (output_dir, f))


if __name__ == '__main__':
    pass