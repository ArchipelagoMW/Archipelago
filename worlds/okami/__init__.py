import random
from BaseClasses import Item, ItemClassification, Tutorial, Location, MultiWorld
from .Items import item_table, create_item, create_multiple_items, create_junk_items, item_frequencies, \
    create_brush_techniques_items, get_item_name_to_id_dict, create_divine_instrument_items
from .Regions import create_regions
from .Locations import is_location_valid,get_total_locations, get_location_names
from .Rules import set_rules
from .Options import create_option_groups, OkamiOptions, slot_data_options
from worlds.AutoWorld import World, WebWorld, CollectionState
from typing import List, Dict, TextIO
from Utils import local_path
from .Types import DivineInstruments, OkamiItem



# TODO: Replace
class OkamiWebWolrd(WebWorld):
    theme = "partyTime"
    option_groups = create_option_groups()
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Okami HD to be played in Archipelago.",
        "English",
        "",
        "",
        [""]
    )]


# TODO: Replace
class OkamiWorld(World):
    """
    OKami HD
    """

    game = "Okami"
    item_name_to_id = get_item_name_to_id_dict()
    location_name_to_id = get_location_names()
    options_dataclass = OkamiOptions
    options: OkamiOptions
    web = OkamiWebWolrd()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)


    def create_regions(self):
        # noinspection PyClassVar

        create_regions(self)

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
        itempool += create_brush_techniques_items(world)
        itempool += create_divine_instrument_items(world)
        for name in item_table.keys():
            item_type: ItemClassification = item_table.get(name).classification
            itempool += create_multiple_items(world, name, item_frequencies.get(name, 1), item_type)
        itempool += create_junk_items(world, get_total_locations(world) - len(itempool))

        if world.options.StartWithDivineInstrument:
            # Get a random divine instrument.
            di = random.choice(list(world.item_name_groups.get('divine_instrument')))
            world.push_precollected(OkamiItem(di,ItemClassification.progression,0,world.player))

        return itempool

    # Probably has to be a better way to do this.
    item_name_groups = {
            "divine_instrument":[DivineInstruments.DIVINE_RETRIBUTION.value.item_name,
                                 DivineInstruments.DEVOUT_BEADS.value.item_name,
                                 DivineInstruments.TSUMUGARI.value.item_name]
    }