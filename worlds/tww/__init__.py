import os
import zipfile
from base64 import b64encode
from collections.abc import Mapping
from typing import Any, ClassVar, NamedTuple

import yaml

from BaseClasses import CollectionState, Item, ItemClassification as IC, MultiWorld, Region, Tutorial
from Options import Toggle
from worlds.AutoWorld import WebWorld, World
from worlds.Files import APPlayerContainer
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, icon_paths, launch_subprocess
from worlds.generic.Rules import add_item_rule

from .Items import ISLAND_NUMBER_TO_CHART_NAME, ITEM_TABLE, TWWItem, item_name_groups
from .Locations import LOCATION_TABLE, TWWFlag, TWWLocation
from .Options import TWWOptions, tww_option_groups
from .Presets import tww_options_presets
from .Rules import set_rules
from .randomizers.Charts import ISLAND_NUMBER_TO_NAME, ChartRandomizer
from .randomizers.Dungeons import Dungeon, create_dungeons
from .randomizers.Entrances import ALL_EXITS, BOSS_EXIT_TO_DUNGEON, MINIBOSS_EXIT_TO_DUNGEON, EntranceRandomizer
from .randomizers.ItemPool import generate_itempool
from .randomizers.RequiredBosses import RequiredBossesRandomizer

class DatastorageParsed(NamedTuple):
    """Parsed datastorage key for deferred entrance tracking."""
    team: int
    player: int
    stage_name: str


VERSION: tuple[int, int, int] = (3, 0, 0)

def run_client() -> None:
    """
    Launch the The Wind Waker client.
    """
    print("Running The Wind Waker Client")
    from .TWWClient import main

    launch_subprocess(main, name="TheWindWakerClient")


components.append(
    Component(
        "The Wind Waker Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".aptww"),
        icon="The Wind Waker",
    )
)
icon_paths["The Wind Waker"] = "ap:worlds.tww/assets/icon.png"


class TWWContainer(APPlayerContainer):
    """
    This class defines the container file for The Wind Waker.
    """

    game: str = "The Wind Waker"
    patch_file_ending: str = ".aptww"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "data" in kwargs:
            self.data = kwargs["data"]
            del kwargs["data"]

        super().__init__(*args, **kwargs)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        """
        Write the contents of the container file.
        """
        super().write_contents(opened_zipfile)

        # Record the data for the game under the key `plando`.
        opened_zipfile.writestr("plando", b64encode(bytes(yaml.safe_dump(self.data, sort_keys=False), "utf-8")))


class TWWWeb(WebWorld):
    """
    This class handles the web interface for The Wind Waker.

    The web interface includes the setup guide and the options page for generating YAMLs.
    """

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago The Wind Waker software on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["tanjo3", "Lunix"],
        ),
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago The Wind Waker software on your computer.",
            "Français",
            "setup_fr.md",
            "setup/fr",
            ["mobby45"]
        )
    ]
    theme = "ocean"
    options_presets = tww_options_presets
    option_groups = tww_option_groups
    rich_text_options_doc = True


class TWWWorld(World):
    """
    Legend has it that whenever evil has appeared, a hero named Link has arisen to defeat it. The legend continues on
    the surface of a vast and mysterious sea as Link sets sail in his most epic, awe-inspiring adventure yet. Aided by a
    magical conductor's baton called the Wind Waker, he will face unimaginable monsters, explore puzzling dungeons, and
    meet a cast of unforgettable characters as he searches for his kidnapped sister.
    """

    options_dataclass = TWWOptions
    options: TWWOptions

    game: ClassVar[str] = "The Wind Waker"
    topology_present: bool = True

    item_name_to_id: ClassVar[dict[str, int]] = {
        name: TWWItem.get_apid(data.code) for name, data in ITEM_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: TWWLocation.get_apid(data.code) for name, data in LOCATION_TABLE.items() if data.code is not None
    }

    item_name_groups: ClassVar[dict[str, set[str]]] = item_name_groups

    required_client_version: tuple[int, int, int] = (0, 5, 1)

    web: ClassVar[TWWWeb] = TWWWeb()

    origin_region_name: str = "The Great Sea"

    create_items = generate_itempool

    logic_rematch_bosses_skipped: bool
    logic_in_swordless_mode: bool
    logic_in_required_bosses_mode: bool
    logic_obscure_1: bool
    logic_obscure_2: bool
    logic_obscure_3: bool
    logic_precise_1: bool
    logic_precise_2: bool
    logic_precise_3: bool
    logic_tuner_logic_enabled: bool

    # Universal Tracker stuff, does not do anything in normal gen
    using_ut: bool # A way to check if Universal Tracker is active via early setting and forgetting
    glitches_item_name = "Glitched"
    ut_can_gen_without_yaml = True # class var that tells it to ignore the player yaml

    # Deferred entrances support for Universal Tracker
    # Mapping from game stage names (from memory) to region/exit names
    # This is used for deferred entrance tracking - when the client sends a visited stage,
    # we can map it to the corresponding entrance exit using this mapping.
    # Only includes stages that are actual entrance exit destinations from the 44 randomized entrances.
    # Based on stage names from https://github.com/LagoLunatic/wwrando/blob/master/data/stage_names.txt
    stage_name_to_exit: ClassVar[dict[str, str]] = {
        # Boss arenas (6 boss entrances)
        "M_DragB": "Gohma Boss Arena",
        "kinBOSS": "Kalle Demos Boss Arena",
        "SirenB": "Gohdan Boss Arena",
        "M2tower": "Helmaroc King Boss Arena",
        "M_DaiB": "Jalhalla Boss Arena",
        "kazeB": "Molgera Boss Arena",
        # Dungeon entrances (5)
        "M_NewD2": "Dragon Roost Cavern",
        "kindan": "Forbidden Woods",
        "Siren": "Tower of the Gods",
        "M_Dai": "Earth Temple",
        "kaze": "Wind Temple",
        # Miniboss arenas (5 miniboss entrances)
        "kinMB": "Forbidden Woods Miniboss Arena",
        "SirenMB": "Tower of the Gods Miniboss Arena",
        "M_DaiMB": "Earth Temple Miniboss Arena",
        "kazeMB": "Wind Temple Miniboss Arena",
        "kenroom": "Master Sword Chamber",
        # Secret cave entrances (20)
        "Cave09": "Savage Labyrinth",
        "Cave01": "Bomb Island Secret Cave",
        "Cave02": "Star Island Secret Cave",
        "Cave03": "Cliff Plateau Isles Secret Cave",
        "Cave04": "Rock Spire Isle Secret Cave",
        "Cave05": "Horseshoe Island Secret Cave",
        "Cave07": "Pawprint Isle Wizzrobe Cave",
        "TyuTyu": "Pawprint Isle Chuchu Cave",
        "SubD42": "Needle Rock Isle Secret Cave",
        "SubD43": "Angular Isles Secret Cave",
        "SubD71": "Boating Course Secret Cave",
        "TF_01": "Stone Watcher Island Secret Cave",
        "TF_02": "Overlook Island Secret Cave",
        "TF_03": "Bird's Peak Rock Secret Cave",
        "TF_06": "Dragon Roost Island Secret Cave",
        "MiniKaz": "Fire Mountain Secret Cave",
        "MiniHyo": "Ice Ring Isle Secret Cave",
        "ITest63": "Shark Island Secret Cave",
        "Cave03": "Cliff Plateau Isles Secret Cave",
        "WarpD": "Diamond Steppe Island Warp Maze Cave",
        # Secret cave inner entrances (2)
        "ITest62": "Ice Ring Isle Inner Cave",
        "CliPlaH": "Cliff Plateau Isles Inner Cave",
        # Fairy fountain entrances (6)
        "Fairy01": "Northern Fairy Fountain",
        "Fairy02": "Eastern Fairy Fountain",
        "Fairy03": "Western Fairy Fountain",
        "Fairy04": "Outset Fairy Fountain",
        "Fairy05": "Thorned Fairy Fountain",
        "Fairy06": "Southern Fairy Fountain",
    }

    # List of datastorage keys that UT will track for deferred entrance reconnection
    # Format: tww_{team}_{player}_{stagename}
    # This is populated dynamically when entrances are disconnected
    found_entrances_datastorage_key: list[str] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.progress_locations: set[str] = set()
        self.nonprogress_locations: set[str] = set()

        self.dungeon_local_item_names: set[str] = set()
        self.dungeon_specific_item_names: set[str] = set()
        self.dungeons: dict[str, Dungeon] = {}

        self.item_classification_overrides: dict[str, IC] = {}

        self.useful_pool: list[str] = []
        self.filler_pool: list[str] = []

        self.charts = ChartRandomizer(self)
        self.entrances = EntranceRandomizer(self)
        self.boss_reqs = RequiredBossesRandomizer(self)

        # Deferred entrance tracking
        self.disconnected_entrances: dict[Any, Any] = {}

        # Track whether charts/entrances/required bosses were restored from UT slot_data
        self._charts_restored_from_ut = False
        self._entrances_restored_from_ut = False
        self._required_bosses_restored_from_ut = False

    def _determine_item_classification_overrides(self) -> None:
        """
        Determine item classification overrides. The classification of an item may be affected by which options are
        enabled or disabled.
        """
        options = self.options
        item_classification_overrides = self.item_classification_overrides

        # Override certain items to be filler depending on user options.
        # TODO: Calculate filler items dynamically
        override_as_filler = []
        if not options.progression_dungeons:
            override_as_filler.extend(item_name_groups["Small Keys"] | item_name_groups["Big Keys"])
            override_as_filler.extend(("Command Melody", "Earth God's Lyric", "Wind God's Aria"))
        if not options.progression_short_sidequests:
            override_as_filler.extend(("Maggie's Letter", "Moblin's Letter"))
        if not (options.progression_short_sidequests or options.progression_long_sidequests):
            override_as_filler.append("Progressive Picto Box")
        if not options.progression_spoils_trading:
            override_as_filler.append("Spoils Bag")
        if not options.progression_triforce_charts:
            override_as_filler.extend(item_name_groups["Triforce Charts"])
        if not options.progression_treasure_charts:
            override_as_filler.extend(item_name_groups["Treasure Charts"])
        if not options.progression_misc:
            override_as_filler.extend(item_name_groups["Tingle Statues"])

        for item_name in override_as_filler:
            item_classification_overrides[item_name] = IC.filler

        # Override certain items to be useful depending on user options.
        # TODO: Calculate useful items dynamically
        override_as_useful = []
        if not options.progression_big_octos_gunboats:
            override_as_useful.append("Quiver Capacity Upgrade")
        if options.sword_mode in ("swords_optional", "swordless"):
            override_as_useful.append("Progressive Sword")
        if not options.enable_tuner_logic:
            override_as_useful.append("Tingle Tuner")

        for item_name in override_as_useful:
            item_classification_overrides[item_name] = IC.useful

    def _determine_progress_and_nonprogress_locations(self) -> tuple[set[str], set[str]]:
        """
        Determine which locations are progress and nonprogress in the world based on the player's options.

        :return: A tuple of two sets, the first containing the names of the progress locations and the second containing
        the names of the nonprogress locations.
        """

        def add_flag(option: Toggle, flag: TWWFlag) -> TWWFlag:
            return flag if option else TWWFlag.ALWAYS

        options = self.options

        enabled_flags = TWWFlag.ALWAYS
        enabled_flags |= add_flag(options.progression_dungeons, TWWFlag.DUNGEON | TWWFlag.BOSS)
        enabled_flags |= add_flag(options.progression_tingle_chests, TWWFlag.TNGL_CT)
        enabled_flags |= add_flag(options.progression_dungeon_secrets, TWWFlag.DG_SCRT)
        enabled_flags |= add_flag(options.progression_puzzle_secret_caves, TWWFlag.PZL_CVE)
        enabled_flags |= add_flag(options.progression_combat_secret_caves, TWWFlag.CBT_CVE)
        enabled_flags |= add_flag(options.progression_savage_labyrinth, TWWFlag.SAVAGE)
        enabled_flags |= add_flag(options.progression_great_fairies, TWWFlag.GRT_FRY)
        enabled_flags |= add_flag(options.progression_short_sidequests, TWWFlag.SHRT_SQ)
        enabled_flags |= add_flag(options.progression_long_sidequests, TWWFlag.LONG_SQ)
        enabled_flags |= add_flag(options.progression_spoils_trading, TWWFlag.SPOILS)
        enabled_flags |= add_flag(options.progression_minigames, TWWFlag.MINIGME)
        enabled_flags |= add_flag(options.progression_battlesquid, TWWFlag.SPLOOSH)
        enabled_flags |= add_flag(options.progression_free_gifts, TWWFlag.FREE_GF)
        enabled_flags |= add_flag(options.progression_mail, TWWFlag.MAILBOX)
        enabled_flags |= add_flag(options.progression_platforms_rafts, TWWFlag.PLTFRMS)
        enabled_flags |= add_flag(options.progression_submarines, TWWFlag.SUBMRIN)
        enabled_flags |= add_flag(options.progression_eye_reef_chests, TWWFlag.EYE_RFS)
        enabled_flags |= add_flag(options.progression_big_octos_gunboats, TWWFlag.BG_OCTO)
        enabled_flags |= add_flag(options.progression_expensive_purchases, TWWFlag.XPENSVE)
        enabled_flags |= add_flag(options.progression_island_puzzles, TWWFlag.ISLND_P)
        enabled_flags |= add_flag(options.progression_misc, TWWFlag.MISCELL)

        progress_locations: set[str] = set()
        nonprogress_locations: set[str] = set()
        for location, data in LOCATION_TABLE.items():
            if data.flags & enabled_flags == data.flags:
                progress_locations.add(location)
            else:
                nonprogress_locations.add(location)
        assert progress_locations.isdisjoint(nonprogress_locations)

        return progress_locations, nonprogress_locations

    @staticmethod
    def _get_classification_name(classification: IC) -> str:
        """
        Return a string representation of the item's highest-order classification.

        :param classification: The item's classification.
        :return: A string representation of the item's highest classification. The order of classification is
        progression > trap > useful > filler.
        """

        if IC.progression in classification:
            return "progression"
        elif IC.trap in classification:
            return "trap"
        elif IC.useful in classification:
            return "useful"
        else:
            return "filler"

    def _restore_options_from_ut_slot_data(self, slot_data: dict[str, Any]) -> None:
        """
        Restore all seed-affecting options from slot_data during UT regeneration.

        This method is called during UT's internal regeneration to restore the options
        that were used in the original seed generation. This must happen before any
        option-dependent logic runs in generate_early().

        NOTE: This method restores both OPTIONS and chart mappings from slot_data.
        The entrances and required_bosses will be recalculated during the current regeneration
        since UT's random state differs from the original generation.

        :param slot_data: The slot_data dictionary from re_gen_passthrough.
        """
        # NOTE: required_bosses, charts, and entrances must be restored from the original generation
        # to keep UT in sync with the server's world state.

        if "entrances" in slot_data:
            self._restore_entrance_mappings_from_slot_data(slot_data["entrances"])

        if "charts" in slot_data:
            self._restore_chart_mappings_from_slot_data(slot_data["charts"])

        if "required_boss_item_locations" in slot_data:
            self._restore_required_bosses_from_slot_data(slot_data["required_boss_item_locations"])

        options_restored = []
        options_failed = []

        for key, value in slot_data.items():
            if key == "charts" or key == "entrances" or key == "required_boss_item_locations":
                continue

            try:
                # Get the option from the options dataclass
                opt: Any | None = getattr(self.options, key, None)
                if opt is not None:
                    # Use from_any() to properly deserialize the value
                    # This works for both regular options and OptionSets
                    setattr(self.options, key, opt.from_any(value))
                    options_restored.append(key)
                else:
                    options_failed.append(key)
            except Exception as e:
                options_failed.append(key)

    def _restore_entrance_mappings_from_slot_data(self, entrances_mapping: dict[str, str]) -> None:
        """
        Restore entrance mappings from the server's original generation.

        This prevents UT from re-randomizing entrances with its own random state, which would
        cause the tracker to show different entrance destinations than the actual game world.

        The entrances_mapping dict maps entrance names to exit names from the server's generation.
        We apply these to done_entrances_to_exits before create_regions() randomizes them.

        :param entrances_mapping: Dict from slot_data["entrances"]
        """
        try:
            from .randomizers.Entrances import ZoneEntrance, ZoneExit

            # Apply the server's entrance mappings to override the default mappings
            for entrance_name, exit_name in entrances_mapping.items():
                zone_entrance = ZoneEntrance.all.get(entrance_name)
                zone_exit = ZoneExit.all.get(exit_name)

                if zone_entrance and zone_exit:
                    self.entrances.done_entrances_to_exits[zone_entrance] = zone_exit
                    self.entrances.done_exits_to_entrances[zone_exit] = zone_entrance

            # Mark that entrances have been pre-loaded from UT so we won't re-randomize them
            self._entrances_restored_from_ut = True
            self.entrances.skip_randomization = True
        except Exception as e:
            pass

    def _restore_chart_mappings_from_slot_data(self, charts_mapping: list[int]) -> None:
        """
        Restore chart mappings from the server's original generation.

        This prevents UT from re-randomizing charts with its own random state, which would
        cause the tracker to show different locations than the actual game world.

        The charts_mapping is a list where charts_mapping[i-1] is the island that the chart
        originally at island i now points to (after the server's randomization).

        We invert this to set island_number_to_chart_name correctly.

        :param charts_mapping: List from slot_data["charts"]
        """
        try:
            # Reset to default state first
            self.charts.island_number_to_chart_name = ISLAND_NUMBER_TO_CHART_NAME.copy()

            # For each original island position, find which island its chart ended up at
            for original_island in range(1, 50):  # Islands 1-49
                original_chart_name = ISLAND_NUMBER_TO_CHART_NAME[original_island]
                new_island = charts_mapping[original_island - 1]

                # Restore the mapping: the chart originally at original_island is now at new_island
                self.charts.island_number_to_chart_name[new_island] = original_chart_name

            # Mark that charts were restored from UT so we skip randomization
            self._charts_restored_from_ut = True
            self.charts.skip_randomization = True
        except Exception as e:
            pass

    def _restore_required_bosses_from_slot_data(self, required_boss_item_locations: dict[str, str]) -> None:
        """
        Restore required boss item locations from the server's original generation.

        This prevents UT from re-randomizing required bosses with its own random state, which would
        cause the tracker to show different boss locations than the actual game world.

        :param required_boss_item_locations: Dict from slot_data["required_bosses"]
        """
        try:
            # Directly restore the required boss locations from the server
            self.boss_reqs.required_boss_item_locations = required_boss_item_locations

            # Mark that required bosses have been pre-loaded from UT so we won't re-randomize them
            self._required_bosses_restored_from_ut = True
            self.boss_reqs.skip_randomization = True
        except Exception as e:
            pass

    def generate_early(self) -> None:
        """
        Run before any general steps of the MultiWorld other than options.
        """
        # Handle Universal Tracker Support FIRST - before any option-dependent logic
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        self.using_ut = re_gen_passthrough and self.game in re_gen_passthrough

        if self.using_ut:
            # Restore options from slot_data during UT regeneration
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            self._restore_options_from_ut_slot_data(slot_data)

        # Now continue with normal generation using the restored (or default) options
        options = self.options

        # Only randomize secret cave inner entrances if both puzzle secret caves and combat secret caves are enabled.
        if not (options.progression_puzzle_secret_caves and options.progression_combat_secret_caves):
            options.randomize_secret_cave_inner_entrances.value = False

        # Determine which locations are progression and which are not from options.
        self.progress_locations, self.nonprogress_locations = self._determine_progress_and_nonprogress_locations()

        for dungeon_item in ["randomize_smallkeys", "randomize_bigkeys", "randomize_mapcompass"]:
            option = getattr(options, dungeon_item)
            if option == "local":
                options.local_items.value |= self.item_name_groups[option.item_name_group]
            elif option.in_dungeon:
                self.dungeon_local_item_names |= self.item_name_groups[option.item_name_group]
                if option == "dungeon":
                    self.dungeon_specific_item_names |= self.item_name_groups[option.item_name_group]
                else:
                    options.local_items.value |= self.dungeon_local_item_names

        # Resolve logic options and set them onto the world instance for faster lookup in logic rules.
        self.logic_rematch_bosses_skipped = bool(options.skip_rematch_bosses.value)
        self.logic_in_swordless_mode = options.sword_mode in ("swords_optional", "swordless")
        self.logic_in_required_bosses_mode = bool(options.required_bosses.value)
        self.logic_obscure_3 = options.logic_obscurity == "very_hard"
        self.logic_obscure_2 = self.logic_obscure_3 or options.logic_obscurity == "hard"
        self.logic_obscure_1 = self.logic_obscure_2 or options.logic_obscurity == "normal"
        self.logic_precise_3 = options.logic_precision == "very_hard"
        self.logic_precise_2 = self.logic_precise_3 or options.logic_precision == "hard"
        self.logic_precise_1 = self.logic_precise_2 or options.logic_precision == "normal"
        self.logic_tuner_logic_enabled = bool(options.enable_tuner_logic.value)

        # Determine any item classification overrides based on user options.
        self._determine_item_classification_overrides()

    def create_regions(self) -> None:
        """
        Create and connect regions for the The Wind Waker world.

        This method first randomizes the charts and picks the required bosses if these options are enabled.
        It then loops through all the world's progress locations and creates the locations, assigning dungeon locations
        to their respective dungeons.
        Finally, the flags for sunken treasure locations are updated as appropriate, and the entrances are randomized
        if that option is enabled.
        """
        multiworld = self.multiworld
        player = self.player
        options = self.options

        # "The Great Sea" region contains all locations that are not in a randomizable region.
        great_sea_region = Region("The Great Sea", player, multiworld)
        multiworld.regions.append(great_sea_region)

        # Add all randomizable regions.
        for _exit in ALL_EXITS:
            multiworld.regions.append(Region(_exit.unique_name, player, multiworld))

        # Set up sunken treasure locations, randomizing the charts if necessary.
        self.charts.setup_progress_sunken_treasure_locations()

        # Select required bosses.
        if options.required_bosses:
            self.boss_reqs.randomize_required_bosses()
            self.progress_locations -= self.boss_reqs.banned_locations
            self.nonprogress_locations |= self.boss_reqs.banned_locations

        # Create the dungeon classes.
        create_dungeons(self)

        # Assign each location to their region.
        # Progress locations are sorted for deterministic results.
        for location_name in sorted(self.progress_locations):
            data = LOCATION_TABLE[location_name]

            region = self.get_region(data.region)
            location = TWWLocation(player, location_name, region, data)

            # Additionally, assign dungeon locations to the appropriate dungeon.
            if region.name in self.dungeons:
                location.dungeon = self.dungeons[region.name]
            elif region.name in MINIBOSS_EXIT_TO_DUNGEON and not options.randomize_miniboss_entrances:
                location.dungeon = self.dungeons[MINIBOSS_EXIT_TO_DUNGEON[region.name]]
            elif region.name in BOSS_EXIT_TO_DUNGEON and not options.randomize_boss_entrances:
                location.dungeon = self.dungeons[BOSS_EXIT_TO_DUNGEON[region.name]]
            elif location.name in [
                "Forsaken Fortress - Phantom Ganon",
                "Forsaken Fortress - Chest Outside Upper Jail Cell",
                "Forsaken Fortress - Chest Inside Lower Jail Cell",
                "Forsaken Fortress - Chest Guarded By Bokoblin",
                "Forsaken Fortress - Chest on Bed",
            ]:
                location.dungeon = self.dungeons["Forsaken Fortress"]
            region.locations.append(location)

        # Correct the flags of the sunken treasure locations if the charts are randomized.
        self.charts.update_chart_location_flags()

        # Connect the regions in the multiworld. Randomize entrances to exits if the option is set.
        self.entrances.randomize_entrances()

        # Handle deferred entrance disconnection for Universal Tracker if enabled
        self.connect_entrances()

    def set_rules(self) -> None:
        """
        Set access and item rules on locations.
        """
        # Set the access rules for all progression locations.
        set_rules(self)

        # Ban the Bait Bag slot from having bait.
        # Beedle's shop does not work correctly if the same item is in multiple slots in the same shop.
        if "The Great Sea - Beedle's Shop Ship - 20 Rupee Item" in self.progress_locations:
            beedle_20 = self.get_location("The Great Sea - Beedle's Shop Ship - 20 Rupee Item")
            add_item_rule(beedle_20, lambda item: item.name not in ["All-Purpose Bait", "Hyoi Pear"])

        # For the same reason, the same item should not appear more than once on the Rock Spire Isle shop ship.
        # All non-TWW items use the same item (Father's Letter), so at most one non-TWW item can appear in the shop.
        # The rest must be (unique, but not necessarily local) TWW items.
        locations = [f"Rock Spire Isle - Beedle's Special Shop Ship - {v} Rupee Item" for v in [500, 950, 900]]
        if all(loc in self.progress_locations for loc in locations):
            rock_spire_shop_ship_locations = [self.get_location(location_name) for location_name in locations]

            for i in range(len(rock_spire_shop_ship_locations)):
                curr_loc = rock_spire_shop_ship_locations[i]
                other_locs = rock_spire_shop_ship_locations[:i] + rock_spire_shop_ship_locations[i + 1:]

                add_item_rule(
                    curr_loc,
                    lambda item, locations=other_locs: (
                        item.game == "The Wind Waker"
                        and all(location.item is None or item.name != location.item.name for location in locations)
                    )
                    or (
                        item.game != "The Wind Waker"
                        and all(
                            location.item is None or location.item.game == "The Wind Waker" for location in locations
                        )
                    ),
                )

    @classmethod
    def stage_set_rules(cls, multiworld: MultiWorld) -> None:
        """
        Class method used to modify the rules for The Wind Waker dungeon locations.

        :param multiworld: The MultiWorld.
        """
        from .randomizers.Dungeons import modify_dungeon_location_rules

        # Set additional rules on dungeon locations as necessary.
        modify_dungeon_location_rules(multiworld)

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld) -> None:
        """
        Class method used to correctly place dungeon items for The Wind Waker worlds.

        :param multiworld: The MultiWorld.
        """
        from .randomizers.Dungeons import fill_dungeons_restrictive

        fill_dungeons_restrictive(multiworld)

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output APTWW file that is used to randomize the ISO.

        :param output_directory: The output directory for the APTWW file.
        """
        multiworld = self.multiworld
        player = self.player

        # Determine the current arrangement for charts.
        # Create a list where the original island number is the index, and the value is the new island number.
        # Without randomized charts, this array would be just an ordered list of the numbers 1 to 49.
        # With randomized charts, the new island number is where the chart for the original island now leads.
        chart_name_to_island_number = {
            chart_name: island_number for island_number, chart_name in self.charts.island_number_to_chart_name.items()
        }
        charts_mapping: list[int] = []
        for i in range(1, 49 + 1):
            original_chart_name = ISLAND_NUMBER_TO_CHART_NAME[i]
            new_island_number = chart_name_to_island_number[original_chart_name]
            charts_mapping.append(new_island_number)

        # Output seed name and slot number to seed RNG in randomizer client.
        output_data = {
            "Version": list(VERSION),
            "Seed": multiworld.seed_name,
            "Slot": player,
            "Name": self.player_name,
            "Options": self.options.get_output_dict(),
            "Required Bosses": self.boss_reqs.required_boss_item_locations,
            "Locations": {},
            "Entrances": {},
            "Charts": charts_mapping,
        }

        # Output which item has been placed at each location.
        output_locations = output_data["Locations"]
        locations = multiworld.get_locations(player)
        for location in locations:
            if location.name != "Defeat Ganondorf":
                if location.item:
                    item_info = {
                        "player": location.item.player,
                        "name": location.item.name,
                        "game": location.item.game,
                        "classification": self._get_classification_name(location.item.classification),
                    }
                else:
                    item_info = {"name": "Nothing", "game": "The Wind Waker", "classification": "filler"}
                output_locations[location.name] = item_info

        # Output the mapping of entrances to exits.
        output_entrances = output_data["Entrances"]
        for zone_entrance, zone_exit in self.entrances.done_entrances_to_exits.items():
            output_entrances[zone_entrance.entrance_name] = zone_exit.unique_name

        # Output the plando details to file.
        aptww = TWWContainer(
            path=os.path.join(
                output_directory, f"{multiworld.get_out_file_name_base(player)}{TWWContainer.patch_file_ending}"
            ),
            player=player,
            player_name=self.player_name,
            data=output_data,
        )
        aptww.write()

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        """
        Fill in additional information text into locations, displayed when hinted.

        :param hint_data: A dictionary of mapping a player ID to a dictionary mapping location IDs to the extra hint
        information text. This dictionary should be modified as a side-effect of this method.
        """
        # Create a mapping of island names to numbers for sunken treasure hints.
        island_name_to_number = {v: k for k, v in ISLAND_NUMBER_TO_NAME.items()}

        hint_data[self.player] = {}
        for location in self.multiworld.get_locations(self.player):
            if location.address is not None and location.item is not None:
                # Regardless of ER settings, always hint at the outermost entrance for every "interior" location.
                zone_exit = self.entrances.get_zone_exit_for_item_location(location.name)
                if zone_exit is not None:
                    outermost_entrance = self.entrances.get_outermost_entrance_for_exit(zone_exit)
                    assert outermost_entrance is not None and outermost_entrance.island_name is not None
                    hint_data[self.player][location.address] = outermost_entrance.island_name

                # Hint at which chart leads to the sunken treasure for these locations.
                if location.name.endswith(" - Sunken Treasure"):
                    island_name = location.name.removesuffix(" - Sunken Treasure")
                    island_number = island_name_to_number[island_name]
                    chart_name = self.charts.island_number_to_chart_name[island_number]
                    hint_data[self.player][location.address] = chart_name

    def create_item(self, name: str) -> TWWItem:
        """
        Create an item for this world type and player.

        :param name: The name of the item to create.
        :raises KeyError: If an invalid item name is provided.
        """
        if name in ITEM_TABLE:
            return TWWItem(name, self.player, ITEM_TABLE[name], self.item_classification_overrides.get(name))
        raise KeyError(f"Invalid item name: {name}")

    def get_filler_item_name(self, strict: bool = True) -> str:
        """
        This method is called when the item pool needs to be filled with additional items to match the location count.

        :param strict: Whether the item should be one strictly classified as filler. Defaults to `True`.
        :return: The name of a filler item from this world.
        """
        # If there are still useful items to place, place those first.
        if not strict and len(self.useful_pool) > 0:
            return self.useful_pool.pop()

        # If there are still vanilla filler items to place, place those first.
        if len(self.filler_pool) > 0:
            return self.filler_pool.pop()

        # Use the same weights for filler items used in the base randomizer.
        filler_consumables = ["Yellow Rupee", "Red Rupee", "Purple Rupee", "Joy Pendant"]
        filler_weights = [3, 7, 10, 3]
        if not strict:
            filler_consumables.append("Orange Rupee")
            filler_weights.append(15)
        return self.multiworld.random.choices(filler_consumables, weights=filler_weights, k=1)[0]

    def get_pre_fill_items(self) -> list[Item]:
        """
        Return items that need to be collected when creating a fresh `all_state` but don't exist in the multiworld's
        item pool.

        :return: A list of pre-fill items.
        """
        res = []
        if self.dungeon_local_item_names:
            for dungeon in self.dungeons.values():
                for item in dungeon.all_items:
                    if item.name in self.dungeon_local_item_names:
                        res.append(item)
        return res

    def fill_slot_data(self) -> Mapping[str, Any]:
        """
        Return the `slot_data` field that will be in the `Connected` network package.

        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        For Universal Tracker integration, this method includes:
        - All seed-affecting options via self.options.get_slot_data_dict()
        - Entrance mappings for entrance randomization
        - Deferred entrance datastorage keys (for Universal Tracker to hide unrevealed entrances)
        - Chart mappings for sunken treasure location tracking
        - Required boss locations for required bosses mode

        :return: A dictionary to be sent to the client when it connects to the server.
        """
        slot_data = self.options.get_slot_data_dict()

        # Add entrances to `slot_data`. This is the same data that is written to the .aptww file.
        # For deferred entrances, exclude them from slot_data so Universal Tracker doesn't
        # display them initially.
        deferred_entrance_names = set()
        if hasattr(self, 'disconnected_entrances'):
            # Build set of entrance names that are deferred
            # Extract deferred entrance names from disconnected_entrances
            disconnected_entrance_names_only = {
                entrance.name.split(" -> ")[0] if " -> " in entrance.name else entrance.name
                for entrance in self.disconnected_entrances.keys()
            }

            deferred_entrance_names = {
                zone_entrance.entrance_name
                for zone_entrance in self.entrances.done_entrances_to_exits.keys()
                if zone_entrance.entrance_name in disconnected_entrance_names_only
            }

        entrances = {
            zone_entrance.entrance_name: zone_exit.unique_name
            for zone_entrance, zone_exit in self.entrances.done_entrances_to_exits.items()
            if zone_entrance.entrance_name not in deferred_entrance_names
        }
        slot_data["entrances"] = entrances

        # Add deferred entrance tracking keys for Universal Tracker
        # These keys should be initially hidden from the tracker until the datastorage key is revealed
        if hasattr(self, 'found_entrances_datastorage_key') and self.found_entrances_datastorage_key:
            slot_data["deferred_entrance_keys"] = self.found_entrances_datastorage_key

        # Add chart mapping for sunken treasure randomization.
        # Create a list where the original island number is the index, and the value is the new island number.
        # This is needed for UT to correctly track sunken treasure locations.
        chart_name_to_island_number = {
            chart_name: island_number for island_number, chart_name in self.charts.island_number_to_chart_name.items()
        }
        charts_mapping: list[int] = []
        for i in range(1, 49 + 1):
            original_chart_name = ISLAND_NUMBER_TO_CHART_NAME[i]
            new_island_number = chart_name_to_island_number[original_chart_name]
            charts_mapping.append(new_island_number)
        slot_data["charts"] = charts_mapping

        # Add required bosses information.
        slot_data["required_boss_item_locations"] = self.boss_reqs.required_boss_item_locations
        return slot_data

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> dict[str, Any]:
        """
        Interpret the slot data from the server and return it for UT regeneration.

        This method is called when UT connects to the server and receives slot data.
        By returning the slot_data dict, we tell UT to do a regeneration, which will then
        call generate_early() with the slot_data available in re_gen_passthrough.

        :param slot_data: The slot data dictionary from the server.
        :return: The slot_data unchanged, for UT's regeneration.
        """
        return slot_data

    @staticmethod
    def _extract_entrance_name(full_entrance_name: str) -> str:
        """
        Extract just the entrance name, removing the '-> Region' part.

        :param full_entrance_name: The full entrance name (e.g., "Entrance -> Region").
        :return: Just the entrance name part (e.g., "Entrance").
        """
        separator = " -> "
        return full_entrance_name.split(separator)[0] if separator in full_entrance_name else full_entrance_name

    @staticmethod
    def _format_datastorage_key(team: int, player: int, stage_name: str) -> str:
        """
        Format a datastorage key for deferred entrance tracking.

        :param team: The team number.
        :param player: The player number.
        :param stage_name: The stage name visited by the player.
        :return: The formatted datastorage key.
        """
        return f"tww_{team}_{player}_{stage_name}"

    @staticmethod
    def _parse_datastorage_key(key: str) -> DatastorageParsed | None:
        """
        Parse a datastorage key and return parsed components or None if invalid.

        Expected format: tww_<team>_<player>_<stagename>

        :param key: The datastorage key to parse.
        :return: DatastorageParsed with team, player, stage_name, or None if invalid.
        """
        parts = key.split("_")
        min_parts = 4
        if len(parts) < min_parts or parts[0] != "tww":
            return None
        try:
            team = int(parts[1])
            player = int(parts[2])
            stage_name = "_".join(parts[3:])
            return DatastorageParsed(team=team, player=player, stage_name=stage_name)
        except (ValueError, IndexError):
            return None

    def connect_entrances(self) -> None:
        """
        Connect entrances with deferred entrance support for Universal Tracker.

        During UT regeneration with enforce_deferred_connections enabled on the server,
        entrances are disconnected so they're not revealed until the player visits areas.
        """
        if self._should_defer_entrances():
            self._disconnect_entrances()

    def _should_defer_entrances(self) -> bool:
        """
        Check if entrances should be deferred based on UT and server settings.

        :return: True if entrances should be deferred, False otherwise.
        """
        # Only defer entrances during UT regeneration
        if not hasattr(self.multiworld, "generation_is_fake"):
            return False

        # Check if server has deferred connections enabled
        deferred_enabled = getattr(
            self.multiworld,
            "enforce_deferred_connections",
            None
        ) in ("on", "default")

        # Only defer if entrances are actually randomized
        has_randomized_entrances = bool(self.entrances.done_entrances_to_exits)

        return deferred_enabled and has_randomized_entrances

    def _disconnect_entrances(self) -> None:
        """
        Disconnect all randomized entrances to enable deferred spoilers.

        When entrances are disconnected, existing trackers will either display nothing or a fallback
        to indicate that an entrance has not been found yet. The use of reconnect_found_entrances
        will restore these connections.

        Only entrances from enabled entrance pools will be disconnected. If a pool is not shuffled
        (e.g., secret caves when only dungeons are randomized), those entrances remain connected
        and fully visible in the tracker.

        This method populates:
        - self.disconnected_entrances: Dict mapping entrance objects to their original regions
        - self.found_entrances_datastorage_key: List of datastorage keys for UT tracking
        """
        from .randomizers.Entrances import (
            DUNGEON_ENTRANCES, MINIBOSS_ENTRANCES, BOSS_ENTRANCES,
            SECRET_CAVE_ENTRANCES, SECRET_CAVE_INNER_ENTRANCES, FAIRY_FOUNTAIN_ENTRANCES
        )

        # Only initialize on first call; if already disconnected, don't reinitialize
        if not hasattr(self, 'disconnected_entrances'):
            self.disconnected_entrances = {}
        if not hasattr(self, 'found_entrances_datastorage_key'):
            self.found_entrances_datastorage_key = []
        # If we've already disconnected entrances in this generation, skip re-disconnecting
        if len(self.disconnected_entrances) > 0:
            return

        # Determine which entrance pools are enabled based on options
        # Use DRY approach to avoid code repetition
        entrance_pool_config = [
            (self.options.randomize_dungeon_entrances, DUNGEON_ENTRANCES),
            (self.options.randomize_miniboss_entrances, MINIBOSS_ENTRANCES),
            (self.options.randomize_boss_entrances, BOSS_ENTRANCES),
            (self.options.randomize_secret_cave_entrances, SECRET_CAVE_ENTRANCES),
            (self.options.randomize_secret_cave_inner_entrances, SECRET_CAVE_INNER_ENTRANCES),
            (self.options.randomize_fairy_fountain_entrances, FAIRY_FOUNTAIN_ENTRANCES),
        ]
        enabled_pools = {
            e.entrance_name
            for option_enabled, entrance_pool in entrance_pool_config
            if option_enabled
            for e in entrance_pool
        }

        # Build a set of randomized entrance names that are in ENABLED pools only
        randomized_entrance_names = {zone_entrance.entrance_name
                                     for zone_entrance in self.entrances.done_entrances_to_exits.keys()
                                     if zone_entrance.entrance_name in enabled_pools}

        # Get all actual entrances
        all_entrances = list(self.get_entrances())
        if len(all_entrances) == 0:
            return

        # Get team and player info for datastorage keys
        team = getattr(self.multiworld, "team", 0)
        player = self.player

        # Disconnect matching entrances and store mappings
        for entrance in all_entrances:
            # Extract just the entrance name (before the "->") for matching
            # Entrance objects have names like "Dungeon Entrance on Dragon Roost Island -> Forbidden Woods"
            entrance_name_only = self._extract_entrance_name(entrance.name)

            if entrance.connected_region and entrance_name_only in randomized_entrance_names:
                original_region = entrance.connected_region
                self.disconnected_entrances[entrance] = original_region

                # Extract stage name from entrance's destination region
                # We need to find which stage_name maps to this destination
                destination_region_name = original_region.name
                stage_name = None

                try:
                    for stage, region_name in self.stage_name_to_exit.items():
                        if region_name == destination_region_name:
                            stage_name = stage
                            break

                    if stage_name:
                        # Format datastorage key via standard means: "game_team_player_stagename"
                        datastorage_key = self._format_datastorage_key(team, player, stage_name)
                        self.found_entrances_datastorage_key.append(datastorage_key)
                except (KeyError, AttributeError):
                    # Skip if stage mapping fails
                    pass

                # Disconnect the entrance
                entrance.connected_region = None

                # Update the entrance name to remove the "-> Region" part so Universal Tracker
                # doesn't display the connection prematurely, keeping spoilers hidden until
                # the entrance is reconnected
                entrance.name = entrance_name_only


    def reconnect_found_entrances(self, key: str, value: Any) -> None:
        """
        Reconnect entrances when the player physically enters a stage in the game.

        This is called by UT when a datastorage key is triggered, indicating the player has visited
        a specific stage. The key format is: tww_team_player_stagename. We extract the stage name
        and reconnect all entrances that lead to that stage.

        :param key: The datastorage key (format: tww_team_player_stagename).
        :param value: The value associated with the datastorage key.
        """
        if not value:
            return

        parsed = self._parse_datastorage_key(key)
        if parsed is None:
            return

        self._reconnect_entrance_for_stage(parsed.stage_name)

    def _reconnect_entrance_for_stage(self, stage_name: str) -> int:
        """
        Reconnect all entrances leading to the given stage.

        :param stage_name: The stage name from the datastorage key.
        :return: The number of entrances reconnected.
        """
        exit_region_name = self.stage_name_to_exit.get(stage_name)
        if exit_region_name is None:
            return 0

        exit_region = self.get_region(exit_region_name)
        if exit_region is None:
            return 0

        return self._reconnect_matching_entrances(exit_region, exit_region_name)

    def _reconnect_matching_entrances(self, target_region: Region, region_name: str) -> int:
        """
        Reconnect all entrances that lead to the target region.

        :param target_region: The region to reconnect entrances to.
        :param region_name: The display name of the region.
        :return: The number of entrances reconnected.
        """
        if not hasattr(self, 'disconnected_entrances'):
            return 0

        count = 0
        for entrance, original_region in self.disconnected_entrances.items():
            if original_region == target_region:
                self._reconnect_entrance(entrance, region_name)
                count += 1
        return count

    def _reconnect_entrance(self, entrance: Any, region_name: str) -> None:
        """
        Reconnect a single entrance to its region, restoring the connection display.

        :param entrance: The entrance object to reconnect.
        :param region_name: The name of the region being reconnected to.
        """
        entrance.connected_region = self.get_region(region_name)
        entrance_name = self._extract_entrance_name(entrance.name)
        entrance.name = f"{entrance_name} -> {region_name}"
