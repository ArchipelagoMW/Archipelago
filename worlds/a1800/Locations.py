# import logging

from dataclasses import dataclass
from typing import ClassVar, Optional

from BaseClasses import Location, Region


@dataclass
class A1800LocationData:
    __location_id: ClassVar[int] = 1
    """The next location ID to use when creating location data."""

    name: str
    """The name of this location according to Archipelago.

    This needs to be unique within this world."""

    region: str
    """The region of this location."""

    ap_code: Optional[int] = None
    """Archipelago's internal ID for this location (also known as its "address")."""

    is_event: Optional[bool] = False
    """Whether this location is an event location with no ID."""

    def __post_init__(self):
        if not self.ap_code and not self.is_event:
            self.ap_code = A1800LocationData.__location_id
            A1800LocationData.__location_id += 1


class A1800Location(Location):
    game: str = "Anno 1800"
    data: A1800LocationData

    def __init__(self, player: int, data: A1800LocationData, parent: Region):
        super().__init__(player, data.name, None if data.is_event else data.ap_code, parent)
        self.data = data


_anno_1800_unlock_locations: list[A1800LocationData] = [
    A1800LocationData("50 Farmers - Fishery", "Old World"),
    A1800LocationData("100 Farmers - Sheep Farm", "Old World"),
    A1800LocationData("100 Farmers - Framework Knitters", "Old World"),
    A1800LocationData("100 Farmers - Potato Farm", "Old World"),
    A1800LocationData("100 Farmers - Schnapps Distillery", "Old World"),
    A1800LocationData("100 Farmers - Worker Residence", "Old World"),
    A1800LocationData("150 Farmers - Fire Station", "Old World"),
    A1800LocationData("150 Farmers - Pub", "Old World"),
    A1800LocationData("1 Worker - Paved Street", "Old World"),
    A1800LocationData("1 Worker - Clay Pit", "Old World"),
    A1800LocationData("1 Worker - Brick Factory", "Old World"),
    A1800LocationData("1 Worker - Pig Farm", "Old World"),
    A1800LocationData("1 Worker - Slaugherhouse", "Old World"),
    A1800LocationData("1 Worker - Medium Warehouse", "Old World"),
    A1800LocationData("1 Worker - Medium Trading Post", "Old World"),
    A1800LocationData("1 Worker - Trade Union", "Old World"),
    A1800LocationData("150 Workers - Grain Farm", "Old World"),
    A1800LocationData("150 Workers - Flour Mill", "Old World"),
    A1800LocationData("150 Workers - Bakery", "Old World"),
    A1800LocationData("150 Workers - Church", "Old World"),
    A1800LocationData("150 Workers - Sailmakers", "Old World"),
    A1800LocationData("150 Workers - Sailing Shipyard", "Old World"),
    A1800LocationData("150 Workers - Mounted Guns", "Old World"),
    A1800LocationData("150 Workers - Quay", "Old World"),
    A1800LocationData("150 Workers - Depot", "Old World"),
    A1800LocationData("150 Workers - Harbourmaster's Office", "Old World"),
    A1800LocationData("300 Workers - Charcoal Kiln", "Old World"),
    A1800LocationData("300 Workers - Iron Mine", "Old World"),
    A1800LocationData("300 Workers - Furnace", "Old World"),
    A1800LocationData("300 Workers - Steelworks", "Old World"),
    A1800LocationData("300 Workers - Rendering Works", "Old World"),
    A1800LocationData("300 Workers - Soap Factory", "Old World"),
    A1800LocationData("300 Workers - Weapon Factory", "Old World"),
    A1800LocationData("300 Workers - Cannon Tower", "Old World"),
    A1800LocationData("500 Workers - Hop Farm", "Old World"),
    A1800LocationData("500 Workers - Malthouse", "Old World"),
    A1800LocationData("500 Workers - Brewery", "Old World"),
    A1800LocationData("500 Workers - Police Station", "Old World"),
    A1800LocationData("750 Workers - School", "Old World"),
    A1800LocationData("750 Workers - Artisan Residence", "Old World"),
]

_anno_1800_event_locations: list[A1800LocationData] = [
    A1800LocationData("OW: Marketplace", "Old World", is_event=True),
    A1800LocationData("OW: Farmer Residence", "Old World", is_event=True),
    A1800LocationData("OW: Lumberjack's Hut", "Old World", is_event=True),
    A1800LocationData("OW: Sawmill", "Old World", is_event=True),
    A1800LocationData("OW: Fishery", "Old World", is_event=True),
    A1800LocationData("OW: Sheep Farm", "Old World", is_event=True),
    A1800LocationData("OW: Framework Knitters", "Old World", is_event=True),
    A1800LocationData("OW: Potato Farm", "Old World", is_event=True),
    A1800LocationData("OW: Schnapps Distillery", "Old World", is_event=True),
    A1800LocationData("OW: Worker Residence", "Old World", is_event=True),
    A1800LocationData("OW: Fire Station", "Old World", is_event=True),
    A1800LocationData("OW: Pub", "Old World", is_event=True),
    A1800LocationData("OW: Clay Pit", "Old World", is_event=True),
    A1800LocationData("OW: Brick Factory", "Old World", is_event=True),
    A1800LocationData("OW: Pig Farm", "Old World", is_event=True),
    A1800LocationData("OW: Slaughterhouse", "Old World", is_event=True),
    A1800LocationData("OW: Grain Farm", "Old World", is_event=True),
    A1800LocationData("OW: Flour Mill", "Old World", is_event=True),
    A1800LocationData("OW: Bakery", "Old World", is_event=True),
    A1800LocationData("OW: Church", "Old World", is_event=True),
    A1800LocationData("OW: Sailmakers", "Old World", is_event=True),
    A1800LocationData("OW: Sailing Shipyard", "Old World", is_event=True),
    A1800LocationData("OW: Charcoal Kiln", "Old World", is_event=True),
    A1800LocationData("OW: Iron Mine", "Old World", is_event=True),
    A1800LocationData("OW: Furnace", "Old World", is_event=True),
    A1800LocationData("OW: Steelworks", "Old World", is_event=True),
    A1800LocationData("OW: Rendering Works", "Old World", is_event=True),
    A1800LocationData("OW: Soap Factory", "Old World", is_event=True),
    A1800LocationData("OW: Weapon Factory", "Old World", is_event=True),
    A1800LocationData("OW: Hop Farm", "Old World", is_event=True),
    A1800LocationData("OW: Malthouse", "Old World", is_event=True),
    A1800LocationData("OW: Brewery", "Old World", is_event=True),
    A1800LocationData("OW: Police Station", "Old World", is_event=True),
    A1800LocationData("OW: School", "Old World", is_event=True),
    A1800LocationData("OW: Artisan Residence", "Old World", is_event=True),
    A1800LocationData("Victory Condition", "Old World", is_event=True),
]

unlock_location_list: list[A1800LocationData] = [
    *_anno_1800_unlock_locations,
]

event_location_list: list[A1800LocationData] = [
    *_anno_1800_event_locations,
]

location_list: list[A1800LocationData] = [
    *unlock_location_list,
    *event_location_list,
]
