import collections
from collections.abc import Mapping
import concurrent.futures
import logging
import os
import tempfile
import time
from typing import Any
import zipfile
import zlib

import worlds
from BaseClasses import CollectionState, Item, Location, LocationProgressType, MultiWorld
from Fill import FillError, balance_multiworld_progression, distribute_items_restrictive, flood_items, \
    parse_planned_blocks, distribute_planned_blocks, resolve_early_locations_for_planned
from NetUtils import convert_to_base_types
from Options import StartInventoryPool
from Utils import __version__, output_path, restricted_dumps, version_tuple
from settings import get_settings
from worlds import AutoWorld
from worlds.generic.Rules import exclusion_rules, locality_rules

__all__ = ["main"]


def main(args, seed=None, baked_server_options: dict[str, object] | None = None):
    if not baked_server_options:
        baked_server_options = get_settings().server_options.as_dict()
    assert isinstance(baked_server_options, dict)
    if args.outputpath:
        os.makedirs(args.outputpath, exist_ok=True)
        output_path.cached_path = args.outputpath

    start = time.perf_counter()
    # initialize the multiworld
    multiworld = MultiWorld(args.multi)

    logger = logging.getLogger()
    multiworld.set_seed(seed, args.race, str(args.outputname) if args.outputname else None)
    multiworld.plando_options = args.plando
    multiworld.game = args.game.copy()
    multiworld.player_name = args.name.copy()
    multiworld.sprite = args.sprite.copy()
    multiworld.sprite_pool = args.sprite_pool.copy()

    multiworld.set_options(args)
    if args.csv_output:
        from Options import dump_player_options
        dump_player_options(multiworld)
    multiworld.set_item_links()
    multiworld.state = CollectionState(multiworld)
    logger.info('Archipelago Version %s  -  Seed: %s\n', __version__, multiworld.seed)

    logger.info(f"Found {len(AutoWorld.AutoWorldRegister.world_types)} World Types:")
    longest_name = max(len(text) for text in AutoWorld.AutoWorldRegister.world_types)

    world_classes = AutoWorld.AutoWorldRegister.world_types.values()

    version_count = max(len(cls.world_version.as_simple_string()) for cls in world_classes)
    item_count = len(str(max(len(cls.item_names) for cls in world_classes)))
    location_count = len(str(max(len(cls.location_names) for cls in world_classes)))

    for name, cls in AutoWorld.AutoWorldRegister.world_types.items():
        if not cls.hidden and len(cls.item_names) > 0:
            logger.info(f" {name:{longest_name}}: "
                        f"v{cls.world_version.as_simple_string():{version_count}} | "
                        f"Items: {len(cls.item_names):{item_count}} | "
                        f"Locations: {len(cls.location_names):{location_count}}")

    del item_count, location_count

    # This assertion method should not be necessary to run if we are not outputting any multidata.
    if not args.skip_output and not args.spoiler_only:
        AutoWorld.call_stage(multiworld, "assert_generate")

    AutoWorld.call_all(multiworld, "generate_early")

    logger.info('')

    for player in multiworld.player_ids:
        for item_name, count in multiworld.worlds[player].options.start_inventory.value.items():
            for _ in range(count):
                multiworld.push_precollected(multiworld.create_item(item_name, player))

        for item_name, count in getattr(multiworld.worlds[player].options,
                                        "start_inventory_from_pool",
                                        StartInventoryPool({})).value.items():
            for _ in range(count):
                multiworld.push_precollected(multiworld.create_item(item_name, player))
            # remove from_pool items also from early items handling, as starting is plenty early.
            early = multiworld.early_items[player].get(item_name, 0)
            if early:
                multiworld.early_items[player][item_name] = max(0, early-count)
                remaining_count = count-early
                if remaining_count > 0:
                    local_early = multiworld.local_early_items[player].get(item_name, 0)
                    if local_early:
                        multiworld.early_items[player][item_name] = max(0, local_early - remaining_count)
                    del local_early
            del early

        # items can't be both local and non-local, prefer local
        multiworld.worlds[player].options.non_local_items.value -= multiworld.worlds[player].options.local_items.value
        multiworld.worlds[player].options.non_local_items.value -= set(multiworld.local_early_items[player])

    # Clear non-applicable local and non-local items.
    if multiworld.players == 1:
        multiworld.worlds[1].options.non_local_items.value = set()
        multiworld.worlds[1].options.local_items.value = set()

    logger.info('Creating MultiWorld.')
    AutoWorld.call_all(multiworld, "create_regions")

    logger.info('Creating Items.')
    AutoWorld.call_all(multiworld, "create_items")

    logger.info('Calculating Access Rules.')
    AutoWorld.call_all(multiworld, "set_rules")

    for player in multiworld.player_ids:
        exclusion_rules(multiworld, player, multiworld.worlds[player].options.exclude_locations.value)
        multiworld.worlds[player].options.priority_locations.value -= multiworld.worlds[player].options.exclude_locations.value
        world_excluded_locations = set()
        for location_name in multiworld.worlds[player].options.priority_locations.value:
            try:
                location = multiworld.get_location(location_name, player)
            except KeyError:
                continue

            if location.progress_type != LocationProgressType.EXCLUDED:
                location.progress_type = LocationProgressType.PRIORITY
            else:
                logger.warning(f"Unable to prioritize location \"{location_name}\" in player {player}'s world because the world excluded it.")
                world_excluded_locations.add(location_name)
        multiworld.worlds[player].options.priority_locations.value -= world_excluded_locations

    # Set local and non-local item rules.
    # This function is called so late because worlds might otherwise overwrite item_rules which are how locality works
    if multiworld.players > 1:
        locality_rules(multiworld)

    multiworld.plando_item_blocks = parse_planned_blocks(multiworld)

    AutoWorld.call_all(multiworld, "connect_entrances")
    AutoWorld.call_all(multiworld, "generate_basic")

    # remove starting inventory from pool items.
    # Because some worlds don't actually create items during create_items this has to be as late as possible.
    fallback_inventory = StartInventoryPool({})
    depletion_pool: dict[int, dict[str, int]] = {
        player: getattr(multiworld.worlds[player].options, "start_inventory_from_pool", fallback_inventory).value.copy()
        for player in multiworld.player_ids
    }
    target_per_player = {
        player: sum(target_items.values()) for player, target_items in depletion_pool.items() if target_items
    }

    if target_per_player:
        new_itempool: list[Item] = []

        # Make new itempool with start_inventory_from_pool items removed
        for item in multiworld.itempool:
            if depletion_pool[item.player].get(item.name, 0):
                depletion_pool[item.player][item.name] -= 1
            else:
                new_itempool.append(item)

        # Create filler in place of the removed items, warn if any items couldn't be found in the multiworld itempool
        for player, target in target_per_player.items():
            unfound_items = {item: count for item, count in depletion_pool[player].items() if count}

            if unfound_items:
                player_name = multiworld.get_player_name(player)
                logger.warning(f"{player_name} tried to remove items from their pool that don't exist: {unfound_items}")

            needed_items = target_per_player[player] - sum(unfound_items.values())
            new_itempool += [multiworld.worlds[player].create_filler() for _ in range(needed_items)]

        assert len(multiworld.itempool) == len(new_itempool), "Item Pool amounts should not change."
        multiworld.itempool[:] = new_itempool

    multiworld.link_items()

    if any(world.options.item_links for world in multiworld.worlds.values()):
        multiworld._all_state = None

    logger.info("Running Item Plando.")
    resolve_early_locations_for_planned(multiworld)
    distribute_planned_blocks(multiworld, [x for player in multiworld.plando_item_blocks
                                           for x in multiworld.plando_item_blocks[player]])

    logger.info('Running Pre Main Fill.')

    AutoWorld.call_all(multiworld, "pre_fill")

    logger.info(f'Filling the multiworld with {len(multiworld.itempool)} items.')

    if multiworld.algorithm == 'flood':
        flood_items(multiworld)  # different algo, biased towards early game progress items
    elif multiworld.algorithm == 'balanced':
        distribute_items_restrictive(multiworld, get_settings().generator.panic_method)

    AutoWorld.call_all(multiworld, 'post_fill')

    if multiworld.players > 1 and not args.skip_prog_balancing:
        balance_multiworld_progression(multiworld)
    else:
        logger.info("Progression balancing skipped.")

    # we're about to output using multithreading, so we're removing the global random state to prevent accidental use
    multiworld.random.passthrough = False

    if args.skip_output:
        logger.info('Done. Skipped output/spoiler generation. Total Time: %s', time.perf_counter() - start)
        return multiworld

    logger.info(f'Beginning output...')
    outfilebase = 'AP_' + multiworld.seed_name

    if args.spoiler_only:
        if args.spoiler > 1:
            logger.info('Calculating playthrough.')
            multiworld.spoiler.create_playthrough(create_paths=args.spoiler > 2)

        multiworld.spoiler.to_file(output_path('%s_Spoiler.txt' % outfilebase))
        logger.info('Done. Skipped multidata modification. Total time: %s', time.perf_counter() - start)
        return multiworld

    output = tempfile.TemporaryDirectory()
    with output as temp_dir:
        output_players = [player for player in multiworld.player_ids if AutoWorld.World.generate_output.__code__
                          is not multiworld.worlds[player].generate_output.__code__]
        with concurrent.futures.ThreadPoolExecutor(len(output_players) + 2) as pool:
            check_accessibility_task = pool.submit(multiworld.fulfills_accessibility)

            output_file_futures = [pool.submit(AutoWorld.call_stage, multiworld, "generate_output", temp_dir)]
            for player in output_players:
                # skip starting a thread for methods that say "pass".
                output_file_futures.append(
                    pool.submit(AutoWorld.call_single, multiworld, "generate_output", player, temp_dir))

            # collect ER hint info
            er_hint_data: dict[int, dict[int, str]] = {}
            AutoWorld.call_all(multiworld, 'extend_hint_information', er_hint_data)

            def write_multidata():
                import NetUtils
                from NetUtils import HintStatus
                slot_data: dict[int, Mapping[str, Any]] = {}
                client_versions: dict[int, tuple[int, int, int]] = {}
                games: dict[int, str] = {}
                minimum_versions: NetUtils.MinimumVersions = {
                    "server": AutoWorld.World.required_server_version, "clients": client_versions
                }
                slot_info: dict[int, NetUtils.NetworkSlot] = {}
                names = [[name for player, name in sorted(multiworld.player_name.items())]]
                for slot in multiworld.player_ids:
                    player_world: AutoWorld.World = multiworld.worlds[slot]
                    minimum_versions["server"] = max(minimum_versions["server"], player_world.required_server_version)
                    client_versions[slot] = player_world.required_client_version
                    games[slot] = multiworld.game[slot]
                    slot_info[slot] = NetUtils.NetworkSlot(names[0][slot - 1], multiworld.game[slot],
                                                           multiworld.player_types[slot])
                for slot, group in multiworld.groups.items():
                    games[slot] = multiworld.game[slot]
                    slot_info[slot] = NetUtils.NetworkSlot(group["name"], multiworld.game[slot], multiworld.player_types[slot],
                                                           group_members=sorted(group["players"]))
                precollected_items = {player: [item.code for item in world_precollected if type(item.code) == int]
                                      for player, world_precollected in multiworld.precollected_items.items()}
                precollected_hints: dict[int, set[NetUtils.Hint]] = {
                    player: set() for player in range(1, multiworld.players + 1 + len(multiworld.groups))
                }

                for slot in multiworld.player_ids:
                    slot_data[slot] = multiworld.worlds[slot].fill_slot_data()

                def precollect_hint(location: Location, auto_status: HintStatus):
                    entrance = er_hint_data.get(location.player, {}).get(location.address, "")
                    hint = NetUtils.Hint(location.item.player, location.player, location.address,
                                         location.item.code, False, entrance, location.item.flags, auto_status)
                    precollected_hints[location.player].add(hint)
                    if location.item.player not in multiworld.groups:
                        precollected_hints[location.item.player].add(hint)
                    else:
                        for player in multiworld.groups[location.item.player]["players"]:
                            precollected_hints[player].add(hint)

                locations_data: dict[int, dict[int, tuple[int, int, int]]] = {player: {} for player in multiworld.player_ids}
                for location in multiworld.get_filled_locations():
                    if type(location.address) == int:
                        assert location.item.code is not None, "item code None should be event, " \
                                                               "location.address should then also be None. Location: " \
                                                               f" {location}, Item: {location.item}"
                        assert location.address not in locations_data[location.player], (
                            f"Locations with duplicate address. {location} and "
                            f"{locations_data[location.player][location.address]}")
                        locations_data[location.player][location.address] = \
                            location.item.code, location.item.player, location.item.flags
                        auto_status = HintStatus.HINT_AVOID if location.item.trap else HintStatus.HINT_PRIORITY
                        if location.name in multiworld.worlds[location.player].options.start_location_hints:
                            if not location.item.trap:  # Unspecified status for location hints, except traps
                                auto_status = HintStatus.HINT_UNSPECIFIED
                            precollect_hint(location, auto_status)
                        elif location.item.name in multiworld.worlds[location.item.player].options.start_hints:
                            precollect_hint(location, auto_status)
                        elif any([location.item.name in multiworld.worlds[player].options.start_hints
                                  for player in multiworld.groups.get(location.item.player, {}).get("players", [])]):
                            precollect_hint(location, auto_status)

                # embedded data package
                data_package = {
                    game_world.game: worlds.network_data_package["games"][game_world.game]
                    for game_world in multiworld.worlds.values()
                }
                data_package["Archipelago"] = worlds.network_data_package["games"]["Archipelago"]

                checks_in_area: dict[int, dict[str, int | list[int]]] = {}

                # get spheres -> filter address==None -> skip empty
                spheres: list[dict[int, set[int]]] = []
                for sphere in multiworld.get_sendable_spheres():
                    current_sphere: dict[int, set[int]] = collections.defaultdict(set)
                    for sphere_location in sphere:
                        current_sphere[sphere_location.player].add(sphere_location.address)

                    if current_sphere:
                        spheres.append(dict(current_sphere))

                multidata: NetUtils.MultiData | bytes = {
                    "slot_data": slot_data,
                    "slot_info": slot_info,
                    "connect_names": {name: (0, player) for player, name in multiworld.player_name.items()},
                    "locations": locations_data,
                    "checks_in_area": checks_in_area,
                    "server_options": baked_server_options,
                    "er_hint_data": er_hint_data,
                    "precollected_items": precollected_items,
                    "precollected_hints": precollected_hints,
                    "version": (version_tuple.major, version_tuple.minor, version_tuple.build),
                    "tags": ["AP"],
                    "minimum_versions": minimum_versions,
                    "seed_name": multiworld.seed_name,
                    "spheres": spheres,
                    "datapackage": data_package,
                    "race_mode": int(multiworld.is_race),
                }
                # TODO: change to `"version": version_tuple` after getting better serialization
                AutoWorld.call_all(multiworld, "modify_multidata", multidata)

                for key in ("slot_data", "er_hint_data"):
                    multidata[key] = convert_to_base_types(multidata[key])

                multidata = zlib.compress(restricted_dumps(multidata), 9)

                with open(os.path.join(temp_dir, f'{outfilebase}.archipelago'), 'wb') as f:
                    f.write(bytes([3]))  # version of format
                    f.write(multidata)

            output_file_futures.append(pool.submit(write_multidata))
            if not check_accessibility_task.result():
                if not multiworld.can_beat_game():
                    raise FillError("Game appears as unbeatable. Aborting.", multiworld=multiworld)
                else:
                    logger.warning("Location Accessibility requirements not fulfilled.")

            # retrieve exceptions via .result() if they occurred.
            for i, future in enumerate(concurrent.futures.as_completed(output_file_futures), start=1):
                if i % 10 == 0 or i == len(output_file_futures):
                    logger.info(f'Generating output files ({i}/{len(output_file_futures)}).')
                future.result()

        if args.spoiler > 1:
            logger.info('Calculating playthrough.')
            multiworld.spoiler.create_playthrough(create_paths=args.spoiler > 2)

        if args.spoiler:
            multiworld.spoiler.to_file(os.path.join(temp_dir, '%s_Spoiler.txt' % outfilebase))

        zipfilename = output_path(f"AP_{multiworld.seed_name}.zip")
        logger.info(f"Creating final archive at {zipfilename}")
        with zipfile.ZipFile(zipfilename, mode="w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zf:
            for file in os.scandir(temp_dir):
                zf.write(file.path, arcname=file.name)

    logger.info('Done. Enjoy. Total Time: %s', time.perf_counter() - start)
    return multiworld
