import random
import logging
import os
import threading
import typing

from BaseClasses import Item, CollectionState, Tutorial
from .SubClasses import ALttPItem
from ..AutoWorld import World, WebWorld, LogicMixin
from .Options import alttp_options, smallkey_shuffle
from .Items import as_dict_item_table, item_name_groups, item_table, GetBeemizerItem
from .Regions import lookup_name_to_id, create_regions, mark_light_world_regions
from .Rules import set_rules
from .ItemPool import generate_itempool, difficulties
from .Shops import create_shops, ShopSlotFill
from .Dungeons import create_dungeons
from .Rom import LocalRom, patch_rom, patch_race_rom, patch_enemizer, apply_rom_settings, get_hash_string, \
    get_base_rom_path, LttPDeltaPatch
import Patch
from itertools import chain

from .InvertedRegions import create_inverted_regions, mark_dark_world_regions
from .EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect

lttp_logger = logging.getLogger("A Link to the Past")


class ALTTPWeb(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago ALttP Software on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Farrak Kilhn"]
    )

    setup_de = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Deutsch",
        "multiworld_de.md",
        "multiworld/de",
        ["Fischfilet"]
    )

    setup_es = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Español",
        "multiworld_es.md",
        "multiworld/es",
        ["Edos"]
    )

    setup_fr = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Français",
        "multiworld_fr.md",
        "multiworld/fr",
        ["Coxla"]
    )

    msu = Tutorial(
        "MSU-1 Setup Tutorial",
        "A guide to setting up MSU-1, which allows for custom in-game music.",
        "English",
        "msu1_en.md",
        "msu1/en",
        ["Farrak Kilhn"]
    )

    msu_es = Tutorial(
        msu.tutorial_name,
        msu.description,
        "Español",
        "msu1_es.md",
        "msu1/en",
        ["Edos"]
    )

    msu_fr = Tutorial(
        msu.tutorial_name,
        msu.description,
        "Français",
        "msu1_fr.md",
        "msu1/fr",
        ["Coxla"]
    )

    plando = Tutorial(
        "Plando Tutorial",
        "A guide to creating Multiworld Plandos with LTTP",
        "English",
        "plando_en.md",
        "plando/en",
        ["Berserker"]
    )

    tutorials = [setup_en, setup_de, setup_es, setup_fr, msu, msu_es, msu_fr, plando]


class ALTTPWorld(World):
    """
    The Legend of Zelda: A Link to the Past is an action/adventure game. Take on the role of
    Link, a boy who is destined to save the land of Hyrule. Delve through three palaces and nine
    dungeons on your quest to rescue the descendents of the seven wise men and defeat the evil
    Ganon!
    """
    game: str = "A Link to the Past"
    options = alttp_options
    topology_present = True
    item_name_groups = item_name_groups
    hint_blacklist = {"Triforce"}

    item_name_to_id = {name: data.item_code for name, data in item_table.items() if type(data.item_code) == int}
    location_name_to_id = lookup_name_to_id

    data_version = 8
    remote_items: bool = False
    remote_start_inventory: bool = False
    required_client_version = (0, 3, 2)
    web = ALTTPWeb()

    set_rules = set_rules

    create_items = generate_itempool

    def __init__(self, *args, **kwargs):
        self.dungeon_local_item_names = set()
        self.dungeon_specific_item_names = set()
        self.rom_name_available_event = threading.Event()
        self.has_progressive_bows = False
        super(ALTTPWorld, self).__init__(*args, **kwargs)

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def generate_early(self):
        player = self.player
        world = self.world

        # system for sharing ER layouts
        self.er_seed = str(world.random.randint(0, 2 ** 64))

        if "-" in world.shuffle[player]:
            shuffle, seed = world.shuffle[player].split("-", 1)
            world.shuffle[player] = shuffle
            if shuffle == "vanilla":
                self.er_seed = "vanilla"
            elif seed.startswith("group-") or world.is_race:
                self.er_seed = get_same_seed(world, (
                    shuffle, seed, world.retro_caves[player], world.mode[player], world.logic[player]))
            else:  # not a race or group seed, use set seed as is.
                self.er_seed = seed
        elif world.shuffle[player] == "vanilla":
            self.er_seed = "vanilla"
        for dungeon_item in ["smallkey_shuffle", "bigkey_shuffle", "compass_shuffle", "map_shuffle"]:
            option = getattr(world, dungeon_item)[player]
            if option == "own_world":
                world.local_items[player].value |= self.item_name_groups[option.item_name_group]
            elif option == "different_world":
                world.non_local_items[player].value |= self.item_name_groups[option.item_name_group]
            elif option.in_dungeon:
                self.dungeon_local_item_names |= self.item_name_groups[option.item_name_group]
                if option == "original_dungeon":
                    self.dungeon_specific_item_names |= self.item_name_groups[option.item_name_group]

        world.difficulty_requirements[player] = difficulties[world.difficulty[player]]

    def create_regions(self):
        player = self.player
        world = self.world
        if world.open_pyramid[player] == 'goal':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt',
                                                                'localganontriforcehunt', 'ganonpedestal'}
        elif world.open_pyramid[player] == 'auto':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt',
                                                                'localganontriforcehunt', 'ganonpedestal'} and \
                                         (world.shuffle[player] in {'vanilla', 'dungeonssimple', 'dungeonsfull',
                                                                    'dungeonscrossed'} or not world.shuffle_ganon)
        else:
            world.open_pyramid[player] = {'on': True, 'off': False, 'yes': True, 'no': False}.get(
                world.open_pyramid[player], 'auto')

        world.triforce_pieces_available[player] = max(world.triforce_pieces_available[player],
                                                      world.triforce_pieces_required[player])

        if world.mode[player] != 'inverted':
            create_regions(world, player)
        else:
            create_inverted_regions(world, player)
        create_shops(world, player)
        create_dungeons(world, player)

        if world.logic[player] not in ["noglitches", "minorglitches"] and world.shuffle[player] in \
                {"vanilla", "dungeonssimple", "dungeonsfull", "simple", "restricted", "full"}:
            world.fix_fake_world[player] = False

        # seeded entrance shuffle
        old_random = world.random
        world.random = random.Random(self.er_seed)

        if world.mode[player] != 'inverted':
            link_entrances(world, player)
            mark_light_world_regions(world, player)
        else:
            link_inverted_entrances(world, player)
            mark_dark_world_regions(world, player)

        world.random = old_random
        plando_connect(world, player)

    def collect_item(self, state: CollectionState, item: Item, remove=False):
        item_name = item.name
        if item_name.startswith('Progressive '):
            if remove:
                if 'Sword' in item_name:
                    if state.has('Golden Sword', item.player):
                        return 'Golden Sword'
                    elif state.has('Tempered Sword', item.player):
                        return 'Tempered Sword'
                    elif state.has('Master Sword', item.player):
                        return 'Master Sword'
                    elif state.has('Fighter Sword', item.player):
                        return 'Fighter Sword'
                    else:
                        return None
                elif 'Glove' in item.name:
                    if state.has('Titans Mitts', item.player):
                        return 'Titans Mitts'
                    elif state.has('Power Glove', item.player):
                        return 'Power Glove'
                    else:
                        return None
                elif 'Shield' in item_name:
                    if state.has('Mirror Shield', item.player):
                        return 'Mirror Shield'
                    elif state.has('Red Shield', item.player):
                        return 'Red Shield'
                    elif state.has('Blue Shield', item.player):
                        return 'Blue Shield'
                    else:
                        return None
                elif 'Bow' in item_name:
                    if state.has('Silver Bow', item.player):
                        return 'Silver Bow'
                    elif state.has('Bow', item.player):
                        return 'Bow'
                    else:
                        return None
            else:
                if 'Sword' in item_name:
                    if state.has('Golden Sword', item.player):
                        pass
                    elif state.has('Tempered Sword', item.player) and self.world.difficulty_requirements[
                        item.player].progressive_sword_limit >= 4:
                        return 'Golden Sword'
                    elif state.has('Master Sword', item.player) and self.world.difficulty_requirements[
                        item.player].progressive_sword_limit >= 3:
                        return 'Tempered Sword'
                    elif state.has('Fighter Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                        return 'Master Sword'
                    elif self.world.difficulty_requirements[item.player].progressive_sword_limit >= 1:
                        return 'Fighter Sword'
                elif 'Glove' in item_name:
                    if state.has('Titans Mitts', item.player):
                        return
                    elif state.has('Power Glove', item.player):
                        return 'Titans Mitts'
                    else:
                        return 'Power Glove'
                elif 'Shield' in item_name:
                    if state.has('Mirror Shield', item.player):
                        return
                    elif state.has('Red Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                        return 'Mirror Shield'
                    elif state.has('Blue Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                        return 'Red Shield'
                    elif self.world.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                        return 'Blue Shield'
                elif 'Bow' in item_name:
                    if state.has('Silver Bow', item.player):
                        return
                    elif state.has('Bow', item.player) and (self.world.difficulty_requirements[item.player].progressive_bow_limit >= 2
                        or self.world.logic[item.player] == 'noglitches'
                        or self.world.swordless[item.player]): # modes where silver bow is always required for ganon
                        return 'Silver Bow'
                    elif self.world.difficulty_requirements[item.player].progressive_bow_limit >= 1:
                        return 'Bow'
        elif item.advancement:
            return item_name

    def pre_fill(self):
        from Fill import fill_restrictive, FillError
        attempts = 5
        world = self.world
        player = self.player
        all_state = world.get_all_state(use_cache=True)
        crystals = [self.create_item(name) for name in ['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6']]
        crystal_locations = [world.get_location('Turtle Rock - Prize', player),
                             world.get_location('Eastern Palace - Prize', player),
                             world.get_location('Desert Palace - Prize', player),
                             world.get_location('Tower of Hera - Prize', player),
                             world.get_location('Palace of Darkness - Prize', player),
                             world.get_location('Thieves\' Town - Prize', player),
                             world.get_location('Skull Woods - Prize', player),
                             world.get_location('Swamp Palace - Prize', player),
                             world.get_location('Ice Palace - Prize', player),
                             world.get_location('Misery Mire - Prize', player)]
        placed_prizes = {loc.item.name for loc in crystal_locations if loc.item}
        unplaced_prizes = [crystal for crystal in crystals if crystal.name not in placed_prizes]
        empty_crystal_locations = [loc for loc in crystal_locations if not loc.item]
        for attempt in range(attempts):
            try:
                prizepool = unplaced_prizes.copy()
                prize_locs = empty_crystal_locations.copy()
                world.random.shuffle(prize_locs)
                fill_restrictive(world, all_state, prize_locs, prizepool, True, lock=True)
            except FillError as e:
                lttp_logger.exception("Failed to place dungeon prizes (%s). Will retry %s more times", e,
                                                attempts - attempt)
                for location in empty_crystal_locations:
                    location.item = None
                continue
            break
        else:
            raise FillError('Unable to place dungeon prizes')

    @classmethod
    def stage_pre_fill(cls, world):
        from .Dungeons import fill_dungeons_restrictive
        fill_dungeons_restrictive(world)

    @classmethod
    def stage_post_fill(cls, world):
        ShopSlotFill(world)

    def generate_output(self, output_directory: str):
        world = self.world
        player = self.player
        try:
            use_enemizer = (world.boss_shuffle[player] != 'none' or world.enemy_shuffle[player]
                            or world.enemy_health[player] != 'default' or world.enemy_damage[player] != 'default'
                            or world.pot_shuffle[player] or world.bush_shuffle[player]
                            or world.killable_thieves[player])

            rom = LocalRom(get_base_rom_path())

            patch_rom(world, rom, player, use_enemizer)

            if use_enemizer:
                patch_enemizer(world, player, rom, world.enemizer, output_directory)

            if world.is_race:
                patch_race_rom(rom, world, player)

            world.spoiler.hashes[player] = get_hash_string(rom.hash)

            palettes_options = {
                'dungeon': world.uw_palettes[player],
                'overworld': world.ow_palettes[player],
                'hud': world.hud_palettes[player],
                'sword': world.sword_palettes[player],
                'shield': world.shield_palettes[player],
                'link': world.link_palettes[player]
            }
            palettes_options = {key: option.current_key for key, option in palettes_options.items()}

            apply_rom_settings(rom, world.heartbeep[player].current_key,
                               world.heartcolor[player].current_key,
                               world.quickswap[player],
                               world.menuspeed[player].current_key,
                               world.music[player],
                               world.sprite[player],
                               palettes_options, world, player, True,
                               reduceflashing=world.reduceflashing[player] or world.is_race,
                               triforcehud=world.triforcehud[player].current_key,
                               deathlink=world.death_link[player],
                               allowcollect=world.allow_collect[player])

            outfilepname = f'_P{player}'
            outfilepname += f"_{world.get_file_safe_player_name(player).replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.sfc')
            rom.write_to_file(rompath)
            patch = LttPDeltaPatch(os.path.splitext(rompath)[0]+LttPDeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rompath)
            patch.write()
            os.unlink(rompath)
            self.rom_name = rom.name
        except:
            raise
        finally:
            self.rom_name_available_event.set() # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.world.player_name[self.player]]

    def create_item(self, name: str) -> Item:
        return ALttPItem(name, self.player, **as_dict_item_table[name])

    @classmethod
    def stage_fill_hook(cls, world, progitempool, nonexcludeditempool, localrestitempool, nonlocalrestitempool,
                        restitempool, fill_locations):
        trash_counts = {}
        standard_keyshuffle_players = set()
        for player in world.get_game_players("A Link to the Past"):
            if world.mode[player] == 'standard' and world.smallkey_shuffle[player] \
                    and world.smallkey_shuffle[player] != smallkey_shuffle.option_universal and \
                    world.smallkey_shuffle[player] != smallkey_shuffle.option_own_dungeons:
                standard_keyshuffle_players.add(player)
            if not world.ganonstower_vanilla[player] or \
                    world.logic[player] in {'owglitches', 'hybridglitches', "nologic"}:
                pass
            elif 'triforcehunt' in world.goal[player] and ('local' in world.goal[player] or world.players == 1):
                trash_counts[player] = world.random.randint(world.crystals_needed_for_gt[player] * 2,
                                                            world.crystals_needed_for_gt[player] * 4)
            else:
                trash_counts[player] = world.random.randint(0, world.crystals_needed_for_gt[player] * 2)

        # Make sure the escape small key is placed first in standard with key shuffle to prevent running out of spots
        # TODO: this might be worthwhile to introduce as generic option for various games and then optimize it
        if standard_keyshuffle_players:
            viable = {}
            for location in world.get_locations():
                if location.player in standard_keyshuffle_players \
                        and location.item is None \
                        and location.can_reach(world.state):
                    viable.setdefault(location.player, []).append(location)

            for player in standard_keyshuffle_players:
                loc = world.random.choice(viable[player])
                key = world.create_item("Small Key (Hyrule Castle)", player)
                loc.place_locked_item(key)
                fill_locations.remove(loc)
            world.random.shuffle(fill_locations)
            # TODO: investigate not creating the key in the first place
            progitempool[:] = [item for item in progitempool if
                               item.player not in standard_keyshuffle_players or
                               item.name != "Small Key (Hyrule Castle)"]

        if trash_counts:
            locations_mapping = {player: [] for player in trash_counts}
            for location in fill_locations:
                if 'Ganons Tower' in location.name and location.player in locations_mapping:
                    locations_mapping[location.player].append(location)

            for player, trash_count in trash_counts.items():
                gtower_locations = locations_mapping[player]
                world.random.shuffle(gtower_locations)
                localrest = localrestitempool[player]
                if localrest:
                    gt_item_pool = restitempool + localrest
                    world.random.shuffle(gt_item_pool)
                else:
                    gt_item_pool = restitempool.copy()

                while gtower_locations and gt_item_pool and trash_count > 0:
                    spot_to_fill = gtower_locations.pop()
                    item_to_place = gt_item_pool.pop()
                    if item_to_place in localrest:
                        localrest.remove(item_to_place)
                    else:
                        restitempool.remove(item_to_place)
                    world.push_item(spot_to_fill, item_to_place, False)
                    fill_locations.remove(spot_to_fill)  # very slow, unfortunately
                    trash_count -= 1

    def get_filler_item_name(self) -> str:
        if self.world.goal[self.player] == "icerodhunt":
            item = "Nothing"
        else:
            item = self.world.random.choice(chain(difficulties[self.world.difficulty[self.player]].extras[0:5]))
        return GetBeemizerItem(self.world, self.player, item)

    def get_pre_fill_items(self):
        res = []
        if self.dungeon_local_item_names:
            for (name, player), dungeon in self.world.dungeons.items():
                if player == self.player:
                    for item in dungeon.all_items:
                        if item.name in self.dungeon_local_item_names:
                            res.append(item)
        return res


def get_same_seed(world, seed_def: tuple) -> str:
    seeds: typing.Dict[tuple, str] = getattr(world, "__named_seeds", {})
    if seed_def in seeds:
        return seeds[seed_def]
    seeds[seed_def] = str(world.random.randint(0, 2 ** 64))
    world.__named_seeds = seeds
    return seeds[seed_def]


class ALttPLogic(LogicMixin):
    def _lttp_has_key(self, item, player, count: int = 1):
        if self.world.logic[player] == 'nologic':
            return True
        if self.world.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
            return self.can_buy_unlimited('Small Key (Universal)', player)
        return self.prog_items[item, player] >= count
