import logging
import os
import random
import threading
import typing

import Utils
from BaseClasses import Item, CollectionState, Tutorial, MultiWorld
from .Dungeons import create_dungeons
from .EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect, \
    indirect_connections, indirect_connections_inverted, indirect_connections_not_inverted
from .InvertedRegions import create_inverted_regions, mark_dark_world_regions
from .ItemPool import generate_itempool, difficulties
from .Items import item_init_table, item_name_groups, item_table, GetBeemizerItem
from .Options import alttp_options, smallkey_shuffle
from .Regions import lookup_name_to_id, create_regions, mark_light_world_regions, lookup_vanilla_location_to_entrance, \
    is_main_entrance
from .Client import ALTTPSNIClient
from .Rom import LocalRom, patch_rom, patch_race_rom, check_enemizer, patch_enemizer, apply_rom_settings, \
    get_hash_string, get_base_rom_path, LttPDeltaPatch
from .Rules import set_rules
from .Shops import create_shops, ShopSlotFill
from .SubClasses import ALttPItem
from worlds.AutoWorld import World, WebWorld, LogicMixin

lttp_logger = logging.getLogger("A Link to the Past")

extras_list = sum(difficulties['normal'].extras[0:5], [])


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
        "msu1/es",
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
    option_definitions = alttp_options
    topology_present = True
    item_name_groups = item_name_groups
    hint_blacklist = {"Triforce"}

    item_name_to_id = {name: data.item_code for name, data in item_table.items() if type(data.item_code) == int}
    location_name_to_id = lookup_name_to_id

    data_version = 8
    required_client_version = (0, 3, 2)
    web = ALTTPWeb()

    pedestal_credit_texts: typing.Dict[int, str] = \
        {data.item_code: data.pedestal_credit for data in item_table.values() if data.pedestal_credit}
    sickkid_credit_texts: typing.Dict[int, str] = \
        {data.item_code: data.sick_kid_credit for data in item_table.values() if data.sick_kid_credit}
    zora_credit_texts: typing.Dict[int, str] = \
        {data.item_code: data.zora_credit for data in item_table.values() if data.zora_credit}
    magicshop_credit_texts: typing.Dict[int, str] = \
        {data.item_code: data.witch_credit for data in item_table.values() if data.witch_credit}
    fluteboy_credit_texts: typing.Dict[int, str] = \
        {data.item_code: data.flute_boy_credit for data in item_table.values() if data.flute_boy_credit}

    set_rules = set_rules

    create_items = generate_itempool

    enemizer_path: str = Utils.get_options()["generator"]["enemizer_path"] \
        if os.path.isabs(Utils.get_options()["generator"]["enemizer_path"]) \
        else Utils.local_path(Utils.get_options()["generator"]["enemizer_path"])

    def __init__(self, *args, **kwargs):
        self.dungeon_local_item_names = set()
        self.dungeon_specific_item_names = set()
        self.rom_name_available_event = threading.Event()
        self.has_progressive_bows = False
        super(ALTTPWorld, self).__init__(*args, **kwargs)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)
        if multiworld.is_race:
            import xxtea
        for player in multiworld.get_game_players(cls.game):
            if multiworld.worlds[player].use_enemizer:
                check_enemizer(multiworld.worlds[player].enemizer_path)
                break

    def generate_early(self):

        player = self.player
        world = self.multiworld

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

        # enforce pre-defined local items.
        if world.goal[player] in ["localtriforcehunt", "localganontriforcehunt"]:
            world.local_items[player].value.add('Triforce Piece')

        # Not possible to place crystals outside boss prizes yet (might as well make it consistent with pendants too).
        world.non_local_items[player].value -= item_name_groups['Pendants']
        world.non_local_items[player].value -= item_name_groups['Crystals']

    def create_regions(self):
        player = self.player
        world = self.multiworld

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
            for region_name, entrance_name in indirect_connections_not_inverted.items():
                world.register_indirect_condition(world.get_region(region_name, player),
                                                  world.get_entrance(entrance_name, player))
        else:
            link_inverted_entrances(world, player)
            mark_dark_world_regions(world, player)
            for region_name, entrance_name in indirect_connections_inverted.items():
                world.register_indirect_condition(world.get_region(region_name, player),
                                                  world.get_entrance(entrance_name, player))

        world.random = old_random
        plando_connect(world, player)

        for region_name, entrance_name in indirect_connections.items():
            world.register_indirect_condition(world.get_region(region_name, player),
                                              world.get_entrance(entrance_name, player))


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
                    elif state.has('Tempered Sword', item.player) and self.multiworld.difficulty_requirements[
                        item.player].progressive_sword_limit >= 4:
                        return 'Golden Sword'
                    elif state.has('Master Sword', item.player) and self.multiworld.difficulty_requirements[
                        item.player].progressive_sword_limit >= 3:
                        return 'Tempered Sword'
                    elif state.has('Fighter Sword', item.player) and self.multiworld.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                        return 'Master Sword'
                    elif self.multiworld.difficulty_requirements[item.player].progressive_sword_limit >= 1:
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
                    elif state.has('Red Shield', item.player) and self.multiworld.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                        return 'Mirror Shield'
                    elif state.has('Blue Shield', item.player) and self.multiworld.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                        return 'Red Shield'
                    elif self.multiworld.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                        return 'Blue Shield'
                elif 'Bow' in item_name:
                    if state.has('Silver Bow', item.player):
                        return
                    elif state.has('Bow', item.player) and (self.multiworld.difficulty_requirements[item.player].progressive_bow_limit >= 2
                                                            or self.multiworld.logic[item.player] == 'noglitches'
                                                            or self.multiworld.swordless[item.player]): # modes where silver bow is always required for ganon
                        return 'Silver Bow'
                    elif self.multiworld.difficulty_requirements[item.player].progressive_bow_limit >= 1:
                        return 'Bow'
        elif item.advancement:
            return item_name

    def pre_fill(self):
        from Fill import fill_restrictive, FillError
        attempts = 5
        world = self.multiworld
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

    @property
    def use_enemizer(self) -> bool:
        world = self.multiworld
        player = self.player
        return bool(world.boss_shuffle[player] or world.enemy_shuffle[player]
                    or world.enemy_health[player] != 'default' or world.enemy_damage[player] != 'default'
                    or world.pot_shuffle[player] or world.bush_shuffle[player]
                    or world.killable_thieves[player])

    def generate_output(self, output_directory: str):
        world = self.multiworld
        player = self.player
        try:
            use_enemizer = self.use_enemizer

            rom = LocalRom(get_base_rom_path())

            patch_rom(world, rom, player, use_enemizer)

            if use_enemizer:
                patch_enemizer(world, player, rom, self.enemizer_path, output_directory)

            if world.is_race:
                patch_race_rom(rom, world, player)

            world.spoiler.hashes[player] = get_hash_string(rom.hash)

            palettes_options = {
                'dungeon': world.uw_palettes[player],
                'overworld': world.ow_palettes[player],
                'hud': world.hud_palettes[player],
                'sword': world.sword_palettes[player],
                'shield': world.shield_palettes[player],
                # 'link': world.link_palettes[player]
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

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
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

    @classmethod
    def stage_extend_hint_information(cls, world, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        er_hint_data = {player: {} for player in world.get_game_players("A Link to the Past") if
                        world.shuffle[player] != "vanilla" or world.retro_caves[player]}

        for region in world.regions:
            if region.player in er_hint_data and region.locations:
                main_entrance = region.get_connecting_entrance(is_main_entrance)
                for location in region.locations:
                    if type(location.address) == int:  # skips events and crystals
                        if lookup_vanilla_location_to_entrance[location.address] != main_entrance.name:
                            er_hint_data[region.player][location.address] = main_entrance.name
        hint_data.update(er_hint_data)

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def create_item(self, name: str) -> Item:
        return ALttPItem(name, self.player, **item_init_table[name])

    @classmethod
    def stage_fill_hook(cls, world, progitempool, usefulitempool, filleritempool, fill_locations):
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

                while gtower_locations and filleritempool and trash_count > 0:
                    spot_to_fill = gtower_locations.pop()
                    for index, item in enumerate(filleritempool):
                        if spot_to_fill.item_rule(item):
                            filleritempool.pop(index)  # remove from outer fill
                            world.push_item(spot_to_fill, item, False)
                            fill_locations.remove(spot_to_fill)  # very slow, unfortunately
                            trash_count -= 1
                            break
                    else:
                        logging.warning(f"Could not trash fill Ganon's Tower for player {player}.")

    def get_filler_item_name(self) -> str:
        if self.multiworld.goal[self.player] == "icerodhunt":
            item = "Nothing"
        else:
            item = self.multiworld.random.choice(extras_list)
        return GetBeemizerItem(self.multiworld, self.player, item)

    def get_pre_fill_items(self):
        res = []
        if self.dungeon_local_item_names:
            for (name, player), dungeon in self.multiworld.dungeons.items():
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
        if self.multiworld.logic[player] == 'nologic':
            return True
        if self.multiworld.smallkey_shuffle[player] == smallkey_shuffle.option_universal:
            return self.can_buy_unlimited('Small Key (Universal)', player)
        return self.prog_items[item, player] >= count
