import argparse, random, sys
from utility import *
from generator import Generator
from dataparser import RandomizerData
import mapfileio

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
    #pre_modify_map_data(mod, apply_fixes=apply_fixes, open_mode=open_mode, shuffle_music=shuffle_music, shuffle_backgrounds=shuffle_backgrounds, no_laggy_backgrounds=no_laggy_backgrounds, no_difficult_backgrounds=no_difficult_backgrounds, super_attack_mode=super_attack_mode, hyper_attack_mode=hyper_attack_mode)
    #apply_item_specific_fixes(mod, assigned_locations)
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
