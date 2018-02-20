import random
import time

LAGGY_BACKGROUNDS = set((37, 65, 66, 80, 84, 88, 89, 99))
DIFFICULT_BACKGROUNDS = set((36, 37, 56, 57, 60, 65, 66, 80, 84, 89, 103, 110))

def to_tile_index(x, y):
    return x*18 + y

def shuffle_backgrounds(stored_datas, no_laggy_backgrounds, no_difficult_backgrounds):
    #start_time = time.time()
    shuffler = BackgroundShuffler(stored_datas, no_laggy_backgrounds, no_difficult_backgrounds)
    shuffler.shuffle()
    print('Backgrounds shuffled')

    shuffler = RoomColorShuffler(stored_datas)
    shuffler.shuffle()
    print('Tile colors shuffled')
    #print('Backgrounds shuffled in %f seconds' % (time.time()-start_time))


class BackgroundShuffler(object):
    def __init__(self, stored_datas, no_laggy_backgrounds, no_difficult_backgrounds):
        self.stored_datas = stored_datas
        original_locations = []

        filter_function = self.filter_function
        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, val)
                for posindex, val in enumerate(data.tiledata_roombg) if filter_function(val))
        self.specify_original_backgrounds(original_locations)

        self.original_locations = original_locations
        self.no_laggy_backgrounds = no_laggy_backgrounds
        self.no_difficult_backgrounds = no_difficult_backgrounds

    def filter_function(self, val):
        # don't shuffle DLC backgrounds
        # don't shuffle Noah3 background because it does weird things to boss doors
        # don't shuffle library entrance background because it removes springs
        return val <= 118 and val not in (0,23,17,83,104,110)

    def specify_original_backgrounds(self, original_locations):
        # Replace roombg == 0 tiles with specified backgrounds.
        # This is required for some bg fixes to work.
        original_locations += [
            # Area around the Saya boss fight
            (4, to_tile_index(21,3), 6),
            (4, to_tile_index(22,3), 6),
            (4, to_tile_index(23,3), 6),
            (4, to_tile_index(24,3), 6),
            (4, to_tile_index(23,4), 6),
            (4, to_tile_index(24,4), 6),
        ]

    def shuffle(self):
        backgrounds = list(set(val for areaid, posindex, val in self.original_locations))
        new_backgrounds = list(backgrounds)
        if self.no_laggy_backgrounds:
            new_backgrounds = [b for b in new_backgrounds if b not in LAGGY_BACKGROUNDS]
        if self.no_difficult_backgrounds:
            new_backgrounds = [b for b in new_backgrounds if b not in DIFFICULT_BACKGROUNDS]
        while len(new_backgrounds) < len(backgrounds):
            new_backgrounds += new_backgrounds

        random.shuffle(new_backgrounds)
        allocation = dict(zip(backgrounds, new_backgrounds))

        stored_datas = self.stored_datas
        for areaid, posindex, val in self.original_locations:
            # Fix for pyramid super-trampoline bug
            if areaid == 1 and posindex == to_tile_index(16,11): continue

            # Fix for Alius3 Noah becoming the Noah1 boss fight bug
            if areaid == 8 and posindex == to_tile_index(17,7): continue
            if areaid == 8 and posindex == to_tile_index(18,7): continue
            # Fix for Noah1 becoming the Alius3 Noah boss fight bug
            if areaid == 8 and posindex == to_tile_index(18,5) and allocation[val] == 9: continue

            # Fix for early sysint computer bug
            if areaid == 4 and posindex == to_tile_index(17,16): continue

            # Fix for bug where you can't enter warps if it has computer room background.
            if allocation[val] == 64:
                # plurkwood warp from starting forest
                if areaid == 0 and posindex == to_tile_index(8,4): continue
                # warp to exit plurkwood
                if areaid == 6 and posindex == to_tile_index(9,3): continue
                # warp to exit sysint
                if areaid == 9 and posindex == to_tile_index(14,8): continue

            # Fix for Evernight dark passage background bugs:
            if allocation[val] == 56:
                # Saya escapes her boss fight
                if areaid == 4 and posindex == to_tile_index(21,3): continue
                if areaid == 4 and posindex == to_tile_index(22,3): continue
                if areaid == 4 and posindex == to_tile_index(23,3): continue
                if areaid == 4 and posindex == to_tile_index(24,3): continue
                
                # Vanilla doesn't spawn at all
                if areaid == 2 and posindex == to_tile_index(14,4): continue
                
                # UPRPRC bombers can't bomb in pyramid
                if areaid == 1 and posindex == to_tile_index(14,13): continue
                if areaid == 1 and posindex == to_tile_index(15,13): continue
                if areaid == 1 and posindex == to_tile_index(18,13): continue
                if areaid == 1 and posindex == to_tile_index(17,13): continue
                
                # UPRPRC bombers can't bomb in cocoa cave
                if areaid == 0 and posindex == to_tile_index(13,11): continue
                if areaid == 0 and posindex == to_tile_index(14,11): continue
                if areaid == 0 and posindex == to_tile_index(15,11): continue
                if areaid == 0 and posindex == to_tile_index(16,11): continue
                if areaid == 0 and posindex == to_tile_index(17,11): continue
                if areaid == 0 and posindex == to_tile_index(18,11): continue
                if areaid == 0 and posindex == to_tile_index(19,11): continue
                if areaid == 0 and posindex == to_tile_index(20,11): continue
                
                # UPRPRC bombers can't bomb in volcanic caverns
                if areaid == 7 and posindex == to_tile_index(7,4): continue
                if areaid == 7 and posindex == to_tile_index(8,4): continue
                if areaid == 7 and posindex == to_tile_index(9,4): continue
                
                # Night forest UPRPRC fight doesn't work properly (unconfirmed)
                if areaid == 0 and posindex == to_tile_index(7,6): continue
                if areaid == 0 and posindex == to_tile_index(8,6): continue
                if areaid == 0 and posindex == to_tile_index(9,6): continue

            stored_datas[areaid].tiledata_roombg[posindex] = allocation[val]


class RoomColorShuffler(object):
    def __init__(self, stored_datas):
        self.stored_datas = stored_datas
        original_locations = []

        filter_function = self.filter_function
        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, val)
                for posindex, val in enumerate(data.tiledata_roomcolor) if filter_function(val))

        self.original_locations = original_locations

    def filter_function(self, val):
        # don't shuffle DLC colors
        # don't shuffle library color (24) because it deletes trampolines
        # don't shuffle FC2/HoM colors (6,30) because they do weird things to bosses
        return val <= 31 and val not in (0,5,6,24,30) # DLC: (0,5,32,34,55)

    def shuffle(self):
        backgrounds = list(set(val for areaid, posindex, val in self.original_locations))
        new_backgrounds = list(backgrounds)
        random.shuffle(new_backgrounds)
        allocation = dict(zip(backgrounds, new_backgrounds))

        stored_datas = self.stored_datas
        for areaid, posindex, val in self.original_locations:
            stored_datas[areaid].tiledata_roomcolor[posindex] = allocation[val]
