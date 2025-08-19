import logging
import os
import random
import threading
import typing

import settings
from BaseClasses import Item, CollectionState, Tutorial, MultiWorld
from worlds.AutoWorld import World, WebWorld, LogicMixin
from .Client import ALTTPSNIClient
from .Dungeons import create_dungeons, Dungeon
from .EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect
from .InvertedRegions import create_inverted_regions, mark_dark_world_regions
from .ItemPool import generate_itempool, difficulties
from .Items import item_init_table, item_name_groups, item_table, GetBeemizerItem
from .Options import ALTTPOptions, small_key_shuffle
from .Regions import lookup_name_to_id, create_regions, mark_light_world_regions, lookup_vanilla_location_to_entrance, \
    is_main_entrance, key_drop_data
from .Rom import LocalRom, patch_rom, patch_race_rom, check_enemizer, patch_enemizer, apply_rom_settings, \
    get_hash_string, get_base_rom_path, LttPDeltaPatch
from .Rules import set_rules
from .Shops import create_shops, Shop, push_shop_inventories, ShopType, price_rate_display, price_type_display_name
from .StateHelpers import can_buy_unlimited
from .SubClasses import ALttPItem, LTTPRegionType

lttp_logger = logging.getLogger("A Link to the Past")

extras_list = sum(difficulties['normal'].extras[0:5], [])


class ALTTPSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the v1.0 J rom"""
        description = "ALTTP v1.0 J ROM File"
        copy_to = "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc"
        md5s = [LttPDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class ALTTPWeb(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago ALttP Software on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Farrak Kilhn", "Berserker"]
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
        "MSU-1 Setup Guide",
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
        "Plando Guide",
        "A guide to creating Multiworld Plandos with LTTP",
        "English",
        "plando_en.md",
        "plando/en",
        ["Berserker"]
    )

    oof_sound = Tutorial(
        "'OOF' Sound Replacement",
        "A guide to customizing Link's 'oof' sound",
        "English",
        "oof_sound_en.md",
        "oof_sound/en",
        ["Nyx Edelstein"]
    )

    tutorials = [setup_en, setup_de, setup_es, setup_fr, msu, msu_es, msu_fr, plando, oof_sound]
    game_info_languages = ["en", "fr"]


class ALTTPWorld(World):
    """
    The Legend of Zelda: A Link to the Past is an action/adventure game. Take on the role of
    Link, a boy who is destined to save the land of Hyrule. Delve through three palaces and nine
    dungeons on your quest to rescue the descendents of the seven wise men and defeat the evil
    Ganon!
    """
    game = "A Link to the Past"
    options_dataclass = ALTTPOptions
    options: ALTTPOptions
    settings_key = "lttp_options"
    settings: typing.ClassVar[ALTTPSettings]
    topology_present = True
    explicit_indirect_conditions = False
    item_name_groups = item_name_groups
    location_name_groups = {
        "Blind's Hideout": {"Blind's Hideout - Top", "Blind's Hideout - Left", "Blind's Hideout - Right",
                            "Blind's Hideout - Far Left", "Blind's Hideout - Far Right"},
        "Kakariko Well": {"Kakariko Well - Top", "Kakariko Well - Left", "Kakariko Well - Middle",
                          "Kakariko Well - Right", "Kakariko Well - Bottom"},
        "Mini Moldorm Cave": {"Mini Moldorm Cave - Far Left", "Mini Moldorm Cave - Left", "Mini Moldorm Cave - Right",
                              "Mini Moldorm Cave - Far Right", "Mini Moldorm Cave - Generous Guy"},
        "Paradox Cave": {"Paradox Cave Lower - Far Left", "Paradox Cave Lower - Left", "Paradox Cave Lower - Right",
                         "Paradox Cave Lower - Far Right", "Paradox Cave Lower - Middle", "Paradox Cave Upper - Left",
                         "Paradox Cave Upper - Right"},
        "Hype Cave": {"Hype Cave - Top", "Hype Cave - Middle Right", "Hype Cave - Middle Left",
                      "Hype Cave - Bottom", "Hype Cave - Generous Guy"},
        "Hookshot Cave": {"Hookshot Cave - Top Right", "Hookshot Cave - Top Left", "Hookshot Cave - Bottom Right",
                          "Hookshot Cave - Bottom Left"},
        "Hyrule Castle": {"Hyrule Castle - Boomerang Chest", "Hyrule Castle - Map Chest",
                          "Hyrule Castle - Zelda's Chest", "Hyrule Castle - Big Key Drop",
                          "Hyrule Castle - Boomerang Guard Key Drop", "Hyrule Castle - Map Guard Key Drop",
                          "Sewers - Dark Cross", "Sewers - Secret Room - Left",
                          "Sewers - Secret Room - Middle", "Sewers - Secret Room - Right",
                          "Sewers - Key Rat Key Drop"},
        "Eastern Palace": {"Eastern Palace - Compass Chest", "Eastern Palace - Big Chest",
                           "Eastern Palace - Cannonball Chest", "Eastern Palace - Big Key Chest",
                           "Eastern Palace - Dark Eyegore Key Drop", "Eastern Palace - Dark Square Pot Key",
                           "Eastern Palace - Map Chest", "Eastern Palace - Boss"},
        "Desert Palace": {"Desert Palace - Big Chest", "Desert Palace - Torch", "Desert Palace - Map Chest",
                          "Desert Palace - Beamos Hall Pot Key", "Desert Palace - Desert Tiles 1 Pot Key",
                          "Desert Palace - Desert Tiles 2 Pot Key", "Desert Palace - Compass Chest",
                          "Desert Palace - Big Key Chest", "Desert Palace - Boss"},
        "Tower of Hera": {"Tower of Hera - Basement Cage", "Tower of Hera - Map Chest", "Tower of Hera - Big Key Chest",
                          "Tower of Hera - Compass Chest", "Tower of Hera - Big Chest", "Tower of Hera - Boss"},
        "Castle Tower": {"Castle Tower - Room 03", "Castle Tower - Dark Maze",
                         "Castle Tower - Dark Archer Key Drop", "Castle Tower - Circle of Pots Key Drop"},
        "Palace of Darkness": {"Palace of Darkness - Shooter Room", "Palace of Darkness - The Arena - Bridge",
                               "Palace of Darkness - Stalfos Basement", "Palace of Darkness - Big Key Chest",
                               "Palace of Darkness - The Arena - Ledge", "Palace of Darkness - Map Chest",
                               "Palace of Darkness - Compass Chest", "Palace of Darkness - Dark Basement - Left",
                               "Palace of Darkness - Dark Basement - Right", "Palace of Darkness - Dark Maze - Top",
                               "Palace of Darkness - Dark Maze - Bottom", "Palace of Darkness - Big Chest",
                               "Palace of Darkness - Harmless Hellway", "Palace of Darkness - Boss"},
        "Swamp Palace": {"Swamp Palace - Entrance", "Swamp Palace - Map Chest", "Swamp Palace - Big Chest",
                         "Swamp Palace - Compass Chest", "Swamp Palace - Big Key Chest", "Swamp Palace - West Chest",
                         "Swamp Palace - Flooded Room - Left", "Swamp Palace - Flooded Room - Right",
                         "Swamp Palace - Hookshot Pot Key", "Swamp Palace - Pot Row Pot Key",
                         "Swamp Palace - Trench 1 Pot Key", "Swamp Palace - Trench 2 Pot Key",
                         "Swamp Palace - Waterway Pot Key", "Swamp Palace - Waterfall Room", "Swamp Palace - Boss"},
        "Thieves' Town": {"Thieves' Town - Big Key Chest", "Thieves' Town - Map Chest", "Thieves' Town - Compass Chest",
                          "Thieves' Town - Ambush Chest", "Thieves' Town - Attic", "Thieves' Town - Big Chest",
                          "Thieves' Town - Hallway Pot Key", "Thieves' Town - Spike Switch Pot Key",
                          "Thieves' Town - Blind's Cell", "Thieves' Town - Boss"},
        "Skull Woods": {"Skull Woods - Map Chest", "Skull Woods - Pinball Room", "Skull Woods - Compass Chest",
                        "Skull Woods - Pot Prison", "Skull Woods - Big Chest", "Skull Woods - Big Key Chest",
                        "Skull Woods - Spike Corner Key Drop", "Skull Woods - West Lobby Pot Key",
                        "Skull Woods - Bridge Room", "Skull Woods - Boss"},
        "Ice Palace": {"Ice Palace - Compass Chest", "Ice Palace - Freezor Chest", "Ice Palace - Big Chest",
                       "Ice Palace - Freezor Chest", "Ice Palace - Big Chest", "Ice Palace - Iced T Room",
                       "Ice Palace - Spike Room", "Ice Palace - Big Key Chest", "Ice Palace - Map Chest",
                       "Ice Palace - Conveyor Key Drop", "Ice Palace - Hammer Block Key Drop",
                       "Ice Palace - Jelly Key Drop", "Ice Palace - Many Pots Pot Key",
                       "Ice Palace - Boss"},
        "Misery Mire": {"Misery Mire - Big Chest", "Misery Mire - Map Chest", "Misery Mire - Main Lobby",
                        "Misery Mire - Bridge Chest", "Misery Mire - Spike Chest", "Misery Mire - Compass Chest",
                        "Misery Mire - Conveyor Crystal Key Drop", "Misery Mire - Fishbone Pot Key",
                        "Misery Mire - Spikes Pot Key", "Misery Mire - Big Key Chest", "Misery Mire - Boss"},
        "Turtle Rock": {"Turtle Rock - Compass Chest", "Turtle Rock - Roller Room - Left",
                        "Turtle Rock - Roller Room - Right", "Turtle Rock - Chain Chomps", "Turtle Rock - Big Key Chest",
                        "Turtle Rock - Big Chest", "Turtle Rock - Crystaroller Room",
                        "Turtle Rock - Eye Bridge - Bottom Left", "Turtle Rock - Eye Bridge - Bottom Right",
                        "Turtle Rock - Eye Bridge - Top Left", "Turtle Rock - Eye Bridge - Top Right",
                        "Turtle Rock - Pokey 1 Key Drop", "Turtle Rock - Pokey 2 Key Drop",
                        "Turtle Rock - Boss"},
        "Ganons Tower": {"Ganons Tower - Bob's Torch", "Ganons Tower - Hope Room - Left",
                         "Ganons Tower - Hope Room - Right", "Ganons Tower - Tile Room",
                         "Ganons Tower - Compass Room - Top Left", "Ganons Tower - Compass Room - Top Right",
                         "Ganons Tower - Compass Room - Bottom Left", "Ganons Tower - Compass Room - Bottom Right",
                         "Ganons Tower - DMs Room - Top Left", "Ganons Tower - DMs Room - Top Right",
                         "Ganons Tower - DMs Room - Bottom Left", "Ganons Tower - DMs Room - Bottom Right",
                         "Ganons Tower - Map Chest", "Ganons Tower - Firesnake Room",
                         "Ganons Tower - Randomizer Room - Top Left", "Ganons Tower - Randomizer Room - Top Right",
                         "Ganons Tower - Randomizer Room - Bottom Left", "Ganons Tower - Randomizer Room - Bottom Right",
                         "Ganons Tower - Bob's Chest", "Ganons Tower - Big Chest", "Ganons Tower - Big Key Room - Left",
                         "Ganons Tower - Big Key Room - Right", "Ganons Tower - Big Key Chest",
                         "Ganons Tower - Conveyor Cross Pot Key", "Ganons Tower - Conveyor Star Pits Pot Key",
                         "Ganons Tower - Double Switch Pot Key", "Ganons Tower - Mini Helmasaur Room - Left",
                         "Ganons Tower - Mini Helmasaur Room - Right", "Ganons Tower - Pre-Moldorm Chest",
                         "Ganons Tower - Mini Helmasaur Key Drop", "Ganons Tower - Validation Chest"},
        "Ganons Tower Climb": {"Ganons Tower - Mini Helmasaur Room - Left", "Ganons Tower - Mini Helmasaur Room - Right",
                               "Ganons Tower - Mini Helmasaur Key Drop", "Ganons Tower - Pre-Moldorm Chest",
                               "Ganons Tower - Validation Chest"},
    }
    hint_blacklist = {"Triforce"}

    item_name_to_id = {name: data.item_code for name, data in item_table.items() if type(data.item_code) == int}
    location_name_to_id = lookup_name_to_id

    required_client_version = (0, 4, 1)
    web = ALTTPWeb()

    shops: list[Shop]

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

    _enemizer_path: typing.ClassVar[typing.Optional[str]] = None

    @property
    def enemizer_path(self) -> str:
        # TODO: directly use settings
        cls = self.__class__
        if cls._enemizer_path is None:
            cls._enemizer_path = settings.get_settings().generator.enemizer_path
            assert isinstance(cls._enemizer_path, str)
        return cls._enemizer_path

    # custom instance vars
    dungeon_local_item_names: typing.Set[str]
    dungeon_specific_item_names: typing.Set[str]
    rom_name_available_event: threading.Event
    has_progressive_bows: bool
    dungeons: typing.Dict[str, Dungeon]
    waterfall_fairy_bottle_fill: str
    pyramid_fairy_bottle_fill: str
    escape_assist: list

    can_take_damage: bool = True
    swamp_patch_required: bool = False
    powder_patch_required: bool = False
    ganon_at_pyramid: bool = True
    ganonstower_vanilla: bool = True
    fix_fake_world: bool = True

    clock_mode: str = ""
    treasure_hunt_required: int = 0
    treasure_hunt_total: int = 0
    light_world_light_cone: bool = False
    dark_world_light_cone: bool = False
    save_and_quit_from_boss: bool = True
    rupoor_cost: int = 10

    def __init__(self, *args, **kwargs):
        self.dungeon_local_item_names = set()
        self.dungeon_specific_item_names = set()
        self.rom_name_available_event = threading.Event()
        self.pushed_shop_inventories = threading.Event()
        self.has_progressive_bows = False
        self.dungeons = {}
        self.waterfall_fairy_bottle_fill = "Bottle"
        self.pyramid_fairy_bottle_fill = "Bottle"
        self.fix_trock_doors = None
        self.fix_skullwoods_exit = None
        self.fix_palaceofdarkness_exit = None
        self.fix_trock_exit = None
        self.required_medallions = ["Ether", "Quake"]
        self.escape_assist = []
        self.shops = []
        super(ALTTPWorld, self).__init__(*args, **kwargs)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)
        if multiworld.is_race:
            import xxtea  # noqa
        for player in multiworld.get_game_players(cls.game):
            if multiworld.worlds[player].use_enemizer:
                check_enemizer(multiworld.worlds[player].enemizer_path)
                break

    def generate_early(self):
        multiworld = self.multiworld

        self.fix_trock_doors = (self.options.entrance_shuffle != 'vanilla' or self.options.mode == 'inverted')
        self.fix_skullwoods_exit = self.options.entrance_shuffle not in ['vanilla', 'simple', 'restricted', 'dungeons_simple']
        self.fix_palaceofdarkness_exit = self.options.entrance_shuffle not in ['dungeons_simple', 'vanilla', 'simple', 'restricted']
        self.fix_trock_exit = self.options.entrance_shuffle not in ['vanilla', 'simple', 'restricted', 'dungeons_simple']

        # fairy bottle fills
        bottle_options = [
            "Bottle (Red Potion)", "Bottle (Green Potion)", "Bottle (Blue Potion)",
            "Bottle (Bee)", "Bottle (Good Bee)"
        ]
        if self.options.item_pool not in ["hard", "expert"]:
            bottle_options.append("Bottle (Fairy)")
        self.waterfall_fairy_bottle_fill = self.random.choice(bottle_options)
        self.pyramid_fairy_bottle_fill = self.random.choice(bottle_options)

        if self.options.mode == 'standard':
            if self.options.small_key_shuffle:
                if (self.options.small_key_shuffle not in
                        (small_key_shuffle.option_universal, small_key_shuffle.option_own_dungeons,
                         small_key_shuffle.option_start_with)):
                    self.multiworld.local_early_items[self.player]["Small Key (Hyrule Castle)"] = 1
                self.options.local_items.value.add("Small Key (Hyrule Castle)")
                self.options.non_local_items.value.discard("Small Key (Hyrule Castle)")
            if self.options.big_key_shuffle:
                self.options.local_items.value.add("Big Key (Hyrule Castle)")
                self.options.non_local_items.value.discard("Big Key (Hyrule Castle)")

        # system for sharing ER layouts
        self.er_seed = str(multiworld.random.randint(0, 2 ** 64))

        if self.options.entrance_shuffle != "vanilla" and self.options.entrance_shuffle_seed != "random":
            shuffle = self.options.entrance_shuffle.current_key
            if shuffle == "vanilla":
                self.er_seed = "vanilla"
            elif (not self.options.entrance_shuffle_seed.value.isdigit()) or multiworld.is_race:
                self.er_seed = get_same_seed(multiworld, (
                    shuffle, self.options.entrance_shuffle_seed.value,
                    self.options.retro_caves,
                    self.options.mode,
                    self.options.glitches_required
                ))
            else:  # not a race or group seed, use set seed as is.
                self.er_seed = int(self.options.entrance_shuffle_seed.value)
        elif self.options.entrance_shuffle == "vanilla":
            self.er_seed = "vanilla"

        for dungeon_item in ["small_key_shuffle", "big_key_shuffle", "compass_shuffle", "map_shuffle"]:
            option = getattr(self.options, dungeon_item)
            if option == "own_world":
                self.options.local_items.value |= self.item_name_groups[option.item_name_group]
            elif option == "different_world":
                self.options.non_local_items.value |= self.item_name_groups[option.item_name_group]
                if self.options.mode == "standard":
                    self.options.non_local_items.value -= {"Small Key (Hyrule Castle)"}
            elif option.in_dungeon:
                self.dungeon_local_item_names |= self.item_name_groups[option.item_name_group]
                if option == "original_dungeon":
                    self.dungeon_specific_item_names |= self.item_name_groups[option.item_name_group]
                else:
                    self.options.local_items.value |= self.dungeon_local_item_names

        self.difficulty_requirements = difficulties[self.options.item_pool.current_key]

        # enforce pre-defined local items.
        if self.options.goal in ["local_triforce_hunt", "local_ganon_triforce_hunt"]:
            self.options.local_items.value.add('Triforce Piece')

        # Not possible to place crystals outside boss prizes yet (might as well make it consistent with pendants too).
        self.options.non_local_items.value -= item_name_groups['Pendants']
        self.options.non_local_items.value -= item_name_groups['Crystals']

    create_dungeons = create_dungeons

    def create_regions(self):
        player = self.player
        multiworld = self.multiworld

        if self.options.mode != 'inverted':
            create_regions(multiworld, player)
        else:
            create_inverted_regions(multiworld, player)
        create_shops(multiworld, player)
        self.create_dungeons()

        if (self.options.glitches_required not in ["no_glitches", "minor_glitches"] and
                self.options.entrance_shuffle in [
                    "vanilla", "dungeons_simple", "dungeons_full", "simple", "restricted", "full"]):
            self.fix_fake_world = False

        # seeded entrance shuffle
        old_random = multiworld.random
        multiworld.random = random.Random(self.er_seed)

        if self.options.mode != 'inverted':
            link_entrances(multiworld, player)
            mark_light_world_regions(multiworld, player)
        else:
            link_inverted_entrances(multiworld, player)
            mark_dark_world_regions(multiworld, player)

        multiworld.random = old_random
        plando_connect(multiworld, player)

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
                    elif (state.has('Tempered Sword', item.player) and
                          self.difficulty_requirements.progressive_sword_limit >= 4):
                        return 'Golden Sword'
                    elif (state.has('Master Sword', item.player) and
                          self.difficulty_requirements.progressive_sword_limit >= 3):
                        return 'Tempered Sword'
                    elif (state.has('Fighter Sword', item.player) and
                          self.difficulty_requirements.progressive_sword_limit >= 2):
                        return 'Master Sword'
                    elif self.difficulty_requirements.progressive_sword_limit >= 1:
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
                    elif (state.has('Red Shield', item.player) and
                          self.difficulty_requirements.progressive_shield_limit >= 3):
                        return 'Mirror Shield'
                    elif (state.has('Blue Shield', item.player) and
                          self.difficulty_requirements.progressive_shield_limit >= 2):
                        return 'Red Shield'
                    elif self.difficulty_requirements.progressive_shield_limit >= 1:
                        return 'Blue Shield'
                elif 'Bow' in item_name:
                    if state.has('Silver Bow', item.player):
                        return
                    elif state.has('Bow', item.player) and (self.difficulty_requirements.progressive_bow_limit >= 2
                                                            or self.options.glitches_required == 'no_glitches'
                                                            or self.options.swordless):
                        # modes where silver bow is always required for ganon
                        return 'Silver Bow'
                    elif self.difficulty_requirements.progressive_bow_limit >= 1:
                        return 'Bow'
        elif item.advancement:
            return item_name

    def pre_fill(self):
        from Fill import fill_restrictive, FillError
        attempts = 5
        all_state = self.multiworld.get_all_state(perform_sweep=False)
        crystals = [self.create_item(name) for name in ['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6']]
        for crystal in crystals:
            all_state.remove(crystal)
        all_state.sweep_for_advancements()
        crystal_locations = [self.get_location('Turtle Rock - Prize'),
                             self.get_location('Eastern Palace - Prize'),
                             self.get_location('Desert Palace - Prize'),
                             self.get_location('Tower of Hera - Prize'),
                             self.get_location('Palace of Darkness - Prize'),
                             self.get_location('Thieves\' Town - Prize'),
                             self.get_location('Skull Woods - Prize'),
                             self.get_location('Swamp Palace - Prize'),
                             self.get_location('Ice Palace - Prize'),
                             self.get_location('Misery Mire - Prize')]
        placed_prizes = {loc.item.name for loc in crystal_locations if loc.item}
        unplaced_prizes = [crystal for crystal in crystals if crystal.name not in placed_prizes]
        empty_crystal_locations = [loc for loc in crystal_locations if not loc.item]
        for attempt in range(attempts):
            try:
                prizepool = unplaced_prizes.copy()
                prize_locs = empty_crystal_locations.copy()
                self.multiworld.random.shuffle(prize_locs)
                fill_restrictive(self.multiworld, all_state, prize_locs, prizepool, True, lock=True,
                                 name="LttP Dungeon Prizes")
            except FillError as e:
                lttp_logger.exception("Failed to place dungeon prizes (%s). Will retry %s more times", e,
                                                attempts - attempt)
                for location in empty_crystal_locations:
                    location.item = None
                continue
            break
        else:
            raise FillError('Unable to place dungeon prizes')
        if self.options.mode == 'standard' and self.options.small_key_shuffle \
                and self.options.small_key_shuffle != small_key_shuffle.option_universal and \
                self.options.small_key_shuffle != small_key_shuffle.option_own_dungeons:
            self.multiworld.local_early_items[self.player]["Small Key (Hyrule Castle)"] = 1

    @classmethod
    def stage_pre_fill(cls, world):
        from .Dungeons import fill_dungeons_restrictive
        fill_dungeons_restrictive(world)

    @classmethod
    def stage_generate_output(cls, multiworld, output_directory):
        push_shop_inventories(multiworld)

    @property
    def use_enemizer(self) -> bool:
        return bool(self.options.boss_shuffle or self.options.enemy_shuffle
                    or self.options.enemy_health != 'default' or self.options.enemy_damage != 'default'
                    or self.options.pot_shuffle or self.options.bush_shuffle
                    or self.options.killable_thieves)

    def generate_output(self, output_directory: str):
        multiworld = self.multiworld
        player = self.player

        self.pushed_shop_inventories.wait()

        try:
            use_enemizer = self.use_enemizer

            rom = LocalRom(get_base_rom_path())

            patch_rom(multiworld, rom, player, use_enemizer)

            if use_enemizer:
                patch_enemizer(self, rom, self.enemizer_path, output_directory)

            if multiworld.is_race:
                patch_race_rom(rom, multiworld, player)

            multiworld.spoiler.hashes[player] = get_hash_string(rom.hash)

            palettes_options = {
                'dungeon': self.options.uw_palettes,
                'overworld': self.options.ow_palettes,
                'hud': self.options.hud_palettes,
                'sword': self.options.sword_palettes,
                'shield': self.options.shield_palettes,
                # 'link': world.link_palettes[player]
            }
            palettes_options = {key: option.current_key for key, option in palettes_options.items()}

            apply_rom_settings(rom, self.options.heartbeep.current_key,
                               self.options.heartcolor.current_key,
                               self.options.quickswap,
                               self.options.menuspeed.current_key,
                               self.options.music,
                               multiworld.sprite[player],
                               None,
                               palettes_options, multiworld, player, True,
                               reduceflashing=self.options.reduceflashing or multiworld.is_race,
                               triforcehud=self.options.triforcehud.current_key,
                               deathlink=self.options.death_link,
                               allowcollect=self.options.allow_collect)

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            patch = LttPDeltaPatch(os.path.splitext(rompath)[0]+LttPDeltaPatch.patch_file_ending, player=player,
                                   player_name=multiworld.player_name[player], patched_path=rompath)
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
                        world.worlds[player].options.entrance_shuffle != "vanilla" or world.worlds[player].options.retro_caves}

        for region in world.regions:
            if region.player in er_hint_data and region.locations:
                main_entrance = region.get_connecting_entrance(is_main_entrance)
                for location in region.locations:
                    if type(location.address) == int:  # skips events and crystals
                        if lookup_vanilla_location_to_entrance[location.address] != main_entrance.name:
                            er_hint_data[region.player][location.address] = main_entrance.name
        hint_data.update(er_hint_data)

    @classmethod
    def stage_modify_multidata(cls, multiworld, multidata: dict):

        ordered_areas = (
            'Light World', 'Dark World', 'Hyrule Castle', 'Agahnims Tower', 'Eastern Palace', 'Desert Palace',
            'Tower of Hera', 'Palace of Darkness', 'Swamp Palace', 'Skull Woods', 'Thieves Town', 'Ice Palace',
            'Misery Mire', 'Turtle Rock', 'Ganons Tower', "Total"
        )

        checks_in_area = {player: {area: list() for area in ordered_areas}
                          for player in multiworld.get_game_players(cls.game)}

        for player in checks_in_area:
            checks_in_area[player]["Total"] = 0
            for location in multiworld.get_locations(player):
                if location.game == cls.game and type(location.address) is int:
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
                    else:
                        assert False, "Unknown Location area."
                    # TODO: remove Total as it's duplicated data and breaks consistent typing
                    checks_in_area[location.player]["Total"] += 1

        multidata["checks_in_area"].update(checks_in_area)

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
    def stage_fill_hook(cls, multiworld, progitempool, usefulitempool, filleritempool, fill_locations):
        trash_counts = {}
        for player in multiworld.get_game_players("A Link to the Past"):
            world = multiworld.worlds[player]
            if not world.ganonstower_vanilla or \
                    world.options.glitches_required.current_key in {'overworld_glitches', 'hybrid_major_glitches', "no_logic"}:
                pass
            elif 'triforce_hunt' in world.options.goal.current_key and ('local' in world.options.goal.current_key or multiworld.players == 1):
                trash_counts[player] = multiworld.random.randint(world.options.crystals_needed_for_gt * 2,
                                                            world.options.crystals_needed_for_gt * 4)
            else:
                trash_counts[player] = multiworld.random.randint(0, world.options.crystals_needed_for_gt * 2)

        if trash_counts:
            locations_mapping = {player: [] for player in trash_counts}
            for location in fill_locations:
                if 'Ganons Tower' in location.name and location.player in locations_mapping:
                    locations_mapping[location.player].append(location)

            for player, trash_count in trash_counts.items():
                gtower_locations = locations_mapping[player]
                multiworld.random.shuffle(gtower_locations)

                while gtower_locations and filleritempool and trash_count > 0:
                    spot_to_fill = gtower_locations.pop()
                    for index, item in enumerate(filleritempool):
                        if spot_to_fill.item_rule(item):
                            filleritempool.pop(index)  # remove from outer fill
                            multiworld.push_item(spot_to_fill, item, False)
                            fill_locations.remove(spot_to_fill)  # very slow, unfortunately
                            trash_count -= 1
                            break
                    else:
                        logging.warning(f"Could not trash fill Ganon's Tower for player {player}.")

    def write_spoiler_header(self, spoiler_handle: typing.TextIO) -> None:
        def bool_to_text(variable: typing.Union[bool, str]) -> str:
            if type(variable) == str:
                return variable
            return "Yes" if variable else "No"

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        player_name = self.multiworld.get_player_name(self.player)
        spoiler_handle.write("\n\nMedallions:\n")
        spoiler_handle.write(f"\nMisery Mire ({player_name}):"
                             f" {self.required_medallions[0]}")
        spoiler_handle.write(
            f"\nTurtle Rock ({player_name}):"
            f" {self.required_medallions[1]}")
        spoiler_handle.write("\n\nFairy Fountain Bottle Fill:\n")
        spoiler_handle.write(f"\nPyramid Fairy ({player_name}):"
                             f" {self.pyramid_fairy_bottle_fill}")
        spoiler_handle.write(f"\nWaterfall Fairy ({player_name}):"
                             f" {self.waterfall_fairy_bottle_fill}")
        if self.options.boss_shuffle != "none":
            def create_boss_map() -> typing.Dict:
                boss_map = {
                    "Eastern Palace": self.dungeons["Eastern Palace"].boss.name,
                    "Desert Palace": self.dungeons["Desert Palace"].boss.name,
                    "Tower Of Hera": self.dungeons["Tower of Hera"].boss.name,
                    "Hyrule Castle": "Agahnim",
                    "Palace Of Darkness": self.dungeons["Palace of Darkness"].boss.name,
                    "Swamp Palace": self.dungeons["Swamp Palace"].boss.name,
                    "Skull Woods": self.dungeons["Skull Woods"].boss.name,
                    "Thieves Town": self.dungeons["Thieves Town"].boss.name,
                    "Ice Palace": self.dungeons["Ice Palace"].boss.name,
                    "Misery Mire": self.dungeons["Misery Mire"].boss.name,
                    "Turtle Rock": self.dungeons["Turtle Rock"].boss.name,
                    "Ganons Tower": "Agahnim 2",
                    "Ganon": "Ganon"
                }
                if self.options.mode != 'inverted':
                    boss_map.update({
                        "Ganons Tower Basement":
                            self.dungeons["Ganons Tower"].bosses["bottom"].name,
                        "Ganons Tower Middle": self.dungeons["Ganons Tower"].bosses[
                            "middle"].name,
                        "Ganons Tower Top": self.dungeons["Ganons Tower"].bosses[
                            "top"].name
                    })
                else:
                    boss_map.update({
                        "Ganons Tower Basement": self.dungeons["Inverted Ganons Tower"].bosses["bottom"].name,
                        "Ganons Tower Middle": self.dungeons["Inverted Ganons Tower"].bosses["middle"].name,
                        "Ganons Tower Top": self.dungeons["Inverted Ganons Tower"].bosses["top"].name
                    })
                return boss_map

            bossmap = create_boss_map()
            spoiler_handle.write(
                f'\n\nBosses{(f" ({self.multiworld.get_player_name(self.player)})" if self.multiworld.players > 1 else "")}:\n')
            spoiler_handle.write('    ' + '\n    '.join([f'{x}: {y}' for x, y in bossmap.items()]))

        def build_shop_info(shop: Shop) -> typing.Dict[str, str]:
            shop_data = {
                "location": str(shop.region),
                "type": "Take Any" if shop.type == ShopType.TakeAny else "Shop"
            }

            for index, item in enumerate(shop.inventory):
                if item is None:
                    continue
                price = item["price"] // price_rate_display.get(item["price_type"], 1)
                shop_data["item_{}".format(index)] = f"{item['item']} - {price} {price_type_display_name[item['price_type']]}"
                if item["player"]:
                    shop_data["item_{}".format(index)] =\
                        shop_data["item_{}".format(index)].replace("—", "(Player {}) — ".format(item["player"]))

                if item["max"] == 0:
                    continue
                shop_data["item_{}".format(index)] += " x {}".format(item["max"])
                if item["replacement"] is None:
                    continue
                shop_data["item_{}".format(index)] +=\
                    f", {item['replacement']} - {item['replacement_price'] // price_rate_display.get(item['replacement_price_type'], 1)}" \
                    f" {price_type_display_name[item['replacement_price_type']]}"

            return shop_data

        if shop_info := [build_shop_info(shop) for shop in self.shops if shop.custom]:
            spoiler_handle.write('\n\nShops:\n\n')
        for shop_data in shop_info:
            spoiler_handle.write("{} [{}]\n    {}\n".format(shop_data['location'], shop_data['type'], "\n    ".join(
                item for item in [shop_data.get('item_0', None), shop_data.get('item_1', None), shop_data.get('item_2', None)] if
                item)))

    def get_filler_item_name(self) -> str:
        item = self.multiworld.random.choice(extras_list)
        return GetBeemizerItem(self.multiworld, self.player, item)

    def get_pre_fill_items(self):
        res = [self.create_item(name) for name in ('Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1',
                                                   'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5',
                                                   'Crystal 6')]
        if self.dungeon_local_item_names:
            for dungeon in self.dungeons.values():
                for item in dungeon.all_items:
                    if item.name in self.dungeon_local_item_names:
                        res.append(item)

        return res

    def fill_slot_data(self):
        slot_data = {}
        if not self.multiworld.is_race:
            # all of these option are NOT used by the SNI- or Text-Client.
            # they are used by the alttp-poptracker pack (https://github.com/StripesOO7/alttp-ap-poptracker-pack)
            # for convenient auto-tracking of the generated settings and adjusting the tracker accordingly

            slot_options = ["crystals_needed_for_gt", "crystals_needed_for_ganon", "open_pyramid",
                            "big_key_shuffle", "small_key_shuffle", "compass_shuffle", "map_shuffle",
                            "progressive", "swordless", "retro_bow", "retro_caves", "shop_item_slots",
                            "boss_shuffle", "pot_shuffle", "enemy_shuffle", "key_drop_shuffle", "bombless_start",
                            "randomize_shop_inventories", "shuffle_shop_inventories", "shuffle_capacity_upgrades",
                            "entrance_shuffle", "dark_room_logic", "goal", "mode",
                            "triforce_pieces_mode", "triforce_pieces_percentage", "triforce_pieces_required",
                            "triforce_pieces_available", "triforce_pieces_extra",
            ]

            slot_data = {option_name: getattr(self.options, option_name).value for option_name in slot_options}

            slot_data.update({
                'mm_medalion': self.required_medallions[0],
                'tr_medalion': self.required_medallions[1],
                }
            )
        return slot_data


def get_same_seed(world, seed_def: tuple) -> str:
    seeds: typing.Dict[tuple, str] = getattr(world, "__named_seeds", {})
    if seed_def in seeds:
        return seeds[seed_def]
    seeds[seed_def] = str(world.random.randint(0, 2 ** 64))
    world.__named_seeds = seeds
    return seeds[seed_def]


class ALttPLogic(LogicMixin):
    def _lttp_has_key(self, item, player, count: int = 1):
        if self.multiworld.worlds[player].options.glitches_required == 'no_logic':
            return True
        if self.multiworld.worlds[player].options.small_key_shuffle == small_key_shuffle.option_universal:
            return can_buy_unlimited(self, 'Small Key (Universal)', player)
        return self.prog_items[player][item] >= count
