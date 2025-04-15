import typing
import uuid
from typing import TextIO, Dict

from BaseClasses import CollectionState, Tutorial
from entrance_rando import ERPlacementState
from worlds.AutoWorld import World, WebWorld
from .locations import location_descriptions, locations
from .items import items, CandyBox2Item, candy_box_2_base_id
from .options import CandyBox2Options
from .regions import create_regions, connect_entrances, quest_names_reverse, quest_friendly_names
from .rules import set_rules

EXPECTED_CLIENT_VERSION = "20250409-1+"

class CandyBox2WebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Candy Box 2 for Archipelago.",
        "English",
        "guide_en.md",
        "setup/en",
        ["Victor Tran"]
    )]

    location_descriptions = location_descriptions

class CandyBox2World(World):
    """Text-based web game with fun ASCII art"""

    game = "Candy Box 2"
    web = CandyBox2WebWorld()
    base_id = 1
    location_name_to_id = locations
    item_name_to_id = {name: data.code for name, data in items.items() if data.code is not None}
    options_dataclass = CandyBox2Options
    options: CandyBox2Options
    topology_present = True

    entrance_randomisation: ERPlacementState = None
    should_randomize_hp_bar: bool
    starting_weapon: int
    original_entrances: list[tuple[str, str]]
    calculated_entrances: list[tuple[str, str]]

    def __init__(self, multiworld, player):
        super(CandyBox2World, self).__init__(multiworld, player)
        self.should_randomize_hp_bar = False
        self.starting_weapon = 0
        self.original_entrances: list[tuple[str, str]] = []
        self.calculated_entrances: list[tuple[str, str]] = []

    def is_ut_regen(self):
        return hasattr(self.multiworld, "re_gen_passthrough")

    def generate_early(self) -> None:
        self.should_randomize_hp_bar = self.multiworld.re_gen_passthrough["Candy Box 2"]["defaults"]["hpBarRandomized"] if self.is_ut_regen() else self.options.randomise_hp_bar.value
        self.starting_weapon = self.multiworld.re_gen_passthrough["Candy Box 2"]["defaults"]["weapon"] if self.is_ut_regen() else self.options.starting_weapon.value

    def create_regions(self) -> None:
        return create_regions(self)

    def create_item(self, name: str) -> CandyBox2Item:
        data = items[name]
        item = CandyBox2Item(name, data.classification, data.code, self.player)

        return item

    def create_items(self):
        for name, data in items.items():
            required_amount = data.required_amount(self)
            if required_amount > 0:
                for i in range(required_amount):
                    if not self.options.randomise_hp_bar and name == "HP Bar":
                        continue
                    self.multiworld.itempool += [self.create_item(name)]

    def connect_entrances(self) -> None:
        self.calculated_entrances = connect_entrances(self)

    def interpret_slot_data(self, slot):
        return slot

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            "uuid": str(uuid.uuid4()),
            "entranceInformation": self.calculated_entrances,
            "deathLink": self.options.death_link.value,
            "energyLink": self.options.energy_link.value,
            "gifting": self.options.gifting.value,
            "expectedClientVersion": EXPECTED_CLIENT_VERSION,
            "multipliers": {
                "candies": self.options.candy_production_multiplier.value,
                "lollipops": self.options.lollipop_production_multiplier.value
            },
            "prices": {
                "candyMerchantHat": self.options.candy_merchant_hat_price.value,
                "sorceressHat": self.options.sorceress_hat_price.value,
            },
            "health": {
                "teapot": self.options.teapot_hp.value
            },
            "defaults": {
                "weapon": self.options.starting_weapon.value,
                "hpBarRandomized": self.options.randomise_hp_bar.value
            }
        }

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: self.completion_rule(state)
        set_rules(self, self.player)

    def completion_rule(self, state: CollectionState):
        return state.has("Progressive World Map", self.player, 7) and \
            state.has("P Stone", self.player) and \
            state.has("L Stone", self.player) and \
            state.has("A Stone", self.player) and \
            state.has("Y Stone", self.player) and \
            state.has("Locked Candy Box", self.player)

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nCandy Box 2 Entrance randomisation for {self.player_name}:\n")
        slot_data = self.fill_slot_data()
        for entrance in slot_data.get("entranceInformation", []):
            spoiler_handle.write(f"{quest_friendly_names[quest_names_reverse[entrance[0]]]} -> {quest_friendly_names[quest_names_reverse[entrance[1]]]}\n")

    def generate_basic(self) -> None:
        if not self.should_randomize_hp_bar:
            self.multiworld.get_location("HP Bar Unlock", self.player).place_locked_item(self.create_item("HP Bar"))

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        er_hint_data = {}

        for entrance, destination in self.calculated_entrances:
            region = self.multiworld.get_region(quest_friendly_names[quest_names_reverse[destination]], self.player)
            for location in region.locations:
                er_hint_data[location.address] = quest_friendly_names[quest_names_reverse[entrance]]

        hint_data[self.player] = er_hint_data
