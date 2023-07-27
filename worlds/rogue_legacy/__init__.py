from logging import warning
from typing import Dict, List, Union

from BaseClasses import Region, Tutorial
from Options import Option
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import allow_self_locking_items
from .Items import RLItem, filler_items, item_groups, item_table
from .Locations import location_groups, location_table
from .Options import options_table
from .Regions import region_table

# Before you use my world as a reference, just note this variable is only useful for Rogue Legacy; you don't need it. :P
WORLD_VERSION = 2


class RLWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Rogue Legacy Randomizer - Setup Guide",
        "A guide to setting up the Rogue Legacy Randomizer on your computer. This guide works for single-player and "
        "multiworld.",
        "English",
        "rogue-legacy_en.md",
        "rogue-legacy/en",
        ["Phar"]
    )]
    bug_report_page = "https://github.com/ThePhar/RogueLegacyRandomizer/issues/new?assignees=&labels=bug&template=" \
                      "report-an-issue---.md&title=%5BIssue%5D"


class RLWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each time you die, your child will succeed
    you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a dwarf.
    But that's OK, because no one is perfect, and you don't have to be to succeed.
    """
    game = "Rogue Legacy"
    option_definitions = options_table
    data_version = 5
    required_client_version = (0, 4, 2)
    web = RLWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items() if not data.event}
    location_name_to_id = {name: data.address for name, data in location_table.items() if not data.event}
    item_name_groups = item_groups
    location_name_groups = location_groups

    fountain_piece_requirement = 0

    def generate_early(self):
        # Give these at the beginning so the updated client can connect to version 1 worlds.
        self.multiworld.push_precollected(self.create_item("Blacksmith"))
        self.multiworld.push_precollected(self.create_item("Enchantress"))

        if self.get_setting("architect") == "start_unlocked":
            self.multiworld.push_precollected(self.create_item("Architect"))
        elif self.get_setting("architect") == "early":
            self.multiworld.early_items[self.player]["Architect"] = 1

        # If shuffled, make at least one blacksmith and/or enchantress upgrade local "early."
        if self.get_setting("shuffle_blacksmith"):
            possible_items = [
                "Blacksmith - Sword",
                "Blacksmith - Helm",
                "Blacksmith - Chest",
                "Blacksmith - Limbs",
                "Blacksmith - Cape",
            ]
            self.multiworld.local_early_items[self.player][self.random.choice(possible_items)] = 1

        if self.get_setting("shuffle_enchantress"):
            possible_items = [
                "Enchantress - Sword",
                "Enchantress - Helm",
                "Enchantress - Chest",
                "Enchantress - Limbs",
                "Enchantress - Cape",
            ]
            self.multiworld.local_early_items[self.player][self.random.choice(possible_items)] = 1

    def create_item(self, name: str) -> RLItem:
        item_data = item_table[name]
        return RLItem(name, item_data.classification, item_data.code, self.player)

    def create_items(self):
        item_pool: List[RLItem] = []
        location_count = len(self.multiworld.get_unfilled_locations(self.player))
        self.fountain_piece_requirement = 0

        # Create each item we can create.
        for item_data in item_table.values():
            item_pool += [
                self.create_item(item_data.name)
                for _ in range(item_data.creation_quantity(self.multiworld, self.player))
            ]

        # Handle fountain piece creation.
        if self.get_setting("fountain_door_requirement") != "bosses":
            maximum_fountain_pieces: int = self.get_setting("fountain_pieces_available").value
            remaining_item_slots = location_count - len(item_pool)
            fountain_pieces = [
                self.create_item("Piece of the Fountain")
                for _ in range(min(maximum_fountain_pieces, remaining_item_slots))
            ]

            # Calculate requirement and add to item pool.
            percentage: int = self.get_setting("fountain_pieces_percentage").value
            self.fountain_piece_requirement = round(max(len(fountain_pieces) * (percentage / 100), 1))
            item_pool += fountain_pieces

            # Log a warning if not enough locations were able to create requested pieces.
            warning(
                f"Not enough locations available in {self.multiworld.player_name[self.player]}'s RLWorld to create the "
                f"requested amount of fountain pieces."
                f"\n\tReducing available fountain pieces to: {len(fountain_pieces)}"
                f"\n\tReducing required fountain pieces to:  {self.fountain_piece_requirement}"
            )

        # If we didn't generate enough items to fill our locations, generate some filler!
        while len(item_pool) < location_count:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Defeat The Fountain", self.player)

        # Special rules to allow this specific region to "lock itself"... because why not.
        allow_self_locking_items(self.multiworld.get_region("Cheapskate Elf", self.player), "Nerdy Glasses Shrine")

    def create_regions(self):
        # Instantiate Regions
        for region_name in region_table.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        # Create locations.
        for location_data in location_table.values():
            # Ignore locations that cannot be created as the appropriate settings are not valid.
            if not location_data.can_create(self.multiworld, self.player):
                continue

            location_data.create_location(self.multiworld, self.player)

        # Connect regions and set access rules.
        for region_name, region_exits in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            exits = [region_exit.region for region_exit in region_exits]
            region.add_exits(exits, {
                region_exit.region: lambda state, region_exit=region_exit: region_exit.access_rule(state, self.player)
                for region_exit in region_exits
            })

    # TODO: Replace calls to this function with #933's solution, once that PR is merged.
    def get_setting(self, name: str) -> Option:
        return getattr(self.multiworld, name)[self.player]

    def get_filler_item_name(self) -> str:
        if self.get_setting("include_traps"):
            filler_names = filler_items["names"] + filler_items["trap_names"]
            filler_weights = filler_items["weights"] + filler_items["trap_weights"]
            return self.random.choices(filler_names, filler_weights, k=1)[0]

        return self.random.choices(filler_items["names"], filler_items["weights"], k=1)[0]

    def fill_slot_data(self) -> dict:
        slot_data: Dict[str, Union[str, int, bool]] = {
            "world_version":              WORLD_VERSION,
            "starting_gender":            self.get_setting("starting_gender").current_key,
            "starting_class":             self.get_setting("starting_class").current_key,
            "new_game_plus":              bool(self.get_setting("new_game_plus")),
            "universal_chests":           bool(self.get_setting("universal_chests")),
            "universal_fairy_chests":     bool(self.get_setting("universal_fairy_chests")),
            "chests_per_zone":            self.get_setting("chests_per_zone").value,
            "fairy_chests_per_zone":      self.get_setting("fairy_chests_per_zone").value,
            "free_diary_per_generation":  bool(self.get_setting("free_diary_per_generation")),
            "architect_fee":              self.get_setting("architect_fee").value,
            "disable_charon":             bool(self.get_setting("disable_charon")),
            "shuffle_blacksmith":         bool(self.get_setting("shuffle_blacksmith")),
            "shuffle_enchantress":        bool(self.get_setting("shuffle_enchantress")),
            "require_vendor_purchasing":  bool(self.get_setting("require_vendor_purchasing")),
            "require_skill_purchasing":   bool(self.get_setting("require_skill_purchasing")),
            "gold_gain_multiplier":       self.get_setting("gold_gain_multiplier").current_key,
            "spending_restrictions":      bool(self.get_setting("spending_restrictions")),
            "number_of_children":         self.get_setting("number_of_children").current_key,
            "castle_size":                self.get_setting("castle_size").current_key,
            "challenge_khidr":            bool(self.get_setting("khidr")),
            "challenge_alexander":        bool(self.get_setting("alexander")),
            "challenge_leon":             bool(self.get_setting("leon")),
            "challenge_herodotus":        bool(self.get_setting("herodotus")),
            "require_bosses":             bool(self.get_setting("fountain_door_requirement") != "fountain_pieces"),
            "fountain_piece_requirement": self.fountain_piece_requirement,
            "death_link":                 self.get_setting("death_link").current_key,
        }

        return slot_data
