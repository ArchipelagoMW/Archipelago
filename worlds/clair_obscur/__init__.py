import typing
from typing import List, Mapping, Any

from BaseClasses import Tutorial, Group, CollectionState
from worlds.AutoWorld import WebWorld, World
from worlds.clair_obscur.Data import data
from worlds.clair_obscur.Items import create_item_name_to_ap_id, ClairObscurItem, get_classification, offset_item_value
from worlds.clair_obscur.Locations import create_location_name_to_ap_id, create_locations
from worlds.clair_obscur.Options import OPTIONS_GROUP, ClairObscurOptions
from worlds.clair_obscur.Const import BASE_OFFSET
from worlds.clair_obscur.Rules import set_rules

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
    #me either but i'll get there

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

    # item_name_groups = {
    #
    # }

    required_client_version = (0, 5, 4)

    settings: typing.ClassVar[ClairObscurSettings]


    def create_items(self) -> None:

        #Amounts of each item to generate (anything else will be added once). Progressive Rock and quest items
        #shouldn't change; other items can be adjusted based on options once options are implemented
        amounts = {
            "Progressive Rock": 5,
            "Rock Crystal": 3,
            "Lost Gestral": 9,
            "Chroma Catalyst": 10,
            "Polished Chroma Catalyst": 30,
            "Resplendent Chroma Catalyst": 40,
            "Grandiose Chroma Catalyst": 30,
            "Shape of Health": 2,
            "Shape of Life": 2,
            "Shape of Energy": 2,

            #Only 10 are possible to get in a normal playthrough
            "Perfect Chroma Catalyst": 10
        }

        self.item_pool = []

        #TODO- Populate this from options
        excluded = ["Journal"]

        for item_id, item_data in data.items.items():
            amount = 1


            if item_data.type in excluded:
                continue
            if item_data.name in amounts:
                amount = amounts[item_data.name]
            for i in range(0, amount):
                item = self.create_item_by_id(item_id)
                self.item_pool.append(item)

        #Add filler to match the amount of locations


        location_count = len(data.locations)

        remaining_items_to_generate = location_count - len(self.item_pool)

        #TODO- proper filler generation. Add proportional amounts of upgrade mats to an array i.e. Polished, Polished,
        #Polished, Polished 3-pack - and modulo iterate through them

        #filler_item_sequence = []
        # for i in range(0, remaining_items_to_generate):
            #i modulo filler_item_sequence length

        for i in range(0, remaining_items_to_generate):
            item = self.create_item("Resplendent Chroma Catalyst")
            self.item_pool.append(item)
        self.multiworld.itempool += self.item_pool

    def fill_slot_data(self) -> typing.Dict[str, Any]:
        return self.options.as_dict(
            "goal"
        )

    def create_item(self, name: str) -> ClairObscurItem:
        return self.create_item_by_id(self.item_name_to_id[name])


    def create_item_by_id(self, ap_id: int) -> ClairObscurItem:
        if ap_id < BASE_OFFSET:
            #Should only offset the ID if it hasn't been already; calling create_item on an already created item
            #by name would otherwise offset twice
            ap_id = offset_item_value(ap_id)

        return ClairObscurItem(
            self.item_id_to_name[ap_id],
            get_classification(ap_id),
            ap_id,
            self.player
        )

    def get_pre_fill_items(self) -> List[ClairObscurItem]:
        return [self.create_item(self.get_filler_item_name())]

    def get_filler_item_name(self) -> str:
        return "Resplendent Chroma Catalyst"

    def create_regions(self) -> None:
        from .Regions import create_regions, connect_regions
        from .Locations import create_locations

        regions = create_regions(self)
        connect_regions(self)
        create_locations(self, regions)

    def set_rules(self):
        set_rules(self)

