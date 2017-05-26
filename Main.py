from BaseClasses import World, CollectionState, Item
from Regions import create_regions
from EntranceShuffle import link_entrances
from Rom import patch_rom
from Rules import set_rules
from Dungeons import fill_dungeons
from Items import ItemFactory
import random
import time
import logging
import argparse
import os

__version__ = '0.2-dev'

logic_hash = [182, 244, 92, 144, 149, 200, 93, 183, 124, 169, 226, 46, 111, 163, 5, 193, 13, 112, 125, 101, 128, 84, 31, 67, 107, 94, 184, 100, 189, 18, 8, 171,
              142, 57, 173, 38, 37, 211, 253, 131, 98, 239, 167, 116, 32, 186, 70, 148, 66, 151, 143, 86, 59, 83, 16, 51, 240, 152, 60, 242, 190, 117, 76, 122,
              15, 221, 62, 39, 174, 177, 223, 34, 150, 50, 178, 238, 95, 219, 10, 162, 222, 0, 165, 202, 74, 36, 206, 209, 251, 105, 175, 135, 121, 88, 214, 247,
              154, 161, 71, 19, 85, 157, 40, 96, 225, 27, 230, 49, 231, 207, 64, 35, 249, 134, 132, 108, 63, 24, 4, 127, 255, 14, 145, 23, 81, 216, 113, 90, 194,
              110, 65, 229, 43, 1, 11, 168, 147, 103, 156, 77, 80, 220, 28, 227, 213, 198, 172, 79, 75, 140, 44, 146, 188, 17, 6, 102, 56, 235, 166, 89, 218, 246,
              99, 78, 187, 126, 119, 196, 69, 137, 181, 55, 20, 215, 199, 130, 9, 45, 58, 185, 91, 33, 197, 72, 115, 195, 114, 29, 30, 233, 141, 129, 155, 159, 47,
              224, 236, 21, 234, 191, 136, 104, 87, 106, 26, 73, 250, 248, 228, 48, 53, 243, 237, 241, 61, 180, 12, 208, 245, 232, 192, 2, 7, 170, 123, 176, 160, 201,
              153, 217, 252, 158, 25, 205, 22, 133, 254, 138, 203, 118, 210, 204, 82, 97, 52, 164, 68, 139, 120, 109, 54, 3, 41, 179, 212, 42]


def main(args, seed=None):
    start = time.clock()

    # initialize the world
    world = World(args.shuffle, args.logic, args.mode, args.difficulty, args.goal, not args.nodungeonitems)
    logger = logging.getLogger('')

    if seed is None:
        random.seed(None)
        world.seed = random.randint(0, 999999999)
    else:
        world.seed = seed
    random.seed(world.seed)

    world.spoiler += 'ALttP Entrance Randomizer Version %s  -  Seed: %s\n\n' % (__version__, world.seed)
    world.spoiler += 'Logic: %s  Mode: %s  Goal: %s  Entrance Shuffle: %s  Filling Algorithm: %s\n\n' % (args.logic, args.mode, args.goal, args.shuffle, args.algorithm)  # todo

    logger.info(world.spoiler)

    create_regions(world)

    logger.info('Shuffling the World about.')

    world.spoiler += link_entrances(world)

    logger.info('Calculating Access Rules.')

    world.spoiler += set_rules(world)

    logger.info('Generating Item Pool and placing Dungeon Items.')

    world.spoiler += generate_itempool(world)

    logger.info('Fill the world.')

    if args.algorithm == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    else:
        distribute_items(world)
    world.spoiler += print_location_spoiler(world)

    logger.info('Calculating playthrough.')

    world.spoiler += create_playthrough(world)

    logger.info('Patching ROM.')

    rom = bytearray(open(args.rom, 'rb').read())
    patched_rom = patch_rom(world, rom, logic_hash, args.quickswap, args.heartbeep)

    outfilebase = 'ER_%s_%s_%s_%s' % (world.mode, world.goal, world.shuffle, world.seed)

    with open('%s.sfc' % outfilebase, 'wb') as outfile:
        outfile.write(patched_rom)
    if args.create_spoiler:
        with open('%s_Spoiler.txt' % outfilebase, 'w') as outfile:
            outfile.write(world.spoiler)

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s' % (time.clock() - start))

    return world


def distribute_items(world):
    # get list of locations to fill in
    fill_locations = world.get_unfilled_locations()
    random.shuffle(fill_locations)

    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool

    progress_done = False

    while itempool and fill_locations:
        candidate_item_to_place = None
        item_to_place = None
        for item in itempool:
            if progress_done:
                item_to_place = item
                break
            if item.advancement:
                candidate_item_to_place = item
                if world.unlocks_new_location(item):
                    item_to_place = item
                    break

        if item_to_place is None:
            # check if we can reach all locations and that is why we find no new locations to place
            if len(world.get_reachable_locations()) == len(world.get_locations()):
                progress_done = True
                continue
            # we might be in a situation where all new locations require multiple items to reach. If that is the case, just place any advancement item we've found and continue trying
            if candidate_item_to_place is not None:
                item_to_place = candidate_item_to_place
            else:
                # we placed all available progress items. Maybe the game can be beaten anyway?
                if world.can_beat_game():
                    logging.getLogger('').warning('Not all locations reachable. Game beatable anyway.')
                    progress_done = True
                    continue
                raise RuntimeError('No more progress items left to place.')

        spot_to_fill = None
        for location in fill_locations:
            if world.state.can_reach(location) and location.item_rule(item_to_place):
                spot_to_fill = location
                break

        if spot_to_fill is None:
            # we filled all reachable spots. Maybe the game can be beaten anyway?
            if world.can_beat_game():
                logging.getLogger('').warning('Not all items placed. Game beatable anyway.')
                break
            raise RuntimeError('No more spots to place %s' % item_to_place)

        world.push_item(spot_to_fill, item_to_place, True)
        itempool.remove(item_to_place)
        fill_locations.remove(spot_to_fill)

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s' % (itempool, fill_locations))


def flood_items(world):
    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool
    progress_done = False

    # fill world from top of itempool while we can
    while not progress_done:
        location_list = world.get_unfilled_locations()
        random.shuffle(location_list)
        spot_to_fill = None
        for location in location_list:
            if world.state.can_reach(location):
                spot_to_fill = location
                break

        if spot_to_fill:
            item = itempool.pop(0)
            world.push_item(spot_to_fill, item, True)
            continue

        # ran out of spots, check if we need to step in and correct things
        if len(world.get_reachable_locations()) == len(world.get_locations()):
            progress_done = True
            continue

        # need to place a progress item instead of an already placed item, find candidate
        item_to_place = None
        candidate_item_to_place = None
        for item in itempool:
            if item.advancement:
                candidate_item_to_place = item
                if world.unlocks_new_location(item):
                    item_to_place = item
                    break

        # we might be in a situation where all new locations require multiple items to reach. If that is the case, just place any advancement item we've found and continue trying
        if item_to_place is None:
            if candidate_item_to_place is not None:
                item_to_place = candidate_item_to_place
            else:
                raise RuntimeError('No more progress items left to place.')

        # find item to replace with progress item
        location_list = world.get_reachable_locations()
        random.shuffle(location_list)
        for location in location_list:
            if location.item is not None and not location.item.advancement and not location.item.key and 'Map' not in location.item.name and 'Compass' not in location.item.name:
                # safe to replace
                replace_item = location.item
                replace_item.location = None
                itempool.append(replace_item)
                world.push_item(location, item_to_place, True)
                itempool.remove(item_to_place)
                break


def generate_itempool(world):
    if world.difficulty != 'normal' or world.goal not in ['ganon', 'pedestal', 'dungeons'] or world.mode not in ['open', 'standard']:
        raise NotImplementedError('Not supported yet')

    world.push_item('Ganon', ItemFactory('Triforce'), False)

    # set up item pool
    world.itempool = ItemFactory(['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6 + ['Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] +
                                 ['Progressive Armor'] * 2 + ['Progressive Shield'] * 3 + ['Progressive Sword'] * 3 + ['Progressive Glove'] * 2 +
                                 ['Bottle'] * 4 +
                                 ['Bombos', 'Book of Mudora', 'Blue Boomerang', 'Bow', 'Bug Catching Net', 'Cane of Byrna', 'Cane of Somaria',
                                  'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp', 'Cape', 'Magic Powder',
                                  'Red Boomerang', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Silver Arrows'] +
                                 ['Single Arrow', 'Sanctuary Heart Container', 'Rupees (100)'] + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24 +
                                 ['Rupees (50)'] * 7 + ['Rupees (5)'] * 4 + ['Rupee (1)'] * 2 + ['Rupees (300)'] * 4 + ['Rupees (20)'] * 28 +
                                 ['Arrows (10)'] * 4 + ['Bombs (3)'] * 10)

    if world.mode == 'standard':
        world.push_item('Uncle', ItemFactory('Progressive Sword'))
    else:
        world.itempool.append(ItemFactory('Progressive Sword'))

    # provide mirror and pearl so you can avoid fake DW/LW and do dark world exploration as intended by algorithm, for now
    if world.shuffle == 'insanity':
        world.push_item('[cave-040] Links House', ItemFactory('Magic Mirror'))
        world.push_item('[dungeon-C-1F] Sanctuary', ItemFactory('Moon Pearl'))
    else:
        world.itempool.extend(ItemFactory(['Magic Mirror', 'Moon Pearl']))

    if world.goal == 'pedestal':
        world.push_item('Altar', ItemFactory('Triforce'))
        items = list(world.itempool)
        random.shuffle(items)
        for item in items:
            if not item.advancement:
                # save to remove
                world.itempool.remove(item)
                break
                # ToDo what to do if EVERYTHING is a progress item?

    if random.randint(0, 3) == 0:
        world.itempool.append(ItemFactory('Magic Upgrade (1/4)'))
    else:
        world.itempool.append(ItemFactory('Magic Upgrade (1/2)'))

    # distribute crystals
    crystals = ItemFactory(['Green Pendant', 'Red Pendant', 'Blue Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7'])
    crystal_locations = [world.get_location('Armos - Pendant'), world.get_location('Lanmolas - Pendant'), world.get_location('Moldorm - Pendant'), world.get_location('Helmasaur - Crystal'),
                         world.get_location('Blind - Crystal'), world.get_location('Mothula - Crystal'), world.get_location('Arrghus - Crystal'), world.get_location('Kholdstare - Crystal'),
                         world.get_location('Vitreous - Crystal'), world.get_location('Trinexx - Crystal')]
    random.shuffle(crystals)
    for location, crystal in zip(crystal_locations, crystals):
        world.push_item(location, crystal, False)

    # shuffle medallions
    mm_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    tr_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    world.required_medallions = (mm_medallion, tr_medallion)

    # push dungeon items
    fill_dungeons(world)

    return 'Misery Mire Medallion: %s\nTurtle Rock Medallion: %s\n\n' % (mm_medallion, tr_medallion)


def copy_world(world):
    # ToDo: Not good yet
    ret = World(world.shuffle, world.logic, world.mode, world.difficulty, world.goal, world.place_dungeon_items)
    ret.required_medallions = list(world.required_medallions)
    ret.agahnim_fix_required = world.agahnim_fix_required
    ret.swamp_patch_required = world.swamp_patch_required
    create_regions(ret)

    # connect copied world
    for region in world.regions:
        for entrance in region.entrances:
            ret.get_entrance(entrance.name).connect(ret.get_region(region.name))

    set_rules(ret)

    # fill locations
    for location in world.get_locations():
        if location.item is not None:
            item = Item(location.item.name, location.item.advancement, location.item.key)
            ret.get_location(location.name).item = item
            item.location = ret.get_location(location.name)

    # copy remaining itempool. No item in itempool should have an assigned location
    for item in world.itempool:
        ret.itempool.append(Item(item.name, item.advancement, item.key))

    # copy progress items in state
    ret.state.prog_items = list(world.state.prog_items)

    return ret


def create_playthrough(world):
    # create a copy as we will modify it
    world = copy_world(world)

    # get locations containing progress items
    prog_locations = [location for location in world.get_locations() if location.item is not None and location.item.advancement]

    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = list(prog_locations)
    while sphere_candidates:
        sphere = []
        # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
        for location in sphere_candidates:
            if state.can_reach(location):
                sphere.append(location)

        for location in sphere:
            sphere_candidates.remove(location)
            state.collect(location.item)

        collection_spheres.append(sphere)

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each range of influence to the bare minimum required inside it
    for sphere in reversed(collection_spheres):
        to_delete = []
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            old_item = location.item
            location.item = None
            state.remove(old_item)
            world._item_cache = {}  # need to invalidate
            if world.can_beat_game():
                to_delete.append(location)
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        for location in to_delete:
            sphere.remove(location)

    # we are now down to just the required progress items in collection_spheres in a minimum number of spheres. As a cleanup, we right trim empty spheres (can happen if we have multiple triforces)
    collection_spheres = [sphere for sphere in collection_spheres if sphere]

    # we can finally output our playthrough
    return 'Playthrough:\n' + ''.join(['%s: {\n%s}\n' % (i + 1, ''.join(['  %s: %s\n' % (location, location.item) for location in sphere])) for i, sphere in enumerate(collection_spheres)]) + '\n'


def print_location_spoiler(world):
    return 'Locations:\n\n' + '\n'.join(['%s: %s' % (location, location.item if location.item is not None else 'Nothing') for location in world.get_locations()]) + '\n\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--create_spoiler', help='Output a Spoiler File', action='store_true')
    parser.add_argument('--logic', default='noglitches', const='noglitches', nargs='?', choices=['noglitches', 'minorglitches'],
                        help='Select Enforcement of Item Requirements. Minor Glitches may require Fake Flippers, Bunny Revival and Dark Room Navigation.')
    parser.add_argument('--mode', default='open', const='open', nargs='?', choices=['standard', 'open'],
                        help='Select game mode. Standard fixes Hyrule Castle Secret Entrance and Front Door, but may lead to weird rain state issues if you exit through the Hyrule Castle side exits before rescuing Zelda in a full shuffle.')
    parser.add_argument('--goal', default='ganon', const='ganon', nargs='?', choices=['ganon', 'pedestal', 'dungeons'],
                        help='Select completion goal. Pedestal places a second Triforce at the Master Sword Pedestal, the playthrough may still deem Ganon to be the easier goal. All dungeons is not enforced ingame but considered in the rules.')
    parser.add_argument('--difficulty', default='normal', const='normal', nargs='?', choices=['normal'], help='Select game difficulty. Affects available itempool.')
    parser.add_argument('--algorithm', default='regular', const='regular', nargs='?', choices=['regular', 'flood'],
                        help='Select item filling algorithm. Regular is the ordinary VT algorithm. Flood pushes out items starting from Link\'s House and is slightly biased to placing progression items with less restrictions.')
    parser.add_argument('--shuffle', default='full', const='full', nargs='?', choices=['default', 'simple', 'restricted', 'full', 'madness', 'insanity', 'dungeonsfull', 'dungeonssimple'],
                        help='Select Entrance Shuffling Algorithm. Default is the Vanilla layout. \n'
                             'Simple shuffles Dungeon Entrances/Exits between each other and keeps all 4-entrance dungeons confined to one location. All caves outside of death mountain are shuffled in pairs.\n'
                             'Restricted uses Dungeons shuffling from Simple but freely connects remaining entrances.\n'
                             'Full mixes cave and dungeon entrances freely.\n'
                             'Madness decouples entrances and exits from each other and shuffles them freely, only ensuring that no fake Light/Dark World happens and all locations are reachable.\n'
                             'Insanity is Madness without the world restrictions. Mirror and Pearl are provided early to ensure Filling algorithm works properly. Deal with Fake LW/DW at your discretion. Experimental.\n'
                             'The dungeon variants only mix up dungeons and keep the rest of the overworld vanilla.')
    parser.add_argument('--rom', default='Base_Rom.sfc', help='Path to a VT21 standard normal difficulty rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--count', help='Use to batch generate multiple seeds with same settings. If --seed is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with --seed given will produce the same 10 (different) roms each time).', type=int)
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--nodungeonitems', help='Remove Maps and Compasses from Itempool, replacing them by empty slots.', action='store_true')
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?', choices=['normal', 'half', 'quarter', 'off'],
                        help='Select the rate at which the heart beep sound is played at low health.')
    args = parser.parse_args()

    if not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if args.count is not None:
        seed = args.seed
        for i in range(args.count):
            main(seed=seed, args=args)
            seed = random.randint(0, 999999999)
    else:
        main(seed=args.seed, args=args)
