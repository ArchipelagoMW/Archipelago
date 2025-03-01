from typing import Any, Dict, List, Tuple

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
    items_with_tag,
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

    item_name_to_id = item_names_to_id()
    location_name_to_id = location_names_to_id()

    item_name_groups = item_groups()
    location_name_groups = location_groups()

    required_client_version: Tuple[int, int, int] = (0, 4, 4)

    web = ZorkGrandInquisitorWebWorld()

    filler_item_names: List[str] = item_groups()["Filler"]
    item_name_to_item: Dict[str, ZorkGrandInquisitorItems] = item_names_to_item()

    def create_regions(self) -> None:
        deathsanity: bool = bool(self.options.deathsanity)

        region_mapping: Dict[ZorkGrandInquisitorRegions, Region] = dict()

        region_enum_item: ZorkGrandInquisitorRegions
        for region_enum_item in region_data.keys():
            region_mapping[region_enum_item] = Region(region_enum_item.value, self.player, self.multiworld)

        region_locations_mapping: Dict[ZorkGrandInquisitorRegions, List[ZorkGrandInquisitorLocations]]
        region_locations_mapping = locations_by_region(include_deathsanity=deathsanity)

        region_enum_item: ZorkGrandInquisitorRegions
        region: Region
        for region_enum_item, region in region_mapping.items():
            regions_locations: List[ZorkGrandInquisitorLocations] = region_locations_mapping[region_enum_item]

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

                if isinstance(location_enum_item, ZorkGrandInquisitorEvents):
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
        quick_port_foozle: bool = bool(self.options.quick_port_foozle)
        start_with_hotspot_items: bool = bool(self.options.start_with_hotspot_items)

        item_pool: List[ZorkGrandInquisitorItem] = list()

        item: ZorkGrandInquisitorItems
        data: ZorkGrandInquisitorItemData
        for item, data in item_data.items():
            tags: Tuple[ZorkGrandInquisitorTags, ...] = data.tags or tuple()

            if ZorkGrandInquisitorTags.FILLER in tags:
                continue
            elif ZorkGrandInquisitorTags.HOTSPOT in tags and start_with_hotspot_items:
                continue

            item_pool.append(self.create_item(item.value))

        total_locations: int = len(self.multiworld.get_unfilled_locations(self.player))
        item_pool += [self.create_filler() for _ in range(total_locations - len(item_pool))]

        self.multiworld.itempool += item_pool

        if quick_port_foozle:
            self.multiworld.early_items[self.player][ZorkGrandInquisitorItems.ROPE.value] = 1
            self.multiworld.early_items[self.player][ZorkGrandInquisitorItems.LANTERN.value] = 1

            if not start_with_hotspot_items:
                self.multiworld.early_items[self.player][ZorkGrandInquisitorItems.HOTSPOT_WELL.value] = 1
                self.multiworld.early_items[self.player][ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR.value] = 1

                self.multiworld.early_items[self.player][
                    ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL.value
                ] = 1

        if start_with_hotspot_items:
            item: ZorkGrandInquisitorItems
            for item in sorted(items_with_tag(ZorkGrandInquisitorTags.HOTSPOT), key=lambda item: item.name):
                self.multiworld.push_precollected(self.create_item(item.value))

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
            "quick_port_foozle",
            "start_with_hotspot_items",
            "deathsanity",
            "grant_missable_location_checks",
        )

    def get_filler_item_name(self) -> str:
        return self.random.choice(self.filler_item_names)
