import collections
import concurrent.futures
import logging
import os
import pickle
import tempfile
import time
import zipfile
import zlib
from typing import Dict, List, Optional, Set, Tuple, Union

import worlds
from BaseClasses import CollectionState, Item, Location, LocationProgressType, MultiWorld, Region
from Fill import balance_multiworld_progression, distribute_items_restrictive, distribute_planned, flood_items
from Options import StartInventoryPool
from Utils import __version__, output_path, version_tuple
from settings import get_settings
from worlds import AutoWorld
from worlds.generic.Rules import exclusion_rules, locality_rules

__all__ = ["main"]


def main(args, seed=None, baked_server_options: Optional[Dict[str, object]] = None):
    if not baked_server_options:
        baked_server_options = get_settings().server_options.as_dict()
    assert isinstance(baked_server_options, dict)
    if args.outputpath:
        os.makedirs(args.outputpath, exist_ok=True)
        output_path.cached_path = args.outputpath

    start = time.perf_counter()
    # initialize the world
    world = MultiWorld(args.multi)

    logger = logging.getLogger()
    world.set_seed(seed, args.race, str(args.outputname) if args.outputname else None)
    world.plando_options = args.plando_options

    world.shuffle = args.shuffle.copy()
    world.logic = args.logic.copy()
    world.mode = args.mode.copy()
    world.difficulty = args.difficulty.copy()
    world.item_functionality = args.item_functionality.copy()
    world.timer = args.timer.copy()
    world.goal = args.goal.copy()
    world.boss_shuffle = args.shufflebosses.copy()
    world.enemy_health = args.enemy_health.copy()
    world.enemy_damage = args.enemy_damage.copy()
    world.beemizer_total_chance = args.beemizer_total_chance.copy()
    world.beemizer_trap_chance = args.beemizer_trap_chance.copy()
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
    world.player_name = args.name.copy()
    world.sprite = args.sprite.copy()
    world.glitch_triforce = args.glitch_triforce  # This is enabled/disabled globally, no per player option.

    world.set_options(args)
    world.set_item_links()
    world.state = CollectionState(world)
    logger.info('Archipelago Version %s  -  Seed: %s\n', __version__, world.seed)

    logger.info(f"Found {len(AutoWorld.AutoWorldRegister.world_types)} World Types:")
    longest_name = max(len(text) for text in AutoWorld.AutoWorldRegister.world_types)

    max_item = 0
    max_location = 0
    for cls in AutoWorld.AutoWorldRegister.world_types.values():
        if cls.item_id_to_name:
            max_item = max(max_item, max(cls.item_id_to_name))
            max_location = max(max_location, max(cls.location_id_to_name))

    item_digits = len(str(max_item))
    location_digits = len(str(max_location))
    item_count = len(str(max(len(cls.item_names) for cls in AutoWorld.AutoWorldRegister.world_types.values())))
    location_count = len(str(max(len(cls.location_names) for cls in AutoWorld.AutoWorldRegister.world_types.values())))
    del max_item, max_location

    for name, cls in AutoWorld.AutoWorldRegister.world_types.items():
        if not cls.hidden and len(cls.item_names) > 0:
            logger.info(f" {name:{longest_name}}: {len(cls.item_names):{item_count}} "
                        f"Items (IDs: {min(cls.item_id_to_name):{item_digits}} - "
                        f"{max(cls.item_id_to_name):{item_digits}}) | "
                        f"{len(cls.location_names):{location_count}} "
                        f"Locations (IDs: {min(cls.location_id_to_name):{location_digits}} - "
                        f"{max(cls.location_id_to_name):{location_digits}})")

    del item_digits, location_digits, item_count, location_count

    # This assertion method should not be necessary to run if we are not outputting any multidata.
    if not args.skip_output:
        AutoWorld.call_stage(world, "assert_generate")

    AutoWorld.call_all(world, "generate_early")

    logger.info('')

    for player in world.player_ids:
        for item_name, count in world.worlds[player].options.start_inventory.value.items():
            for _ in range(count):
                world.push_precollected(world.create_item(item_name, player))

        for item_name, count in world.start_inventory_from_pool.setdefault(player, StartInventoryPool({})).value.items():
            for _ in range(count):
                world.push_precollected(world.create_item(item_name, player))

    logger.info('Creating World.')
    AutoWorld.call_all(world, "create_regions")

    logger.info('Creating Items.')
    AutoWorld.call_all(world, "create_items")

    logger.info('Calculating Access Rules.')

    for player in world.player_ids:
        # items can't be both local and non-local, prefer local
        world.worlds[player].options.non_local_items.value -= world.worlds[player].options.local_items.value
        world.worlds[player].options.non_local_items.value -= set(world.local_early_items[player])

    AutoWorld.call_all(world, "set_rules")

    for player in world.player_ids:
        exclusion_rules(world, player, world.worlds[player].options.exclude_locations.value)
        world.worlds[player].options.priority_locations.value -= world.worlds[player].options.exclude_locations.value
        for location_name in world.worlds[player].options.priority_locations.value:
            try:
                location = world.get_location(location_name, player)
            except KeyError as e:  # failed to find the given location. Check if it's a legitimate location
                if location_name not in world.worlds[player].location_name_to_id:
                    raise Exception(f"Unable to prioritize location {location_name} in player {player}'s world.") from e
            else:
                location.progress_type = LocationProgressType.PRIORITY

    # Set local and non-local item rules.
    if world.players > 1:
        locality_rules(world)
    else:
        world.worlds[1].options.non_local_items.value = set()
        world.worlds[1].options.local_items.value = set()
    
    AutoWorld.call_all(world, "generate_basic")

    # remove starting inventory from pool items.
    # Because some worlds don't actually create items during create_items this has to be as late as possible.
    if any(world.start_inventory_from_pool[player].value for player in world.player_ids):
        new_items: List[Item] = []
        depletion_pool: Dict[int, Dict[str, int]] = {
            player: world.start_inventory_from_pool[player].value.copy() for player in world.player_ids}
        for player, items in depletion_pool.items():
            player_world: AutoWorld.World = world.worlds[player]
            for count in items.values():
                for _ in range(count):
                    new_items.append(player_world.create_filler())
        target: int = sum(sum(items.values()) for items in depletion_pool.values())
        for i, item in enumerate(world.itempool):
            if depletion_pool[item.player].get(item.name, 0):
                target -= 1
                depletion_pool[item.player][item.name] -= 1
                # quick abort if we have found all items
                if not target:
                    new_items.extend(world.itempool[i+1:])
                    break
            else:
                new_items.append(item)

        # leftovers?
        if target:
            for player, remaining_items in depletion_pool.items():
                remaining_items = {name: count for name, count in remaining_items.items() if count}
                if remaining_items:
                    raise Exception(f"{world.get_player_name(player)}"
                                    f" is trying to remove items from their pool that don't exist: {remaining_items}")
        assert len(world.itempool) == len(new_items), "Item Pool amounts should not change."
        world.itempool[:] = new_items

    # temporary home for item links, should be moved out of Main
    for group_id, group in world.groups.items():
        def find_common_pool(players: Set[int], shared_pool: Set[str]) -> Tuple[
            Optional[Dict[int, Dict[str, int]]], Optional[Dict[str, int]]
        ]:
            classifications: Dict[str, int] = collections.defaultdict(int)
            counters = {player: {name: 0 for name in shared_pool} for player in players}
            for item in world.itempool:
                if item.player in counters and item.name in shared_pool:
                    counters[item.player][item.name] += 1
                    classifications[item.name] |= item.classification

            for player in players.copy():
                if all([counters[player][item] == 0 for item in shared_pool]):
                    players.remove(player)
                    del (counters[player])

            if not players:
                return None, None

            for item in shared_pool:
                count = min(counters[player][item] for player in players)
                if count:
                    for player in players:
                        counters[player][item] = count
                else:
                    for player in players:
                        del (counters[player][item])
            return counters, classifications

        common_item_count, classifications = find_common_pool(group["players"], group["item_pool"])
        if not common_item_count:
            continue

        new_itempool: List[Item] = []
        for item_name, item_count in next(iter(common_item_count.values())).items():
            for _ in range(item_count):
                new_item = group["world"].create_item(item_name)
                # mangle together all original classification bits
                new_item.classification |= classifications[item_name]
                new_itempool.append(new_item)

        region = Region("Menu", group_id, world, "ItemLink")
        world.regions.append(region)
        locations = region.locations
        for item in world.itempool:
            count = common_item_count.get(item.player, {}).get(item.name, 0)
            if count:
                loc = Location(group_id, f"Item Link: {item.name} -> {world.player_name[item.player]} {count}",
                               None, region)
                loc.access_rule = lambda state, item_name = item.name, group_id_ = group_id, count_ = count: \
                    state.has(item_name, group_id_, count_)

                locations.append(loc)
                loc.place_locked_item(item)
                common_item_count[item.player][item.name] -= 1
            else:
                new_itempool.append(item)

        itemcount = len(world.itempool)
        world.itempool = new_itempool

        while itemcount > len(world.itempool):
            items_to_add = []
            for player in group["players"]:
                if group["link_replacement"]:
                    item_player = group_id
                else:
                    item_player = player
                if group["replacement_items"][player]:
                    items_to_add.append(AutoWorld.call_single(world, "create_item", item_player,
                                                                group["replacement_items"][player]))
                else:
                    items_to_add.append(AutoWorld.call_single(world, "create_filler", item_player))
            world.random.shuffle(items_to_add)
            world.itempool.extend(items_to_add[:itemcount - len(world.itempool)])

    if any(world.item_links.values()):
        world._all_state = None

    logger.info("Running Item Plando.")

    distribute_planned(world)

    logger.info('Running Pre Main Fill.')

    AutoWorld.call_all(world, "pre_fill")

    logger.info(f'Filling the world with {len(world.itempool)} items.')

    if world.algorithm == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    elif world.algorithm == 'balanced':
        distribute_items_restrictive(world)

    AutoWorld.call_all(world, 'post_fill')

    if world.players > 1 and not args.skip_prog_balancing:
        balance_multiworld_progression(world)
    else:
        logger.info("Progression balancing skipped.")

    # we're about to output using multithreading, so we're removing the global random state to prevent accidental use
    world.random.passthrough = False

    if args.skip_output:
        logger.info('Done. Skipped output/spoiler generation. Total Time: %s', time.perf_counter() - start)
        return world

    logger.info(f'Beginning output...')
    outfilebase = 'AP_' + world.seed_name

    output = tempfile.TemporaryDirectory()
    with output as temp_dir:
        output_players = [player for player in world.player_ids if AutoWorld.World.generate_output.__code__
                          is not world.worlds[player].generate_output.__code__]
        with concurrent.futures.ThreadPoolExecutor(len(output_players) + 2) as pool:
            check_accessibility_task = pool.submit(world.fulfills_accessibility)

            output_file_futures = [pool.submit(AutoWorld.call_stage, world, "generate_output", temp_dir)]
            for player in output_players:
                # skip starting a thread for methods that say "pass".
                output_file_futures.append(
                    pool.submit(AutoWorld.call_single, world, "generate_output", player, temp_dir))

            # collect ER hint info
            er_hint_data: Dict[int, Dict[int, str]] = {}
            AutoWorld.call_all(world, 'extend_hint_information', er_hint_data)

            def write_multidata():
                import NetUtils
                slot_data = {}
                client_versions = {}
                games = {}
                minimum_versions = {"server": AutoWorld.World.required_server_version, "clients": client_versions}
                slot_info = {}
                names = [[name for player, name in sorted(world.player_name.items())]]
                for slot in world.player_ids:
                    player_world: AutoWorld.World = world.worlds[slot]
                    minimum_versions["server"] = max(minimum_versions["server"], player_world.required_server_version)
                    client_versions[slot] = player_world.required_client_version
                    games[slot] = world.game[slot]
                    slot_info[slot] = NetUtils.NetworkSlot(names[0][slot - 1], world.game[slot],
                                                           world.player_types[slot])
                for slot, group in world.groups.items():
                    games[slot] = world.game[slot]
                    slot_info[slot] = NetUtils.NetworkSlot(group["name"], world.game[slot], world.player_types[slot],
                                                           group_members=sorted(group["players"]))
                precollected_items = {player: [item.code for item in world_precollected if type(item.code) == int]
                                      for player, world_precollected in world.precollected_items.items()}
                precollected_hints = {player: set() for player in range(1, world.players + 1 + len(world.groups))}

                for slot in world.player_ids:
                    slot_data[slot] = world.worlds[slot].fill_slot_data()

                def precollect_hint(location):
                    entrance = er_hint_data.get(location.player, {}).get(location.address, "")
                    hint = NetUtils.Hint(location.item.player, location.player, location.address,
                                         location.item.code, False, entrance, location.item.flags)
                    precollected_hints[location.player].add(hint)
                    if location.item.player not in world.groups:
                        precollected_hints[location.item.player].add(hint)
                    else:
                        for player in world.groups[location.item.player]["players"]:
                            precollected_hints[player].add(hint)

                locations_data: Dict[int, Dict[int, Tuple[int, int, int]]] = {player: {} for player in world.player_ids}
                for location in world.get_filled_locations():
                    if type(location.address) == int:
                        assert location.item.code is not None, "item code None should be event, " \
                                                               "location.address should then also be None. Location: " \
                                                               f" {location}"
                        assert location.address not in locations_data[location.player], (
                            f"Locations with duplicate address. {location} and "
                            f"{locations_data[location.player][location.address]}")
                        locations_data[location.player][location.address] = \
                            location.item.code, location.item.player, location.item.flags
                        if location.name in world.worlds[location.player].options.start_location_hints:
                            precollect_hint(location)
                        elif location.item.name in world.worlds[location.item.player].options.start_hints:
                            precollect_hint(location)
                        elif any([location.item.name in world.worlds[player].options.start_hints
                                  for player in world.groups.get(location.item.player, {}).get("players", [])]):
                            precollect_hint(location)

                # embedded data package
                data_package = {
                    game_world.game: worlds.network_data_package["games"][game_world.game]
                    for game_world in world.worlds.values()
                }

                checks_in_area: Dict[int, Dict[str, Union[int, List[int]]]] = {}

                multidata = {
                    "slot_data": slot_data,
                    "slot_info": slot_info,
                    "connect_names": {name: (0, player) for player, name in world.player_name.items()},
                    "locations": locations_data,
                    "checks_in_area": checks_in_area,
                    "server_options": baked_server_options,
                    "er_hint_data": er_hint_data,
                    "precollected_items": precollected_items,
                    "precollected_hints": precollected_hints,
                    "version": tuple(version_tuple),
                    "tags": ["AP"],
                    "minimum_versions": minimum_versions,
                    "seed_name": world.seed_name,
                    "datapackage": data_package,
                }
                AutoWorld.call_all(world, "modify_multidata", multidata)

                multidata = zlib.compress(pickle.dumps(multidata), 9)

                with open(os.path.join(temp_dir, f'{outfilebase}.archipelago'), 'wb') as f:
                    f.write(bytes([3]))  # version of format
                    f.write(multidata)

            output_file_futures.append(pool.submit(write_multidata))
            if not check_accessibility_task.result():
                if not world.can_beat_game():
                    raise Exception("Game appears as unbeatable. Aborting.")
                else:
                    logger.warning("Location Accessibility requirements not fulfilled.")

            # retrieve exceptions via .result() if they occurred.
            for i, future in enumerate(concurrent.futures.as_completed(output_file_futures), start=1):
                if i % 10 == 0 or i == len(output_file_futures):
                    logger.info(f'Generating output files ({i}/{len(output_file_futures)}).')
                future.result()

        if args.spoiler > 1:
            logger.info('Calculating playthrough.')
            world.spoiler.create_playthrough(create_paths=args.spoiler > 2)

        if args.spoiler:
            world.spoiler.to_file(os.path.join(temp_dir, '%s_Spoiler.txt' % outfilebase))

        zipfilename = output_path(f"AP_{world.seed_name}.zip")
        logger.info(f"Creating final archive at {zipfilename}")
        with zipfile.ZipFile(zipfilename, mode="w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zf:
            for file in os.scandir(temp_dir):
                zf.write(file.path, arcname=file.name)

    logger.info('Done. Enjoy. Total Time: %s', time.perf_counter() - start)
    return world
