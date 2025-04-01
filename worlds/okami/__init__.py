from BaseClasses import Item, ItemClassification, Tutorial, Location, MultiWorld
from .Items import item_table, create_item, create_itempool
from .Regions import create_regions, randomize_act_entrances, chapter_act_info, create_events, get_shuffled_region
from .Locations import location_table, contract_locations, is_location_valid, get_location_names, TASKSANITY_START_ID, \
    get_total_locations
from .Rules import set_rules, has_paintings
from .Options import AHITOptions, slot_data_options, adjust_options, RandomizeHatOrder, EndGoal, create_option_groups
from worlds.AutoWorld import World, WebWorld, CollectionState
from worlds.generic.Rules import add_rule
from typing import List, Dict, TextIO
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type
from Utils import local_path


def launch_client():
    from .Client import launch
    launch_component(launch, name="AHITClient")


components.append(Component("A Hat in Time Client", "AHITClient", func=launch_client,
                            component_type=Type.CLIENT, icon='yatta'))

icon_paths['yatta'] = local_path('data', 'yatta.png')


# TODO: Replace
class AWebInTime(WebWorld):
    theme = "partyTime"
    option_groups = create_option_groups()
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up A Hat in Time to be played in Archipelago.",
        "English",
        "ahit_en.md",
        "setup/en",
        ["CookieCat"]
    )]


# TODO: Replace
class OkamiWorld(World):
    """
    OOOOOOOOOOKAMI
    """

    game = "Okami"
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = AHITOptions
    options: AHITOptions
    web = AWebInTime()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)


    def create_regions(self):
        # noinspection PyClassVar

        create_regions(self)

        create_events(self)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def set_rules(self):

        set_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def fill_slot_data(self) -> dict:
        slot_data: dict = {"SeedNumber": str(self.multiworld.seed),  # For shop prices
                           "SeedName": self.multiworld.seed_name,
                           "TotalLocations": get_total_locations(self)}

        for name, value in self.options.as_dict(*self.options_dataclass.type_hints).items():
            if name in slot_data_options:
                slot_data[name] = value

        return slot_data


    def collect(self, state: "CollectionState", item: "Item") -> bool:
        old_count: int = state.count(item.name, self.player)
        change = super().collect(state, item)
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        old_count: int = state.count(item.name, self.player)
        change = super().remove(state, item)
        return change

