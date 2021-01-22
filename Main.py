from collections import OrderedDict
import copy
from itertools import zip_longest
import json
import logging
import os
import random
import time
import zlib
import concurrent.futures

from BaseClasses import World, CollectionState, Item, Region, Location
from Shops import ShopSlotFill, create_shops, SHOP_ID_START
from Items import ItemFactory, item_table, item_name_groups, lookup_id_to_name as lookup_items_id_to_name
from Regions import create_regions, mark_light_world_regions, lookup_vanilla_location_to_entrance, lookup_name_to_id as lookup_region_name_to_id, lookup_id_to_name as lookup_region_id_to_name
from InvertedRegions import create_inverted_regions, mark_dark_world_regions
from EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect
from Rom import patch_rom, patch_race_rom, patch_enemizer, apply_rom_settings, LocalRom, get_hash_string
from Rules import set_rules
from Dungeons import create_dungeons, fill_dungeons, fill_dungeons_restrictive
from Fill import distribute_items_restrictive, flood_items, balance_multiworld_progression, distribute_planned
from ItemPool import generate_itempool, difficulties, fill_prizes
from Utils import output_path, parse_player_names, get_options, __version__, _version_tuple
import Patch

seeddigits = 20


def get_seed(seed=None):
    if seed is None:
        random.seed(None)
        return random.randint(0, pow(10, seeddigits) - 1)
    return seed


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
    world.seed = get_seed(seed)
    if args.race:
        world.secure()
    else:
        world.random.seed(world.seed)

    world.remote_items = args.remote_items.copy()
    world.mapshuffle = args.mapshuffle.copy()
    world.compassshuffle = args.compassshuffle.copy()
    world.keyshuffle = args.keyshuffle.copy()
    world.bigkeyshuffle = args.bigkeyshuffle.copy()
    world.crystals_needed_for_ganon = {
        player: world.random.randint(0, 7) if args.crystals_ganon[player] == 'random' else int(
            args.crystals_ganon[player]) for player in range(1, world.players + 1)}
    world.crystals_needed_for_gt = {
        player: world.random.randint(0, 7) if args.crystals_gt[player] == 'random' else int(args.crystals_gt[player])
        for player in range(1, world.players + 1)}
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
    world.progressive = args.progressive.copy()
    world.dungeon_counters = args.dungeon_counters.copy()
    world.glitch_boots = args.glitch_boots.copy()
    world.triforce_pieces_available = args.triforce_pieces_available.copy()
    world.triforce_pieces_required = args.triforce_pieces_required.copy()
    world.shop_shuffle = args.shop_shuffle.copy()
    world.shop_shuffle_slots = args.shop_shuffle_slots.copy()
    world.progression_balancing = {player: not balance for player, balance in args.skip_progression_balancing.items()}
    world.shuffle_prizes = args.shuffle_prizes.copy()
    world.sprite_pool = args.sprite_pool.copy()
    world.dark_room_logic = args.dark_room_logic.copy()
    world.plando_items = args.plando_items.copy()
    world.plando_texts = args.plando_texts.copy()
    world.plando_connections = args.plando_connections.copy()
    world.restrict_dungeon_item_on_boss = args.restrict_dungeon_item_on_boss.copy()
    world.required_medallions = args.required_medallions.copy()

    world.rom_seeds = {player: random.Random(world.random.randint(0, 999999999)) for player in range(1, world.players + 1)}

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

        for tok in filter(None, args.startinventory[player].split(',')):
            item = ItemFactory(tok.strip(), player)
            if item:
                world.push_precollected(item)
        # item in item_table gets checked in mystery, but not CLI - so we double-check here
        world.local_items[player] = {item.strip() for item in args.local_items[player].split(',') if
                                     item.strip() in item_table}
        world.non_local_items[player] = {item.strip() for item in args.non_local_items[player].split(',') if
                                         item.strip() in item_table}

        # enforce pre-defined local items.
        if world.goal[player] in ["localtriforcehunt", "localganontriforcehunt"]:
            world.local_items[player].add('Triforce Piece')

        # items can't be both local and non-local, prefer local
        world.non_local_items[player] -= world.local_items[player]

        # dungeon items can't be in non-local if the appropriate dungeon item shuffle setting is not set.
        if not world.mapshuffle[player]:
            world.non_local_items[player] -= item_name_groups['Maps']

        if not world.compassshuffle[player]:
            world.non_local_items[player] -= item_name_groups['Compasses']

        if not world.keyshuffle[player]:
            world.non_local_items[player] -= item_name_groups['Small Keys']

        if not world.bigkeyshuffle[player]:
            world.non_local_items[player] -= item_name_groups['Big Keys']

        # Not possible to place pendants/crystals out side of boss prizes yet.
        world.non_local_items[player] -= item_name_groups['Pendants']
        world.non_local_items[player] -= item_name_groups['Crystals']

        world.triforce_pieces_available[player] = max(world.triforce_pieces_available[player], world.triforce_pieces_required[player])

        if world.mode[player] != 'inverted':
            create_regions(world, player)
        else:
            create_inverted_regions(world, player)
        create_shops(world, player)
        create_dungeons(world, player)

    logger.info('Shuffling the World about.')

    for player in range(1, world.players + 1):
        if world.logic[player] not in ["noglitches", "minorglitches"] and world.shuffle[player] in \
                {"vanilla", "dungeonssimple", "dungeonsfull", "simple", "restricted", "full"}:
            world.fix_fake_world[player] = False

        if world.mode[player] != 'inverted':
            link_entrances(world, player)
            mark_light_world_regions(world, player)
        else:
            link_inverted_entrances(world, player)
            mark_dark_world_regions(world, player)
        plando_connect(world, player)

    logger.info('Generating Item Pool.')

    for player in range(1, world.players + 1):
        generate_itempool(world, player)

    logger.info('Calculating Access Rules.')

    for player in range(1, world.players + 1):
        set_rules(world, player)

    logger.info('Placing Dungeon Prizes.')

    fill_prizes(world)

    logger.info("Running Item Plando")

    distribute_planned(world)

    logger.info('Placing Dungeon Items.')

    if args.algorithm in ['balanced', 'vt26'] or any(
            list(args.mapshuffle.values()) + list(args.compassshuffle.values()) +
            list(args.keyshuffle.values()) + list(args.bigkeyshuffle.values())):
        fill_dungeons_restrictive(world)
    else:
        fill_dungeons(world)

    logger.info('Fill the world.')

    if args.algorithm == 'flood':
        flood_items(world)  # different algo, biased towards early game progress items
    elif args.algorithm == 'vt25':
        distribute_items_restrictive(world, False)
    elif args.algorithm == 'vt26':
        distribute_items_restrictive(world, True)
    elif args.algorithm == 'balanced':
        distribute_items_restrictive(world, True)

    if world.players > 1:
        balance_multiworld_progression(world)

    logger.info("Filling Shop Slots")

    ShopSlotFill(world)

    logger.info('Patching ROM.')



    outfilebase = 'BM_%s' % (args.outputname if args.outputname else world.seed)

    rom_names = []

    def _gen_rom(team: int, player: int):
        use_enemizer = (world.boss_shuffle[player] != 'none' or world.enemy_shuffle[player]
                        or world.enemy_health[player] != 'default' or world.enemy_damage[player] != 'default'
                        or world.shufflepots[player] or world.bush_shuffle[player]
                        or world.killable_thieves[player])

        rom = LocalRom(args.rom)

        patch_rom(world, rom, player, team, use_enemizer)

        if use_enemizer:
            patch_enemizer(world, player, rom, args.enemizercli)

        if args.race:
            patch_race_rom(rom, world, player)

        world.spoiler.hashes[(player, team)] = get_hash_string(rom.hash)

        palettes_options={}
        palettes_options['dungeon']=args.uw_palettes[player]
        palettes_options['overworld']=args.ow_palettes[player]
        palettes_options['hud']=args.hud_palettes[player]
        palettes_options['sword']=args.sword_palettes[player]
        palettes_options['shield']=args.shield_palettes[player]
        palettes_options['link']=args.link_palettes[player]
        
        apply_rom_settings(rom, args.heartbeep[player], args.heartcolor[player], args.quickswap[player],
                           args.fastmenu[player], args.disablemusic[player], args.sprite[player],
                           palettes_options, world, player, True)

        mcsb_name = ''
        if all([world.mapshuffle[player], world.compassshuffle[player], world.keyshuffle[player],
                world.bigkeyshuffle[player]]):
            mcsb_name = '-keysanity'
        elif [world.mapshuffle[player], world.compassshuffle[player], world.keyshuffle[player],
              world.bigkeyshuffle[player]].count(True) == 1:
            mcsb_name = '-mapshuffle' if world.mapshuffle[player] else \
                '-compassshuffle' if world.compassshuffle[player] else \
                '-universal_keys' if world.keyshuffle[player] == "universal" else \
                '-keyshuffle' if world.keyshuffle[player] else '-bigkeyshuffle'
        elif any([world.mapshuffle[player], world.compassshuffle[player], world.keyshuffle[player],
                  world.bigkeyshuffle[player]]):
            mcsb_name = '-%s%s%s%sshuffle' % (
                'M' if world.mapshuffle[player] else '', 'C' if world.compassshuffle[player] else '',
                'U' if world.keyshuffle[player] == "universal" else 'S' if world.keyshuffle[player] else '',
                'B' if world.bigkeyshuffle[player] else '')

        outfilepname = f'_T{team + 1}' if world.teams > 1 else ''
        outfilepname += f'_P{player}'
        outfilepname += f"_{world.player_names[player][team].replace(' ', '_')}" \
            if world.player_names[player][team] != 'Player%d' % player else ''
        outfilestuffs = {
          "logic": world.logic[player],                                    # 0
          "difficulty": world.difficulty[player],                          # 1
          "difficulty_adjustments": world.difficulty_adjustments[player],  # 2
          "mode": world.mode[player],                                      # 3
          "goal": world.goal[player],                                      # 4
          "timer": str(world.timer[player]),                               # 5
          "shuffle": world.shuffle[player],                                # 6
          "algorithm": world.algorithm,                                    # 7
          "mscb": mcsb_name,                                               # 8
          "retro": world.retro[player],                                    # 9
          "progressive": world.progressive,                                # A
          "hints": 'True' if world.hints[player] else 'False'              # B
        }
        #                  0  1  2  3  4 5  6  7 8 9 A B
        outfilesuffix = ('_%s_%s-%s-%s-%s%s_%s-%s%s%s%s%s' % (
          #  0          1      2      3    4     5    6      7     8        9         A     B           C
          # _noglitches_normal-normal-open-ganon-ohko_simple-balanced-keysanity-retro-prog_random-nohints
          # _noglitches_normal-normal-open-ganon     _simple-balanced-keysanity-retro
          # _noglitches_normal-normal-open-ganon     _simple-balanced-keysanity      -prog_random
          # _noglitches_normal-normal-open-ganon     _simple-balanced-keysanity                  -nohints
          outfilestuffs["logic"], # 0

          outfilestuffs["difficulty"],              # 1
          outfilestuffs["difficulty_adjustments"],  # 2
          outfilestuffs["mode"],                    # 3
          outfilestuffs["goal"],                    # 4
          "" if outfilestuffs["timer"] in ['False', 'none', 'display'] else "-" + outfilestuffs["timer"], # 5

          outfilestuffs["shuffle"],     # 6
          outfilestuffs["algorithm"],   # 7
          outfilestuffs["mscb"],        # 8

          "-retro" if outfilestuffs["retro"] == "True" else "",  # 9
          "-prog_" + outfilestuffs["progressive"] if outfilestuffs["progressive"] in ['off', 'random'] else "",  # A
          "-nohints" if not outfilestuffs["hints"] == "True" else "")  # B
        ) if not args.outputname else ''
        rompath = output_path(f'{outfilebase}{outfilepname}{outfilesuffix}.sfc')
        rom.write_to_file(rompath, hide_enemizer=True)
        if args.create_diff:
            Patch.create_patch_file(rompath)
        return player, team, bytes(rom.name).decode()

    pool = concurrent.futures.ThreadPoolExecutor()
    multidata_task = None
    check_accessibility_task = pool.submit(world.fulfills_accessibility)
    if not args.suppress_rom:

        rom_futures = []

        for team in range(world.teams):
            for player in range(1, world.players + 1):
                rom_futures.append(pool.submit(_gen_rom, team, player))

        def get_entrance_to_region(region: Region):
            for entrance in region.entrances:
                if entrance.parent_region.type in (RegionType.DarkWorld, RegionType.LightWorld):
                    return entrance
            for entrance in region.entrances:  # BFS might be better here, trying DFS for now.
                return get_entrance_to_region(entrance.parent_region)

        # collect ER hint info
        er_hint_data = {player: {} for player in range(1, world.players + 1) if world.shuffle[player] != "vanilla" or world.retro[player]}
        from Regions import RegionType
        for region in world.regions:
            if region.player in er_hint_data and region.locations:
                main_entrance = get_entrance_to_region(region)
                for location in region.locations:
                    if type(location.address) == int:  # skips events and crystals
                        if location.address >= SHOP_ID_START + 33:  continue
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
            if location.parent_region.dungeon:
                dungeonname = {'Inverted Agahnims Tower': 'Agahnims Tower',
                               'Inverted Ganons Tower': 'Ganons Tower'}\
                    .get(location.parent_region.dungeon.name, location.parent_region.dungeon.name)
                checks_in_area[location.player][dungeonname].append(location.address)
            elif main_entrance.parent_region.type == RegionType.LightWorld:
                checks_in_area[location.player]["Light World"].append(location.address)
            elif main_entrance.parent_region.type == RegionType.DarkWorld:
                checks_in_area[location.player]["Dark World"].append(location.address)
            checks_in_area[location.player]["Total"] += 1

        oldmancaves = []
        for region in [world.get_region("Old Man Sword Cave", player) for player in range(1, world.players + 1) if world.retro[player]]:
            item = ItemFactory(region.shop.inventory[0]['item'], region.player)
            player = region.player
            location_id = SHOP_ID_START + 33

            if region.type == RegionType.LightWorld:
                checks_in_area[player]["Light World"].append(location_id)
            else:
                checks_in_area[player]["Dark World"].append(location_id)
            checks_in_area[player]["Total"] += 1

            er_hint_data[player][location_id] = get_entrance_to_region(region).name
            oldmancaves.append(((location_id, player), (item.code, player)))

        precollected_items = [[] for player in range(world.players)]
        for item in world.precollected_items:
            precollected_items[item.player - 1].append(item.code)

        def write_multidata(roms):
            for future in roms:
                rom_name = future.result()
                rom_names.append(rom_name)
            multidatatags = ["ER"]
            if args.race:
                multidatatags.append("Race")
            if args.create_spoiler:
                multidatatags.append("Spoiler")
                if not args.skip_playthrough:
                    multidatatags.append("Play through")
            minimum_versions = {"server": (1, 0, 0)}
            minimum_versions["clients"] = client_versions = []
            for (slot, team, name) in rom_names:
                if world.shop_shuffle_slots[slot]:
                    client_versions.append([team, slot, [3, 6, 1]])
            multidata = zlib.compress(json.dumps({"names": parsed_names,
                                                  # backwards compat for < 2.4.1
                                                  "roms": [(slot, team, list(name.encode()))
                                                           for (slot, team, name) in rom_names],
                                                  "rom_strings": rom_names,
                                                  "remote_items": [player for player in range(1, world.players + 1) if
                                                                   world.remote_items[player]],
                                                  "locations": [((location.address, location.player),
                                                                 (location.item.code, location.item.player))
                                                                for location in world.get_filled_locations() if
                                                                type(location.address) is int] + oldmancaves,
                                                  "checks_in_area": checks_in_area,
                                                  "server_options": get_options()["server_options"],
                                                  "er_hint_data": er_hint_data,
                                                  "precollected_items": precollected_items,
                                                  "version": _version_tuple,
                                                  "tags": multidatatags,
                                                  "minimum_versions": minimum_versions,
                                                  "lookup_region_id_to_name": lookup_region_id_to_name,
                                                  "lookup_items_id_to_name": {key: value for key, value in lookup_items_id_to_name.items() if isinstance(key, int)},
                                                  "item_name_groups": {key: list(value) for key, value in item_name_groups.items()}
                                                  }).encode("utf-8"), 9)

            with open(output_path('%s.multidata' % outfilebase), 'wb') as f:
                f.write(multidata)

        multidata_task = pool.submit(write_multidata, rom_futures)
    if not check_accessibility_task.result():
        if not world.can_beat_game():
            raise Exception("Game appears is unbeatable. Aborting.")
        else:
            logger.warning("Location Accessibility requirements not fulfilled.")
    if not args.skip_playthrough:
        logger.info('Calculating playthrough.')
        create_playthrough(world)
    if multidata_task:
        multidata_task.result()  # retrieve exception if one exists
    pool.shutdown()  # wait for all queued tasks to complete
    if args.create_spoiler:  # needs spoiler.hashes to be filled, that depend on rom_futures being done
        world.spoiler.to_file(output_path('%s_Spoiler.txt' % outfilebase))

    logger.info('Done. Enjoy. Total Time: %s', time.perf_counter() - start)
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
    ret.shuffle_prizes = world.shuffle_prizes.copy()
    ret.shop_shuffle =  world.shop_shuffle.copy()
    ret.shop_shuffle_slots = world.shop_shuffle_slots.copy()
    ret.dark_room_logic = world.dark_room_logic.copy()
    ret.restrict_dungeon_item_on_boss = world.restrict_dungeon_item_on_boss.copy()

    for player in range(1, world.players + 1):
        if world.mode[player] != 'inverted':
            create_regions(ret, player)
        else:
            create_inverted_regions(ret, player)
        create_shops(ret, player)
        create_dungeons(ret, player)

    copy_dynamic_regions_and_locations(world, ret)

    # copy bosses
    for dungeon in world.dungeons:
        for level, boss in dungeon.bosses.items():
            ret.get_dungeon(dungeon.name, dungeon.player).bosses[level] = boss

    for shop in world.shops:
        copied_shop = ret.get_region(shop.region.name, shop.region.player).shop
        copied_shop.inventory = copy.copy(shop.inventory)

    # connect copied world
    for region in world.regions:
        copied_region = ret.get_region(region.name, region.player)
        copied_region.is_light_world = region.is_light_world
        copied_region.is_dark_world = region.is_dark_world
        for exit in copied_region.exits:
            old_connection = world.get_entrance(exit.name, exit.player).connected_region
            exit.connect(ret.get_region(old_connection.name, old_connection.player))

    # fill locations
    for location in world.get_locations():
        if location.item is not None:
            item = Item(location.item.name, location.item.advancement, location.item.priority, location.item.type, player = location.item.player)
            ret.get_location(location.name, location.player).item = item
            item.location = ret.get_location(location.name, location.player)
            item.world = ret
        if location.event:
            ret.get_location(location.name, location.player).event = True
        if location.locked:
            ret.get_location(location.name, location.player).locked = True

    # copy remaining itempool. No item in itempool should have an assigned location
    for item in world.itempool:
        ret.itempool.append(Item(item.name, item.advancement, item.priority, item.type, player = item.player))

    for item in world.precollected_items:
        ret.push_precollected(ItemFactory(item.name, item.player))

    # copy progress items in state
    ret.state.prog_items = world.state.prog_items.copy()
    ret.state.stale = {player: True for player in range(1, world.players + 1)}

    for player in range(1, world.players + 1):
        set_rules(ret, player)


    return ret


def copy_dynamic_regions_and_locations(world, ret):
    for region in world.dynamic_regions:
        new_reg = Region(region.name, region.type, region.hint_text, region.player)
        ret.regions.append(new_reg)
        ret.initialize_regions([new_reg])
        ret.dynamic_regions.append(new_reg)

        # Note: ideally exits should be copied here, but the current use case (Take anys) do not require this

        if region.shop:
            new_reg.shop = region.shop.__class__(new_reg, region.shop.room_id, region.shop.shopkeeper_config,
                                                 region.shop.custom, region.shop.locked)
            ret.shops.append(new_reg.shop)

    for location in world.dynamic_locations:
        new_reg = ret.get_region(location.parent_region.name, location.parent_region.player)
        new_loc = Location(location.player, location.name, location.address, location.crystal, location.hint_text, new_reg)
        # todo: this is potentially dangerous. later refactor so we
        # can apply dynamic region rules on top of copied world like other rules
        new_loc.access_rule = location.access_rule
        new_loc.always_allow = location.always_allow
        new_loc.item_rule = location.item_rule
        new_reg.locations.append(new_loc)

    ret.clear_location_cache()


def create_playthrough(world):
    # create a copy as we will modify it
    old_world = world
    world = copy_world(world)

    # get locations containing progress items
    prog_locations = [location for location in world.get_filled_locations() if location.item.advancement]
    state_cache = [None]
    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = list(prog_locations)
    logging.debug('Building up collection spheres.')
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
