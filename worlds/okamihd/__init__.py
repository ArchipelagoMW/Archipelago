import random
from BaseClasses import Item, ItemClassification, Tutorial, Location, MultiWorld
from .Items import item_table, create_item, create_multiple_items, create_junk_items, item_frequencies, \
    create_brush_techniques_items, get_item_name_to_id_dict, create_divine_instrument_items, karmic_transformers, \
    progressive_weapons
from .Regions import create_regions
from .Locations import is_location_valid, get_total_locations, get_location_names, okami_events
from .Rules import set_rules
from .Options import create_option_groups, OkamiOptions, slot_data_options, KarmicTransformers
from worlds.AutoWorld import World, WebWorld, CollectionState
from typing import List, Dict, TextIO
from Utils import local_path
from .Types import OkamiItem
from .Enums.DivineInstruments import DivineInstruments
from .Enums.RegionNames import RegionNames


# TODO: Replace
class OkamiWebWolrd(WebWorld):
    theme = "grassFlowers"
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
    Okami HD
    """

    game = "Okami HD"
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

        di = None

        if not world.options.ProgressiveWeapons:
            # Get a random tier 1 divine instrument to start with.
            di = random.choice(list(world.item_name_groups.get('divine_instrument_tier_1')))
            world.push_precollected(
                OkamiItem(di, ItemClassification.progression, get_item_name_to_id_dict()[di], world.player))
        else:
            #FIXME
            di_name = random.choice(progressive_weapons.keys())
            di = progressive_weapons[di_name]
            world.push_precollected(OkamiItem(di_name,ItemClassification.progression,di.code,world.player))
            for (progressive_waepon_name,progressive_weapon) in progressive_weapons:
                if di_name==progressive_waepon_name:
                    count=4
                else:
                    count=5
                for i in range(count):
                    itempool += [OkamiItem(di_name, di.classification, di.code, world.player)]

        match world.options.KarmicTransformers:
            case KarmicTransformers.option_precollected:
                for (k_name,k) in karmic_transformers.items():
                    world.push_precollected(OkamiItem(k_name,k.classification,k.code,world.player))
            case KarmicTransformers.option_in_item_pool:
                for (k_name, k) in karmic_transformers.items():
                    if k_name=="Karmic Returner":
                        world.push_precollected(OkamiItem(k_name, k.classification, k.code, world.player))
                    else:
                        itempool+=[OkamiItem(k_name, k.classification, k.code, world.player)]

        # Event Items Creation
        for name in RegionNames:
            if name in okami_events:
                for (event_name, event_data) in okami_events[name].items():
                    if isinstance(event_data.precollected, bool):
                        precollected_item_event_state = event_data.precollected
                    else:
                        precollected_item_event_state = event_data.precollected(world.options)

                        if precollected_item_event_state:
                            # With the current options this event is unlocked at the start, so we create a precollected item
                            # Classification probably doesn't matter much for precollected items I'd guess
                            world.push_precollected(
                                OkamiItem(event_name, ItemClassification.progression, event_data.id, world.player))
                        # If it's precollected, no need to add it to the itempool
                        else:
                            if isinstance(event_data.is_event_item, bool):
                                is_event_item_state = event_data.is_event_item
                            else:
                                is_event_item_state = event_data.is_event_item(world.options)
                            if is_event_item_state:
                                # With the current options this event becomes its own item, so we need to add it to the item pool
                                itempool += OkamiItem(event_name, ItemClassification.progression, event_data.id,
                                                      world.player)

        itempool += create_brush_techniques_items(world)
        for name in item_table.keys():
            item_type: ItemClassification = item_table.get(name).classification
            itempool += create_multiple_items(world, name, item_frequencies.get(name, 1), item_type)
        itempool += create_junk_items(world, get_total_locations(world) - len(itempool))

        return itempool

    # Probably has to be a better way to do this.
    item_name_groups = {
        "divine_instrument_tier_1": [DivineInstruments.DIVINE_RETRIBUTION.value.item_name,
                                     DivineInstruments.DEVOUT_BEADS.value.item_name,
                                     DivineInstruments.TSUMUGARI.value.item_name],
        "divine_instrument_tier_2": [DivineInstruments.SNARLING_BEAST.value.item_name,
                                     DivineInstruments.LIFE_BEADS.value.item_name,
                                     DivineInstruments.SEVEN_STRIKE.value.item_name],
        "divine_instrument_tier_3": [DivineInstruments.INFINITY_JUDGE.value.item_name,
                                     DivineInstruments.EXORCISM_BEADS.value.item_name,
                                     DivineInstruments.BLADE_OF_KUSANAGI.value.item_name],
        "divine_instrument_tier_4": [DivineInstruments.TRINITY_MIRROR.value.item_name,
                                     DivineInstruments.RESURRECTION_BEADS.value.item_name,
                                     DivineInstruments.EIGHT_WONDER.value.item_name],
        "divine_instrument_tier_5": [DivineInstruments.SOLAR_FLARE.value.item_name,
                                     DivineInstruments.TUNDRA_BEADS.value.item_name,
                                     DivineInstruments.THUNDER_EDGE.value.item_name]
    }
