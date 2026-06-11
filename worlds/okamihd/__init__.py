import Fill
from BaseClasses import Item, ItemClassification, Tutorial, MultiWorld, Location, LocationProgressType
from Utils import visualize_regions
from .Enums.LocationType import excluded_biteable_location_types
from .Items import item_table, create_item, create_multiple_items, create_junk_items, get_item_name_to_id_dict, \
    karmic_transformers, \
    progressive_weapons, create_standard_item, create_static_precollected_item_list, global_local_items, \
    soup_ingredient_local_items
from .Regions import create_regions, get_region_name
from .Locations import get_location_names, get_total_locations, get_unfilled_locations_count
from .RegionsData import okami_events, okami_locations, okami_shop_locations
from .Rules import set_completion_rules
from .Options import create_option_groups, OkamiOptions, slot_data_options, KarmicTransformers
from worlds.AutoWorld import World, WebWorld, CollectionState
from typing import List
from .Types import OkamiItem, resolve_option_callable, LocalItem
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
        ["Axertin", "Ragmoa"]
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
    local_items = []

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    def create_regions(self):
        # noinspection PyClassVar

        create_regions(self)
        # DEBUG
        #visualize_regions(self.multiworld.get_region("Menu", self.player),"G:\projets\OkamiAP\worlds\okamihd\docs\OkamiHD.puml")

    def create_items(self):
        self.prepare_local_items()
        self.multiworld.itempool += self.create_itempool()

    def prepare_local_items(self):
        self.local_items = global_local_items.copy()
        if not self.options.IngredientsInMoonCave.value:
            self.local_items.append(soup_ingredient_local_items)

    def set_rules(self):

        set_completion_rules(self)

    def create_item(self, name: str) -> Item:
        return create_standard_item(self, name)

    def fill_slot_data(self) -> dict:
        slot_data: dict = {
            "SeedNumber": str(self.multiworld.seed),  # For shop prices
            "SeedName": self.multiworld.seed_name,
            "TotalLocations": get_total_locations(self),
            # Client configuration
            "supported_client_version": "0.8.2",  # Minimum client version required
        }

        # Add game options to slot_data
        for name, value in self.options.as_dict(*slot_data_options).items():
            slot_data[name] = value

        return slot_data

    def get_local_items_name(self) -> List[str]:
        local_items_names: List[str] = []
        for l in self.local_items:
            local_items_names += l.items
        return local_items_names

    def pre_fill(self) -> None:
        from Fill import fill_restrictive, FillError

        # local items randomization
        attempts = 5
        for local_item_data in self.local_items:
            valid_locations = self.get_valid_local_item_locations(local_item_data)
            local_item_pool = []
            state = self.multiworld.get_all_state(collect_pre_fill_items=True, perform_sweep=False)
            for i in local_item_data.items:
                local_item = self.create_item(i)
                state.remove(local_item)
                local_item_pool.append(local_item)
            state.sweep_for_advancements()
            for a in range(attempts):
                try:
                    fill_step_name = (local_item_data.prefill_name if local_item_data.prefill_name is not None else
                                      local_item_data.items[0]) + " for " + self.player_name + " (Try " + str(
                        a + 1) + ')'
                    print("Prefilling " + fill_step_name)
                    locations = valid_locations.copy()
                    item_pool = local_item_pool.copy()
                    # Important - Archipelago will try to place on every location in the list by order, so we shuffle it to not always get the same result.
                    self.multiworld.random.shuffle(locations)
                    fill_restrictive(self.multiworld, state, locations, item_pool, single_player_placement=True,
                                     name=fill_step_name)
                except FillError:
                    continue
                break

    def get_pre_fill_items(self) -> List["Item"]:
        res = []
        for i in self.get_local_items_name():
            res.append(self.create_item(i))
        return res

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        old_count: int = state.count(item.name, self.player)
        change = super().collect(state, item)
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        old_count: int = state.count(item.name, self.player)
        change = super().remove(state, item)
        return change

    def create_itempool(self) -> List[Item]:
        itempool: List[Item] = []
        precollected_items: List[Item] = []

        # Static Precollected Items
        precollected_items = create_static_precollected_item_list(self)

        if not self.options.ProgressiveWeapons:
            # Create normal weapons
            for (divine_instrument_data) in list(DivineInstruments):
                if divine_instrument_data.value.item_name != DivineInstruments.DIVINE_RETRIBUTION.value.item_name:
                    itempool += [create_item(divine_instrument_data.value.item_name, divine_instrument_data.value.code,
                                             ItemClassification.progression, self)]

        else:
            # Create progressive weapons
            for (progressive_weapon_name, progressive_weapon) in progressive_weapons.items():
                # Only Randomize 4 Progressive Mirrors since we start with Divine Retribution
                if progressive_weapon_name == 'Progressive Mirror':
                    count = 4
                else:
                    count = 5
                for i in range(count):
                    itempool += [
                        create_item(progressive_weapon_name, progressive_weapon.code, progressive_weapon.classification,
                                    self)]

        match self.options.KarmicTransformers:
            case KarmicTransformers.option_precollected:
                for (k_name, k) in karmic_transformers.items():
                    precollected_items.append(create_item(k_name, k.code, k.classification, self))
            case KarmicTransformers.option_in_item_pool:
                for (k_name, k) in karmic_transformers.items():
                    if k_name == "Karmic Returner":
                        precollected_items.append(create_item(k_name, k.code, k.classification, self))
                    else:
                        itempool += [create_item(k_name, k.code, k.classification, self)]

        # Event Items Creation
        for name in RegionNames:
            if name in okami_events:
                for (event_name, event_data) in okami_events[name].items():
                    precollected_item_event_state = resolve_option_callable(event_data.precollected, self)

                    if precollected_item_event_state:
                        # With the current options this event is unlocked at the start, so we create a precollected item
                        # Classification probably doesn't matter much for precollected items I'd guess
                        self.push_precollected(
                            create_item(event_name, event_data.id, ItemClassification.progression, self))
                    # If it's precollected, no need to add it to the itempool
                    else:
                        is_event_item_state = resolve_option_callable(event_data.is_event_item, self)

                        if is_event_item_state:
                            # With the current options this event becomes its own item, so we need to add it to the item pool
                            itempool += [create_standard_item(self, event_data.event_item_name)]

        for name in item_table.keys():
            item_type: ItemClassification = item_table.get(name).classification
            item_count: int = resolve_option_callable(item_table.get(name).count_in_pool, self)
            # If the item is locally randomized we have to put one less
            if name in self.get_local_items_name():
                item_count -= 1
            if item_type != ItemClassification.filler and item_count > 0:
                itempool += create_multiple_items(self, name, item_count, item_type)
        # Create a number of junk items equal to the locations remaining, minus items that have a fixed count in the item pool, and the locally placed ones.
        junk_fill_count = get_unfilled_locations_count(self) - len(itempool) - len(self.get_local_items_name())
        itempool += create_junk_items(self, junk_fill_count)

        for pi in precollected_items:
            self.push_precollected(pi)
        return itempool

    def get_valid_local_item_locations(self, local_item_data: LocalItem) -> \
            List[Location]:
        list = []
        for r in local_item_data.allowed_regions:
            # Check we don't try to place this on a region that doesn't exist.
            if r in okami_locations.keys():
                for loc_name, loc_data in okami_locations[r].items():
                    # Check this isn't a location we've excluded or that we have already prefilled
                    if loc_name not in local_item_data.exclude_locations and resolve_option_callable(
                            loc_data.progress_type, self) != LocationProgressType.EXCLUDED:
                        # If this is a biteable item, exclude places that place it directly in your inventory
                        if not local_item_data.is_biteable or loc_data.type not in excluded_biteable_location_types:
                            list.append(self.get_location(loc_name))
            # Second loop for shops, only if the item is not biteable
            if not local_item_data.is_biteable and r in okami_shop_locations.keys():
                for shop_loc_name in okami_locations[r].keys():
                    list.append(self.get_location(shop_loc_name))

        return list

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
            "Satomi Power Orb (Rei)",
            "Satomi Power Orb (Shin)",
            "Satomi Power Orb (Chi)",
            "Satomi Power Orb (Ko)",
            "Satomi Power Orb (Tei)",
            "Satomi Power Orb (Loyalty)",
            "Satomi Power Orb (Justice)",
            "Satomi Power Orb (Duty)"
        ],

        "soup_ingredients": [
            "Ogre Liver",
            "Ice Lips",
            "Fire Eye",
            "Black Demon Horn"
        ]
    }
