import typing, settings
from math import ceil
from typing import List, Any, Dict

from BaseClasses import Tutorial, Group, CollectionState
from worlds.AutoWorld import WebWorld, World
from worlds.clair_obscur.Data import data
from worlds.clair_obscur.Items import create_item_name_to_ap_id, ClairObscurItem, get_classification, offset_item_value, \
    create_item_groups
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

class ClairObscurSettings(settings.Group):
    """
    No idea
    """

class ClairObscurWorld(World):
    game = "Clair Obscur Expedition 33"
    web = WebClairObscur()
    topology_present = True

    item_pool: typing.List[ClairObscurItem]

    options_dataclass = ClairObscurOptions
    options: ClairObscurOptions

    allow_surplus_items = True

    item_name_to_id = create_item_name_to_ap_id()
    location_name_to_id = create_location_name_to_ap_id()

    item_name_groups = create_item_groups(data.items)

    required_client_version = (0, 5, 4)

    settings: typing.ClassVar[ClairObscurSettings]

    def convert_pictos(self, pictos_level: int) -> int:
        #Converts the connection destination's pictos level into an amount of pictos required to reach that level with
        #scale-by-order-received.
        return ceil((pictos_level - 1) * 5.8)

    def create_items(self) -> None:

        #Amounts of each item to generate (anything else will be added once). Progressive Rock and quest items
        #shouldn't change; other items can be adjusted based on options once options are implemented
        amounts = {
            "Progressive Rock": 5,
            "Rock Crystal": 3,
            "Lost Gestral": 9,
            "Shape of Health": 2,
            "Shape of Life": 2,
            "Shape of Energy": 2,
            "Healing Tint Shard": 10,
            "Energy Tint Shard": 10,
            "Revive Tint Shard": 10,

            #Only 10 are possible to get in a normal playthrough
            "Perfect Chroma Catalyst": 10
        }

        self.item_pool = []

        excluded_types = ["Journal", "Character"]
        excluded_names = []
        if not self.options.gestral_shuffle: excluded_names.append("Lost Gestral")
        if not self.options.shuffle_free_aim: excluded_names.append("Free Aim")

        for item_id, item_data in data.items.items():
            amount = 1

            if item_data.type in excluded_types or item_data.name in excluded_names:
                continue
            if item_data.name in amounts:
                amount = amounts[item_data.name]
            for i in range(0, amount):
                item = self.create_item_by_id(item_id)
                self.item_pool.append(item)

        if self.options.char_shuffle:
            #Create items for characters if character shuffle is on.
            chars = ["Gustave", "Maelle", "Lune", "Sciel", "Monoco", "Verso"]
            starting_char = self.options.starting_char.current_option_name
            for char in chars:
                char_item = self.create_item(char)
                if char == starting_char:
                    self.push_precollected(char_item)
                else:
                    self.item_pool.append(char_item)

        #Add filler to match the amount of locations
        remaining_items_to_generate = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.item_pool)

        filler_amounts = {
            "Chroma Catalyst (5)": 1,
            "Polished Chroma Catalyst (5)": 2,
            "Resplendent Chroma Catalyst (5)": 3,
            "Grandiose Chroma Catalyst (5)": 4,
            "Colour of Lumina (5)": 10
        }

        filler_item_sequence: List[str] = []
        for item, amount in filler_amounts.items():
            filler_item_sequence += [item] * amount

        sequence_length = len(filler_item_sequence)
        for i in range(0, remaining_items_to_generate):
            item_name = filler_item_sequence[i % sequence_length]
            self.item_pool.append(self.create_item(item_name))

        self.multiworld.itempool += self.item_pool

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {}
        slot_data["options"] = self.options.as_dict(
            "goal", "char_shuffle", "starting_char", "gestral_shuffle", "gear_scaling", "shuffle_free_aim",
            "exclude_endgame_locations", "exclude_endless_tower"
        )

        slot_data["totals"]: Dict[str, int] = {}
        slot_data["totals"]["pictos"] = len(self.item_name_groups["Picto"])
        slot_data["totals"]["weapons"] = len(self.item_name_groups["Weapon"])

        match self.options.gear_scaling:
            case 0:
                #Scale by sphere placement
                slot_data["pictos"]: List[int] = []
                slot_data["weapons"]: List[int] = []
                spheres = self.multiworld.get_spheres()
                for sphere in spheres:
                    for loc in sphere:
                        if loc.item.name in self.item_name_groups["Picto"]:
                            slot_data["pictos"].append(loc.item.code)
                        elif loc.item.name in self.item_name_groups["Weapon"]:
                            slot_data["weapons"].append(loc.item.code)
            case 1:
                # Scale by order received (handled entirely by client)
                return slot_data
            case 2:
                #Random scaling
                slot_data["pictos"]: List[int] = []
                slot_data["weapons"]: List[int] = []
                for picto in self.item_name_groups["Picto"]:
                    slot_data["pictos"].append(self.item_name_to_id[picto])
                for weapon in self.item_name_groups["Weapon"]:
                    slot_data["weapons"].append(self.item_name_to_id[weapon])
                self.random.shuffle(slot_data["pictos"])
                self.random.shuffle(slot_data["weapons"])
            case 3:
                #Full random scaling (handled entirely by client)
                return slot_data

        return slot_data



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
        return "Colour of Lumina (5)"

    def create_regions(self) -> None:
        from .Regions import create_regions, connect_regions
        from .Locations import create_locations

        regions = create_regions(self)
        connect_regions(self)
        create_locations(self, regions)

    def set_rules(self):
        set_rules(self)

