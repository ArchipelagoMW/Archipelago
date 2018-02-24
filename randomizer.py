import argparse, random, sys
from utility import *
from generator import Generator
from dataparser import RandomizerData
import mapfileio
import musicrandomizer
import backgroundrandomizer
import converter.diffgenerator as diffgenerator

VERSION_STRING = '{PLACEHOLDER_VERSION}'

def parse_args():
    args = argparse.ArgumentParser(description='Rabi-Ribi Randomizer - %s' % VERSION_STRING)
    args.add_argument('--version', action='store_true', help='Print Randomizer Version')
    args.add_argument('-output_dir', default='generated_maps', help='Output directory for generated maps')
    args.add_argument('-config_file', default='config.txt', help='Config file to use')
    args.add_argument('-seed', default=None, type=str, help='Random seed')
    args.add_argument('--no-write', dest='write', default=True, action='store_false', help='Flag to disable map generation, and do only map analysis')
    args.add_argument('--no-fixes', dest='apply_fixes', default=True, action='store_false', help='Flag to disable randomizer-specific map fixes')
    args.add_argument('--reset', action='store_true', help='Reset maps by copying the original maps to the output directory.')
    args.add_argument('--hash', action='store_true', help='Generate a hash of the maps in the output directory.')
    args.add_argument('--check-for-updates', action='store_true', help='Check for the latest version of randomizer.')
    args.add_argument('--check-branch', action='store_true', help='Displays which branch the randomizer is currently on (D or M).')
    args.add_argument('--shuffle-music', action='store_true', help='Shuffles the music in the map.')
    args.add_argument('--shuffle-backgrounds', action='store_true', help='Shuffles the backgrounds in the map.')
    args.add_argument('--shuffle-map-transitions', action='store_true', help='Shuffles map transitions between maps.')
    args.add_argument('--shuffle-gift-items', action='store_true', help='Shuffles certain gift items in the maps.')
    args.add_argument('--no-laggy-backgrounds', action='store_true', help='Don\'t include laggy backgrounds in background shuffle.')
    args.add_argument('--no-difficult-backgrounds', action='store_true', help='Don\'t include backgrounds in background shuffle that interfere with visibility.')
    args.add_argument('--super-attack-mode', action='store_true', help='Start the game with a bunch of attack ups, so you do lots more damage.')
    args.add_argument('--hyper-attack-mode', action='store_true', help='Like Super Attack Mode, but with 35 attack ups.')
    args.add_argument('--open-mode', action='store_true', help='Removes prologue triggers that restrict exploration.')
    args.add_argument('--hide-unreachable', action='store_true', help='Hide list of unreachable items. Affects seed.')
    args.add_argument('--hide-difficulty', action='store_true', help='Hide difficulty rating. Affects seed.')
    args.add_argument('--egg-goals', action='store_true', help='Egg goals mode. Hard-to-reach items are replaced with easter eggs. All other eggs are removed from the map.')
    args.add_argument('-extra-eggs', default=0, type=int, help='Number of extra randomly-chosen eggs for egg-goals mode (in addition to the hard-to-reach eggs)')

    return args.parse_args(sys.argv[1:])


def apply_item_specific_fixes(mod, allocation):
    item_at_location = allocation.item_at_item_location

    if is_egg(item_at_location['PURE_LOVE']):
        data = mod.stored_datas[1]
        data.tiledata_event[xy_to_index(404,12)] = 3

    if is_egg(item_at_location['ATK_UP_SNOWLAND']):
        data = mod.stored_datas[3]
        data.tiledata_event[xy_to_index(93,119)] = 3

    if is_egg(item_at_location['HP_UP_NORTH_FOREST']):
        data = mod.stored_datas[0]
        data.tiledata_map[xy_to_index(271,51)] = 0
        data.tiledata_tiles1[xy_to_index(271,51)] = 0

def apply_fixes_for_randomizer(areaid, data):
    if areaid == 0:
        # Remove save point and autosave point before Cocoa1
        for y in range(84,88):
            data.tiledata_event[xy_to_index(358,y)] = 0
            data.tiledata_event[xy_to_index(363,y)] = 0
            data.tiledata_event[xy_to_index(364,y)] = 0
        for y in range(85,88):
            data.tiledata_event[xy_to_index(361,y)] = 0
            data.tiledata_event[xy_to_index(365,y)] = 0

        # Add autosave point at ledge above Cocoa1
        data.tiledata_event[xy_to_index(378,80)] = 42
        data.tiledata_event[xy_to_index(378,81)] = 42
        data.tiledata_event[xy_to_index(380,80)] = 44
        data.tiledata_event[xy_to_index(380,81)] = 44
        data.tiledata_event[xy_to_index(376,80)] = 44
        data.tiledata_event[xy_to_index(376,81)] = 44
        data.tiledata_event[xy_to_index(376,82)] = 44

    if areaid == 1:
        # Remove trampoline at crisis boost location
        data.tiledata_event[xy_to_index(246,63)] = 0
        data.tiledata_event[xy_to_index(246,64)] = 0

    if areaid == 4:
        # Remove save point at slide location in lab
        for y in range(185,189):
            data.tiledata_event[xy_to_index(309,y)] = 0
        for y in range(186,189):
            data.tiledata_event[xy_to_index(310,y)] = 0

    if areaid == 8:
        # Remove autosaves from warp destination
        data.tiledata_event = [0 if x==42 else x for x in data.tiledata_event]

def apply_open_mode_fixes(areaid, data):
    # Prologue triggers that prevent you from getting past many areas
    data.tiledata_event = [0 if x==300 else x for x in data.tiledata_event]

    if areaid == 0:
        # Trigger blocking going to beach from start
        data.tiledata_event = [0 if x==301 else x for x in data.tiledata_event]

def configure_shaft(mod, settings):
    events_list = []

    event_flag_set_list = []

    if settings.apply_fixes:
        # Turn on warp stones from the start
        event_flag_set_list += [(281,)]

    if settings.shuffle_gift_items:
        # Disable event where miriam gives you speed boost and bunny strike.
        event_flag_set_list += [(374,), (378,)]
        # The P.Hairpin event is (453,), but I remove it from the maps in the diff instead of disabling it.

    if len(event_flag_set_list) > 0:
        events_list += [(525,)] + event_flag_set_list + [(524,)]

    if settings.open_mode:
        # Add ribbon
        events_list.append((558, 5008, 5001))

    # Add attack ups
    if settings.hyper_attack_mode:
        for i in range(0,30):
            events_list.append((558, 5223-i, 5001))
        print('Hyper attack mode applied')
    elif settings.super_attack_mode:
        for i in range(0,20):
            events_list.append((558, 5223-i, 5001))
        print('Super attack mode applied')

    # Build shaft only if there is something to build.
    if len(events_list) > 0:
        for areaid, data in mod.stored_datas.items():
            build_start_game_shaft(areaid, data, events_list)


def build_start_game_shaft(areaid, data, events_list):
    # area 0 only.
    if areaid != 0: return

    MAX_EVENTS = 37
    EVENT_COUNT = len(events_list)
    if EVENT_COUNT > MAX_EVENTS:
        fail('Too many events in start game shaft: %d/%d' % (EVENT_COUNT, MAX_EVENTS))
    
    # EV_MOVEDOWN event to move erina down to start position
    data.tiledata_event[xy_to_index(111,43)] = 554

    # Place events in shaft
    for i, ev_tuple in enumerate(events_list):
        y = 43 - EVENT_COUNT + i
        for dx, ev in enumerate(ev_tuple):
            data.tiledata_event[xy_to_index(111+dx,y)] = ev

    # Remove old start event
    data.tiledata_event[xy_to_index(113,98)] = 0
    # Place new start event
    data.tiledata_event[xy_to_index(111,42-EVENT_COUNT)] = 34

    # Add collision data
    data.tiledata_map[xy_to_index(110,44)] = 1
    data.tiledata_map[xy_to_index(111,44)] = 1
    data.tiledata_map[xy_to_index(112,44)] = 1
    for i in range(0,EVENT_COUNT+5):
        y = 43-i
        data.tiledata_map[xy_to_index(110,y)] = 1
        data.tiledata_map[xy_to_index(112,y)] = 1
    data.tiledata_map[xy_to_index(111,43-EVENT_COUNT-4)] = 1

    # Blanket with black graphical tiles
    for y in range(0,45):
        for x in range(100,120):
            data.tiledata_tiles1[xy_to_index(x,y)] = 33

    # Change room type and background
    for y in range(0,4):
        data.tiledata_roombg[to_tile_index(5,y)] = 56
        data.tiledata_roomtype[to_tile_index(5,y)] = 3


def apply_diff_patch_fixes(mod, diff_patch_files):
    def apply_diff(arrays, diffs):
        for layer_name, diff in diffs.items():
            array = arrays[layer_name]
            for index, coords, value in diff:
                array[index] = value

    area_arrays = {}
    for areaid, stored_data in mod.stored_datas.items():
        area_arrays[areaid] = {
            'roomtype': stored_data.tiledata_roomtype,
            'roomcolor': stored_data.tiledata_roomcolor,
            'roombg': stored_data.tiledata_roombg,
            'collision': stored_data.tiledata_map,
            'event': stored_data.tiledata_event,
            'tiles0': stored_data.tiledata_tiles0,
            'tiles1': stored_data.tiledata_tiles1,
            'tiles2': stored_data.tiledata_tiles2,
            'tiles3': stored_data.tiledata_tiles3,
            'tiles4': stored_data.tiledata_tiles4,
            'tiles5': stored_data.tiledata_tiles5,
            'tiles6': stored_data.tiledata_tiles6,
        }

    for diff_path_file in diff_patch_files:
        diff_data = diffgenerator.DiffData(diff_path_file)
        for areaid, diffs in diff_data.area_diffs.items():
            apply_diff(area_arrays[areaid], diffs)

def pre_modify_map_data(mod, settings, diff_patch_files):
    # apply rando fixes
    if settings.apply_fixes:
        for areaid, data in mod.stored_datas.items():
            apply_fixes_for_randomizer(areaid, data)
        diff_patch_files += [
            './maptemplates/event_warps/ew_cicini_to_ravine.txt',
            './maptemplates/event_warps/ew_forest_to_beach.txt',
            './maptemplates/event_warps/ew_town_to_riverbank.txt',
        ]
        print('Map fixes applied')

    if settings.open_mode:
        for areaid, data in mod.stored_datas.items():
            apply_open_mode_fixes(areaid, data)
        print('Open mode applied')

    # Note: because musicrandomizer requires room color info, the music
    # must be shuffled before the room colors!

    if settings.shuffle_music:
        musicrandomizer.shuffle_music(mod.stored_datas)

    if settings.shuffle_backgrounds:
        backgroundrandomizer.shuffle_backgrounds(mod.stored_datas, settings.no_laggy_backgrounds, settings.no_difficult_backgrounds)

    # Add shaft if needed
    configure_shaft(mod, settings)

    # Apply map patches from list of patches. We apply this only after everything else has been applied.
    apply_diff_patch_fixes(mod, diff_patch_files)
    print('Map patches applied')


def apply_map_transition_shuffle(mod, data, settings, allocation):
    events_2d_dict = {}
    for areaid, tiledata in mod.stored_datas.items():
        tiledata_event = tiledata.tiledata_event
        events_2d_dict[areaid] = [tiledata_event[i:i+200] for i in range(0,len(tiledata_event),200)]

    def set_target_in_map(transition, area_target, entry_target):
        events_2d = events_2d_dict[transition.area_current]
        tiledata_event = mod.stored_datas[transition.area_current].tiledata_event
        x1,y1,w,h = transition.rect
        events_cropped = [x for row in events_2d[x1:x1+w] for x in row[y1:y1+h]]

        original_map_event = transition.area_target + 161
        original_entry_event = transition.entry_target + 200
        new_map_event = area_target + 161
        new_entry_event = entry_target + 200

        for i in (i for i,ev in enumerate(events_cropped) if ev == original_map_event):
            tiledata_event[xy_to_index(x1+i//h, y1+i%h)] = new_map_event

        for i in (i for i,ev in enumerate(events_cropped) if ev == original_entry_event):
            tiledata_event[xy_to_index(x1+i//h, y1+i%h)] = new_entry_event

    for rtr, ltr in zip(data.walking_right_transitions, allocation.walking_left_transitions):
        set_target_in_map(rtr, ltr.area_current, ltr.entry_current)
        set_target_in_map(ltr, rtr.area_current, rtr.entry_current)


def insert_items_into_map(mod, data, settings, allocation):
    name_to_id = dict((item.name, item.itemid) for item in data.items)
    name_to_id.update(data.additional_items)

    mod.clear_items()
    for original_item in data.items:
        item = original_item.copy()
        item_at_location = allocation.item_at_item_location[item.name]
        if item_at_location != None:
            #item.name = item_at_location
            item.itemid = name_to_id[item_at_location]
            mod.add_item(item)


def get_default_areaids():
    return list(range(10))


def run_randomizer(seed, source_dir, settings):
    if seed != None: random.seed(seed)
    randomizer_data = RandomizerData(settings)
    generator = Generator(randomizer_data, settings)
    allocation, analyzer = generator.generate_seed()
    print('done')

    areaids = get_default_areaids()
    if not mapfileio.exists_map_files(areaids, source_dir):
        fail('Maps not found in the directory %s! Place the original Rabi-Ribi maps '
             'in this directory for the randomizer to work.' % source_dir)

    mapfileio.grab_original_maps(source_dir, settings.output_dir)
    print('Maps copied...')
    mod = mapfileio.ItemModifier(areaids, source_dir=source_dir, no_load=True)
    pre_modify_map_data(mod, settings, allocation.map_modifications)
    apply_item_specific_fixes(mod, allocation)
    apply_map_transition_shuffle(mod, randomizer_data, settings, allocation)
    insert_items_into_map(mod, randomizer_data, settings, allocation)

    mod.save(settings.output_dir)
    print('Maps saved successfully to %s.' % settings.output_dir)

    hash_digest = hash_map_files(areaids, settings.output_dir)
    print('Hash: %s' % hash_digest)


if __name__ == '__main__':
    args = parse_args()
    source_dir='original_maps'

    if args.seed == None:
        seed = None
    else:
        seed = string_to_integer_seed('%s_ha:%s_hd:%s' % (args.seed, args.hide_unreachable, args.hide_difficulty))

    run_randomizer(seed, source_dir, args)
