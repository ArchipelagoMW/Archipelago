from itertools import zip_longest, chain
import logging
import os
import time
import zlib
import concurrent.futures
import pickle
import tempfile
import zipfile
from typing import Dict, Tuple, Optional

from BaseClasses import MultiWorld, CollectionState, Region, RegionType
from worlds.alttp.Items import item_name_groups
from worlds.alttp.Regions import lookup_vanilla_location_to_entrance
from Fill import distribute_items_restrictive, flood_items, balance_multiworld_progression, distribute_planned
from worlds.alttp.Shops import SHOP_ID_START, total_shop_slots, FillDisabledShopSlots
from Utils import output_path, get_options, __version__, version_tuple
from worlds.generic.Rules import locality_rules, exclusion_rules
from worlds import AutoWorld


ordered_areas = (
    'Light World', 'Dark World', 'Hyrule Castle', 'Agahnims Tower', 'Eastern Palace', 'Desert Palace',
    'Tower of Hera', 'Palace of Darkness', 'Swamp Palace', 'Skull Woods', 'Thieves Town', 'Ice Palace',
    'Misery Mire', 'Turtle Rock', 'Ganons Tower', "Total"
)


def main(args, seed=None, baked_server_options: Optional[Dict[str, object]] = None):
    if not baked_server_options:
        baked_server_options = get_options()["server_options"]
    if args.outputpath:
        os.makedirs(args.outputpath, exist_ok=True)
        output_path.cached_path = args.outputpath

    start = time.perf_counter()
    # initialize the world
    world = MultiWorld(args.multi)

    logger = logging.getLogger()
    world.set_seed(seed, args.race, str(args.outputname if args.outputname else world.seed))

    world.shuffle = args.shuffle.copy()
    world.logic = args.logic.copy()
    world.mode = args.mode.copy()
    world.difficulty = args.difficulty.copy()
    world.item_functionality = args.item_functionality.copy()
    world.timer = args.timer.copy()
    world.goal = args.goal.copy()

    if hasattr(args, "algorithm"):  # current GUI options
        world.algorithm = args.algorithm
        world.shuffleganon = args.shuffleganon
        world.custom = args.custom
        world.customitemarray = args.customitemarray

    world.open_pyramid = args.open_pyramid.copy()
    world.boss_shuffle = args.shufflebosses.copy()
    world.enemy_health = args.enemy_health.copy()
    world.enemy_damage = args.enemy_damage.copy()
    world.beemizer_total_chance = args.beemizer_total_chance.copy()
    world.beemizer_trap_chance = args.beemizer_trap_chance.copy()
    world.timer = args.timer.copy()
    world.countdown_start_time = args.countdown_start_time.copy()
    world.red_clock_time = args.red_clock_time.copy()
    world.blue_clock_time = args.blue_clock_time.copy()
    world.green_clock_time = args.green_clock_time.copy()
    world.dungeon_counters = args.dungeon_counters.copy()
    world.triforce_pieces_available = args.triforce_pieces_available.copy()
    world.triforce_pieces_required = args.triforce_pieces_required.copy()
    world.shop_shuffle = args.shop_shuffle.copy()
    world.shuffle_prizes = args.shuffle_prizes.copy()
    world.sprite_pool = args.sprite_pool.copy()
    world.dark_room_logic = args.dark_room_logic.copy()
    world.plando_items = args.plando_items.copy()
    world.plando_texts = args.plando_texts.copy()
    world.plando_connections = args.plando_connections.copy()
    world.required_medallions = args.required_medallions.copy()
    world.game = args.game.copy()
    world.set_options(args)
    world.player_name = args.name.copy()
    world.enemizer = args.enemizercli
    world.sprite = args.sprite.copy()
    world.glitch_triforce = args.glitch_triforce  # This is enabled/disabled globally, no per player option.

    logger.info('Archipelago Version %s  -  Seed: %s\n', __version__, world.seed)

    logger.info("Found World Types:")
    longest_name = max(len(text) for text in AutoWorld.AutoWorldRegister.world_types)
    numlength = 8
    for name, cls in AutoWorld.AutoWorldRegister.world_types.items():
        if not cls.hidden:
            logger.info(f"  {name:{longest_name}}: {len(cls.item_names):3} Items | "
                        f"{len(cls.location_names):3} Locations")
            logger.info(f"   Item IDs: {min(cls.item_id_to_name):{numlength}} - "
                        f"{max(cls.item_id_to_name):{numlength}} | "
                        f"Location IDs: {min(cls.location_id_to_name):{numlength}} - "
                        f"{max(cls.location_id_to_name):{numlength}}")

    AutoWorld.call_all(world, "generate_early")

    logger.info('')

    for player in world.player_ids:
        for item_name, count in world.start_inventory[player].value.items():
            for _ in range(count):
                world.push_precollected(world.create_item(item_name, player))

    for player in world.player_ids:
        if player in world.get_game_players("A Link to the Past"):
            # enforce pre-defined local items.
            if world.goal[player] in ["localtriforcehunt", "localganontriforcehunt"]:
                world.local_items[player].value.add('Triforce Piece')

            # Not possible to place pendants/crystals out side of boss prizes yet.
            world.non_local_items[player].value -= item_name_groups['Pendants']
            world.non_local_items[player].value -= item_name_groups['Crystals']

        # items can't be both local and non-local, prefer local
        world.non_local_items[player].value -= world.local_items[player].value

    logger.info('Creating World.')
    AutoWorld.call_all(world, "create_regions")

    logger.info('Creating Items.')
    AutoWorld.call_all(world, "create_items")

    logger.info('Calculating Access Rules.')
    if world.players > 1:
        for player in world.player_ids:
            locality_rules(world, player)
    else:
        world.non_local_items[1].value = set()
        world.local_items[1].value = set()

    AutoWorld.call_all(world, "set_rules")

    for player in world.player_ids:
        exclusion_rules(world, player, world.exclude_locations[player].value)

    AutoWorld.call_all(world, "generate_basic")

    logger.info("Running Item Plando")

    for item in world.itempool:
        item.world = world

    distribute_planned(world)

    logger.info('Running Pre Main Fill.')

    AutoWorld.call_all(world, "pre_fill")

    logger.info(f'Filling the world with {len(world.itempool)} items.')

    if world.algorithm == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    elif world.algorithm == 'balanced':
        distribute_items_restrictive(world)

    AutoWorld.call_all(world, 'post_fill')

    if world.players > 1:
        balance_multiworld_progression(world)

    logger.info(f'Beginning output...')
    outfilebase = 'AP_' + world.seed_name

    output = tempfile.TemporaryDirectory()
    with output as temp_dir:
        with concurrent.futures.ThreadPoolExecutor(world.players + 2) as pool:
            check_accessibility_task = pool.submit(world.fulfills_accessibility)

            output_file_futures = [pool.submit(AutoWorld.call_stage, world, "generate_output", temp_dir)]
            for player in world.player_ids:
                # skip starting a thread for methods that say "pass".
                if AutoWorld.World.generate_output.__code__ is not world.worlds[player].generate_output.__code__:
                    output_file_futures.append(
                        pool.submit(AutoWorld.call_single, world, "generate_output", player, temp_dir))

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

            checks_in_area = {player: {area: list() for area in ordered_areas}
                              for player in range(1, world.players + 1)}

            for player in range(1, world.players + 1):
                checks_in_area[player]["Total"] = 0

            for location in world.get_filled_locations():
                if type(location.address) is int:
                    main_entrance = get_entrance_to_region(location.parent_region)
                    if location.game != "A Link to the Past":
                        checks_in_area[location.player]["Light World"].append(location.address)
                    elif location.parent_region.dungeon:
                        dungeonname = {'Inverted Agahnims Tower': 'Agahnims Tower',
                                       'Inverted Ganons Tower': 'Ganons Tower'} \
                            .get(location.parent_region.dungeon.name, location.parent_region.dungeon.name)
                        checks_in_area[location.player][dungeonname].append(location.address)
                    elif location.parent_region.type == RegionType.LightWorld:
                        checks_in_area[location.player]["Light World"].append(location.address)
                    elif location.parent_region.type == RegionType.DarkWorld:
                        checks_in_area[location.player]["Dark World"].append(location.address)
                    elif main_entrance.parent_region.type == RegionType.LightWorld:
                        checks_in_area[location.player]["Light World"].append(location.address)
                    elif main_entrance.parent_region.type == RegionType.DarkWorld:
                        checks_in_area[location.player]["Dark World"].append(location.address)
                    checks_in_area[location.player]["Total"] += 1

            oldmancaves = []
            takeanyregions = ["Old Man Sword Cave", "Take-Any #1", "Take-Any #2", "Take-Any #3", "Take-Any #4"]
            for index, take_any in enumerate(takeanyregions):
                for region in [world.get_region(take_any, player) for player in
                               world.get_game_players("A Link to the Past") if world.retro[player]]:
                    item = world.create_item(
                        region.shop.inventory[(0 if take_any == "Old Man Sword Cave" else 1)]['item'],
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
                games = {}
                minimum_versions = {"server": (0, 2, 4), "clients": client_versions}
                slot_info = {}
                names = [[name for player, name in sorted(world.player_name.items())]]
                for slot in world.player_ids:
                    client_versions[slot] = world.worlds[slot].get_required_client_version()
                    games[slot] = world.game[slot]
                    slot_info[slot] = NetUtils.NetworkSlot(names[0][slot-1], world.game[slot], world.player_types[slot])
                precollected_items = {player: [item.code for item in world_precollected]
                                      for player, world_precollected in world.precollected_items.items()}
                precollected_hints = {player: set() for player in range(1, world.players + 1)}

                sending_visible_players = set()

                for slot in world.player_ids:
                    slot_data[slot] = world.worlds[slot].fill_slot_data()
                    if world.worlds[slot].sending_visible:
                        sending_visible_players.add(slot)

                def precollect_hint(location):
                    hint = NetUtils.Hint(location.item.player, location.player, location.address,
                                         location.item.code, False, "", location.item.flags)
                    precollected_hints[location.player].add(hint)
                    precollected_hints[location.item.player].add(hint)

                locations_data: Dict[int, Dict[int, Tuple[int, int, int]]] = {player: {} for player in world.player_ids}
                for location in world.get_filled_locations():
                    if type(location.address) == int:
                        # item code None should be event, location.address should then also be None
                        assert location.item.code is not None
                        locations_data[location.player][location.address] = \
                            location.item.code, location.item.player, location.item.flags
                        if location.player in sending_visible_players:
                            precollect_hint(location)
                        elif location.name in world.start_location_hints[location.player]:
                            precollect_hint(location)
                        elif location.item.name in world.start_hints[location.item.player]:
                            precollect_hint(location)

                multidata = {
                    "slot_data": slot_data,
                    "slot_info": slot_info,
                    "names": names,  # TODO: remove around 0.2.5 in favor of slot_info
                    "games": games,  # TODO: remove around 0.2.5 in favor of slot_info
                    "connect_names": {name: (0, player) for player, name in world.player_name.items()},
                    "remote_items": {player for player in world.player_ids if
                                     world.worlds[player].remote_items},
                    "remote_start_inventory": {player for player in world.player_ids if
                                               world.worlds[player].remote_start_inventory},
                    "locations": locations_data,
                    "checks_in_area": checks_in_area,
                    "server_options": baked_server_options,
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
                    f.write(bytes([2]))  # version of format
                    f.write(multidata)

            multidata_task = pool.submit(write_multidata)
            if not check_accessibility_task.result():
                if not world.can_beat_game():
                    raise Exception("Game appears as unbeatable. Aborting.")
                else:
                    logger.warning("Location Accessibility requirements not fulfilled.")

            # retrieve exceptions via .result() if they occured.
            multidata_task.result()
            for i, future in enumerate(concurrent.futures.as_completed(output_file_futures), start=1):
                if i % 10 == 0 or i == len(output_file_futures):
                    logger.info(f'Generating output files ({i}/{len(output_file_futures)}).')
                future.result()

        if args.spoiler > 1:
            logger.info('Calculating playthrough.')
            create_playthrough(world)

        if args.spoiler:
            world.spoiler.to_file(os.path.join(temp_dir, '%s_Spoiler.txt' % outfilebase))

        zipfilename = output_path(f"AP_{world.seed_name}.zip")
        logger.info(f'Creating final archive at {zipfilename}.')
        with zipfile.ZipFile(zipfilename, mode="w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zf:
            for file in os.scandir(temp_dir):
                zf.write(file.path, arcname=file.name)

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
            if any([world.accessibility[location.item.player] != 'minimal' for location in sphere_candidates]):
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
    for item in (i for i in chain.from_iterable(world.precollected_items.values()) if i.advancement):
        logging.debug('Checking if %s (Player %d) is required to beat the game.', item.name, item.player)
        world.precollected_items[item.player].remove(item)
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
            # If Pyramid Fairy Entrance needs to be reached, also path to Big Bomb Shop
            # Maybe move the big bomb over to the Event system instead?
            if any(exit_path == 'Pyramid Fairy' for path in world.spoiler.paths.values() for (_, exit_path) in path):
                if world.mode[player] != 'inverted':
                    world.spoiler.paths[str(world.get_region('Big Bomb Shop', player))] = \
                        get_path(state, world.get_region('Big Bomb Shop', player))
                else:
                    world.spoiler.paths[str(world.get_region('Inverted Big Bomb Shop', player))] = \
                        get_path(state, world.get_region('Inverted Big Bomb Shop', player))

    # we can finally output our playthrough
    world.spoiler.playthrough = {"0": sorted([str(item) for item in
                                              chain.from_iterable(world.precollected_items.values())
                                              if item.advancement])}

    for i, sphere in enumerate(collection_spheres):
        world.spoiler.playthrough[str(i + 1)] = {str(location): str(location.item) for location in sorted(sphere)}

    # repair the world again
    for location, item in restore_later.items():
        location.item = item

    for item in removed_precollected:
        world.push_precollected(item)
