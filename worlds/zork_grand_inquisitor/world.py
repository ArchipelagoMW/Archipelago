from typing import Any, Dict, List, Set, Tuple

from BaseClasses import Item, ItemClassification, Location, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .data.item_data import item_data, ZorkGrandInquisitorItemData
from .data.location_data import location_data, ZorkGrandInquisitorLocationData
from .data.region_data import region_data

from .data_funcs import (
    item_names_to_id,
    item_names_to_item,
    location_names_to_id,
    item_groups,
    location_groups,
    locations_by_region,
    location_access_rule_for,
    entrance_access_rule_for,
)

from .enums import (
    ZorkGrandInquisitorEvents,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorRegions,
    ZorkGrandInquisitorTags,
)

from .options import ZorkGrandInquisitorOptions


class ZorkGrandInquisitorItem(Item):
    game = "Zork Grand Inquisitor"


class ZorkGrandInquisitorLocation(Location):
    game = "Zork Grand Inquisitor"


class ZorkGrandInquisitorWebWorld(WebWorld):
    theme: str = "stone"

    tutorials: List[Tutorial] = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Zork Grand Inquisitor randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Serpent.AI"],
        )
    ]


class ZorkGrandInquisitorWorld(World):
    """
    Zork: Grand Inquisitor is a 1997 point-and-click adventure game for PC.
    Magic has been banned from the great Underground Empire of Zork. By edict of the Grand Inquisitor Mir Yannick, the
    Empire has been sealed off and the practice of mystic arts declared punishable by "Totemization" (a very bad thing).
    The only way to restore magic to the kingdom is to find three hidden artifacts: The Coconut of Quendor, The Cube of
    Foundation, and The Skull of Yoruk.
    """

    options_dataclass = ZorkGrandInquisitorOptions
    options: ZorkGrandInquisitorOptions

    game = "Zork Grand Inquisitor"

    topology_present = False

    item_name_to_id = item_names_to_id()
    location_name_to_id = location_names_to_id()

    item_name_groups = item_groups()
    location_name_groups = location_groups()

    required_client_version: Tuple[int, int, int] = (0, 4, 4)

    web = ZorkGrandInquisitorWebWorld()

    item_name_to_item: Dict[str, ZorkGrandInquisitorItems] = item_names_to_item()

    def create_regions(self) -> None:
        region_mapping: Dict[ZorkGrandInquisitorRegions, Region] = dict()

        region_enum_item: ZorkGrandInquisitorRegions
        for region_enum_item in region_data.keys():
            region_mapping[region_enum_item] = Region(region_enum_item.value, self.player, self.multiworld)

        region_locations_mapping: Dict[ZorkGrandInquisitorRegions, Set[ZorkGrandInquisitorLocations]]
        region_locations_mapping = locations_by_region(include_deathsanity=self.options.deathsanity.value == 1)

        region_enum_item: ZorkGrandInquisitorRegions
        region: Region
        for region_enum_item, region in region_mapping.items():
            regions_locations: Set[ZorkGrandInquisitorLocations] = region_locations_mapping[region_enum_item]

            # Locations
            location_enum_item: ZorkGrandInquisitorLocations
            for location_enum_item in regions_locations:
                data: ZorkGrandInquisitorLocationData = location_data[location_enum_item]

                location: ZorkGrandInquisitorLocation = ZorkGrandInquisitorLocation(
                    self.player,
                    location_enum_item.value,
                    data.archipelago_id,
                    region_mapping[data.region],
                )

                location.event = isinstance(location_enum_item, ZorkGrandInquisitorEvents)

                if location.event:
                    location.place_locked_item(
                        ZorkGrandInquisitorItem(
                            data.event_item_name,
                            ItemClassification.progression,
                            None,
                            self.player,
                        )
                    )

                location_access_rule: str = location_access_rule_for(location_enum_item, self.player)

                if location_access_rule != "lambda state: True":
                    location.access_rule = eval(location_access_rule)

                region.locations.append(location)

            # Connections
            region_exit: ZorkGrandInquisitorRegions
            for region_exit in region_data[region_enum_item].exits or tuple():
                entrance_access_rule: str = entrance_access_rule_for(region_enum_item, region_exit, self.player)

                if entrance_access_rule == "lambda state: True":
                    region.connect(region_mapping[region_exit])
                else:
                    region.connect(region_mapping[region_exit], rule=eval(entrance_access_rule))

            self.multiworld.regions.append(region)

    def create_items(self) -> None:
        item_pool: List[ZorkGrandInquisitorItem] = list()

        item: ZorkGrandInquisitorItems
        data: ZorkGrandInquisitorItemData
        for item, data in item_data.items():
            if ZorkGrandInquisitorTags.FILLER in (data.tags or tuple()):
                continue

            item_pool.append(self.create_item(item.value))

        total_locations: int = len(self.multiworld.get_unfilled_locations(self.player))

        for _ in range(total_locations - len(item_pool)):
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool

        if self.options.early_rope_and_lantern.value == 1:
            self.multiworld.early_items[self.player][ZorkGrandInquisitorItems.ROPE.value] = 1
            self.multiworld.early_items[self.player][ZorkGrandInquisitorItems.LANTERN.value] = 1

    def create_item(self, name: str) -> ZorkGrandInquisitorItem:
        data: ZorkGrandInquisitorItemData = item_data[self.item_name_to_item[name]]

        return ZorkGrandInquisitorItem(
            name,
            data.classification,
            data.archipelago_id,
            self.player,
        )

    def generate_basic(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict(
            "goal",
            "early_rope_and_lantern",
            "deathsanity",
        )

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(list(self.item_name_groups["Filler"]))
