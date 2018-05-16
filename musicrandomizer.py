import random
import time
from utility import to_position, to_index, xy_to_index, print_ln

# NOTE: Music must be shuffled before room colors!
def shuffle_music(stored_datas):
    #start_time = time.time()
    shuffler = MusicShuffler(stored_datas)
    shuffler.shuffle()
    print_ln('Music shuffled')
    #print_ln('Music shuffled in %f seconds' % (time.time()-start_time))

is_bgm = lambda v : 129 <= v and v <= 159

class MusicShuffler(object):

    def __init__(self, stored_datas):
        self.stored_datas = stored_datas
        original_locations = []

        self.preprocess_tile_music(stored_datas)
        for areaid, data in stored_datas.items():
            self.place_extra_music_triggers(areaid, data.tiledata_event)

        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, eventid)
                for posindex, eventid in enumerate(data.tiledata_event) if is_bgm(eventid))

        self.original_locations = original_locations


    def shuffle(self):
        musics = set(eventid for areaid, posindex, eventid in self.original_locations)
        # Add music trigger 136 (Bounce Bounce), which does not exist in the maps.
        musics.add(136)
        musics = list(musics)

        new_musics = list(musics)
        random.shuffle(new_musics)
        allocation = dict(zip(musics, new_musics))

        stored_datas = self.stored_datas
        for areaid, posindex, eventid in self.original_locations:
            stored_datas[areaid].tiledata_event[posindex] = allocation[eventid]

    def preprocess_tile_music(self, stored_datas):
        self.tilemusics = {}
        for areaid in range(10):
            if areaid in stored_datas:
                tilecolors = stored_datas[areaid].tiledata_roomcolor
                music_fun = music_by_area[areaid]
                tilemusic = [music_fun(tileid, tilecolor)
                             for tileid, tilecolor in enumerate(tilecolors)]
                self.tilemusics[areaid] = tilemusic

    def get_music_from_coords(self, areaid, x, y):
        if areaid not in self.tilemusics: return None
        minitileid = xy_to_minimaptileid(x, y)
        tilemusic = self.tilemusics[areaid]
        if minitileid >= len(tilemusic): return None
        return tilemusic[minitileid]

    def try_place_trigger(self, tiledata_event, areaid, x, y):
        if x < 0 or y < 0 or x >= 500 or y >= 200: return
        tileid = xy_to_index(x, y)
        if tiledata_event[tileid] == 0:
            musicid = self.get_music_from_coords(areaid, x, y)
            if musicid != None:
                tiledata_event[tileid] = musicid

    def place_extra_music_triggers(self, areaid, tiledata_event):
        for tileid, eventid in enumerate(tiledata_event):
            # map transition entrances
            #if (227 <= eventid and eventid <= 232) or (176 <= eventid and eventid <= 178):
            # this line is less readable than the above line, but more performant.
            if (176 <= eventid and eventid <= 232 and not (178 < eventid and eventid < 227)):
                x, y = to_position(tileid)
                for dy in (-1,0,1,2,3):
                    # 9-10 steps on left, 8-9 steps on right is where you spawn
                    for dx in (-8,-9,-10,-11,7,8,9,10):
                        self.try_place_trigger(tiledata_event, areaid, x+dx, y+dy)

                if areaid == 8:
                    # for warp destination map, surround the entrance itself
                    for dy in (-2,-1,0,1,2):
                        for dx in (-2,-1,0,1,2):
                            self.try_place_trigger(tiledata_event, areaid, x+dx, y+dy)

            # warp point targets
            if eventid == 32:
                x, y = to_position(tileid)
                for dy in (1,2,3):
                    for dx in (-2,-1,0,1,2):
                        self.try_place_trigger(tiledata_event, areaid, x+dx, y+dy)
        
        if areaid == 1:
            # Library entrance
            self.try_place_trigger(tiledata_event, areaid, 267, 51)
            self.try_place_trigger(tiledata_event, areaid, 267, 52)
            self.try_place_trigger(tiledata_event, areaid, 268, 51)
            self.try_place_trigger(tiledata_event, areaid, 268, 52)

        if areaid == 5:
            # Terrible effort to surround town entrance after steele events
            self.try_place_trigger(tiledata_event, areaid, 231, 140)
            self.try_place_trigger(tiledata_event, areaid, 231, 141)
            self.try_place_trigger(tiledata_event, areaid, 231, 142)
            self.try_place_trigger(tiledata_event, areaid, 234, 141)
            self.try_place_trigger(tiledata_event, areaid, 235, 141)
            self.try_place_trigger(tiledata_event, areaid, 236, 141)
            self.try_place_trigger(tiledata_event, areaid, 224, 140)
            self.try_place_trigger(tiledata_event, areaid, 224, 141)
            self.try_place_trigger(tiledata_event, areaid, 224, 142)

        if areaid == 9:
            # after cyberspace maids
            for y in range(91,99):
                self.try_place_trigger(tiledata_event, areaid, 327, y)   
            # before save point (backup)
            self.try_place_trigger(tiledata_event, areaid, 338, 96)
            self.try_place_trigger(tiledata_event, areaid, 338, 97)
            self.try_place_trigger(tiledata_event, areaid, 338, 98)             


# transforms from tile sprite xy to minimap tile id 
def xy_to_minimaptileid(x, y):
    mini_x = x//20
    mini_y = (y//45)*4
    if y%45 >= 12: mini_y += (y%45-1)//11
    return mini_x*18+mini_y


## MUSIC DECIDER FUNCTIONS - START

default_music = lambda tilecolor : tilecolor + 128

def area0_music(tileid, tilecolor):
    if tilecolor in (1,2,3,6,7): return default_music(tilecolor)
    else: return None

def area1_music(tileid, tilecolor):
    if tilecolor in (3,9,10,15,21): return default_music(tilecolor)
    elif tilecolor == 24:
        if tileid in (185,203): return 128
        elif tileid in (202,220,221,198,216,234,252): return 133
        else: return default_music(tilecolor)
    #if tilecolor == 34: return None # halloween
    if tileid in (40,58,76): return 149 # missing tiles in graveyard above bridge
    else: return None
    

def area2_music(tileid, tilecolor):
    #if tilecolor == 5: return None
    if tilecolor in (11,13,14,26): return default_music(tilecolor)
    if tileid == 291: return 154 # missing tiles in skyhighbridge above bridge
    #if tilecolor == 55: return None # ravine 2
    else: return None

def area3_music(tileid, tilecolor):
    if tilecolor in (16,23): return default_music(tilecolor)
    elif tilecolor == 4: return 132
    elif tilecolor == 25:
        if tileid in (209,210,211,227,228,229): return 132
        else: return default_music(tilecolor)
    else: return None

def area4_music(tileid, tilecolor):
    if tilecolor in (18,19,20): return default_music(tilecolor)
    else: return None

def area5_music(tileid, tilecolor):
    if tilecolor == 12: return default_music(tilecolor)
    else: return None

def area6_music(tileid, tilecolor):
    if tilecolor == 29: return default_music(tilecolor)
    else: return None

def area7_music(tileid, tilecolor):
    if tilecolor in (28,32): return default_music(tilecolor)
    else: return None

def area8_music(tileid, tilecolor):
    if tilecolor in (27,29): return 155
    else: return None

def area9_music(tileid, tilecolor):
    if tilecolor in (17,22): return default_music(tilecolor)
    else: return None

music_by_area = {
    0: area0_music,
    1: area1_music,
    2: area2_music,
    3: area3_music,
    4: area4_music,
    5: area5_music,
    6: area6_music,
    7: area7_music,
    8: area8_music,
    9: area9_music,
}

## MUSIC DECIDER FUNCTIONS - END