from BaseClasses import Location
import typing

class LegacyLocation(Location):
    game: str = "Rogue Legacy"

location_table = {
    **{ f"Fairy Chest {i + 1}": 44300 + i for i in range(0, 55) },
    **{ f"Chest {i + 1}": 44400 + i for i in range(0, 453 - 55) },
}

lookup_id_to_name: typing.Dict[int, str] = { id: name for name, id in location_table.items() }
