# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import Item, MultiWorld, Tutorial
from Fill import fill_restrictive
from .Items import item_table, item_groups, MeritousItem
from .Locations import location_table, MeritousLocation
from .Options import MeritousOptions, cost_scales
from .Regions import create_regions
from .Rules import set_rules
from ..AutoWorld import World, WebWorld

client_version = 1


class MeritousWeb(WebWorld):
    tutorials = [Tutorial(
        "Meritous Setup Guide",
        "A guide to setting up the Archipelago Meritous software on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["KewlioMZX"]
    )]
    theme = "ice"
    bug_report_page = "https://github.com/FelicitusNeko/meritous-ap/issues"


class MeritousWorld(World):
    """
        Meritous Gaiden is a procedurally generated bullet-hell dungeon crawl game.
        Five generations after the Orcus Dome incident, strange experiments conducted in a new
        structure on the moon are tearing at the very fabric of reality...
    """

    game: str = "Meritous"
    topology_present: False

    web = MeritousWeb()

    item_name_to_id = item_table
    location_name_to_id = location_table
    item_name_groups = item_groups

    # NOTE: Remember to change this before this game goes live
    required_client_version = (0, 2, 4)

    options: MeritousOptions
    options_dataclass = MeritousOptions

    def __init__(self, multiworld: MultiWorld, player: int):
        super(MeritousWorld, self).__init__(multiworld, player)
        self.goal = 0
        self.include_evolution_traps = False
        self.include_psi_keys = False
        self.item_cache_cost = 0
        self.death_link = False

    @staticmethod
    def _is_progression(name):
        return "PSI Key" in name or name in [
            "Cursed Seal", "Agate Knife", "Dodge Enhancer",
            "Shield Boost", "Metabolism", "Circuit Booster"
        ]

    def create_item(self, name: str) -> Item:

        return MeritousItem(name, self._is_progression(
            name), item_table[name], self.player)

    def create_event(self, event: str):
        event = MeritousItem(event, True, None, self.player)
        event.type = "Victory"
        return event

    def _create_item_in_quantities(self, name: str, qty: int) -> [Item]:
        return [self.create_item(name) for _ in range(0, qty)]

    def _make_crystals(self, qty: int) -> [MeritousItem]:
        crystal_pool = []

        for _ in range(0, qty):
            crystal_pool.append(self.create_filler())

        return crystal_pool

    def get_filler_item_name(self) -> str:
        rand_crystals = self.multiworld.random.randrange(0, 32)
        if rand_crystals < 16:
            return "Crystals x500"
        elif rand_crystals < 28:
            return "Crystals x1000"
        else:
            return "Crystals x2000"

    def generate_early(self):
        self.goal = self.options.goal.value
        self.include_evolution_traps = self.options.include_evolution_traps.value
        self.include_psi_keys = self.options.include_psi_keys.value
        self.item_cache_cost = self.options.item_cache_cost.value
        self.death_link = self.options.death_link.value

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def create_items(self):
        frequencies = [0, # Nothing [0]
                       25, 23, 22, # PSI Enhancements [1-3]
                       1, 1, 1, 1, 1, 1, 1, 1, 1, # Artifacts [4-12]
                       1, 1, 1, # PSI Keys [13-15]
                       0, 0, # Seal & Knife [16-17]
                       3] # Traps [18]
        location_count = len(location_table) - 2
        item_pool = []

        if not self.include_psi_keys:
            location_count -= 3
            for i in range(3):
                frequencies[i - 6] = 0

        if not self.include_evolution_traps:
            frequencies[-1] = 0
            location_count -= 3

        for i, name in enumerate(item_table):
            if i < len(frequencies):
                item_pool += self._create_item_in_quantities(
                    name, frequencies[i])

        if len(item_pool) < location_count:
            item_pool += self._make_crystals(location_count - len(item_pool))

        self.multiworld.itempool += item_pool

    def set_rules(self):
        set_rules(self.multiworld, self.player)
        if self.goal == 0:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_any(
                ["Victory", "Full Victory"], self.player)
        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                "Full Victory", self.player)

    def generate_basic(self):
        self.multiworld.get_location("Place of Power", self.player).place_locked_item(
            self.create_item("Cursed Seal"))
        self.multiworld.get_location("The Last Place You'll Look", self.player).place_locked_item(
            self.create_item("Agate Knife"))
        self.multiworld.get_location("Wervyn Anixil", self.player).place_locked_item(
            self.create_event("Victory"))
        self.multiworld.get_location("Wervyn Anixil?", self.player).place_locked_item(
            self.create_event("Full Victory"))
        for boss in ["Meridian", "Ataraxia", "Merodach"]:
            self.multiworld.get_location(f"{boss} Defeat", self.player).place_locked_item(
                self.create_event(f"{boss} Defeated"))

        if not self.include_psi_keys:
            psi_keys = []
            psi_key_storage = []
            for i in range(0, 3):
                psi_keys += [self.create_item(f"PSI Key {i + 1}")]
                psi_key_storage += [self.multiworld.get_location(
                    f"PSI Key Storage {i + 1}", self.player)]

            fill_restrictive(self.multiworld, self.multiworld.get_all_state(
                False), psi_key_storage, psi_keys)

        if not self.include_evolution_traps:
            for boss in ["Meridian", "Ataraxia", "Merodach"]:
                self.multiworld.get_location(boss, self.player).place_locked_item(
                    self.create_item("Evolution Trap"))

    def fill_slot_data(self) -> dict:
        return {
            "goal": self.goal,
            "cost_scale": cost_scales[self.item_cache_cost],
            "death_link": self.death_link
        }
