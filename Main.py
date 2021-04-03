import copy
from itertools import zip_longest
import logging
import os
import random
import time
import zlib
import concurrent.futures
import pickle
from typing import Dict

from BaseClasses import MultiWorld, CollectionState, Region, Item
from worlds.alttp import ALttPLocation
from worlds.alttp.Items import ItemFactory, item_table, item_name_groups
from worlds.alttp.Regions import create_regions, mark_light_world_regions, \
    lookup_vanilla_location_to_entrance
from worlds.alttp.InvertedRegions import create_inverted_regions, mark_dark_world_regions
from worlds.alttp.EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect
from worlds.alttp.Rom import patch_rom, patch_race_rom, patch_enemizer, apply_rom_settings, LocalRom, get_hash_string
from worlds.alttp.Rules import set_rules
from worlds.alttp.Dungeons import create_dungeons, fill_dungeons, fill_dungeons_restrictive
from Fill import distribute_items_restrictive, flood_items, balance_multiworld_progression, distribute_planned
from worlds.alttp.Shops import create_shops, ShopSlotFill, SHOP_ID_START, total_shop_slots, FillDisabledShopSlots
from worlds.alttp.ItemPool import generate_itempool, difficulties, fill_prizes
from Utils import output_path, parse_player_names, get_options, __version__, _version_tuple
from worlds.hk import gen_hollow, set_rules as set_hk_rules
from worlds.hk import create_regions as hk_create_regions
from worlds.factorio import gen_factorio, factorio_create_regions
from worlds.factorio.Mod import generate_mod
from worlds.generic.Rules import locality_rules
from worlds import Games
import Patch

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

    # initialize the world
    world = MultiWorld(args.multi)

    logger = logging.getLogger('')
    world.seed = get_seed(seed)
    if args.race:
        world.secure()
    else:
        world.random.seed(world.seed)

    world.shuffle = args.shuffle.copy()
    world.logic = args.logic.copy()
    world.mode = args.mode.copy()
    world.swords = args.swords.copy()
    world.difficulty = args.difficulty.copy()
    world.item_functionality = args.item_functionality.copy()
    world.timer = args.timer.copy()
    world.progressive = args.progressive.copy()
    world.goal = args.goal.copy()
    world.local_items = args.local_items.copy()
    if hasattr(args, "algorithm"): # current GUI options
        world.algorithm = args.algorithm
        world.shuffleganon = args.shuffleganon
        world.custom = args.custom
        world.customitemarray = args.customitemarray

    world.accessibility = args.accessibility.copy()
    world.retro = args.retro.copy()

    world.hints = args.hints.copy()

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
    import Options
    for hk_option in Options.hollow_knight_options:
        setattr(world, hk_option, getattr(args, hk_option, {}))
    for factorio_option in Options.factorio_options:
        setattr(world, factorio_option, getattr(args, factorio_option, {}))
    world.glitch_triforce = args.glitch_triforce  # This is enabled/disabled globally, no per player option.

    world.rom_seeds = {player: random.Random(world.random.randint(0, 999999999)) for player in range(1, world.players + 1)}

    for player in range(1, world.players+1):
        world.er_seeds[player] = str(world.random.randint(0, 2 ** 64))

        if "-" in world.shuffle[player]:
            shuffle, seed = world.shuffle[player].split("-", 1)
            world.shuffle[player] = shuffle
            if shuffle == "vanilla":
                world.er_seeds[player] = "vanilla"
            elif seed.startswith("group-") or args.race:
                # renamed from team to group to not confuse with existing team name use
                world.er_seeds[player] = get_same_seed(world, (shuffle, seed, world.retro[player], world.mode[player], world.logic[player]))
            else:  # not a race or group seed, use set seed as is.
                world.er_seeds[player] = seed
        elif world.shuffle[player] == "vanilla":
            world.er_seeds[player] = "vanilla"

    logger.info('Archipelago Version %s  -  Seed: %s\n', __version__, world.seed)

    parsed_names = parse_player_names(args.names, world.players, args.teams)
    world.teams = len(parsed_names)
    for i, team in enumerate(parsed_names, 1):
        if world.players > 1:
            logger.info('%s%s', 'Team%d: ' % i if world.teams > 1 else 'Players: ', ', '.join(team))
        for player, name in enumerate(team, 1):
            world.player_names[player].append(name)

    logger.info('')

    for player in world.alttp_player_ids:
        world.difficulty_requirements[player] = difficulties[world.difficulty[player]]

    for player in world.player_ids:
        for tok in filter(None, args.startinventory[player].split(',')):
            item = ItemFactory(tok.strip(), player)
            if item:
                world.push_precollected(item)

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

    for player in world.hk_player_ids:
        hk_create_regions(world, player)

    for player in world.factorio_player_ids:
        factorio_create_regions(world, player)

    for player in world.alttp_player_ids:
        if world.open_pyramid[player] == 'goal':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt', 'localganontriforcehunt', 'ganonpedestal'}
        elif world.open_pyramid[player] == 'auto':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt', 'localganontriforcehunt', 'ganonpedestal'} and \
                                         (world.shuffle[player] in {'vanilla', 'dungeonssimple', 'dungeonsfull'} or not world.shuffle_ganon)
        else:
            world.open_pyramid[player] = {'on': True, 'off': False, 'yes': True, 'no': False}.get(world.open_pyramid[player], world.open_pyramid[player])


        world.triforce_pieces_available[player] = max(world.triforce_pieces_available[player], world.triforce_pieces_required[player])

        if world.mode[player] != 'inverted':
            create_regions(world, player)
        else:
            create_inverted_regions(world, player)
        create_shops(world, player)
        create_dungeons(world, player)

    logger.info('Shuffling the World about.')

    for player in world.alttp_player_ids:
        if world.logic[player] not in ["noglitches", "minorglitches"] and world.shuffle[player] in \
                {"vanilla", "dungeonssimple", "dungeonsfull", "simple", "restricted", "full"}:
            world.fix_fake_world[player] = False

        # seeded entrance shuffle
        old_random = world.random
        world.random = random.Random(world.er_seeds[player])

        if world.mode[player] != 'inverted':
            link_entrances(world, player)
            mark_light_world_regions(world, player)
        else:
            link_inverted_entrances(world, player)
            mark_dark_world_regions(world, player)

        world.random = old_random
        plando_connect(world, player)

    logger.info('Generating Item Pool.')

    for player in world.alttp_player_ids:
        generate_itempool(world, player)

    logger.info('Calculating Access Rules.')
    if world.players > 1:
        for player in world.player_ids:
            locality_rules(world, player)

    for player in world.alttp_player_ids:
        set_rules(world, player)

    for player in world.hk_player_ids:
        gen_hollow(world, player)

    for player in world.factorio_player_ids:
        gen_factorio(world, player)

    logger.info("Running Item Plando")

    for item in world.itempool:
        item.world = world

    distribute_planned(world)

    logger.info('Placing Dungeon Prizes.')

    fill_prizes(world)

    logger.info('Placing Dungeon Items.')

    if world.algorithm in ['balanced', 'vt26'] or any(
            list(args.mapshuffle.values()) + list(args.compassshuffle.values()) +
            list(args.keyshuffle.values()) + list(args.bigkeyshuffle.values())):
        fill_dungeons_restrictive(world)
    else:
        fill_dungeons(world)

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

    if world.players > 1:
        balance_multiworld_progression(world)

    logger.info('Generating output files.')

    outfilebase = 'AP_%s' % (args.outputname if args.outputname else world.seed)

    rom_names = []

    def _gen_rom(team: int, player: int):
        use_enemizer = (world.boss_shuffle[player] != 'none' or world.enemy_shuffle[player]
                        or world.enemy_health[player] != 'default' or world.enemy_damage[player] != 'default'
                        or world.shufflepots[player] or world.bush_shuffle[player]
                        or world.killable_thieves[player])

        rom = LocalRom(args.rom)

        patch_rom(world, rom, player, team, use_enemizer)

        if use_enemizer:
            patch_enemizer(world, team, player, rom, args.enemizercli)

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
                           palettes_options, world, player, True,
                           reduceflashing=args.reduceflashing[player] or args.race,
                           triforcehud=args.triforcehud[player])

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
          "item_functionality": world.item_functionality[player],          # 2
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
          outfilestuffs["item_functionality"],      # 2
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
        return player, team, bytes(rom.name)

    pool = concurrent.futures.ThreadPoolExecutor()
    multidata_task = None
    check_accessibility_task = pool.submit(world.fulfills_accessibility)
    if not args.suppress_rom:

        rom_futures = []
        mod_futures = []
        for team in range(world.teams):
            for player in world.alttp_player_ids:
                rom_futures.append(pool.submit(_gen_rom, team, player))
        for player in world.factorio_player_ids:
            mod_futures.append(pool.submit(generate_mod, world, player))

        def get_entrance_to_region(region: Region):
            for entrance in region.entrances:
                if entrance.parent_region.type in (RegionType.DarkWorld, RegionType.LightWorld):
                    return entrance
            for entrance in region.entrances:  # BFS might be better here, trying DFS for now.
                return get_entrance_to_region(entrance.parent_region)

        # collect ER hint info
        er_hint_data = {player: {} for player in range(1, world.players + 1) if world.shuffle[player] != "vanilla" or world.retro[player]}
        from worlds.alttp.Regions import RegionType
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
            if location.game != Games.LTTP:
                checks_in_area[location.player]["Light World"].append(location.address)
            elif location.parent_region.dungeon:
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
        takeanyregions = ["Old Man Sword Cave", "Take-Any #1", "Take-Any #2", "Take-Any #3", "Take-Any #4"]
        for index, take_any in enumerate(takeanyregions):
            for region in [world.get_region(take_any, player) for player in range(1, world.players + 1) if world.retro[player]]:
                item = ItemFactory(region.shop.inventory[(0 if take_any == "Old Man Sword Cave" else 1)]['item'], region.player)
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

        precollected_items = [[] for player in range(world.players)]
        for item in world.precollected_items:
            precollected_items[item.player - 1].append(item.code)

        FillDisabledShopSlots(world)

        def write_multidata(roms, mods):
            import base64
            for future in roms:
                rom_name = future.result()
                rom_names.append(rom_name)
            minimum_versions = {"server": (0, 0, 2)}
            connect_names = {base64.b64encode(rom_name).decode(): (team, slot) for
                              slot, team, rom_name in rom_names}

            for i, team in enumerate(parsed_names):
                for player, name in enumerate(team, 1):
                    if player not in world.alttp_player_ids:
                        connect_names[name] = (i, player)
            multidata = zlib.compress(pickle.dumps({"names": parsed_names,
                                                    "connect_names": connect_names,
                                                    "remote_items": {player for player in range(1, world.players + 1) if
                                                                     world.remote_items[player] or
                                                                     world.game[player] != "A Link to the Past"},
                                                    "locations": {
                                                        (location.address, location.player):
                                                            (location.item.code, location.item.player)
                                                        for location in world.get_filled_locations() if
                                                        type(location.address) is int},
                                                    "checks_in_area": checks_in_area,
                                                    "server_options": get_options()["server_options"],
                                                    "er_hint_data": er_hint_data,
                                                    "precollected_items": precollected_items,
                                                    "version": tuple(_version_tuple),
                                                    "tags": ["AP"],
                                                    "minimum_versions": minimum_versions,
                                                    }), 9)

            with open(output_path('%s.archipelago' % outfilebase), 'wb') as f:
                f.write(bytes([1]))  # version of format
                f.write(multidata)
            for future in mods:
                future.result() # collect errors if they occured

        multidata_task = pool.submit(write_multidata, rom_futures, mod_futures)
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
    if args.create_spoiler:  # needs spoiler.hashes to be filled, that depend on rom_futures being done
        world.spoiler.to_file(output_path('%s_Spoiler.txt' % outfilebase))

    logger.info('Done. Enjoy. Total Time: %s', time.perf_counter() - start)
    return world



def copy_world(world):
    # ToDo: Not good yet
    # delete now?
    ret = MultiWorld(world.players, world.shuffle, world.logic, world.mode, world.swords, world.difficulty, world.item_functionality, world.timer, world.progressive, world.goal, world.algorithm, world.accessibility, world.shuffle_ganon, world.retro, world.custom, world.customitemarray, world.hints)
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
    ret.game = world.game.copy()
    ret.completion_condition = world.completion_condition.copy()

    for player in world.alttp_player_ids:
        if world.mode[player] != 'inverted':
            create_regions(ret, player)
        else:
            create_inverted_regions(ret, player)
        create_shops(ret, player)
        create_dungeons(ret, player)

    for player in world.hk_player_ids:
        hk_create_regions(ret, player)

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
            item = Item(location.item.name, location.item.advancement, location.item.code, player = location.item.player)
            ret.get_location(location.name, location.player).item = item
            item.location = ret.get_location(location.name, location.player)
            item.world = ret
            item.type = location.item.type
            item.game = location.item.game

        if location.event:
            ret.get_location(location.name, location.player).event = True
        if location.locked:
            ret.get_location(location.name, location.player).locked = True


    # copy remaining itempool. No item in itempool should have an assigned location
    for old_item in world.itempool:
        item = Item(old_item.name, old_item.advancement, old_item.code, player = old_item.player)
        item.type = old_item.type
        ret.itempool.append(item)

    for old_item in world.precollected_items:
        item = Item(old_item.name, old_item.advancement, old_item.code, player = old_item.player)
        item.type = old_item.type
        ret.push_precollected(item)

    # copy progress items in state
    ret.state.prog_items = world.state.prog_items.copy()
    ret.state.stale = {player: True for player in range(1, world.players + 1)}

    for player in world.alttp_player_ids:
        set_rules(ret, player)

    for player in world.hk_player_ids:
        set_hk_rules(ret, player)


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
                                                 region.shop.custom, region.shop.locked, region.shop.sram_offset)
            ret.shops.append(new_reg.shop)

    for location in world.dynamic_locations:
        new_reg = ret.get_region(location.parent_region.name, location.parent_region.player)
        new_loc = ALttPLocation(location.player, location.name, location.address, location.crystal, location.hint_text, new_reg)
        # todo: this is potentially dangerous. later refactor so we
        # can apply dynamic region rules on top of copied world like other rules
        new_loc.access_rule = location.access_rule
        new_loc.always_allow = location.always_allow
        new_loc.item_rule = location.item_rule
        new_reg.locations.append(new_loc)

    ret.clear_location_cache()


def create_playthrough(world):
    """Destructive to the world it is run on."""
    # get locations containing progress items
    prog_locations = {location for location in world.get_filled_locations() if location.item.advancement}
    state_cache = [None]
    collection_spheres = []
    state = CollectionState(world)
    sphere_candidates = set(prog_locations)
    logging.debug('Building up collection spheres.')
    while sphere_candidates:
        state.sweep_for_events(key_only=True)

        # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres

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
            logging.debug('Checking if %s (Player %d) is required to beat the game.', location.item.name, location.item.player)
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

        logging.debug('Calculated final sphere %i, containing %i of %i progress items.', len(collection_spheres), len(sphere), len(required_locations))
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

    world.spoiler.paths = dict()
    for player in range(1, world.players + 1):
        world.spoiler.paths.update({ str(location) : get_path(state, location.parent_region) for sphere in collection_spheres for location in sphere if location.player == player})
        if player in world.alttp_player_ids:
            for path in dict(world.spoiler.paths).values():
                if any(exit == 'Pyramid Fairy' for (_, exit) in path):
                    if world.mode[player] != 'inverted':
                        world.spoiler.paths[str(world.get_region('Big Bomb Shop', player))] = get_path(state, world.get_region('Big Bomb Shop', player))
                    else:
                        world.spoiler.paths[str(world.get_region('Inverted Big Bomb Shop', player))] = get_path(state, world.get_region('Inverted Big Bomb Shop', player))

    # we can finally output our playthrough
    world.spoiler.playthrough = {"0": sorted([str(item) for item in world.precollected_items if item.advancement])}

    for i, sphere in enumerate(collection_spheres):
        world.spoiler.playthrough[str(i + 1)] = {str(location): str(location.item) for location in sorted(sphere)}

    # repair the world again
    for location, item in restore_later.items():
        location.item = item

    for item in removed_precollected:
        world.push_precollected(item)
