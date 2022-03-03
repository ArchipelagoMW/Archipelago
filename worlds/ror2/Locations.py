from BaseClasses import Location
import typing

class RiskOfRainLocation(Location):
    game: str = "Risk of Rain 2"

# 37000 - 38000
base_location_table = {
    "Victory": None,
    "Level One": None,
    "Level Two": None,
    "Level Three": None,
    "Level Four": None,
    "Level Five": None
}
# 37006 - 37506
item_pickups = {
    f"ItemPickup{i}": 37005+i for i in range(1, 501)
}

location_table = {**base_location_table, **item_pickups}

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, id in location_table.items()}
