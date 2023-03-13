import collections
import logging
import os
import time
import zlib
import concurrent.futures
import pickle
import tempfile
import zipfile
from typing import Dict, List, Tuple, Optional, Set

from BaseClasses import Item, MultiWorld, CollectionState, Region, LocationProgressType, Location
import worlds
from worlds.alttp.SubClasses import LTTPRegionType
from worlds.alttp.Regions import is_main_entrance
from Fill import distribute_items_restrictive, flood_items, balance_multiworld_progression, distribute_planned
from worlds.alttp.Shops import FillDisabledShopSlots
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

    AutoWorld.call_stage(world, "assert_generate")

    AutoWorld.call_all(world, "generate_early")

    logger.info('')

    for player in world.player_ids:
        for item_name, count in world.start_inventory[player].value.items():
            for _ in range(count):
                world.push_precollected(world.create_item(item_name, player))

    logger.info('Creating World.')
    AutoWorld.call_all(world, "create_regions")

    logger.info('Creating Items.')
    AutoWorld.call_all(world, "create_items")

    # All worlds should have finished creating all regions, locations, and entrances.
    # Recache to ensure that they are all visible for locality rules.
    world._recache()

    logger.info('Calculating Access Rules.')

    for player in world.player_ids:
        # items can't be both local and non-local, prefer local
        world.non_local_items[player].value -= world.local_items[player].value
        world.non_local_items[player].value -= set(world.local_early_items[player])

    if world.players > 1:
        locality_rules(world)
    else:
        world.non_local_items[1].value = set()
        world.local_items[1].value = set()

    AutoWorld.call_all(world, "set_rules")

    for player in world.player_ids:
        exclusion_rules(world, player, world.exclude_locations[player].value)
        world.priority_locations[player].value -= world.exclude_locations[player].value
        for location_name in world.priority_locations[player].value:
            world.get_location(location_name, player).progress_type = LocationProgressType.PRIORITY

    AutoWorld.call_all(world, "generate_basic")

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
        locations = region.locations = []
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
        world._recache()
        world._all_state = None

    logger.info("Running Item Plando")

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

    # we're about to output using multithreading, so we're removing the global random state to prevent accidental use
    world.random.passthrough = False

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

            # collect ER hint info
            er_hint_data: Dict[int, Dict[int, str]] = {}
            AutoWorld.call_all(world, 'extend_hint_information', er_hint_data)

            checks_in_area = {player: {area: list() for area in ordered_areas}
                              for player in range(1, world.players + 1)}

            for player in range(1, world.players + 1):
                checks_in_area[player]["Total"] = 0

            for location in world.get_filled_locations():
                if type(location.address) is int:
                    if location.game != "A Link to the Past":
                        checks_in_area[location.player]["Light World"].append(location.address)
                    else:
                        main_entrance = location.parent_region.get_connecting_entrance(is_main_entrance)
                        if location.parent_region.dungeon:
                            dungeonname = {'Inverted Agahnims Tower': 'Agahnims Tower',
                                           'Inverted Ganons Tower': 'Ganons Tower'} \
                                .get(location.parent_region.dungeon.name, location.parent_region.dungeon.name)
                            checks_in_area[location.player][dungeonname].append(location.address)
                        elif location.parent_region.type == LTTPRegionType.LightWorld:
                            checks_in_area[location.player]["Light World"].append(location.address)
                        elif location.parent_region.type == LTTPRegionType.DarkWorld:
                            checks_in_area[location.player]["Dark World"].append(location.address)
                        elif main_entrance.parent_region.type == LTTPRegionType.LightWorld:
                            checks_in_area[location.player]["Light World"].append(location.address)
                        elif main_entrance.parent_region.type == LTTPRegionType.DarkWorld:
                            checks_in_area[location.player]["Dark World"].append(location.address)
                    checks_in_area[location.player]["Total"] += 1

            FillDisabledShopSlots(world)

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
                        locations_data[location.player][location.address] = \
                            location.item.code, location.item.player, location.item.flags
                        if location.name in world.start_location_hints[location.player]:
                            precollect_hint(location)
                        elif location.item.name in world.start_hints[location.item.player]:
                            precollect_hint(location)
                        elif any([location.item.name in world.start_hints[player]
                                  for player in world.groups.get(location.item.player, {}).get("players", [])]):
                            precollect_hint(location)

                # custom datapackage
                datapackage = {}
                for game_world in world.worlds.values():
                    if game_world.data_version == 0 and game_world.game not in datapackage:
                        datapackage[game_world.game] = worlds.network_data_package["games"][game_world.game]
                        datapackage[game_world.game]["item_name_groups"] = game_world.item_name_groups
                        datapackage[game_world.game]["location_name_groups"] = game_world.location_name_groups

                multidata = {
                    "slot_data": slot_data,
                    "slot_info": slot_info,
                    "names": names,  # TODO: remove after 0.3.9
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
                    "datapackage": datapackage,
                }
                AutoWorld.call_all(world, "modify_multidata", multidata)

                multidata = zlib.compress(pickle.dumps(multidata), 9)

                with open(os.path.join(temp_dir, f'{outfilebase}.archipelago'), 'wb') as f:
                    f.write(bytes([3]))  # version of format
                    f.write(multidata)

            multidata_task = pool.submit(write_multidata)
            if not check_accessibility_task.result():
                if not world.can_beat_game():
                    raise Exception("Game appears as unbeatable. Aborting.")
                else:
                    logger.warning("Location Accessibility requirements not fulfilled.")

            # retrieve exceptions via .result() if they occurred.
            multidata_task.result()
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
