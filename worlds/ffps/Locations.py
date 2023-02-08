from BaseClasses import Location
import typing
from .Items import item_table


class LocData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str
    setId: str


class FFPSLocations(Location):
    game: str = "FFPS"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


location_table = {
    "Salvage ScrapTrap": LocData(57500, 'Salvage', "m3"),
    "Salvage Scrap Baby": LocData(57501, 'Salvage', "m4"),
    "Salvage Lefty": LocData(57502, 'Salvage', "m5"),
    "Salvage Molten Freddy": LocData(57503, 'Salvage', "m2"),
    "Unlocked Catalogue 2": LocData(57504, 'Pizzeria', "un1"),
    "Unlocked Catalogue 3": LocData(57505, 'Pizzeria', "un2"),
    "Unlocked Catalogue 4": LocData(57506, 'Pizzeria', "un3"),
    "Bought Printer Upgrade": LocData(57507, 'Office', "printer"),
    "Bought Handyman Upgrade": LocData(57508, 'Office', "handyman"),
    "Bought Internet Upgrade": LocData(57509, 'Office', "hispeed"),
}

for name, data in item_table.items():
    if data.setId != "":
        if data.code >= 55600 and data.setId != "stage" and data.setId != "cups" and data.setId != "speakers":
            location_table.update({"Buy " + name: LocData(len(location_table)+57500, 'Pizzeria', data.setId), })
for i in range(5):
    location_table.update({"Buy Stage Upgrade " +
                           str(i+1): LocData(len(location_table)+57500, 'Pizzeria', 'stage'), })
for i in range(4):
    location_table.update({"Buy Cups Upgrade " +
                           str(i+1): LocData(len(location_table)+57500, 'Pizzeria', 'cups'), })
for i in range(2):
    location_table.update({"Buy Speaker Upgrade " +
                           str(i+1): LocData(len(location_table)+57500, 'Pizzeria', 'speakers'), })

exclusion_table = {
}

events_table = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.id: item_name for item_name, data in location_table.items() if data.id}
