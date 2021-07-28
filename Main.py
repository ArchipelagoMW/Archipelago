from itertools import zip_longest
import logging
import os
import random
import time
import zlib
import concurrent.futures
import pickle
import tempfile
import zipfile
from typing import Dict, Tuple

from BaseClasses import MultiWorld, CollectionState, Region, RegionType
from worlds.alttp.Items import item_name_groups
from worlds.alttp.Regions import lookup_vanilla_location_to_entrance
from Fill import distribute_items_restrictive, flood_items, balance_multiworld_progression, distribute_planned
from worlds.alttp.Shops import ShopSlotFill, SHOP_ID_START, total_shop_slots, FillDisabledShopSlots
from worlds.alttp.ItemPool import difficulties
from Utils import output_path, get_options, __version__, version_tuple
from worlds.generic.Rules import locality_rules, exclusion_rules
from worlds import AutoWorld
from variaRandomizer.logic.logic import Logic

seeddigits = 20


def get_seed(seed=None):
    if seed is None:
        random.seed(None)
        return random.randint(0, pow(10, seeddigits) - 1)
    return seed


def get_same_seed(world: MultiWorld, seed_def: tuple) -> str:
    seeds: Dict[tuple, str] = getattr(world, "__named_seeds", {})
    if seed_def in seeds:
        return seeds[seed_def]
    seeds[seed_def] = str(world.random.randint(0, 2 ** 64))
    world.__named_seeds = seeds
    return seeds[seed_def]


def main(args, seed=None):
    if args.outputpath:
        os.makedirs(args.outputpath, exist_ok=True)
        output_path.cached_path = args.outputpath

    start = time.perf_counter()
    Logic.factory('vanilla')
    # initialize the world
    world = MultiWorld(args.multi)

    logger = logging.getLogger('')
    world.seed = get_seed(seed)
    if args.race:
        world.secure()
    else:
        world.random.seed(world.seed)
    world.seed_name = str(args.outputname if args.outputname else world.seed)

    world.shuffle = args.shuffle.copy()
    world.logic = args.logic.copy()
    world.mode = args.mode.copy()
    world.swordless = args.swordless.copy()
    world.difficulty = args.difficulty.copy()
    world.item_functionality = args.item_functionality.copy()
    world.timer = args.timer.copy()
    world.goal = args.goal.copy()
    world.local_items = args.local_items.copy()
    if hasattr(args, "algorithm"):  # current GUI options
        world.algorithm = args.algorithm
        world.shuffleganon = args.shuffleganon
        world.custom = args.custom
        world.customitemarray = args.customitemarray

    world.accessibility = args.accessibility.copy()
    world.retro = args.retro.copy()

    world.hints = args.hints.copy()

    world.mapshuffle = args.mapshuffle.copy()
    world.compassshuffle = args.compassshuffle.copy()
    world.keyshuffle = args.keyshuffle.copy()
    world.bigkeyshuffle = args.bigkeyshuffle.copy()
    world.open_pyramid = args.open_pyramid.copy()
    world.boss_shuffle = args.shufflebosses.copy()
    world.enemy_shuffle = args.enemy_shuffle.copy()
    world.enemy_health = args.enemy_health.copy()
    world.enemy_damage = args.enemy_damage.copy()
    world.killable_thieves = args.killable_thieves.copy()
    world.bush_shuffle = args.bush_shuffle.copy()
    world.tile_shuffle = args.tile_shuffle.copy()
    world.beemizer = args.beemizer.copy()
    world.timer = args.timer.copy()
    world.countdown_start_time = args.countdown_start_time.copy()
    world.red_clock_time = args.red_clock_time.copy()
    world.blue_clock_time = args.blue_clock_time.copy()
    world.green_clock_time = args.green_clock_time.copy()
    world.shufflepots = args.shufflepots.copy()
    world.dungeon_counters = args.dungeon_counters.copy()
    world.glitch_boots = args.glitch_boots.copy()
    world.triforce_pieces_available = args.triforce_pieces_available.copy()
    world.triforce_pieces_required = args.triforce_pieces_required.copy()
    world.shop_shuffle = args.shop_shuffle.copy()
    world.progression_balancing = args.progression_balancing.copy()
    world.shuffle_prizes = args.shuffle_prizes.copy()
    world.sprite_pool = args.sprite_pool.copy()
    world.dark_room_logic = args.dark_room_logic.copy()
    world.plando_items = args.plando_items.copy()
    world.plando_texts = args.plando_texts.copy()
    world.plando_connections = args.plando_connections.copy()
    world.er_seeds = getattr(args, "er_seeds", {})
    world.restrict_dungeon_item_on_boss = args.restrict_dungeon_item_on_boss.copy()
    world.required_medallions = args.required_medallions.copy()
    world.game = args.game.copy()
    world.set_options(args)
    world.player_name = args.name.copy()
    world.alttp_rom = args.rom
    world.enemizer = args.enemizercli
    world.sprite = args.sprite.copy()
    world.glitch_triforce = args.glitch_triforce  # This is enabled/disabled globally, no per player option.

    world.slot_seeds = {player: random.Random(world.random.getrandbits(64)) for player in
                        range(1, world.players + 1)}

    AutoWorld.call_all(world, "generate_early")

    # system for sharing ER layouts
    for player in world.get_game_players("A Link to the Past"):
        world.er_seeds[player] = str(world.random.randint(0, 2 ** 64))

        if "-" in world.shuffle[player]:
            shuffle, seed = world.shuffle[player].split("-", 1)
            world.shuffle[player] = shuffle
            if shuffle == "vanilla":
                world.er_seeds[player] = "vanilla"
            elif seed.startswith("group-") or args.race:
                world.er_seeds[player] = get_same_seed(world, (
                shuffle, seed, world.retro[player], world.mode[player], world.logic[player]))
            else:  # not a race or group seed, use set seed as is.
                world.er_seeds[player] = seed
        elif world.shuffle[player] == "vanilla":
            world.er_seeds[player] = "vanilla"

    logger.info('Archipelago Version %s  -  Seed: %s\n', __version__, world.seed)

    logger.info("Found World Types:")
    longest_name = max(len(text) for text in AutoWorld.AutoWorldRegister.world_types)
    for name, cls in AutoWorld.AutoWorldRegister.world_types.items():
        logger.info(f"  {name:{longest_name}}: {len(cls.item_names):3} Items | {len(cls.location_names):3} Locations")


    logger.info('')
    for player in world.get_game_players("A Link to the Past"):
        world.difficulty_requirements[player] = difficulties[world.difficulty[player]]

    for player in world.player_ids:
        for item_name in args.startinventory[player]:
            world.push_precollected(world.create_item(item_name, player))

    for player in world.player_ids:
        if player in world.get_game_players("A Link to the Past"):
            # enforce pre-defined local items.
            if world.goal[player] in ["localtriforcehunt", "localganontriforcehunt"]:
                world.local_items[player].add('Triforce Piece')

            # dungeon items can't be in non-local if the appropriate dungeon item shuffle setting is not set.
            if not world.mapshuffle[player]:
                world.non_local_items[player] -= item_name_groups['Maps']

            if not world.compassshuffle[player]:
                world.non_local_items[player] -= item_name_groups['Compasses']

            if not world.keyshuffle[player]:
                world.non_local_items[player] -= item_name_groups['Small Keys']
            # This could probably use a more elegant solution.
            elif world.keyshuffle[player] == True and world.mode[player] == "Standard":
                world.local_items[player].add("Small Key (Hyrule Castle)")
            if not world.bigkeyshuffle[player]:
                world.non_local_items[player] -= item_name_groups['Big Keys']

            # Not possible to place pendants/crystals out side of boss prizes yet.
            world.non_local_items[player] -= item_name_groups['Pendants']
            world.non_local_items[player] -= item_name_groups['Crystals']

        # items can't be both local and non-local, prefer local
        world.non_local_items[player] -= world.local_items[player]

    logger.info('Creating World.')
    AutoWorld.call_all(world, "create_regions")

    logger.info('Creating Items.')
    AutoWorld.call_all(world, "create_items")

    logger.info('Calculating Access Rules.')
    if world.players > 1:
        for player in world.player_ids:
            locality_rules(world, player)

    AutoWorld.call_all(world, "set_rules")

    for player in world.player_ids:
        exclusion_rules(world, player, args.excluded_locations[player])

    AutoWorld.call_all(world, "generate_basic")

    logger.info("Running Item Plando")

    for item in world.itempool:
        item.world = world

    distribute_planned(world)

    logger.info('Running Pre Main Fill.')

    AutoWorld.call_all(world, "pre_fill")

    logger.info('Fill the world.')

    if world.algorithm == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    elif world.algorithm == 'vt25':
        distribute_items_restrictive(world, False)
    elif world.algorithm == 'vt26':
        distribute_items_restrictive(world, True)
    elif world.algorithm == 'balanced':
        distribute_items_restrictive(world, True)

    logger.info("Filling Shop Slots")

    ShopSlotFill(world)

    #if world.players > 1:
    #    balance_multiworld_progression(world)

    logger.info('Generating output files.')
    outfilebase = 'AP_' + world.seed_name

    pool = concurrent.futures.ThreadPoolExecutor()

    output = tempfile.TemporaryDirectory()
    with output as temp_dir:
        check_accessibility_task = pool.submit(world.fulfills_accessibility)

        output_file_futures = []

        for player in world.player_ids:
            output_file_futures.append(pool.submit(AutoWorld.call_single, world, "generate_output", player, temp_dir))
        output_file_futures.append(pool.submit(AutoWorld.call_stage, world, "generate_output", temp_dir))

        def get_entrance_to_region(region: Region):
            for entrance in region.entrances:
                if entrance.parent_region.type in (RegionType.DarkWorld, RegionType.LightWorld, RegionType.Generic):
                    return entrance
            for entrance in region.entrances:  # BFS might be better here, trying DFS for now.
                return get_entrance_to_region(entrance.parent_region)

        # collect ER hint info
        er_hint_data = {player: {} for player in world.get_game_players("A Link to the Past") if
                        world.shuffle[player] != "vanilla" or world.retro[player]}

        for region in world.regions:
            if region.player in er_hint_data and region.locations:
                main_entrance = get_entrance_to_region(region)
                for location in region.locations:
                    if type(location.address) == int:  # skips events and crystals
                        if lookup_vanilla_location_to_entrance[location.address] != main_entrance.name:
                            er_hint_data[region.player][location.address] = main_entrance.name

        ordered_areas = ('Light World', 'Dark World', 'Hyrule Castle', 'Agahnims Tower', 'Eastern Palace', 'Desert Palace',
                         'Tower of Hera', 'Palace of Darkness', 'Swamp Palace', 'Skull Woods', 'Thieves Town', 'Ice Palace',
                         'Misery Mire', 'Turtle Rock', 'Ganons Tower', "Total")

        checks_in_area = {player: {area: list() for area in ordered_areas}
                          for player in range(1, world.players + 1)}

        for player in range(1, world.players + 1):
            checks_in_area[player]["Total"] = 0

        for location in [loc for loc in world.get_filled_locations() if type(loc.address) is int]:
            main_entrance = get_entrance_to_region(location.parent_region)
            if location.game != "A Link to the Past":
                checks_in_area[location.player]["Light World"].append(location.address)
            elif location.parent_region.dungeon:
                dungeonname = {'Inverted Agahnims Tower': 'Agahnims Tower',
                               'Inverted Ganons Tower': 'Ganons Tower'} \
                    .get(location.parent_region.dungeon.name, location.parent_region.dungeon.name)
                checks_in_area[location.player][dungeonname].append(location.address)
            elif main_entrance.parent_region.type == RegionType.LightWorld:
                checks_in_area[location.player]["Light World"].append(location.address)
            elif main_entrance.parent_region.type == RegionType.DarkWorld:
                checks_in_area[location.player]["Dark World"].append(location.address)
            checks_in_area[location.player]["Total"] += 1

        oldmancaves = []
        takeanyregions = ["Old Man Sword Cave", "Take-Any #1", "Take-Any #2", "Take-Any #3", "Take-Any #4"]
        for index, take_any in enumerate(takeanyregions):
            for region in [world.get_region(take_any, player) for player in range(1, world.players + 1) if
                           world.retro[player]]:
                item = world.create_item(region.shop.inventory[(0 if take_any == "Old Man Sword Cave" else 1)]['item'],
                                         region.player)
                player = region.player
                location_id = SHOP_ID_START + total_shop_slots + index

                main_entrance = get_entrance_to_region(region)
                if main_entrance.parent_region.type == RegionType.LightWorld:
                    checks_in_area[player]["Light World"].append(location_id)
                else:
                    checks_in_area[player]["Dark World"].append(location_id)
                checks_in_area[player]["Total"] += 1

                er_hint_data[player][location_id] = main_entrance.name
                oldmancaves.append(((location_id, player), (item.code, player)))

        FillDisabledShopSlots(world)

        def write_multidata():
            import NetUtils
            slot_data = {}
            client_versions = {}
            minimum_versions = {"server": (0, 1, 1), "clients": client_versions}
            games = {}
            for slot in world.player_ids:
                client_versions[slot] = world.worlds[slot].get_required_client_version()
                games[slot] = world.game[slot]
            precollected_items = {player: [] for player in range(1, world.players + 1)}
            for item in world.precollected_items:
                precollected_items[item.player].append(item.code)
            precollected_hints = {player: set() for player in range(1, world.players + 1)}
            # for now special case Factorio tech_tree_information
            sending_visible_players = set()
            for player in world.get_game_players("Factorio"):
                if world.tech_tree_information[player].value == 2:
                    sending_visible_players.add(player)

            for slot in world.player_ids:
                slot_data[slot] = world.worlds[slot].fill_slot_data()

            locations_data: Dict[int, Dict[int, Tuple[int, int]]] = {player: {} for player in world.player_ids}
            for location in world.get_filled_locations():
                if type(location.address) == int:
                    locations_data[location.player][location.address] = location.item.code, location.item.player
                    if location.player in sending_visible_players and location.item.player != location.player:
                        hint = NetUtils.Hint(location.item.player, location.player, location.address,
                                             location.item.code, False)
                        precollected_hints[location.player].add(hint)
                        precollected_hints[location.item.player].add(hint)
                    elif location.item.name in args.start_hints[location.item.player]:
                        hint = NetUtils.Hint(location.item.player, location.player, location.address,
                                             location.item.code, False,
                                             er_hint_data.get(location.player, {}).get(location.address, ""))
                        precollected_hints[location.player].add(hint)
                        precollected_hints[location.item.player].add(hint)

            multidata = {
                "slot_data": slot_data,
                "games": games,
                "names": [{player: name for player, name in world.player_name.items()}],
                "connect_names": {name: (0, player) for player, name in world.player_name.items()},
                "remote_items": {player for player in world.player_ids if
                                 world.worlds[player].remote_items},
                "locations": locations_data,
                "checks_in_area": checks_in_area,
                "server_options": get_options()["server_options"],
                "er_hint_data": er_hint_data,
                "precollected_items": precollected_items,
                "precollected_hints": precollected_hints,
                "version": tuple(version_tuple),
                "tags": ["AP"],
                "minimum_versions": minimum_versions,
                "seed_name": world.seed_name
            }
            AutoWorld.call_all(world, "modify_multidata", multidata)

            multidata = zlib.compress(pickle.dumps(multidata), 9)

            with open(os.path.join(temp_dir, f'{outfilebase}.archipelago'), 'wb') as f:
                f.write(bytes([1]))  # version of format
                f.write(multidata)


        multidata_task = pool.submit(write_multidata)
        if not check_accessibility_task.result():
            if not world.can_beat_game():
                raise Exception("Game appears as unbeatable. Aborting.")
            else:
                logger.warning("Location Accessibility requirements not fulfilled.")
        if multidata_task:
            multidata_task.result()  # retrieve exception if one exists
        pool.shutdown()  # wait for all queued tasks to complete
        if not args.skip_playthrough:
            logger.info('Calculating playthrough.')
            create_playthrough(world)
        if args.create_spoiler:
            world.spoiler.to_file(os.path.join(temp_dir, '%s_Spoiler.txt' % outfilebase))
        for future in output_file_futures:
            future.result()
        zipfilename = output_path(f"AP_{world.seed_name}.zip")
        logger.info(f'Creating final archive at {zipfilename}.')
        with zipfile.ZipFile(zipfilename, mode="w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zf:
            for file in os.scandir(temp_dir):
                zf.write(os.path.join(temp_dir, file), arcname=file.name)

    logger.info('Done. Enjoy. Total Time: %s', time.perf_counter() - start)
    return world


def create_playthrough(world):
    """Destructive to the world while it is run, damage gets repaired afterwards."""
    # get locations containing progress items
    prog_locations = {location for location in world.get_filled_locations() if location.item.advancement}
    state_cache = [None]
    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = set(prog_locations)
    logging.debug('Building up collection spheres.')
    while sphere_candidates:
        state.sweep_for_events(key_only=True)

        # build up spheres of collection radius.
        # Everything in each sphere is independent from each other in dependencies and only depends on lower spheres

        sphere = {location for location in sphere_candidates if state.can_reach(location)}

        for location in sphere:
            state.collect(location.item, True, location)

        sphere_candidates -= sphere
        collection_spheres.append(sphere)
        state_cache.append(state.copy())

        logging.debug('Calculated sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere),
                      len(prog_locations))
        if not sphere:
            logging.debug('The following items could not be reached: %s', ['%s (Player %d) at %s (Player %d)' % (
                location.item.name, location.item.player, location.name, location.player) for location in
                                                                           sphere_candidates])
            if any([world.accessibility[location.item.player] != 'none' for location in sphere_candidates]):
                raise RuntimeError(f'Not all progression items reachable ({sphere_candidates}). '
                                   f'Something went terribly wrong here.')
            else:
                world.spoiler.unreachables = sphere_candidates
                break

    # in the second phase, we cull each sphere such that the game is still beatable,
    # reducing each range of influence to the bare minimum required inside it
    restore_later = {}
    for num, sphere in reversed(tuple(enumerate(collection_spheres))):
        to_delete = set()
        for location in sphere:
            # we remove the item at location and check if game is still beatable
            logging.debug('Checking if %s (Player %d) is required to beat the game.', location.item.name,
                          location.item.player)
            old_item = location.item
            location.item = None
            if world.can_beat_game(state_cache[num]):
                to_delete.add(location)
                restore_later[location] = old_item
            else:
                # still required, got to keep it around
                location.item = old_item

        # cull entries in spheres for spoiler walkthrough at end
        sphere -= to_delete

    # second phase, sphere 0
    removed_precollected = []
    for item in (i for i in world.precollected_items if i.advancement):
        logging.debug('Checking if %s (Player %d) is required to beat the game.', item.name, item.player)
        world.precollected_items.remove(item)
        world.state.remove(item)
        if not world.can_beat_game():
            world.push_precollected(item)
        else:
            removed_precollected.append(item)

    # we are now down to just the required progress items in collection_spheres. Unfortunately
    # the previous pruning stage could potentially have made certain items dependant on others
    # in the same or later sphere (because the location had 2 ways to access but the item originally
    # used to access it was deemed not required.) So we need to do one final sphere collection pass
    # to build up the correct spheres

    required_locations = {item for sphere in collection_spheres for item in sphere}
    state = CollectionState(world)
    collection_spheres = []
    while required_locations:
        state.sweep_for_events(key_only=True)

        sphere = set(filter(state.can_reach, required_locations))

        for location in sphere:
            state.collect(location.item, True, location)

        required_locations -= sphere

        collection_spheres.append(sphere)

        logging.debug('Calculated final sphere %i, containing %i of %i progress items.', len(collection_spheres),
                      len(sphere), len(required_locations))
        if not sphere:
            raise RuntimeError(f'Not all required items reachable. Unreachable locations: {required_locations}')

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

    world.spoiler.paths = {}
    topology_worlds = (player for player in world.player_ids if world.worlds[player].topology_present)
    for player in topology_worlds:
        world.spoiler.paths.update(
            {str(location): get_path(state, location.parent_region) for sphere in collection_spheres for location in
             sphere if location.player == player})
        if player in world.get_game_players("A Link to the Past"):
            for path in dict(world.spoiler.paths).values():
                if any(exit == 'Pyramid Fairy' for (_, exit) in path):
                    if world.mode[player] != 'inverted':
                        world.spoiler.paths[str(world.get_region('Big Bomb Shop', player))] = get_path(state,
                                                                                                       world.get_region(
                                                                                                           'Big Bomb Shop',
                                                                                                           player))
                    else:
                        world.spoiler.paths[str(world.get_region('Inverted Big Bomb Shop', player))] = get_path(state,
                                                                                                                world.get_region(
                                                                                                                    'Inverted Big Bomb Shop',
                                                                                                                    player))

    # we can finally output our playthrough
    world.spoiler.playthrough = {"0": sorted([str(item) for item in world.precollected_items if item.advancement])}

    for i, sphere in enumerate(collection_spheres):
        world.spoiler.playthrough[str(i + 1)] = {str(location): str(location.item) for location in sorted(sphere)}

    # repair the world again
    for location, item in restore_later.items():
        location.item = item

    for item in removed_precollected:
        world.push_precollected(item)
