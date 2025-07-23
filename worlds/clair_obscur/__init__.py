import typing
from typing import List, Mapping, Any

from BaseClasses import Tutorial, Group, CollectionState
from worlds.AutoWorld import WebWorld, World
from worlds.clair_obscur.Data import data
from worlds.clair_obscur.Items import create_item_name_to_ap_id, ClairObscurItem, get_classification, offset_item_value
from worlds.clair_obscur.Locations import create_location_name_to_ap_id, create_locations
from worlds.clair_obscur.Options import OPTIONS_GROUP, ClairObscurOptions


class WebClairObscur(WebWorld):
    """
    Webhost for Clair Obscur Expedition 33.
    """

    theme = "stone"

    setup = Tutorial(
        "Multiworld Setup Guide",
        "Setup guide for Clair Obscur Expedition 33.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Démorck"]
    )

    tutorials = [setup]
    option_groups = OPTIONS_GROUP

class ClairObscurSettings(Group):
    """
    No idea
    """

class ClairObscurWorld(World):
    game = "Clair Obscur Expedition 33"
    web = WebClairObscur()
    topology_present = True

    item_pool: typing.List[ClairObscurItem]

    options_dataclass = ClairObscurOptions
    options = ClairObscurOptions

    allow_surplus_items = True

    item_name_to_id = create_item_name_to_ap_id()
    location_name_to_id = create_location_name_to_ap_id()

    required_client_version = (0, 5, 4)

    settings: typing.ClassVar[ClairObscurSettings]


    def create_items(self) -> None:
        self.item_pool = []
        for item_id, item_data in data.items.items():
            item = self.create_item_by_id(item_id)
            self.item_pool.append(item)

        #Add 4 more Progressive Rocks
        for i in range(0, 4):
            #item = self.create_item("Progressive Rock")
            # ^ This ends up adding the offset twice. For now, I'm hardcoding in the ID as with the filler items above.
            item = self.create_item_by_id(14)
            self.item_pool.append(item)

        #Add filler to match the amount of locations
        location_count = len(data.locations)
        remaining_items_to_generate = location_count - len(self.item_pool) + 1
        for i in range(0, remaining_items_to_generate):
            item = self.create_item_by_id(2)
            self.item_pool.append(item)
        self.multiworld.itempool += self.item_pool

    def fill_slot_data(self) -> typing.Dict[str, Any]:
        return self.options.as_dict(
            "goal"
        )

    def create_item(self, name: str) -> ClairObscurItem:
        return self.create_item_by_id(self.item_name_to_id[name])


    def create_item_by_id(self, ap_id: int) -> ClairObscurItem:
        real_ap_id = offset_item_value(ap_id)

        return ClairObscurItem(
            self.item_id_to_name[real_ap_id],
            get_classification(real_ap_id),
            real_ap_id,
            self.player
        )

    def get_pre_fill_items(self) -> List[ClairObscurItem]:
        return [self.create_item(self.get_filler_item_name())]

    def get_filler_item_name(self) -> str:
        return "UpgradeMaterial_Level3"

    def create_regions(self) -> None:
        from .Regions import create_regions
        from .Locations import create_locations

        regions = create_regions(self)

        create_locations(self, regions)

        # self.multiworld.completion_condition[self.player] = (lambda state: state.has("Progressive Rock", self.player, 4)
        #                                                      and state.has("Barrier Breaker", self.player))

        self.multiworld.completion_condition[self.player] = (lambda state: state.can_reach_location("Chest_Lumiere_17", self.player))

