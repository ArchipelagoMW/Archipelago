import logging
import os
from threading import Event
from typing import List, Union, ClassVar, Any, Optional, Tuple, Type

import settings
from BaseClasses import Tutorial, Region, Location, LocationProgressType, Item, ItemClassification, MultiWorld, CollectionState
from Fill import fill_restrictive
from Options import Accessibility, OptionError, Option
from worlds.AutoWorld import WebWorld, World
from .Client import OracleOfSeasonsClient  # Unused, but required to register with BizHawkClient
from .Hints import create_region_hints, create_item_hints
from .Logic import create_connections, apply_self_locking_rules
from .Options import *
from .PatchWriter import oos_create_ap_procedure_patch
from .Util import *
from .data import LOCATIONS_DATA
from .data.Constants import *
from .data.Items import ITEMS_DATA
from .data.Regions import REGIONS, NATZU_REGIONS, GASHA_REGIONS


class OracleOfSeasonsSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Oracle of Seasons US ROM"""
        copy_to = "Legend of Zelda, The - Oracle of Seasons (USA).gbc"
        description = "OoS ROM File"
        md5s = [ROM_HASH]

    class AgesRomFile(settings.UserFilePath):
        """File name of the Oracle of Ages US ROM (only needed for cross items)"""
        copy_to = "Legend of Zelda, The - Oracle of Ages (USA).gbc"
        description = "OoA ROM File"
        md5s = [AGES_ROM_HASH]

    class OoSCharacterSprite(str):
        """
        The name of the sprite file to use (from "data/sprites/oos_ooa/").
        Putting "link" as a value uses the default game sprite.
        Putting "random" as a value randomly picks a sprite from your sprites directory for each generated ROM.
        If you want some weighted result, you can arrange the options like in your option yaml.
        """

    class OoSCharacterPalette(str):
        """
        The color palette used for character sprite throughout the game.
        Valid values are: "green", "red", "blue", "orange", and "random"
        If you want some weighted result, you can arrange the options like in your option yaml.
        If you want a color weight to only apply to a specific sprite, you can write color|sprite: weight.
        For example, red|link: 1 would add red in the possible palettes with a weight of 1 only if link is the selected sprite
        """

    class OoSRevealDiggingSpots(str):
        """
        If enabled, hidden digging spots in Subrosia are revealed as diggable tiles.
        """

    class OoSHeartBeepInterval(str):
        """
        A factor applied to the infamous heart beep sound interval.
        Valid values are: "vanilla", "half", "quarter", "disabled"
        """

    class OoSRemoveMusic(str):
        """
        If true, no music will be played in the game while sound effects remain untouched
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    ages_rom_file: AgesRomFile = AgesRomFile(AgesRomFile.copy_to)
    rom_start: bool = True
    character_sprite: Union[OoSCharacterSprite, str] = "link"
    character_palette: Union[OoSCharacterPalette, str] = "green"
    reveal_hidden_subrosia_digging_spots: Union[OoSRevealDiggingSpots, bool] = True
    heart_beep_interval: Union[OoSHeartBeepInterval, str] = "vanilla"
    remove_music: Union[OoSRemoveMusic, bool] = False


class OracleOfSeasonsWeb(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Oracle of Seasons for Archipelago on your computer.",
        "English",
        "oos_setup_en.md",
        "oos_setup/en",
        ["Dinopony"]
    )

    setup_fr = Tutorial(
        "Guide de configuration MultiWorld",
        "Un guide pour configurer Oracle of Seasons d'Archipelago sur votre PC.",
        "Français",
        "oos_setup_fr.md",
        "oos_setup/fr",
        ["Deoxis"]
    )
    tutorials = [setup_en, setup_fr]
    option_groups = option_groups


class OracleOfSeasonsWorld(World):
    """
    The Legend of Zelda: Oracles of Seasons is one of the rare Capcom entries to the series.
    The seasons in the world of Holodrum have been a mess since Onox captured Din, the Oracle of Seasons.
    Gather the Essences of Nature, confront Onox and rescue Din to give nature some rest in Holodrum.
    """
    game = "The Legend of Zelda - Oracle of Seasons"
    options_dataclass = OracleOfSeasonsOptions
    options: OracleOfSeasonsOptions
    # required_client_version = (0, 5, 1)
    web = OracleOfSeasonsWeb()
    topology_present = True

    settings: ClassVar[OracleOfSeasonsSettings]
    settings_key = "tloz_oos_options"

    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS
    origin_region_name = "impa's house"

    @classmethod
    def version(cls) -> str:
        return f"{cls.world_version.major}.{cls.world_version.minor}"

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

        self.pre_fill_items: List[Item] = []
        self.default_seasons: Dict[str, str] = DEFAULT_SEASONS.copy()
        self.dungeon_entrances: Dict[str, str] = DUNGEON_CONNECTIONS.copy()
        self.portal_connections: Dict[str, str] = PORTAL_CONNECTIONS.copy()
        self.lost_woods_item_sequence: List[List] = LOST_WOODS_ITEM_SEQUENCE.copy()
        self.lost_woods_main_sequence: List[List] = LOST_WOODS_MAIN_SEQUENCE.copy()
        self.old_man_rupee_values: Dict[str, int] = OLD_MAN_RUPEE_VALUES.copy()
        self.samasa_gate_code: List[int] = SAMASA_GATE_CODE.copy()
        self.shop_prices: Dict[str, int] = VANILLA_SHOP_PRICES.copy()
        self.shop_order: List[List[str]] = []
        self.shop_rupee_requirements: Dict[str, int] = {}
        self.essences_in_game: List[str] = ITEM_GROUPS["Essences"].copy()
        self.random_rings_pool: List[str] = []
        self.remaining_progressive_gasha_seeds = 0

        self.made_hints = Event()
        self.region_hints: list[tuple[str, str | int]] = []
        self.item_hints: list[Item | None] = []

    def generate_early(self):
        if self.interpret_slot_data(None):
            return

        if self.options.randomize_ai:
            self.options.golden_beasts_requirement.value = 0

        conflicting_rings = self.options.required_rings.value & self.options.excluded_rings.value
        if len(conflicting_rings) > 0:
            raise OptionError("Required Rings and Excluded Rings contain the same element(s)", conflicting_rings)

        self.remaining_progressive_gasha_seeds = self.options.deterministic_gasha_locations.value

        self.pick_essences_in_game()
        if len(self.essences_in_game) < self.options.treehouse_old_man_requirement:
            self.options.treehouse_old_man_requirement.value = len(self.essences_in_game)

        self.restrict_non_local_items()
        self.randomize_default_seasons()
        self.randomize_old_men()

        if self.options.shuffle_dungeons:
            self.shuffle_dungeons()
        if self.options.shuffle_portals != "vanilla":
            self.shuffle_portals()

        if self.options.randomize_lost_woods_item_sequence:
            # Pick 4 random seasons & directions (last one has to be "left")
            self.lost_woods_item_sequence = []
            for i in range(4):
                self.lost_woods_item_sequence.append([
                    self.random.choice(DIRECTIONS) if i < 3 else DIRECTION_LEFT,
                    self.random.choice(SEASONS)
                ])

        if self.options.randomize_lost_woods_main_sequence:
            # Pick 4 random seasons & directions (last one has to be "up")
            self.lost_woods_main_sequence = []
            for i in range(4):
                self.lost_woods_main_sequence.append([
                    self.random.choice(DIRECTIONS) if i < 3 else DIRECTION_UP,
                    self.random.choice(SEASONS)
                ])

        if self.options.randomize_samasa_gate_code:
            self.samasa_gate_code = []
            for i in range(self.options.samasa_gate_code_length.value):
                self.samasa_gate_code.append(self.random.randint(0, 3))

        self.randomize_shop_order()
        self.randomize_shop_prices()
        self.compute_rupee_requirements()

        self.create_random_rings_pool()

    def pick_essences_in_game(self):
        # If the value for "Placed Essences" is lower than "Required Essences" (which can happen when using random
        # values for both), a new random value is automatically picked in the valid range.
        if self.options.required_essences > self.options.placed_essences:
            self.options.placed_essences.value = self.random.randint(self.options.required_essences.value, 8)

        # If some essence pedestal locations were excluded and essences are not shuffled,
        # remove those essences in priority
        if not self.options.shuffle_essences:
            excluded_locations_data = {name: data for name, data in LOCATIONS_DATA.items() if name in self.options.exclude_locations.value}
            for loc_name, loc_data in excluded_locations_data.items():
                if "essence" in loc_data and loc_data["essence"] is True:
                    self.essences_in_game.remove(loc_data["vanilla_item"])
            if len(self.essences_in_game) < self.options.required_essences:
                raise ValueError("Too many essence pedestal locations were excluded, seed will be unbeatable")

        # If we need to remove more essences, pick them randomly
        self.random.shuffle(self.essences_in_game)
        self.essences_in_game = self.essences_in_game[0:self.options.placed_essences]

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        if not self.options.keysanity_small_keys:
            self.options.non_local_items.value -= self.item_name_groups["Small Keys"]
            self.options.non_local_items.value -= self.item_name_groups["Master Keys"]
        if not self.options.keysanity_boss_keys:
            self.options.non_local_items.value -= self.item_name_groups["Boss Keys"]
        if not self.options.keysanity_maps_compasses:
            self.options.non_local_items.value -= self.item_name_groups["Dungeon Maps"]
            self.options.non_local_items.value -= self.item_name_groups["Compasses"]

    def randomize_default_seasons(self):
        if self.options.default_seasons == "randomized":
            seasons_pool = SEASONS
        elif self.options.default_seasons.current_key.endswith("singularity"):
            single_season = self.options.default_seasons.current_key.replace("_singularity", "")
            if single_season == "random":
                single_season = self.random.choice(SEASONS)
            else:
                single_season = next(byte for byte, name in SEASON_NAMES.items() if name == single_season)
            seasons_pool = [single_season]
        else:
            return

        for region in self.default_seasons:
            if region == "HORON_VILLAGE" and not self.options.normalize_horon_village_season:
                continue
            self.default_seasons[region] = self.random.choice(seasons_pool)

    def shuffle_dungeons(self):
        shuffled_dungeons = list(self.dungeon_entrances.values())
        self.random.shuffle(shuffled_dungeons)
        self.dungeon_entrances = dict(zip(self.dungeon_entrances, shuffled_dungeons))

        # If alt entrances are left as-is, we need to ensure D3 entrance doesn't lead to a dungeon with an alternate
        # entrance (D0 or D2) because people might leave by the front door and get caught in a drowning loop of doom
        forbidden_d3_dungeons = []
        if not self.options.remove_d0_alt_entrance:
            forbidden_d3_dungeons.append("enter d0")
        if not self.options.remove_d2_alt_entrance:
            forbidden_d3_dungeons.append("enter d2")

        d3_dungeon = self.dungeon_entrances["d3 entrance"]
        if d3_dungeon in forbidden_d3_dungeons:
            # Randomly pick a valid dungeon for D3 entrance, and make the entrance that was going to that dungeon
            # lead to the problematic dungeon instead
            allowed_dungeons = [d for d in DUNGEON_CONNECTIONS.values() if d not in forbidden_d3_dungeons]
            dungeon_to_swap = self.random.choice(allowed_dungeons)
            for k in self.dungeon_entrances.keys():
                if self.dungeon_entrances[k] == dungeon_to_swap:
                    self.dungeon_entrances[k] = d3_dungeon
                    break
            self.dungeon_entrances["d3 entrance"] = dungeon_to_swap

    def shuffle_portals(self):
        holodrum_portals = list(PORTAL_CONNECTIONS.keys())
        subrosian_portals = list(PORTAL_CONNECTIONS.values())
        if self.options.shuffle_portals == "shuffle_outwards":
            # Shuffle Outwards: connect Holodrum portals with random Subrosian portals
            self.random.shuffle(subrosian_portals)
            self.portal_connections = dict(zip(holodrum_portals, subrosian_portals))
        else:
            # Shuffle: connect any portal with any other portal. To keep both dimensions available, we need to ensure
            # that at least one Subrosian portal that is not D8 portal is connected to Holodrum that isn't the
            # temple remains upper portal (since that portal is only available with a subrosia access)
            self.random.shuffle(holodrum_portals)
            if holodrum_portals[0] == "temple remains upper portal":
                holodrum_portals[0], holodrum_portals[1] = holodrum_portals[1], holodrum_portals[0]
            guaranteed_portal_holodrum = holodrum_portals.pop(0)

            self.random.shuffle(subrosian_portals)
            if subrosian_portals[0] == "d8 entrance portal":
                subrosian_portals[0], subrosian_portals[1] = subrosian_portals[1], subrosian_portals[0]
            guaranteed_portal_subrosia = subrosian_portals.pop(0)

            shuffled_portals = holodrum_portals + subrosian_portals
            self.random.shuffle(shuffled_portals)
            it = iter(shuffled_portals)
            self.portal_connections = dict(zip(it, it))
            self.portal_connections[guaranteed_portal_holodrum] = guaranteed_portal_subrosia

        # If accessibility option expects all locations or all progression items to be reachable, portals need to be
        # set in a way that is valid regarding this condition. If that is not the case, re-shuffle portals recursively
        # until we end up with a satisfying shuffle.
        if self.options.accessibility != Accessibility.option_minimal and not self.is_volcanoes_west_portal_reachable():
            return self.shuffle_portals()

        # If essences are placed in dungeons and D8 dungeon portal is unreachable, this makes the seed unbeatable.
        # To avoid this, we re-shuffle portals recursively until we end up with a satisfying shuffle.
        # We only need to check that if accessibility is minimal since the above check should cover the blocked D8 already otherwise
        if (self.options.accessibility == Accessibility.option_minimal
                and self.options.required_essences == self.options.placed_essences
                and not self.options.shuffle_essences and not self.is_d8_portal_reachable()):
            return self.shuffle_portals()

    def are_portals_connected(self, portal_1, portal_2):
        if portal_1 in self.portal_connections:
            if self.portal_connections[portal_1] == portal_2:
                return True
        if portal_2 in self.portal_connections:
            if self.portal_connections[portal_2] == portal_1:
                return True
        return False

    def is_volcanoes_west_portal_reachable(self):
        if self.are_portals_connected("temple remains upper portal", "volcanoes west portal"):
            return False
        if self.are_portals_connected("d8 entrance portal", "volcanoes west portal"):
            return False
        return True

    def is_d8_portal_reachable(self):
        return not self.are_portals_connected("d8 entrance portal", "volcanoes west portal")

    def randomize_old_men(self):
        if self.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_shuffled_values:
            shuffled_rupees = list(self.old_man_rupee_values.values())
            self.random.shuffle(shuffled_rupees)
            self.old_man_rupee_values = dict(zip(self.old_man_rupee_values, shuffled_rupees))
        elif self.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_random_values:
            for key in self.old_man_rupee_values.keys():
                sign = self.random.choice([-1, 1])
                self.old_man_rupee_values[key] = self.random.choice(get_old_man_values_pool()) * sign
        elif self.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_random_positive_values:
            for key in self.old_man_rupee_values.keys():
                self.old_man_rupee_values[key] = self.random.choice(get_old_man_values_pool())
        else:
            # Remove the old man values from the pool so that they don't count negative when they are shuffled as items
            self.old_man_rupee_values = {}

    def randomize_shop_order(self):
        self.shop_order = [
            ["horonShop1", "horonShop2", "horonShop3"],
            ["memberShop1", "memberShop2", "memberShop3"],
            ["syrupShop1", "syrupShop2", "syrupShop3"]
        ]
        if self.options.advance_shop:
            self.shop_order.append(["advanceShop1", "advanceShop2", "advanceShop3"])
        if self.options.shuffle_business_scrubs:
            self.shop_order.extend([["spoolSwampScrub"], ["samasaCaveScrub"], ["d2Scrub"], ["d4Scrub"]])
        self.random.shuffle(self.shop_order)

    def randomize_shop_prices(self):
        if self.options.shop_prices == "vanilla":
            if self.options.enforce_potion_in_shop:
                self.shop_prices["horonShop3"] = 300
            return
        if self.options.shop_prices == "free":
            self.shop_prices = {k: 0 for k in self.shop_prices}
            return

        # Prices are randomized, get a random price that follow set options for each shop location.
        # Values must be rounded to nearest valid rupee amount.
        average = AVERAGE_PRICE_PER_LOCATION[self.options.shop_prices.current_key]
        deviation = min(19 * (average / 50), 100)
        for i, shop in enumerate(self.shop_order):
            shop_price_factor = (i / len(self.shop_order)) + 0.5
            for location_code in shop:
                value = self.random.gauss(average, deviation) * shop_price_factor
                self.shop_prices[location_code] = min(VALID_RUPEE_PRICE_VALUES, key=lambda x: abs(x - value))
        # Subrosia market special cases
        for i in range(2, 6):
            value = self.random.gauss(average, deviation) * 0.5
            self.shop_prices[f"subrosianMarket{i}"] = min(VALID_RUPEE_PRICE_VALUES, key=lambda x: abs(x - value))

    def compute_rupee_requirements(self):
        # Compute global rupee requirements for each shop, based on shop order and item prices
        cumulated_requirement = 0
        for shop in self.shop_order:
            if shop[0].startswith("advance") and not self.options.advance_shop:
                continue
            if shop[0].endswith("Scrub") and not self.options.shuffle_business_scrubs:
                continue
            # Add the price of each shop location in there to the requirement
            for shop_location in shop:
                cumulated_requirement += self.shop_prices[shop_location]
            # Deduce the shop name from the code of the first location
            shop_name = shop[0]
            if not shop_name.endswith("Scrub"):
                shop_name = shop_name[:-1]
            self.shop_rupee_requirements[shop_name] = cumulated_requirement

    def create_random_rings_pool(self):
        # Get a subset of as many rings as needed, with a potential filter depending on chosen options
        ring_names = [name for name, idata in ITEMS_DATA.items() if "ring" in idata]

        # Remove required rings because they'll be added later anyway
        ring_names = [name for name in ring_names if name not in self.options.required_rings.value and name not in self.options.excluded_rings.value]

        self.random.shuffle(ring_names)
        self.random_rings_pool = ring_names

    def location_is_active(self, location_name, location_data):
        if not location_data.get("conditional", False):
            return True

        region_id = location_data["region_id"]
        if region_id == "advance shop":
            return self.options.advance_shop.value
        if location_name in SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS:
            return self.options.shuffle_golden_ore_spots
        if location_name in RUPEE_OLD_MAN_LOCATIONS:
            return self.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_turn_into_locations
        if location_name in SCRUB_LOCATIONS:
            return self.options.shuffle_business_scrubs
        if location_name == "Horon Village: Shop #3":
            return not self.options.enforce_potion_in_shop
        if location_name.startswith("Gasha Nut #"):
            return int(location_name[11:]) <= self.options.deterministic_gasha_locations
        if location_name == "Horon Village: Item Inside Maku Tree (3+ Essences)":
            return len(self.essences_in_game) >= 3
        if location_name == "Horon Village: Item Inside Maku Tree (5+ Essences)":
            return len(self.essences_in_game) >= 5
        if location_name == "Horon Village: Item Inside Maku Tree (7+ Essences)":
            return len(self.essences_in_game) >= 7
        if location_name in SECRETS:
            return self.options.secret_locations
        return False

    def create_location(self, region_name: str, location_name: str, local: bool):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
        region.locations.append(location)
        if local:
            location.item_rule = lambda item: item.player == self.player

    def create_regions(self):
        # Create regions
        for region_name in REGIONS:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name in NATZU_REGIONS[self.options.animal_companion.current_key]:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        if self.options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell:
            region = Region("rooster adventure", self.player, self.multiworld)
            self.multiworld.regions.append(region)

        if self.options.deterministic_gasha_locations > 0:
            for i in range(self.options.deterministic_gasha_locations):
                region = Region(GASHA_REGIONS[i], self.player, self.multiworld)
                self.multiworld.regions.append(region)

        # Create locations
        for location_name, location_data in LOCATIONS_DATA.items():
            if not self.location_is_active(location_name, location_data):
                continue

            is_local = "local" in location_data and location_data["local"] is True
            self.create_location(location_data["region_id"], location_name, is_local)

        self.create_events()
        self.exclude_locations_automatically()

    def create_event(self, region_name, event_item_name):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, region_name + ".event", None, region)
        region.locations.append(location)
        location.place_locked_item(Item(event_item_name, ItemClassification.progression, None, self.player))

    def create_events(self):
        # Events to indicate a given tree stump is reachable
        self.create_event("spool stump", "_reached_spool_stump")
        self.create_event("temple remains lower stump", "_reached_remains_stump")
        self.create_event("temple remains upper stump", "_reached_remains_stump")
        self.create_event("d1 stump", "_reached_eyeglass_stump")
        self.create_event("d2 stump", "_reached_d2_stump")
        self.create_event("d5 stump", "_reached_eyeglass_stump")
        self.create_event("sunken city dimitri", "_saved_dimitri_in_sunken_city")
        self.create_event("ghastly stump", "_reached_ghastly_stump")
        self.create_event("coast stump", "_reached_coast_stump")
        # Events for beating golden beasts
        self.create_event("golden darknut", "_beat_golden_darknut")
        self.create_event("golden lynel", "_beat_golden_lynel")
        self.create_event("golden octorok", "_beat_golden_octorok")
        self.create_event("golden moblin", "_beat_golden_moblin")
        # Events for "wild" seeds that can be found inside respawnable bushes in dungeons
        self.create_event("d4 miniboss room wild embers", "_wild_ember_seeds")
        self.create_event("d5 armos chest", "_wild_ember_seeds")
        self.create_event("d7 entrance wild embers", "_wild_ember_seeds")
        self.create_event("frypolar room wild mystery", "_wild_mystery_seeds")
        # Various events to help with logic
        self.create_event("bomb temple remains", "_triggered_volcano")
        self.create_event("subrosia market sector", "_reached_rosa")
        self.create_event("subrosian dance hall", "_reached_subrosian_dance_hall")
        self.create_event("subrosia pirates sector", "_met_pirates")
        self.create_event("tower of autumn", "_opened_tower_of_autumn")
        self.create_event("d2 moblin chest", "_reached_d2_bracelet_room")
        self.create_event("d5 drop ball", "_dropped_d5_magnet_ball")
        self.create_event("d2 rupee room", "_reached_d2_rupee_room")
        self.create_event("d6 rupee room", "_reached_d6_rupee_room")
        self.create_event("maku seed", "Maku Seed")

        if self.options.goal == OracleOfSeasonsGoal.option_beat_onox:
            self.create_event("onox beaten", "_beaten_game")
        elif self.options.goal == OracleOfSeasonsGoal.option_beat_ganon:
            self.create_event("ganon beaten", "_beaten_game")

        # Create events for reaching Gasha spots, used when Gasha-sanity is on
        for region_name in GASHA_SPOT_REGIONS:
            self.create_event(region_name, f"_reached_{region_name}")

        # Create event items to represent rupees obtained from Old Men, unless they are turned into locations
        if self.options.shuffle_old_men != OracleOfSeasonsOldMenShuffle.option_turn_into_locations:
            for region_name in self.old_man_rupee_values:
                self.create_event(region_name, "rupees from " + region_name)

    def exclude_locations_automatically(self):
        locations_to_exclude = set()
        # If goal essence requirement is set to a specific value, prevent essence-bound checks which require more
        # essences than this goal to hold anything of value
        if self.options.required_essences < 7 <= len(self.essences_in_game):
            locations_to_exclude.add("Horon Village: Item Inside Maku Tree (7+ Essences)")
            if self.options.required_essences < 5 <= len(self.essences_in_game):
                locations_to_exclude.add("Horon Village: Item Inside Maku Tree (5+ Essences)")
                if self.options.required_essences < 3 <= len(self.essences_in_game):
                    locations_to_exclude.add("Horon Village: Item Inside Maku Tree (3+ Essences)")
        if self.options.required_essences < self.options.treehouse_old_man_requirement:
            locations_to_exclude.add("Holodrum Plain: Old Man in Treehouse")

        # If dungeons without essence need to be excluded, do it if conditions are met
        if self.options.exclude_dungeons_without_essence and not self.options.shuffle_essences:
            for i, essence_name in enumerate(ITEM_GROUPS["Essences"]):
                if essence_name not in self.essences_in_game:
                    locations_to_exclude.update(self.location_name_groups[f"D{i + 1}"])

        if not self.options.shuffle_business_scrubs:
            locations_to_exclude.difference_update(SCRUB_LOCATIONS)

        if self.options.randomize_ai:
            locations_to_exclude.add("Western Coast: Black Beast's Chest")

        for name in locations_to_exclude:
            self.multiworld.get_location(name, self.player).progress_type = LocationProgressType.EXCLUDED

    def set_rules(self):
        create_connections(self.multiworld, self.player, self.origin_region_name, self.options)
        apply_self_locking_rules(self.multiworld, self.player)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("_beaten_game", self.player)

        self.multiworld.register_indirect_condition(self.get_region("lost woods top statue"), self.get_entrance("lost woods -> lost woods deku"))
        self.multiworld.register_indirect_condition(self.get_region("lost woods phonograph"), self.get_entrance("lost woods stump -> lost woods"))
        self.multiworld.register_indirect_condition(self.get_region("lost woods phonograph"), self.get_entrance("d6 sector -> lost woods"))
        self.multiworld.register_indirect_condition(self.get_region("lost woods deku"), self.get_entrance("lost woods -> d6 sector"))
        self.multiworld.register_indirect_condition(self.get_region("lost woods deku"), self.get_entrance("lost woods stump -> d6 sector"))

        if self.options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell:
            cucco_region = self.get_region("rooster adventure")
            # This saves using an event which is slightly more efficient
            self.multiworld.register_indirect_condition(cucco_region, self.get_entrance("d6 sector -> old man near d6"))
            self.multiworld.register_indirect_condition(cucco_region, self.get_entrance("d6 sector -> d6 entrance"))
            self.multiworld.register_indirect_condition(self.get_region("lost woods top statue"), self.get_entrance("rooster adventure -> lost woods deku"))

    def create_item(self, name: str) -> Item:
        # If item name has a "!PROG" suffix, force it to be progression. This is typically used to create the right
        # amount of progression rupees while keeping them a filler item as default
        if name.endswith("!PROG"):
            name = name.removesuffix("!PROG")
            classification = ItemClassification.progression_deprioritized_skip_balancing
        elif name.endswith("!USEFUL"):
            # Same for above but with useful. This is typically used for Required Rings,
            # as we don't want those locked in a barren dungeon
            name = name.removesuffix("!USEFUL")
            classification = ITEMS_DATA[name]["classification"]
            if classification == ItemClassification.filler:
                classification = ItemClassification.useful
        elif name.endswith("!FILLER"):
            name = name.removesuffix("!FILLER")
            classification = ItemClassification.filler
        else:
            classification = ITEMS_DATA[name]["classification"]
        ap_code = self.item_name_to_id[name]

        # A few items become progression only in hard logic
        progression_items_in_medium_logic = ["Expert's Ring", "Fist Ring", "Swimmer's Ring", "Energy Ring", "Heart Ring L-2"]
        if self.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium and name in progression_items_in_medium_logic:
            classification = ItemClassification.progression
        if self.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_hard and name == "Heart Ring L-1":
            classification = ItemClassification.progression
        # As many Gasha Seeds become progression as the number of deterministic Gasha Nuts
        if self.remaining_progressive_gasha_seeds > 0 and name == "Gasha Seed":
            self.remaining_progressive_gasha_seeds -= 1
            classification = ItemClassification.progression_deprioritized

        # Players in Medium+ are expected to know the default paths through Lost Woods, Phonograph becomes filler
        if self.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium and not self.options.randomize_lost_woods_item_sequence and name == "Phonograph":
            classification = ItemClassification.filler

        # UT doesn't let us know if the item is progression or not, so it is always progression
        if hasattr(self.multiworld, "generation_is_fake"):
            classification = ItemClassification.progression

        return Item(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        excluded_mapass = set()
        if self.options.exclude_dungeons_without_essence and not self.options.shuffle_essences:
            for i, essence_name in enumerate(ITEM_GROUPS["Essences"]):
                if essence_name not in self.essences_in_game:
                    excluded_mapass.add(f"Dungeon Map ({DUNGEON_NAMES[i]})")
                    excluded_mapass.add(f"Compass ({DUNGEON_NAMES[i]})")

        item_pool_dict = {}
        filler_item_count = 0
        rupee_item_count = 0
        ore_item_count = 0
        for loc_name, loc_data in LOCATIONS_DATA.items():
            if not self.location_is_active(loc_name, loc_data):
                continue
            if "vanilla_item" not in loc_data:
                continue

            item_name = loc_data["vanilla_item"]
            if "Ring" in item_name:
                item_name = "Random Ring"
            if item_name == "Filler Item":
                filler_item_count += 1
                continue
            if item_name.startswith("Rupees ("):
                if self.options.shop_prices == OracleOfSeasonsShopPrices.option_free:
                    filler_item_count += 1
                else:
                    rupee_item_count += 1
                continue
            if item_name.startswith("Ore Chunks ("):
                if self.options.shop_prices == OracleOfSeasonsShopPrices.option_free or not self.options.shuffle_golden_ore_spots:
                    filler_item_count += 1
                else:
                    ore_item_count += 1
                continue
            if self.options.master_keys != OracleOfSeasonsMasterKeys.option_disabled and "Small Key" in item_name:
                # Small Keys don't exist if Master Keys are set to replace them
                filler_item_count += 1
                continue
            if self.options.master_keys == OracleOfSeasonsMasterKeys.option_all_dungeon_keys and "Boss Key" in item_name:
                # Boss keys don't exist if Master Keys are set to replace them
                filler_item_count += 1
                continue
            if self.options.starting_maps_compasses and ("Compass" in item_name or "Dungeon Map" in item_name):
                # Compasses and Dungeon Maps don't exist if player starts with them
                filler_item_count += 1
                continue
            if "essence" in loc_data and loc_data["essence"] is True:
                # If essence was decided not to be placed because of "Placed Essences" option or
                # because of pedestal being an excluded location, replace it with a filler item
                if item_name not in self.essences_in_game:
                    filler_item_count += 1
                    continue
                # If essences are not shuffled, place and lock this item directly on the pedestal.
                # Otherwise, the fill algorithm will take care of placing them anywhere in the multiworld.
                if not self.options.shuffle_essences:
                    essence_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(essence_item)
                    continue

            if item_name == "Gasha Seed":
                # Remove all gasha seeds from the pool to read as many as needed a later while limiting their impact on the item pool
                filler_item_count += 1
                continue

            if item_name == "Fool's Ore" and self.options.fools_ore == OracleOfSeasonsFoolsOre.option_excluded:
                filler_item_count += 1
                continue

            if item_name.startswith("Bombs (") or item_name.startswith("Bombchus ("):
                # Not enough bombs in the pool, erase everything to redistribute them
                filler_item_count += 1
                continue

            if item_name == "Flute":
                item_name = self.options.animal_companion.current_key.title() + "'s Flute"
            elif item_name in excluded_mapass:
                item_name += "!FILLER"

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        if self.options.exclude_dungeons_without_essence and len(self.essences_in_game) < 4:
            # Compact the bomb items for smaller seeds to not clog the pool
            item_pool_dict["Bombchus (20)"] = 5
            item_pool_dict["Bombs (20)"] = 5
            extra_items = 10
        else:
            item_pool_dict["Bombchus (10)"] = 10
            item_pool_dict["Bombs (10)"] = 10
            extra_items = 20
        if self.options.cross_items:
            item_pool_dict["Cane of Somaria"] = 1
            item_pool_dict["Switch Hook"] = 2
            item_pool_dict["Seed Shooter"] = 1
            extra_items += 4

        # If Master Keys are enabled, put one for every dungeon
        if self.options.master_keys != OracleOfSeasonsMasterKeys.option_disabled:
            for small_key_name in ITEM_GROUPS["Master Keys"]:
                item_pool_dict[small_key_name] = 1
                extra_items += 1

        # Add the required gasha seeds to the pool
        required_gasha_seeds = self.options.deterministic_gasha_locations.value
        item_pool_dict["Gasha Seed"] = required_gasha_seeds
        extra_items += required_gasha_seeds

        if rupee_item_count > 0:
            rupee_item_pool, filler_item_count = self.build_rupee_item_dict(rupee_item_count, filler_item_count)
            item_pool_dict.update(rupee_item_pool)

        if ore_item_count > 0:
            ore_item_pool, filler_item_count = self.build_ore_item_dict(ore_item_count, filler_item_count)
            item_pool_dict.update(ore_item_pool)

        # Remove items from pool
        for item, removed_amount in self.options.remove_items_from_pool.items():
            if item in item_pool_dict:
                current_amount = item_pool_dict[item]
            else:
                current_amount = 0
            new_amount = current_amount - removed_amount
            if new_amount < 0:
                logging.warning(f"Not enough {item} to satisfy {self.player_name}'s remove_items_from_pool: "
                                f"{-new_amount} missing")
                new_amount = 0
            item_pool_dict[item] = new_amount
            filler_item_count += current_amount - new_amount

        # Add the required rings
        ring_copy = sorted(self.options.required_rings.value.copy())
        for _ in range(len(ring_copy)):
            ring_name = f"{ring_copy.pop()}!USEFUL"
            item_pool_dict[ring_name] = item_pool_dict.get(ring_name, 0) + 1

            if item_pool_dict["Random Ring"] > 0:
                # Take from set ring pool first
                item_pool_dict["Random Ring"] -= 1
            else:
                # Take from filler after
                filler_item_count -= 1

        assert filler_item_count >= extra_items
        filler_item_count -= extra_items

        # Add as many filler items as required
        for _ in range(filler_item_count):
            random_filler_item = self.get_filler_item_name()
            item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1

        if "Random Ring" in item_pool_dict:
            quantity = item_pool_dict["Random Ring"]
            for _ in range(quantity):
                ring_name = self.get_random_ring_name()
                item_pool_dict[ring_name] = item_pool_dict.get(ring_name, 0) + 1
            del item_pool_dict["Random Ring"]

        return item_pool_dict

    def build_rupee_item_dict(self, rupee_item_count: int, filler_item_count: int) -> Tuple[int, int]:
        sorted_shop_values = sorted(self.shop_rupee_requirements.values())
        total_cost = sorted_shop_values[-1]

        # Count the old man's contribution, it's especially important as it may be negative
        # (We ignore dungeons here because we don't want to worry about whether they'll be available)
        # TODO : With GER that note will be obsolete
        old_man_rupee = 0
        for name in self.old_man_rupee_values:
            old_man_rupee += self.old_man_rupee_values[name]

        target = total_cost / 2 - old_man_rupee
        total_cost = max(total_cost - old_man_rupee, sorted_shop_values[-3])  # Ensure it doesn't drop too low due to the old men
        return self.build_currency_item_dict(rupee_item_count, filler_item_count, target, total_cost, "Rupees", VALID_RUPEE_ITEM_VALUES)

    def build_ore_item_dict(self, ore_item_count: int, filler_item_count: int) -> Tuple[int, int]:
        total_cost = sum([self.shop_prices[loc] for loc in MARKET_LOCATIONS])
        target = total_cost / 2

        return self.build_currency_item_dict(ore_item_count, filler_item_count, target, total_cost, "Ore Chunks", VALID_ORE_ITEM_VALUES)

    def build_currency_item_dict(self, currency_item_count: int, filler_item_count: int, initial_target: int,
                                 total_cost: int, currency_name: str, valid_currency_item_values: list[int]):
        average_value = total_cost / currency_item_count
        deviation = average_value / 2.5
        currency_item_dict = {}
        target = initial_target
        for i in range(0, currency_item_count):
            value = self.random.gauss(average_value, deviation)
            value = min(valid_currency_item_values, key=lambda x: abs(x - value))
            if value > average_value / 3:
                # Put a "!PROG" suffix to force them to be created as progression items (see `create_item`)
                item_name = f"{currency_name} ({value})!PROG"
                target -= value
            else:
                # Don't count little packs as progression since they are likely irrelevant
                item_name = f"{currency_name} ({value})"
            currency_item_dict[item_name] = currency_item_dict.get(item_name, 0) + 1
        # If the target is positive, it means there aren't enough rupees, so we'll steal a filler from the pool and reroll
        if target > 0:
            return self.build_currency_item_dict(currency_item_count + 1, filler_item_count - 1, initial_target,
                                                 total_cost, currency_name, valid_currency_item_values)
        return currency_item_dict, filler_item_count

    def create_items(self):
        item_pool_dict = self.build_item_pool_dict()
        items = []
        for item_name, quantity in item_pool_dict.items():
            for _ in range(quantity):
                items.append(self.create_item(item_name))
        self.filter_confined_dungeon_items_from_pool(items)
        self.multiworld.itempool.extend(items)
        self.pre_fill_seeds()

    def get_pre_fill_items(self):
        return self.pre_fill_items

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld):
        cls.stage_pre_fill_dungeon_items(multiworld)

    def filter_confined_dungeon_items_from_pool(self, items: List[Item]):
        confined_dungeon_items = []
        excluded_dungeons = []
        if self.options.exclude_dungeons_without_essence and not self.options.shuffle_essences:
            for i, essence_name in enumerate(ITEM_GROUPS["Essences"]):
                if essence_name not in self.essences_in_game:
                    excluded_dungeons.append(i + 1)

        # Put Small Keys / Master Keys unless keysanity is enabled for those
        if self.options.master_keys != OracleOfSeasonsMasterKeys.option_disabled:
            small_keys_name = "Master Key"
        else:
            small_keys_name = "Small Key"
        if not self.options.keysanity_small_keys:
            confined_dungeon_items.extend([item for item in items if item.name.startswith(small_keys_name)])
        else:
            for i in excluded_dungeons:
                confined_dungeon_items.extend([item for item in items if item.name == f"{small_keys_name} ({DUNGEON_NAMES[i]})"])

        # Put Boss Keys unless keysanity is enabled for those
        if not self.options.keysanity_boss_keys:
            confined_dungeon_items.extend([item for item in items if item.name.startswith("Boss Key")])
        else:
            for i in excluded_dungeons:
                confined_dungeon_items.extend([item for item in items if item.name == f"Boss Key ({DUNGEON_NAMES[i]})"])

        # Put Maps & Compasses unless keysanity is enabled for those
        if not self.options.keysanity_maps_compasses:
            confined_dungeon_items.extend([item for item in items if item.name.startswith("Dungeon Map")
                                           or item.name.startswith("Compass")])

        for item in confined_dungeon_items:
            items.remove(item)
        self.pre_fill_items.extend(confined_dungeon_items)

    @classmethod
    def stage_pre_fill_dungeon_items(cls, multiworld: MultiWorld):
        # If keysanity is off, dungeon items can only be put inside local dungeon locations, and there are not so many
        # of those which makes them pretty crowded.
        # This usually ends up with generator not having anywhere to place a few small keys, making the seed unbeatable.
        # To circumvent this, we perform a restricted pre-fills here, placing only those dungeon items
        # before anything else.
        oos_players = multiworld.get_game_players(cls.game)

        base_all_state = multiworld.get_all_state(False, collect_pre_fill_items=False, perform_sweep=False)
        # Collect all pre_fill_items except our OoS's and then sweep. This gives more accurate results in cases of item
        # plando being used to remove items from the item pool and placing them into locations locked behind pre_fill
        # items.
        for player in multiworld.player_ids:
            if player in oos_players:
                continue
            subworld = multiworld.worlds[player]
            for item in subworld.get_pre_fill_items():
                subworld.collect(base_all_state, item)
        base_all_state.sweep_for_advancements()

        for filling_player in oos_players:
            # Create a player-specific state for just the player that is filling dungeons.
            per_player_base_all_state = base_all_state.copy()
            # Collect the pre_fill_items() of all other OoS players into the state.
            for other_player in oos_players:
                if other_player == filling_player:
                    continue
                subworld = multiworld.worlds[other_player]
                for item in subworld.get_pre_fill_items():
                    subworld.collect(per_player_base_all_state, item)
            # And then sweep the state to pick up pre-placed items.
            per_player_base_all_state.sweep_for_advancements()

            # Get the world for the player that is filling.
            filling_world = multiworld.worlds[filling_player]

            # Fill each of this world's dungeons.
            for i in range(0, 9):
                # Build a list of locations in this dungeon
                dungeon_location_names = [name for name, loc in LOCATIONS_DATA.items()
                                          if "dungeon" in loc and loc["dungeon"] == i]
                dungeon_locations = [loc for loc in multiworld.get_locations(filling_player)
                                     if loc.name in dungeon_location_names and not loc.locked]

                # From the list of all dungeon items that needs to be placed restrictively, only filter the ones for the
                # dungeon we are currently processing.
                confined_dungeon_items = [item for item in filling_world.pre_fill_items
                                          if item.name.endswith(f"({DUNGEON_NAMES[i]})")]
                if len(confined_dungeon_items) == 0:
                    continue  # This list might be empty with some keysanity options

                # Remove from the pre_fill_items the items we're about to place
                for item in confined_dungeon_items:
                    filling_world.pre_fill_items.remove(item)
                collection_state = per_player_base_all_state.copy()
                # Collect the remaining pre_fill_items into the state.
                for item in filling_world.get_pre_fill_items():
                    collection_state.collect(item, True)
                # Sweep the copied state across the entire multiworld to again account for unusual item plando. It is
                # also beneficial to pass as maximal a state as possible to fill_restrictive to reduce how much sweeping
                # fill_restrictive must do.
                collection_state.sweep_for_advancements()
                # Perform a prefill to place confined items inside locations of this dungeon
                filling_world.random.shuffle(dungeon_locations)
                fill_restrictive(multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                                 single_player_placement=True, lock=True, allow_excluded=True)

    def pre_fill_seeds(self) -> None:
        # The prefill algorithm for seeds has a few constraints:
        #   - it needs to place the "default seed" into Horon Village seed tree
        #   - it needs to place a random seed on the "duplicate tree" (can be Horon's tree)
        #   - it needs to place one of each seed on the 5 remaining trees
        # This has a few implications:
        #   - if Horon is the duplicate tree, this is the simplest case: we just place a starting seed in Horon's tree
        #     and scatter the 5 seed types on the 5 other trees
        #   - if Horon is NOT the duplicate tree, we need to remove Horon's seed from the pool of 5 seeds to scatter
        #     and put a random seed inside the duplicate tree. Then, we place the 4 remaining seeds on the 4 remaining
        #     trees
        TREES_TABLE = {
            OracleOfSeasonsDuplicateSeedTree.option_horon_village: "Horon Village: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_woods_of_winter: "Woods of Winter: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_north_horon: "Holodrum Plain: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_spool_swamp: "Spool Swamp: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_sunken_city: "Sunken City: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_tarm_ruins: "Tarm Ruins: Seed Tree",
        }
        duplicate_tree_name = TREES_TABLE[self.options.duplicate_seed_tree.value]

        def place_seed(seed_name: str, location_name: str):
            seed_item = self.create_item(seed_name)
            self.multiworld.get_location(location_name, self.player).place_locked_item(seed_item)

        seeds_to_place = list(SEED_ITEMS)

        manually_placed_trees = ["Horon Village: Seed Tree", duplicate_tree_name]
        trees_to_process = [name for name in TREES_TABLE.values() if name not in manually_placed_trees]

        # Place default seed type in Horon Village tree
        place_seed(SEED_ITEMS[self.options.default_seed.value], "Horon Village: Seed Tree")

        # If duplicate tree is not Horon's, remove Horon seed from the pool of placeable seeds
        if duplicate_tree_name != "Horon Village: Seed Tree":
            del seeds_to_place[self.options.default_seed.value]
            place_seed(self.random.choice(SEED_ITEMS), duplicate_tree_name)

        # Place remaining seeds on remaining trees
        self.random.shuffle(trees_to_process)
        for seed in seeds_to_place:
            place_seed(seed, trees_to_process.pop())

    def get_filler_item_name(self) -> str:
        FILLER_ITEM_NAMES = [
            "Rupees (1)", "Rupees (5)", "Rupees (10)", "Rupees (10)",
            "Rupees (20)", "Rupees (30)",
            "Ore Chunks (10)", "Ore Chunks (10)", "Ore Chunks (25)",
            "Random Ring", "Random Ring", "Random Ring",
            "Gasha Seed", "Gasha Seed",
            "Potion"
        ]

        item_name = self.random.choice(FILLER_ITEM_NAMES)
        if item_name == "Random Ring":
            return self.get_random_ring_name()
        return item_name

    def get_random_ring_name(self):
        if len(self.random_rings_pool) > 0:
            return self.random_rings_pool.pop()
        return self.get_filler_item_name()  # It might loop but not enough to really matter

    @classmethod
    def stage_fill_hook(cls, multiworld: MultiWorld, progitempool, usefulitempool, filleritempool, fill_locations):
        players = multiworld.get_game_players(OracleOfSeasonsWorld.game)
        if not players:
            return
        weight_dict = {}
        for player in players:
            possible_items = [["Flippers", "Bush Breaker"], ["Power Bracelet"]]
            bush_breakers = [["Progressive Sword"], ["Biggoron's Sword"]]
            world: OracleOfSeasonsWorld = multiworld.worlds[player]
            portal_connections = {world.portal_connections[key]: key for key in world.portal_connections}
            portal_connections.update(world.portal_connections)

            bad_portals = {"spool swamp portal", "horon village portal", "eyeglass lake portal", "temple remains lower portal", "d8 entrance portal"}
            if portal_connections["temple remains lower portal"] in bad_portals:
                bad_portals.add("temple remains upper portal")

            if multiworld.random.random() < 0.5:
                if portal_connections["horon village portal"] not in bad_portals:
                    possible_items.append(["Progressive Boomerang", "Progressive Boomerang"])
                else:
                    bush_breakers.append(["Progressive Boomerang", "Progressive Boomerang"])

            if portal_connections["eyeglass lake portal"] not in bad_portals and world.options.default_seed == "pegasus":
                items = ["Progressive Feather", "Progressive Feather", "Seed Satchel", "Bush Breaker"]
                if world.default_seasons["EYEGLASS_LAKE"] != SEASON_WINTER:
                    items.append("Rod of Seasons (Winter)")
                possible_items.append(items)

            if world.options.default_seed == "ember":
                possible_items.append(["Seed Satchel"])
                possible_items.append(["Progressive Slingshot"])
                if world.options.cross_items:
                    possible_items.append(["Seed Shooter"])

            if world.options.animal_companion == "dimitri":
                possible_items.append(["Dimitri's Flute"])
            elif world.options.animal_companion == "ricky":
                bush_breakers.append(["Ricky's Flute"])
            else:
                bush_breakers.append(["Moosh's Flute"])

            if not world.options.remove_d0_alt_entrance:
                if world.dungeon_entrances["d2 entrance"] == "enter d0" \
                        or world.dungeon_entrances["d5 entrance"] == "enter d0" \
                        or world.dungeon_entrances["d7 entrance"] == "enter d0" \
                        or (world.dungeon_entrances["d8 entrance"] == "enter d0" and portal_connections["d8 entrance portal"] not in bad_portals):
                    possible_items.append(["Bush Breaker"])

            if world.options.logic_difficulty > 0:
                if multiworld.random.random() < 0.5:
                    bush_breakers.append(["Bombs (10)", "Bombs (10)"])
                if world.options.default_seed == "gale":
                    bush_breakers.append(["Progressive Slingshot"])
                    if world.options.cross_items:
                        bush_breakers.append(["Seed Shooter"])

            if world.options.cross_items:
                bush_breakers.append(["Switch Hook"])

            items = multiworld.random.choice(possible_items)
            if "Bush Breaker" in items:
                items.remove("Bush Breaker")
                items.extend(multiworld.random.choice(bush_breakers))
            for item in multiworld.precollected_items[player]:
                if item.name in items:
                    items.remove(item.name)
            weight_dict[player] = items

        indexes = {player: [] for player in players}
        for i in range(len(progitempool)):
            item = progitempool[i]
            player = item.player
            if player not in players:
                continue

            if len(indexes[player]) < len(weight_dict[player]):
                indexes[player].append(i)
            if item.name not in weight_dict[player]:
                continue
            other_index = indexes[player].pop()
            progitempool[i], progitempool[other_index] = progitempool[other_index], progitempool[i]
            weight_dict[player].remove(item.name)
            for player in players:
                if len(weight_dict[player]) > 0:
                    break
            else:
                break

    def generate_output(self, output_directory: str):
        if self.options.bird_hint.know_it_all():
            self.region_hints = create_region_hints(self)

        if self.options.bird_hint.owl():
            self.item_hints = create_item_hints(self)
        self.made_hints.set()
        patch = oos_create_ap_procedure_patch(self)
        rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                  f"{patch.patch_file_ending}")
        patch.write(rom_path)

    def fill_slot_data(self) -> dict:
        slot_data = {
            "version": f"{self.world_version.as_simple_string()}",
            "options": self.options.as_dict(
                *[option_name for option_name in OracleOfSeasonsOptions.type_hints
                  if hasattr(OracleOfSeasonsOptions.type_hints[option_name], "include_in_slot_data")]),
            # "samasa_gate_sequence": ' '.join([str(x) for x in self.samasa_gate_code]),
            "lost_woods_item_sequence": self.lost_woods_item_sequence,
            "lost_woods_main_sequence": self.lost_woods_main_sequence,
            "default_seasons": self.default_seasons,
            "old_man_rupee_values": self.old_man_rupee_values,
            "dungeon_entrances": {a.replace(" entrance", ""): b.replace("enter ", "")
                                  for a, b in self.dungeon_entrances.items()},
            "subrosia_portals": self.portal_connections,
            "shop_rupee_requirements": self.shop_rupee_requirements,
            "shop_costs": self.shop_prices,
        }

        self.made_hints.wait()
        # The structure is made to make it easy to call CreateHints
        slot_data_item_hints = []
        for item_hint in self.item_hints:
            if item_hint is None:
                # Joke hint
                slot_data_item_hints.append(None)
                continue
            location = item_hint.location
            slot_data_item_hints.append((location.address, location.player))
        slot_data["item_hints"] = slot_data_item_hints

        return slot_data

    def write_spoiler(self, spoiler_handle):
        spoiler_handle.write(f"\n\nDefault Seasons ({self.multiworld.player_name[self.player]}):\n")
        for region_name, season in self.default_seasons.items():
            spoiler_handle.write(f"\t- {region_name} --> {SEASON_NAMES[season]}\n")

        if self.options.shuffle_dungeons:
            spoiler_handle.write(f"\nDungeon Entrances ({self.multiworld.player_name[self.player]}):\n")
            for entrance, dungeon in self.dungeon_entrances.items():
                spoiler_handle.write(f"\t- {entrance} --> {dungeon.replace('enter ', '')}\n")

        if self.options.shuffle_portals != "vanilla":
            spoiler_handle.write(f"\nSubrosia Portals ({self.multiworld.player_name[self.player]}):\n")
            for portal_holo, portal_sub in self.portal_connections.items():
                spoiler_handle.write(f"\t- {portal_holo} --> {portal_sub}\n")

        spoiler_handle.write(f"\nShop Prices ({self.multiworld.player_name[self.player]}):\n")
        shop_codes = [code for shop in self.shop_order for code in shop]
        shop_codes.extend(MARKET_LOCATIONS)
        for shop_code in shop_codes:
            price = self.shop_prices[shop_code]
            for loc_name, loc_data in LOCATIONS_DATA.items():
                if loc_data.get("symbolic_name", None) is None or loc_data["symbolic_name"] != shop_code:
                    continue
                if self.location_is_active(loc_name, loc_data):
                    currency = "Ore Chunks" if shop_code.startswith("subrosia") else "Rupees"
                    spoiler_handle.write(f"\t- {loc_name}: {price} {currency}\n")
                break

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if not change:
            return False

        if item.name == "Bombs (10)":
            state.prog_items[self.player]["Bombs"] += 1
        elif item.name == "Bombs (20)":
            state.prog_items[self.player]["Bombs"] += 2
        elif item.name == "Bombchus (10)":
            state.prog_items[self.player]["Bombchus"] += 1
        elif item.name == "Bombchus (20)":
            state.prog_items[self.player]["Bombchus"] += 2

        if self.options.logic_difficulty < OracleOfSeasonsLogicDifficulty.option_hell:
            return True
        if item.code is None or item.code >= 0x2100 and item.code != 0x2e00:  # Not usable item nor ember nor flippers
            return True
        state.tloz_oos_available_cuccos[self.player] = None
        return True

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if not change:
            return False

        if item.name == "Bombs (10)":
            state.prog_items[self.player]["Bombs"] -= 1
        elif item.name == "Bombs (20)":
            state.prog_items[self.player]["Bombs"] -= 2
        elif item.name == "Bombchus (10)":
            state.prog_items[self.player]["Bombchus"] -= 1
        elif item.name == "Bombchus (20)":
            state.prog_items[self.player]["Bombchus"] -= 2

        if self.options.logic_difficulty < OracleOfSeasonsLogicDifficulty.option_hell:
            return True
        if item.code is None or item.code >= 0x2100 and item.code != 0x2e00:  # Not usable item nor ember nor flippers
            return True
        state.tloz_oos_available_cuccos[self.player] = None
        return True

    # UT stuff
    def interpret_slot_data(self, slot_data: Optional[dict[str, Any]]) -> Any:
        if slot_data is not None:
            return slot_data

        if not hasattr(self.multiworld, "re_gen_passthrough") or self.game not in self.multiworld.re_gen_passthrough:
            return False

        slot_data = self.multiworld.re_gen_passthrough[self.game]

        for option in [option_name for option_name in OracleOfSeasonsOptions.type_hints
                       if hasattr(OracleOfSeasonsOptions.type_hints[option_name], "include_in_slot_data")]:
            option_class: Type[Option] = OracleOfSeasonsOptions.type_hints[option]
            self.options.__setattr__(option, option_class.from_any(slot_data["options"][option]))

        self.lost_woods_item_sequence = slot_data["lost_woods_item_sequence"]
        self.lost_woods_main_sequence = slot_data["lost_woods_main_sequence"]
        self.default_seasons = slot_data["default_seasons"]
        self.old_man_rupee_values = slot_data["old_man_rupee_values"]
        self.dungeon_entrances = {f"{a} entrance": f"enter {b}"
                                  for a, b in slot_data["dungeon_entrances"].items()}
        self.portal_connections = slot_data["subrosia_portals"]
        self.shop_rupee_requirements = slot_data["shop_rupee_requirements"]
        self.shop_prices = slot_data["shop_costs"]

        return True
