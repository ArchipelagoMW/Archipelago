from BaseClasses import World, CollectionState
from Regions import create_regions, location_addresses, crystal_locations, dungeon_music_addresses
from EntranceShuffle import link_entrances, door_addresses, single_doors
from Text import string_to_alttp_text, text_addresses, altar_text
from Rules import set_rules
from Dungeons import fill_dungeons
from Items import *
import random
import time
import logging
import argparse
import os

__version__ = '0.1-dev'


def main(seed=None, shuffle='default', logic='noglitches', mode='standard', difficulty='normal', goal='ganon', algo='regular', spoiler=True, base_rom='Open_Base_Rom.sfc'):
    start = time.clock()

    # initialize the world
    world = World(shuffle, logic, mode, difficulty, goal)
    logger = logging.getLogger('')

    if seed is None:
        random.seed(None)
        world.seed = random.randint(0, 999999999)
    else:
        world.seed = seed
    random.seed(world.seed)

    world.spoiler += 'ALttP Entrance Randomizer Version %s  -  Seed: %s\n\n' % (__version__, world.seed)
    world.spoiler += 'Logic: %s  Mode: %s  Goal: %s  Entrance Shuffle: %s  Filling Algorithm: %s\n\n' % (logic, mode, goal, shuffle, algo)  # todo

    logger.info(world.spoiler)

    create_regions(world)

    logger.info('Shuffling the World about.')

    world.spoiler += link_entrances(world)

    logger.info('Calculating Access Rules.')

    world.spoiler += set_rules(world)

    logger.info('Generating Item Pool and placing Dungeon Items.')

    world.spoiler += generate_itempool(world)

    logger.info('Fill the world.')

    if algo == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    else:
        distribute_items(world)
    world.spoiler += print_location_spoiler(world)

    logger.info('Calculating playthrough.')

    world.spoiler += create_playthrough(world)

    logger.info('Patching ROM.')

    rom = bytearray(open(base_rom, 'rb').read())
    patched_rom = patch_rom(world, rom)

    outfilebase = 'ER_%s_%s_%s_%s' % (world.mode, world.goal, world.shuffle, world.seed)

    with open('%s.sfc' % outfilebase, 'wb') as outfile:
        outfile.write(patched_rom)
    if spoiler:
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
                    break
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

    world.push_item('Ganon', Triforce(), False)

    # set up item pool
    world.itempool = [
        ArrowUpgrade5(), ArrowUpgrade5(), ArrowUpgrade5(), ArrowUpgrade5(), ArrowUpgrade5(), ArrowUpgrade5(),
        ArrowUpgrade10(),
        SingleArrow(),
        ProgressiveArmor(), ProgressiveArmor(),
        BombUpgrade5(), BombUpgrade5(), BombUpgrade5(), BombUpgrade5(), BombUpgrade5(), BombUpgrade5(),
        BombUpgrade10(),
        Bombos(),
        Book(),
        BlueBoomerang(),
        Bottle(), Bottle(), Bottle(), Bottle(),
        Bow(),
        Net(),
        Byrna(),
        Somaria(),
        Ether(),
        Rupees50(), Rupees50(), Rupees50(), Rupees50(), Rupees50(), Rupees50(), Rupees50(),
        ProgressiveShield(), ProgressiveShield(), ProgressiveShield(),
        ProgressiveSword(), ProgressiveSword(), ProgressiveSword(),
        FireRod(),
        Rupees5(), Rupees5(), Rupees5(), Rupees5(),
        Flippers(),
        Ocarina(),
        Hammer(),
        SancHeart(),
        HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(), HeartContainer(),
        Hookshot(),
        IceRod(),
        Lamp(),
        Cape(),
        Mirror(),
        Powder(),
        RedBoomerang(),
        Pearl(),
        Mushroom(),
        Rupees100(),
        Rupee(), Rupee(),
        Boots(),
        PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(),
        PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(), PieceOfHeart(),
        ProgressiveGlove(), ProgressiveGlove(),
        Quake(),
        Shovel(),
        SilverArrows(),
        Arrows10(), Arrows10(), Arrows10(), Arrows10(),
        Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(), Bombs3(),
        Rupees300(), Rupees300(), Rupees300(), Rupees300(),
        Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(),
        Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20(), Rupees20()
    ]

    if world.mode == 'standard':
        world.push_item('Uncle', ProgressiveSword())
    else:
        world.itempool.append(ProgressiveSword())

    if world.goal == 'pedestal':
        world.push_item('Altar', Triforce())
        items = list(world.itempool)
        random.shuffle(items)
        for item in items:
            if not item.advancement:
                # save to remove
                world.itempool.remove(item)
                break
                # ToDo what to do if EVERYTHING is a progress item?

    if random.randint(0, 3) == 0:
        world.itempool.append(QuarterMagic())
    else:
        world.itempool.append(HalfMagic())

    # distribute crystals
    crystals = [GreenPendant(), RedPendant(), BluePendant(), Crystal1(), Crystal2(), Crystal3(), Crystal4(), Crystal5(), Crystal6(), Crystal7()]
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
    ret = World(world.shuffle, world.logic, world.mode, world.difficulty, world.goal)
    ret.required_medallions = list(world.required_medallions)
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


def patch_rom(world, rom):
    # patch items
    for location in world.get_locations():
        if location.name == 'Ganon':
            # cannot shuffle this yet
            continue

        itemid = location.item.code if location.item is not None else 0x5A

        try:
            # regular items
            locationaddress = location_addresses[location.name]
            write_byte(rom, locationaddress, itemid)
        except KeyError:
            # crystals
            locationaddress = crystal_locations[location.name]
            for address, value in zip(locationaddress, itemid):
                write_byte(rom, address, value)

            # patch music
            music_addresses = dungeon_music_addresses[location.name]
            music = 0x11 if 'Pendant' in location.item.name else 0x16
            for music_address in music_addresses:
                write_byte(rom, music_address, music)

    # patch entrances
    for region in world.regions:
        for exit in region.exits:
            if exit.target is not None:
                try:
                    addresses = door_addresses[exit.name]
                    write_byte(rom, addresses[0], exit.target[0])
                    write_byte(rom, addresses[1], exit.target[1])
                except KeyError:
                    # probably cave
                    addresses = single_doors[exit.name]
                    if not isinstance(addresses, tuple):
                        addresses = (addresses,)
                    for address in addresses:
                        write_byte(rom, address, exit.target)

    # patch medallion requirements
    if world.required_medallions[0] == 'Bombos':
        write_byte(rom, 0x180022, 0x00)  # requirement
        write_byte(rom, 0x4FF2, 0x31)  # sprite
        write_byte(rom, 0x50D1, 0x80)
        write_byte(rom, 0x51B0, 0x00)
    elif world.required_medallions[0] == 'Quake':
        write_byte(rom, 0x180022, 0x02)  # requirement
        write_byte(rom, 0x4FF2, 0x31)  # sprite
        write_byte(rom, 0x50D1, 0x88)
        write_byte(rom, 0x51B0, 0x00)
    if world.required_medallions[1] == 'Bombos':
        write_byte(rom, 0x180023, 0x00)  # requirement
        write_byte(rom, 0x5020, 0x31)  # sprite
        write_byte(rom, 0x50FF, 0x90)
        write_byte(rom, 0x51DE, 0x00)
    elif world.required_medallions[1] == 'Ether':
        write_byte(rom, 0x180023, 0x01)  # requirement
        write_byte(rom, 0x5020, 0x31)  # sprite
        write_byte(rom, 0x50FF, 0x98)
        write_byte(rom, 0x51DE, 0x00)

    if world.swamp_patch_required:
        # patch swamp: Need to enable permanent drain of water as dam or swamp were moved
        rom = rom.replace(bytearray([0xAF, 0xBB, 0xF2, 0x7E, 0x29, 0xDF, 0x8F, 0xBB, 0xF2, 0x7E]), bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))
        rom = rom.replace(bytearray([0xAF, 0xFB, 0xF2, 0x7E, 0x29, 0xDF, 0x8F, 0xFB, 0xF2, 0x7E]), bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))
        rom = rom.replace(bytearray([0xAF, 0x16, 0xF2, 0x7E, 0x29, 0x7F, 0x8F, 0x16, 0xF2, 0x7E]), bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))
        rom = rom.replace(bytearray([0xAF, 0x51, 0xF0, 0x7E, 0x29, 0xFE, 0x8F, 0x51, 0xF0, 0x7E]), bytearray([0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA, 0xEA]))

    # set correct flag for hera basement item
    if world.get_location('[dungeon-L3-1F] Tower of Hera - Freestanding Key').item is not None and world.get_location('[dungeon-L3-1F] Tower of Hera - Freestanding Key').item.name == 'Small Key (Tower of Hera)':
        write_byte(rom, 0x4E3BB, 0xE4)
    else:
        write_byte(rom, 0x4E3BB, 0xEB)

    # write strings
    write_string_to_rom(rom, 'Ganon2', 'Did you find the silver arrows in Hyrule?')
    write_string_to_rom(rom, 'Uncle', 'Good Luck!\nYou will need it.')
    write_string_to_rom(rom, 'Triforce', 'Product has Hole in center. Bad seller, 0 out of 5.')
    write_string_to_rom(rom, 'BombShop1', 'Big Bomb?\nI Uh … Never heard of that. Move along.')
    write_string_to_rom(rom, 'BombShop2', 'Bombs!\nBombs!\nBiggest!\nBestest!\nGreatest!\nBoomest!')
    write_string_to_rom(rom, 'PyramidFairy', 'May I talk to you about our lord and savior, Ganon?')
    write_string_to_rom(rom, 'Sahasrahla1', 'How Did you Find me?')
    write_string_to_rom(rom, 'Sahasrahla2', 'You already got my item, idiot.')
    write_string_to_rom(rom, 'Blind', 'I bet you expected a vision related pun?\n\nNot Today.\n Didn\'t see that coming, did you?')
    write_string_to_rom(rom, 'Ganon1', '\n\n\n\n\n\n\n\n\nWhy are you reading an empty textbox?')
    write_string_to_rom(rom, 'TavernMan', 'Did you know that talking to random NPCs wastes time in a race? I hope this information may be of use to you in the future.')

    altaritem = world.get_location('Altar').item.name if world.get_location('Altar').item is not None else 'Nothing'
    write_string_to_rom(rom, 'Altar', altar_text.get(altaritem, 'Unknown Item.'))

    return rom


def write_byte(rom, address, value):
    rom[address] = value


def write_string_to_rom(rom, target, string):
    address, maxbytes = text_addresses[target]
    for i, byte in enumerate(string_to_alttp_text(string, maxbytes)):
        write_byte(rom, address + i, byte)


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
    parser.add_argument('--shuffle', default='full', const='full', nargs='?', choices=['default', 'simple', 'restricted', 'full', 'madness', 'dungeonsfull', 'dungeonssimple'],
                        help='Select Entrance Shuffling Algorithm. Default is the Vanilla layout. Simple shuffles Dungeon Entrances/Exits between each other and keeps all 4-entrance dungeons confined to one location. All caves outside of death mountain are shuffled in pairs. '
                             'Restricted uses Dungeons shuffling from Simple but freely connects remaining entrances. Full mixes cave and dungeon entrances freely. Madness decouples entrances and exits from each other and shuffles them freely, only ensuring that no fake Light/Dark World happens and '
                             'all locations are reachable. The dungeon variants only mix up dungeons and keep the rest of the overworld vanilla.')
    parser.add_argument('--openrom', default='Open_Base_Rom.sfc', help='Path to a VT21 open normal difficulty rom to use as a base.')
    parser.add_argument('--standardrom', default='Standard_Base_Rom.sfc', help='Path to a VT21 standard normal difficulty rom to use as a base.')
    parser.add_argument('--loglevel', default='info', const='info', nargs='?', choices=['error', 'info', 'warning', 'debug'], help='Select level of logging for output.')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--count', help='Use to batch generate multiple seeds with same settings. If --seed is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with --seed given will produce the same 10 (different) roms each time).', type=int)
    args = parser.parse_args()

    # check if rom for patching is available
    rom_to_use = None
    expected_name = ''
    if args.mode == 'open':
        if os.path.isfile(args.openrom):
            rom_to_use = args.openrom  # ToDo check checksum or some such in future when common base rom is in use
            expected_name = args.openrom
    elif args.mode == 'standard':
        if os.path.isfile(args.standardrom):
            rom_to_use = args.standardrom  # ToDo check checksum or some such in future when common base rom is in use
            expected_name = args.standardrom

    if rom_to_use is None:
        input('Could not find valid base rom for patching at expected path %s. Please run with -h to see help for further information. \nPress Enter to exit.' % expected_name)
        exit(1)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    if args.count is not None:
        seed = args.seed
        for i in range(args.count):
            main(seed=seed, logic=args.logic, mode=args.mode, goal=args.goal, difficulty=args.difficulty, algo=args.algorithm, shuffle=args.shuffle, base_rom=rom_to_use, spoiler=args.create_spoiler)
            seed = random.randint(0, 999999999)
    else:
        main(seed=args.seed, logic=args.logic, mode=args.mode, goal=args.goal, difficulty=args.difficulty, algo=args.algorithm, shuffle=args.shuffle, base_rom=rom_to_use, spoiler=args.create_spoiler)
