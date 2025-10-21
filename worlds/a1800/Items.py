# import logging

from dataclasses import dataclass
from typing import ClassVar, TYPE_CHECKING, Optional
from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import A1800World


services: list[str] = ["Market", "Pub", "Church", "School"]
institutions: list[str] = ["OW Fire Station", "OW Police Station"]
products: list[str] = [
    "Wood", "Timber", "Fish", "Wool", "Work Clothes", "Potatoes", "Schnapps", "Clay", "Bricks", "Pigs", "Sausages",
    "Grain", "Flour", "Bread", "Sails", "Coal", "Iron", "Steel", "Steel Beams", "Tallow", "Soap", "Weapons", "Hops",
    "Malt", "Beer"
]
workforces: list[str] = ["Farmers", "Workers", "Artisans"]


def get_event_item_name(raw_name: str) -> str:
    if raw_name in products:
        return f"Product: {raw_name}"
    elif raw_name in services:
        return f"Service: {raw_name}"
    elif raw_name in institutions:
        return f"Institution: {raw_name}"
    elif raw_name in workforces:
        return f"Workforce: {raw_name}"
    else:
        return raw_name


@dataclass
class A1800ItemData:
    __item_id: ClassVar[int] = 1
    name: str
    classification: ItemClassification
    anno_GUIDs: list[int] = []
    ap_code: Optional[int] = None
    is_event: Optional[bool] = False
    event_locations: list[str] = []

    def __post_init__(self) -> None:
        if not self.ap_code and not self.is_event:
            self.ap_code = A1800ItemData.__item_id
            A1800ItemData.__item_id += 1

        if self.is_event:
            self.name = get_event_item_name(self.name)
        else:
            self.name = f"Unlock: {self.name}"


class A1800Item(Item):
    game: str = "Anno 1800"
    data: A1800ItemData

    def __init__(self, player: int, data: A1800ItemData):
        super().__init__(data.name, data.classification, None if data.is_event else data.ap_code, player)
        self.data = data


def create_itempool(world: "A1800World") -> list[Item]:
    itempool: list[Item] = []

    for data in _item_list:
        item = create_item(world, data)

        if data.is_event:
            for location_name in data.event_locations:
                location = world.multiworld.get_location(location_name, world.player)
                location.place_locked_item(item)
        else:
            itempool.append(item)

    return itempool


def create_item(world: "A1800World", item: str | A1800ItemData) -> Item:
    if isinstance(item, A1800ItemData):
        data = item
    else:
        data = item_dict[item]
    return A1800Item(world.player, data)


def create_and_push_starting_items(world: "A1800World") -> None:
    for item in _starting_items:
        world.multiworld.push_precollected(create_item(world, item))


_starting_items: list[A1800ItemData] = [
    A1800ItemData("OW: Small Trading Post", ItemClassification.progression, anno_GUIDs=[1010517]),
    A1800ItemData("OW: Dirt Road", ItemClassification.progression, anno_GUIDs=[1000178]),
    A1800ItemData("OW: Marketplace", ItemClassification.progression, anno_GUIDs=[1010372, 120020]),
    A1800ItemData("OW: Farmer Residence", ItemClassification.progression, anno_GUIDs=[1010343]),
    A1800ItemData("OW: Small Warehouse", ItemClassification.progression, anno_GUIDs=[1010371]),
    A1800ItemData("OW: Lumberjack's Hut", ItemClassification.progression, anno_GUIDs=[1010266, 120008, 500091]),
    A1800ItemData("OW: Sawmill", ItemClassification.progression, anno_GUIDs=[100451, 1010196, 500091]),
]

_anno_1800_unlock_items: list[A1800ItemData] = [
    A1800ItemData("OW: Fishery", ItemClassification.progression, anno_GUIDs=[1010278, 1010200]),
    A1800ItemData("OW: Sheep Farm", ItemClassification.progression, anno_GUIDs=[1010267, 1010197, 500505]),
    A1800ItemData("OW: Framework Knitters", ItemClassification.progression, anno_GUIDs=[1010315, 1010237, 500505]),
    A1800ItemData("OW: Potato Farm", ItemClassification.filler, anno_GUIDs=[1010265, 1010195, 500002]),
    A1800ItemData("OW: Schnapps Distillery", ItemClassification.filler, anno_GUIDs=[1010294, 1010216, 500002]),
    A1800ItemData("OW: Worker Residence", ItemClassification.progression, anno_GUIDs=[1010344]),
    A1800ItemData("OW: Fire Station", ItemClassification.filler, anno_GUIDs=[1010463]),
    A1800ItemData("OW: Pub", ItemClassification.filler, anno_GUIDs=[1010358, 1010358]),
    A1800ItemData("OW: Paved Street", ItemClassification.filler, anno_GUIDs=[1010035]),
    A1800ItemData("OW: Clay Pit", ItemClassification.progression, anno_GUIDs=[100416, 1010201, 500024]),
    A1800ItemData("OW: Brick Factory", ItemClassification.progression, anno_GUIDs=[1010283, 1010205, 500024]),
    A1800ItemData("OW: Pig Farm", ItemClassification.progression, anno_GUIDs=[1010269, 1010199, 25000244]),
    A1800ItemData("OW: Slaughterhouse", ItemClassification.progression, anno_GUIDs=[1010316, 1010238, 25000244]),
    A1800ItemData("OW: Medium Warehouse", ItemClassification.filler, anno_GUIDs=[100516]),
    A1800ItemData("OW: Medium Trading Post", ItemClassification.filler, anno_GUIDs=[100510]),
    A1800ItemData("OW: Trade Union", ItemClassification.filler, anno_GUIDs=[1010516]),
    A1800ItemData("OW: Grain Farm", ItemClassification.progression, anno_GUIDs=[1010262, 1010192, 500004]),
    A1800ItemData("OW: Flour Mill", ItemClassification.progression, anno_GUIDs=[1010313, 1010235, 500004]),
    A1800ItemData("OW: Bakery", ItemClassification.progression, anno_GUIDs=[1010291, 1010213, 500004]),
    A1800ItemData("OW: Church", ItemClassification.filler, anno_GUIDs=[1010359, 1010350]),
    A1800ItemData("OW: Sailmakers", ItemClassification.progression, anno_GUIDs=[1010288, 1010288, 500009]),
    A1800ItemData("OW: Sailing Shipyard", ItemClassification.progression, anno_GUIDs=[1010520]),
    A1800ItemData("OW: Mounted Guns", ItemClassification.filler, anno_GUIDs=[1010522]),
    A1800ItemData("OW: Quay", ItemClassification.filler, anno_GUIDs=[1010567]),
    A1800ItemData("OW: Depot", ItemClassification.filler, anno_GUIDs=[1010519]),
    A1800ItemData("OW: Harbourmaster's Office", ItemClassification.filler, anno_GUIDs=[100586]),
    A1800ItemData("OW: Charcoal Kiln", ItemClassification.progression, anno_GUIDs=[1010298, 1010226, 500005]),
    A1800ItemData("OW: Iron Mine", ItemClassification.progression, anno_GUIDs=[1010305, 1010227, 500005]),
    A1800ItemData("OW: Furnace", ItemClassification.progression, anno_GUIDs=[1010297, 1010219, 500005]),
    A1800ItemData("OW: Steelworks", ItemClassification.progression, anno_GUIDs=[1010296, 1010218, 500005]),
    A1800ItemData("OW: Rendering Works", ItemClassification.progression, anno_GUIDs=[1010312, 1010234, 25000220]),
    A1800ItemData("OW: Soap Factory", ItemClassification.progression, anno_GUIDs=[1010281, 1010203, 25000220]),
    A1800ItemData("OW: Weapon Factory", ItemClassification.filler, anno_GUIDs=[1010299, 1010221, 500145]),
    A1800ItemData("OW: Cannon Tower", ItemClassification.filler, anno_GUIDs=[1010523]),
    A1800ItemData("OW: Hop Farm", ItemClassification.filler, anno_GUIDs=[1010264, 1010194, 500006]),
    A1800ItemData("OW: Malthouse", ItemClassification.filler, anno_GUIDs=[1010314, 1010236, 500006]),
    A1800ItemData("OW: Brewery", ItemClassification.filler, anno_GUIDs=[1010292, 1010214, 500006]),
    A1800ItemData("OW: Police Station", ItemClassification.filler, anno_GUIDs=[1010462]),
    A1800ItemData("OW: School", ItemClassification.progression, anno_GUIDs=[1010360, 1010351]),
    A1800ItemData("OW: Artisan Residence", ItemClassification.progression, anno_GUIDs=[1010345]),
]

_anno_1800_event_items: list[A1800ItemData] = [
    A1800ItemData("Market", ItemClassification.progression, is_event=True, event_locations=["OW: Marketplace"]),
    A1800ItemData("Farmers", ItemClassification.progression, is_event=True, event_locations=["OW: Farmer Residence"]),
    A1800ItemData("Wood", ItemClassification.progression, is_event=True, event_locations=["OW: Lumberjack's Hut"]),
    A1800ItemData("Timber", ItemClassification.progression, is_event=True, event_locations=["OW: Sawmill"]),
    A1800ItemData("Fish", ItemClassification.progression, is_event=True, event_locations=["OW: Fishery"]),
    A1800ItemData("Wool", ItemClassification.progression, is_event=True, event_locations=["OW: Sheep Farm"]),
    A1800ItemData("Work Clothes", ItemClassification.progression,
                  is_event=True, event_locations=["OW: Framework Knitters"]),
    A1800ItemData("Potatoes", ItemClassification.filler, is_event=True, event_locations=["OW: Potato Farm"]),
    A1800ItemData("Schnapps", ItemClassification.filler, is_event=True, event_locations=["OW: Schnapps Distillery"]),
    A1800ItemData("Workers", ItemClassification.progression, is_event=True, event_locations=["OW: Worker Residence"]),
    A1800ItemData("OW Fire Station", ItemClassification.filler, is_event=True, event_locations=["OW: Fire Station"]),
    A1800ItemData("Pub", ItemClassification.filler, is_event=True, event_locations=["OW: Pub"]),
    A1800ItemData("Clay", ItemClassification.progression, is_event=True, event_locations=["OW: Clay Pit"]),
    A1800ItemData("Bricks", ItemClassification.progression, is_event=True, event_locations=["OW: Brick Factory"]),
    A1800ItemData("Pigs", ItemClassification.progression, is_event=True, event_locations=["OW: Pig Farm"]),
    A1800ItemData("Sausages", ItemClassification.progression, is_event=True, event_locations=["OW: Slaughterhouse"]),
    A1800ItemData("Grain", ItemClassification.progression, is_event=True, event_locations=["OW: Grain Farm"]),
    A1800ItemData("Flour", ItemClassification.progression, is_event=True, event_locations=["OW: Flour Mill"]),
    A1800ItemData("Bread", ItemClassification.progression, is_event=True, event_locations=["OW: Bakery"]),
    A1800ItemData("Church", ItemClassification.filler, is_event=True, event_locations=["OW: Church"]),
    A1800ItemData("Sails", ItemClassification.progression, is_event=True, event_locations=["OW: Sailmakers"]),
    A1800ItemData("Ships", ItemClassification.progression, is_event=True, event_locations=["OW: Sailing Shipyard"]),
    A1800ItemData("Coal", ItemClassification.progression, is_event=True, event_locations=["OW: Charcoal Kiln"]),
    A1800ItemData("Iron", ItemClassification.progression, is_event=True, event_locations=["OW: Iron Mine"]),
    A1800ItemData("Steel", ItemClassification.progression, is_event=True, event_locations=["OW: Furnace"]),
    A1800ItemData("Steel Beams", ItemClassification.progression, is_event=True, event_locations=["OW: Steelworks"]),
    A1800ItemData("Tallow", ItemClassification.progression, is_event=True, event_locations=["OW: Rendering Works"]),
    A1800ItemData("Soap", ItemClassification.progression, is_event=True, event_locations=["OW: Soap Factory"]),
    A1800ItemData("Weapons", ItemClassification.filler, is_event=True, event_locations=["OW: Weapon Factory"]),
    A1800ItemData("Hops", ItemClassification.filler, is_event=True, event_locations=["OW: Hop Farm"]),
    A1800ItemData("Malt", ItemClassification.filler, is_event=True, event_locations=["OW: Malthouse"]),
    A1800ItemData("Beer", ItemClassification.filler, is_event=True, event_locations=["OW: Brewery"]),
    A1800ItemData("OW Police Station", ItemClassification.filler,
                  is_event=True, event_locations=["OW: Police Station"]),
    A1800ItemData("School", ItemClassification.progression, is_event=True, event_locations=["OW: School"]),
    A1800ItemData("Artisans", ItemClassification.progression,
                  is_event=True, event_locations=["OW: Artisan Residence"]),
    A1800ItemData("Victory", ItemClassification.progression, is_event=True, event_locations=["Victory Condition"]),
]

_unlock_item_list: list[A1800ItemData] = [
    *_anno_1800_unlock_items
]

_event_item_list: list[A1800ItemData] = [
    *_anno_1800_event_items
]

_item_list: list[A1800ItemData] = [
    *_unlock_item_list,
    *_event_item_list,
]

item_dict: dict[str, A1800ItemData] = {data.name: data for data in _item_list}
