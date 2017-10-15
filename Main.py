from BaseClasses import World, CollectionState, Item
from Regions import create_regions
from EntranceShuffle import link_entrances
from Rom import patch_rom, LocalRom, JsonRom
from Rules import set_rules
from Dungeons import create_dungeons, fill_dungeons
from Items import ItemFactory
from collections import OrderedDict
import random
import time
import logging
import json

__version__ = '0.4.7-dev'

logic_hash = [118, 17, 154, 187, 209, 19, 0, 97, 63, 62, 164, 160, 155, 28, 136, 220, 251, 76, 55, 109, 174, 36, 82, 140, 87, 226, 26, 150, 200, 115, 6, 238,
              85, 229, 49, 141, 66, 199, 112, 212, 182, 98, 249, 54, 201, 161, 148, 126, 179, 5, 47, 162, 108, 152, 67, 203, 239, 15, 211, 132, 198, 124, 221, 81,
              217, 191, 177, 37, 145, 216, 84, 56, 65, 190, 163, 138, 186, 157, 9, 23, 189, 8, 188, 69, 204, 29, 22, 114, 79, 175, 59, 202, 107, 231, 96, 91,
              45, 64, 228, 2, 43, 74, 89, 205, 246, 123, 166, 83, 219, 248, 117, 241, 94, 60, 227, 20, 35, 18, 1, 252, 250, 110, 137, 58, 42, 102, 106, 93,
              101, 105, 193, 77, 39, 119, 223, 73, 51, 218, 78, 100, 21, 247, 41, 214, 170, 185, 237, 130, 12, 24, 92, 180, 16, 178, 235, 4, 240, 158, 57, 197,
              133, 88, 142, 234, 147, 196, 146, 224, 139, 207, 31, 232, 243, 3, 121, 210, 167, 99, 13, 44, 70, 213, 168, 244, 153, 127, 171, 233, 172, 75, 34, 236,
              113, 25, 149, 134, 53, 222, 122, 80, 195, 254, 27, 169, 255, 242, 143, 159, 225, 135, 230, 151, 48, 33, 72, 10, 95, 103, 253, 184, 52, 125, 206, 144,
              128, 32, 61, 176, 215, 50, 194, 40, 183, 173, 131, 46, 111, 90, 192, 208, 86, 181, 68, 104, 129, 116, 165, 156, 11, 14, 120, 30, 71, 245, 7, 38]


def main(args, seed=None):
    start = time.clock()

    # initialize the world
    world = World(args.shuffle, args.logic, args.mode, args.difficulty, args.goal, args.algorithm, not args.nodungeonitems, args.beatableonly, args.shuffleganon, args.quickswap)
    logger = logging.getLogger('')
    if seed is None:
        random.seed(None)
        world.seed = random.randint(0, 999999999)
    else:
        world.seed = int(seed)
    random.seed(world.seed)

    logger.info('ALttP Entrance Randomizer Version %s  -  Seed: %s\n\n' % (__version__, world.seed))

    create_regions(world)
    
    create_dungeons(world);

    logger.info('Shuffling the World about.')

    link_entrances(world)

    logger.info('Calculating Access Rules.')

    set_rules(world)

    logger.info('Generating Item Pool.')

    generate_itempool(world)

    logger.info('Placing Dungeon Items.')

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

    logger.info('Calculating playthrough.')

    create_playthrough(world)

    logger.info('Patching ROM.')

    if args.sprite is not None:
        sprite = bytearray(open(args.sprite, 'rb').read())
    else:
        sprite = None

    outfilebase = 'ER_%s_%s-%s-%s_%s-%s%s%s_%s' % (world.logic, world.difficulty, world.mode, world.goal, world.shuffle, world.algorithm, "-quickswap" if world.quickswap else "", "-shuffleganon" if world.shuffle_ganon else "", world.seed)

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


def distribute_items_cutoff(world, cutoffrate=0.33):
    # get list of locations to fill in
    fill_locations = world.get_unfilled_locations()
    random.shuffle(fill_locations)

    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool

    total_advancement_items = len([item for item in itempool if item.advancement])
    placed_advancement_items = 0

    progress_done = False
    advancement_placed = False

    # sweep once to pick up preplaced items
    world.state.sweep_for_events()

    while itempool and fill_locations:
        candidate_item_to_place = None
        item_to_place = None
        for item in itempool:
            if advancement_placed or (progress_done and (item.advancement or item.priority)):
                item_to_place = item
                break
            if item.advancement:
                candidate_item_to_place = item
                if world.unlocks_new_location(item):
                    item_to_place = item
                    placed_advancement_items += 1
                    break

        if item_to_place is None:
            # check if we can reach all locations and that is why we find no new locations to place
            if not progress_done and len(world.get_reachable_locations()) == len(world.get_locations()):
                progress_done = True
                continue
            # check if we have now placed all advancement items
            if progress_done:
                advancement_placed = True
                continue
            # we might be in a situation where all new locations require multiple items to reach. If that is the case, just place any advancement item we've found and continue trying
            if candidate_item_to_place is not None:
                item_to_place = candidate_item_to_place
                placed_advancement_items += 1
            else:
                # we placed all available progress items. Maybe the game can be beaten anyway?
                if world.can_beat_game():
                    logging.getLogger('').warning('Not all locations reachable. Game beatable anyway.')
                    progress_done = True
                    continue
                raise RuntimeError('No more progress items left to place.')

        spot_to_fill = None
        for location in (fill_locations if placed_advancement_items/total_advancement_items < cutoffrate else reversed(fill_locations)):
            if world.state.can_reach(location) and location.can_fill(item_to_place):
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

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s' % ([item.name for item in itempool], [location.name for location in fill_locations]))


def distribute_items_staleness(world):
    # get list of locations to fill in
    fill_locations = world.get_unfilled_locations()
    random.shuffle(fill_locations)

    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool

    progress_done = False
    advancement_placed = False

    # sweep once to pick up preplaced items
    world.state.sweep_for_events()

    while itempool and fill_locations:
        candidate_item_to_place = None
        item_to_place = None
        for item in itempool:
            if advancement_placed or (progress_done and (item.advancement or item.priority)):
                item_to_place = item
                break
            if item.advancement:
                candidate_item_to_place = item
                if world.unlocks_new_location(item):
                    item_to_place = item
                    break

        if item_to_place is None:
            # check if we can reach all locations and that is why we find no new locations to place
            if not progress_done and len(world.get_reachable_locations()) == len(world.get_locations()):
                progress_done = True
                continue
            # check if we have now placed all advancement items
            if progress_done:
                advancement_placed = True
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
            # increase likelyhood of skipping a location if it has been found stale
            if not progress_done and random.randint(0, location.staleness_count) > 2:
                continue

            if world.state.can_reach(location) and location.can_fill(item_to_place):
                spot_to_fill = location
                break
            else:
                location.staleness_count += 1

        # might have skipped too many locations due to potential staleness. Do not check for staleness now to find a candidate
        if spot_to_fill is None:
            for location in fill_locations:
                if world.state.can_reach(location) and location.can_fill(item_to_place):
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

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s' % ([item.name for item in itempool], [location.name for location in fill_locations]))


def fill_restrictive(world, base_state, locations, itempool):
    def sweep_from_pool():
        new_state = base_state.copy()
        for item in itempool:
            new_state.collect(item, True)
        new_state.sweep_for_events()
        return new_state

    while itempool and locations:
        item_to_place = itempool.pop()
        maximum_exploration_state = sweep_from_pool()

        spot_to_fill = None
        for location in locations:
            if location.can_fill(item_to_place):
                if world.check_beatable_only:
                    starting_state = base_state.copy()
                    for item in itempool:
                        starting_state.collect(item, True)

                if maximum_exploration_state.can_reach(location):
                    if world.check_beatable_only:
                        starting_state.collect(item_to_place, True)
                    else:
                        spot_to_fill = location
                        break

                if world.check_beatable_only and world.can_beat_game(starting_state):
                    spot_to_fill = location
                    break

        if spot_to_fill is None:
            # we filled all reachable spots. Maybe the game can be beaten anyway?
            if world.can_beat_game():
                if not world.check_beatable_only:
                    logging.getLogger('').warning('Not all items placed. Game beatable anyway.')
                break
            raise RuntimeError('No more spots to place %s' % item_to_place)

        world.push_item(spot_to_fill, item_to_place, False)
        locations.remove(spot_to_fill)
        spot_to_fill.event = True


def distribute_items_restrictive(world, gftower_trash_count=0):
    # get list of locations to fill in
    fill_locations = world.get_unfilled_locations()

    # get items to distribute
    random.shuffle(world.itempool)
    progitempool = [item for item in world.itempool if item.advancement]
    prioitempool = [item for item in world.itempool if not item.advancement and item.priority]
    restitempool = [item for item in world.itempool if not item.advancement and not item.priority]

    # fill in gtower locations with trash first
    gtower_locations = [location for location in fill_locations if 'Ganons Tower' in location.name]
    random.shuffle(gtower_locations)
    trashcnt = 0
    while gtower_locations and restitempool and trashcnt < gftower_trash_count:
        spot_to_fill = gtower_locations.pop()
        item_to_place = restitempool.pop()
        world.push_item(spot_to_fill, item_to_place, False)
        fill_locations.remove(spot_to_fill)
        trashcnt += 1

    random.shuffle(fill_locations)

    fill_restrictive(world, world.state, fill_locations, progitempool)

    random.shuffle(fill_locations)

    while prioitempool and fill_locations:
        spot_to_fill = fill_locations.pop()
        item_to_place = prioitempool.pop()
        world.push_item(spot_to_fill, item_to_place, False)

    while restitempool and fill_locations:
        spot_to_fill = fill_locations.pop()
        item_to_place = restitempool.pop()
        world.push_item(spot_to_fill, item_to_place, False)

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s' % ([item.name for item in progitempool + prioitempool + restitempool], [location.name for location in fill_locations]))


def flood_items(world):
    # get items to distribute
    random.shuffle(world.itempool)
    itempool = world.itempool
    progress_done = False

    # sweep once to pick up preplaced items
    world.state.sweep_for_events()

    # fill world from top of itempool while we can
    while not progress_done:
        location_list = world.get_unfilled_locations()
        random.shuffle(location_list)
        spot_to_fill = None
        for location in location_list:
            if world.state.can_reach(location) and location.can_fill(itempool[0]):
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
            if location.item is not None and not location.item.advancement and not location.item.priority and not location.item.key:
                # safe to replace
                replace_item = location.item
                replace_item.location = None
                itempool.append(replace_item)
                world.push_item(location, item_to_place, True)
                itempool.remove(item_to_place)
                break


def generate_itempool(world):
    if world.difficulty not in ['normal', 'timed', 'timed-ohko', 'timed-countdown'] or world.goal not in ['ganon', 'pedestal', 'dungeons', 'triforcehunt', 'crystals'] or world.mode not in ['open', 'standard', 'swordless']:
        raise NotImplementedError('Not supported yet')

    world.push_item('Ganon', ItemFactory('Triforce'), False)
    world.push_item('Agahnim 1', ItemFactory('Beat Agahnim 1'), False)
    world.get_location('Agahnim 1').event = True
    world.push_item('Agahnim 2', ItemFactory('Beat Agahnim 2'), False)
    world.get_location('Agahnim 2').event = True

    # set up item pool
    if world.difficulty in ['timed', 'timed-countdown']:
        world.itempool = ItemFactory(['Arrow Upgrade (+5)'] * 2 + ['Bomb Upgrade (+5)'] * 2 + ['Arrow Upgrade (+10)'] * 3 + ['Bomb Upgrade (+10)'] * 3 +
                                     ['Progressive Armor'] * 2 + ['Progressive Shield'] * 3 + ['Progressive Glove'] * 2 +
                                     ['Bottle'] * 4 +
                                     ['Bombos', 'Book of Mudora', 'Blue Boomerang', 'Bow', 'Bug Catching Net', 'Cane of Byrna', 'Cane of Somaria',
                                      'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp', 'Cape', 'Magic Powder',
                                      'Red Boomerang', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Silver Arrows'] +
                                     ['Sanctuary Heart Container'] + ['Rupees (100)'] * 2 + ['Boss Heart Container'] * 12 + ['Piece of Heart'] * 16 +
                                     ['Rupees (50)'] * 8 + ['Rupees (300)'] * 6 + ['Rupees (20)'] * 4 +
                                     ['Arrows (10)'] * 3 + ['Bombs (3)'] * 10 + ['Red Clock'] * 10 + ['Blue Clock'] * 10 + ['Green Clock'] * 20)
        world.clock_mode = 'stopwatch' if world.difficulty == 'timed' else 'countdown'
    elif world.difficulty == 'timed-ohko':
        world.itempool = ItemFactory(['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6 + ['Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] +
                                     ['Progressive Armor'] * 2 + ['Progressive Shield'] * 3 + ['Progressive Glove'] * 2 +
                                     ['Bottle'] * 4 +
                                     ['Bombos', 'Book of Mudora', 'Blue Boomerang', 'Bow', 'Bug Catching Net', 'Cane of Byrna', 'Cane of Somaria',
                                      'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp', 'Cape', 'Magic Powder',
                                      'Red Boomerang', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Silver Arrows'] +
                                     ['Single Arrow', 'Sanctuary Heart Container'] + ['Rupees (100)'] * 3 + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24 +
                                     ['Rupees (50)'] * 7 + ['Rupees (300)'] * 7 + ['Rupees (20)'] * 5 +
                                     ['Arrows (10)'] * 5 + ['Bombs (3)'] * 10 + ['Green Clock'] * 25)
        world.clock_mode = 'ohko'
    else:
        world.itempool = ItemFactory(['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6 + ['Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] +
                                     ['Progressive Armor'] * 2 + ['Progressive Shield'] * 3 + ['Progressive Glove'] * 2 +
                                     ['Bottle'] * 4 +
                                     ['Bombos', 'Book of Mudora', 'Blue Boomerang', 'Bow', 'Bug Catching Net', 'Cane of Byrna', 'Cane of Somaria',
                                      'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp', 'Cape', 'Magic Powder',
                                      'Red Boomerang', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Silver Arrows'] +
                                     ['Single Arrow', 'Sanctuary Heart Container', 'Rupees (100)'] + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24 +
                                     ['Rupees (50)'] * 7 + ['Rupees (5)'] * 4 + ['Rupee (1)'] * 2 + ['Rupees (300)'] * 5 + ['Rupees (20)'] * 28 +
                                     ['Arrows (10)'] * 5 + ['Bombs (3)'] * 10)

    if world.mode == 'swordless':
        world.push_item('Ether Tablet', ItemFactory('Rupees (20)'), False)
        world.push_item('Bombos Tablet', ItemFactory('Rupees (20)'), False)
        world.itempool.extend(ItemFactory(['Rupees (20)', 'Rupees (20)']))
    elif world.mode == 'standard':
        world.push_item('Uncle', ItemFactory('Progressive Sword'), False)
        world.get_location('Uncle').event = True
        world.itempool.extend(ItemFactory(['Progressive Sword'] * 3))
    else:
        world.itempool.extend(ItemFactory(['Progressive Sword'] * 4))

    # provide mirror and pearl so you can avoid fake DW/LW and do dark world exploration as intended by algorithm, for now
    if world.shuffle == 'insanity':
        world.push_item('[cave-040] Links House', ItemFactory('Magic Mirror'), False)
        world.get_location('[cave-040] Links House').event = True
        world.push_item('[dungeon-C-1F] Sanctuary', ItemFactory('Moon Pearl'), False)
        world.get_location('[dungeon-C-1F] Sanctuary').event = True
    else:
        world.itempool.extend(ItemFactory(['Magic Mirror', 'Moon Pearl']))

    if world.goal == 'pedestal':
        world.push_item('Altar', ItemFactory('Triforce'), False)
    elif world.goal == 'triforcehunt':
        world.treasure_hunt_count = 20
        world.treasure_hunt_icon = 'Triforce Piece'
        world.itempool.extend(ItemFactory(['Triforce Piece'] * 30))

    if random.randint(0, 3) == 0:
        world.itempool.append(ItemFactory('Magic Upgrade (1/4)'))
    else:
        world.itempool.append(ItemFactory('Magic Upgrade (1/2)'))

    # shuffle medallions
    mm_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    tr_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    world.required_medallions = (mm_medallion, tr_medallion)

    # distribute crystals
    crystals = ItemFactory(['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6'])
    crystal_locations = [world.get_location('Trinexx - Crystal'), world.get_location('Armos - Pendant'), world.get_location('Lanmolas - Pendant'), world.get_location('Moldorm - Pendant'), world.get_location('Helmasaur - Crystal'),
                         world.get_location('Blind - Crystal'), world.get_location('Mothula - Crystal'), world.get_location('Arrghus - Crystal'), world.get_location('Kholdstare - Crystal'),
                         world.get_location('Vitreous - Crystal')]

    random.shuffle(crystal_locations)

    fill_restrictive(world, world.get_all_state(keys=True), crystal_locations, crystals)


def copy_world(world):
    # ToDo: Not good yet
    ret = World(world.shuffle, world.logic, world.mode, world.difficulty, world.goal, world.algorithm, world.place_dungeon_items, world.check_beatable_only, world.shuffle_ganon, world.quickswap)
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
    prog_locations = [location for location in world.get_locations() if location.item is not None and location.item.advancement]

    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = list(prog_locations)
    logging.getLogger('').debug('Building up collection spheres.')
    while sphere_candidates:
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

