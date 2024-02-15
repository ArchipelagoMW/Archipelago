# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import BumpStikItem, item_table, item_groups
from .Locations import location_table
from .Options import *
from .Regions import create_regions
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import forbid_item


class BumpStikWeb(WebWorld):
    tutorials = [Tutorial(
        "Bumper Stickers Setup Tutorial",
        "A guide to setting up the Archipelago Bumper Stickers software on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["KewlioMZX"]
    )]
    theme = "stone"
    bug_report_page = "https://github.com/FelicitusNeko/FlixelBumpStik/issues"


class BumpStikWorld(World):
    """
        Bumper Stickers is a match-three puzzle game unlike any you've seen.
        Launch Bumpers onto the field, and match them in sets of three of the same color.
        How long can you go without getting Jammed?
    """

    game = "Bumper Stickers"
    web = BumpStikWeb()

    item_name_to_id = item_table
    location_name_to_id = location_table
    item_name_groups = item_groups

    data_version = 1

    required_client_version = (0, 3, 8)

    option_definitions = bumpstik_options

    def __init__(self, world: MultiWorld, player: int):
        super(BumpStikWorld, self).__init__(world, player)
        self.task_advances = TaskAdvances.default
        self.turners = Turners.default
        self.paint_cans = PaintCans.default
        self.traps = Traps.default
        self.rainbow_trap_weight = RainbowTrapWeight.default
        self.spinner_trap_weight = SpinnerTrapWeight.default
        self.killer_trap_weight = KillerTrapWeight.default

    def create_item(self, name: str) -> Item:
        return BumpStikItem(name, ItemClassification.filler, item_table[name], self.player)

    def create_event(self, event: str) -> Item:
        return BumpStikItem(event, ItemClassification.filler, None, self.player)

    def _create_item_in_quantities(self, name: str, qty: int) -> [Item]:
        return [self.create_item(name) for _ in range(0, qty)]

    def _create_traps(self):
        max_weight = self.rainbow_trap_weight + \
            self.spinner_trap_weight + self.killer_trap_weight
        rainbow_threshold = self.rainbow_trap_weight
        spinner_threshold = self.rainbow_trap_weight + self.spinner_trap_weight
        trap_return = [0, 0, 0]

        for i in range(self.traps):
            draw = self.multiworld.random.randrange(0, max_weight)
            if draw < rainbow_threshold:
                trap_return[0] += 1
            elif draw < spinner_threshold:
                trap_return[1] += 1
            else:
                trap_return[2] += 1

        return trap_return

    def get_filler_item_name(self) -> str:
        return "Nothing"

    def generate_early(self):
        self.task_advances = self.multiworld.task_advances[self.player].value
        self.turners = self.multiworld.turners[self.player].value
        self.paint_cans = self.multiworld.paint_cans[self.player].value
        self.traps = self.multiworld.trap_count[self.player].value
        self.rainbow_trap_weight = self.multiworld.rainbow_trap_weight[self.player].value
        self.spinner_trap_weight = self.multiworld.spinner_trap_weight[self.player].value
        self.killer_trap_weight = self.multiworld.killer_trap_weight[self.player].value

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def create_items(self):
        frequencies = [
            0, 0, self.task_advances, self.turners, 0, self.paint_cans, 5, 25, 33
        ] + self._create_traps()
        item_pool = []

        for i, name in enumerate(item_table):
            if i < len(frequencies):
                item_pool += self._create_item_in_quantities(
                    name, frequencies[i])

        item_delta = len(location_table) - len(item_pool)
        if item_delta > 0:
            item_pool += self._create_item_in_quantities(
                "Score Bonus", item_delta)

        self.multiworld.itempool += item_pool

    def set_rules(self):
        for x in range(1, 32):
            self.multiworld.get_location(f"Treasure Bumper {x + 1}", self.player).access_rule = \
                lambda state, x = x: state.has("Treasure Bumper", self.player, x)
        for x in range(1, 5):
            self.multiworld.get_location(f"Bonus Booster {x + 1}", self.player).access_rule = \
                lambda state, x = x: state.has("Booster Bumper", self.player, x)
        self.multiworld.get_location("Level 5 - Cleared all Hazards", self.player).access_rule = \
            lambda state: state.has("Hazard Bumper", self.player, 25)
            
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Booster Bumper", self.player, 5) and \
            state.has("Treasure Bumper", self.player, 32)

