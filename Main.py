from BaseClasses import World, CollectionState, Item
from Regions import create_regions
from EntranceShuffle import link_entrances
from Rom import patch_rom, LocalRom, JsonRom
from Rules import set_rules
from Dungeons import create_dungeons, fill_dungeons, fill_dungeons_restrictive
from Items import ItemFactory
from Fill import distribute_items_cutoff, distribute_items_staleness, distribute_items_restrictive, fill_restrictive, flood_items
from collections import OrderedDict
from ItemList import generate_itempool
import random
import time
import logging
import json

__version__ = '0.5.0-dev'

logic_hash = [217, 163, 29, 168, 46, 16, 56, 85, 183, 60, 44, 118, 98, 125, 64, 42, 161, 36, 131, 95, 247, 37, 127, 164, 47, 14, 19, 40, 96, 174, 67, 200,
              240, 119, 189, 4, 243, 155, 162, 32, 159, 186, 84, 180, 233, 99, 86, 242, 105, 26, 216, 196, 249, 214, 45, 70, 72, 224, 78, 87, 93, 182, 38, 248,
              173, 109, 30, 205, 73, 7, 193, 113, 241, 251, 52, 62, 171, 43, 41, 222, 138, 49, 145, 170, 103, 48, 21, 235, 74, 110, 176, 201, 253, 114, 68, 117,
              89, 207, 82, 54, 211, 61, 53, 88, 158, 226, 218, 177, 50, 213, 25, 9, 104, 140, 203, 169, 166, 116, 152, 2, 33, 149, 20, 220, 165, 108, 254, 179,
              107, 6, 22, 128, 69, 250, 231, 94, 92, 97, 252, 160, 172, 148, 237, 81, 77, 199, 35, 215, 184, 187, 136, 28, 129, 71, 210, 178, 102, 195, 198, 121,
              80, 135, 111, 151, 17, 223, 228, 238, 51, 147, 133, 79, 55, 12, 122, 1, 100, 120, 225, 202, 144, 63, 185, 208, 181, 204, 134, 142, 188, 146, 126, 27,
              153, 91, 191, 13, 157, 5, 59, 234, 83, 141, 23, 15, 18, 236, 137, 31, 143, 209, 229, 34, 132, 57, 75, 0, 230, 190, 90, 115, 76, 123, 197, 39,
              3, 206, 255, 112, 244, 167, 212, 154, 65, 124, 219, 221, 106, 139, 175, 10, 101, 239, 150, 227, 11, 246, 24, 156, 8, 130, 245, 66, 194, 58, 232, 192]


def main(args, seed=None):
    start = time.clock()

    # initialize the world
    world = World(args.shuffle, args.logic, args.mode, args.difficulty, args.timer, args.progressive, args.goal, args.algorithm, not args.nodungeonitems, args.beatableonly, args.shuffleganon, args.quickswap, args.fastmenu, args.disablemusic, args.keysanity)
    logger = logging.getLogger('')
    if seed is None:
        random.seed(None)
        world.seed = random.randint(0, 999999999)
    else:
        world.seed = int(seed)
    random.seed(world.seed)

    logger.info('ALttP Entrance Randomizer Version %s  -  Seed: %s\n\n' % (__version__, world.seed))

    create_regions(world)

    create_dungeons(world)

    logger.info('Shuffling the World about.')

    link_entrances(world)

    logger.info('Calculating Access Rules.')

    set_rules(world)

    logger.info('Generating Item Pool.')

    generate_itempool(world)

    logger.info('Placing Dungeon Items.')

    shuffled_locations = None
    if args.algorithm == 'vt26' or args.keysanity:
        shuffled_locations = world.get_unfilled_locations()
        random.shuffle(shuffled_locations)
        fill_dungeons_restrictive(world, shuffled_locations)
    else:
        fill_dungeons(world)

    logger.info('Fill the world.')

    if args.algorithm == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    elif args.algorithm == 'vt21':
        distribute_items_cutoff(world, 1)
    elif args.algorithm == 'vt22':
        distribute_items_cutoff(world, 0.66)
    elif args.algorithm == 'freshness':
        distribute_items_staleness(world)
    elif args.algorithm == 'vt25':
        distribute_items_restrictive(world, 0)
    elif args.algorithm == 'vt26':
        distribute_items_restrictive(world, random.randint(0, 15), shuffled_locations)
    elif args.algorithm == 'balanced':
        distribute_items_restrictive(world, random.randint(0, 15))

    logger.info('Calculating playthrough.')

    create_playthrough(world)

    logger.info('Patching ROM.')

    if args.sprite is not None:
        sprite = bytearray(open(args.sprite, 'rb').read())
    else:
        sprite = None

    outfilebase = 'ER_%s_%s-%s-%s%s_%s-%s%s%s%s%s%s_%s' % (world.logic, world.difficulty, world.mode, world.goal, "" if world.timer in ['none', 'display'] else "-" + world.timer, world.shuffle, world.algorithm, "-keysanity" if world.keysanity else "", "-progressives_" + world.progressive if world.progressive in ['off', 'random'] else "", "-fastmenu" if world.fastmenu else "", "-quickswap" if world.quickswap else "", "-shuffleganon" if world.shuffle_ganon else "", world.seed)

    if not args.suppress_rom:
        if args.jsonout:
            rom = JsonRom()
        else:
            rom = LocalRom(args.rom)
        patch_rom(world, rom, bytearray(logic_hash), args.heartbeep, sprite)
        if args.jsonout:
            print(json.dumps({'patch': rom.patches, 'spoiler': world.spoiler.to_json()}))
        else:
            rom.write_to_file(args.jsonout or '%s.sfc' % outfilebase)

    if args.create_spoiler and not args.jsonout:
        world.spoiler.to_file('%s_Spoiler.txt' % outfilebase)

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s' % (time.clock() - start))

    return world

def copy_world(world):
    # ToDo: Not good yet
    ret = World(world.shuffle, world.logic, world.mode, world.difficulty, world.timer, world.progressive, world.goal, world.algorithm, world.place_dungeon_items, world.check_beatable_only, world.shuffle_ganon, world.quickswap, world.fastmenu, world.disable_music, world.keysanity)
    ret.required_medallions = list(world.required_medallions)
    ret.swamp_patch_required = world.swamp_patch_required
    ret.ganon_at_pyramid = world.ganon_at_pyramid
    ret.treasure_hunt_count = world.treasure_hunt_count
    ret.treasure_hunt_icon = world.treasure_hunt_icon
    ret.sewer_light_cone = world.sewer_light_cone
    ret.light_world_light_cone = world.light_world_light_cone
    ret.dark_world_light_cone = world.dark_world_light_cone
    ret.seed = world.seed
    ret.can_access_trock_eyebridge = world.can_access_trock_eyebridge
    create_regions(ret)
    create_dungeons(ret)

    # connect copied world
    for region in world.regions:
        for entrance in region.entrances:
            ret.get_entrance(entrance.name).connect(ret.get_region(region.name))

    # fill locations
    for location in world.get_locations():
        if location.item is not None:
            item = Item(location.item.name, location.item.advancement, location.item.priority, location.item.type)
            ret.get_location(location.name).item = item
            item.location = ret.get_location(location.name)
        if location.event:
            ret.get_location(location.name).event = True

    # copy remaining itempool. No item in itempool should have an assigned location
    for item in world.itempool:
        ret.itempool.append(Item(item.name, item.advancement, item.priority, item.type))

    # copy progress items in state
    ret.state.prog_items = list(world.state.prog_items)

    set_rules(ret)

    return ret

def create_playthrough(world):
    # create a copy as we will modify it
    old_world = world
    world = copy_world(world)

    # in treasure hunt and pedestal goals, ganon is invincible
    if world.goal in ['pedestal', 'triforcehunt']:
        world.get_location('Ganon').item = None

    # if we only check for beatable, we can do this sanity check first before writing down spheres
    if world.check_beatable_only and not world.can_beat_game():
        raise RuntimeError('Cannot beat game. Something went terribly wrong here!')

    # get locations containing progress items
    prog_locations = [location for location in world.get_locations() if location.item is not None and (location.item.advancement or (location.item.key and world.keysanity))]

    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = list(prog_locations)
    logging.getLogger('').debug('Building up collection spheres.')
    while sphere_candidates:
        if not world.keysanity:
            state.sweep_for_events(key_only=True)

        sphere = []
        # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
        for location in sphere_candidates:
            if state.can_reach(location):
                sphere.append(location)

        for location in sphere:
            sphere_candidates.remove(location)
            state.collect(location.item, True)

        collection_spheres.append(sphere)

        logging.getLogger('').debug('Calculated sphere %i, containing %i of %i progress items.' % (len(collection_spheres), len(sphere), len(prog_locations)))

        if not sphere:
            logging.getLogger('').debug('The following items could not be reached: %s' % ['%s at %s' % (location.item.name, location.name) for location in sphere_candidates])
            if not world.check_beatable_only:
                raise RuntimeError('Not all progression items reachable. Something went terribly wrong here.')
            else:
                break

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

    # store the required locations for statistical analysis
    old_world.required_locations = [location.name for sphere in collection_spheres for location in sphere]

    # we can finally output our playthrough
    old_world.spoiler.playthrough = OrderedDict([(str(i + 1), {str(location): str(location.item) for location in sphere}) for i, sphere in enumerate(collection_spheres)])
