# import logging

from dataclasses import dataclass, field
from typing import ClassVar, TYPE_CHECKING, Optional
from BaseClasses import Item, ItemClassification as IC

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
    ICification: IC
    anno_guids: tuple[list[int], list[int]] = field(default_factory=lambda: ([], []))
    ap_code: Optional[int] = None
    is_event: Optional[bool] = False
    event_locations: list[str] = field(default_factory=lambda: [])

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
        super().__init__(data.name, data.ICification, None if data.is_event else data.ap_code, player)
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

    world.multiworld.local_early_items[world.player]["Unlock: OW: Fishery"] = 1
    world.multiworld.local_early_items[world.player]["Unlock: OW: Sheep Farm"] = 1
    world.multiworld.local_early_items[world.player]["Unlock: OW: Framework Knitters"] = 1
    world.multiworld.local_early_items[world.player]["Unlock: OW: Worker Residence"] = 1

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
    A1800ItemData("OW: Dirt Road", IC.progression, anno_guids=([1000178], [1000178])),
    A1800ItemData("OW: Marketplace", IC.progression, anno_guids=([130057], [1010372, 120020])),
    A1800ItemData("OW: Farmer Residence", IC.progression, anno_guids=([1010343], [1010343])),
    A1800ItemData("OW: Small Warehouse", IC.progression, anno_guids=([130040], [1010371])),
    A1800ItemData("OW: Lumberjack's Hut", IC.progression, anno_guids=([140029], [1010266, 120008, 500091])),
    A1800ItemData("OW: Sawmill", IC.progression, anno_guids=([140029], [100451, 1010196, 500091])),
]

_anno_1800_unlock_items: list[A1800ItemData] = [
    A1800ItemData("OW: Fishery", IC.progression, anno_guids=([130056], [1010278, 1010200])),
    A1800ItemData("OW: Sheep Farm", IC.progression, anno_guids=([130060], [1010267, 1010197, 500505])),
    A1800ItemData("OW: Framework Knitters", IC.progression, anno_guids=([130060], [1010315, 1010237, 500505])),
    A1800ItemData("OW: Potato Farm", IC.progression, anno_guids=([140028], [1010265, 1010195, 500002])),
    A1800ItemData("OW: Schnapps Distillery", IC.progression, anno_guids=([140028], [1010294, 1010216, 500002])),
    A1800ItemData("OW: Worker Residence", IC.progression, anno_guids=([1010344], [1010344])),
    A1800ItemData("OW: Fire Station", IC.progression, anno_guids=([1010463], [1010463])),
    A1800ItemData("OW: Pub", IC.progression, anno_guids=([130042], [1010358, 1010349])),
    A1800ItemData("OW: Paved Street", IC.filler, anno_guids=([1010035], [1010035])),
    A1800ItemData("OW: Clay Pit", IC.progression, anno_guids=([140031], [100416, 1010201, 500024])),
    A1800ItemData("OW: Brick Factory", IC.progression, anno_guids=([140031], [1010283, 1010205, 500024])),
    A1800ItemData("OW: Pig Farm", IC.progression, anno_guids=([140027], [1010269, 1010199, 25000244])),
    A1800ItemData("OW: Slaughterhouse", IC.progression, anno_guids=([140027], [1010316, 1010238, 25000244])),
    A1800ItemData("OW: Medium Warehouse", IC.filler, anno_guids=([130053], [100516])),
    A1800ItemData("OW: Medium Trading Post", IC.filler, anno_guids=([130053], [100510, 100514])),
    A1800ItemData("OW: Trade Union", IC.filler, anno_guids=([1010516], [1010516])),
    A1800ItemData("OW: Grain Farm", IC.progression, anno_guids=([140033], [1010262, 1010192, 500004])),
    A1800ItemData("OW: Flour Mill", IC.progression, anno_guids=([140033], [1010313, 1010235, 500004])),
    A1800ItemData("OW: Bakery", IC.progression, anno_guids=([140033], [1010291, 1010213, 500004])),
    A1800ItemData("OW: Church", IC.progression, anno_guids=([130043], [1010359, 1010350])),
    A1800ItemData("OW: Sailmakers", IC.progression, anno_guids=([140050], [1010288, 1010210, 500009])),
    A1800ItemData("OW: Sailing Shipyard", IC.progression, anno_guids=([130050], [1010520])),
    A1800ItemData("OW: Mounted Guns", IC.filler, anno_guids=([1010522], [1010522])),
    A1800ItemData("OW: Quay", IC.filler, anno_guids=([130121], [1010567])),
    A1800ItemData("OW: Depot", IC.filler, anno_guids=([130121], [1010519])),
    A1800ItemData("OW: Harbourmaster's Office", IC.filler, anno_guids=([100586], [100586])),
    A1800ItemData("OW: Charcoal Kiln", IC.progression, anno_guids=([140034], [1010298, 1010226, 500005])),
    A1800ItemData("OW: Iron Mine", IC.progression, anno_guids=([140034], [1010305, 1010227, 500005])),
    A1800ItemData("OW: Furnace", IC.progression, anno_guids=([140034], [1010297, 1010219, 500005])),
    A1800ItemData("OW: Steelworks", IC.progression, anno_guids=([140034], [1010296, 1010218, 500005])),
    A1800ItemData("OW: Rendering Works", IC.progression, anno_guids=([140030], [1010312, 1010234, 25000220])),
    A1800ItemData("OW: Soap Factory", IC.progression, anno_guids=([140030], [1010281, 1010203, 25000220])),
    A1800ItemData("OW: Weapon Factory", IC.progression, anno_guids=([140051], [1010299, 1010221, 500145])),
    A1800ItemData("OW: Cannon Tower", IC.filler, anno_guids=([1010523], [1010523])),
    A1800ItemData("OW: Hop Farm", IC.progression, anno_guids=([140035], [1010264, 1010194, 500006])),
    A1800ItemData("OW: Malthouse", IC.progression, anno_guids=([140035], [1010314, 1010236, 500006])),
    A1800ItemData("OW: Brewery", IC.progression, anno_guids=([140035], [1010292, 1010214, 500006])),
    A1800ItemData("OW: Police Station", IC.progression, anno_guids=([1010462], [1010462])),
    A1800ItemData("OW: School", IC.progression, anno_guids=([130044], [1010360, 1010351])),
    A1800ItemData("OW: Artisan Residence", IC.progression, anno_guids=([1010345], [1010345])),
]

_anno_1800_event_items: list[A1800ItemData] = [
    A1800ItemData("Market", IC.progression, is_event=True, event_locations=["OW: Marketplace"]),
    A1800ItemData("Farmers", IC.progression, is_event=True, event_locations=["OW: Farmer Residence"]),
    A1800ItemData("Wood", IC.progression, is_event=True, event_locations=["OW: Lumberjack's Hut"]),
    A1800ItemData("Timber", IC.progression, is_event=True, event_locations=["OW: Sawmill"]),
    A1800ItemData("Fish", IC.progression, is_event=True, event_locations=["OW: Fishery"]),
    A1800ItemData("Wool", IC.progression, is_event=True, event_locations=["OW: Sheep Farm"]),
    A1800ItemData("Work Clothes", IC.progression, is_event=True, event_locations=["OW: Framework Knitters"]),
    A1800ItemData("Potatoes", IC.progression, is_event=True, event_locations=["OW: Potato Farm"]),
    A1800ItemData("Schnapps", IC.progression, is_event=True, event_locations=["OW: Schnapps Distillery"]),
    A1800ItemData("Workers", IC.progression, is_event=True, event_locations=["OW: Worker Residence"]),
    A1800ItemData("OW Fire Station", IC.progression, is_event=True, event_locations=["OW: Fire Station"]),
    A1800ItemData("Pub", IC.progression, is_event=True, event_locations=["OW: Pub"]),
    A1800ItemData("Clay", IC.progression, is_event=True, event_locations=["OW: Clay Pit"]),
    A1800ItemData("Bricks", IC.progression, is_event=True, event_locations=["OW: Brick Factory"]),
    A1800ItemData("Pigs", IC.progression, is_event=True, event_locations=["OW: Pig Farm"]),
    A1800ItemData("Sausages", IC.progression, is_event=True, event_locations=["OW: Slaughterhouse"]),
    A1800ItemData("Grain", IC.progression, is_event=True, event_locations=["OW: Grain Farm"]),
    A1800ItemData("Flour", IC.progression, is_event=True, event_locations=["OW: Flour Mill"]),
    A1800ItemData("Bread", IC.progression, is_event=True, event_locations=["OW: Bakery"]),
    A1800ItemData("Church", IC.progression, is_event=True, event_locations=["OW: Church"]),
    A1800ItemData("Sails", IC.progression, is_event=True, event_locations=["OW: Sailmakers"]),
    A1800ItemData("Ships", IC.progression, is_event=True, event_locations=["OW: Sailing Shipyard"]),
    A1800ItemData("Coal", IC.progression, is_event=True, event_locations=["OW: Charcoal Kiln"]),
    A1800ItemData("Iron", IC.progression, is_event=True, event_locations=["OW: Iron Mine"]),
    A1800ItemData("Steel", IC.progression, is_event=True, event_locations=["OW: Furnace"]),
    A1800ItemData("Steel Beams", IC.progression, is_event=True, event_locations=["OW: Steelworks"]),
    A1800ItemData("Tallow", IC.progression, is_event=True, event_locations=["OW: Rendering Works"]),
    A1800ItemData("Soap", IC.progression, is_event=True, event_locations=["OW: Soap Factory"]),
    A1800ItemData("Weapons", IC.filler, is_event=True, event_locations=["OW: Weapon Factory"]),
    A1800ItemData("Hops", IC.progression, is_event=True, event_locations=["OW: Hop Farm"]),
    A1800ItemData("Malt", IC.progression, is_event=True, event_locations=["OW: Malthouse"]),
    A1800ItemData("Beer", IC.progression, is_event=True, event_locations=["OW: Brewery"]),
    A1800ItemData("OW Police Station", IC.progression, is_event=True, event_locations=["OW: Police Station"]),
    A1800ItemData("School", IC.progression, is_event=True, event_locations=["OW: School"]),
    A1800ItemData("Artisans", IC.progression, is_event=True, event_locations=["OW: Artisan Residence"]),
    A1800ItemData("Victory", IC.progression, is_event=True, event_locations=["Victory Condition"]),
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
