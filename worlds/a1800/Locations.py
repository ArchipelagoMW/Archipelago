# import logging

from dataclasses import dataclass
from typing import ClassVar, Optional

from BaseClasses import Location, Region

_populations: dict[str, int] = {
    "Farmers": 15000000,
    "Workers": 15000001,
    "Artisans": 15000002
}


@dataclass
class A1800LocationData:
    __location_id: ClassVar[int] = 1
    """The next location ID to use when creating location data."""

    name: str
    """The name of this location according to Archipelago.

    This needs to be unique within this world."""

    region: str
    """The region of this location."""

    population: Optional[str] = None

    amount: Optional[int] = None

    population_guid: Optional[int] = None

    ap_code: Optional[int] = None
    """Archipelago's internal ID for this location (also known as its "address")."""

    is_event: bool = False
    """Whether this location is an event location with no ID."""

    def __post_init__(self):
        if not self.ap_code and not self.is_event:
            self.ap_code = A1800LocationData.__location_id
            A1800LocationData.__location_id += 1
        if self.population:
            self.population_guid = _populations[self.population]
        if self.population and self.amount and not self.is_event:
            self.name = f"{self.amount} {self.population if self.amount != 1 else self.population[:-1]} - {self.name}"


class A1800Location(Location):
    game: str = "Anno 1800"
    data: A1800LocationData

    def __init__(self, player: int, data: A1800LocationData, parent: Region):
        super().__init__(player, data.name, None if data.is_event else data.ap_code, parent)
        self.show_in_spoiler = not data.is_event
        self.data = data


_anno_1800_unlock_locations: list[A1800LocationData] = [
    A1800LocationData("Fishery", "Old World", "Farmers", 50),
    A1800LocationData("Sheep Farm", "Old World", "Farmers", 100),
    A1800LocationData("Framework Knitters", "Old World", "Farmers", 100),
    A1800LocationData("Potato Farm", "Old World", "Farmers", 100),
    A1800LocationData("Schnapps Distillery", "Old World", "Farmers", 100),
    A1800LocationData("Worker Residence", "Old World", "Farmers", 100),
    A1800LocationData("Fire Station", "Old World", "Farmers", 150),
    A1800LocationData("Pub", "Old World", "Farmers", 150),
    A1800LocationData("Paved Street", "Old World", "Workers", 1),
    A1800LocationData("Clay Pit", "Old World", "Workers", 1),
    A1800LocationData("Brick Factory", "Old World", "Workers", 1),
    A1800LocationData("Pig Farm", "Old World", "Workers", 1),
    A1800LocationData("Slaugherhouse", "Old World", "Workers", 1),
    A1800LocationData("Medium Warehouse", "Old World", "Workers", 1),
    A1800LocationData("Medium Trading Post", "Old World", "Workers", 1),
    A1800LocationData("Trade Union", "Old World", "Workers", 1),
    A1800LocationData("Grain Farm", "Old World", "Workers", 150),
    A1800LocationData("Flour Mill", "Old World", "Workers", 150),
    A1800LocationData("Bakery", "Old World", "Workers", 150),
    A1800LocationData("Church", "Old World", "Workers", 150),
    A1800LocationData("Sailmakers", "Old World", "Workers", 150),
    A1800LocationData("Sailing Shipyard", "Old World", "Workers", 150),
    A1800LocationData("Mounted Guns", "Old World", "Workers", 150),
    A1800LocationData("Quay", "Old World", "Workers", 150),
    A1800LocationData("Depot", "Old World", "Workers", 150),
    A1800LocationData("Harbourmaster's Office", "Old World", "Workers", 150),
    A1800LocationData("Charcoal Kiln", "Old World", "Workers", 300),
    A1800LocationData("Iron Mine", "Old World", "Workers", 300),
    A1800LocationData("Furnace", "Old World", "Workers", 300),
    A1800LocationData("Steelworks", "Old World", "Workers", 300),
    A1800LocationData("Rendering Works", "Old World", "Workers", 300),
    A1800LocationData("Soap Factory", "Old World", "Workers", 300),
    A1800LocationData("Weapon Factory", "Old World", "Workers", 300),
    A1800LocationData("Cannon Tower", "Old World", "Workers", 300),
    A1800LocationData("Hop Farm", "Old World", "Workers", 500),
    A1800LocationData("Malthouse", "Old World", "Workers", 500),
    A1800LocationData("Brewery", "Old World", "Workers", 500),
    A1800LocationData("Police Station", "Old World", "Workers", 500),
    A1800LocationData("School", "Old World", "Workers", 750),
    A1800LocationData("Artisan Residence", "Old World", "Workers", 750),
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
    A1800LocationData("Victory Condition", "Old World", "Artisans", 1, is_event=True),
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
