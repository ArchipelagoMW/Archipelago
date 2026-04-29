import random
from BaseClasses import Item, ItemClassification, Tutorial, Location, MultiWorld
from .Items import item_table, create_item, create_multiple_items, create_junk_items, get_item_name_to_id_dict, \
    karmic_transformers, \
    progressive_weapons, create_standard_item, create_static_precollected_item_list
from .Regions import create_regions
from .Locations import get_location_names, get_total_locations
from .RegionsData import okami_events,okami_locations
from .Rules import set_rules
from .Options import create_option_groups, OkamiOptions, slot_data_options, KarmicTransformers
from worlds.AutoWorld import World, WebWorld, CollectionState
from typing import List
from .Types import OkamiItem, resolve_option_callable
from .Enums.DivineInstruments import DivineInstruments
from .Enums.RegionNames import RegionNames



class OkamiWebWolrd(WebWorld):
    theme = "grassFlowers"
    option_groups = create_option_groups()
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Okami HD to be played in Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Axertin","Ragmoa"]
    )]


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
        return create_standard_item(self, name)

    def fill_slot_data(self) -> dict:
        slot_data: dict = {
            "SeedNumber": str(self.multiworld.seed),  # For shop prices
            "SeedName": self.multiworld.seed_name,
            "TotalLocations": get_total_locations(self),
            # Client configuration
            "supported_client_version": "0.7.3",  # Minimum client version required
        }

        # Add game options to slot_data
        for name, value in self.options.as_dict(*slot_data_options).items():
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
        precollected_items: List [Item] = []

        # Static Precollected Items
        precollected_items = create_static_precollected_item_list(world)

        if not world.options.ProgressiveWeapons:
            # Get a random tier 1 divine instrument to start with.
            di = random.choice(list(world.item_name_groups.get('divine_instrument_tier_1')))
            precollected_items.append(create_item(di, get_item_name_to_id_dict()[di], ItemClassification.progression, world))
            # Create other weapons
            for (divine_instrument_data) in list(DivineInstruments):
                if divine_instrument_data.value.item_name != di:
                    itempool+=[create_item(divine_instrument_data.value.item_name,divine_instrument_data.value.code,ItemClassification.progression,world)]
        else:
            # Get a random progressive weapon
            (di_name, di) = random.choice(list(progressive_weapons.items()))
            precollected_items.append(create_item(di_name, di.code, ItemClassification.progression, world))
            # Create other progressive weapons
            for (progressive_weapon_name, progressive_weapon) in progressive_weapons.items():
                if di_name == progressive_weapon_name:
                    count = 4
                else:
                    count = 5
                for i in range(count):
                    itempool += [create_item(di_name, di.code, di.classification, world)]

        match world.options.KarmicTransformers:
            case KarmicTransformers.option_precollected:
                for (k_name, k) in karmic_transformers.items():
                    precollected_items.append(create_item(k_name, k.code, k.classification, world))
            case KarmicTransformers.option_in_item_pool:
                for (k_name, k) in karmic_transformers.items():
                    if k_name == "Karmic Returner":
                        precollected_items.append(create_item(k_name, k.code, k.classification, world))
                    else:
                        itempool += [create_item(k_name, k.code, k.classification, world)]

        # Event Items Creation
        for name in RegionNames:
            if name in okami_events:
                for (event_name, event_data) in okami_events[name].items():
                    precollected_item_event_state = resolve_option_callable(event_data.precollected, world)

                    if precollected_item_event_state:
                        # With the current options this event is unlocked at the start, so we create a precollected item
                        # Classification probably doesn't matter much for precollected items I'd guess
                        world.push_precollected(
                            create_item(event_name, event_data.id, ItemClassification.progression, world))
                    # If it's precollected, no need to add it to the itempool
                    else:
                        is_event_item_state = resolve_option_callable(event_data.is_event_item, world)

                        if is_event_item_state:
                            # With the current options this event becomes its own item, so we need to add it to the item pool
                            itempool += [create_standard_item(world,event_data.event_item_name)]

        for name in item_table.keys():
            item_type: ItemClassification = item_table.get(name).classification
            item_count:int = resolve_option_callable(item_table.get(name).count_in_pool,world)
            if item_count > 0:
                itempool += create_multiple_items(world, name, item_count, item_type)

        itempool += create_junk_items(world, get_total_locations(world) - len(itempool))

        for pi in precollected_items:
            world.push_precollected(pi)

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
                                     DivineInstruments.THUNDER_EDGE.value.item_name],
        "canine_warriors": [
            "Save Rei",
            "Save Shin",
            "Save Chi",
            "Save Ko",
            "Save Tei",
            "Loyalty Orb",
            "Justice Orb",
            "Duty Orb"
        ],

        "soup_ingredients":[
            "Ogre Liver",
            "Ice Lips",
            "Fire Eye",
            "Black Demon Horn"
        ]
    }
