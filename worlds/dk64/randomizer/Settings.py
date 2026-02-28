"""Settings class and functions."""

import json
import logging
import math
import random
import os
from version import version
from copy import deepcopy

from randomizer.Enums.Transitions import Transitions
import randomizer.ItemPool as ItemPool
import randomizer.Lists.Exceptions as Ex
import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.JungleJapes
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import GetKongs, Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Models import Model, Sprite
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import *
from randomizer.Enums.SongType import SongType
from randomizer.Enums.Types import Types, BarrierItems
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import (
    ChunkyMoveLocations,
    DiddyMoveLocations,
    DonkeyMoveLocations,
    LankyMoveLocations,
    PreGivenLocations,
    ProgressiveHintLocations,
    SharedShopLocations,
    ShopLocationReference,
    TinyMoveLocations,
    TrainingBarrelLocations,
    WrinklyHintLocations,
)
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId, RegionMapList
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Lists.Songs import song_data
from randomizer.Lists.Switches import SwitchData
from randomizer.Patching.Library.Generic import IsItemSelected, HelmDoorInfo, HelmDoorRandomInfo, DoorItemToBarrierItem, getCompletableBonuses, IsDDMSSelected, MEDAL_PROGRESSIVE_RATIOS
from randomizer.Patching.CoinPlacer import gen_mayhem_coins
from randomizer.Prices import CompleteVanillaPrices, RandomizePrices, VanillaPrices
from randomizer.SettingStrings import encrypt_settings_string_enum
from randomizer.ShuffleBosses import (
    BossMapList,
    KRoolMaps,
    ShuffleBosses,
    ShuffleBossKongs,
    ShuffleKKOPhaseOrder,
    ShuffleKutoutKongs,
    ShuffleTinyPhaseToes,
)
from version import version as randomizer_version


class Settings:
    """Class used to store settings for seed generation."""

    def __init__(self, form_data: dict, random=random):
        """Init all the settings using the form data to set the flags.

        Args:
            form_data (dict): Post data from the html form.
        """
        self.__hash = randomizer_version
        self.public_hash = randomizer_version
        self.algorithm = FillAlgorithm.forward
        self.generate_main()
        self.generate_progression()
        self.generate_misc()
        self.rom_data = 0x1FED020
        self.move_location_data = 0x1FEF000
        self.form_data = form_data

        # Debugging
        self.version = version
        self.branch = os.environ.get("BRANCH", "LOCAL")

        self.apply_form_data(form_data)
        self.seed_id = str(self.seed)
        if self.generate_spoilerlog is None:
            self.generate_spoilerlog = False
        self.random = random
        self.seed = str(self.seed) + self.__hash + str(json.dumps(form_data))
        if not self.archipelago:
            self.set_seed()
        self.seed_hash = [self.random.randint(0, 9) for i in range(5)]
        self.krool_keys_required = []
        self.starting_key_list = []
        # Settings which are not yet implemented on the web page
        # B Locker and T&S max values
        # Shorter: 20 GB
        # Short: 35 GB
        # Medium: 50 GB
        # Long: 65 GB
        # Longer: 80 GB
        if self.blocker_text is not None and self.blocker_text != "":
            self.blocker_max = int(self.blocker_text)
        else:
            self.blocker_max = 50
        if self.troff_text is not None and self.troff_text != "":
            self.troff_max = int(self.troff_text)
        else:
            self.troff_max = 270
        self.troff_min = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.60]  # Weights for the minimum value of troff
        if self.tns_selection_behavior == TroffSetting.normal_random:
            self.troff_min = [0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]  # Add 20% to the minimum for hard T&S
        # In hard level progression we go through levels in a random order, so we set every level's troff min weight to the largest weight
        if self.level_randomization == LevelRandomization.level_order_complex:
            self.troff_min = [self.troff_min[-1] for x in self.troff_min]

        CompleteVanillaPrices()
        self.prices = VanillaPrices.copy()
        self.original_prices = self.prices.copy()
        self.level_order = {
            1: Levels.JungleJapes,
            2: Levels.AngryAztec,
            3: Levels.FranticFactory,
            4: Levels.GloomyGalleon,
            5: Levels.FungiForest,
            6: Levels.CrystalCaves,
            7: Levels.CreepyCastle,
            8: Levels.HideoutHelm,
        }

        # Used by hints in level order rando
        # By default (and in LZR) assume you have access to everything everywhere so hints are unrestricted
        self.owned_kongs_by_level = {
            Levels.JungleJapes: GetKongs().copy(),
            Levels.AngryAztec: GetKongs().copy(),
            Levels.FranticFactory: GetKongs().copy(),
            Levels.GloomyGalleon: GetKongs().copy(),
            Levels.FungiForest: GetKongs().copy(),
            Levels.CrystalCaves: GetKongs().copy(),
            Levels.CreepyCastle: GetKongs().copy(),
        }
        self.owned_moves_by_level = {
            Levels.JungleJapes: ItemPool.AllKongMoves().copy(),
            Levels.AngryAztec: ItemPool.AllKongMoves().copy(),
            Levels.FranticFactory: ItemPool.AllKongMoves().copy(),
            Levels.GloomyGalleon: ItemPool.AllKongMoves().copy(),
            Levels.FungiForest: ItemPool.AllKongMoves().copy(),
            Levels.CrystalCaves: ItemPool.AllKongMoves().copy(),
            Levels.CreepyCastle: ItemPool.AllKongMoves().copy(),
        }

        self.item_check_counts = {
            # Item, Checks
            ItemRandoListSelected.shop: [0, 100],
            ItemRandoListSelected.moves: [36, 0],
            ItemRandoListSelected.shockwave: [2, 0],
            ItemRandoListSelected.bfi_gift: [0, 1],
            ItemRandoListSelected.banana: [161, 0],
            ItemRandoListSelected.banana_checks: [0, 134],
            ItemRandoListSelected.racebanana: [0, 11],
            ItemRandoListSelected.gauntletbanana: [0, 16],
            ItemRandoListSelected.blueprintbanana: [40, 0],
            ItemRandoListSelected.sniderewards: [0, 40],
            ItemRandoListSelected.arenas: [0, 10],
            ItemRandoListSelected.crown: [10, 0],
            ItemRandoListSelected.blueprint: [40, 0],
            ItemRandoListSelected.kasplat: [0, 40],
            ItemRandoListSelected.key: [8, 0],
            ItemRandoListSelected.bosses: [0, 7],
            ItemRandoListSelected.endofhelm: [0, 1],
            ItemRandoListSelected.medal: [40, 0],
            ItemRandoListSelected.medal_checks: [0, 35],
            ItemRandoListSelected.medal_checks_helm: [0, 5],
            ItemRandoListSelected.nintendocoin: [1, 0],
            ItemRandoListSelected.arcade: [0, 1],
            ItemRandoListSelected.rarewarecoin: [1, 0],
            ItemRandoListSelected.jetpac: [0, 1],
            ItemRandoListSelected.kong: [4, 0],
            ItemRandoListSelected.kong_cages: [0, 4],
            ItemRandoListSelected.fairy: [20, 0],
            ItemRandoListSelected.fairy_checks: [0, 20],
            ItemRandoListSelected.rainbowcoin: [16, 0],
            ItemRandoListSelected.dirt_patches: [0, 16],
            ItemRandoListSelected.pearl: [5, 0],
            ItemRandoListSelected.clams: [0, 5],
            ItemRandoListSelected.bean: [1, 0],
            ItemRandoListSelected.anthillreward: [0, 1],
            ItemRandoListSelected.crateitem: [0, 13],
            ItemRandoListSelected.halfmedal: [0, 40],
            ItemRandoListSelected.shopowners: [0, 0],  # Max is 4, calculated during post-processing
            ItemRandoListSelected.hint: [35, 0],
            ItemRandoListSelected.wrinkly: [0, 35],
            ItemRandoListSelected.boulderitem: [0, 16],
            ItemRandoListSelected.enemies: [0, 289],
            ItemRandoListSelected.trainingmoves: [4, 0],
            ItemRandoListSelected.trainingbarrels: [0, 4],
        }
        self.pool_index_with_shops = None

        if self.enable_plandomizer:
            self.ApplyPlandomizerSettings()

            # Remove these as plando features get implemented
            self.plandomizer_dict["plando_shop_location_rando"] = -1
            # ---------------------------------------------------
            # Prevent custom locations selected for plandomizer from being used by a different randomizer
            self.plandomizer_dict["reserved_custom_locations"] = {
                Levels.DKIsles: [],
                Levels.JungleJapes: [],
                Levels.AngryAztec: [],
                Levels.FranticFactory: [],
                Levels.GloomyGalleon: [],
                Levels.FungiForest: [],
                Levels.CrystalCaves: [],
                Levels.CreepyCastle: [],
                Levels.HideoutHelm: [],
            }
            crown_to_level = {
                Locations.JapesBattleArena: Levels.JungleJapes,
                Locations.AztecBattleArena: Levels.AngryAztec,
                Locations.FactoryBattleArena: Levels.FranticFactory,
                Locations.GalleonBattleArena: Levels.GloomyGalleon,
                Locations.ForestBattleArena: Levels.FungiForest,
                Locations.CavesBattleArena: Levels.CrystalCaves,
                Locations.CastleBattleArena: Levels.CreepyCastle,
                Locations.IslesBattleArena2: Levels.DKIsles,
                Locations.IslesBattleArena1: Levels.DKIsles,
                Locations.HelmBattleArena: Levels.HideoutHelm,
            }
            for key in ["plando_dirt_patches", "plando_melon_crates", "plando_battle_arenas"]:
                for customloc in self.plandomizer_dict[key]:
                    selected_location = ""
                    level = -1
                    if key == "plando_battle_arenas":
                        selected_location = self.plandomizer_dict[key][customloc]
                        level = crown_to_level[int(customloc)]
                    else:
                        selected_location = customloc["location"]
                        level = customloc["level"]
                    if level != -1:
                        self.plandomizer_dict["reserved_custom_locations"][level].append(selected_location)
        if self.music_selections is not None:
            self.ApplyMusicSelections()

        self.resolve_settings()

        # Generate the settings string - DO THIS LAST because the encryption method alters the form data
        try:
            logger = logging.getLogger(__name__)
            self.settings_string = encrypt_settings_string_enum(form_data)
            # logger.warning("Using settings string: " + self.settings_string)
        except Exception as ex:
            raise Ex.SettingsIncompatibleException("Settings string is in an invalid state. Try applying a preset and recreating your changes.")

    def apply_form_data(self, form_data):
        """Convert and apply the provided form data to this class."""

        def get_enum_value(keyString, valueString):
            """Take in a key and value, and return an enum."""
            try:
                return SettingsMap[keyString](valueString)
            except ValueError:
                # We may have been given a string representing an enum name.
                # Failsafe in case enum conversion didn't happen elsewhere.
                try:
                    return SettingsMap[keyString][valueString]
                except ValueError:
                    raise ValueError(f"Value '{valueString}' is invalid for setting '{keyString}'.")

        for k, v in form_data.items():
            # If this setting key is associated with an enum, convert the
            # value(s) to that enum.
            if k in SettingsMap:
                if type(v) is list:
                    settingValue = []
                    for val in v:
                        settingValue.append(get_enum_value(k, val))
                    setattr(self, k, settingValue)
                else:
                    settingValue = get_enum_value(k, v)
                    setattr(self, k, settingValue)
            else:
                # The value is a basic type, so assign it directly.
                setattr(self, k, v)

        # Sync homebrew_header values - if either is True, set both to True
        if hasattr(self, "homebrew_header_patch") and self.homebrew_header_patch:
            self.homebrew_header = True
        elif hasattr(self, "homebrew_header") and self.homebrew_header:
            if not hasattr(self, "homebrew_header_patch"):
                self.homebrew_header_patch = False

    def update_progression_totals(self):
        """Update the troff and blocker totals if we're randomly setting them."""
        # Assign weights to Troff n Scoff based on level order if not shuffling loading zones
        # Hard level shuffling makes these weights meaningless, as you'll be going into levels in a random order
        self.troff_weight_0 = 0.5
        self.troff_weight_1 = 0.55
        self.troff_weight_2 = 0.6
        self.troff_weight_3 = 0.7
        self.troff_weight_4 = 0.8
        self.troff_weight_5 = 0.9
        self.troff_weight_6 = 1.0
        self.troff_weight_7 = 1.0
        if self.level_randomization in (LevelRandomization.loadingzone, LevelRandomization.loadingzonesdecoupled) or self.hard_level_progression:
            self.troff_weight_0 = 1
            self.troff_weight_1 = 1
            self.troff_weight_2 = 1
            self.troff_weight_3 = 1
            self.troff_weight_4 = 1
            self.troff_weight_5 = 1
            self.troff_weight_6 = 1
            self.troff_weight_7 = 1

        if self.tns_selection_behavior != TroffSetting.pre_selected:
            randomlist = []
            for min_percentage in self.troff_min:
                randomlist.append(self.random.randint(round(self.troff_max * min_percentage), self.troff_max))
            cbs = randomlist
            self.troff_0 = round(min(cbs[0] * self.troff_weight_0, 500))
            self.troff_1 = round(min(cbs[1] * self.troff_weight_1, 500))
            self.troff_2 = round(min(cbs[2] * self.troff_weight_2, 500))
            self.troff_3 = round(min(cbs[3] * self.troff_weight_3, 500))
            self.troff_4 = round(min(cbs[4] * self.troff_weight_4, 500))
            self.troff_5 = round(min(cbs[5] * self.troff_weight_5, 500))
            self.troff_6 = round(min(cbs[6] * self.troff_weight_6, 500))
            self.troff_7 = round(min(cbs[7] * self.troff_weight_7, 500))
        self.BossBananas = [
            self.troff_0,
            self.troff_1,
            self.troff_2,
            self.troff_3,
            self.troff_4,
            self.troff_5,
            self.troff_6,
            self.troff_7,
        ]

        self.BLockerEntryItems = [BarrierItems.GoldenBanana] * 8
        self.BLockerEntryCount = [0] * 8

        self.blocker_limits = {
            # Will give customization to this eventually, just need to get a proof of concept working
            # BarrierItems.Nothing: 0,
            # BarrierItems.Kong: 5,
            # BarrierItems.Move: 41,
            BarrierItems.GoldenBanana: self.total_gbs - 1,
            BarrierItems.Blueprint: 40,
            BarrierItems.Fairy: self.total_fairies,
            # BarrierItems.Key: 8,
            BarrierItems.Crown: self.total_crowns,
            BarrierItems.CompanyCoin: 2,
            BarrierItems.Medal: self.total_medals,
            BarrierItems.Bean: 1,
            BarrierItems.Pearl: self.total_pearls,
            BarrierItems.RainbowCoin: self.total_rainbow_coins,
            # BarrierItems.IceTrap: 10,
            # BarrierItems.Percentage: 20,
            # BarrierItems.ColoredBanana: 1000,
        }

        if self.blocker_selection_behavior == BLockerSetting.chaos:
            self.blocker_text = min(self.blocker_text, 100) / 100.0  # Clamp value at 100%
            locked_blocker_items = []
            for slot in range(8):
                item = self.random.choice([key for key in self.blocker_limits.keys() if key not in locked_blocker_items])
                count = 0
                if self.blocker_text > 0:
                    count = self.random.randint(1, math.ceil(self.blocker_limits[item] * self.blocker_text))
                self.BLockerEntryItems[slot] = item
                self.BLockerEntryCount[slot] = count
                # Some barriers can only show up once
                if item in (BarrierItems.Bean, BarrierItems.Pearl, BarrierItems.CompanyCoin):
                    locked_blocker_items.append(item)
        else:
            if self.blocker_selection_behavior != BLockerSetting.pre_selected:
                if self.blocker_max > 0:
                    choice_list = range(1, self.blocker_max)
                    if self.blocker_max < 7:
                        # Can't create a random list with purely the range. Too small of a list
                        choice_list = [int(x / 10) for x in range(10, (self.blocker_max * 10) + 9)]
                    randomlist = self.random.choices(choice_list, k=7)
                    b_lockers = randomlist
                    if self.shuffle_loading_zones == ShuffleLoadingZones.all or self.hard_level_progression:
                        b_lockers.append(self.random.randint(1, self.blocker_max))
                        self.random.shuffle(b_lockers)
                    else:
                        b_lockers.append(1)
                        b_lockers.sort()
                else:
                    b_lockers = [0, 0, 0, 0, 0, 0, 0, 0]
                self.blocker_0 = b_lockers[0]
                self.blocker_1 = b_lockers[1]
                self.blocker_2 = b_lockers[2]
                self.blocker_3 = b_lockers[3]
                self.blocker_4 = b_lockers[4]
                self.blocker_5 = b_lockers[5]
                self.blocker_6 = b_lockers[6]
                if self.maximize_helm_blocker:
                    self.blocker_7 = self.blocker_max
                else:
                    self.blocker_7 = b_lockers[7]
            # Store banana values in array
            self.BLockerEntryCount = [
                self.blocker_0,
                self.blocker_1,
                self.blocker_2,
                self.blocker_3,
                self.blocker_4,
                self.blocker_5,
                self.blocker_6,
                self.blocker_7,
            ]

    def generate_main(self):
        """Set Default items on main page."""
        self.seed = None
        self.download_patch_file = None
        self.load_patch_file = None
        self.bonus_barrel_rando = None  # Deprecated
        self.disable_hard_minigames = None
        self.loading_zone_coupled = None
        self.move_rando = MoveRando.off
        self.ice_trap_frequency = IceTrapFrequency.mild  # Deprecated
        self.ice_trap_model_v2 = IceTrapModel2.simple
        self.start_with_slam = False
        self.random_patches = None
        self.random_crates = None
        self.random_fairies = None
        self.random_prices = None
        self.boss_location_rando = None
        # self.boss_kong_rando = None  # Deprecated
        self.krool_in_boss_pool_v2 = KroolInBossPool.off
        self.kasplat_rando_setting = None
        # self.puzzle_rando = None  # Deprecated
        self.puzzle_rando_difficulty = PuzzleRando.off
        self.jetpac_platform_data = [
            (0xC0, 0x30, 4),
            (0x20, 0x48, 4),
            (0x78, 0x60, 2),
        ]
        self.shuffle_shops = None
        # self.switchsanity = SwitchsanityLevel.off  # Deprecated
        self.switchsanity_enabled = False
        self.switchsanity_switch_isles_to_kroc_top = SwitchsanityKong.tiny
        self.switchsanity_switch_isles_helm_lobby = SwitchsanityGone.gone_pad
        self.switchsanity_switch_isles_aztec_lobby_back_room = SwitchsanityKong.tiny
        self.switchsanity_switch_isles_fungi_lobby_fairy = SwitchsanityKong.tiny
        self.switchsanity_switch_isles_spawn_rocketbarrel = SwitchsanityKong.lanky
        self.switchsanity_switch_japes_to_hive = SwitchsanityKong.tiny
        self.switchsanity_switch_japes_to_rambi = SwitchsanityKong.donkey
        self.switchsanity_switch_japes_to_painting_room = SwitchsanityKong.diddy
        self.switchsanity_switch_japes_to_cavern = SwitchsanityKong.diddy
        self.switchsanity_switch_japes_free_kong = SwitchsanityKong.donkey
        self.switchsanity_switch_aztec_to_kasplat_room = SwitchsanityKong.donkey
        self.switchsanity_switch_aztec_llama_front = SwitchsanityKong.donkey
        self.switchsanity_switch_aztec_llama_side = SwitchsanityKong.lanky
        self.switchsanity_switch_aztec_llama_back = SwitchsanityKong.tiny
        self.switchsanity_switch_aztec_sand_tunnel = SwitchsanityKong.donkey
        self.switchsanity_switch_aztec_to_connector_tunnel = SwitchsanityKong.diddy
        self.switchsanity_switch_aztec_free_lanky = SwitchsanityKong.donkey
        self.switchsanity_switch_aztec_free_tiny = SwitchsanityKong.diddy
        self.switchsanity_switch_factory_free_kong = SwitchsanityKong.lanky
        self.switchsanity_switch_galleon_to_lighthouse_side = SwitchsanityKong.donkey
        self.switchsanity_switch_galleon_to_shipwreck_side = SwitchsanityKong.diddy
        self.switchsanity_switch_galleon_to_cannon_game = SwitchsanityKong.chunky
        self.switchsanity_switch_fungi_yellow_tunnel = SwitchsanityKong.lanky
        self.switchsanity_switch_fungi_green_tunnel_near = SwitchsanityKong.tiny
        self.switchsanity_switch_fungi_green_tunnel_far = SwitchsanityKong.chunky
        self.diddy_freeing_kong = Kongs.donkey
        self.lanky_freeing_kong = Kongs.donkey
        self.tiny_freeing_kong = Kongs.diddy
        self.chunky_freeing_kong = Kongs.lanky
        self.switchsanity_data = {}
        self.extreme_debugging = False  # Use when you want to know VERY specifically where things fail in the fill - unnecessarily slows seed generation!

        # Item Counts
        self.total_gbs = 201
        self.total_crowns = 10
        self.total_pearls = 5
        self.total_medals = 40
        self.total_fairies = 20
        self.total_rainbow_coins = 16

        # The major setting for item randomization
        self.shuffle_items = True
        self.enemy_drop_rando = False
        self.snide_reward_rando = False
        self.most_snide_rewards = 25

        # In item rando, can any Kong collect any item?
        self.free_trade_setting = False

    def set_seed(self):
        """Forcibly re-set the random seed to the seed set in the config."""
        self.random.seed(self.seed)

    def generate_progression(self):
        """Set default items on progression page."""
        self.blocker_0 = None
        self.blocker_1 = None
        self.blocker_2 = None
        self.blocker_3 = None
        self.blocker_4 = None
        self.blocker_5 = None
        self.blocker_6 = None
        self.blocker_7 = None
        self.troff_0 = None
        self.troff_1 = None
        self.troff_2 = None
        self.troff_3 = None
        self.troff_4 = None
        self.troff_5 = None
        self.troff_6 = None
        self.troff_7 = None
        self.troff_min = None
        self.troff_max = None
        self.blocker_text = ""
        self.troff_text = ""
        self.blocker_difficulty = BLockerDifficulty.normal  # Deprecated

    def generate_misc(self):
        """Set default items on misc page."""
        #  Settings which affect logic
        self.enable_plandomizer = False
        # crown_door_random: bool
        # crown_door_item: HelmDoorItem
        # crown_door_item_count: int
        self.crown_door_random = False
        self.crown_door_item = HelmDoorItem.vanilla
        self.crown_door_item_count = 1
        # coin_door_random: bool
        # coin_door_item: HelmDoorItem
        # coin_door_item_count: int
        self.coin_door_random = False
        self.coin_door_item = HelmDoorItem.vanilla
        self.coin_door_item_count = 1
        # krool_phase_count: int, [1-5]
        self.krool_phase_count = 5
        self.krool_random = False
        self.cannons_require_blast = False  # Affects the Chunky phase slam switch and all(!) blast barrels - this is likely to be split up later
        # helm_phase_count: int, [1-5]
        self.helm_phase_count = 3
        self.helm_random = False
        # krool_key_count: int, [0-8]
        self.krool_key_count = 0
        self.keys_random = False
        # starting_kongs_count: int, [1-5]
        self.starting_kong = Kongs.any
        self.starting_kongs_count = 5
        self.starting_random = False

        self.disable_racing_patches = False

        self.has_password = False
        self.password = [1] * 8

        # bonus_barrels: MinigameBarrels
        # skip (auto-completed)
        # normal
        # random
        # selected
        self.bonus_barrels = MinigameBarrels.normal
        # helm_barrels: MinigameBarrels
        # skip (helm skip all)
        # normal
        # random
        self.helm_barrels = MinigameBarrels.normal
        self.training_barrels_minigames = MinigameBarrels.normal
        self.bonus_barrel_auto_complete = False

        # Alternate Minecart Mayhem where you get coins to win
        self.alt_minecart_mayhem = False

        # Not making these a series of settings that can be toggled by the user yet.
        # If people want to be able to toggle this, we can make a simple UI switch and the back-end has already been handled appropriately
        self.sprint_barrel_requires_sprint = True
        self.fix_lanky_tiny_prod = True

        self.chaos_blockers = False  # Deprecated

        # hard_shooting: bool
        self.hard_shooting = False  # Deprecated

        # hard_mode: bool
        # self.hard_mode = None  # Deprecated

        # damage multiplier: DamageAmount
        self.damage_amount = DamageAmount.default
        self.wipe_file_on_death = False

        # logic_type: LogicType
        # nologic - No Logical considerations
        # glitch - Glitch logic factored in
        # glitchless - Glitchless ruleset
        self.logic_type = LogicType.glitchless

        # shuffle_loading_zones: ShuffleLoadingZones
        # none
        # levels
        # all
        self.shuffle_loading_zones = ShuffleLoadingZones.none

        # decoupled_loading_zones: bool
        self.decoupled_loading_zones = False

        # Always start with training barrels currently
        # training_barrels: TrainingBarrels
        # normal
        # shuffled
        self.training_barrels = TrainingBarrels.normal

        # climbing_status: ClimbingStatus
        # normal
        # shuffled
        self.climbing_status = ClimbingStatus.normal

        # The status of camera & shockwave: ShockwaveStatus
        # vanilla - both located at Banana Fairy Isle
        # shuffled - located in a random valid location
        # shuffled_decoupled - camera and shockwave are separate upgrades and can be anywhere
        # start_with - start with camera and shockwave
        self.shockwave_status = ShockwaveStatus.vanilla

        self.shops_dont_cost = False
        self.less_fragile_boulders = False

        #  Music
        self.music_bgm_randomized = False
        self.music_majoritems_randomized = False
        self.music_minoritems_randomized = False
        self.music_events_randomized = False
        self.random_music = False
        self.music_rando_enabled = False
        self.music_is_custom = False
        self.music_vanilla_locations = False
        self.music_disable_reverb = False
        self.isles_cool_musical = False
        self.music_selection_dict = {
            "vanilla": {},
            "custom": {},
        }
        self.music_selections = None
        self.bgm_songs_selected = False
        self.majoritems_songs_selected = False
        self.minoritems_songs_selected = False
        self.events_songs_selected = False

        #  Unlock Moves - 0-40?
        self.starting_moves_count = 0
        self.starting_moves_list_counts = []
        self.starting_moves_lists = []

        #  Color
        self.colors = {}
        self.color_palettes = {}
        # Random Model Swaps
        self.random_models = RandomModels.off
        # self.random_enemy_colors = RandomModels.off  # Deprecated
        self.random_kong_colors = False
        self.random_colors_selected = []
        self.bother_klaptrap_model = Model.KlaptrapGreen
        self.beetle_model = Model.Beetle
        self.rabbit_model = Model.Rabbit
        self.panic_fairy_model = Model.BananaFairy
        self.turtle_model = Model.Turtle
        self.panic_klaptrap_model = Model.KlaptrapGreen
        self.seek_klaptrap_model = Model.KlaptrapGreen
        self.fungi_tomato_model = Model.Tomato
        self.caves_tomato_model = Model.IceTomato
        self.piano_burp_model = Model.KoshKremlingRed
        self.spotlight_fish_model = Model.SpotlightFish
        self.candy_cutscene_model = Model.Candy
        self.funky_cutscene_model = Model.Funky
        self.boot_cutscene_model = Model.Boot
        #
        self.minigame_melon_sprite = Sprite.BouncingMelon
        # DK
        self.dk_fur_colors = CharacterColors.vanilla
        self.dk_fur_custom_color = "#000000"
        self.dk_tie_colors = CharacterColors.vanilla
        self.dk_tie_custom_color = "#000000"
        # Diddy
        self.diddy_clothes_colors = CharacterColors.vanilla
        self.diddy_clothes_custom_color = "#000000"
        # Lanky
        self.lanky_clothes_colors = CharacterColors.vanilla
        self.lanky_clothes_custom_color = "#000000"
        self.lanky_fur_colors = CharacterColors.vanilla
        self.lanky_fur_custom_color = "#000000"
        # Tiny
        self.tiny_clothes_colors = CharacterColors.vanilla
        self.tiny_clothes_custom_color = "#000000"
        self.tiny_hair_colors = CharacterColors.vanilla
        self.tiny_hair_custom_color = "#000000"
        # Chunky
        self.chunky_main_colors = CharacterColors.vanilla
        self.chunky_main_custom_color = "#000000"
        self.chunky_other_colors = CharacterColors.vanilla
        self.chunky_other_custom_color = "#000000"
        # Transformations
        self.rambi_skin_colors = CharacterColors.vanilla
        self.rambi_skin_custom_color = "#000000"
        self.enguarde_skin_colors = CharacterColors.vanilla
        self.enguarde_skin_custom_color = "#000000"
        # Misc
        self.gb_colors = CharacterColors.vanilla
        self.gb_custom_color = "#000000"

        self.disco_donkey = False
        self.disco_chunky = False
        self.dark_mode_textboxes = False
        self.pause_hint_coloring = True
        self.menu_texture_index = None
        self.menu_texture_name = "Default"
        self.wrinkly_rgb = [255, 255, 255]
        self.krusha_ui = KrushaUi.no_slot
        self.kong_model_dk = KongModels.default
        self.kong_model_diddy = KongModels.default
        self.kong_model_lanky = KongModels.default
        self.kong_model_tiny = KongModels.default
        self.kong_model_chunky = KongModels.default
        self.kong_model_mode = KongModelMode.manual
        self.krusha_kong = None
        self.misc_cosmetics = False
        self.remove_water_oscillation = False
        self.rainbow_ammo = False
        self.song_speed_near_win = False
        self.disable_flavor_text = False
        self.head_balloons = False
        self.homebrew_header = False
        self.homebrew_header_patch = False
        self.camera_is_follow = False
        self.sfx_volume = 100
        self.music_volume = 100
        # self.true_widescreen = False  # Deprecated
        self.anamorphic_widescreen = False
        self.troff_brighten = False
        self.better_dirt_patch_cosmetic = False
        self.crosshair_outline = False
        self.camera_is_not_inverted = False
        self.fps_display = False
        self.sound_type = SoundType.stereo
        self.custom_music_proportion = 100
        self.smoother_camera = False
        self.fill_with_custom_music = False
        self.pool_tracks = False
        self.color_coded_powerups = True
        self.show_song_name = False

        # Custom Textures
        self.custom_transition = None
        self.custom_troff_portal = None
        self.painting_isles = None
        self.painting_museum_krool = None
        self.painting_museum_knight = None
        self.painting_museum_swords = None
        self.painting_treehouse_dolphin = None
        self.painting_treehouse_candy = None

        #  Misc
        self.generate_spoilerlog = None
        self.fast_start_beginning_of_game = True
        self.fast_start_beginning_of_game_dummy = True  # Decoupled from the actual setting for a little bit until we improve stability
        self.helm_setting = None
        self.helm_room_bonus_count = HelmBonuses.two
        # self.quality_of_life = None  # Deprecated
        self.wrinkly_available = False
        self.shorten_boss = False
        self.enable_tag_anywhere = None
        self.krool_phase_order_rando = None
        self.krool_access = False
        self.win_condition_spawns_ship = 0  # 0 = Key-based, 1 = Win condition-based
        self.helm_phase_order_rando = None
        self.open_lobbies = None
        self.randomize_pickups = False
        self.random_medal_requirement = False
        self.medal_requirement = 15
        self.medal_cb_req = 75
        self.rareware_gb_fairies = 20
        self.mermaid_gb_pearls = 5
        self.medal_jetpac_behavior = RandomRequirement.pre_selected
        self.pearl_mermaid_behavior = RandomRequirement.pre_selected
        self.fairy_queen_behavior = RandomRequirement.pre_selected
        self.cb_medal_behavior = RandomRequirement.pre_selected  # Deprecated
        self.cb_medal_behavior_new = CBRequirement.pre_selected
        self.medal_cb_req_level = [75] * 8
        self.bananaport_rando = BananaportRando.off
        self.activate_all_bananaports = ActivateAllBananaports.off
        self.shop_indicator = False
        self.randomize_cb_required_amounts = False  # Deprecated
        self.randomize_blocker_required_amounts = False  # Deprecated
        self.maximize_helm_blocker = False
        self.perma_death = False
        self.disable_tag_barrels = False
        self.ice_traps_damage = False
        self.level_randomization = LevelRandomization.vanilla
        self.shuffle_helm_location = False
        self.kong_rando = False
        self.kongs_for_progression = False
        self.wrinkly_hints = WrinklyHints.off
        self.spoiler_hints = SpoilerHints.off
        self.dim_solved_hints = False
        self.spoiler_include_woth_count = False
        self.spoiler_include_level_order = False
        self.serious_hints = False
        self.fast_warps = False
        self.dpad_display = DPadDisplays.off
        self.auto_keys = False
        self.kko_phase_order = [0] * 4
        self.toe_order = [0] * 10
        self.mill_levers = [0] * 5
        self.jetpac_enemy_order = list(range(8))
        self.crypt_levers = [1, 4, 3]
        self.dartboard_order = [3, 1, 2, 0, 5, 4]  # Orange, Melon, Banana, Crystal, Medal, Ammo Crate
        self.diddy_rnd_doors = [[0] * 4, [0] * 4, [0] * 4]
        # self.enemy_rando = False  # Deprecated
        # self.crown_enemy_rando = CrownEnemyRando.off  # Deprecated
        self.crown_enemy_difficulty = CrownEnemyDifficulty.vanilla
        self.crown_difficulties = [CrownEnemyDifficulty.vanilla] * 10
        self.enemy_speed_rando = False
        self.normalize_enemy_sizes = False
        self.randomize_enemy_sizes = False
        # self.cb_rando = CBRando.off  # Deprecated
        self.cb_rando_list_selected = []
        self.cb_rando_enabled = False
        self.coin_rando = False
        self.race_coin_rando = False
        self.crown_placement_rando = False
        self.bananaport_placement_rando = ShufflePortLocations.off
        self.useful_bananaport_placement = True
        self.override_cosmetics = True
        self.hard_level_progression = False
        self.hard_blockers = False
        self.hard_troff_n_scoff = False  # Deprecated
        self.blocker_selection_behavior = BLockerSetting.normal_random
        self.tns_selection_behavior = TroffSetting.normal_random
        self.wrinkly_location_rando = False
        self.tns_location_rando = False
        # self.dk_portal_location_rando = False  # Deprecated
        self.dk_portal_location_rando_v2 = DKPortalRando.off
        self.level_portal_destinations = [
            {
                "map": Maps.JungleJapes,
                "exit": 15,
            },
            {
                "map": Maps.AngryAztec,
                "exit": 0,
            },
            {
                "map": Maps.FranticFactory,
                "exit": 0,
            },
            {
                "map": Maps.GloomyGalleon,
                "exit": 0,
            },
            {
                "map": Maps.FungiForest,
                "exit": 27,
            },
            {
                "map": Maps.CrystalCaves,
                "exit": 0,
            },
            {
                "map": Maps.CreepyCastle,
                "exit": 0,
            },
        ]
        self.level_void_maps = [
            Maps.JungleJapes,
            Maps.AngryAztec,
            Maps.FranticFactory,
            Maps.GloomyGalleon,
            Maps.FungiForest,
            Maps.CrystalCaves,
            Maps.CreepyCastle,
        ]
        self.level_entrance_regions = [
            Regions.JungleJapesStart,
            Regions.AngryAztecStart,
            Regions.FranticFactoryStart,
            Regions.GloomyGalleonStart,
            Regions.FungiForestStart,
            Regions.CrystalCavesMain,
            Regions.CreepyCastleMain,
        ]
        self.mech_fish_entrance = {
            "map": Maps.GalleonMechafish,
            "exit": 0,
        }
        self.vanilla_door_rando = False
        self.dos_door_rando = False
        self.minigames_list_selected = []
        self.item_rando_list_selected = []
        self.misc_changes_selected = []
        self.bosses_selected = []
        self.allow_boss_duping = False
        self.hard_mode_selected = []
        # Item Rando
        self.item_rando_list_0 = []
        self.item_rando_list_1 = []
        self.item_rando_list_2 = []
        self.item_rando_list_3 = []
        self.item_rando_list_4 = []
        self.item_rando_list_5 = []
        self.item_rando_list_6 = []
        self.item_rando_list_7 = []
        self.item_rando_list_8 = []
        self.item_rando_list_9 = []
        self.item_search = [
            [],
            [],
            [],
            [],
        ]
        self.check_search = [
            [],
            [],
            [],
            [],
        ]
        self.decouple_item_rando = False
        self.filler_items_selected = []
        # self.hard_bosses = False  # Deprecated
        self.hard_bosses_selected = []
        self.mirror_mode = False
        # self.faster_checks_enabled = False  # Deprecated
        # self.remove_barriers_enabled = False  # Deprecated
        self.faster_checks_selected = []
        self.remove_barriers_selected = []
        # self.songs_excluded = False  # Deprecated
        self.excluded_songs_selected = []
        # self.music_filtering = False  # Deprecated
        self.music_filtering_selected = []
        self.enemies_selected = []
        self.glitches_selected = []
        self.starting_keys_list_selected = []
        self.warp_level_list_selected = []
        self.select_keys = False
        self.helm_hurry = False
        self.colorblind_mode = ColorblindMode.off
        self.big_head_mode = BigHeadMode.off
        # self.win_condition = WinCondition.beat_krool  # Deprecated
        self.win_condition_random = False
        self.win_condition_item = WinConditionComplex.get_keys_3_and_8
        self.win_condition_count = 1
        self.key_8_helm = False
        self.k_rool_vanilla_requirement = False
        self.random_starting_region = False
        self.random_starting_region_new = RandomStartingRegion.off
        self.starting_region = {}
        self.holiday_setting = False
        self.holiday_setting_offseason = False
        self.remove_wrinkly_puzzles = False
        self.smaller_shops = False
        self.no_consumable_upgrades = False
        self.alter_switch_allocation = False
        self.prog_slam_level_1 = SlamRequirement.green
        self.prog_slam_level_2 = SlamRequirement.green
        self.prog_slam_level_3 = SlamRequirement.green
        self.prog_slam_level_4 = SlamRequirement.green
        self.prog_slam_level_5 = SlamRequirement.blue
        self.prog_slam_level_6 = SlamRequirement.blue
        self.prog_slam_level_7 = SlamRequirement.red
        self.prog_slam_level_8 = SlamRequirement.red
        self.ice_trap_count = 0
        self.trap_weight_bubble = 3
        self.trap_weight_reverse = 3
        self.trap_weight_slow = 3
        self.trap_weight_disablea = 1
        self.trap_weight_disableb = 1
        self.trap_weight_disablez = 1
        self.trap_weight_disablecu = 1
        self.trap_weight_getout = 1
        self.trap_weight_dry = 2
        self.trap_weight_flip = 2
        self.trap_weight_icefloor = 2
        self.trap_weight_paper = 2
        self.trap_weight_slip = 3
        self.trap_weight_animal = 1
        self.trap_weight_rockfall = 1
        self.trap_weight_disabletag = 2
        self.switch_allocation = [
            self.prog_slam_level_1,
            self.prog_slam_level_2,
            self.prog_slam_level_3,
            self.prog_slam_level_4,
            self.prog_slam_level_5,
            self.prog_slam_level_6,
            self.prog_slam_level_7,
            self.prog_slam_level_8,
        ]
        self.item_reward_previews = False
        self.microhints_enabled = MicrohintsEnabled.off
        self.more_cutscene_skips = ExtraCutsceneSkips.off
        self.portal_numbers = False
        self.fungi_time = FungiTimeSetting.day
        self.fungi_time_internal = FungiTimeSetting.day
        self.galleon_water = GalleonWaterSetting.lowered
        self.galleon_water_internal = GalleonWaterSetting.lowered
        self.chunky_phase_slam_req = SlamRequirement.blue
        self.chunky_phase_slam_req_internal = SlamRequirement.blue
        # Helm Hurry
        self.helmhurry_list_starting_time = 1200
        self.helmhurry_list_golden_banana = 20
        self.helmhurry_list_blueprint = 45
        self.helmhurry_list_company_coins = 300
        self.helmhurry_list_move = 30
        self.helmhurry_list_banana_medal = 60
        self.helmhurry_list_rainbow_coin = 15
        self.helmhurry_list_boss_key = 150
        self.helmhurry_list_battle_crown = 90
        self.helmhurry_list_bean = 120
        self.helmhurry_list_pearl = 50
        self.helmhurry_list_kongs = 240
        self.helmhurry_list_fairies = 50
        self.helmhurry_list_colored_bananas = 3
        self.helmhurry_list_ice_traps = -40
        # Point spread
        self.points_list_kongs = 11
        self.points_list_keys = 11
        self.points_list_shopkeepers = 11
        self.points_list_guns = 9
        self.points_list_instruments = 9
        self.points_list_training_moves = 7
        self.points_list_important_shared = 5
        self.points_list_fairy_moves = 7
        self.points_list_pad_moves = 3
        self.points_list_barrel_moves = 7
        self.points_list_active_moves = 5
        self.points_list_bean = 3
        # Progressive hints
        self.progressive_hint_item = ProgressiveHintItem.off
        # self.enable_progressive_hints = False  # Deprecated
        # self.progressive_hint_text = 0  # Deprecated
        self.progressive_hint_count = 0
        # Misc
        self.archipelago = False

    def shuffle_prices(self, spoiler):
        """Price randomization. Reuseable if we need to reshuffle prices."""
        # Price Rando
        if self.random_prices != RandomPrices.vanilla:
            self.prices = RandomizePrices(spoiler, self.random_prices)
            self.original_prices = self.prices.copy()

    def resolve_settings(self):
        """Resolve settings which are not directly set through the UI."""
        self.fast_start_beginning_of_game = True  # Double make sure this is set
        # Correct the invalid items in the starting move lists and identify the total number of starting moves
        guaranteed_starting_moves = []
        self.starting_moves_list_counts = [
            self.starting_moves_list_count_1,
            self.starting_moves_list_count_2,
            self.starting_moves_list_count_3,
            self.starting_moves_list_count_4,
            self.starting_moves_list_count_5,
        ]
        self.starting_moves_lists = [self.starting_moves_list_1, self.starting_moves_list_2, self.starting_moves_list_3, self.starting_moves_list_4, self.starting_moves_list_5]
        for i in range(len(self.starting_moves_lists)):
            copy_of_list = self.starting_moves_lists[i].copy()
            for item in copy_of_list:
                # The additional fake progressive items are translated into the correct version
                if item in (Items.ProgressiveSlam2, Items.ProgressiveSlam3):
                    self.starting_moves_lists[i].remove(item)
                    self.starting_moves_lists[i].append(Items.ProgressiveSlam)
                if item == Items.ProgressiveAmmoBelt2:
                    self.starting_moves_lists[i].remove(item)
                    self.starting_moves_lists[i].append(Items.ProgressiveAmmoBelt)
                elif item in (Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3):
                    self.starting_moves_lists[i].remove(item)
                    self.starting_moves_lists[i].append(Items.ProgressiveInstrumentUpgrade)
            # If we are intending to place every item in this pool, these moves are guaranteed to be placed
            if len(self.starting_moves_lists[i]) <= self.starting_moves_list_counts[i]:
                self.starting_moves_list_counts[i] = len(self.starting_moves_lists[i])
                guaranteed_starting_moves.extend(self.starting_moves_lists[i])
        self.starting_moves_count = sum(self.starting_moves_list_counts)

        # Some settings have to be derived from the guaranteed starting moves - this needs to be done early in this method
        # If we are *guaranteed* to start with a slam, place it in the training grounds reward slot and don't make it hintable, as before
        if Items.ProgressiveSlam in guaranteed_starting_moves:
            self.start_with_slam = True
        else:
            self.start_with_slam = False
        # If we are *guaranteed* to start with ALL training moves, put them in their vanilla locations and don't make them hintable, as before
        if Items.Vines in guaranteed_starting_moves and Items.Barrels in guaranteed_starting_moves and Items.Oranges in guaranteed_starting_moves and Items.Swim in guaranteed_starting_moves:
            self.training_barrels = TrainingBarrels.normal
        else:
            self.training_barrels = TrainingBarrels.shuffled
        # If Climbing is a guaranteed starting move, treat it like the others as well.
        if Items.Climbing in guaranteed_starting_moves:
            self.climbing_status = ClimbingStatus.normal
        else:
            self.climbing_status = ClimbingStatus.shuffled
        # If you start with two copies of Progressive Instrument Upgrade, you start with 3 melons of health
        if guaranteed_starting_moves.count(Items.ProgressiveInstrumentUpgrade) == 2:
            self.start_with_3rd_melon = True
        else:
            self.start_with_3rd_melon = False

        # Switchsanity handling
        ShufflableExits[Transitions.AztecMainToLlama].entryKongs = {
            Kongs.donkey,
            Kongs.lanky,
            Kongs.tiny,
        }  # This might get changed here, reset this to the default now
        self.switchsanity_data = deepcopy(SwitchData)
        if self.switchsanity_enabled:
            ssanity_setting_values = {
                Switches.IslesMonkeyport: self.switchsanity_switch_isles_to_kroc_top,
                Switches.IslesHelmLobbyGone: self.switchsanity_switch_isles_helm_lobby,
                Switches.IslesAztecLobbyFeather: self.switchsanity_switch_isles_aztec_lobby_back_room,
                Switches.IslesFungiLobbyFeather: self.switchsanity_switch_isles_fungi_lobby_fairy,
                Switches.IslesSpawnRocketbarrel: self.switchsanity_switch_isles_spawn_rocketbarrel,
                Switches.JapesFeather: self.switchsanity_switch_japes_to_hive,
                Switches.JapesRambi: self.switchsanity_switch_japes_to_rambi,
                Switches.JapesPainting: self.switchsanity_switch_japes_to_painting_room,
                Switches.JapesDiddyCave: self.switchsanity_switch_japes_to_cavern,
                Switches.JapesFreeKong: self.switchsanity_switch_japes_free_kong,
                Switches.AztecBlueprintDoor: self.switchsanity_switch_aztec_to_kasplat_room,
                Switches.AztecLlamaCoconut: self.switchsanity_switch_aztec_llama_front,
                Switches.AztecLlamaGrape: self.switchsanity_switch_aztec_llama_side,
                Switches.AztecLlamaFeather: self.switchsanity_switch_aztec_llama_back,
                Switches.AztecQuicksandSwitch: self.switchsanity_switch_aztec_sand_tunnel,
                Switches.AztecGuitar: self.switchsanity_switch_aztec_to_connector_tunnel,
                Switches.AztecLlamaPuzzle: self.switchsanity_switch_aztec_free_lanky,
                Switches.AztecOKONGPuzzle: self.switchsanity_switch_aztec_free_tiny,
                Switches.FactoryFreeKong: self.switchsanity_switch_factory_free_kong,
                Switches.GalleonLighthouse: self.switchsanity_switch_galleon_to_lighthouse_side,
                Switches.GalleonShipwreck: self.switchsanity_switch_galleon_to_shipwreck_side,
                Switches.GalleonCannonGame: self.switchsanity_switch_galleon_to_cannon_game,
                Switches.FungiYellow: self.switchsanity_switch_fungi_yellow_tunnel,
                Switches.FungiGreenFeather: self.switchsanity_switch_fungi_green_tunnel_near,
                Switches.FungiGreenPineapple: self.switchsanity_switch_fungi_green_tunnel_far,
            }

            kongs = GetKongs()
            for slot in ssanity_setting_values:
                if slot == Switches.IslesHelmLobbyGone:
                    # Has a unique setting mapping due to the plethora of choices
                    applied_setting = ssanity_setting_values[slot]
                    gone_mapping = {
                        SwitchsanityGone.bongos: (Kongs.donkey, SwitchType.InstrumentPad),
                        SwitchsanityGone.guitar: (Kongs.diddy, SwitchType.InstrumentPad),
                        SwitchsanityGone.trombone: (Kongs.lanky, SwitchType.InstrumentPad),
                        SwitchsanityGone.sax: (Kongs.tiny, SwitchType.InstrumentPad),
                        SwitchsanityGone.triangle: (Kongs.chunky, SwitchType.InstrumentPad),
                        SwitchsanityGone.lever: (Kongs.donkey, SwitchType.MiscActivator),
                        SwitchsanityGone.gong: (Kongs.diddy, SwitchType.MiscActivator),
                        SwitchsanityGone.gone_pad: (Kongs.chunky, SwitchType.PadMove),
                    }
                    if applied_setting == SwitchsanityGone.random:
                        applied_setting = self.random.choice(list(gone_mapping.keys()))
                    self.switchsanity_data[slot].kong = gone_mapping[applied_setting][0]
                    self.switchsanity_data[slot].switch_type = gone_mapping[applied_setting][1]
                else:
                    applied_setting = ssanity_setting_values[slot]
                    kong_mapping = {
                        SwitchsanityKong.donkey: Kongs.donkey,
                        SwitchsanityKong.diddy: Kongs.diddy,
                        SwitchsanityKong.lanky: Kongs.lanky,
                        SwitchsanityKong.tiny: Kongs.tiny,
                        SwitchsanityKong.chunky: Kongs.chunky,
                        SwitchsanityKong.any: Kongs.any,
                    }
                    bad_kongs = [self.switchsanity_data[x].kong for x in self.switchsanity_data[slot].tied_settings]
                    options = [
                        SwitchsanityKong.donkey,
                        SwitchsanityKong.diddy,
                        SwitchsanityKong.lanky,
                        SwitchsanityKong.tiny,
                        SwitchsanityKong.chunky,
                    ]
                    options = [x for x in options if kong_mapping[x] not in bad_kongs]
                    if slot == Switches.IslesMonkeyport:
                        options = [SwitchsanityKong.donkey, SwitchsanityKong.lanky, SwitchsanityKong.tiny]
                    elif slot == Switches.AztecOKONGPuzzle:
                        options = [SwitchsanityKong.diddy, SwitchsanityKong.chunky]
                    elif slot == Switches.AztecQuicksandSwitch:
                        options = [
                            SwitchsanityKong.donkey,
                            SwitchsanityKong.diddy,
                            SwitchsanityKong.lanky,
                            SwitchsanityKong.tiny,
                            SwitchsanityKong.chunky,
                        ]
                    if applied_setting == SwitchsanityKong.random:
                        applied_setting = self.random.choice(options)
                    if slot == Switches.FactoryFreeKong:
                        self.switchsanity_data[slot].kong = Kongs.lanky
                    else:
                        if applied_setting == SwitchsanityKong.any:
                            self.switchsanity_data[slot].kong = Kongs.any
                        else:
                            self.switchsanity_data[slot].kong = Kongs.donkey + (applied_setting - SwitchsanityKong.donkey)
            # If we've shuffled all loading zones, we need to account for some entrances changing hands
            if self.shuffle_loading_zones == ShuffleLoadingZones.all:
                ShufflableExits[Transitions.AztecMainToLlama].entryKongs = {
                    self.switchsanity_data[Switches.AztecLlamaCoconut].kong,
                    self.switchsanity_data[Switches.AztecLlamaGrape].kong,
                    self.switchsanity_data[Switches.AztecLlamaFeather].kong,
                }
        self.diddy_freeing_kong = self.switchsanity_data[Switches.JapesFreeKong].kong
        self.lanky_freeing_kong = self.switchsanity_data[Switches.AztecLlamaPuzzle].kong
        self.tiny_freeing_kong = self.switchsanity_data[Switches.AztecOKONGPuzzle].kong
        self.chunky_freeing_kong = self.switchsanity_data[Switches.FactoryFreeKong].kong

        # Determine item requirements if random
        req_data = {
            "pearls": {
                RandomRequirement.easy_random: (1, 2),
                RandomRequirement.medium_random: (2, 3),
                RandomRequirement.hard_random: (3, 5),
            },
            "medals": {
                RandomRequirement.easy_random: (1, 10),
                RandomRequirement.medium_random: (11, 20),
                RandomRequirement.hard_random: (21, 40),
            },
            "fairies": {
                RandomRequirement.easy_random: (1, 6),
                RandomRequirement.medium_random: (7, 13),
                RandomRequirement.hard_random: (14, 20),
            },
            "cbs": {
                CBRequirement.easy_random: (1, 30),
                CBRequirement.medium_random: (31, 50),
                CBRequirement.hard_random: (51, 100),
            },
        }
        if self.pearl_mermaid_behavior != RandomRequirement.pre_selected:
            min_bound = req_data["pearls"][self.pearl_mermaid_behavior][0]
            max_bound = req_data["pearls"][self.pearl_mermaid_behavior][1]
            self.mermaid_gb_pearls = self.random.randint(min_bound, max_bound)
        if self.medal_jetpac_behavior != RandomRequirement.pre_selected:
            min_bound = req_data["medals"][self.medal_jetpac_behavior][0]
            max_bound = req_data["medals"][self.medal_jetpac_behavior][1]
            self.medal_requirement = self.random.randint(min_bound, max_bound)
        if self.fairy_queen_behavior != RandomRequirement.pre_selected:
            min_bound = req_data["fairies"][self.fairy_queen_behavior][0]
            max_bound = req_data["fairies"][self.fairy_queen_behavior][1]
            self.rareware_gb_fairies = self.random.randint(min_bound, max_bound)
        if self.cb_medal_behavior_new == CBRequirement.pre_selected:
            self.medal_cb_req_level = [self.medal_cb_req] * 8
        elif self.cb_medal_behavior_new == CBRequirement.progressive:
            ratios = MEDAL_PROGRESSIVE_RATIOS.copy()
            if not IsItemSelected(self.cb_rando_enabled, self.cb_rando_list_selected, Levels.DKIsles):
                ratios[6] = 1
            allocation = [int(self.medal_cb_req * x) for x in ratios]
            self.random.shuffle(allocation)
            self.medal_cb_req_level = allocation.copy()
        else:
            min_bound = req_data["cbs"][self.cb_medal_behavior_new][0]
            max_bound = req_data["cbs"][self.cb_medal_behavior_new][1]
            req = self.random.randint(min_bound, max_bound)
            self.medal_cb_req_level = [req] * 8

        # If water is lava, then Instrument Upgrades are considered important for the purposes of getting 3rd Melon
        if IsDDMSSelected(self.hard_mode_selected, HardModeSelected.water_is_lava):
            ItemList[Items.ProgressiveInstrumentUpgrade].playthrough = True
            ItemPool.ImportantSharedMoves = [
                Items.ProgressiveSlam,
                Items.ProgressiveSlam,
                Items.ProgressiveSlam,
                Items.SniperSight,
                Items.HomingAmmo,
                Items.ProgressiveInstrumentUpgrade,
                Items.ProgressiveInstrumentUpgrade,
                Items.ProgressiveInstrumentUpgrade,
            ]
            ItemPool.JunkSharedMoves = [Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt]

        # Dos' Doors requires this to be on - it's a variant on vanilla door shuffle
        if self.dos_door_rando:
            self.vanilla_door_rando = True
        # If we're using the vanilla door shuffle, turn both wrinkly and tns rando on
        if self.vanilla_door_rando:
            self.wrinkly_location_rando = True
            self.tns_location_rando = True

        # Krusha Kong
        # if self.krusha_ui == KrushaUi.random:
        #     slots = [x for x in range(5) if x != Kongs.chunky or not self.disco_chunky]  # Only add Chunky if Disco not on (People with disco on probably don't want Krusha as Chunky)
        #     self.krusha_kong = self.random.choice(slots)
        # else:
        #     self.krusha_kong = None
        #     krusha_conversion = {
        #         KrushaUi.no_slot: None,
        #         KrushaUi.dk: Kongs.donkey,
        #         KrushaUi.diddy: Kongs.diddy,
        #         KrushaUi.lanky: Kongs.lanky,
        #         KrushaUi.tiny: Kongs.tiny,
        #         KrushaUi.chunky: Kongs.chunky,
        #     }
        #     if self.krusha_ui in krusha_conversion:
        #         self.krusha_kong = krusha_conversion[self.krusha_ui]

        # Fungi Time of Day
        if self.fungi_time == FungiTimeSetting.random:
            self.fungi_time_internal = self.random.choice([FungiTimeSetting.day, FungiTimeSetting.night])
        else:
            self.fungi_time_internal = self.fungi_time

        # Galleon Water Level
        if self.galleon_water == GalleonWaterSetting.random:
            self.galleon_water_internal = self.random.choice([GalleonWaterSetting.lowered, GalleonWaterSetting.raised])
        else:
            self.galleon_water_internal = self.galleon_water

        # Chunky Phase Slam Requirement
        if self.chunky_phase_slam_req == SlamRequirement.random:
            self.chunky_phase_slam_req_internal = self.random.choice([SlamRequirement.green, SlamRequirement.blue, SlamRequirement.red])
        else:
            self.chunky_phase_slam_req_internal = self.chunky_phase_slam_req

        # Helm Doors
        helmdoor_items = {
            HelmDoorItem.req_gb: HelmDoorInfo(self.total_gbs),
            HelmDoorItem.req_bp: HelmDoorInfo(
                40,
                HelmDoorRandomInfo(20, 30, 0.1),
                HelmDoorRandomInfo(10, 20, 0.2),
                HelmDoorRandomInfo(4, 10, 0.25),
            ),
            HelmDoorItem.req_companycoins: HelmDoorInfo(
                2,
                HelmDoorRandomInfo(1, 2, 0.05),
            ),
            HelmDoorItem.req_key: HelmDoorInfo(8),
            HelmDoorItem.req_medal: HelmDoorInfo(
                self.total_medals,
                HelmDoorRandomInfo(20, 30, 0.2),
                HelmDoorRandomInfo(10, 20, 0.21),
                HelmDoorRandomInfo(4, 10, 0.25),
            ),
            HelmDoorItem.req_crown: HelmDoorInfo(
                self.total_crowns,
                HelmDoorRandomInfo(5, 7, 0.14),
                HelmDoorRandomInfo(3, 5, 0.14),
                HelmDoorRandomInfo(1, 3, 0.1),
            ),
            HelmDoorItem.req_fairy: HelmDoorInfo(
                self.total_fairies,
                HelmDoorRandomInfo(9, 14, 0.18),
                HelmDoorRandomInfo(5, 9, 0.18),
                HelmDoorRandomInfo(2, 5, 0.18),
            ),  # Remove two fairies since you can't get the final two fairies glitchless if on the crown door
            HelmDoorItem.req_rainbowcoin: HelmDoorInfo(
                self.total_rainbow_coins,
                HelmDoorRandomInfo(8, 12, 0.18),
                HelmDoorRandomInfo(4, 8, 0.18),
                HelmDoorRandomInfo(2, 4, 0.18),
            ),
            HelmDoorItem.req_bean: HelmDoorInfo(
                1,
                HelmDoorRandomInfo(1, 1, 0.05),
                HelmDoorRandomInfo(1, 1, 0.01),
            ),
            HelmDoorItem.req_pearl: HelmDoorInfo(
                self.total_pearls,
                HelmDoorRandomInfo(2, 4, 0.1),
                HelmDoorRandomInfo(1, 2, 0.08),
                HelmDoorRandomInfo(1, 1, 0.04),
            ),
        }
        random_helm_door_settings = (HelmDoorItem.easy_random, HelmDoorItem.medium_random, HelmDoorItem.hard_random)
        self.crown_door_random = self.crown_door_item in random_helm_door_settings
        self.coin_door_random = self.coin_door_item in random_helm_door_settings
        crown_door_pool = {}
        coin_door_pool = {}
        if self.blocker_selection_behavior == BLockerSetting.chaos:
            helmdoor_items[HelmDoorItem.req_gb].hard = HelmDoorRandomInfo(60, 100, 0.05)
            helmdoor_items[HelmDoorItem.req_gb].medium = HelmDoorRandomInfo(30, 60, 0.1)
            helmdoor_items[HelmDoorItem.req_gb].easy = HelmDoorRandomInfo(10, 30, 0.125)
            helmdoor_items[HelmDoorItem.req_bp].hard.selection_weight = 0.05
            helmdoor_items[HelmDoorItem.req_bp].medium.selection_weight = 0.1
            helmdoor_items[HelmDoorItem.req_bp].easy.selection_weight = 0.125
        crown_diff = random_helm_door_settings.index(self.crown_door_item) if self.crown_door_item in random_helm_door_settings else None
        coin_diff = random_helm_door_settings.index(self.coin_door_item) if self.coin_door_item in random_helm_door_settings else None
        for item in helmdoor_items:
            data = helmdoor_items[item]
            crown_door_info = data.getDifficultyInfo(crown_diff)
            coin_door_info = data.getDifficultyInfo(coin_diff)
            if crown_door_info is not None:
                crown_door_pool[item] = crown_door_info.chooseAmount(self.random)
            if coin_door_info is not None:
                coin_door_pool[item] = coin_door_info.chooseAmount(self.random)
        if self.crown_door_random:
            potential_items = [x for x in list(crown_door_pool.keys()) if x != self.coin_door_item]
            potential_item_weights = []
            for x in potential_items:
                data = helmdoor_items[x].getDifficultyInfo(crown_diff)
                weight = 0 if data is None else data.selection_weight
                potential_item_weights.append(weight)
            selected_item = self.random.choices(potential_items, weights=potential_item_weights, k=1)[0]
            self.crown_door_item = selected_item
            self.crown_door_item_count = crown_door_pool[selected_item]
        if self.coin_door_random:
            potential_items = [x for x in list(coin_door_pool.keys()) if x != self.crown_door_item]
            potential_item_weights = []
            for x in potential_items:
                data = helmdoor_items[x].getDifficultyInfo(coin_diff)
                weight = 0 if data is None else data.selection_weight
                potential_item_weights.append(weight)
            selected_item = self.random.choices(potential_items, weights=potential_item_weights, k=1)[0]
            self.coin_door_item = selected_item
            self.coin_door_item_count = coin_door_pool[selected_item]
        if self.crown_door_item in helmdoor_items.keys():
            self.crown_door_item_count = min(self.crown_door_item_count, helmdoor_items[self.crown_door_item].absolute_max)
        if self.coin_door_item in helmdoor_items.keys():
            self.coin_door_item_count = min(self.coin_door_item_count, helmdoor_items[self.coin_door_item].absolute_max)
        self.coin_door_item = DoorItemToBarrierItem(self.coin_door_item, True)
        self.crown_door_item = DoorItemToBarrierItem(self.crown_door_item, False, True)

        # Determine ice trap order
        effects = {
            "bubble": self.trap_weight_bubble,
            "reverse": self.trap_weight_reverse,
            "slow": self.trap_weight_slow,
            "disa": self.trap_weight_disablea,
            "disb": self.trap_weight_disableb,
            "discu": self.trap_weight_disablecu,
            "disz": self.trap_weight_disablez,
            "getout": self.trap_weight_getout,
            "dry": self.trap_weight_dry,
            "flip": self.trap_weight_flip,
            "icefloor": self.trap_weight_icefloor,
            "paper": self.trap_weight_paper,
            "slip": self.trap_weight_slip,
            "animal": self.trap_weight_animal,
            "rockfall": self.trap_weight_rockfall,
            "disabletag": self.trap_weight_disabletag,
        }
        if self.ice_trap_model_v2 == IceTrapModel2.simple:
            models_chance = {"gb": 1}  # Only GB models
        elif self.ice_trap_model_v2 == IceTrapModel2.fair:
            models_chance = {"gb": 10, "bean": 1, "fairy": 4}  # Weighted distribution
        else:  # IceTrapModel2.complex
            models_chance = {"gb": 10, "key": 2, "bean": 1, "fairy": 4}  # Weighted distribution
        trap_data = {
            "gb": {
                "bubble": Items.IceTrapBubble,
                "reverse": Items.IceTrapReverse,
                "slow": Items.IceTrapSlow,
                "disa": Items.IceTrapDisableA,
                "disb": Items.IceTrapDisableB,
                "disz": Items.IceTrapDisableZ,
                "discu": Items.IceTrapDisableCU,
                "getout": Items.IceTrapGetOutGB,
                "dry": Items.IceTrapDryGB,
                "flip": Items.IceTrapFlipGB,
                "icefloor": Items.IceTrapIceFloorGB,
                "paper": Items.IceTrapPaperGB,
                "slip": Items.IceTrapSlipGB,
                "animal": Items.IceTrapAnimalGB,
                "rockfall": Items.IceTrapRockfallGB,
                "disabletag": Items.IceTrapDisableTagGB,
            },
            "bean": {
                "bubble": Items.IceTrapBubbleBean,
                "reverse": Items.IceTrapReverseBean,
                "slow": Items.IceTrapSlowBean,
                "disa": Items.IceTrapDisableABean,
                "disb": Items.IceTrapDisableBBean,
                "disz": Items.IceTrapDisableZBean,
                "discu": Items.IceTrapDisableCUBean,
                "getout": Items.IceTrapGetOutBean,
                "dry": Items.IceTrapDryBean,
                "flip": Items.IceTrapFlipBean,
                "icefloor": Items.IceTrapIceFloorBean,
                "paper": Items.IceTrapPaperBean,
                "slip": Items.IceTrapSlipBean,
                "animal": Items.IceTrapAnimalBean,
                "rockfall": Items.IceTrapRockfallBean,
                "disabletag": Items.IceTrapDisableTagBean,
            },
            "key": {
                "bubble": Items.IceTrapBubbleKey,
                "reverse": Items.IceTrapReverseKey,
                "slow": Items.IceTrapSlowKey,
                "disa": Items.IceTrapDisableAKey,
                "disb": Items.IceTrapDisableBKey,
                "disz": Items.IceTrapDisableZKey,
                "discu": Items.IceTrapDisableCUKey,
                "getout": Items.IceTrapGetOutKey,
                "dry": Items.IceTrapDryKey,
                "flip": Items.IceTrapFlipKey,
                "icefloor": Items.IceTrapIceFloorKey,
                "paper": Items.IceTrapPaperKey,
                "slip": Items.IceTrapSlipKey,
                "animal": Items.IceTrapAnimalKey,
                "rockfall": Items.IceTrapRockfallKey,
                "disabletag": Items.IceTrapDisableTagKey,
            },
            "fairy": {
                "bubble": Items.IceTrapBubbleFairy,
                "reverse": Items.IceTrapReverseFairy,
                "slow": Items.IceTrapSlowFairy,
                "disa": Items.IceTrapDisableAFairy,
                "disb": Items.IceTrapDisableBFairy,
                "disz": Items.IceTrapDisableZFairy,
                "discu": Items.IceTrapDisableCUFairy,
                "getout": Items.IceTrapGetOutFairy,
                "dry": Items.IceTrapDryFairy,
                "flip": Items.IceTrapFlipFairy,
                "icefloor": Items.IceTrapIceFloorFairy,
                "paper": Items.IceTrapPaperFairy,
                "slip": Items.IceTrapSlipFairy,
                "animal": Items.IceTrapAnimalFairy,
                "rockfall": Items.IceTrapRockfallFairy,
                "disabletag": Items.IceTrapDisableTagFairy,
            },
        }
        self.trap_assortment = []
        trap_limit = self.ice_trap_count
        if self.archipelago:
            trap_limit = 0
        elif trap_limit > 0 and ItemRandoFiller.icetraps not in self.filler_items_selected:
            self.filler_items_selected.append(ItemRandoFiller.icetraps)
        for _ in range(trap_limit):
            chosen_effect = self.random.choices(list(effects.keys()), list(effects.values()), k=1)[0]
            chosen_model = self.random.choices(list(models_chance.keys()), list(models_chance.values()), k=1)[0]
            chosen_item = trap_data[chosen_model][chosen_effect]
            self.trap_assortment.append(chosen_item)

        if self.has_password:
            for x in range(8):
                self.password[x] = self.random.randint(1, 6)
        if self.dk_portal_location_rando_v2 != DKPortalRando.off:
            level_base_maps = [Maps.JungleJapes, Maps.AngryAztec, Maps.FranticFactory, Maps.GloomyGalleon, Maps.FungiForest, Maps.CrystalCaves, Maps.CreepyCastle]
            self.level_portal_destinations = [
                {
                    "map": k,
                    "exit": -1,
                }
                for k in level_base_maps
            ]

        self.item_pool_info = []
        self.shuffled_location_types = []
        self.junk_offset = 0
        self.shuffled_check_allowances = {}
        if self.shuffle_items:
            item_ui_pairing = {
                # value: tuple(TiedType, TiedItemType, IsCheck)
                ItemRandoListSelected.shop: (Types.Shop, Types.Shop, True),
                ItemRandoListSelected.moves: (Types.Shop, Types.Shop, False),
                ItemRandoListSelected.shockwave: (Types.Shockwave, Types.Shockwave, False),
                ItemRandoListSelected.bfi_gift: (Types.Shockwave, Types.Shockwave, True),
                ItemRandoListSelected.banana: (Types.Banana, Types.Banana, False),
                ItemRandoListSelected.banana_checks: (Types.Banana, Types.Banana, True),
                ItemRandoListSelected.racebanana: (Types.Banana, Types.RaceBanana, True),
                ItemRandoListSelected.gauntletbanana: (Types.Banana, Types.GauntletBanana, True),
                ItemRandoListSelected.blueprintbanana: (Types.BlueprintBanana, Types.BlueprintBanana, False),
                ItemRandoListSelected.sniderewards: (Types.BlueprintBanana, Types.BlueprintBanana, True),
                ItemRandoListSelected.arenas: (Types.Crown, Types.Crown, True),
                ItemRandoListSelected.crown: (Types.Crown, Types.Crown, False),
                ItemRandoListSelected.blueprint: (Types.Blueprint, Types.Blueprint, False),
                ItemRandoListSelected.kasplat: (Types.Blueprint, Types.Blueprint, True),
                ItemRandoListSelected.key: (Types.Key, Types.Key, False),
                ItemRandoListSelected.bosses: (Types.Key, Types.Key, True),
                ItemRandoListSelected.endofhelm: (Types.Key, Types.HelmKey, True),
                ItemRandoListSelected.medal: (Types.Medal, Types.Medal, False),
                ItemRandoListSelected.medal_checks: (Types.Medal, Types.Medal, True),
                ItemRandoListSelected.medal_checks_helm: (Types.Medal, Types.HelmMedal, True),
                ItemRandoListSelected.nintendocoin: (Types.NintendoCoin, Types.NintendoCoin, False),
                ItemRandoListSelected.arcade: (Types.NintendoCoin, Types.NintendoCoin, True),
                ItemRandoListSelected.rarewarecoin: (Types.RarewareCoin, Types.RarewareCoin, False),
                ItemRandoListSelected.jetpac: (Types.RarewareCoin, Types.RarewareCoin, True),
                ItemRandoListSelected.kong: (Types.Kong, Types.Kong, False),
                ItemRandoListSelected.kong_cages: (Types.Kong, Types.Kong, True),
                ItemRandoListSelected.fairy: (Types.Fairy, Types.Fairy, False),
                ItemRandoListSelected.fairy_checks: (Types.Fairy, Types.Fairy, True),
                ItemRandoListSelected.rainbowcoin: (Types.RainbowCoin, Types.RainbowCoin, False),
                ItemRandoListSelected.dirt_patches: (Types.RainbowCoin, Types.RainbowCoin, True),
                ItemRandoListSelected.pearl: (Types.Pearl, Types.Pearl, False),
                ItemRandoListSelected.clams: (Types.Pearl, Types.Pearl, True),
                ItemRandoListSelected.bean: (Types.Bean, Types.Bean, False),
                ItemRandoListSelected.anthillreward: (Types.Bean, Types.Bean, True),
                ItemRandoListSelected.crateitem: (Types.CrateItem, Types.CrateItem, True),
                ItemRandoListSelected.shopowners: (Types.Cranky, Types.Cranky, False),
                ItemRandoListSelected.hint: (Types.Hint, Types.Hint, False),
                ItemRandoListSelected.wrinkly: (Types.Hint, Types.Hint, True),
                ItemRandoListSelected.boulderitem: (Types.BoulderItem, Types.BoulderItem, True),
                ItemRandoListSelected.enemies: (Types.Enemies, Types.Enemies, True),
                ItemRandoListSelected.dummyitem_enemies: (Types.Enemies, Types.Enemies, False),
                ItemRandoListSelected.dummyitem_boulderitem: (Types.BoulderItem, Types.BoulderItem, False),
                ItemRandoListSelected.dummyitem_crateitem: (Types.CrateItem, Types.CrateItem, False),
                ItemRandoListSelected.trainingmoves: (Types.TrainingBarrel, Types.TrainingBarrel, False),
                ItemRandoListSelected.trainingbarrels: (Types.TrainingBarrel, Types.TrainingBarrel, True),
                ItemRandoListSelected.halfmedal: (Types.HalfMedal, Types.HalfMedal, True),
                ItemRandoListSelected.dummyitem_halfmedal: (Types.HalfMedal, Types.HalfMedal, False),
            }
            for selector_value, data in item_ui_pairing.items():
                self.shuffled_check_allowances[data[0]] = []

            filler_pairing = {
                ItemRandoFiller.junkitem: Types.JunkItem,
                ItemRandoFiller.icetraps: Types.FakeItem,
                ItemRandoFiller.banana: Types.FillerBanana,
                ItemRandoFiller.crown: Types.FillerCrown,
                ItemRandoFiller.fairy: Types.FillerFairy,
                ItemRandoFiller.medal: Types.FillerMedal,
                ItemRandoFiller.pearl: Types.FillerPearl,
                ItemRandoFiller.rainbowcoin: Types.FillerRainbowCoin,
            }
            item_search_removal = [
                # Anything which doesn't have accompanying checks. Usually starts with dummy_item
                ItemRandoListSelected.dummyitem_enemies,
                ItemRandoListSelected.dummyitem_boulderitem,
                ItemRandoListSelected.dummyitem_crateitem,
                ItemRandoListSelected.dummyitem_halfmedal,
            ]
            dummy_location_types = [Types.HelmKey, Types.HelmMedal]
            self.item_search = [
                self.item_rando_list_1.copy(),
                self.item_rando_list_2.copy(),
                self.item_rando_list_3.copy(),
                self.item_rando_list_4.copy(),
            ]
            self.check_search = [
                self.item_rando_list_6.copy(),
                self.item_rando_list_7.copy(),
                self.item_rando_list_8.copy(),
                self.item_rando_list_9.copy(),
            ]
            if not self.decouple_item_rando:
                # reconstruct check_search based on item_search
                for x in range(4):
                    self.check_search[x] = []  # Wipe cache
                for selector_value, data in item_ui_pairing.items():
                    paired_slot = None
                    paired_type = None
                    for index, slot in enumerate(self.item_search):
                        if selector_value in slot:
                            paired_slot = index
                            paired_type = data[0]
                            break
                    if paired_type is None:
                        continue
                    paired_selectors = []
                    for test_value, test_data in item_ui_pairing.items():
                        if test_data[0] == paired_type and test_data[2]:
                            # Is check
                            paired_selectors.append(test_value)
                    self.check_search[paired_slot].extend(paired_selectors)
            # Post-processing to clear anything that shouldn't be there
            for x in range(4):
                self.item_search[x] = [y for y in self.item_search[x] if y not in item_search_removal]
            # Build mapping based on item_search and check_search
            shopkeeper_type_mapping = {
                Types.Cranky: Items.Cranky,
                Types.Funky: Items.Funky,
                Types.Candy: Items.Candy,
                Types.Snide: Items.Snide,
            }
            for pool_index in range(4):
                self.item_pool_info.append(ItemPoolInfo())
                for selector_value in self.check_search[pool_index]:
                    selector_type = item_ui_pairing[selector_value][1]
                    selector_types = [selector_type]
                    if selector_type == Types.Cranky:
                        selector_types = [sk for sk in [Types.Cranky, Types.Snide, Types.Candy, Types.Funky] if shopkeeper_type_mapping[sk] not in guaranteed_starting_moves]
                    elif selector_type == Types.TrainingBarrel:
                        selector_types = [Types.TrainingBarrel, Types.PreGivenMove]
                        if self.climbing_status != ClimbingStatus.normal:
                            selector_types.append(Types.Climbing)
                    elif selector_type == Types.Medal and IsItemSelected(self.cb_rando_enabled, self.cb_rando_list_selected, Levels.DKIsles):
                        selector_types = [Types.Medal, Types.IslesMedal]
                    # Add items which are in the designated pools
                    for item_selector_value in self.item_search[pool_index]:
                        item_type = item_ui_pairing[item_selector_value][1]
                        item_types = [item_type]
                        if item_type == Types.Cranky:
                            item_types = [sk for sk in [Types.Cranky, Types.Snide, Types.Candy, Types.Funky] if shopkeeper_type_mapping[sk] not in guaranteed_starting_moves]
                        elif item_type == Types.TrainingBarrel:
                            # Only include TrainingBarrel type if training moves aren't all guaranteed starting moves
                            training_barrel_items = [Items.Vines, Items.Swim, Items.Oranges, Items.Barrels]
                            if all(tb_item in guaranteed_starting_moves for tb_item in training_barrel_items):
                                item_types = []
                            else:
                                item_types = [Types.TrainingBarrel, Types.PreGivenMove]
                                if self.climbing_status != ClimbingStatus.normal:
                                    item_types.append(Types.Climbing)
                        elif item_type == Types.Medal and IsItemSelected(self.cb_rando_enabled, self.cb_rando_list_selected, Levels.DKIsles):
                            item_types = [Types.Medal, Types.IslesMedal]
                        for x in selector_types:
                            if x not in dummy_location_types:
                                self.shuffled_location_types.append(x)
                                self.item_pool_info[pool_index].location_types.append(x)
                            for y in item_types:
                                if x not in self.shuffled_check_allowances:
                                    self.shuffled_check_allowances[x] = []
                                self.shuffled_check_allowances[x].append(y)
                                if y not in dummy_location_types:
                                    self.shuffled_location_types.append(y)
                                    self.item_pool_info[pool_index].item_types.append(y)
                    for check, item_type in filler_pairing.items():
                        if check in self.filler_items_selected:
                            for x in selector_types:
                                self.shuffled_check_allowances[x].append(item_type)
                    for check, item_type in filler_pairing.items():
                        if check in self.filler_items_selected:
                            self.shuffled_location_types.append(item_type)
                    for x in selector_types:
                        self.shuffled_check_allowances[x] = list(set(self.shuffled_check_allowances[x]))
                self.item_pool_info[pool_index].location_types = list(set(self.item_pool_info[pool_index].location_types))
                self.item_pool_info[pool_index].item_types = list(set(self.item_pool_info[pool_index].item_types))
                # If location and item types are the same and exactly one type, then the pool isn't shuffled
                if (
                    len(self.item_pool_info[pool_index].location_types) == 1
                    and len(self.item_pool_info[pool_index].item_types) == 1
                    and self.item_pool_info[pool_index].location_types[0] == self.item_pool_info[pool_index].item_types[0]
                ):
                    self.item_pool_info[pool_index].is_shuffled = False
            self.shuffled_location_types = list(set(self.shuffled_location_types))

            # If training moves are not in any shuffled pool, add them to guaranteed_starting_moves
            if Types.TrainingBarrel not in self.shuffled_location_types:
                training_barrel_items = [Items.Vines, Items.Swim, Items.Oranges, Items.Barrels]
                for tb_item in training_barrel_items:
                    if tb_item not in guaranteed_starting_moves:
                        guaranteed_starting_moves.append(tb_item)
                self.training_barrels = TrainingBarrels.normal

            self.enemy_drop_rando = Types.Enemies in self.shuffled_location_types
            if Types.Shop in self.shuffled_location_types:
                self.move_rando = MoveRando.item_shuffle
            if Types.Shockwave not in self.shuffled_location_types:
                self.shockwave_status = ShockwaveStatus.vanilla
            elif Items.Camera in guaranteed_starting_moves and Items.Shockwave in guaranteed_starting_moves:
                self.shockwave_status = ShockwaveStatus.start_with
            else:
                self.shockwave_status = ShockwaveStatus.shuffled_decoupled
            banana_types = [Types.Banana, Types.GauntletBanana, Types.RaceBanana, Types.BlueprintBanana]
            has_banana = False
            for btype in banana_types:
                if btype in self.shuffled_location_types:
                    has_banana = True
            if not has_banana:
                self.total_gbs = 201
            if Types.Crown not in self.shuffled_location_types:
                self.total_crowns = 10
            if Types.RainbowCoin not in self.shuffled_location_types:
                self.total_rainbow_coins = 16
            if Types.Fairy not in self.shuffled_location_types:
                self.total_fairies = 20
            if Types.Medal not in self.shuffled_location_types:
                self.total_medals = 40
            if Types.Pearl not in self.shuffled_location_types:
                self.total_pearls = 5

        kongs = GetKongs()

        # B Locker and Troff n Scoff amounts Rando
        self.update_progression_totals()
        self.junk_offset = self.random.randint(0, 255)  # Offset when seeding junk just to make sure it's not all the same every time

        # Handle K. Rool Phases
        self.krool_donkey = False
        self.krool_diddy = False
        self.krool_lanky = False
        self.krool_tiny = False
        self.krool_chunky = False
        self.krool_dillo1 = False
        self.krool_dillo2 = False
        self.krool_dog1 = False
        self.krool_dog2 = False
        self.krool_madjack = False
        self.krool_pufftoss = False
        self.krool_kutout = False

        phases = [
            Maps.KroolDonkeyPhase,
            Maps.KroolDiddyPhase,
            Maps.KroolLankyPhase,
            Maps.KroolTinyPhase,
            Maps.KroolChunkyPhase,
        ]
        if self.krool_in_boss_pool_v2 == KroolInBossPool.full_shuffle:
            phases.extend(
                [
                    Maps.JapesBoss,
                    Maps.AztecBoss,
                    Maps.FactoryBoss,
                    Maps.GalleonBoss,
                    Maps.FungiBoss,
                    Maps.CavesBoss,
                    Maps.CastleBoss,
                ]
            )
        # This guard is for backwards compatibility
        if not self.bosses_selected:
            self.bosses_selected = BossMapList.copy() + KRoolMaps.copy()
        phases = [x for x in phases if x in self.bosses_selected]
        possible_phases = phases.copy()
        if self.krool_phase_order_rando:
            self.random.shuffle(phases)
        if self.krool_random:
            self.krool_phase_count = self.random.randint(1, 5)
        if isinstance(self.krool_phase_count, str) is True:
            self.krool_phase_count = 5
        self.allow_boss_duping = len(self.bosses_selected) < (7 + self.krool_phase_count)
        # Dupe phases so there's enough choice
        if len(phases) < self.krool_phase_count:
            if len(phases) == 0:  # This will get caught by a SettingsIncompatibleException later, but this means we have no valid K. Rool options.
                dupe_count = 0
            else:
                dupe_count = math.ceil(self.krool_phase_count / len(phases))
            init_phases = phases.copy()
            for _ in range(dupe_count):
                phases.extend(init_phases)
        # Pick phases
        if self.krool_phase_count < len(phases):
            if self.krool_phase_order_rando:
                phases = self.random.sample(phases, self.krool_phase_count)
            else:
                phases = phases[: self.krool_phase_count]
        if len(phases) > 0 and phases[-1] == Maps.GalleonBoss:
            # Pufftoss can't be last. Pick something else
            if self.allow_boss_duping:
                phases[-1] = self.random.choice([x for x in possible_phases if x != Maps.GalleonBoss])
            else:
                phases[-1] = self.random.choice([x for x in possible_phases if x not in phases and x != Maps.GalleonBoss])
        # Plandomized K. Rool algorithm
        if self.enable_plandomizer:
            planned_phases = []
            # Place planned phases and clear out others
            for i in range(len(phases)):
                if self.plandomizer_dict["plando_krool_order_" + str(i)] != -1:  # Note that input validation guarantees this key exists in this dict
                    phases[i] = Maps(self.plandomizer_dict["plando_krool_order_" + str(i)])
                    planned_phases.append(Maps(self.plandomizer_dict["plando_krool_order_" + str(i)]))
                else:
                    phases[i] = None
            # Fill cleared out phases with available phases
            for i in range(len(phases)):
                if phases[i] is None:
                    available_phases = [map_id for map_id in possible_phases if map_id not in planned_phases]
                    phases[i] = self.random.choice(available_phases)
                    planned_phases.append(phases[i])
            for i in range(len(phases)):
                phases[i] = int(phases[i])
        orderedPhases = []
        # TODO: Fix logic (lol) (update: copilot autofilled "this is a mess" so now it has to stay forever)
        for map_id in phases:
            if map_id == Maps.KroolDonkeyPhase:
                self.krool_donkey = True
            elif map_id == Maps.KroolDiddyPhase:
                self.krool_diddy = True
            elif map_id == Maps.KroolLankyPhase:
                self.krool_lanky = True
            elif map_id == Maps.KroolTinyPhase:
                self.krool_tiny = True
            elif map_id == Maps.KroolChunkyPhase:
                self.krool_chunky = True
            elif map_id == Maps.JapesBoss:
                self.krool_dillo1 = True
            elif map_id == Maps.AztecBoss:
                self.krool_dog1 = True
            elif map_id == Maps.FactoryBoss:
                self.krool_madjack = True
            elif map_id == Maps.GalleonBoss:
                self.krool_pufftoss = True
            elif map_id == Maps.FungiBoss:
                self.krool_dog2 = True
            elif map_id == Maps.CavesBoss:
                self.krool_dillo2 = True
            elif map_id == Maps.CastleBoss:
                self.krool_kutout = True
            orderedPhases.append(map_id)
        self.krool_order = orderedPhases

        # Identify if any bosses are plando'd. If so, then the normal boss placement algorithm will be discarded for a random placement.
        self.boss_plando = self.enable_plandomizer and any([self.plandomizer_dict["plando_boss_order_" + str(i)] != -1 for i in range(7)])

        # Helm Order
        self.helm_donkey = False
        self.helm_diddy = False
        self.helm_lanky = False
        self.helm_tiny = False
        self.helm_chunky = False

        rooms = [Kongs.donkey, Kongs.chunky, Kongs.tiny, Kongs.lanky, Kongs.diddy]
        if self.helm_phase_order_rando:
            self.random.shuffle(rooms)
        if self.helm_random:
            self.helm_phase_count = self.random.randint(1, 5)
        if isinstance(self.helm_phase_count, str) is True:
            self.helm_phase_count = 5
        if self.helm_phase_count < 5:
            if self.helm_phase_order_rando:
                rooms = self.random.sample(rooms, self.helm_phase_count)
            else:
                rooms = rooms[: self.helm_phase_count]
        # Plandomized Helm room algorithm - only applies when we're already shuffling Helm Order!
        if self.enable_plandomizer and self.helm_phase_order_rando:
            planned_rooms = []
            # Place planned rooms and clear out others
            for i in range(len(rooms)):
                if self.plandomizer_dict["plando_helm_order_" + str(i)] != -1:  # Note that input validation guarantees this key exists in this dict
                    rooms[i] = Kongs(self.plandomizer_dict["plando_helm_order_" + str(i)])
                    planned_rooms.append(Kongs(self.plandomizer_dict["plando_helm_order_" + str(i)]))
                else:
                    rooms[i] = Kongs.any
            # Fill cleared out rooms with available rooms
            for i in range(len(rooms)):
                if rooms[i] == Kongs.any:
                    available_rooms = [kong for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky] if kong not in planned_rooms]
                    rooms[i] = self.random.choice(available_rooms)
                    planned_rooms.append(rooms[i])
        orderedRooms = []
        for kong in rooms:
            if kong == Kongs.donkey:
                orderedRooms.append(0)
                self.helm_donkey = True
            elif kong == Kongs.diddy:
                self.helm_diddy = True
                orderedRooms.append(4)
            elif kong == Kongs.lanky:
                self.helm_lanky = True
                orderedRooms.append(3)
            elif kong == Kongs.tiny:
                self.helm_tiny = True
                orderedRooms.append(2)
            elif kong == Kongs.chunky:
                self.helm_chunky = True
                orderedRooms.append(1)
        self.helm_order = orderedRooms
        self.kong_helm_order = rooms

        # Win Condition
        wincon_items = {
            WinConditionComplex.beat_krool: HelmDoorInfo(
                1,
                HelmDoorRandomInfo(1, 1, 0.06),
                HelmDoorRandomInfo(1, 1, 0.06),
                HelmDoorRandomInfo(1, 1, 0.03),
            ),
            WinConditionComplex.dk_rap_items: HelmDoorInfo(
                1,
                HelmDoorRandomInfo(1, 1, 0.04),
                HelmDoorRandomInfo(1, 1, 0.04),
                HelmDoorRandomInfo(1, 1, 0.02),
            ),
            WinConditionComplex.krem_kapture: HelmDoorInfo(
                1,
                HelmDoorRandomInfo(1, 1, 0.06),
                HelmDoorRandomInfo(1, 1, 0.03),
            ),
            WinConditionComplex.get_key8: HelmDoorInfo(1),
            WinConditionComplex.get_keys_3_and_8: HelmDoorInfo(1),
            WinConditionComplex.req_gb: HelmDoorInfo(
                self.total_gbs,
                HelmDoorRandomInfo(int(0.4 * self.total_gbs), int(0.75 * self.total_gbs), 0.1),
                HelmDoorRandomInfo(int(0.3 * self.total_gbs), int(0.4 * self.total_gbs), 0.1),
                HelmDoorRandomInfo(int(0.2 * self.total_gbs), int(0.3 * self.total_gbs), 0.15),
            ),
            WinConditionComplex.req_bp: HelmDoorInfo(
                40,
                HelmDoorRandomInfo(25, 35, 0.09),
                HelmDoorRandomInfo(20, 25, 0.1),
                HelmDoorRandomInfo(5, 20, 0.1),
            ),
            WinConditionComplex.req_companycoins: HelmDoorInfo(
                2,
                HelmDoorRandomInfo(1, 2, 0.05),
            ),
            WinConditionComplex.req_key: HelmDoorInfo(
                8,
                HelmDoorRandomInfo(7, 8, 0.05),
                HelmDoorRandomInfo(7, 8, 0.1),
                HelmDoorRandomInfo(7, 8, 0.1),
            ),
            WinConditionComplex.req_medal: HelmDoorInfo(
                self.total_medals,
                HelmDoorRandomInfo(int(0.625 * self.total_medals), int(0.875 * self.total_medals), 0.09),
                HelmDoorRandomInfo(int(0.5 * self.total_medals), int(0.625 * self.total_medals), 0.1),
                HelmDoorRandomInfo(int(0.125 * self.total_medals), int(0.5 * self.total_medals), 0.1),
            ),
            WinConditionComplex.req_crown: HelmDoorInfo(
                self.total_crowns,
                HelmDoorRandomInfo(int(0.7 * self.total_crowns), int(0.9 * self.total_crowns), 0.1),
                HelmDoorRandomInfo(int(0.4 * self.total_crowns), int(0.7 * self.total_crowns), 0.1),
                HelmDoorRandomInfo(int(0.2 * self.total_crowns), int(0.4 * self.total_crowns), 0.06),
            ),
            WinConditionComplex.req_fairy: HelmDoorInfo(
                self.total_fairies,
                HelmDoorRandomInfo(int(0.6 * self.total_fairies), int(0.9 * self.total_fairies), 0.1),
                HelmDoorRandomInfo(int(0.4 * self.total_fairies), int(0.6 * self.total_fairies), 0.12),
                HelmDoorRandomInfo(int(0.05 * self.total_fairies), int(0.4 * self.total_fairies), 0.18),
            ),
            WinConditionComplex.req_rainbowcoin: HelmDoorInfo(
                self.total_rainbow_coins,
                HelmDoorRandomInfo(int(0.625 * self.total_rainbow_coins), int(1.0 * self.total_rainbow_coins), 0.11),
                HelmDoorRandomInfo(int(0.375 * self.total_rainbow_coins), int(0.625 * self.total_rainbow_coins), 0.14),
                HelmDoorRandomInfo(int(0.1875 * self.total_rainbow_coins), int(0.375 * self.total_rainbow_coins), 0.18),
            ),
            WinConditionComplex.req_bean: HelmDoorInfo(
                1,
                HelmDoorRandomInfo(1, 1, 0.05),
                HelmDoorRandomInfo(1, 1, 0.01),
            ),
            WinConditionComplex.req_pearl: HelmDoorInfo(
                self.total_pearls,
                HelmDoorRandomInfo(int(0.8 * self.total_pearls), int(1.0 * self.total_pearls), 0.05),
                HelmDoorRandomInfo(int(0.6 * self.total_pearls), int(0.8 * self.total_pearls), 0.1),
                HelmDoorRandomInfo(int(0.2 * self.total_pearls), int(0.6 * self.total_pearls), 0.13),
            ),
            WinConditionComplex.req_bosses: HelmDoorInfo(7),
            WinConditionComplex.req_bonuses: HelmDoorInfo(len(getCompletableBonuses(self))),
        }
        random_win_con_settings = (
            WinConditionComplex.easy_random,
            WinConditionComplex.medium_random,
            WinConditionComplex.hard_random,
        )
        self.win_condition_random = self.win_condition_item in random_win_con_settings
        win_con_pool = {}
        wc_diff = random_win_con_settings.index(self.win_condition_item) if self.win_condition_item in random_win_con_settings else None
        for item in wincon_items:
            data = wincon_items[item]
            wc_info = data.getDifficultyInfo(wc_diff)
            if wc_info is not None:
                win_con_pool[item] = wc_info.chooseAmount(self.random)
        if self.win_condition_random:
            potential_items = list(win_con_pool.keys())
            potential_item_weights = []
            for x in potential_items:
                data = wincon_items[x].getDifficultyInfo(wc_diff)
                weight = 0 if data is None else data.selection_weight
                potential_item_weights.append(weight)
            selected_item = random.choices(potential_items, weights=potential_item_weights, k=1)[0]
            self.win_condition_item = selected_item
            self.win_condition_count = win_con_pool[selected_item]
        if self.win_condition_item in wincon_items.keys():
            self.win_condition_count = min(self.win_condition_count, wincon_items[self.win_condition_item].absolute_max)

        # Initial Switch Level Placement - Will be corrected if level order rando is on during the fill process. Disable it for vanilla
        if self.level_randomization == LevelRandomization.vanilla:
            self.alter_switch_allocation = False
        if self.alter_switch_allocation:
            slams = [SlamRequirement.green, SlamRequirement.blue, SlamRequirement.red]
            if self.prog_slam_level_1 == SlamRequirement.random:
                self.prog_slam_level_1 = self.random.choice(slams)
            if self.prog_slam_level_2 == SlamRequirement.random:
                self.prog_slam_level_2 = self.random.choice(slams)
            if self.prog_slam_level_3 == SlamRequirement.random:
                self.prog_slam_level_3 = self.random.choice(slams)
            if self.prog_slam_level_4 == SlamRequirement.random:
                self.prog_slam_level_4 = self.random.choice(slams)
            if self.prog_slam_level_5 == SlamRequirement.random:
                self.prog_slam_level_5 = self.random.choice(slams)
            if self.prog_slam_level_6 == SlamRequirement.random:
                self.prog_slam_level_6 = self.random.choice(slams)
            if self.prog_slam_level_7 == SlamRequirement.random:
                self.prog_slam_level_7 = self.random.choice(slams)
            if self.prog_slam_level_8 == SlamRequirement.random:
                self.prog_slam_level_8 = self.random.choice(slams)
            allocation = [
                self.prog_slam_level_1,
                self.prog_slam_level_2,
                self.prog_slam_level_3,
                self.prog_slam_level_4,
                self.prog_slam_level_5,
                self.prog_slam_level_6,
                self.prog_slam_level_7,
            ]
            if self.level_randomization in (LevelRandomization.level_order, LevelRandomization.level_order_complex, LevelRandomization.level_order_moderate):
                # Add an extra 3 into the calculation
                allocation.append(self.prog_slam_level_8)
                self.random.shuffle(allocation)
            else:
                # If LZR, always make Helm SDSS
                self.random.shuffle(allocation)
                allocation.append(self.prog_slam_level_8)
            self.switch_allocation = allocation.copy()

        if self.crown_enemy_difficulty != CrownEnemyDifficulty.vanilla:
            self.crown_difficulties = [self.crown_enemy_difficulty] * 10
            if self.crown_enemy_difficulty == CrownEnemyDifficulty.progressive:
                allocation = [CrownEnemyDifficulty.easy] * 4
                allocation.extend([CrownEnemyDifficulty.medium] * 4)
                allocation.extend([CrownEnemyDifficulty.hard] * 2)
                # Start out with a default of 4 easy, 4 medium, then 2 hard crowns
                # Randomize placement for LZR (Matching level order will come from a different calculation)
                self.random.shuffle(allocation)
                self.crown_difficulties = allocation.copy()

        # Mill Levers
        mill_shortened = IsDDMSSelected(self.faster_checks_selected, FasterChecksSelected.forest_mill_conveyor)
        if self.puzzle_rando_difficulty == PuzzleRando.off and mill_shortened:
            self.mill_levers = [2, 3, 1, 0, 0]
        elif self.puzzle_rando_difficulty != PuzzleRando.off:
            mill_lever_cap = 3 if mill_shortened else 5
            self.mill_levers = [0] * 5
            for slot in range(mill_lever_cap):
                self.mill_levers[slot] = self.random.randint(1, 3)

        # Jetpac Platforms
        if self.puzzle_rando_difficulty in (PuzzleRando.medium, PuzzleRando.hard, PuzzleRando.chaos):
            self.jetpac_platform_data = []
            exclusion_zones = [
                # Order: minx maxz miny maxy
                (158, 178, 0, 200),  # Drop chute
            ]
            exclusion_y = 0x30
            exclusion_pad_x = 4
            for _ in range(3):
                x = None
                y = None
                width = None
                while True:
                    x = random.randint(32, 192)
                    y = random.randint(exclusion_y, 170 - exclusion_y)
                    width = random.choice([1, 2, 2, 3, 3, 4, 4, 5])
                    x_right = x + 0x10 + (width * 8)
                    is_excluded = False
                    for zone in exclusion_zones:
                        if x_right < zone[0] or x > zone[1]:
                            continue
                        if y > zone[2] and y < zone[3]:
                            is_excluded = True
                    if not is_excluded:
                        break
                self.jetpac_platform_data.append((x, y, width))
                exclusion_zones.append(
                    [
                        x - exclusion_pad_x,
                        x + 0x10 + (width * 8) + exclusion_pad_x,
                        y - exclusion_y,
                        y + exclusion_y,
                    ]
                )

        if IsDDMSSelected(self.hard_mode_selected, HardModeSelected.shuffled_jetpac_enemies):
            jetpac_levels = list(range(8))
            self.random.shuffle(jetpac_levels)
            self.jetpac_enemy_order = jetpac_levels

        # Mayhem Coins
        gen_mayhem_coins(self, self.random)

        if self.puzzle_rando_difficulty != PuzzleRando.off:
            # Crypt Levers
            self.crypt_levers = self.random.sample([x + 1 for x in range(6)], 3)
            dartboard_order = []
            for _ in range(6):
                dartboard_order.append(self.random.randint(0, 7))
            self.dartboard_order = dartboard_order.copy()
            # Diddy R&D Doors
            self.diddy_rnd_doors = []
            start = list(range(4))
            self.random.shuffle(start)
            for id in range(3):
                code = [start[id]]
                selected_all_zeros = start[id] == 0
                for subindex in range(1, 4):
                    perm = self.random.randint(0, 3)
                    if subindex == 3 and selected_all_zeros:
                        perm = self.random.randint(1, 3)
                    if perm != 0:
                        selected_all_zeros = False
                    code.append(perm)
                self.diddy_rnd_doors.append(code)

        # Set keys required for KRool
        KeyEvents = [
            Events.JapesKeyTurnedIn,
            Events.AztecKeyTurnedIn,
            Events.FactoryKeyTurnedIn,
            Events.GalleonKeyTurnedIn,
            Events.ForestKeyTurnedIn,
            Events.CavesKeyTurnedIn,
            Events.CastleKeyTurnedIn,
            Events.HelmKeyTurnedIn,
        ]
        key_list = KeyEvents.copy()
        required_key_count = 0
        # Start by requiring every key
        self.krool_keys_required = KeyEvents.copy()
        # Determine how many keys we need - this can be random or selected
        if self.keys_random:
            required_key_count = self.random.randint(0, 8)
        else:
            # I mean, I guess this works
            required_key_count = 8 - self.krool_key_count
        key_8_required = self.krool_access or self.win_condition_item == WinConditionComplex.get_key8
        # Remove the need for keys we intend to start with
        if self.select_keys:
            for key in self.starting_keys_list_selected:
                if key == Items.JungleJapesKey:
                    self.krool_keys_required.remove(key_list[0])
                if key == Items.AngryAztecKey:
                    self.krool_keys_required.remove(key_list[1])
                if key == Items.FranticFactoryKey:
                    self.krool_keys_required.remove(key_list[2])
                if key == Items.GloomyGalleonKey:
                    self.krool_keys_required.remove(key_list[3])
                if key == Items.FungiForestKey:
                    self.krool_keys_required.remove(key_list[4])
                if key == Items.CrystalCavesKey:
                    self.krool_keys_required.remove(key_list[5])
                if key == Items.CreepyCastleKey:
                    self.krool_keys_required.remove(key_list[6])
                if key == Items.HideoutHelmKey and not key_8_required:  # Don't allow Key 8 to be started with if it's required
                    self.krool_keys_required.remove(key_list[7])
        # If the list of required keys is still greater than the amount of keys we want to require, we need to remove required keys
        if len(self.krool_keys_required) > required_key_count:
            while len(self.krool_keys_required) > required_key_count:
                # The Helm Key is not eligible to be removed if it's guaranteed to be needed
                removable_keys = [event for event in self.krool_keys_required if event != Events.HelmKeyTurnedIn or not key_8_required]
                if len(removable_keys) == 0:  # Key 8 being required is stronger than a need for 0 Keys - this will trigger if Key 8 is your last key to require but Key 8 is always required
                    break
                key_to_remove = self.random.choice(removable_keys)
                self.krool_keys_required.remove(key_to_remove)
        self.starting_key_list = []
        if Events.JapesKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.JungleJapesKey].playthrough = False
            self.starting_key_list.append(Items.JungleJapesKey)
        if Events.AztecKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.AngryAztecKey].playthrough = False
            self.starting_key_list.append(Items.AngryAztecKey)
        if Events.FactoryKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.FranticFactoryKey].playthrough = False
            self.starting_key_list.append(Items.FranticFactoryKey)
        if Events.GalleonKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.GloomyGalleonKey].playthrough = False
            self.starting_key_list.append(Items.GloomyGalleonKey)
        if Events.ForestKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.FungiForestKey].playthrough = False
            self.starting_key_list.append(Items.FungiForestKey)
        if Events.CavesKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.CrystalCavesKey].playthrough = False
            self.starting_key_list.append(Items.CrystalCavesKey)
        if Events.CastleKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.CreepyCastleKey].playthrough = False
            self.starting_key_list.append(Items.CreepyCastleKey)
        if Events.HelmKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.HideoutHelmKey].playthrough = False
            self.starting_key_list.append(Items.HideoutHelmKey)

        # Banana medals
        if self.random_medal_requirement:
            # Range roughly from 4 to 15, average around 10
            self.medal_requirement = round(self.random.normalvariate(10, 1.5))
        self.original_medal_requirement = self.medal_requirement
        if self.original_medal_requirement == 0:
            self.logical_medal_requirement = 0
        else:
            self.logical_medal_requirement = min(self.total_medals, max(self.medal_requirement + 1, math.floor(self.medal_requirement * 1.2)))
        self.original_fairy_requirement = self.rareware_gb_fairies
        if self.original_fairy_requirement == 0:
            self.logical_fairy_requirement = 0
        else:
            self.logical_fairy_requirement = min(self.total_fairies, max(self.rareware_gb_fairies + 1, int(self.rareware_gb_fairies * 1.2)))

        # Boss Rando
        self.boss_maps = ShuffleBosses(self.boss_location_rando, self)
        self.boss_kongs = ShuffleBossKongs(self)
        self.kutout_kongs = ShuffleKutoutKongs(self.random, self.boss_maps, self.boss_kongs, self.boss_location_rando)
        self.kko_phase_order = ShuffleKKOPhaseOrder(self)
        self.toe_order = ShuffleTinyPhaseToes(self.random)

        # Bonus Barrel Rando
        if self.bonus_barrel_auto_complete:
            self.bonus_barrels = MinigameBarrels.skip
        elif self.minigames_list_selected:
            self.bonus_barrels = MinigameBarrels.selected
        # Helm Barrel Rando
        if self.helm_setting == HelmSetting.skip_all:
            self.helm_barrels = MinigameBarrels.skip
        elif len(self.minigames_list_selected) > 0:
            self.helm_barrels = MinigameBarrels.random
        if self.fast_start_beginning_of_game:
            self.training_barrels_minigames = MinigameBarrels.skip
        elif len(self.minigames_list_selected) > 0:
            self.training_barrels_minigames = MinigameBarrels.random

        # Loading Zone Rando
        if self.level_randomization in (LevelRandomization.level_order, LevelRandomization.level_order_complex, LevelRandomization.level_order_moderate):
            self.shuffle_loading_zones = ShuffleLoadingZones.levels
            self.hard_level_progression = self.level_randomization == LevelRandomization.level_order_complex
        elif self.level_randomization == LevelRandomization.loadingzone:
            self.shuffle_loading_zones = ShuffleLoadingZones.all
        elif self.level_randomization == LevelRandomization.loadingzonesdecoupled:
            self.shuffle_loading_zones = ShuffleLoadingZones.all
            self.decoupled_loading_zones = True
        elif self.level_randomization == LevelRandomization.vanilla:
            self.shuffle_loading_zones = ShuffleLoadingZones.none
        self.shuffle_aztec_temples = self.shuffle_items and Types.Kong in self.shuffled_location_types

        # Kong rando - this is generally forced on in most settings, but it can be disabled
        # Disabling this variable causes Kongs to not be placed during the fill, use with caution
        if self.starting_random:
            self.starting_kongs_count = self.random.randint(1, 5)
        if Types.Kong in self.shuffled_location_types:
            self.kong_rando = True
        if self.starting_kongs_count == 5:
            self.kong_rando = False
        if self.kong_rando:
            if self.enable_plandomizer:
                # Filter out -1 from the plando dict (if it's there)
                self.starting_kong_list = [Kongs(kong) for kong in self.plandomizer_dict["plando_starting_kongs_selected"] if kong != -1]
                # If we chose to start with a random number of Kongs, we might have too many selected, remove any that aren't the starting Kong
                while len(self.starting_kong_list) > self.starting_kongs_count:
                    eligible_kongs_to_be_removed = [kong for kong in self.starting_kong_list if kong != self.starting_kong]
                    self.starting_kong_list.remove(self.random.choice(eligible_kongs_to_be_removed))
                # If we don't have enough Kongs selected by now, the plando validation means we'll always have "Random" as an option so we can fill with anything
                # That said, prioritize putting the chosen starting Kong
                if len(self.starting_kong_list) < self.starting_kongs_count and self.starting_kong != Kongs.any and self.starting_kong not in self.starting_kong_list:
                    self.starting_kong_list.append(self.starting_kong)
                # Otherwise fill with randoms until we have enough
                while len(self.starting_kong_list) < self.starting_kongs_count:
                    self.starting_kong_list.append(self.random.choice([kong for kong in kongs.copy() if kong not in self.starting_kong_list]))
                # If we don't care who is the starting Kong or if the starting Kong choice was invalid, pick a random starting Kong
                if self.starting_kong == Kongs.any or self.starting_kong not in self.starting_kong_list:
                    self.starting_kong = self.random.choice(self.starting_kong_list)
            else:
                # Randomly pick starting kong list and starting kong
                if self.starting_kong == Kongs.any:
                    self.starting_kong_list = self.random.sample(kongs, self.starting_kongs_count)
                    self.starting_kong = self.random.choice(self.starting_kong_list)
                # Randomly pick starting kongs but include chosen starting kong
                else:
                    possible_kong_list = kongs.copy()
                    possible_kong_list.remove(self.starting_kong)
                    self.starting_kong_list = self.random.sample(possible_kong_list, self.starting_kongs_count - 1)
                    self.starting_kong_list.append(self.starting_kong)
            # Kong freers are decided in the fill, set as any kong for now

            if self.shuffle_items and Types.Kong in self.shuffled_location_types:
                self.kong_locations = [
                    Locations.DiddyKong,
                    Locations.LankyKong,
                    Locations.TinyKong,
                    Locations.ChunkyKong,
                ]
            else:
                self.kong_locations = self.SelectKongLocations()
        else:
            possible_kong_list = kongs.copy()
            possible_kong_list.remove(0)
            self.starting_kong_list = self.random.sample(possible_kong_list, self.starting_kongs_count - 1)
            self.starting_kong_list.append(Kongs.donkey)
            self.starting_kong = Kongs.donkey
            # Set up kong locations with vanilla kongs in them, removing any kongs we start with
            self.kong_locations = [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong]
            if Kongs.diddy in self.starting_kong_list:
                self.kong_locations.remove(Locations.DiddyKong)
            if Kongs.lanky in self.starting_kong_list:
                self.kong_locations.remove(Locations.LankyKong)
            if Kongs.tiny in self.starting_kong_list:
                self.kong_locations.remove(Locations.TinyKong)
            if Kongs.chunky in self.starting_kong_list:
                self.kong_locations.remove(Locations.ChunkyKong)

        # Kongs needed for level progression
        if self.starting_kongs_count < 5 and self.shuffle_loading_zones in (ShuffleLoadingZones.levels, ShuffleLoadingZones.none) and self.logic_type not in (LogicType.nologic, LogicType.minimal):
            self.kongs_for_progression = True

        # Kasplat Rando
        self.kasplat_rando = False
        self.kasplat_location_rando = False
        if self.kasplat_rando_setting == KasplatRandoSetting.vanilla_locations:
            self.kasplat_rando = True
        if self.kasplat_rando_setting == KasplatRandoSetting.location_shuffle:
            self.kasplat_rando = True
            self.kasplat_location_rando = True

        # Force win_condition_spawns_ship based on win condition
        # Krool's Challenge always requires beating K. Rool
        if self.win_condition_item == WinConditionComplex.krools_challenge:
            self.win_condition_spawns_ship = 1
        # Kill the Rabbit cannot require beating K. Rool (would softlock)
        elif self.win_condition_item == WinConditionComplex.kill_the_rabbit:
            self.win_condition_spawns_ship = 0

        # Some settings (mostly win conditions) require modification of items in order to better generate the spoiler log
        if self.win_condition_item == WinConditionComplex.req_fairy or self.crown_door_item == BarrierItems.Fairy or self.coin_door_item == BarrierItems.Fairy:
            ItemList[Items.BananaFairy].playthrough = True
            ItemList[Items.FillerFairy].playthrough = True
        if self.win_condition_item == WinConditionComplex.req_rainbowcoin or self.crown_door_item == BarrierItems.RainbowCoin or self.coin_door_item == BarrierItems.RainbowCoin:
            ItemList[Items.RainbowCoin].playthrough = True
            ItemList[Items.FillerRainbowCoin].playthrough = True
        if self.win_condition_item == WinConditionComplex.req_bp or self.crown_door_item == BarrierItems.Blueprint or self.coin_door_item == BarrierItems.Blueprint:
            for item_index in ItemList:
                if ItemList[item_index].type == Types.Blueprint:
                    ItemList[item_index].playthrough = True
        if self.win_condition_item == WinConditionComplex.req_medal or self.crown_door_item == BarrierItems.Medal or self.coin_door_item == BarrierItems.Medal:
            ItemList[Items.BananaMedal].playthrough = True
            ItemList[Items.FillerMedal].playthrough = True
        if self.win_condition_item == WinConditionComplex.req_crown or self.crown_door_item == BarrierItems.Crown or self.coin_door_item == BarrierItems.Crown:
            ItemList[Items.BattleCrown].playthrough = True
            ItemList[Items.FillerCrown].playthrough = True
        if (
            self.win_condition_item == WinConditionComplex.req_bean
            or self.crown_door_item == BarrierItems.Bean
            or self.coin_door_item == BarrierItems.Bean
            or Types.Bean in self.shuffled_location_types
        ):
            ItemList[Items.Bean].playthrough = True
        if (
            self.win_condition_item == WinConditionComplex.req_pearl
            or self.crown_door_item == BarrierItems.Pearl
            or self.coin_door_item == BarrierItems.Pearl
            or Types.Pearl in self.shuffled_location_types
        ):
            ItemList[Items.Pearl].playthrough = True
            ItemList[Items.FillerPearl].playthrough = True

        self.free_trade_items = self.free_trade_setting
        self.free_trade_blueprints = self.free_trade_setting

        if IsDDMSSelected(self.misc_changes_selected, MiscChangesSelected.remove_wrinkly_puzzles):
            self.remove_wrinkly_puzzles = True

        # TODO: Rework this when minimal shops is implemented so it can take into account the starting move situation
        # Calculate the net balance of locations being added to the pool vs number of items being shuffled
        # Positive means we have more locations than items, negatives means we have more items than locations (very bad!)
        # The number is effectively (locations - items) so losing locations means we lower this value, losing items means we raise this value
        self.location_item_balance = 0
        if self.shuffle_items:
            if Types.Shop in self.shuffled_location_types:
                self.location_item_balance -= 34  # We're placing 34 shop items, but the number of locations varies by the number of shared shops. This forms the crux of how we use this balance.
            if self.starting_moves_count < 4:
                self.location_item_balance -= 4 - self.starting_moves_count  # We lose locations if we start with fewer than 4 moves
            elif self.starting_moves_count > 4:
                self.location_item_balance += self.starting_moves_count - 4  # We gain locations if we start with more than 4 moves
            if Types.Shockwave in self.shuffled_location_types and self.shockwave_status == ShockwaveStatus.shuffled_decoupled:
                self.location_item_balance -= 1  # If camera/shockwave is decoupled and shuffled, we gain one additional item
            self.location_item_balance += 8 - len(self.krool_keys_required)  # We don't have to place starting keys so we may lose items here
            # if Types.Kong in self.shuffled_location_types:
            #     self.location_item_balance -= 4  # Kong cages *can* be filled by Kongs, but nothing else. We'll treat these as lost locations in all worlds due to the rarity of this.
        # With some light algebra we get the maximum number of shared shops we can fill before we start running into fill problems
        shop_reduction = 4
        self.max_shared_shops = math.floor(25 - self.location_item_balance / -shop_reduction)
        if self.smaller_shops:
            shop_reduction = 2
            self.max_shared_shops = math.floor(30 - self.location_item_balance / -shop_reduction)
        self.snide_reward_rando = Types.BlueprintBanana in self.shuffled_location_types
        buffers = self.getPoolBuffer()
        if self.pool_index_with_shops is not None:
            self.max_shared_shops = min(self.max_shared_shops, int(buffers[self.pool_index_with_shops] / shop_reduction) - 2)  # Never have more shared shops than spaces allow
        self.max_shared_shops -= 1  # Subtract 1 shared shop for a little buffer. If we manage to solve the empty Helm fill issue then we can probably remove this line.
        self.placed_shared_shops = 0

        prog_hint_max = {
            ProgressiveHintItem.off: 0,
            ProgressiveHintItem.req_gb: self.total_gbs,
            ProgressiveHintItem.req_bp: 40,
            ProgressiveHintItem.req_key: 8,
            ProgressiveHintItem.req_medal: self.total_medals,
            ProgressiveHintItem.req_crown: self.total_crowns,
            ProgressiveHintItem.req_fairy: self.total_fairies,
            ProgressiveHintItem.req_rainbowcoin: self.total_rainbow_coins,
            ProgressiveHintItem.req_bean: 1,
            ProgressiveHintItem.req_pearl: self.total_pearls,
            ProgressiveHintItem.req_cb: 3500,
        }
        prog_max = prog_hint_max.get(self.progressive_hint_item, 0)
        if self.progressive_hint_count <= 0:
            # Disable progressive hints if hint text is 0, or less than 0
            self.progressive_hint_item = ProgressiveHintItem.off
        elif self.progressive_hint_count > prog_max:
            # Cap at prog max
            self.progressive_hint_count = prog_max

        self.excluded_bp_locations = []
        if Types.BlueprintBanana in self.shuffled_location_types and self.most_snide_rewards < 40:
            self.excluded_bp_locations = [Locations.TurnInJungleJapesDonkeyBlueprint + x for x in range(35)] + [Locations.TurnInDKIslesDonkeyBlueprint + x for x in range(5)]
            count_to_exclude = 40 - self.most_snide_rewards
            self.excluded_bp_locations = self.excluded_bp_locations[-count_to_exclude:]

        # Kong Model Mode Randomization
        if self.kong_model_mode == KongModelMode.none:
            self.kong_model_dk = KongModels.default
            self.kong_model_diddy = KongModels.default
            self.kong_model_lanky = KongModels.default
            self.kong_model_tiny = KongModels.default
            self.kong_model_chunky = KongModels.default

        if self.kong_model_mode == KongModelMode.random_one:
            random_krusha = self.random.randint(0, 4)
            kong_model_array = [KongModels.default, KongModels.default, KongModels.default, KongModels.default, KongModels.default]
            kong_model_array[random_krusha] = KongModels.krusha

            self.kong_model_dk = kong_model_array[0]
            self.kong_model_diddy = kong_model_array[1]
            self.kong_model_lanky = kong_model_array[2]
            self.kong_model_tiny = kong_model_array[3]
            self.kong_model_chunky = kong_model_array[4]

        elif self.kong_model_mode == KongModelMode.sometimes_one:
            random_krusha = self.random.randint(0, 4)
            kong_model_array = [KongModels.default, KongModels.default, KongModels.default, KongModels.default, KongModels.default]
            kong_model_array[random_krusha] = self.random.choice([KongModels.default, KongModels.krusha])

            self.kong_model_dk = kong_model_array[0]
            self.kong_model_diddy = kong_model_array[1]
            self.kong_model_lanky = kong_model_array[2]
            self.kong_model_tiny = kong_model_array[3]
            self.kong_model_chunky = kong_model_array[4]

        elif self.kong_model_mode == KongModelMode.random_all:
            kong_model_list = [KongModels.default, KongModels.krusha]

            self.kong_model_dk = self.random.choice(kong_model_list)
            self.kong_model_diddy = self.random.choice(kong_model_list)
            self.kong_model_lanky = self.random.choice(kong_model_list)
            self.kong_model_tiny = self.random.choice(kong_model_list)
            self.kong_model_chunky = self.random.choice(kong_model_list)

    def isBadIceTrapLocation(self, location: Locations):
        """Determine whether an ice trap is safe to house an ice trap outside of individual cases."""
        bad_fake_types = [Types.TrainingBarrel, Types.PreGivenMove, Types.Hint]
        is_bad = location.type in bad_fake_types
        if self.ice_traps_damage:
            if self.damage_amount in (DamageAmount.quad, DamageAmount.ohko) or self.perma_death or self.wipe_file_on_death:
                is_bad = location.type in bad_fake_types or (location.type == Types.Medal and location.level != Levels.HideoutHelm) or location.type == Types.Shockwave
        return is_bad

    def finalize_world_settings(self, spoiler):
        """Finalize the world state after settings initialization."""
        # Starting Region Randomization
        if self.random_starting_region_new != RandomStartingRegion.off:
            self.RandomizeStartingLocation(spoiler)
        self.shuffle_prices(spoiler)
        # Starting Move Location handling
        # Undo any damage that might leak between seeds
        spoiler.LocationList[Locations.IslesVinesTrainingBarrel].default = Items.Vines
        spoiler.LocationList[Locations.IslesVinesTrainingBarrel].type = Types.TrainingBarrel
        spoiler.LocationList[Locations.IslesSwimTrainingBarrel].default = Items.Swim
        spoiler.LocationList[Locations.IslesSwimTrainingBarrel].type = Types.TrainingBarrel
        spoiler.LocationList[Locations.IslesBarrelsTrainingBarrel].default = Items.Barrels
        spoiler.LocationList[Locations.IslesBarrelsTrainingBarrel].type = Types.TrainingBarrel
        spoiler.LocationList[Locations.IslesOrangesTrainingBarrel].default = Items.Oranges
        spoiler.LocationList[Locations.IslesOrangesTrainingBarrel].type = Types.TrainingBarrel
        # Always block PreGiven locations and only unblock them as we intentionally place moves there
        for location_id in TrainingBarrelLocations:
            spoiler.LocationList[location_id].inaccessible = True
        for location_id in PreGivenLocations:
            spoiler.LocationList[location_id].inaccessible = True

        if not IsItemSelected(self.cb_rando_enabled, self.cb_rando_list_selected, Levels.DKIsles):
            spoiler.LocationList[Locations.IslesDonkeyMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesDiddyMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesLankyMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesTinyMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesChunkyMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesDonkeyHalfMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesDiddyHalfMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesLankyHalfMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesTinyHalfMedal].inaccessible = True
            spoiler.LocationList[Locations.IslesChunkyHalfMedal].inaccessible = True

        for location_id in ProgressiveHintLocations:
            spoiler.LocationList[location_id].inaccessible = self.progressive_hint_item == ProgressiveHintItem.off

        if self.progressive_hint_item != ProgressiveHintItem.off and not (Types.Hint in self.shuffled_location_types):
            for location_id in WrinklyHintLocations:
                spoiler.LocationList[location_id].inaccessible = True

        if self.climbing_status == ClimbingStatus.shuffled:
            spoiler.LocationList[Locations.IslesClimbing].inaccessible = True

        # Smaller shop setting blocks 2 Kong-specific locations from each shop randomly but is only valid if item rando is on and includes shops
        if self.smaller_shops and self.shuffle_items and Types.Shop in self.shuffled_location_types:
            # To evenly distribute the locations blocked, we can use the fact there are 20 shops to our advantage
            # These evenly distributed pairs will represent "locations to block" for each shop
            kongPairs = [
                (Kongs.donkey, Kongs.diddy),
                (Kongs.donkey, Kongs.diddy),
                (Kongs.donkey, Kongs.lanky),
                (Kongs.donkey, Kongs.lanky),
                (Kongs.donkey, Kongs.tiny),
                (Kongs.donkey, Kongs.tiny),
                (Kongs.donkey, Kongs.chunky),
                (Kongs.donkey, Kongs.chunky),
                (Kongs.diddy, Kongs.lanky),
                (Kongs.diddy, Kongs.lanky),
                (Kongs.diddy, Kongs.tiny),
                (Kongs.diddy, Kongs.tiny),
                (Kongs.diddy, Kongs.chunky),
                (Kongs.diddy, Kongs.chunky),
                (Kongs.lanky, Kongs.tiny),
                (Kongs.lanky, Kongs.tiny),
                (Kongs.lanky, Kongs.chunky),
                (Kongs.lanky, Kongs.chunky),
                (Kongs.tiny, Kongs.chunky),
                (Kongs.tiny, Kongs.chunky),
            ]
            self.random.shuffle(kongPairs)  # Shuffle this list so we don't block the same locations every time

            # First we identify the locations we need to remove and make them inaccessible
            for level in ShopLocationReference:
                for vendor in ShopLocationReference[level]:
                    # For each shop, get a pair of kongs
                    kongsToBeRemoved = kongPairs.pop()
                    # Determine which shop locations are accessible and inaccessible
                    inaccessible_shops = [
                        ShopLocationReference[level][vendor][kongsToBeRemoved[0]],
                        ShopLocationReference[level][vendor][kongsToBeRemoved[1]],
                    ]
                    accessible_shops = [location_id for location_id in ShopLocationReference[level][vendor] if location_id not in inaccessible_shops]
                    for location_id in inaccessible_shops:
                        spoiler.LocationList[location_id].inaccessible = True
                        spoiler.LocationList[location_id].smallerShopsInaccessible = True
                    for location_id in accessible_shops:
                        spoiler.LocationList[location_id].inaccessible = False
                        spoiler.LocationList[location_id].smallerShopsInaccessible = False

        if Types.Cranky in self.shuffled_location_types:
            spoiler.LocationList[Locations.ShopOwner_Location00].inaccessible = True
        if Types.Funky in self.shuffled_location_types:
            spoiler.LocationList[Locations.ShopOwner_Location01].inaccessible = True
        if Types.Candy in self.shuffled_location_types:
            spoiler.LocationList[Locations.ShopOwner_Location02].inaccessible = True
        if Types.Snide in self.shuffled_location_types:
            spoiler.LocationList[Locations.ShopOwner_Location03].inaccessible = True

        # Designate the Rock GB as a location for the starting kong
        spoiler.LocationList[Locations.IslesDonkeyJapesRock].kong = self.starting_kong
        if IsDDMSSelected(self.faster_checks_selected, FasterChecksSelected.factory_arcade_round_1):
            # On Fast GBs, this location refers to the blast course, not the arcade
            spoiler.LocationList[Locations.FactoryDonkeyDKArcade].name = "Factory Donkey Blast Course"

    def update_valid_locations(self, spoiler):
        """Calculate (or recalculate) valid locations for items by type."""
        self.valid_locations = {}
        self.valid_locations[Types.Kong] = self.kong_locations.copy()
        if self.shuffle_items and any(self.shuffled_location_types):
            # All shuffled locations are valid except for Kong locations (the Kong inside the cage, not the GB) and Shop Owner Locations - those can only be Kongs and Shop Owners respectively
            shuffledLocations = [
                location
                for location in spoiler.LocationList
                if spoiler.LocationList[location].type in self.shuffled_location_types and spoiler.LocationList[location].type not in (Types.Cranky, Types.Funky, Types.Candy, Types.Snide)
            ]
            shuffledLocationsShopOwner = [
                location
                for location in shuffledLocations  # Placing a shop owner in a shop owner location is boring and we don't want to do it ever
                if spoiler.LocationList[location].type
                not in (
                    Types.Shop,
                    Types.Shockwave,
                    Types.PreGivenMove,
                    Types.TrainingBarrel,
                    Types.Climbing,
                )
            ]
            shuffledNonMoveLocations = [location for location in shuffledLocations if spoiler.LocationList[location].type != Types.PreGivenMove]
            fairyBannedLocations = [location for location in shuffledNonMoveLocations if spoiler.LocationList[location].type != Types.Fairy]
            if Types.Shop in self.shuffled_location_types:
                self.valid_locations[Types.Shop] = {}
                # Cross-kong acquisition is assumed in full item rando, calculate the list of all Kong-specific shops
                allKongMoveLocations = DonkeyMoveLocations.copy()
                allKongMoveLocations.update(DiddyMoveLocations.copy())
                allKongMoveLocations.update(TinyMoveLocations.copy())
                allKongMoveLocations.update(ChunkyMoveLocations.copy())
                allKongMoveLocations.update(LankyMoveLocations.copy())
                # Generate a list of all valid locations EXCEPT the Kong-specific shops - these are valid locations for shared moves
                locations_excluding_kong_shops = [location for location in shuffledLocations if location not in allKongMoveLocations]
                # Shockwave and Training Barrels can only be shuffled if shops are shuffled and their valid locations are non-Kong-specific shops
                if Types.Shockwave in self.shuffled_location_types:
                    locations_excluding_kong_shops.append(Locations.CameraAndShockwave)
                    self.valid_locations[Types.Shockwave] = locations_excluding_kong_shops.copy()
                if Types.TrainingBarrel in self.shuffled_location_types or self.training_barrels != TrainingBarrels.normal:
                    self.valid_locations[Types.TrainingBarrel] = locations_excluding_kong_shops.copy()
                if Types.Climbing in self.shuffled_location_types:
                    self.valid_locations[Types.Climbing] = locations_excluding_kong_shops.copy()
                self.valid_locations[Types.Shop][Kongs.any] = locations_excluding_kong_shops.copy()
                # Kong-specific moves can go in any non-shared shop location
                locations_excluding_shared_shops = [location for location in shuffledLocations if location not in SharedShopLocations]
                self.valid_locations[Types.Shop][Kongs.donkey] = locations_excluding_shared_shops.copy()
                self.valid_locations[Types.Shop][Kongs.diddy] = locations_excluding_shared_shops.copy()
                self.valid_locations[Types.Shop][Kongs.lanky] = locations_excluding_shared_shops.copy()
                self.valid_locations[Types.Shop][Kongs.tiny] = locations_excluding_shared_shops.copy()
                self.valid_locations[Types.Shop][Kongs.chunky] = locations_excluding_shared_shops.copy()
            if Types.Blueprint in self.shuffled_location_types:
                # Blueprints are banned from Key, Crown, Fairy and Rainbow Coin Locations
                badBlueprintTypes = [
                    Types.Crown,
                    Types.Key,
                    Types.Fairy,
                    Types.RainbowCoin,
                    Types.Kong,
                ]
                badBlueprintLocations = [
                    Locations.IslesDonkeyJapesRock,
                ]
                if self.free_trade_setting:
                    badBlueprintTypes = [Types.Fairy]
                    badBlueprintLocations = []
                badBlueprintLocations.extend([Locations.TurnInDKIslesDonkeyBlueprint + x for x in range(40)])  # Don't allow blueprints on snide rewards... very bad idea
                badBlueprintLocations.extend(SharedShopLocations)  # Blueprints in shared shops plays poorly with the fill and in practice
                blueprintValidTypes = [typ for typ in self.shuffled_location_types if typ not in badBlueprintTypes]

                # These locations do not have a set Kong assigned to them and can't have blueprints
                blueprintLocations = [location for location in shuffledNonMoveLocations if location not in badBlueprintLocations and spoiler.LocationList[location].type in blueprintValidTypes]
                self.valid_locations[Types.Blueprint] = {}
                for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]:
                    if self.free_trade_setting:
                        self.valid_locations[Types.Blueprint][kong] = [location for location in blueprintLocations if spoiler.LocationList[location].kong in (kong, Kongs.any)]
                    else:
                        self.valid_locations[Types.Blueprint][kong] = [location for location in blueprintLocations if spoiler.LocationList[location].kong == kong]
            banana_types = [
                Types.Banana,
                Types.RaceBanana,
                Types.GauntletBanana,
                Types.BlueprintBanana,
            ]
            has_banana = False
            for btype in banana_types:
                if btype in self.shuffled_location_types:
                    has_banana = True
            if has_banana:
                self.valid_locations[Types.Banana] = [location for location in shuffledNonMoveLocations]
            if Types.FillerBanana in self.shuffled_location_types:
                self.valid_locations[Types.FillerBanana] = [location for location in shuffledNonMoveLocations]
            regular_items = (
                Types.Crown,
                Types.Key,
                Types.NintendoCoin,
                Types.RarewareCoin,
                Types.Pearl,
                Types.Bean,
                Types.Fairy,
                Types.FillerCrown,
                Types.FillerFairy,
                Types.FillerPearl,
            )
            for item in regular_items:
                if item in self.shuffled_location_types:
                    self.valid_locations[item] = shuffledNonMoveLocations.copy()
            if Types.Hint in self.shuffled_location_types:
                self.valid_locations[Types.Hint] = [location for location in shuffledNonMoveLocations if spoiler.LocationList[location].level != Levels.HideoutHelm]
            for item in (Types.Medal, Types.FillerMedal):
                if item in self.shuffled_location_types:
                    self.valid_locations[item] = fairyBannedLocations.copy()
            shop_owner_items = (Types.Cranky, Types.Candy, Types.Funky)
            for item in shop_owner_items:
                if item in self.shuffled_location_types:
                    self.valid_locations[item] = shuffledLocationsShopOwner.copy()
            if Types.Snide in self.shuffled_location_types:
                # Snide can't be placed in/after expected Helm Access. To help out fill, we'll ban Snide from any locations in Helm
                self.valid_locations[Types.Snide] = [x for x in shuffledLocationsShopOwner.copy() if spoiler.LocationList[x].level != Levels.HideoutHelm]
            for item in (Types.RainbowCoin, Types.FillerRainbowCoin):
                if item in self.shuffled_location_types:
                    self.valid_locations[item] = [
                        x for x in shuffledNonMoveLocations if spoiler.LocationList[x].type not in (Types.Shop, Types.TrainingBarrel, Types.Shockwave, Types.PreGivenMove, Types.Climbing)
                    ]
            if Types.FakeItem in self.shuffled_location_types:
                bad_fake_locations = (
                    # Miscellaneous issues
                    Locations.NintendoCoin,
                    Locations.RarewareCoin,
                    # Caves Beetle Race causes issues with a blueprint potentially being there
                    Locations.CavesLankyBeetleRace,
                    # Stuff that may be required to access other stuff - Not really fair
                    Locations.JapesDonkeyFreeDiddy,
                    Locations.JapesDonkeyFrontofCage,
                    Locations.IslesDonkeyJapesRock,
                    Locations.FactoryDonkeyDKArcade,
                    Locations.FactoryTinyDartboard,
                    Locations.JapesLankyFairyCave,
                    Locations.AztecLankyVulture,
                    Locations.AztecDiddyRamGongs,
                    Locations.ForestDiddyRafters,
                    Locations.CavesTiny5DoorIgloo,
                    Locations.CavesDiddy5DoorCabinUpper,
                    Locations.CavesTinyCaveBarrel,
                    Locations.CastleDonkeyTree,
                    Locations.CastleLankyGreenhouse,
                    # Messes with the ice trap audio
                    Locations.HelmBananaFairy1,
                    Locations.HelmBananaFairy2,
                    # Snide Rewards
                    Locations.TurnInDKIslesDonkeyBlueprint,
                    Locations.TurnInDKIslesDiddyBlueprint,
                    Locations.TurnInDKIslesLankyBlueprint,
                    Locations.TurnInDKIslesTinyBlueprint,
                    Locations.TurnInDKIslesChunkyBlueprint,
                    Locations.TurnInJungleJapesDonkeyBlueprint,
                    Locations.TurnInJungleJapesDiddyBlueprint,
                    Locations.TurnInJungleJapesLankyBlueprint,
                    Locations.TurnInJungleJapesTinyBlueprint,
                    Locations.TurnInJungleJapesChunkyBlueprint,
                    Locations.TurnInAngryAztecDonkeyBlueprint,
                    Locations.TurnInAngryAztecDiddyBlueprint,
                    Locations.TurnInAngryAztecLankyBlueprint,
                    Locations.TurnInAngryAztecTinyBlueprint,
                    Locations.TurnInAngryAztecChunkyBlueprint,
                    Locations.TurnInFranticFactoryDonkeyBlueprint,
                    Locations.TurnInFranticFactoryDiddyBlueprint,
                    Locations.TurnInFranticFactoryLankyBlueprint,
                    Locations.TurnInFranticFactoryTinyBlueprint,
                    Locations.TurnInFranticFactoryChunkyBlueprint,
                    Locations.TurnInGloomyGalleonDonkeyBlueprint,
                    Locations.TurnInGloomyGalleonDiddyBlueprint,
                    Locations.TurnInGloomyGalleonLankyBlueprint,
                    Locations.TurnInGloomyGalleonTinyBlueprint,
                    Locations.TurnInGloomyGalleonChunkyBlueprint,
                    Locations.TurnInFungiForestDonkeyBlueprint,
                    Locations.TurnInFungiForestDiddyBlueprint,
                    Locations.TurnInFungiForestLankyBlueprint,
                    Locations.TurnInFungiForestTinyBlueprint,
                    Locations.TurnInFungiForestChunkyBlueprint,
                    Locations.TurnInCrystalCavesDonkeyBlueprint,
                    Locations.TurnInCrystalCavesDiddyBlueprint,
                    Locations.TurnInCrystalCavesLankyBlueprint,
                    Locations.TurnInCrystalCavesTinyBlueprint,
                    Locations.TurnInCrystalCavesChunkyBlueprint,
                    Locations.TurnInCreepyCastleDonkeyBlueprint,
                    Locations.TurnInCreepyCastleDiddyBlueprint,
                    Locations.TurnInCreepyCastleLankyBlueprint,
                    Locations.TurnInCreepyCastleTinyBlueprint,
                    Locations.TurnInCreepyCastleChunkyBlueprint,
                )
                self.valid_locations[Types.FakeItem] = [x for x in shuffledNonMoveLocations if not self.isBadIceTrapLocation(spoiler.LocationList[x]) and x not in bad_fake_locations]
            if Types.JunkItem in self.shuffled_location_types:
                self.valid_locations[Types.JunkItem] = [
                    x
                    for x in shuffledNonMoveLocations
                    if spoiler.LocationList[x].type
                    not in (
                        Types.Shop,
                        Types.Shockwave,
                        Types.Crown,
                        Types.PreGivenMove,
                        Types.CrateItem,
                        Types.BoulderItem,
                        Types.Enemies,
                    )
                    and (spoiler.LocationList[x].type != Types.Key or spoiler.LocationList[x].level == Levels.HideoutHelm)
                ]
            if Types.Kong in self.shuffled_location_types:
                # Banned because it defeats the purpose of starting with X Kongs
                banned_kong_locations = (
                    Locations.IslesSwimTrainingBarrel,
                    Locations.IslesVinesTrainingBarrel,
                    Locations.IslesBarrelsTrainingBarrel,
                    Locations.IslesOrangesTrainingBarrel,
                    Locations.IslesDonkeyJapesRock,
                )
                self.valid_locations[Types.Kong].extend(
                    [loc for loc in shuffledNonMoveLocations if loc not in banned_kong_locations]
                )  # No items can be in Kong cages but Kongs can be in all other locations

            # If our Helm fairy locations are unshuffled, ban any item used for helm doors from being on either location.
            # This is because the two locations are always behind both doors. If you put a door-required crown here, you may as well have deleted it.
            if not self.random_fairies and Types.Fairy in self.shuffled_location_types:
                # Going in order of the HelmDoorItem enum:
                # GBs cannot be in Helm
                # Blueprints cannot be on fairies
                # Company coins cannot be on fairies
                # Keys can be on fairies, but this is staggeringly rare
                if Types.Key in self.shuffled_location_types and (self.crown_door_item == BarrierItems.Key or self.coin_door_item == BarrierItems.Key):
                    self.valid_locations[Types.Key].remove(Locations.HelmBananaFairy1)
                    self.valid_locations[Types.Key].remove(Locations.HelmBananaFairy2)
                # Medals cannot be on fairies
                # The big winner: Crowns will not be locked behind a crown door requirement
                if Types.Crown in self.shuffled_location_types and (self.crown_door_item == BarrierItems.Crown or self.coin_door_item == BarrierItems.Crown):
                    self.valid_locations[Types.Crown].remove(Locations.HelmBananaFairy1)
                    self.valid_locations[Types.Crown].remove(Locations.HelmBananaFairy2)
                # Fairies are the one exception: these are allowed to be vanilla
                # Rainbow coins cannot be on fairies
                # The Bean/Pearls cannot be on fairies (you might be sensing a pattern here)

            # Invert allowances for restrictions
            inverted_allowances = {}
            for item_type in self.shuffled_check_allowances:
                for k in self.shuffled_check_allowances[item_type]:
                    if k not in inverted_allowances:
                        inverted_allowances[k] = []
                    inverted_allowances[k].append(item_type)
            for item_type in inverted_allowances:
                inverted_allowances[item_type] = list(set(inverted_allowances[item_type]))
            race_gb_locations = [
                Locations.JapesDiddyMinecarts,
                Locations.AztecDiddyVultureRace,
                Locations.AztecTinyBeetleRace,
                Locations.FactoryTinyCarRace,
                Locations.GalleonDonkeySealRace,
                Locations.ForestDiddyOwlRace,
                Locations.ForestLankyRabbitRace,
                Locations.ForestChunkyMinecarts,
                Locations.CavesLankyBeetleRace,
                Locations.CastleDonkeyMinecarts,
                Locations.CastleTinyCarRace,
            ]
            gauntlet_gb_locations = [
                Locations.JapesLankyFairyCave,
                Locations.AztecTinyKlaptrapRoom,
                Locations.AztecChunkyKlaptrapRoom,
                Locations.FactoryDiddyRandD,
                Locations.ForestLankyAttic,
                Locations.ForestTinyAnthill,
                Locations.ForestTinySpiderBoss,
                Locations.ForestChunkyApple,
                Locations.CavesDonkey5DoorCabin,
                Locations.CavesDiddy5DoorCabinLower,
                Locations.CavesLanky5DoorIgloo,
                Locations.CavesTiny5DoorCabin,
                Locations.CavesChunky5DoorIgloo,
                Locations.CastleDonkeyLibrary,
                Locations.CastleTinyTrashCan,
                Locations.CastleChunkyShed,
            ]
            blueprint_gb_locations = [Locations.TurnInDKIslesDonkeyBlueprint + x for x in range(40)]
            banana_types = {
                Types.Banana: [
                    x
                    for x in spoiler.LocationList
                    if spoiler.LocationList[x].type == Types.Banana and x not in race_gb_locations and x not in gauntlet_gb_locations and x not in blueprint_gb_locations
                ],
                Types.RaceBanana: race_gb_locations.copy(),
                Types.GauntletBanana: gauntlet_gb_locations.copy(),
                Types.BlueprintBanana: blueprint_gb_locations.copy(),
            }
            for item_type in self.valid_locations:
                if item_type in inverted_allowances:
                    valid_allowance_types = inverted_allowances[item_type].copy()
                    valid_locations_lambda_list = [
                        lambda l, _: l.type in valid_allowance_types,
                    ]
                    valid_locations_lambda = lambda l, _: l.type in valid_allowance_types
                    # Banana
                    valid_banana_locations = []
                    for btype in banana_types:
                        if btype in valid_allowance_types:
                            valid_allowance_types.remove(btype)
                            valid_banana_locations.extend(banana_types[btype])
                    valid_locations_lambda_list.append(lambda _, v: v in valid_banana_locations)
                    # Medal
                    if Types.HelmMedal in valid_allowance_types and Types.Medal not in valid_allowance_types:
                        valid_allowance_types.remove(Types.HelmMedal)
                        valid_locations_lambda_list.append(lambda l, _: l.type == Types.Medal and l.level == Levels.HideoutHelm)
                    elif Types.Medal in valid_allowance_types and Types.HelmMedal not in valid_allowance_types:
                        valid_allowance_types.remove(Types.Medal)
                        valid_locations_lambda_list.append(lambda l, _: l.type == Types.Medal and l.level != Levels.HideoutHelm)
                    # Key
                    if Types.HelmKey in valid_allowance_types and Types.Key not in valid_allowance_types:
                        valid_allowance_types.remove(Types.HelmKey)
                        valid_locations_lambda_list.append(lambda l, _: l.type == Types.Key and l.level == Levels.HideoutHelm)
                    elif Types.Key in valid_allowance_types and Types.HelmKey not in valid_allowance_types:
                        valid_allowance_types.remove(Types.Key)
                        valid_locations_lambda_list.append(lambda l, _: l.type == Types.Key and l.level != Levels.HideoutHelm)
                    valid_locations_lambda = lambda l, v: any(f(l, v) for f in valid_locations_lambda_list)
                    if item_type in [Types.Shop, Types.Blueprint]:  # kong-based
                        for kong in self.valid_locations[item_type]:
                            self.valid_locations[item_type][kong] = [v for v in self.valid_locations[item_type][kong] if valid_locations_lambda(spoiler.LocationList[v], v)]
                    else:
                        self.valid_locations[item_type] = [v for v in self.valid_locations[item_type] if valid_locations_lambda(spoiler.LocationList[v], v)]

    def GetValidLocationsForItem(self, item_id):
        """Return the valid locations the input item id can be placed in."""
        item_obj = ItemList[item_id]
        valid_locations = []
        # Some types of items have restrictions on valid locations based on their kong
        if item_obj.type in (Types.Shop, Types.Blueprint):
            valid_locations = self.valid_locations[item_obj.type][item_obj.kong]
        else:
            valid_locations = self.valid_locations[item_obj.type]
        return valid_locations

    def SelectKongLocations(self):
        """Select which random kong locations to use depending on number of starting kongs."""
        # First determine which kong cages will have a kong to free
        kongCageLocations = [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong]
        # Randomly decide which kong cages will not have kongs in them
        for i in range(0, self.starting_kongs_count - 1):
            kongLocation = self.random.choice(kongCageLocations)
            kongCageLocations.remove(kongLocation)

        # The following cases do not apply if you could bypass the Guitar door without Diddy
        bypass_guitar_door = IsDDMSSelected(self.remove_barriers_selected, RemovedBarriersSelected.aztec_tunnel_door) or self.activate_all_bananaports == ActivateAllBananaports.all
        # In case both Diddy and Chunky need to be freed but only Aztec locations are available
        # This would be impossible, as one of them must free the Tiny location and Diddy is needed for the Lanky location
        if (
            not bypass_guitar_door
            and self.starting_kongs_count == 3
            and Kongs.diddy not in self.starting_kong_list
            and Kongs.chunky not in self.starting_kong_list
            and Locations.TinyKong in kongCageLocations
            and Locations.LankyKong in kongCageLocations
        ):
            # Move a random location to a non-Aztec location
            kongCageLocations.pop()
            kongCageLocations.append(self.random.choice([Locations.DiddyKong, Locations.ChunkyKong]))
        # In case Diddy is the only kong to free, he can't be in the Llama Temple since it's behind the Guitar door
        if not bypass_guitar_door and self.starting_kongs_count == 4 and Kongs.diddy not in self.starting_kong_list and Locations.LankyKong in kongCageLocations:
            # Move diddy kong from llama temple to another cage randomly chosen
            kongCageLocations.remove(Locations.LankyKong)
            kongCageLocations.append(self.random.choice([Locations.DiddyKong, Locations.TinyKong, Locations.ChunkyKong]))
        return kongCageLocations

    def RandomizeStartingLocation(self, spoiler):
        """Randomize the starting point of this seed."""
        if self.random_starting_region_new == RandomStartingRegion.isles_only:
            region_data = [
                randomizer.LogicFiles.DKIsles.LogicRegions,
            ]
        else:
            region_data = [
                randomizer.LogicFiles.DKIsles.LogicRegions,
                randomizer.LogicFiles.JungleJapes.LogicRegions,
                randomizer.LogicFiles.AngryAztec.LogicRegions,
                randomizer.LogicFiles.FranticFactory.LogicRegions,
                randomizer.LogicFiles.GloomyGalleon.LogicRegions,
                randomizer.LogicFiles.FungiForest.LogicRegions,
                randomizer.LogicFiles.CrystalCaves.LogicRegions,
                randomizer.LogicFiles.CreepyCastle.LogicRegions,
            ]
        selected_region_world = self.random.choice(region_data)
        valid_starting_regions = []
        banned_starting_regions = []
        if self.damage_amount in (DamageAmount.quad, DamageAmount.ohko):
            banned_starting_regions.append(Regions.KremIsleMouth)
        if self.enable_plandomizer and self.plandomizer_dict["plando_starting_exit"] != -1:
            # Plandomizer code for random starting location
            planned_transition = self.plandomizer_dict["plando_starting_exit"]
            region = ShufflableExits[planned_transition].back.regionId
            planned_back_transition = ShufflableExits[planned_transition].back
            region_name = ""
            for data in region_data:
                if region in data.keys():
                    region_name = data[region].name
            if region_name == "":
                raise Ex.PlandoIncompatibleException(f"No region found for {planned_transition}")
            if region in RegionMapList:
                tied_map = GetMapId(self, region)
                tied_exit = GetExitId(planned_back_transition)
                valid_starting_regions.append(
                    {
                        "region": region,
                        "map": tied_map,
                        "exit": tied_exit,
                        "region_name": region_name,
                        "exit_name": ShufflableExits[planned_transition].back.name,
                    }
                )
            else:
                raise Ex.PlandoIncompatibleException(f"Starting position {planned_transition} has no map")
        else:
            for region in selected_region_world:
                region_data = selected_region_world[region]
                transitions = [
                    x.exitShuffleId
                    for x in region_data.exits
                    if x.exitShuffleId is not None and x.exitShuffleId in ShufflableExits and ShufflableExits[x.exitShuffleId].back.reverse is not None and not x.isGlitchTransition
                ]
                if region in RegionMapList:
                    # Has tied map
                    tied_map = GetMapId(self, region)
                    if self.random_starting_region_new == RandomStartingRegion.isles_only:
                        if tied_map != Maps.Isles:
                            continue
                    for transition in transitions:
                        relevant_transition = ShufflableExits[transition].back.reverse
                        tied_exit = GetExitId(ShufflableExits[relevant_transition].back)
                        if tied_exit == 11 and tied_map == Maps.Isles:
                            # Castle Lobby exit: Big nono
                            continue
                        valid_starting_regions.append(
                            {
                                "region": region,
                                "map": tied_map,
                                "exit": tied_exit,
                                "region_name": region_data.name,
                                "exit_name": ShufflableExits[relevant_transition].back.name,
                            }
                        )
        if any(banned_starting_regions):
            valid_starting_regions = [region for region in valid_starting_regions if region["region"] not in banned_starting_regions]
            # The only way for this to happen is if someone plandos a settings-banned region as their starting region
            if len(valid_starting_regions) == 0:
                raise Ex.PlandoIncompatibleException("Planned starting region is invalid.")
        self.starting_region = self.random.choice(valid_starting_regions)
        for x in range(2):
            spoiler.RegionList[Regions.GameStart].exits[x + 1].dest = self.starting_region["region"]

    def ApplyPlandomizerSettings(self):
        """Apply settings specified by the plandomizer."""
        self.plandomizer_dict = self.plandomizer_data
        # Leaving space here to handle things as needed, might be unnecessary

    def ApplyMusicSelections(self):
        """Apply user-selected songs."""
        self.music_selection_dict = json.loads(self.music_selections)
        # Determine which categories have songs selected.
        for song_enum, song in song_data.items():
            song_str = str(song_enum.value)
            if song_str in self.music_selection_dict["vanilla"] or song_str in self.music_selection_dict["custom"]:
                if song.type == SongType.BGM:
                    self.bgm_songs_selected = True
                elif song.type == SongType.MajorItem:
                    self.majoritems_songs_selected = True
                elif song.type == SongType.MinorItem:
                    self.minoritems_songs_selected = True
                elif song.type == SongType.Event:
                    self.events_songs_selected = True

    def getPoolBuffer(self):
        """Get the item and check counts for each pool."""
        if self.smaller_shops:
            self.item_check_counts[ItemRandoListSelected.shop] = [0, 60]
        if IsItemSelected(self.cb_rando_enabled, self.cb_rando_list_selected, Levels.DKIsles):
            self.item_check_counts[ItemRandoListSelected.medal_checks] = [0, 40]
        self.item_check_counts[ItemRandoListSelected.kong][0] = 5 - len(self.starting_kong_list)
        self.item_check_counts[ItemRandoListSelected.shopowners][0] = 0  # Reset it back to a default state every time
        if Types.Cranky in self.shuffled_location_types:
            self.item_check_counts[ItemRandoListSelected.shopowners][0] += 1
        if Types.Funky in self.shuffled_location_types:
            self.item_check_counts[ItemRandoListSelected.shopowners][0] += 1
        if Types.Candy in self.shuffled_location_types:
            self.item_check_counts[ItemRandoListSelected.shopowners][0] += 1
        if Types.Snide in self.shuffled_location_types:
            self.item_check_counts[ItemRandoListSelected.shopowners][0] += 1
        self.item_check_counts[ItemRandoListSelected.medal][0] = self.total_medals
        self.item_check_counts[ItemRandoListSelected.banana][0] = self.total_gbs - 40  # Blueprint GBs are their own category for item pool calculations
        self.item_check_counts[ItemRandoListSelected.fairy][0] = self.total_fairies
        self.item_check_counts[ItemRandoListSelected.rainbowcoin][0] = self.total_rainbow_coins
        self.item_check_counts[ItemRandoListSelected.crown][0] = self.total_crowns
        self.item_check_counts[ItemRandoListSelected.pearl][0] = self.total_pearls
        self.item_check_counts[ItemRandoListSelected.blueprintbanana][0] = self.most_snide_rewards
        self.item_check_counts[ItemRandoListSelected.sniderewards][1] = self.most_snide_rewards
        misc_banana_mapping = {
            Types.RaceBanana: ItemRandoListSelected.racebanana,
            Types.GauntletBanana: ItemRandoListSelected.gauntletbanana,
        }
        for item_type, list_type in misc_banana_mapping.items():
            if item_type not in self.shuffled_location_types:
                self.item_check_counts[ItemRandoListSelected.banana][0] -= self.item_check_counts[list_type][1]
        buffers = []
        for x in range(4):
            item_count = 0
            check_count = 0
            for item_selector in self.item_search[x]:
                item_count += self.item_check_counts[item_selector][0]
            for check_selector in self.check_search[x]:
                check_count += self.item_check_counts[check_selector][1]
                if check_selector == ItemRandoListSelected.shop:
                    self.pool_index_with_shops = x
            buffers.append(check_count - item_count)
        return buffers

    def is_valid_item_pool(self):
        """Confirm that the item pool is a valid combination of items. Must be run after valid locations are calculated without any restrictions."""
        if Types.Cranky in self.shuffled_location_types:
            if len(self.valid_locations[Types.Cranky]) <= 0:
                return False
        if Types.Funky in self.shuffled_location_types:
            if len(self.valid_locations[Types.Funky]) <= 0:
                return False
        if Types.Candy in self.shuffled_location_types:
            if len(self.valid_locations[Types.Candy]) <= 0:
                return False
        if Types.Snide in self.shuffled_location_types:
            if len(self.valid_locations[Types.Snide]) <= 0:
                return False

        def check_distribution(liquids, buckets):
            pool_count = 4
            pool_valid = [True] * pool_count
            pool_verified = [False] * pool_count
            pool_liquids = [0] * pool_count
            pool_buckets = [0] * pool_count
            lq_copy = liquids.copy()
            bk_copy = buckets.copy()
            iter_count = 100
            ran_rules = []
            while True:
                # Rule 1:
                # Any pools which only have checks or only have items should get filtered out
                # if their non-filtered version has more than 0 items.
                # This can only be ran once.
                if 1 not in ran_rules:
                    has_liquids = [False] * pool_count
                    has_buckets = [False] * pool_count
                    for lq in lq_copy:
                        for pl in lq["pools"]:
                            has_liquids[pl] = True
                    for bk in bk_copy:
                        for pl in bk["pools"]:
                            has_buckets[pl] = True
                    pools_to_filter = []
                    for x in range(pool_count):
                        if not has_buckets[x] or not has_liquids[x]:
                            pools_to_filter.append(x)
                    for pl in pools_to_filter:
                        for lq in lq_copy:
                            if pl in lq["pools"]:
                                filtered_version = [x for x in lq["pools"] if x not in pools_to_filter]
                                if len(filtered_version) > 0:
                                    lq["pools"] = filtered_version.copy()
                                else:
                                    pool_valid[pl] = False
                                    pool_verified[pl] = True
                        for bk in bk_copy:
                            if pl in bk["pools"]:
                                filtered_version = [x for x in bk["pools"] if x not in pools_to_filter]
                                if len(filtered_version) > 0:
                                    bk["pools"] = filtered_version.copy()
                    ran_rules.append(1)
                # Rule 2:
                # Any completely empty pools should add all of their items/checks in them
                # Any pools with greater amounts of items than checks gets flagged as invalid.
                found_lq = [False] * pool_count
                found_bk = [False] * pool_count
                for lq in lq_copy:
                    for pl in lq["pools"]:
                        found_lq[pl] = True
                for bk in bk_copy:
                    for pl in bk["pools"]:
                        found_bk[pl] = True
                for x in range(pool_count):
                    if not found_lq[x] and not found_bk[x]:
                        if pool_buckets[x] < pool_liquids[x]:
                            pool_valid[x] = False
                            pool_verified[x] = True
                #  Rule 3:
                # Any items/checks which are only part of 1 pool should get filtered out and applied to a guaranteed liq/buck total
                temp_lq = []
                for lq in lq_copy:
                    if len(lq["pools"]) == 1:
                        pool_liquids[lq["pools"][0]] += lq["size"]
                    else:
                        temp_lq.append(lq)
                lq_copy = temp_lq.copy()
                temp_bk = []
                for bk in bk_copy:
                    if len(bk["pools"]) == 1:
                        pool_buckets[bk["pools"][0]] += bk["size"]
                    else:
                        temp_bk.append(bk)
                bk_copy_largest_to_smallest = temp_bk.copy()
                bk_copy_largest_to_smallest.sort(key=lambda x: x["size"], reverse=True)
                # Rule 4:
                # For all remaining buckets, check the pools which need the checks the most
                bucket_deficit = [x - pool_buckets[xi] for xi, x in enumerate(pool_liquids)]
                temp_bk = []
                for bk in bk_copy_largest_to_smallest:
                    remove = False
                    bucket_needed = None
                    bucket_deficit_needed = None
                    for pl in bk["pools"]:
                        if bucket_deficit[pl] >= 0:
                            if bucket_needed is None or bucket_deficit[pl] > bucket_deficit_needed:
                                bucket_needed = pl
                                bucket_deficit_needed = bucket_deficit[pl]
                    if bucket_needed is not None:
                        bucket_capacity_supplied = min(bucket_deficit_needed, bk["size"])
                        bk["size"] -= bucket_capacity_supplied
                        pool_buckets[bucket_needed] += bucket_capacity_supplied
                        bucket_deficit[bucket_needed] -= bucket_capacity_supplied
                        bk["pools"] = [x for x in bk["pools"] if x != bucket_needed]
                        if bk["size"] < 1:
                            remove = True
                    if not remove:
                        temp_bk.append(bk)
                bk_copy = temp_bk.copy()
                # Rule 5:
                # For all remaining liquids, check the pools which have the smallest bucket gap
                bucket_surplus = [x - pool_liquids[xi] for xi, x in enumerate(pool_buckets)]
                temp_lq = []
                for lq in lq_copy:
                    remove = False
                    bucket_needed = None
                    bucket_surplus_needed = None
                    for pl in lq["pools"]:
                        if bucket_surplus[pl] >= 0:
                            if bucket_needed is None or bucket_surplus[pl] < bucket_surplus_needed:
                                bucket_needed = pl
                                bucket_surplus_needed = bucket_surplus[pl]
                    if bucket_needed is not None:
                        liquid_supplied = min(bucket_surplus_needed, lq["size"])
                        lq["size"] -= liquid_supplied
                        pool_liquids[bucket_needed] += liquid_supplied
                        lq["pools"] = [x for x in lq["pools"] if x != bucket_needed]
                        if lq["size"] < 1:
                            remove = True
                    if not remove:
                        temp_lq.append(lq)
                lq_copy = temp_lq.copy()
                # Termination checks
                terminate = len(lq_copy) == 0 and len(bk_copy) == 0
                if terminate:
                    pool_valid = [(pool_valid[i] and v <= pool_buckets[i]) != 0 for i, v in enumerate(pool_liquids)]
                    pool_verified = [True] * pool_count
                terminate_verified = True
                for x in range(pool_count):
                    if pool_valid[x]:
                        terminate = False
                    if not pool_verified[x]:
                        terminate_verified = False
                if terminate or terminate_verified:
                    break
                iter_count -= 1
                if iter_count < 1:
                    break
            valid = True
            for x in pool_valid:
                if not x:
                    valid = False
            return valid

        inputs = {}
        outputs = {}
        self.getPoolBuffer()
        for x in range(4):
            for item_selector in self.item_search[x]:
                if item_selector not in inputs:
                    inputs[item_selector] = {"size": self.item_check_counts[item_selector][0], "pools": [x]}
                else:
                    inputs[item_selector]["pools"].append(x)
            for check_selector in self.check_search[x]:
                if check_selector not in outputs:
                    outputs[check_selector] = {"size": self.item_check_counts[check_selector][1], "pools": [x]}
                else:
                    outputs[check_selector]["pools"].append(x)
        return check_distribution(list(inputs.values()), list(outputs.values()))

    def __repr__(self):
        """Return printable version of the object as json.

        Returns:
            str: Json string of the dict.
        """
        return json.dumps(self.__dict__)

    def __setattr__(self, name, value):
        """Set an attributes value but only after verifying our hash."""
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Delete an attribute if its not our settings hash or if the code has been modified."""
        if name == "_Settings__hash":
            raise Exception("Error: Attempted deletion of race hash.")
        super().__delattr__(name)


class ItemPoolInfo:
    """Class for storing item pool information for analysis."""

    def __init__(self):
        """Initialize the item pool info object."""
        self.item_types = []
        self.location_types = []
        self.is_shuffled = True
        self.foolish = True
