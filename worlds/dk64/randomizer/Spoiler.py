"""Spoiler class and functions."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import TYPE_CHECKING, Dict, List, Optional, OrderedDict, Union

import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Maps import Maps
from randomizer.Enums.MoveTypes import MoveTypes
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Settings import (
    BananaportRando,
    CBRando,
    DKPortalRando,
    GlitchesSelected,
    LogicType,
    HardBossesSelected,
    MinigameBarrels,
    ProgressiveHintItem,
    RandomPrices,
    ShockwaveStatus,
    ShuffleLoadingZones,
    ShufflePortLocations,
    SpoilerHints,
    TrainingBarrels,
    WinConditionComplex,
)
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types, BarrierItems
from randomizer.Lists.EnemyTypes import EnemyMetaData
from randomizer.Lists.Item import ItemFromKong, ItemList, KongFromItem, NameFromKong
from randomizer.Lists.Location import LocationListOriginal, PreGivenLocations, TrainingBarrelLocations
from randomizer.Lists.Logic import GlitchLogicItems
from randomizer.Enums.Maps import Maps
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId
from randomizer.Lists.Minigame import (
    BarrelMetaData,
    HelmMinigameLocations,
    MinigameRequirements,
    TrainingMinigameLocations,
    MinigameSelector,
)
from randomizer.Lists.Multiselectors import FasterCheckSelector, RemovedBarrierSelector, QoLSelector
from randomizer.Lists.EnemyTypes import EnemySelector
from randomizer.Logic import CollectibleRegionsOriginal, LogicVarHolder, RegionsOriginal
from randomizer.Prices import ProgressiveMoves
from randomizer.Settings import Settings
from randomizer.ShuffleBosses import HardBossesEnabled
from randomizer.ShuffleExits import ShufflableExits
from randomizer.ShuffleKasplats import constants, shufflable
from randomizer.Patching.Library.Generic import IsItemSelected

if TYPE_CHECKING:
    from randomizer.Lists.Location import Location
    from randomizer.LogicClasses import Sphere

boss_map_names = {
    Maps.JapesBoss: "Army Dillo 1",
    Maps.AztecBoss: "Dogadon 1",
    Maps.FactoryBoss: "Mad Jack",
    Maps.GalleonBoss: "Pufftoss",
    Maps.FungiBoss: "Dogadon 2",
    Maps.CavesBoss: "Army Dillo 2",
    Maps.CastleBoss: "King Kut Out",
    Maps.KroolDonkeyPhase: "DK Phase",
    Maps.KroolDiddyPhase: "Diddy Phase",
    Maps.KroolLankyPhase: "Lanky Phase",
    Maps.KroolTinyPhase: "Tiny Phase",
    Maps.KroolChunkyPhase: "Chunky Phase",
}


class Spoiler:
    """Class which contains all spoiler data passed into and out of randomizer."""

    def __init__(self, settings: Settings) -> None:
        """Initialize spoiler just with settings."""
        self.settings: Settings = settings
        self.playthrough = {}
        self.woth = {}
        self.woth_locations = {}
        self.woth_paths = {}
        self.krool_paths = {}
        self.rap_win_con_paths = {}
        self.other_paths = {}
        self.shuffled_door_data = {}
        self.shuffled_barrel_data = {}
        self.shuffled_exit_data = {}
        self.shuffled_exit_instructions = []
        self.music_bgm_data = {}
        self.music_majoritem_data = {}
        self.music_minoritem_data = {}
        self.music_event_data = {}
        self.location_data = {}
        self.enemy_replacements = []
        self.cb_placements = []
        self.LogicVariables = LogicVarHolder(self)
        self.RegionList = deepcopy(RegionsOriginal)
        self.CollectibleRegions = deepcopy(CollectibleRegionsOriginal)
        self.LocationList = deepcopy(LocationListOriginal)

        self.move_data = []
        # 0: Cranky, 1: Funky, 2: Candy
        for move_master_type in range(3):
            master_moves = []
            if move_master_type == 0:
                # Shop
                for shop_index in range(3):
                    moves = []
                    # One for each kong
                    for kong_index in range(5):
                        kongmoves = []
                        # One for each level
                        for level_index in range(8):
                            kongmoves.append({"move_type": None})
                        moves.append(kongmoves)
                    master_moves.append(moves)
            elif move_master_type == 1:
                # Training Barrels
                if self.settings.training_barrels == TrainingBarrels.normal:
                    for tbarrel_type in ["dive", "orange", "barrel", "vine"]:
                        master_moves.append({"move_type": "flag", "flag": tbarrel_type, "price": 0})
                else:
                    for tbarrel_type in ["dive", "orange", "barrel", "vine"]:
                        master_moves.append({"move_type": None})
            elif move_master_type == 2:
                # BFI
                if self.settings.shockwave_status == ShockwaveStatus.vanilla:
                    master_moves = [{"move_type": "flag", "flag": "camera_shockwave", "price": 0}]
                else:
                    master_moves = [{"move_type": None}]
            self.move_data.append(master_moves)

        self.hint_list = {}
        self.short_hint_list = {}
        self.tied_hint_flags = {}
        self.tied_hint_regions = [HintRegion.NoRegion] * 35
        self.settings.finalize_world_settings(self)
        self.settings.update_valid_locations(self)

    def FlushAllExcessSpoilerData(self):
        """Flush all spoiler data that is not needed for the final result."""
        del self.LocationList
        del self.RegionList
        del self.CollectibleRegions
        del self.LogicVariables

    def Reset(self) -> None:
        """Reset logic variables and region info that should be reset before a search."""
        self.LogicVariables.Reset()
        self.ResetRegionAccess()
        self.ResetCollectibleRegions()

    def ResetRegionAccess(self) -> None:
        """Reset kong access for all regions."""
        for region in self.RegionList.values():
            region.ResetAccess()

    def ResetCollectibleRegions(self) -> None:
        """Reset if each collectible has been added."""
        for region in self.CollectibleRegions.values():
            for collectible in region:
                collectible.added = False
                # collectible.enabled = collectible.vanilla

    def ClearAllLocations(self) -> None:
        """Clear item from every location."""
        for location in self.LocationList.values():
            location.item = None
        # Always block PreGiven locations and only unblock them as we intentionally place moves there
        for location_id in TrainingBarrelLocations:
            self.LocationList[location_id].inaccessible = True
        for location_id in PreGivenLocations:
            self.LocationList[location_id].inaccessible = True

    def ResetLocationList(self) -> None:
        """Reset the LocationList to values conducive to a new fill."""
        for location in self.LocationList.values():
            location.PlaceDefaultItem(self)
        # Known to be incomplete - it should also confirm the correct locations of Fairies, Dirt, and Crowns

    def InitKasplatMap(self) -> None:
        """Initialize kasplat_map in logic variables with default values."""
        # Just use default kasplat associations.
        self.LogicVariables.kasplat_map = {}
        self.LogicVariables.kasplat_map.update(shufflable)
        self.LogicVariables.kasplat_map.update(constants)

    def getItemGroup(self, item: Optional[Items]) -> str:
        """Get item group from item."""
        if item is None:
            item = Items.NoItem
        if item == Items.NoItem:
            return "Empty"
        item_type = ItemList[item].type
        type_dict = {
            Types.Kong: "Kongs",
            Types.Shop: "Moves",
            Types.Shockwave: "Moves",
            Types.TrainingBarrel: "Moves",
            Types.Climbing: "Moves",
            Types.Banana: "Golden Bananas",
            Types.Blueprint: "Blueprints",
            Types.Fairy: "Fairies",
            Types.Key: "Keys",
            Types.Crown: "Crowns",
            Types.Medal: "Medals",
            Types.NintendoCoin: "Company Coins",
            Types.RarewareCoin: "Company Coins",
            Types.Bean: "Miscellaneous Items",
            Types.Pearl: "Miscellaneous Items",
            Types.RainbowCoin: "Rainbow Coins",
            Types.FakeItem: "Ice Traps",
            Types.JunkItem: "Junk Items",
            Types.CrateItem: "Melon Crates",
            Types.Enemies: "Enemy Drops",
            Types.Cranky: "Shop Owners",
            Types.Funky: "Shop Owners",
            Types.Candy: "Shop Owners",
            Types.Snide: "Shop Owners",
            Types.Hint: "Hints",
        }
        if item_type in type_dict:
            return type_dict[item_type]
        return "Unknown"

    def dumpMultiselector(self, toggle: bool, settings_list: list, selector_list: list):
        """Dump multiselector list to a response which can be dumped to the spoiler."""
        if toggle and any(settings_list):
            lst = []
            selector_name_dict = {}
            for x in selector_list:
                selector_name_dict[x["value"]] = x["name"]
            for x in settings_list:
                if x.name in selector_name_dict:
                    lst.append(selector_name_dict[x.name])
            return lst
        return toggle

    def createJson(self) -> None:
        """Convert spoiler to JSON and save it."""
        # We want to convert raw spoiler data into the important bits and in human-readable formats.
        humanspoiler = OrderedDict()
        # Settings data
        settings = OrderedDict()
        settings["Settings String"] = self.settings.settings_string
        settings["Seed"] = self.settings.seed_id
        # settings["algorithm"] = self.settings.algorithm # Don't need this for now, probably
        logic_types = {
            LogicType.nologic: "No Logic",
            LogicType.glitch: "Glitched Logic",
            LogicType.glitchless: "Glitchless Logic",
        }
        if self.settings.logic_type in logic_types:
            settings["Logic Type"] = logic_types[self.settings.logic_type]
        else:
            settings["Logic Type"] = self.settings.logic_type
        if self.settings.logic_type == LogicType.glitch:
            settings["Glitches Enabled"] = ", ".join(
                [x.name for x in GlitchLogicItems if GlitchesSelected[x.shorthand] in self.settings.glitches_selected or len(self.settings.glitches_selected) == 0]
            )
        settings["Shuffle Enemies"] = self.settings.enemy_rando
        settings["Move Randomization type"] = self.settings.move_rando.name
        settings["Loading Zones Shuffled"] = self.settings.shuffle_loading_zones.name
        settings["Decoupled Loading Zones"] = self.settings.decoupled_loading_zones
        settings["Helm Location Shuffled"] = self.settings.shuffle_helm_location
        startKongList = []
        for x in self.settings.starting_kong_list:
            startKongList.append(x.name.capitalize())
        settings["Hard B Lockers"] = self.settings.hard_blockers
        if self.settings.randomize_blocker_required_amounts:
            settings["Maximum B Locker"] = self.settings.blocker_text
            if self.settings.maximize_helm_blocker:
                settings["Maximum B Locker ensured"] = self.settings.maximize_helm_blocker
        settings["Hard Troff N Scoff"] = self.settings.hard_troff_n_scoff
        if self.settings.randomize_cb_required_amounts:
            settings["Maximum Troff N Scoff"] = self.settings.troff_text
        settings["Open Lobbies"] = self.settings.open_lobbies
        settings["Auto Complete Bonus Barrels"] = self.settings.bonus_barrel_auto_complete
        settings["Auto Key Turn ins"] = self.settings.auto_keys
        settings["Chaos B.Lockers"] = self.settings.chaos_blockers
        settings["Chaos Ratio"] = self.settings.chaos_ratio
        settings["Complex Level Order"] = self.settings.hard_level_progression
        settings["Progressive Switch Strength"] = self.settings.alter_switch_allocation
        settings["Hard Shooting"] = self.settings.hard_shooting
        settings["Dropsanity"] = self.settings.enemy_drop_rando
        settings["Switchsanity"] = self.settings.switchsanity.name
        settings["Free Trade Agreement"] = self.settings.free_trade_setting.name
        settings["Randomize Pickups"] = self.settings.randomize_pickups
        settings["Randomize Patches"] = self.settings.random_patches
        settings["Randomize Crates"] = self.settings.random_crates
        settings["Randomize CB Locations"] = self.settings.cb_rando_enabled
        settings["Randomize Coin Locations"] = self.settings.coin_rando
        settings["Randomize Shop Locations"] = self.settings.shuffle_shops
        settings["Randomize Kasplats"] = self.settings.kasplat_rando_setting.name
        settings["Randomize Banana Fairies"] = self.settings.random_fairies
        settings["Randomize Battle Arenas"] = self.settings.crown_placement_rando
        settings["Vanilla Door Shuffle"] = self.settings.vanilla_door_rando
        settings["Dos' Doors"] = self.settings.dos_door_rando
        settings["Randomize Wrinkly Doors"] = self.settings.wrinkly_location_rando
        settings["Randomize T&S Portals"] = self.settings.tns_location_rando
        settings["Puzzle Randomization"] = self.settings.puzzle_rando_difficulty.name
        settings["Crown Door Open"] = self.settings.crown_door_item == BarrierItems.Nothing
        settings["Coin Door Open"] = self.settings.coin_door_item == BarrierItems.Nothing
        settings["Shockwave Shuffle"] = self.settings.shockwave_status.name
        settings["Random Jetpac Medal Requirement"] = self.settings.random_medal_requirement
        settings["Bananas Required for Medal"] = self.settings.medal_cb_req
        settings["Fairies Required for Rareware GB"] = self.settings.rareware_gb_fairies
        settings["Pearls Required for Mermaid GB"] = self.settings.mermaid_gb_pearls
        settings["Random Shop Prices"] = self.settings.random_prices.name
        settings["Banana Port Randomization"] = self.settings.bananaport_rando.name
        settings["Banana port Location Shuffle"] = self.settings.bananaport_placement_rando.name
        settings["Activated Warps"] = self.settings.activate_all_bananaports.name
        settings["Smaller Shops"] = self.settings.smaller_shops
        settings["Irondonk"] = self.settings.perma_death
        settings["Disable Tag Barrels"] = self.settings.disable_tag_barrels
        settings["Ice Trap Frequency"] = self.settings.ice_trap_frequency.name
        settings["Ice Traps Damage Player"] = self.settings.ice_traps_damage
        settings["Mirror Mode"] = self.settings.mirror_mode
        settings["Damage Amount"] = self.settings.damage_amount.name
        settings["Hard Mode Enabled"] = self.settings.hard_mode and len(self.settings.hard_mode_selected) > 0
        settings["Hard Bosses Enabled"] = self.settings.hard_bosses and len(self.settings.hard_bosses_selected) > 0
        # settings["Krusha Slot"] = self.settings.krusha_ui.name
        settings["DK Model"] = self.settings.kong_model_dk.name
        settings["Diddy Model"] = self.settings.kong_model_diddy.name
        settings["Lanky Model"] = self.settings.kong_model_lanky.name
        settings["Tiny Model"] = self.settings.kong_model_tiny.name
        settings["Chunky Model"] = self.settings.kong_model_chunky.name

        settings["Key 8 Required"] = self.settings.krool_access
        settings["Vanilla K. Rool Requirement"] = self.settings.k_rool_vanilla_requirement
        settings["Key 8 in Helm"] = self.settings.key_8_helm
        settings["Select Starting Keys"] = self.settings.select_keys
        if not self.settings.keys_random:
            settings["Number of Keys Required"] = self.settings.krool_key_count
        settings["Starting Moves Count"] = self.settings.starting_moves_count
        settings["Fast Start"] = self.settings.fast_start_beginning_of_game
        settings["Helm Setting"] = self.settings.helm_setting.name
        settings["Helm Room Bonus Count"] = int(self.settings.helm_room_bonus_count)
        settings["Tag Anywhere"] = self.settings.enable_tag_anywhere
        settings["Kongless Hint Doors"] = self.settings.wrinkly_available
        settings["Quality of Life"] = self.dumpMultiselector(self.settings.quality_of_life, self.settings.misc_changes_selected, QoLSelector)
        settings["Fast GBs"] = self.dumpMultiselector(self.settings.faster_checks_enabled, self.settings.faster_checks_selected, FasterCheckSelector)
        settings["Barriers Removed"] = self.dumpMultiselector(self.settings.remove_barriers_enabled, self.settings.remove_barriers_selected, RemovedBarrierSelector)
        settings["Random Win Condition"] = self.settings.win_condition_random
        if not self.settings.win_condition_random:
            wc_count = self.settings.win_condition_count
            win_con_name_table = {
                WinConditionComplex.beat_krool: "Beat K. Rool",
                WinConditionComplex.get_key8: "Acquire Key 8",
                WinConditionComplex.krem_kapture: "Kremling Kapture",
                WinConditionComplex.dk_rap_items: "Complete the Rap",
                WinConditionComplex.req_bean: "Acquire the Bean",
                WinConditionComplex.req_bp: f"{wc_count} Blueprint{'s' if wc_count != 1 else ''}",
                WinConditionComplex.req_companycoins: f"{wc_count} Company Coin{'s' if wc_count != 1 else ''}",
                WinConditionComplex.req_crown: f"{wc_count} Crown{'s' if wc_count != 1 else ''}",
                WinConditionComplex.req_fairy: f"{wc_count} Fair{'ies' if wc_count != 1 else 'y'}",
                WinConditionComplex.req_gb: f"{wc_count} Golden Banana{'s' if wc_count != 1 else ''}",
                WinConditionComplex.req_key: f"{wc_count} Key{'s' if wc_count != 1 else ''}",
                WinConditionComplex.req_medal: f"{wc_count} Medal{'s' if wc_count != 1 else ''}",
                WinConditionComplex.req_pearl: f"{wc_count} Pearl{'s' if wc_count != 1 else ''}",
                WinConditionComplex.req_rainbowcoin: f"{wc_count} Rainbow Coin{'s' if wc_count != 1 else ''}",
            }
            if self.settings.win_condition_item in win_con_name_table:
                settings["Win Condition"] = win_con_name_table[self.settings.win_condition_item]
            else:
                settings["Win Condition"] = self.settings.win_condition_item.name
        settings["Fungi Time of Day"] = self.settings.fungi_time.name
        settings["Galleon Water Level"] = self.settings.galleon_water.name
        settings["Chunky Phase Slam Requirement"] = self.settings.chunky_phase_slam_req.name
        settings["Hint Preset"] = self.settings.wrinkly_hints
        if self.settings.progressive_hint_item != ProgressiveHintItem.off:
            settings["Progressive Hint Item"] = self.settings.progressive_hint_item.name
            settings["Progressive Hint Cap"] = int(self.settings.progressive_hint_count)
        settings["Dim Solved Hints"] = self.settings.dim_solved_hints
        settings["No Joke Hints"] = self.settings.serious_hints
        settings["Item Reward Previews"] = self.settings.item_reward_previews
        settings["Bonus Barrel Rando"] = self.dumpMultiselector(self.settings.bonus_barrel_rando, self.settings.minigames_list_selected, MinigameSelector)
        if self.settings.enemy_rando and any(self.settings.enemies_selected):
            value_lst = [x.name for x in self.settings.enemies_selected]
            settings["Enemy Rando"] = [enemy["name"] for enemy in EnemySelector if enemy["value"] in value_lst]
        else:
            settings["Enemy Rando"] = self.settings.enemy_rando
        settings["Crown Enemy Rando"] = self.settings.crown_enemy_difficulty.name
        if self.settings.helm_hurry:
            settings["Game Mode"] = "Helm Hurry"
        humanspoiler["Settings"] = settings
        humanspoiler["Randomizer Version"] = self.settings.version
        humanspoiler["Generation Branch"] = self.settings.branch
        humanspoiler["Cosmetics"] = {}
        if self.settings.spoiler_hints != SpoilerHints.off:
            humanspoiler["Spoiler Hints Data"] = {}
            for key in self.level_spoiler.keys():
                if key == "point_spread":
                    humanspoiler["Spoiler Hints Data"][key] = json.dumps(self.level_spoiler[key])
                else:
                    humanspoiler["Spoiler Hints Data"][key] = self.level_spoiler[key].toJSON()
            humanspoiler["Spoiler Hints"] = self.level_spoiler_human_readable
        humanspoiler["Requirements"] = {}
        if self.settings.random_starting_region:
            humanspoiler["Game Start"] = {}
            humanspoiler["Game Start"]["Starting Kong List"] = startKongList
            humanspoiler["Game Start"]["Starting Region"] = self.settings.starting_region["region_name"]
            humanspoiler["Game Start"]["Starting Exit"] = self.settings.starting_region["exit_name"]
        # GB Counts
        gb_counts = {}
        level_list = [
            "Jungle Japes",
            "Angry Aztec",
            "Frantic Factory",
            "Gloomy Galleon",
            "Fungi Forest",
            "Crystal Caves",
            "Creepy Castle",
            "Hideout Helm",
        ]
        for level_index, amount in enumerate(self.settings.BLockerEntryCount):
            item = self.settings.BLockerEntryItems[level_index].name
            item_total = f" {item}s"
            if item == "Percentage":
                item_total = "%"
            elif item == "Fairy" and amount != 1:
                item_total = " Fairies"  # LOL @ English Language
            elif amount == 1:
                item_total = f" {item}"
            gb_counts[level_list[level_index]] = f"{amount}{item_total}"
        humanspoiler["Requirements"]["B Locker Items"] = gb_counts
        # CB Counts
        cb_counts = {}
        for level_index, amount in enumerate(self.settings.BossBananas):
            cb_counts[level_list[level_index]] = amount
        humanspoiler["Requirements"]["Troff N Scoff Bananas"] = cb_counts
        humanspoiler["Requirements"]["Miscellaneous"] = {}
        humanspoiler["Kongs"] = {}
        humanspoiler["Kongs"]["Starting Kong List"] = startKongList
        humanspoiler["Kongs"]["Japes Kong Puzzle Solver"] = ItemList[ItemFromKong(self.settings.diddy_freeing_kong)].name
        humanspoiler["Kongs"]["Tiny Temple Puzzle Solver"] = ItemList[ItemFromKong(self.settings.tiny_freeing_kong)].name
        humanspoiler["Kongs"]["Llama Temple Puzzle Solver"] = ItemList[ItemFromKong(self.settings.lanky_freeing_kong)].name
        humanspoiler["Kongs"]["Factory Kong Puzzle Solver"] = ItemList[ItemFromKong(self.settings.chunky_freeing_kong)].name
        humanspoiler["Requirements"]["Miscellaneous"]["Jetpac Medal Requirement"] = self.settings.medal_requirement
        humanspoiler["End Game"] = {
            "Helm": {},
            "K. Rool": {},
        }
        humanspoiler["End Game"]["K. Rool"]["Keys Required for K Rool"] = self.GetKroolKeysRequired(self.settings.krool_keys_required)
        krool_order = []
        for phase in self.settings.krool_order:
            krool_order.append(boss_map_names[phase])
        humanspoiler["End Game"]["K. Rool"]["K Rool Phases"] = krool_order
        humanspoiler["End Game"]["K. Rool"]["Chunky Phase Slam Requirement"] = self.settings.chunky_phase_slam_req_internal.name
        humanspoiler["End Game"]["K. Rool"]["DK Phase requires Baboon Blast"] = self.settings.cannons_require_blast

        helm_default_order = [Kongs.donkey, Kongs.chunky, Kongs.tiny, Kongs.lanky, Kongs.diddy]
        helm_new_order = []
        for room in self.settings.helm_order:
            helm_new_order.append(helm_default_order[room].name.capitalize())
        humanspoiler["End Game"]["Helm"]["Helm Rooms"] = helm_new_order
        helm_door_names = {
            BarrierItems.Bean: "Bean",
            BarrierItems.Blueprint: "Blueprints",
            BarrierItems.CompanyCoin: "Company Coins",
            BarrierItems.Crown: "Crowns",
            BarrierItems.Fairy: "Fairies",
            BarrierItems.GoldenBanana: "Golden Bananas",
            BarrierItems.Key: "Keys",
            BarrierItems.Medal: "Medals",
            BarrierItems.Pearl: "Pearls",
            BarrierItems.RainbowCoin: "Rainbow Coins",
        }
        if self.settings.crown_door_item != BarrierItems.Nothing:
            item = self.settings.crown_door_item
            humanspoiler["End Game"]["Helm"]["Crown Door Item"] = helm_door_names[item]
            humanspoiler["End Game"]["Helm"]["Crown Door Item Randomized"] = self.settings.crown_door_random
            humanspoiler["End Game"]["Helm"]["Crown Door Item Amount"] = self.settings.crown_door_item_count
        if self.settings.coin_door_item != BarrierItems.Nothing:
            item = self.settings.coin_door_item
            humanspoiler["End Game"]["Helm"]["Coin Door Item"] = helm_door_names[item]
            humanspoiler["End Game"]["Helm"]["Coin Door Item Randomized"] = self.settings.coin_door_random
            humanspoiler["End Game"]["Helm"]["Coin Door Item Amount"] = self.settings.coin_door_item_count
        if self.settings.shuffle_items:
            humanspoiler["Item Pool"] = list(set([enum.name for enum in self.settings.shuffled_location_types]))
        if self.settings.hard_mode_selected and len(self.settings.hard_mode_selected) > 0:
            humanspoiler["Hard Mode"] = list(set([enum.name for enum in self.settings.hard_mode_selected]))
        if self.settings.hard_bosses_selected and len(self.settings.hard_bosses_selected) > 0:
            humanspoiler["Hard Bosses"] = list(set([enum.name for enum in self.settings.hard_bosses_selected]))
        humanspoiler["Items"] = {
            "Kongs": {},
            "Shops": {},
            "DK Isles": {},
            "Jungle Japes": {},
            "Angry Aztec": {},
            "Frantic Factory": {},
            "Gloomy Galleon": {},
            "Fungi Forest": {},
            "Crystal Caves": {},
            "Creepy Castle": {},
            "Hideout Helm": {},
            "Special": {},
        }
        sorted_item_name = "Items (Sorted by Item)"
        humanspoiler[sorted_item_name] = {
            "Kongs": {},
            "Moves": {},
            "Golden Bananas": {},
            "Blueprints": {},
            "Fairies": {},
            "Keys": {},
            "Crowns": {},
            "Company Coins": {},
            "Medals": {},
            "Miscellaneous Items": {},
            "Rainbow Coins": {},
            "Ice Traps": {},
            "Junk Items": {},
            "Melon Crates": {},
            "Hints": {},
            "Enemy Drops": {},
            "Shop Owners": {},
            "Empty": {},
            "Unknown": {},
        }

        self.pregiven_items = []
        self.first_move_item = None
        for location_id, location in self.LocationList.items():
            # No need to spoiler constants
            if location.type == Types.Constant or location.inaccessible:
                continue
            # No hints if hint doors are not in the pool
            if location.type == Types.Hint and Types.Hint not in self.settings.shuffled_location_types:
                continue
            if location.type == Types.ProgressiveHint:
                continue
            if location_id in PreGivenLocations:
                if self.settings.fast_start_beginning_of_game or location_id != Locations.IslesFirstMove:
                    self.pregiven_items.append(location.item)
                else:
                    self.first_move_item = location.item
            # Prevent weird null issues but get the item at the location
            if location.item is None:
                item = Items.NoItem
            else:
                item = ItemList[location.item]
            # Empty PreGiven locations don't really exist and shouldn't show up in the spoiler log
            if location.type in (
                Types.PreGivenMove,
                Types.Cranky,
                Types.Candy,
                Types.Funky,
                Types.Snide,
            ) and location.item in (None, Items.NoItem):
                continue
            # Separate Kong locations
            if location.type == Types.Kong:
                humanspoiler["Items"]["Kongs"][location.name] = item.name
                humanspoiler[sorted_item_name][self.getItemGroup(location.item)][location.name] = item.name
            # Separate Shop locations
            elif location.type == Types.Shop:
                # Ignore shop locations with no items
                if location.item is None or location.item == Items.NoItem:
                    continue
                # Gotta dig up the price - progressive moves look a little weird in the spoiler
                price = ""
                if location.item in ProgressiveMoves.keys():
                    if location.item == Items.ProgressiveSlam:
                        price = f"{self.settings.prices[Items.ProgressiveSlam][0]}->{self.settings.prices[Items.ProgressiveSlam][1]}"
                    elif location.item == Items.ProgressiveAmmoBelt:
                        price = f"{self.settings.prices[Items.ProgressiveAmmoBelt][0]}->{self.settings.prices[Items.ProgressiveAmmoBelt][1]}"
                    elif location.item == Items.ProgressiveInstrumentUpgrade:
                        price = f"{self.settings.prices[Items.ProgressiveInstrumentUpgrade][0]}->{self.settings.prices[Items.ProgressiveInstrumentUpgrade][1]}->{self.settings.prices[Items.ProgressiveInstrumentUpgrade][2]}"
                # Vanilla prices are by item, not by location
                elif self.settings.random_prices == RandomPrices.vanilla:
                    price = str(self.settings.prices[location.item])
                else:
                    price = str(self.settings.prices[location_id])
                humanspoiler["Items"]["Shops"][location.name] = item.name + f" ({price})"
                humanspoiler[sorted_item_name][self.getItemGroup(location.item)][location.name] = item.name
            # Filter everything else by level - each location conveniently contains a level-identifying bit in their name
            else:
                level = "Special"
                if "Isles" in location.name or location.type in (
                    Types.PreGivenMove,
                    Types.Climbing,
                    Types.Cranky,
                    Types.Funky,
                    Types.Candy,
                    Types.Snide,
                ):
                    level = "DK Isles"
                elif "Japes" in location.name:
                    level = "Jungle Japes"
                elif "Aztec" in location.name:
                    level = "Angry Aztec"
                elif "Factory" in location.name:
                    level = "Frantic Factory"
                elif "Galleon" in location.name:
                    level = "Gloomy Galleon"
                elif "Forest" in location.name:
                    level = "Fungi Forest"
                elif "Caves" in location.name:
                    level = "Crystal Caves"
                elif "Castle" in location.name:
                    level = "Creepy Castle"
                elif "Helm" in location.name:
                    level = "Hideout Helm"
                if self.settings.enemy_drop_rando or location.item != Items.EnemyItem:
                    humanspoiler["Items"][level][location.name] = item.name
                humanspoiler[sorted_item_name][self.getItemGroup(location.item)][location.name] = item.name
        if not self.settings.enemy_drop_rando:
            del humanspoiler[sorted_item_name]["Enemy Drops"]
        if self.settings.enemy_rando:
            placement_dict = {}
            for map_id in self.enemy_rando_data:
                map_name = Maps(map_id).name
                map_dict = {}
                for enemy in self.enemy_rando_data[map_id]:
                    map_dict[enemy["location"]] = EnemyMetaData[enemy["enemy"]].name
                placement_dict[map_name] = map_dict
            if not self.settings.enemy_drop_rando:
                humanspoiler["Enemy Placement (Stringified JSON)"] = json.dumps(placement_dict)
            else:
                humanspoiler["Enemy Placement"] = placement_dict
        humanspoiler["Bosses"] = {}
        if self.settings.boss_location_rando:
            shuffled_bosses = OrderedDict()
            for i in range(7):
                shuffled_bosses["".join(map(lambda x: x if x.islower() else " " + x, Levels(i).name)).strip()] = boss_map_names.get(self.settings.boss_maps[i], Maps(self.settings.boss_maps[i]).name)
            humanspoiler["Bosses"]["Shuffled Boss Order"] = shuffled_bosses

        humanspoiler["Bosses"]["King Kut Out Properties"] = {}
        if self.settings.boss_kong_rando:
            shuffled_boss_kongs = OrderedDict()
            for i in range(7):
                shuffled_boss_kongs["".join(map(lambda x: x if x.islower() else " " + x, Levels(i).name)).strip()] = Kongs(self.settings.boss_kongs[i]).name.capitalize()
            humanspoiler["Bosses"]["Shuffled Boss Kongs"] = shuffled_boss_kongs
            kutout_order = ""
            for kong in self.settings.kutout_kongs:
                kutout_order = kutout_order + Kongs(kong).name.capitalize() + ", "
            humanspoiler["Bosses"]["King Kut Out Properties"]["Shuffled Kutout Kong Order"] = kutout_order

        if HardBossesEnabled(self.settings, HardBossesSelected.kut_out_phase_rando):
            phase_names = []
            for phase in self.settings.kko_phase_order:
                phase_names.append(f"Phase {phase+1}")
            humanspoiler["Bosses"]["King Kut Out Properties"]["Shuffled Kutout Phases"] = ", ".join(phase_names)

        if self.settings.bonus_barrels == MinigameBarrels.selected and len(self.settings.minigames_list_selected) > 0:
            selected_minigames = []
            for minigame in self.settings.minigames_list_selected:
                selected_minigames.append(minigame.name)
            humanspoiler["Selected Minigames"] = selected_minigames
        if (
            self.settings.bonus_barrels in (MinigameBarrels.random, MinigameBarrels.selected)
            or self.settings.helm_barrels == MinigameBarrels.random
            or self.settings.training_barrels_minigames == MinigameBarrels.random
        ):
            shuffled_barrels = OrderedDict()
            for location, minigame in self.shuffled_barrel_data.items():
                if location in HelmMinigameLocations and self.settings.helm_barrels == MinigameBarrels.skip:
                    continue
                if location in TrainingMinigameLocations and self.settings.training_barrels_minigames == MinigameBarrels.skip:
                    continue
                if location not in HelmMinigameLocations and location not in TrainingMinigameLocations and self.settings.bonus_barrels == MinigameBarrels.skip:
                    continue
                shuffled_barrels[self.LocationList[location].name] = MinigameRequirements[minigame].name
            if len(shuffled_barrels) > 0:
                humanspoiler["Shuffled Bonus Barrels"] = shuffled_barrels

        if self.settings.kasplat_rando:
            humanspoiler["Shuffled Kasplats"] = self.human_kasplats
        if self.settings.random_fairies:
            humanspoiler["Shuffled Banana Fairies"] = self.fairy_locations_human
        if self.settings.random_patches:
            humanspoiler["Shuffled Dirt Patches"] = self.human_patches
        if self.settings.random_crates:
            humanspoiler["Shuffled Melon Crates"] = self.human_crates
        humanspoiler["Settings"]["Shuffled Bananaport Levels"] = False
        if self.settings.bananaport_placement_rando != ShufflePortLocations.off and self.settings.bananaport_rando == BananaportRando.off:
            shuffled_warp_levels = [x.name for x in self.settings.warp_level_list_selected]
            if len(shuffled_warp_levels) == 0:
                humanspoiler["Settings"]["Shuffled Bananaport Levels"] = True
            else:
                humanspoiler["Settings"]["Shuffled Bananaport Levels"] = shuffled_warp_levels
            humanspoiler["Shuffled Bananaport Locations"] = self.human_warps
        if self.settings.bananaport_rando != BananaportRando.off:
            humanspoiler["Shuffled Bananaport Connections (Source -> Destination)"] = self.human_warp_locations
        if self.settings.wrinkly_location_rando:
            prog_hint_setting = self.settings.progressive_hint_item
            item_types = self.settings.shuffled_location_types
            if prog_hint_setting == ProgressiveHintItem.off or Types.Hint in item_types:
                humanspoiler["Wrinkly Door Locations"] = self.human_hint_doors
        if self.settings.tns_location_rando:
            humanspoiler["T&S Portal Locations"] = self.human_portal_doors
        if self.settings.dk_portal_location_rando_v2 != DKPortalRando.off:
            humanspoiler["DK Portal Locations"] = self.human_entry_doors
        if self.settings.crown_placement_rando:
            humanspoiler["Battle Arena Locations"] = self.human_crowns
        if self.settings.switchsanity:
            ss_data = {}
            ss_name_data = {
                Kongs.donkey: {
                    SwitchType.SlamSwitch: "Donkey Slam Switch",
                    SwitchType.GunSwitch: "Coconut Switch",
                    SwitchType.InstrumentPad: "Bongos Pad",
                    SwitchType.PadMove: "Baboon Blast Pad",
                    SwitchType.MiscActivator: "Gorilla Grab Lever",
                },
                Kongs.diddy: {
                    SwitchType.SlamSwitch: "Diddy Slam Switch",
                    SwitchType.GunSwitch: "Peanut Switch",
                    SwitchType.InstrumentPad: "Guitar Pad",
                    SwitchType.PadMove: "Simian Spring Pad",
                    SwitchType.MiscActivator: "Gong",
                },
                Kongs.lanky: {
                    SwitchType.SlamSwitch: "Lanky Slam Switch",
                    SwitchType.GunSwitch: "Grape Switch",
                    SwitchType.InstrumentPad: "Trombone Pad",
                    SwitchType.PadMove: "Baboon Balloon Pad",
                },
                Kongs.tiny: {
                    SwitchType.SlamSwitch: "Tiny Slam Switch",
                    SwitchType.GunSwitch: "Feather Switch",
                    SwitchType.InstrumentPad: "Saxophone Pad",
                    SwitchType.PadMove: "Monkeyport Pad",
                },
                Kongs.chunky: {
                    SwitchType.SlamSwitch: "Chunky Slam Switch",
                    SwitchType.GunSwitch: "Pineapple Switch",
                    SwitchType.InstrumentPad: "Triangle Pad",
                    SwitchType.PadMove: "Gorilla Gone Pad",
                },
            }
            for slot in self.settings.switchsanity_data.values():
                ss_data[slot.name] = ss_name_data[slot.kong][slot.switch_type]
            humanspoiler["Switchsanity"] = ss_data
        level_dict = {
            Levels.DKIsles: "DK Isles",
            Levels.JungleJapes: "Jungle Japes",
            Levels.AngryAztec: "Angry Aztec",
            Levels.FranticFactory: "Frantic Factory",
            Levels.GloomyGalleon: "Gloomy Galleon",
            Levels.FungiForest: "Fungi Forest",
            Levels.CrystalCaves: "Crystal Caves",
            Levels.CreepyCastle: "Creepy Castle",
        }
        if self.settings.shuffle_shops:
            shop_location_dict = {}
            for level in self.shuffled_shop_locations:
                level_name = "Unknown Level"

                shop_dict = {
                    Regions.CrankyGeneric: "Cranky",
                    Regions.CandyGeneric: "Candy",
                    Regions.FunkyGeneric: "Funky",
                    Regions.Snide: "Snide",
                }
                if level in level_dict:
                    level_name = level_dict[level]
                for shop in self.shuffled_shop_locations[level]:
                    location_name = "Unknown Shop"
                    shop_name = "Unknown Shop"
                    new_shop = self.shuffled_shop_locations[level][shop]
                    if shop in shop_dict:
                        location_name = shop_dict[shop]
                    if new_shop in shop_dict:
                        shop_name = shop_dict[new_shop]
                    shop_location_dict[f"{level_name} - {location_name}"] = shop_name
            humanspoiler["Shop Locations"] = shop_location_dict
        for spoiler_dict in ("Items", "Bosses"):
            is_empty = True
            for y in humanspoiler[spoiler_dict]:
                if humanspoiler[spoiler_dict][y] != {}:
                    is_empty = False
            if is_empty:
                del humanspoiler[spoiler_dict]

        if self.settings.cb_rando_enabled:
            human_cb_type_map = {"cb": " Bananas", "balloons": " Balloons"}
            humanspoiler["Colored Banana Locations"] = {}
            cb_levels = []
            level_dict = {
                Levels.DKIsles: "DK Isles",
                Levels.JungleJapes: "Jungle Japes",
                Levels.AngryAztec: "Angry Aztec",
                Levels.FranticFactory: "Frantic Factory",
                Levels.GloomyGalleon: "Gloomy Galleon",
                Levels.FungiForest: "Fungi Forest",
                Levels.CrystalCaves: "Crystal Caves",
                Levels.CreepyCastle: "Creepy Castle",
            }
            cb_levels = [name for lvl, name in level_dict.items() if IsItemSelected(self.settings.cb_rando_enabled, self.settings.cb_rando_list_selected, lvl)]
            cb_kongs = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
            for lvl in cb_levels:
                for kng in cb_kongs:
                    humanspoiler["Colored Banana Locations"][f"{lvl} {kng}"] = {"Balloons": [], "Bananas": []}
            for group in self.cb_placements:
                lvl_name = level_dict[group["level"]]
                map_name = "".join(map(lambda x: x if x.islower() else " " + x, Maps(group["map"]).name)).strip()
                join_combos = ["2 D Ship", "5 D Ship", "5 D Temple"]
                for combo in join_combos:
                    if combo in map_name:
                        map_name = map_name.replace(combo, combo.replace(" ", ""))
                humanspoiler["Colored Banana Locations"][f"{lvl_name} {NameFromKong(group['kong'])}"][human_cb_type_map[group["type"]].strip()].append(f"{map_name.strip()}: {group['name']}")
        if self.settings.coin_rando:
            humanspoiler["Coin Locations"] = {}
            coin_levels = ["Japes", "Aztec", "Factory", "Galleon", "Fungi", "Caves", "Castle", "Isles"]
            coin_kongs = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
            for lvl in coin_levels:
                for kng in coin_kongs:
                    humanspoiler["Coin Locations"][f"{lvl} {kng}"] = []
            for group in self.coin_placements:
                lvl_name = level_dict[group["level"]]
                idx = 1
                if group["level"] == Levels.FungiForest:
                    idx = 0
                map_name = "".join(map(lambda x: x if x.islower() else " " + x, Maps(group["map"]).name)).strip()
                join_combos = ["2 D Ship", "5 D Ship", "5 D Temple"]
                for combo in join_combos:
                    if combo in map_name:
                        map_name = map_name.replace(combo, combo.replace(" ", ""))
                humanspoiler["Coin Locations"][f"{lvl_name.split(' ')[idx]} {NameFromKong(group['kong'])}"].append(f"{map_name.strip()}: {group['name']}")

        # Playthrough data
        humanspoiler["Playthrough"] = self.playthrough

        # Woth data
        humanspoiler["Way of the Hoard"] = self.woth
        humanspoiler["WotH Paths"] = {}
        slamCount = 0
        pearlCount = 0
        for loc, path in self.woth_paths.items():
            destination_item = ItemList[self.LocationList[loc].item]
            path_dict = {}
            for path_loc_id in path:
                path_location = self.LocationList[path_loc_id]
                path_item = ItemList[path_location.item]
                path_dict[path_location.name] = path_item.name
            extra = ""
            if self.LocationList[loc].item == Items.ProgressiveSlam:
                slamCount += 1
                extra = " " + str(slamCount)
            if self.LocationList[loc].item == Items.Pearl:
                pearlCount += 1
                extra = " " + str(pearlCount)
            humanspoiler["WotH Paths"][destination_item.name + extra] = path_dict
        for map_id, path in self.krool_paths.items():
            path_dict = {}
            for path_loc_id in path:
                path_location = self.LocationList[path_loc_id]
                path_item = ItemList[path_location.item]
                path_dict[path_location.name] = path_item.name
            phase_name = boss_map_names.get(map_id, Maps(map_id).name)
            humanspoiler["WotH Paths"][phase_name] = path_dict
        if self.settings.win_condition_item == WinConditionComplex.dk_rap_items:
            for verse_name, path in self.rap_win_con_paths.items():
                path_dict = {}
                for path_loc_id in path:
                    path_location = self.LocationList[path_loc_id]
                    path_item = ItemList[path_location.item]
                    path_dict[path_location.name] = path_item.name
                humanspoiler["WotH Paths"][verse_name] = path_dict
        humanspoiler["Other Paths"] = {}
        for loc, path in self.other_paths.items():
            destination_item = ItemList[self.LocationList[loc].item]
            path_dict = {}
            for path_loc_id in path:
                path_location = self.LocationList[path_loc_id]
                path_item = ItemList[path_location.item]
                path_dict[path_location.name] = path_item.name
            extra = ""
            if self.LocationList[loc].item == Items.ProgressiveSlam:
                slamCount += 1
                extra = " " + str(slamCount)
            if self.LocationList[loc].item == Items.Pearl:
                pearlCount += 1
                extra = " " + str(pearlCount)
            humanspoiler["Other Paths"][destination_item.name + extra] = path_dict

        if self.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
            # Just show level order
            shuffled_exits = OrderedDict()
            lobby_entrance_order = {
                Transitions.IslesMainToJapesLobby: Levels.JungleJapes,
                Transitions.IslesMainToAztecLobby: Levels.AngryAztec,
                Transitions.IslesMainToFactoryLobby: Levels.FranticFactory,
                Transitions.IslesMainToGalleonLobby: Levels.GloomyGalleon,
                Transitions.IslesMainToForestLobby: Levels.FungiForest,
                Transitions.IslesMainToCavesLobby: Levels.CrystalCaves,
                Transitions.IslesMainToCastleLobby: Levels.CreepyCastle,
                Transitions.IslesMainToHelmLobby: Levels.HideoutHelm,
            }
            lobby_exit_order = {
                Transitions.IslesJapesLobbyToMain: Levels.JungleJapes,
                Transitions.IslesAztecLobbyToMain: Levels.AngryAztec,
                Transitions.IslesFactoryLobbyToMain: Levels.FranticFactory,
                Transitions.IslesGalleonLobbyToMain: Levels.GloomyGalleon,
                Transitions.IslesForestLobbyToMain: Levels.FungiForest,
                Transitions.IslesCavesLobbyToMain: Levels.CrystalCaves,
                Transitions.IslesCastleLobbyToMain: Levels.CreepyCastle,
                Transitions.IslesHelmLobbyToMain: Levels.HideoutHelm,
            }
            for transition, vanilla_level in lobby_entrance_order.items():
                shuffled_level = lobby_exit_order[self.shuffled_exit_data[transition].reverse]
                shuffled_exits[vanilla_level.name] = shuffled_level.name
            humanspoiler["Shuffled Level Order"] = shuffled_exits
        elif self.settings.shuffle_loading_zones != ShuffleLoadingZones.none:
            # Show full shuffled_exits data if more than just levels are shuffled
            shuffled_exits = OrderedDict()
            level_starts = {
                "DK Isles": [
                    "DK Isles",
                    "Japes Lobby",
                    "Aztec Lobby",
                    "Factory Lobby",
                    "Galleon Lobby",
                    "Fungi Lobby",
                    "Caves Lobby",
                    "Castle Lobby",
                    "Helm Lobby",
                    "Snide's Room",
                    "Training Grounds",
                    "Banana Fairy Isle",
                    "DK's Treehouse",
                    "K-Lumsy",
                ],
                "Jungle Japes": ["Jungle Japes"],
                "Angry Aztec": ["Angry Aztec"],
                "Frantic Factory": ["Frantic Factory"],
                "Gloomy Galleon": ["Gloomy Galleon"],
                "Fungi Forest": ["Fungi Forest"],
                "Crystal Caves": ["Crystal Caves"],
                "Creepy Castle": ["Creepy Castle"],
                "Hideout Helm": ["Hideout Helm"],
            }
            level_data = {"Other": {}}
            for level in level_starts:
                level_data[level] = {}
            for exit, dest in self.shuffled_exit_data.items():
                level_name = "Other"
                for level in level_starts:
                    for search_name in level_starts[level]:
                        if dest.spoilerName.find(search_name) == 0:
                            level_name = level
                shuffled_exits[ShufflableExits[exit].name] = dest.spoilerName
                level_data[level_name][ShufflableExits[exit].name] = dest.spoilerName
            humanspoiler["Shuffled Exits"] = shuffled_exits
            humanspoiler["Shuffled Exits (Sorted by destination)"] = level_data
        if self.settings.has_password:
            PASS_NAMES = ["ERROR", "Up", "Down", "Left", "Right", "Z", "Start"]
            humanspoiler["Password"] = " ".join([PASS_NAMES[x] for x in self.settings.password])
        if self.settings.alter_switch_allocation:
            SLAM_NAMES = ["No Slam", "Simian Slam", "Super Simian Slam", "Super Duper Simian Slam"]
            humanspoiler["Level Switch Strength"] = {
                "Jungle Japes": SLAM_NAMES[self.settings.switch_allocation[Levels.JungleJapes]],
                "Angry Aztec": SLAM_NAMES[self.settings.switch_allocation[Levels.AngryAztec]],
                "Frantic Factory": SLAM_NAMES[self.settings.switch_allocation[Levels.FranticFactory]],
                "Gloomy Galleon": SLAM_NAMES[self.settings.switch_allocation[Levels.GloomyGalleon]],
                "Fungi Forest": SLAM_NAMES[self.settings.switch_allocation[Levels.FungiForest]],
                "Crystal Caves": SLAM_NAMES[self.settings.switch_allocation[Levels.CrystalCaves]],
                "Creepy Castle": SLAM_NAMES[self.settings.switch_allocation[Levels.CreepyCastle]],
            }
            if self.settings.shuffle_helm_location:
                humanspoiler["Level Switch Strength"]["Hideout Helm"] = SLAM_NAMES[self.settings.switch_allocation[Levels.HideoutHelm]]

        if len(self.microhints) > 0:
            human_microhints = {}
            for name, hint in self.microhints.items():
                filtered_hint = hint.replace("\x04", "")
                filtered_hint = filtered_hint.replace("\x05", "")
                filtered_hint = filtered_hint.replace("\x06", "")
                filtered_hint = filtered_hint.replace("\x07", "")
                filtered_hint = filtered_hint.replace("\x08", "")
                filtered_hint = filtered_hint.replace("\x09", "")
                filtered_hint = filtered_hint.replace("\x0a", "")
                filtered_hint = filtered_hint.replace("\x0b", "")
                filtered_hint = filtered_hint.replace("\x0c", "")
                filtered_hint = filtered_hint.replace("\x0d", "")
                human_microhints[name] = filtered_hint
            humanspoiler["Direct Item Hints"] = human_microhints
        if len(self.hint_list) > 0:
            human_hint_list = {}
            # Here it filters out the coloring from the hints to make it actually readable in the spoiler log
            for name, hint in self.hint_list.items():
                filtered_hint = hint.replace("\x04", "")
                filtered_hint = filtered_hint.replace("\x05", "")
                filtered_hint = filtered_hint.replace("\x06", "")
                filtered_hint = filtered_hint.replace("\x07", "")
                filtered_hint = filtered_hint.replace("\x08", "")
                filtered_hint = filtered_hint.replace("\x09", "")
                filtered_hint = filtered_hint.replace("\x0a", "")
                filtered_hint = filtered_hint.replace("\x0b", "")
                filtered_hint = filtered_hint.replace("\x0c", "")
                filtered_hint = filtered_hint.replace("\x0d", "")
                human_hint_list[name] = filtered_hint
            humanspoiler["Wrinkly Hints"] = human_hint_list
            # humanspoiler["Unhinted Score"] = self.unhinted_score
            # humanspoiler["Potentially Awful Locations"] = {}
            # for location_description in self.poor_scoring_locations:
            #     humanspoiler["Potentially Awful Locations"][location_description] = self.poor_scoring_locations[location_description]
            # if hasattr(self, "hint_swap_advisory"):
            #     humanspoiler["Hint Swap Advisory"] = self.hint_swap_advisory
        self.json = json.dumps(humanspoiler, indent=4)

    def UpdateKasplats(self, kasplat_map: Dict[Locations, Kongs]) -> None:
        """Update kasplat data."""
        for kasplat, kong in kasplat_map.items():
            # Get kasplat info
            location = self.LocationList[kasplat]
            mapId = location.map
            original = location.kong
            self.human_kasplats[location.name] = NameFromKong(kong)
            map = None
            # See if map already exists in enemy_replacements
            for m in self.enemy_replacements:
                if m["container_map"] == mapId:
                    map = m
                    break
            # If not, create it
            if map is None:
                map = {"container_map": mapId}
                self.enemy_replacements.append(map)
            # Create kasplat_swaps section if doesn't exist
            if "kasplat_swaps" not in map:
                map["kasplat_swaps"] = []
            # Create swap entry and add to map
            swap = {"vanilla_location": original, "replace_with": kong}
            map["kasplat_swaps"].append(swap)

    def UpdateBarrels(self) -> None:
        """Update list of shuffled barrel minigames."""
        self.shuffled_barrel_data = {}
        for location, minigame in [(key, value.minigame) for (key, value) in BarrelMetaData.items()]:
            self.shuffled_barrel_data[location] = minigame

    def UpdateExits(self) -> None:
        """Update list of shuffled exits."""
        self.shuffled_exit_data = {}
        containerMaps = {}
        for key, exit in ShufflableExits.items():
            if exit.shuffled:
                try:
                    vanillaBack = exit.back
                    shuffledBack = ShufflableExits[exit.shuffledId].back
                    self.shuffled_exit_data[key] = shuffledBack
                    containerMapId = GetMapId(self.settings, exit.region)
                    if containerMapId not in containerMaps:
                        containerMaps[containerMapId] = {"container_map": containerMapId, "zones": []}  # DK Isles
                    loading_zone_mapping = {}
                    loading_zone_mapping["vanilla_map"] = GetMapId(self.settings, vanillaBack.regionId)
                    loading_zone_mapping["vanilla_exit"] = GetExitId(vanillaBack)
                    loading_zone_mapping["new_map"] = GetMapId(self.settings, shuffledBack.regionId)
                    loading_zone_mapping["new_exit"] = GetExitId(shuffledBack)
                    containerMaps[containerMapId]["zones"].append(loading_zone_mapping)
                except Exception as ex:
                    print("Exit Update Error with:")
                    print(ex)
        for key, containerMap in containerMaps.items():
            self.shuffled_exit_instructions.append(containerMap)

    def UpdateLocations(self, locations: Dict[Locations, Location]) -> None:
        """Update location list for what was produced by the fill."""
        self.location_data = {}
        self.shuffled_kong_placement = {}
        # Go ahead and set starting kong
        startkong = {"kong": self.settings.starting_kong, "write": 0x151}
        trainingGrounds = {"locked": startkong}
        self.shuffled_kong_placement["TrainingGrounds"] = trainingGrounds
        # Write additional starting kongs to empty cages, if any
        emptyCages = [x for x in [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong] if x not in self.settings.kong_locations]
        for emptyCage in emptyCages:
            self.WriteKongPlacement(emptyCage, Items.NoItem)

        # Loop through locations and set necessary data
        for id, location in locations.items():
            # (There must be an item here) AND (It must not be a constant item expected to be here) AND (It must be in a location not handled by the full item rando shuffler)
            if location.item is not None and location.item is not Items.NoItem and not location.constant and location.type not in self.settings.shuffled_location_types:
                self.location_data[id] = location.item
                if location.type == Types.Shop:
                    # Get indices from the location
                    shop_index = 0  # cranky
                    if location.movetype in [MoveTypes.Guns, MoveTypes.AmmoBelt]:
                        shop_index = 1  # funky
                    elif location.movetype == MoveTypes.Instruments:
                        shop_index = 2  # candy
                    kong_indices = [location.kong]
                    if location.kong == Kongs.any:
                        kong_indices = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
                    level_index = location.level
                    # Isles level index is 8, but we need it to be 7 to fit it in move_data
                    if level_index == 8:
                        level_index = 7
                    # Use the item to find the data to write
                    updated_item = ItemList[location.item]
                    move_type = updated_item.movetype
                    # Determine Price
                    price = 0
                    if id in self.settings.prices:
                        price = self.settings.prices[id]
                    # Vanilla prices are by item, not by location
                    if self.settings.random_prices == RandomPrices.vanilla:
                        price = self.settings.prices[location.item]
                    # Moves that are set with a single flag (e.g. training barrels, shockwave) are handled differently
                    if move_type == MoveTypes.Flag:
                        for kong_index in kong_indices:
                            self.move_data[0][shop_index][kong_index][level_index] = {
                                "move_type": "flag",
                                "flag": updated_item.flag,
                                "price": price,
                            }
                    # This is for every other move typically purchased in a shop
                    else:
                        move_level = updated_item.index - 1
                        move_kong = updated_item.kong
                        for kong_index in kong_indices:
                            # print(f"Shop {shop_index}, Kong {kong_index}, Level {level_index} | Move: {move_type} lvl {move_level} for kong {move_kong}")
                            if (
                                move_type == MoveTypes.Slam
                                or move_type == MoveTypes.AmmoBelt
                                or (move_type == MoveTypes.Guns and move_level > 0)
                                or (move_type == MoveTypes.Instruments and move_level > 0)
                            ):
                                move_kong = kong_index
                            self.move_data[0][shop_index][kong_index][level_index] = {
                                "move_type": ["special", "slam", "gun", "ammo_belt", "instrument"][move_type],
                                "move_lvl": move_level,
                                "move_kong": move_kong,
                                "price": price,
                            }
                elif location.type == Types.Kong:
                    self.WriteKongPlacement(id, location.item)
                elif location.type == Types.TrainingBarrel and self.settings.training_barrels != TrainingBarrels.normal:
                    # Use the item to find the data to write
                    updated_item = ItemList[location.item]
                    move_type = updated_item.movetype
                    # Determine Price to be zero because this is a training barrel
                    price = 0
                    # Moves that are set with a single flag (e.g. training barrels, shockwave) are handled differently
                    if move_type == MoveTypes.Flag:
                        self.move_data[1].append({"move_type": "flag", "flag": updated_item.flag, "price": price})
                    # This is for every other move typically purchased in a shop
                    else:
                        move_level = updated_item.index - 1
                        move_kong = updated_item.kong
                        self.move_data[1].append(
                            {
                                "move_type": ["special", "slam", "gun", "ammo_belt", "instrument"][move_type],
                                "move_lvl": move_level,
                                "move_kong": move_kong % 5,  # Shared moves are 5 but should be 0
                                "price": price,
                            }
                        )
                    # Clean up the default value from this list
                    for x in range(len(self.move_data[1])):
                        if self.move_data[1][x] == {"move_type": None}:
                            del self.move_data[1][x]
                            break
                elif location.type == Types.Shockwave and self.settings.shockwave_status != ShockwaveStatus.vanilla:
                    # Use the item to find the data to write
                    updated_item = ItemList[location.item]
                    move_type = updated_item.movetype
                    # Determine Price to be zero because BFI is free
                    price = 0
                    # Moves that are set with a single flag (e.g. training barrels, shockwave) are handled differently
                    if move_type == MoveTypes.Flag:
                        self.move_data[2] = [{"move_type": "flag", "flag": updated_item.flag, "price": price}]
                    # This is for every other move typically purchased in a shop
                    else:
                        move_level = updated_item.index - 1
                        move_kong = updated_item.kong
                        self.move_data[2] = [
                            {
                                "move_type": ["special", "slam", "gun", "ammo_belt", "instrument"][move_type],
                                "move_lvl": move_level,
                                "move_kong": move_kong % 5,  # Shared moves are 5 but should be 0
                                "price": price,
                            }
                        ]
            # Uncomment for more verbose spoiler with all locations
            # else:
            #     self.location_data[id] = Items.NoItem

    def WriteKongPlacement(self, locationId: Locations, item: Items) -> None:
        """Write kong placement information for the given kong cage location."""
        locationName = "Jungle Japes"
        unlockKong = self.settings.diddy_freeing_kong
        lockedwrite = 0x152
        puzzlewrite = 0x153
        if locationId == Locations.LankyKong:
            locationName = "Llama Temple"
            unlockKong = self.settings.lanky_freeing_kong
            lockedwrite = 0x154
            puzzlewrite = 0x155
        elif locationId == Locations.TinyKong:
            locationName = "Tiny Temple"
            unlockKong = self.settings.tiny_freeing_kong
            lockedwrite = 0x156
            puzzlewrite = 0x157
        elif locationId == Locations.ChunkyKong:
            locationName = "Frantic Factory"
            unlockKong = self.settings.chunky_freeing_kong
            lockedwrite = 0x158
            puzzlewrite = 0x159
        lockedkong = {}
        lockedkong["kong"] = KongFromItem(item)
        lockedkong["write"] = lockedwrite
        puzzlekong = {"kong": unlockKong, "write": puzzlewrite}
        kongLocation = {"locked": lockedkong, "puzzle": puzzlekong}
        self.shuffled_kong_placement[locationName] = kongLocation

    def UpdatePlaythrough(self, locations: Dict[Locations, Location], playthroughLocations: List[Sphere]) -> None:
        """Write playthrough as a list of dicts of location/item pairs."""
        self.playthrough = {}
        i = 0
        for sphere in playthroughLocations:
            newSphere = {}
            newSphere["Available GBs"] = sphere.availableGBs
            sphereLocations = list(map(lambda l: locations[l], sphere.locations))
            sphereLocations.sort(key=self.ScoreLocations)
            for location in sphereLocations:
                newSphere[location.name] = ItemList[location.item].name
            self.playthrough[i] = newSphere
            i += 1

    def UpdateWoth(self, locations: Dict[Locations, Location], wothLocations: List[Union[Locations, int]]) -> None:
        """Write woth locations as a dict of location/item pairs."""
        self.woth = {}
        self.woth_locations = wothLocations
        for locationId in wothLocations:
            location = locations[locationId]
            self.woth[location.name] = ItemList[location.item].name

    def ScoreLocations(self, location: Location) -> int:
        """Score a location with the given settings for sorting the Playthrough."""
        # The Banana Hoard is likely in its own sphere but if it's not put it last
        if location == Locations.BananaHoard:
            return 250
        # GBs go last, there's a lot of them but they arent important
        if ItemList[location.item].type == Types.Banana:
            return 100
        win_con_type_table = {
            WinConditionComplex.req_bean: Types.Bean,
            WinConditionComplex.req_bp: Types.Blueprint,
            WinConditionComplex.req_companycoins: Types.NintendoCoin,  # Also Types.RarewareCoin
            WinConditionComplex.req_crown: Types.Crown,
            WinConditionComplex.req_fairy: Types.Fairy,
            WinConditionComplex.req_gb: Types.Banana,  # Also Types.ToughBanana
            # WinConditionComplex.req_key: Types.Key,
            WinConditionComplex.req_medal: Types.Medal,
            WinConditionComplex.req_pearl: Types.Pearl,
            WinConditionComplex.req_rainbowcoin: Types.RainbowCoin,
        }
        # Win condition items are more important than GBs but less than moves
        if self.settings.win_condition_item in win_con_type_table:
            if ItemList[location.item].type == win_con_type_table[self.settings.win_condition_item]:
                return 10
            if self.settings.win_condition_item == WinConditionComplex.req_companycoins:
                if ItemList[location.item].type == Types.RarewareCoin:
                    return 10
        # Kongs are most the single most important thing and should be at the top of spheres
        if ItemList[location.item].type == Types.Kong:
            return 0
        # Keys are best put first
        elif ItemList[location.item].type == Types.Key:
            return 1
        # Moves are pretty important
        elif ItemList[location.item].type == Types.Shop:
            return 2
        # Everything else here is probably something unusual so it's likely important
        else:
            return 3

    @staticmethod
    def GetKroolKeysRequired(keyEvents: List[Events]) -> List[str]:
        """Get key names from required key events to print in the spoiler."""
        keys = []
        if Events.JapesKeyTurnedIn in keyEvents:
            keys.append("Jungle Japes Key")
        if Events.AztecKeyTurnedIn in keyEvents:
            keys.append("Angry Aztec Key")
        if Events.FactoryKeyTurnedIn in keyEvents:
            keys.append("Frantic Factory Key")
        if Events.GalleonKeyTurnedIn in keyEvents:
            keys.append("Gloomy Galleon Key")
        if Events.ForestKeyTurnedIn in keyEvents:
            keys.append("Fungi Forest Key")
        if Events.CavesKeyTurnedIn in keyEvents:
            keys.append("Crystal Caves Key")
        if Events.CastleKeyTurnedIn in keyEvents:
            keys.append("Creepy Castle Key")
        if Events.HelmKeyTurnedIn in keyEvents:
            keys.append("Hideout Helm Key")
        return keys
