import settings
import typing

from typing import Dict
from BaseClasses import Item, Location, MultiWorld, Tutorial, ItemClassification
from .Items import ItemData, FF1Items, FF1_STARTER_ITEMS, FF1_PROGRESSION_LIST, FF1_BRIDGE
from .Locations import EventId, FF1Locations, generate_rule, CHAOS_TERMINATED_EVENT
from .Options import ff1_options
from ..AutoWorld import World, WebWorld


class FF1Settings(settings.Group):
    display_msgs: bool = True


class FF1Web(WebWorld):
    options_page = "https://finalfantasyrandomizer.com/"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy multiworld. This guide only covers playing multiworld.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["jat2980"]
    )]


class FF1World(World):
    """
    Final Fantasy 1, originally released on the NES on 1987, is the game that started the beloved, long running series.
    The randomizer takes the original 8-bit Final Fantasy game for NES (USA edition) and allows you to
    shuffle important aspects like the location of key items, the difficulty of monsters and fiends,
    and even the location of towns and dungeons.
    Part puzzle and part speed-run, it breathes new life into one of the most influential games ever made.
    """

    option_definitions = ff1_options
    settings: typing.ClassVar[FF1Settings]
    settings_key = "ffr_options"
    game = "Final Fantasy"
    topology_present = False
    data_version = 2

    ff1_items = FF1Items()
    ff1_locations = FF1Locations()
    item_name_groups = ff1_items.get_item_names_per_category()
    item_name_to_id = ff1_items.get_item_name_to_code_dict()
    location_name_to_id = ff1_locations.get_location_name_to_address_dict()

    web = FF1Web()

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.locked_items = []
        self.locked_locations = []

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        # Fail generation if there are no items in the pool
        for player in multiworld.get_game_players(cls.game):
            options = get_options(multiworld, 'items', player)
            assert options,\
                f"FFR settings submitted with no key items ({multiworld.get_player_name(player)}). Please ensure you " \
                f"generated the settings using finalfantasyrandomizer.com AND enabled the AP flag"

    def create_regions(self):
        locations = get_options(self.multiworld, 'locations', self.player)
        rules = get_options(self.multiworld, 'rules', self.player)
        menu_region = self.ff1_locations.create_menu_region(self.player, locations, rules, self.multiworld)
        terminated_event = Location(self.player, CHAOS_TERMINATED_EVENT, EventId, menu_region)
        terminated_item = Item(CHAOS_TERMINATED_EVENT, ItemClassification.progression, EventId, self.player)
        terminated_event.place_locked_item(terminated_item)

        items = get_options(self.multiworld, 'items', self.player)
        goal_rule = generate_rule([[name for name in items.keys() if name in FF1_PROGRESSION_LIST and name != "Shard"]],
                                  self.player)
        if "Shard" in items.keys():
            def goal_rule_and_shards(state):
                return goal_rule(state) and state.has("Shard", self.player, 32)
            terminated_event.access_rule = goal_rule_and_shards
        if "MARK" in items.keys():
            # Fail generation for Noverworld and provide link to old FFR website
            raise Exception("FFR Noverworld seeds must be generated on an older version of FFR. Please ensure you "
                            "generated the settings using 4-4-0.finalfantasyrandomizer.com")
        menu_region.locations.append(terminated_event)
        self.multiworld.regions += [menu_region]

    def create_item(self, name: str) -> Item:
        return self.ff1_items.generate_item(name, self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has(CHAOS_TERMINATED_EVENT, self.player)

    def create_items(self):
        items = get_options(self.multiworld, 'items', self.player)
        if FF1_BRIDGE in items.keys():
            self._place_locked_item_in_sphere0(FF1_BRIDGE)
        if items:
            possible_early_items = [name for name in FF1_STARTER_ITEMS if name in items.keys()]
            if possible_early_items:
                progression_item = self.multiworld.random.choice(possible_early_items)
                self._place_locked_item_in_sphere0(progression_item)

        items = [self.create_item(name) for name, data in items.items() for x in range(data['count']) if name not in
                 self.locked_items]

        self.multiworld.itempool += items

    def _place_locked_item_in_sphere0(self, progression_item: str):
        if progression_item:
            rules = get_options(self.multiworld, 'rules', self.player)
            sphere_0_locations = [name for name, rules in rules.items()
                                  if rules and len(rules[0]) == 0 and name not in self.locked_locations]
            if sphere_0_locations:
                initial_location = self.multiworld.random.choice(sphere_0_locations)
                locked_location = self.multiworld.get_location(initial_location, self.player)
                locked_location.place_locked_item(self.create_item(progression_item))
                self.locked_items.append(progression_item)
                self.locked_locations.append(locked_location.name)

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        return slot_data

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(["Heal", "Pure", "Soft", "Tent", "Cabin", "House"])


def get_options(world: MultiWorld, name: str, player: int):
    return getattr(world, name, None)[player].value
