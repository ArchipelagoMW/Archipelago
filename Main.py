from BaseClasses import World, CollectionState, Item
from Regions import create_regions
from EntranceShuffle import link_entrances
from Rom import patch_rom, patch_base_rom
from Rules import set_rules
from Dungeons import fill_dungeons
from Items import ItemFactory
import random
import time
import logging
import argparse
import os

__version__ = '0.4-dev'

logic_hash = [215, 18, 94, 177, 161, 252, 45, 4, 29, 231, 99, 158, 70, 55, 74, 39, 12, 134, 142, 189, 61, 105, 10, 254, 137, 44, 72, 154, 145, 167, 98, 225,
              100, 217, 126, 187, 13, 255, 138, 51, 64, 130, 139, 233, 168, 69, 175, 25, 58, 160, 1, 27, 206, 169, 223, 210, 188, 111, 186, 240, 133, 26, 41, 241,
              204, 89, 78, 63, 96, 218, 198, 224, 219, 35, 82, 181, 121, 243, 0, 155, 91, 120, 221, 178, 162, 80, 66, 97, 118, 103, 86, 191, 135, 122, 104, 40,
              183, 9, 230, 110, 14, 87, 143, 249, 90, 75, 232, 157, 238, 196, 23, 248, 2, 101, 159, 108, 201, 73, 34, 15, 179, 92, 226, 60, 222, 32, 109, 119,
              49, 56, 16, 6, 22, 209, 190, 21, 136, 113, 205, 192, 146, 30, 212, 43, 200, 193, 185, 242, 71, 163, 102, 239, 24, 220, 166, 228, 208, 47, 3, 112,
              203, 50, 216, 214, 107, 106, 57, 67, 88, 42, 176, 129, 144, 54, 237, 165, 116, 141, 125, 128, 172, 171, 152, 83, 38, 93, 148, 151, 207, 236, 131, 85,
              170, 124, 28, 251, 194, 250, 8, 164, 65, 20, 150, 182, 77, 17, 202, 253, 173, 229, 46, 140, 76, 95, 117, 174, 79, 84, 36, 244, 199, 37, 211, 7,
              247, 213, 31, 62, 59, 153, 197, 19, 48, 114, 53, 115, 149, 81, 5, 184, 147, 68, 227, 234, 52, 156, 132, 127, 235, 245, 11, 33, 123, 180, 246, 195]


def main(args, seed=None):
    start = time.clock()

    # initialize the world
    world = World(args.shuffle, args.logic, args.mode, args.difficulty, args.goal, args.algorithm, not args.nodungeonitems, args.beatableonly)
    logger = logging.getLogger('')

    if seed is None:
        random.seed(None)
        world.seed = random.randint(0, 999999999)
    else:
        world.seed = int(seed)
    random.seed(world.seed)

    world.spoiler += 'ALttP Entrance Randomizer Version %s  -  Seed: %s\n\n' % (__version__, world.seed)
    world.spoiler += 'Logic: %s  Mode: %s  Goal: %s  Entrance Shuffle: %s  Filling Algorithm: %s\n\n' % (args.logic, args.mode, args.goal, args.shuffle, args.algorithm)  # todo

    logger.info(world.spoiler)

    create_regions(world)

    logger.info('Shuffling the World about.')

    world.spoiler += link_entrances(world)

    logger.info('Generating Item Pool.')

    world.spoiler += generate_itempool(world)

    logger.info('Calculating Access Rules.')

    world.spoiler += set_rules(world)

    logger.info('Placing Dungeon Items.')

    world.spoiler += fill_dungeons(world)

    logger.info('Fill the world.')

    if args.algorithm == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    elif args.algorithm == 'vt21':
        distribute_items_cutoff(world, 1)
    elif args.algorithm == 'vt22':
        distribute_items_cutoff(world, 0.66)
    elif args.algorithm == 'freshness':
        distribute_items_staleness(world)
    elif args.algorithm == 'restrictive':
        distribute_items_restrictive(world, 10 if world.goal is not 'starhunt' else 0)

    world.spoiler += print_location_spoiler(world)

    logger.info('Calculating playthrough.')

    world.spoiler += create_playthrough(world)

    logger.info('Patching ROM.')

    if args.sprite is not None:
        sprite = bytearray(open(args.sprite, 'rb').read())
    else:
        sprite = None

    outfilebase = 'ER_%s_%s_%s_%s_%s_%s' % (world.mode, world.goal, world.shuffle, world.difficulty, world.algorithm, world.seed)

    if not args.suppress_rom:
        rom = bytearray(open(args.rom, 'rb').read())
        patch_base_rom(rom)
        patched_rom = patch_rom(world, rom, bytearray(logic_hash), args.quickswap, args.heartbeep, sprite)
        with open('%s.sfc' % outfilebase, 'wb') as outfile:
            outfile.write(patched_rom)

    if args.create_spoiler:
        with open('%s_Spoiler.txt' % outfilebase, 'w') as outfile:
            outfile.write(world.spoiler)

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

            if world.state.can_reach(location) and location.item_rule(item_to_place):
                spot_to_fill = location
                break
            else:
                location.staleness_count += 1

        # might have skipped too many locations due to potential staleness. Do not check for staleness now to find a candidate
        if spot_to_fill is None:
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

    logging.getLogger('').debug('Unplaced items: %s - Unfilled Locations: %s' % ([item.name for item in itempool], [location.name for location in fill_locations]))


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

    def sweep_from_pool():
        new_state = world.state.copy()
        for item in progitempool:
            new_state.collect(item, True)
        new_state.sweep_for_events()
        return new_state

    while progitempool and fill_locations:
        item_to_place = progitempool.pop()
        maximum_exploration_state = sweep_from_pool()

        spot_to_fill = None
        for location in fill_locations:
            if location.item_rule(item_to_place):
                if world.check_beatable_only:
                    starting_state = world.state.copy()
                    for item in progitempool:
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
        fill_locations.remove(spot_to_fill)
        spot_to_fill.event = True

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

    # fill world from top of itempool while we can
    while not progress_done:
        location_list = world.get_unfilled_locations()
        random.shuffle(location_list)
        spot_to_fill = None
        for location in location_list:
            if world.state.can_reach(location) and location.item_rule(itempool[0]):
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
    if world.difficulty not in ['normal', 'timed', 'timed-ohko', 'timed-countdown'] or world.goal not in ['ganon', 'pedestal', 'dungeons', 'starhunt', 'triforcehunt'] or world.mode not in ['open', 'standard']:
        raise NotImplementedError('Not supported yet')

    world.push_item('Ganon', ItemFactory('Triforce'), False)
    world.push_item('Agahnim 1', ItemFactory('Beat Agahnim 1'), False)
    world.get_location('Agahnim 1').event = True
    world.push_item('Agahnim 2', ItemFactory('Beat Agahnim 2'), False)
    world.get_location('Agahnim 2').event = True

    # set up item pool
    if world.difficulty in ['timed', 'timed-countdown']:
        world.itempool = ItemFactory(['Arrow Upgrade (+5)'] * 2 + ['Bomb Upgrade (+5)'] * 2 + ['Arrow Upgrade (+10)'] * 3 + ['Bomb Upgrade (+10)'] * 3 +
                                     ['Progressive Armor'] * 2 + ['Progressive Shield'] * 3 + ['Progressive Sword'] * 3 + ['Progressive Glove'] * 2 +
                                     ['Bottle'] * 4 +
                                     ['Bombos', 'Book of Mudora', 'Blue Boomerang', 'Bow', 'Bug Catching Net', 'Cane of Byrna', 'Cane of Somaria',
                                      'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp', 'Cape', 'Magic Powder',
                                      'Red Boomerang', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Silver Arrows'] +
                                     ['Sanctuary Heart Container'] + ['Rupees (100)'] * 2 + ['Boss Heart Container'] * 12 + ['Piece of Heart'] * 16 +
                                     ['Rupees (50)'] * 8 + ['Rupees (300)'] * 5 + ['Rupees (20)'] * 4 +
                                     ['Arrows (10)'] * 2 + ['Bombs (3)'] * 10 + ['Red Clock'] * 10 + ['Blue Clock'] * 10 + ['Green Clock'] * 20)
        world.clock_mode = 'stopwatch' if world.difficulty == 'timed' else 'countdown'
    elif world.difficulty == 'timed-ohko':
        world.itempool = ItemFactory(['Arrow Upgrade (+5)'] * 6 + ['Bomb Upgrade (+5)'] * 6 + ['Arrow Upgrade (+10)', 'Bomb Upgrade (+10)'] +
                                     ['Progressive Armor'] * 2 + ['Progressive Shield'] * 3 + ['Progressive Sword'] * 3 + ['Progressive Glove'] * 2 +
                                     ['Bottle'] * 4 +
                                     ['Bombos', 'Book of Mudora', 'Blue Boomerang', 'Bow', 'Bug Catching Net', 'Cane of Byrna', 'Cane of Somaria',
                                      'Ether', 'Fire Rod', 'Flippers', 'Ocarina', 'Hammer', 'Hookshot', 'Ice Rod', 'Lamp', 'Cape', 'Magic Powder',
                                      'Red Boomerang', 'Mushroom', 'Pegasus Boots', 'Quake', 'Shovel', 'Silver Arrows'] +
                                     ['Single Arrow', 'Sanctuary Heart Container'] + ['Rupees (100)'] * 3 + ['Boss Heart Container'] * 10 + ['Piece of Heart'] * 24 +
                                     ['Rupees (50)'] * 7 + ['Rupees (300)'] * 6 + ['Rupees (20)'] * 5 +
                                     ['Arrows (10)'] * 4 + ['Bombs (3)'] * 10 + ['Green Clock'] * 25)
        world.clock_mode = 'ohko'
    else:
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
        world.push_item('Uncle', ItemFactory('Progressive Sword'), do_not_sweep=True)
    else:
        world.itempool.append(ItemFactory('Progressive Sword'))

    # provide mirror and pearl so you can avoid fake DW/LW and do dark world exploration as intended by algorithm, for now
    if world.shuffle == 'insanity':
        world.push_item('[cave-040] Links House', ItemFactory('Magic Mirror'), do_not_sweep=True)
        world.push_item('[dungeon-C-1F] Sanctuary', ItemFactory('Moon Pearl'), do_not_sweep=True)
    else:
        world.itempool.extend(ItemFactory(['Magic Mirror', 'Moon Pearl']))

    if world.goal == 'pedestal':
        world.push_item('Altar', ItemFactory('Triforce'), False)
    elif world.goal == 'starhunt':
        world.treasure_hunt_count = 10
        world.treasure_hunt_icon = 'Power Star'
        world.itempool.extend(ItemFactory(['Power Star'] * 15))
    elif world.goal == 'triforcehunt':
        world.treasure_hunt_count = 3
        world.treasure_hunt_icon = 'Triforce Piece'
        world.itempool.extend(ItemFactory(['Triforce Piece'] * 3))

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
        location.event = True

    # shuffle medallions
    mm_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    tr_medallion = ['Ether', 'Quake', 'Bombos'][random.randint(0, 2)]
    world.required_medallions = (mm_medallion, tr_medallion)

    return 'Misery Mire Medallion: %s\nTurtle Rock Medallion: %s\n\n' % (mm_medallion, tr_medallion)


def copy_world(world):
    # ToDo: Not good yet
    ret = World(world.shuffle, world.logic, world.mode, world.difficulty, world.goal, world.algorithm, world.place_dungeon_items, world.check_beatable_only)
    ret.required_medallions = list(world.required_medallions)
    ret.swamp_patch_required = world.swamp_patch_required
    ret.treasure_hunt_count = world.treasure_hunt_count
    ret.treasure_hunt_icon = world.treasure_hunt_icon
    ret.sewer_light_cone = world.sewer_light_cone
    ret.light_world_light_cone = world.light_world_light_cone
    ret.dark_world_light_cone = world.dark_world_light_cone
    ret.seed = world.seed
    create_regions(ret)

    # connect copied world
    for region in world.regions:
        for entrance in region.entrances:
            ret.get_entrance(entrance.name).connect(ret.get_region(region.name))

    set_rules(ret)

    # fill locations
    for location in world.get_locations():
        if location.item is not None:
            item = Item(location.item.name, location.item.advancement, location.item.priority, location.item.key)
            ret.get_location(location.name).item = item
            item.location = ret.get_location(location.name)
        if location.event:
            ret.get_location(location.name).event = True

    # copy remaining itempool. No item in itempool should have an assigned location
    for item in world.itempool:
        ret.itempool.append(Item(item.name, item.advancement, item.priority, item.key))

    # copy progress items in state
    ret.state.prog_items = list(world.state.prog_items)

    return ret


def create_playthrough(world):
    # create a copy as we will modify it
    old_world = world
    world = copy_world(world)

    # in treasure hunt and pedestal goals, ganon is invincible
    if world.goal in ['pedestal', 'starhunt', 'triforcehunt']:
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
        sphere = []
        # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
        for location in sphere_candidates:
            if state.can_reach(location):
                sphere.append(location)

        for location in sphere:
            sphere_candidates.remove(location)
            state.collect(location.item, True)

        state.sweep_for_events(key_only=True)

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
    parser.add_argument('--goal', default='ganon', const='ganon', nargs='?', choices=['ganon', 'pedestal', 'dungeons', 'starhunt', 'triforcehunt'],
                        help='Select completion goal. Pedestal places the Triforce at the Master Sword Pedestal. All dungeons is not enforced ingame but considered in the playthrough. \n'
                             'Star Hunt places 15 Power Stars pieces in the world, collect 10 of them to beat the game.\n'
                             'Triforce Hunt places 3 Triforce Pieces in the world, collect them all to beat the game.')
    parser.add_argument('--difficulty', default='normal', const='normal', nargs='?', choices=['normal', 'timed', 'timed-ohko', 'timed-countdown'],
                        help='Select game difficulty. Affects available itempool.\n'
                             'Timed modes replace low value items with clocks, the overall rupee count in the pool stays roughly the same.\n'
                             'Timed starts with clock at zero. Green Clocks subtract 4 minutes (Total: 20), Blue Clocks subtract 2 minutes (Total: 10), Red Clocks add 2 minutes (Total: 10). Winner is player with lowest time at the end.\n'
                             'Timed OHKO starts clock at 10 minutes. Green Clocks add 5 minutes (Total: 25). As long as clock is at 0, Link will die in one hit.\n'
                             'Timed Countdown starts with clock at 40 minutes. Same clocks as Timed mode. If time runs out, you lose (but can still keep playing).')
    parser.add_argument('--algorithm', default='freshness', const='freshness', nargs='?', choices=['freshness', 'flood', 'vt21', 'vt22', 'restrictive'],
                        help='Select item filling algorithm. vt21 is unbiased in its selection, but has tendency to put Ice Rod in Turtle Rock.\n'
                             'vt22 drops off stale locations after 1/3 of progress items were placed to try to circumvent vt21\'s shortcomings.\n'
                             'freshness keeps track of stale locations (ones that cannot be reached yet) and decreases likeliness of selecting them the more often they were found unreachable.\n'
                             'flood pushes out items starting from Link\'s House and is slightly biased to placing progression items with less restrictions.\n'
                             'restrictive shuffles items and then places them in a random location that it is not impossible to be in.')
    parser.add_argument('--shuffle', default='full', const='full', nargs='?', choices=['vanilla', 'simple', 'restricted', 'full', 'madness', 'insanity', 'dungeonsfull', 'dungeonssimple'],
                        help='Select Entrance Shuffling Algorithm.\n'
                             'Simple shuffles Dungeon Entrances/Exits between each other and keeps all 4-entrance dungeons confined to one location. All caves outside of death mountain are shuffled in pairs.\n'
                             'Restricted uses Dungeons shuffling from Simple but freely connects remaining entrances.\n'
                             'Full mixes cave and dungeon entrances freely.\n'
                             'Madness decouples entrances and exits from each other and shuffles them freely, only ensuring that no fake Light/Dark World happens and all locations are reachable.\n'
                             'Insanity is Madness without the world restrictions. Mirror and Pearl are provided early to ensure Filling algorithm works properly. Deal with Fake LW/DW at your discretion. Experimental.\n'
                             'The dungeon variants only mix up dungeons and keep the rest of the overworld vanilla.')
    parser.add_argument('--rom', default='Zelda no Densetsu - Kamigami no Triforce (Japan).sfc', help='Path to an ALttP JAP(1.0) rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--count', help='Use to batch generate multiple seeds with same settings. If --seed is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with --seed given will produce the same 10 (different) roms each time).', type=int)
    parser.add_argument('--quickswap', help='Enable quick item swapping with L and R.', action='store_true')
    parser.add_argument('--nodungeonitems', help='Remove Maps and Compasses from Itempool, replacing them by empty slots.', action='store_true')
    parser.add_argument('--beatableonly', help='Only check if the game is beatable with placement. Do not ensure all locations are reachable. This only has an effect on the restrictive algorithm currently.', action='store_true')
    parser.add_argument('--heartbeep', default='normal', const='normal', nargs='?', choices=['normal', 'half', 'quarter', 'off'],
                        help='Select the rate at which the heart beep sound is played at low health.')
    parser.add_argument('--sprite', help='Path to a sprite sheet to use for Link. Needs to be in binary format and have a length of 0x7000 (28672) bytes.')
    parser.add_argument('--suppress_rom', help='Do not create an output rom file.', action='store_true')
    args = parser.parse_args()

    # ToDo: Validate files further than mere existance
    if not os.path.isfile(args.rom):
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % args.rom)
        exit(1)
    if args.sprite is not None and not os.path.isfile(args.rom):
        input('Could not find link sprite sheet at given location. \nPress Enter to exit.' % args.sprite)
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
