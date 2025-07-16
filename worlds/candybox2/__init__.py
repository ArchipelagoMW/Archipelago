import typing
import uuid
from typing import TextIO, Dict

from BaseClasses import CollectionState, Tutorial, MultiWorld
from entrance_rando import ERPlacementState
from worlds.AutoWorld import World, WebWorld
from .component import setup_candy_box_2_component
from .expected_client_version import EXPECTED_CLIENT_VERSION
from .locations import location_descriptions, locations, CandyBox2LocationName
from .items import items, CandyBox2Item, candy_box_2_base_id, filler_items, CandyBox2ItemName
from .options import CandyBox2Options, candy_box_2_options_groups
from .regions import create_regions, connect_entrances, can_reach_room
from .rooms import entrance_friendly_names, CandyBox2Room
from .rules import CandyBox2RulesPackage, generate_rules_package

class CandyBox2WebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Candy Box 2 for Archipelago.",
        "English",
        "guide_en.md",
        "guide/en",
        ["Victor Tran"]
    )]

    location_descriptions = location_descriptions
    option_groups = candy_box_2_options_groups
    bug_report_page = "https://github.com/vicr123/candy-box-2/issues"

class CandyBox2World(World):
    """Candy Box 2 is a text-based browser RPG that features beautiful ASCII art"""

    game = "Candy Box 2"
    web = CandyBox2WebWorld()
    base_id = 1
    location_name_to_id = {name.value: location.id for name, location in locations.items()}
    item_name_to_id = {name.value: data.code for name, data in items.items() if data.code is not None}
    options_dataclass = CandyBox2Options
    options: CandyBox2Options
    topology_present = True

    should_randomize_hp_bar: bool
    starting_weapon: int
    progressive_jump: bool
    grimoires: int
    pains_au_chocolat: int
    font_traps: int

    entrance_randomisation: ERPlacementState = None
    original_entrances: list[tuple[str, str]]
    calculated_entrances: list[tuple[str, str]]

    rules_package: CandyBox2RulesPackage = generate_rules_package()

    def __init__(self, multiworld, player):
        super(CandyBox2World, self).__init__(multiworld, player)
        self.should_randomize_hp_bar = False
        self.starting_weapon = 0
        self.progressive_jump = False
        self.original_entrances: list[tuple[str, str]] = []
        self.calculated_entrances: list[tuple[str, str]] = []

    @staticmethod
    def stage_generate_early(multiworld: MultiWorld):
        print(f"Candy Box 2: Client Version: {EXPECTED_CLIENT_VERSION}")
        if EXPECTED_CLIENT_VERSION.endswith("+"):
            print("Candy Box 2: <!> Warning! You are generating this game using a non-stable version of the apworld.")
            print("                 If you plan to play this game with an async, it is recommended that you go back")
            print("                 and use the stable version. If you decide to continue anyway, when you start")
            print("                 the game, bookmark the \"Permalink to this version\" in the bottom left corner of")
            print("                 the game, and ensure you use this version to play.")

    def is_ut_regen(self):
        return hasattr(self.multiworld, "re_gen_passthrough")

    def generate_early(self) -> None:
        self.should_randomize_hp_bar = self.multiworld.re_gen_passthrough["Candy Box 2"]["defaults"]["hpBarRandomized"] if self.is_ut_regen() else self.options.randomise_hp_bar.value
        self.starting_weapon = self.multiworld.re_gen_passthrough["Candy Box 2"]["defaults"]["weapon"] if self.is_ut_regen() else self.options.starting_weapon.value
        self.progressive_jump = self.multiworld.re_gen_passthrough["Candy Box 2"]["defaults"]["progressiveJump"] if self.is_ut_regen() else self.options.progressive_jump.value
        self.grimoires = self.multiworld.re_gen_passthrough["Candy Box 2"]["defaults"]["grimoires"] if self.is_ut_regen() else self.options.grimoires.value
        self.pains_au_chocolat = self.multiworld.re_gen_passthrough["Candy Box 2"]["defaults"]["painsAuChocolat"] if self.is_ut_regen() else self.options.pain_au_chocolat_count.value
        self.font_traps = self.multiworld.re_gen_passthrough["Candy Box 2"]["defaults"]["fontTraps"] if self.is_ut_regen() else self.options.font_traps.value

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
                    self.multiworld.itempool += [self.create_item(name.value)]

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)

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
            "multiX": self.options.x_potion_brewing.value,
            "enableComputer": self.options.enable_computer.value,
            "scouting": self.options.scouting.value,
            "multipliers": {
                "candies": self.options.candy_production_multiplier.value,
                "candyDrops": self.options.candy_drop_multiplier.value,
                "lollipops": self.options.lollipop_production_multiplier.value
            },
            "prices": {
                "candyMerchantHat": self.options.candy_merchant_hat_price.value * 1000,
                "sorceressHat": self.options.sorceress_hat_price.value * 1000,
            },
            "health": {
                "teapot": self.options.teapot_hp.value
            },
            "defaults": {
                "weapon": self.options.starting_weapon.value,
                "hpBarRandomized": self.options.randomise_hp_bar.value,
                "progressiveJump": self.options.progressive_jump.value,
                "grimoires": self.options.grimoires.value,
                "painsAuChocolat": self.options.pain_au_chocolat_count.value,
                "fontTraps": self.options.font_traps.value,
            }
        }

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: self.completion_rule(state)
        self.multiworld.early_items[self.player][CandyBox2ItemName.PROGRESSIVE_WORLD_MAP.value] = 1
        self.rules_package.apply_location_rules(self, self.player)

    def completion_rule(self, state: CollectionState):
        return can_reach_room(state, CandyBox2Room.TOWER, self.player) and \
            state.has(CandyBox2ItemName.P_STONE, self.player) and \
            state.has(CandyBox2ItemName.L_STONE, self.player) and \
            state.has(CandyBox2ItemName.A_STONE, self.player) and \
            state.has(CandyBox2ItemName.Y_STONE, self.player) and \
            state.has(CandyBox2ItemName.LOCKED_CANDY_BOX, self.player)

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nCandy Box 2 Entrance randomisation for {self.player_name}:\n")
        slot_data = self.fill_slot_data()
        for entrance in slot_data.get("entranceInformation", []):
            spoiler_handle.write(f"{entrance_friendly_names[entrance[0]]} -> {entrance_friendly_names[entrance[1]]}\n")

    def generate_basic(self) -> None:
        if not self.should_randomize_hp_bar:
            self.multiworld.get_location(CandyBox2LocationName.HP_BAR_UNLOCK, self.player).place_locked_item(self.create_item(CandyBox2ItemName.HP_BAR))

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        er_hint_data = {}

        for entrance, destination in self.calculated_entrances:
            region = self.multiworld.get_region(entrance_friendly_names[destination], self.player)
            for location in region.locations:
                er_hint_data[location.address] = entrance_friendly_names[entrance]

        hint_data[self.player] = er_hint_data

setup_candy_box_2_component()