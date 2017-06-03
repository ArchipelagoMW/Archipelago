from BaseClasses import World, CollectionState, Item
from Regions import create_regions
from EntranceShuffle import link_entrances
from Rom import patch_rom
from Rules import set_rules
from Items import ItemFactory
import random
import time
import logging
import argparse
import os
import hashlib

__version__ = '0.1-dev'

logic_hash = [182, 244, 144, 92, 149, 200, 93, 183, 124, 169, 226, 46, 111, 163, 5, 193, 13, 112, 125, 101, 128, 84, 31, 67, 107, 94, 184, 100, 189, 18, 8, 171,
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
    world = World('vanilla', 'noglitches', 'standard', 'normal', 'ganon', False)
    logger = logging.getLogger('')

    hasher = hashlib.md5()
    with open(args.plando, 'rb') as plandofile:
        buf = plandofile.read()
        hasher.update(buf)
    world.seed = int(hasher.hexdigest(), 16) % 1000000000

    random.seed(world.seed)

    world.spoiler += 'ALttP Plandomizer Version %s  -  Seed: %s\n\n' % (__version__, args.plando)

    logger.info(world.spoiler)

    create_regions(world)

    world.spoiler += link_entrances(world)

    logger.info('Calculating Access Rules.')

    world.spoiler += set_rules(world)

    logger.info('Fill the world.')

    world.spoiler += fill_world(world, args.plando)

    world.spoiler += print_location_spoiler(world)

    logger.info('Calculating playthrough.')

    world.spoiler += create_playthrough(world)

    logger.info('Patching ROM.')

    if args.sprite is not None:
        sprite = bytearray(open(args.sprite, 'rb').read())
    else:
        sprite = None

    rom = bytearray(open(args.rom, 'rb').read())
    patched_rom = patch_rom(world, rom, logic_hash, args.quickswap, args.heartbeep, sprite)

    outfilebase = 'Plando_%s_%s' % (os.path.splitext(os.path.basename(args.plando))[0], world.seed)

    with open('%s.sfc' % outfilebase, 'wb') as outfile:
        outfile.write(patched_rom)
    if args.create_spoiler:
        with open('%s_Spoiler.txt' % outfilebase, 'w') as outfile:
            outfile.write(world.spoiler)

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s' % (time.clock() - start))

    return world


def fill_world(world, plando):
    mm_medallion = 'Ether'
    tr_medallion = 'Quake'
    logger = logging.getLogger('')
    with open(plando, 'r') as plandofile:
        for line in plandofile.readlines():
            if ':' in line:
                line = line.lstrip()

                if line.startswith('#'):
                    continue
                if line.startswith('!'):
                    if line.startswith('!mm_medallion'):
                        _, medallionstr = line.split(':', 1)
                        mm_medallion = medallionstr.strip()
                    elif line.startswith('!tr_medallion'):
                        _, medallionstr = line.split(':', 1)
                        tr_medallion = medallionstr.strip()
                    elif line.startswith('!mode'):
                        _, modestr = line.split(':', 1)
                        world.mode = modestr.strip()
                    elif line.startswith('!logic'):
                        _, logicstr = line.split(':', 1)
                        world.logic = logicstr.strip()
                    elif line.startswith('!goal'):
                        _, goalstr = line.split(':', 1)
                        world.goal = goalstr.strip()
                    continue

                locationstr, itemstr = line.split(':', 1)
                location = world.get_location(locationstr.strip())
                if location is None:
                    logger.warn('Unknown location: %s' % locationstr)
                    continue
                else:
                    item = ItemFactory(itemstr.strip())
                    if item is not None:
                        world.push_item(location, item)

    world.required_medallions = (mm_medallion, tr_medallion)
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

    # if we do pedestal%, ganon should not be a viable option as far as the playthrough is concerned
    if world.goal == 'pedestal':
        world.get_location('Ganon').item = None

    # get locations containing progress items
    prog_locations = [location for location in world.get_locations() if location.item is not None and location.item.advancement]

    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = list(prog_locations)
    logging.getLogger('').debug('Building up collection spheres.')
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

        logging.getLogger('').debug('Calculated sphere %i, containing %i of %i progress items.' % (len(collection_spheres), len(sphere), len(prog_locations)))

        if not sphere:
            logging.getLogger('').debug('The following items could not be placed: %s' % ['%s at %s' % (location.item.name, location.name) for location in sphere_candidates])
            raise RuntimeError('Not all progression items reachable. Something went terribly wrong here.')

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each range of influence to the bare minimum required inside it
    for sphere in reversed(collection_spheres):
        to_delete = []
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            logging.getLogger('').debug('Checking if %s is required to beat the game.' % location.item.name)
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
    parser.add_argument('--rom', default='Base_Rom.sfc', help='Path to a VT21 standard normal difficulty rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?', choices=['normal', 'half', 'quarter', 'off'],
                        help='Select the rate at which the heart beep sound is played at low health.')
    parser.add_argument('--sprite', help='Path to a sprite sheet to use for Link. Needs to be in binary format and have a length of 0x7000 (28672) bytes.')
    parser.add_argument('--plando', help='Filled out template to use for setting up the rom.')
    args = parser.parse_args()

    # ToDo: Validate files further than mere existance
    if not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        exit(1)
    if not os.path.isfile(args.plando):
        input('Could not find Plandomizer distribution at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.plando)
        exit(1)
    if args.sprite is not None and not os.path.isfile(args.rom):
        input('Could not find link sprite sheet at given location. \nPress Enter to exit.' % args.sprite)
        exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    main(args=args)
