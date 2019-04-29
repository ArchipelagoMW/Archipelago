from collections import OrderedDict
import copy
from itertools import zip_longest
import json
import logging
import random
import time

from BaseClasses import World, CollectionState, Item, Region, Location, Shop
from Regions import create_regions, mark_light_world_regions
from EntranceShuffle import link_entrances
from Rom import patch_rom, Sprite, LocalRom, JsonRom
from Rules import set_rules
from Dungeons import create_dungeons, fill_dungeons, fill_dungeons_restrictive
from Fill import distribute_items_cutoff, distribute_items_staleness, distribute_items_restrictive, flood_items
from ItemList import generate_itempool, difficulties, fill_prizes
from Utils import output_path

__version__ = '0.6.2'

logic_hash = [134, 166, 181, 191, 228, 89, 188, 200, 5, 157, 217, 139, 180, 198, 106, 104,
              88, 223, 138, 28, 54, 18, 216, 129, 248, 19, 109, 220, 159, 75, 238, 57,
              231, 183, 143, 167, 114, 176, 82, 169, 179, 94, 115, 193, 252, 222, 52, 245,
              33, 208, 39, 122, 177, 136, 29, 161, 210, 165, 6, 125, 146, 212, 101, 185,
              65, 247, 253, 85, 171, 147, 71, 148, 203, 202, 230, 1, 13, 64, 254, 141,
              32, 93, 152, 4, 92, 16, 195, 204, 246, 201, 11, 7, 189, 97, 9, 91,
              237, 215, 163, 131, 142, 34, 111, 196, 120, 127, 168, 211, 227, 61, 187, 110,
              190, 162, 59, 80, 225, 186, 37, 154, 76, 72, 27, 17, 79, 206, 207, 243,
              184, 197, 153, 48, 119, 99, 2, 151, 51, 67, 121, 175, 38, 224, 87, 242,
              45, 22, 155, 244, 209, 117, 214, 213, 194, 126, 236, 73, 133, 70, 49, 140,
              229, 108, 156, 124, 105, 226, 44, 23, 112, 102, 173, 219, 14, 116, 58, 103,
              55, 10, 95, 251, 84, 118, 160, 78, 63, 250, 31, 41, 35, 255, 170, 25,
              66, 172, 98, 249, 68, 8, 113, 21, 46, 24, 137, 149, 81, 130, 42, 164,
              50, 12, 158, 15, 47, 182, 30, 40, 36, 83, 77, 205, 20, 241, 3, 132,
              0, 60, 96, 62, 74, 178, 53, 56, 135, 174, 145, 86, 107, 233, 218, 221,
              43, 150, 100, 69, 235, 26, 234, 192, 199, 144, 232, 128, 239, 123, 240, 90]


def main(args, seed=None):
    start = time.clock()

    # initialize the world
    world = World(args.shuffle, args.logic, args.mode, args.difficulty, args.timer, args.progressive, args.goal, args.algorithm, not args.nodungeonitems, args.beatableonly, args.shuffleganon, args.quickswap, args.fastmenu, args.disablemusic, args.keysanity, args.retro, args.custom, args.customitemarray, args.shufflebosses, args.hints)
    logger = logging.getLogger('')
    if seed is None:
        random.seed(None)
        world.seed = random.randint(0, 999999999)
    else:
        world.seed = int(seed)
    random.seed(world.seed)

    logger.info('ALttP Entrance Randomizer Version %s  -  Seed: %s\n\n', __version__, world.seed)

    world.difficulty_requirements = difficulties[world.difficulty]

    create_regions(world)

    create_dungeons(world)

    logger.info('Shuffling the World about.')

    link_entrances(world)
    mark_light_world_regions(world)

    logger.info('Generating Item Pool.')

    generate_itempool(world)

    logger.info('Calculating Access Rules.')

    set_rules(world)

    logger.info('Placing Dungeon Prizes.')

    fill_prizes(world)

    logger.info('Placing Dungeon Items.')

    shuffled_locations = None
    if args.algorithm in ['balanced', 'vt26'] or args.keysanity:
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

        distribute_items_restrictive(world, gt_filler(world), shuffled_locations)
    elif args.algorithm == 'balanced':
        distribute_items_restrictive(world, gt_filler(world))

    logger.info('Calculating playthrough.')

    create_playthrough(world)

    logger.info('Patching ROM.')

    if args.sprite is not None:
        if isinstance(args.sprite, Sprite):
            sprite = args.sprite
        else:
            sprite = Sprite(args.sprite)
    else:
        sprite = None

    outfilebase = 'ER_%s_%s-%s-%s%s_%s-%s%s%s%s%s_%s' % (world.logic, world.difficulty, world.mode, world.goal, "" if world.timer in ['none', 'display'] else "-" + world.timer, world.shuffle, world.algorithm, "-keysanity" if world.keysanity else "", "-retro" if world.retro else "", "-prog_" + world.progressive if world.progressive in ['off', 'random'] else "", "-nohints" if not world.hints else "", world.seed)

    if not args.suppress_rom:
        if args.jsonout:
            rom = JsonRom()
        else:
            rom = LocalRom(args.rom)
        patch_rom(world, rom, bytearray(logic_hash), args.heartbeep, args.heartcolor, sprite)
        if args.jsonout:
            print(json.dumps({'patch': rom.patches, 'spoiler': world.spoiler.to_json()}))
        else:
            rom.write_to_file(args.jsonout or output_path('%s.sfc' % outfilebase))

    if args.create_spoiler and not args.jsonout:
        world.spoiler.to_file(output_path('%s_Spoiler.txt' % outfilebase))

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.clock() - start)

    return world

def gt_filler(world):
    if world.goal == 'triforcehunt':
        return random.randint(15, 50)
    return random.randint(0, 15)

def copy_world(world):
    # ToDo: Not good yet
    ret = World(world.shuffle, world.logic, world.mode, world.difficulty, world.timer, world.progressive, world.goal, world.algorithm, world.place_dungeon_items, world.check_beatable_only, world.shuffle_ganon, world.quickswap, world.fastmenu, world.disable_music, world.keysanity, world.retro, world.custom, world.customitemarray, world.boss_shuffle, world.hints)
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
    ret.can_access_trock_front = world.can_access_trock_front
    ret.can_access_trock_big_chest = world.can_access_trock_big_chest
    ret.can_access_trock_middle = world.can_access_trock_middle
    ret.can_take_damage = world.can_take_damage
    ret.difficulty_requirements = world.difficulty_requirements
    ret.fix_fake_world = world.fix_fake_world
    ret.lamps_needed_for_dark_rooms = world.lamps_needed_for_dark_rooms
    create_regions(ret)
    create_dungeons(ret)

    copy_dynamic_regions_and_locations(world, ret)

    # copy bosses
    for dungeon in world.dungeons:
        for level, boss in dungeon.bosses.items():
            ret.get_dungeon(dungeon.name).bosses[level] = boss

    for shop in world.shops:
        copied_shop = ret.get_region(shop.region.name).shop
        copied_shop.active = shop.active
        copied_shop.inventory = copy.copy(shop.inventory)

    # connect copied world
    for region in world.regions:
        copied_region = ret.get_region(region.name)
        copied_region.is_light_world = region.is_light_world
        copied_region.is_dark_world = region.is_dark_world
        for entrance in region.entrances:
            ret.get_entrance(entrance.name).connect(copied_region)

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

def copy_dynamic_regions_and_locations(world, ret):
    for region in world.dynamic_regions:
        new_reg = Region(region.name, region.type, region.hint_text)
        ret.regions.append(new_reg)
        ret.dynamic_regions.append(new_reg)

        # Note: ideally exits should be copied here, but the current use case (Take anys) do not require this

        if region.shop:
            new_reg.shop = Shop(new_reg, region.shop.room_id, region.shop.type, region.shop.shopkeeper_config, region.shop.replaceable)
            ret.shops.append(new_reg.shop)

    for location in world.dynamic_locations:
        new_loc = Location(location.name, location.address, location.crystal, location.hint_text, location.parent_region)
        new_reg = ret.get_region(location.parent_region.name)
        new_reg.locations.append(new_loc)


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
    prog_locations = [location for location in world.get_filled_locations() if location.item.advancement]
    state_cache = [None]
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
            state.collect(location.item, True, location)

        collection_spheres.append(sphere)

        state_cache.append(state.copy())

        logging.getLogger('').debug('Calculated sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere), len(prog_locations))
        if not sphere:
            logging.getLogger('').debug('The following items could not be reached: %s', ['%s at %s' % (location.item.name, location.name) for location in sphere_candidates])
            if not world.check_beatable_only:
                raise RuntimeError('Not all progression items reachable. Something went terribly wrong here.')
            else:
                break

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each range of influence to the bare minimum required inside it
    for num, sphere in reversed(list(enumerate(collection_spheres))):
        to_delete = []
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            logging.getLogger('').debug('Checking if %s is required to beat the game.', location.item.name)
            old_item = location.item
            location.item = None
            state.remove(old_item)
            ##if world.can_beat_game(state_cache[num]):
            if world.can_beat_game():
                to_delete.append(location)
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        for location in to_delete:
            sphere.remove(location)

    # we are now down to just the required progress items in collection_spheres. Unfortunately
    # the previous pruning stage could potentially have made certain items dependant on others
    # in the same or later sphere (because the location had 2 ways to access but the item originally
    # used to access it was deemed not required.) So we need to do one final sphere collection pass
    # to build up the correct spheres

    required_locations = [item for sphere in collection_spheres for item in sphere]
    state = CollectionState(world)
    collection_spheres = []
    while required_locations:
        if not world.keysanity:
            state.sweep_for_events(key_only=True)

        sphere = list(filter(state.can_reach, required_locations))

        for location in sphere:
            required_locations.remove(location)
            state.collect(location.item, True, location)

        collection_spheres.append(sphere)

        logging.getLogger('').debug('Calculated final sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere), len(required_locations))
        if not sphere:
            raise RuntimeError('Not all required items reachable. Something went terribly wrong here.')

    # store the required locations for statistical analysis
    old_world.required_locations = [location.name for sphere in collection_spheres for location in sphere]

    def flist_to_iter(node):
        while node:
            value, node = node
            yield value

    def get_path(state, region):
        reversed_path_as_flist = state.path.get(region, (region, None))
        string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
        # Now we combine the flat string list into (region, exit) pairs
        pathsiter = iter(string_path_flat)
        pathpairs = zip_longest(pathsiter, pathsiter)
        return list(pathpairs)

    old_world.spoiler.paths = {location.name : get_path(state, location.parent_region) for sphere in collection_spheres for location in sphere}
    if any(exit == 'Pyramid Fairy' for path in old_world.spoiler.paths.values() for (_, exit) in path):
        old_world.spoiler.paths['Big Bomb Shop'] = get_path(state, world.get_region('Big Bomb Shop'))

    # we can finally output our playthrough
    old_world.spoiler.playthrough = OrderedDict([(str(i + 1), {str(location): str(location.item) for location in sphere}) for i, sphere in enumerate(collection_spheres)])
