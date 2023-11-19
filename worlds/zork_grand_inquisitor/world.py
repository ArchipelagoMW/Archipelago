from BaseClasses import Item, ItemClassification, Location, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .data.item_data import item_data
from .data.location_data import location_data
from .data.region_data import region_data

from .data_funcs import (
    item_names_to_id,
    location_names_to_id,
    item_groups,
    location_groups,
    locations_by_region,
    location_access_rule_for,
    entrance_access_rule_for,
)

from .enums import ZorkGrandInquisitorEvents, ZorkGrandInquisitorItems, ZorkGrandInquisitorTags

from .options import ZorkGrandInquisitorOptions


class ZorkGrandInquisitorWebWorld(WebWorld):
    theme = "stone"

    tutorials = [
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

    topology_present = True

    item_name_to_id = item_names_to_id()
    location_name_to_id = location_names_to_id()

    item_name_groups = item_groups()
    location_name_groups = location_groups()

    required_client_version = (0, 4, 3)  # Technically 0.4.4 but server still reports 0.4.3

    web = ZorkGrandInquisitorWebWorld()

    def create_regions(self):
        region_mapping = dict()

        for region in region_data.keys():
            region_mapping[region] = Region(region.value, self.player, self.multiworld)

        region_locations_mapping = locations_by_region(
            include_deathsanity=self.options.deathsanity.value == 1
        )

        for region_enum_item, region in region_mapping.items():
            regions_locations = region_locations_mapping[region_enum_item]

            # Locations
            for location_enum_item in regions_locations:
                data = location_data[location_enum_item]

                location = ZorkGrandInquisitorLocation(
                    self.player,
                    location_enum_item.value,
                    data.archipelago_id,
                    region_mapping[data.region],
                )

                location.event = type(location_enum_item) == ZorkGrandInquisitorEvents

                if location.event:
                    location.place_locked_item(
                        ZorkGrandInquisitorItem(
                            data.event_item_name,
                            ItemClassification.progression,
                            None,
                            self.player,
                        )
                    )

                location.access_rule = eval(location_access_rule_for(location_enum_item, self.player))

                region.locations.append(location)

            # Connections
            for region_exit in region_data[region_enum_item].exits or tuple():
                region.connect(
                    region_mapping[region_exit],
                    rule=eval(entrance_access_rule_for(region_enum_item, region_exit, self.player)),
                )

            self.multiworld.regions.append(region)

    def create_items(self):
        item_pool = list()

        for item, data in item_data.items():
            if ZorkGrandInquisitorTags.FILLER in (data.tags or tuple()):
                continue

            item_pool.append(
                ZorkGrandInquisitorItem(
                    item.value,
                    data.classification,
                    data.archipelago_id,
                    self.player,
                )
            )

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        for _ in range(total_locations - len(item_pool)):
            filler_item_name = self.get_filler_item_name()

            item_pool.append(
                ZorkGrandInquisitorItem(
                    filler_item_name,
                    ItemClassification.filler,
                    self.item_name_to_id[filler_item_name],
                    self.player,
                )
            )

        self.multiworld.itempool += item_pool

        if self.options.early_rope_and_lantern.value == 1:
            self.multiworld.early_items[self.player][ZorkGrandInquisitorItems.ROPE.value] = 1
            self.multiworld.early_items[self.player][ZorkGrandInquisitorItems.LANTERN.value] = 1

    def generate_basic(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def fill_slot_data(self):
        return self.options.as_dict(
            "early_rope_and_lantern",
            "skip_old_scratch_minigame",
            "deathsanity",
        )

    def get_filler_item_name(self):
        return self.multiworld.random.choice(list(self.item_name_groups["Filler"]))


class ZorkGrandInquisitorItem(Item):
    game = "Zork Grand Inquisitor"


class ZorkGrandInquisitorLocation(Location):
    game = "Zork Grand Inquisitor"
