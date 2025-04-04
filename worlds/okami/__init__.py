from BaseClasses import Item, ItemClassification, Tutorial, Location, MultiWorld
from .Items import item_table, create_item, create_multiple_items,create_junk_items,item_frequencies
from .Regions import create_regions2
from .Locations import is_location_valid,get_total_locations
from .Rules import set_rules
from .Options import create_option_groups, OkamiOptions, slot_data_options
from worlds.AutoWorld import World, WebWorld, CollectionState
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
    #TODO:Fixme
    location_name_to_id = get_location_names()
    options_dataclass = OkamiOptions
    options: OkamiOptions
    web = AWebInTime()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)


    def create_regions(self):
        # noinspection PyClassVar

        create_regions2(self)

    def create_items(self):
        self.multiworld.itempool += self.create_itempool()

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

    def create_itempool(world: "OkamiWorld") -> List[Item]:
        itempool: List[Item] = []

        for name in item_table.keys():
            item_type: ItemClassification = item_table.get(name).classification
            itempool += create_multiple_items(world, name, item_frequencies.get(name, 1), item_type)
        itempool += create_junk_items(world, get_total_locations(world) - len(itempool))
        return itempool
