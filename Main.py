from collections import OrderedDict
import copy
from itertools import zip_longest
import json
import logging
import os
import random
import time
import zlib

from BaseClasses import World, CollectionState, Item, Region, Location, Shop
from Items import ItemFactory
from Regions import create_regions, create_shops, mark_light_world_regions
from InvertedRegions import create_inverted_regions, mark_dark_world_regions
from EntranceShuffle import link_entrances, link_inverted_entrances
from Rom import patch_rom, patch_race_rom, patch_enemizer, apply_rom_settings, LocalRom, JsonRom, get_hash_string
from Rules import set_rules
from Dungeons import create_dungeons, fill_dungeons, fill_dungeons_restrictive
from Fill import distribute_items_cutoff, distribute_items_staleness, distribute_items_restrictive, flood_items, balance_multiworld_progression
from ItemList import generate_itempool, difficulties, fill_prizes
from Utils import output_path, parse_player_names, get_options, __version__


def main(args, seed=None):
    if args.outputpath:
        os.makedirs(args.outputpath, exist_ok=True)
        output_path.cached_path = args.outputpath

    start = time.perf_counter()

    # initialize the world
    world = World(args.multi, args.shuffle, args.logic, args.mode, args.swords, args.difficulty,
                  args.item_functionality, args.timer, args.progressive.copy(), args.goal, args.algorithm,
                  args.accessibility, args.shuffleganon, args.retro, args.custom, args.customitemarray, args.hints)
    logger = logging.getLogger('')
    if seed is None:
        random.seed(None)
        world.seed = random.randint(0, 999999999)
    else:
        world.seed = int(seed)
    random.seed(world.seed)

    world.remote_items = args.remote_items.copy()
    world.mapshuffle = args.mapshuffle.copy()
    world.compassshuffle = args.compassshuffle.copy()
    world.keyshuffle = args.keyshuffle.copy()
    world.bigkeyshuffle = args.bigkeyshuffle.copy()
    world.crystals_needed_for_ganon = {player: random.randint(0, 7) if args.crystals_ganon[player] == 'random' else int(args.crystals_ganon[player]) for player in range(1, world.players + 1)}
    world.crystals_needed_for_gt = {player: random.randint(0, 7) if args.crystals_gt[player] == 'random' else int(args.crystals_gt[player]) for player in range(1, world.players + 1)}
    world.open_pyramid = args.openpyramid.copy()
    world.boss_shuffle = args.shufflebosses.copy()
    world.enemy_shuffle = args.shuffleenemies.copy()
    world.enemy_health = args.enemy_health.copy()
    world.enemy_damage = args.enemy_damage.copy()
    world.beemizer = args.beemizer.copy()
    world.timer = args.timer.copy()
    world.shufflepots = args.shufflepots.copy()
    world.progressive = args.progressive.copy()
    world.dungeon_counters = args.dungeon_counters.copy()
    world.extendedmsu = args.extendedmsu.copy()
    world.glitch_boots = args.glitch_boots.copy()

    world.rom_seeds = {player: random.randint(0, 999999999) for player in range(1, world.players + 1)}

    logger.info('ALttP Berserker\'s Multiworld Version %s  -  Seed: %s\n', __version__, world.seed)

    parsed_names = parse_player_names(args.names, world.players, args.teams)
    world.teams = len(parsed_names)
    for i, team in enumerate(parsed_names, 1):
        if world.players > 1:
            logger.info('%s%s', 'Team%d: ' % i if world.teams > 1 else 'Players: ', ', '.join(team))
        for player, name in enumerate(team, 1):
            world.player_names[player].append(name)

    logger.info('')

    for player in range(1, world.players + 1):
        world.difficulty_requirements[player] = difficulties[world.difficulty[player]]

        if world.mode[player] == 'standard' and world.enemy_shuffle[player] != 'none':
            world.escape_assist[player].append('bombs') # enemized escape assumes infinite bombs available and will likely be unbeatable without it

        for tok in filter(None, args.startinventory[player].split(',')):
            item = ItemFactory(tok.strip(), player)
            if item:
                world.push_precollected(item)

        if world.mode[player] != 'inverted':
            create_regions(world, player)
        else:
            create_inverted_regions(world, player)
        create_shops(world, player)
        create_dungeons(world, player)

    logger.info('Shuffling the World about.')

    for player in range(1, world.players + 1):
        if world.mode[player] != 'inverted':
            link_entrances(world, player)
            mark_light_world_regions(world, player)
        else:
            link_inverted_entrances(world, player)
            mark_dark_world_regions(world, player)

    logger.info('Generating Item Pool.')

    for player in range(1, world.players + 1):
        generate_itempool(world, player)

    logger.info('Calculating Access Rules.')

    for player in range(1, world.players + 1):
        set_rules(world, player)

    logger.info('Placing Dungeon Prizes.')

    fill_prizes(world)

    logger.info('Placing Dungeon Items.')

    shuffled_locations = None
    if args.algorithm in ['balanced', 'vt26'] or any(list(args.mapshuffle.values()) + list(args.compassshuffle.values()) +
                                                     list(args.keyshuffle.values()) + list(args.bigkeyshuffle.values())):
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
        distribute_items_restrictive(world, False)
    elif args.algorithm == 'vt26':

        distribute_items_restrictive(world, True, shuffled_locations)
    elif args.algorithm == 'balanced':
        distribute_items_restrictive(world, True)

    if world.players > 1:
        logger.info('Balancing multiworld progression.')
        balance_multiworld_progression(world)

    logger.info('Patching ROM.')

    outfilebase = 'ER_%s' % (args.outputname if args.outputname else world.seed)

    rom_names = []
    jsonout = {}

    def _gen_rom(team: int, player: int):
        sprite_random_on_hit = type(args.sprite[player]) is str and args.sprite[player].lower() == 'randomonhit'
        use_enemizer = (world.boss_shuffle[player] != 'none' or world.enemy_shuffle[player] != 'none'
                        or world.enemy_health[player] != 'default' or world.enemy_damage[player] != 'default'
                        or args.shufflepots[player] or sprite_random_on_hit)

        rom = JsonRom() if args.jsonout or use_enemizer else LocalRom(args.rom, extendedmsu=args.extendedmsu[player])

        patch_rom(world, rom, player, team, use_enemizer)

        if use_enemizer and (args.enemizercli or not args.jsonout):
            patch_enemizer(world, player, rom, args.rom, args.enemizercli, args.shufflepots[player],
                           sprite_random_on_hit, extendedmsu=args.extendedmsu[player])
            if not args.jsonout:
                rom = LocalRom.fromJsonRom(rom, args.rom, 0x400000, args.extendedmsu[player])

        if args.race:
            patch_race_rom(rom)

        world.spoiler.hashes[(player, team)] = get_hash_string(rom.hash)

        apply_rom_settings(rom, args.heartbeep[player], args.heartcolor[player], args.quickswap[player],
                           args.fastmenu[player], args.disablemusic[player], args.sprite[player],
                           args.ow_palettes[player], args.uw_palettes[player])

        if args.jsonout:
            jsonout[f'patch_t{team}_p{player}'] = rom.patches
        else:
            mcsb_name = ''
            if all([world.mapshuffle[player], world.compassshuffle[player], world.keyshuffle[player],
                    world.bigkeyshuffle[player]]):
                mcsb_name = '-keysanity'
            elif [world.mapshuffle[player], world.compassshuffle[player], world.keyshuffle[player],
                  world.bigkeyshuffle[player]].count(True) == 1:
                mcsb_name = '-mapshuffle' if world.mapshuffle[player] else '-compassshuffle' if world.compassshuffle[
                    player] else '-keyshuffle' if world.keyshuffle[player] else '-bigkeyshuffle'
            elif any([world.mapshuffle[player], world.compassshuffle[player], world.keyshuffle[player],
                      world.bigkeyshuffle[player]]):
                mcsb_name = '-%s%s%s%sshuffle' % (
                    'M' if world.mapshuffle[player] else '', 'C' if world.compassshuffle[player] else '',
                    'S' if world.keyshuffle[player] else '', 'B' if world.bigkeyshuffle[player] else '')

            outfilepname = f'_T{team + 1}' if world.teams > 1 else ''
            if world.players > 1:
                outfilepname += f'_P{player}'
            if world.players > 1 or world.teams > 1:
                outfilepname += f"_{world.player_names[player][team].replace(' ', '_')}" if world.player_names[player][
                                                                                                team] != 'Player%d' % player else ''
            outfilesuffix = ('_%s_%s-%s-%s-%s%s_%s-%s%s%s%s%s' % (world.logic[player], world.difficulty[player],
                                                                  world.difficulty_adjustments[player],
                                                                  world.mode[player], world.goal[player],
                                                                  "" if world.timer[player] in [False,
                                                                                                'display'] else "-" +
                                                                                                                world.timer[
                                                                                                                    player],
                                                                  world.shuffle[player], world.algorithm,
                                                                  mcsb_name,
                                                                  "-retro" if world.retro[player] else "",
                                                                  "-prog_" + world.progressive[player] if
                                                                  world.progressive[player] in ['off',
                                                                                                'random'] else "",
                                                                  "-nohints" if not world.hints[
                                                                      player] else "")) if not args.outputname else ''
            rompath = output_path(f'{outfilebase}{outfilepname}{outfilesuffix}.sfc')
            rom.write_to_file(rompath)
            if args.create_diff:
                import Patch
                Patch.create_patch_file(rompath)
        return (player, team, list(rom.name))

    if not args.suppress_rom:
        import concurrent.futures
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as pool:
            for team in range(world.teams):
                for player in range(1, world.players + 1):
                    futures.append(pool.submit(_gen_rom, team, player))
        for future in futures:
            rom_name = future.result()
            rom_names.append(rom_name)
        multidata = zlib.compress(json.dumps({"names": parsed_names,
                                              "roms": rom_names,
                                              "remote_items": [player for player in range(1, world.players + 1) if
                                                               world.remote_items[player]],
                                              "locations": [((location.address, location.player),
                                                             (location.item.code, location.item.player))
                                                            for location in world.get_filled_locations() if
                                                            type(location.address) is int],
                                              "server_options": get_options()["server_options"]
                                              }).encode("utf-8"))
        if args.jsonout:
            jsonout["multidata"] = list(multidata)
        else:
            with open(output_path('%s_multidata' % outfilebase), 'wb') as f:
                f.write(multidata)

    if not args.skip_playthrough:
        logger.info('Calculating playthrough.')
        create_playthrough(world)

    if args.jsonout:
        print(json.dumps({**jsonout, 'spoiler': world.spoiler.to_json()}))
    elif args.create_spoiler and not args.skip_playthrough:
        world.spoiler.to_file(output_path('%s_Spoiler.txt' % outfilebase))

    logger.info('Done. Enjoy.')
    logger.debug('Total Time: %s', time.perf_counter() - start)

    return world


def copy_world(world):
    # ToDo: Not good yet
    ret = World(world.players, world.shuffle, world.logic, world.mode, world.swords, world.difficulty, world.difficulty_adjustments, world.timer, world.progressive, world.goal, world.algorithm, world.accessibility, world.shuffle_ganon, world.retro, world.custom, world.customitemarray, world.hints)
    ret.teams = world.teams
    ret.player_names = copy.deepcopy(world.player_names)
    ret.remote_items = world.remote_items.copy()
    ret.required_medallions = world.required_medallions.copy()
    ret.swamp_patch_required = world.swamp_patch_required.copy()
    ret.ganon_at_pyramid = world.ganon_at_pyramid.copy()
    ret.powder_patch_required = world.powder_patch_required.copy()
    ret.ganonstower_vanilla = world.ganonstower_vanilla.copy()
    ret.treasure_hunt_count = world.treasure_hunt_count.copy()
    ret.treasure_hunt_icon = world.treasure_hunt_icon.copy()
    ret.sewer_light_cone = world.sewer_light_cone.copy()
    ret.light_world_light_cone = world.light_world_light_cone
    ret.dark_world_light_cone = world.dark_world_light_cone
    ret.seed = world.seed
    ret.can_access_trock_eyebridge = world.can_access_trock_eyebridge.copy()
    ret.can_access_trock_front = world.can_access_trock_front.copy()
    ret.can_access_trock_big_chest = world.can_access_trock_big_chest.copy()
    ret.can_access_trock_middle = world.can_access_trock_middle.copy()
    ret.can_take_damage = world.can_take_damage
    ret.difficulty_requirements = world.difficulty_requirements.copy()
    ret.fix_fake_world = world.fix_fake_world.copy()
    ret.lamps_needed_for_dark_rooms = world.lamps_needed_for_dark_rooms
    ret.mapshuffle = world.mapshuffle.copy()
    ret.compassshuffle = world.compassshuffle.copy()
    ret.keyshuffle = world.keyshuffle.copy()
    ret.bigkeyshuffle = world.bigkeyshuffle.copy()
    ret.crystals_needed_for_ganon = world.crystals_needed_for_ganon.copy()
    ret.crystals_needed_for_gt = world.crystals_needed_for_gt.copy()
    ret.open_pyramid = world.open_pyramid.copy()
    ret.boss_shuffle = world.boss_shuffle.copy()
    ret.enemy_shuffle = world.enemy_shuffle.copy()
    ret.enemy_health = world.enemy_health.copy()
    ret.enemy_damage = world.enemy_damage.copy()
    ret.beemizer = world.beemizer.copy()
    ret.timer = world.timer.copy()
    ret.shufflepots = world.shufflepots.copy()
    ret.extendedmsu = world.extendedmsu.copy()
    ret.regions = [copy.copy(region) for region in world.regions]
    ret.shops = [copy.copy(shop) for shop in world.shops]
    ret.dungeons = [copy.copy(dungeon) for dungeon in world.dungeons]
    ret.itempool = world.itempool
    ret.precollected_items = world.precollected_items.copy()

    for shop in ret.shops:
        shop.inventory = shop.inventory.copy()

    ret.initialize_regions()

    # Copy locations
    for region in ret.regions:
        region.locations = [copy.copy(location) for location in region.locations]
        for location in region.locations:
            location.parent_region = region
        region.entrances = [copy.copy(entrance) for entrance in region.entrances]
        for entrance in region.entrances:
            entrance.connected_region = region
            entrance.parent_region = ret.get_region(entrance.parent_region.name, entrance.parent_region.player)
        region.exits = [copy.copy(exit) for exit in region.exits]
        for exit in region.exits:
            exit.parent_region = region
            exit.connected_region = ret.get_region(entrance.connected_region.name, entrance.connected_region.player)

    # copy state
    ret.state = ret.state.copy()
    ret.state.world = ret
    ret.state.prog_items = world.state.prog_items.copy()
    ret.state.stale = {player: True for player in range(1, world.players + 1)}

    return ret


def create_playthrough(world):
    # create a copy as we will modify it
    old_world = world
    world = copy_world(world)

    # if we only check for beatable, we can do this sanity check first before writing down spheres
    if not world.can_beat_game():
        raise RuntimeError('Cannot beat game. Something went terribly wrong here!')

    # get locations containing progress items
    prog_locations = [location for location in world.get_filled_locations() if location.item.advancement]
    state_cache = [None]
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
            state.collect(location.item, True, location)

        collection_spheres.append(sphere)

        state_cache.append(state.copy())

        logging.getLogger('').debug('Calculated sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere), len(prog_locations))
        if not sphere:
            logging.getLogger('').debug('The following items could not be reached: %s', ['%s (Player %d) at %s (Player %d)' % (location.item.name, location.item.player, location.name, location.player) for location in sphere_candidates])
            if any([world.accessibility[location.item.player] != 'none' for location in sphere_candidates]):
                raise RuntimeError('Not all progression items reachable. Something went terribly wrong here.')
            else:
                old_world.spoiler.unreachables = sphere_candidates.copy()
                break

    # in the second phase, we cull each sphere such that the game is still beatable, reducing each range of influence to the bare minimum required inside it
    for num, sphere in reversed(list(enumerate(collection_spheres))):
        to_delete = []
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            logging.getLogger('').debug('Checking if %s (Player %d) is required to beat the game.', location.item.name, location.item.player)
            old_item = location.item
            location.item = None
            if world.can_beat_game(state_cache[num]):
                to_delete.append(location)
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        for location in to_delete:
            sphere.remove(location)

    # second phase, sphere 0
    for item in [i for i in world.precollected_items if i.advancement]:
        logging.getLogger('').debug('Checking if %s (Player %d) is required to beat the game.', item.name, item.player)
        world.precollected_items.remove(item)
        world.state.remove(item)
        if not world.can_beat_game():
            world.push_precollected(item)

    # we are now down to just the required progress items in collection_spheres. Unfortunately
    # the previous pruning stage could potentially have made certain items dependant on others
    # in the same or later sphere (because the location had 2 ways to access but the item originally
    # used to access it was deemed not required.) So we need to do one final sphere collection pass
    # to build up the correct spheres

    required_locations = [item for sphere in collection_spheres for item in sphere]
    state = CollectionState(world)
    collection_spheres = []
    while required_locations:
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
    old_world.required_locations = [(location.name, location.player) for sphere in collection_spheres for location in sphere]

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

    old_world.spoiler.paths = dict()
    for player in range(1, world.players + 1):
        old_world.spoiler.paths.update({ str(location) : get_path(state, location.parent_region) for sphere in collection_spheres for location in sphere if location.player == player})
        for _, path in dict(old_world.spoiler.paths).items():
            if any(exit == 'Pyramid Fairy' for (_, exit) in path):
                if world.mode[player] != 'inverted':
                    old_world.spoiler.paths[str(world.get_region('Big Bomb Shop', player))] = get_path(state, world.get_region('Big Bomb Shop', player))
                else:
                    old_world.spoiler.paths[str(world.get_region('Inverted Big Bomb Shop', player))] = get_path(state, world.get_region('Inverted Big Bomb Shop', player))

    # we can finally output our playthrough
    old_world.spoiler.playthrough = OrderedDict([("0", [str(item) for item in world.precollected_items if item.advancement])])
    for i, sphere in enumerate(collection_spheres):
        old_world.spoiler.playthrough[str(i + 1)] = {str(location): str(location.item) for location in sphere}
