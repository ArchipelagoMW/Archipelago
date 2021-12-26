from BaseClasses import Location
from .Incrementer import Incrementer
from .Constants import LOCATIONS_STARTING_INDEX, FAIRY_CHEST_MAXIMUM_PER_ZONE, \
    CHEST_MAXIMUM_PER_ZONE
import typing
import re


class LegacyLocation(Location):
    game: str = "Rogue Legacy"

    @staticmethod
    def print_location_table():
        print("=== STARTING PRINT LOCATION LIST ======================")
        for name, code in location_table.items():
            print(f"{{ \"{name}\", {code} }},")
        print("=== ENDING PRINT LOCATION LIST ========================")


counter = Incrementer(LOCATIONS_STARTING_INDEX)

base_location_table = {
    # Main Bosses
    "Khindr's Reward Left":                 counter.next(),
    "Khindr's Reward Right":                counter.next(),
    "Alexander's Reward Left":              counter.next(),
    "Alexander's Reward Right":             counter.next(),
    "Ponce de Leon's Reward Left":          counter.next(),
    "Ponce de Leon's Reward Right":         counter.next(),
    "Herodotus's Reward Left":              counter.next(),
    "Herodotus's Reward Right":             counter.next(),

    # 31 Manor Pieces                       
    "Manor Observatory Telescope":          counter.next(),
    "Manor Observatory Base":               counter.next(),
    "Manor Right High Tower":               counter.next(),
    "Manor Right High Upper":               counter.next(),
    "Manor Right High Base":                counter.next(),
    "Manor Right Big Roof":                 counter.next(),
    "Manor Right Big Upper":                counter.next(),
    "Manor Right Big Base":                 counter.next(),
    "Manor Right Wing Roof":                counter.next(),
    "Manor Right Wing Window":              counter.next(),
    "Manor Right Wing Base":                counter.next(),
    "Manor Right Extension":                counter.next(),
    "Manor Left Far Roof":                  counter.next(),
    "Manor Left Far Base":                  counter.next(),
    "Manor Left Big Roof":                  counter.next(),
    "Manor Left Big Upper 2":               counter.next(),
    "Manor Left Big Upper":                 counter.next(),
    "Manor Left Big Windows":               counter.next(),
    "Manor Left Big Base":                  counter.next(),
    "Manor Left Wing Roof":                 counter.next(),
    "Manor Left Wing Window":               counter.next(),
    "Manor Left Wing Base":                 counter.next(),
    "Manor Left Extension":                 counter.next(),
    "Manor Main Roof":                      counter.next(),
    "Manor Main Base":                      counter.next(),
    "Manor Front Top Windows":              counter.next(),
    "Manor Front Bottom Windows":           counter.next(),
    "Manor Ground Road":                    counter.next(),
    "Manor Left Tree 1":                    counter.next(),
    "Manor Left Tree 2":                    counter.next(),
    "Manor Right Tree":                     counter.next(),

    # Special Rooms
    "Carnival":                             counter.next(),
    "Cheapskate Elf":                       counter.next(),
    "Jukebox":                              counter.next(),
    "Secret Room Chest":                    counter.next(),

    # Diary Rooms
    **{f"Diary {i + 1}": counter.next() for i in range(0, 24)},
}

additional_location_table = {
    # Fairy Chests
    **{f"Castle Fairy Chest {i + 1}": counter.next() for i in
       range(0, FAIRY_CHEST_MAXIMUM_PER_ZONE)},
    **{f"Garden Fairy Chest {i + 1}": counter.next() for i in
       range(0, FAIRY_CHEST_MAXIMUM_PER_ZONE)},
    **{f"Tower Fairy Chest {i + 1}": counter.next() for i in
       range(0, FAIRY_CHEST_MAXIMUM_PER_ZONE)},
    **{f"Dungeon Fairy Chest {i + 1}": counter.next() for i in
       range(0, FAIRY_CHEST_MAXIMUM_PER_ZONE)},

    # Non-Fairy Chests
    **{f"Castle Chest {i + 1}": counter.next() for i in
       range(0, CHEST_MAXIMUM_PER_ZONE)},
    **{f"Garden Chest {i + 1}": counter.next() for i in
       range(0, CHEST_MAXIMUM_PER_ZONE)},
    **{f"Tower Chest {i + 1}": counter.next() for i in
       range(0, CHEST_MAXIMUM_PER_ZONE)},
    **{f"Dungeon Chest {i + 1}": counter.next() for i in
       range(0, CHEST_MAXIMUM_PER_ZONE)},
}

required_locations = 67

location_table = {
    **base_location_table,
    **additional_location_table,
}

lookup_id_to_name: typing.Dict[int, str] = {
    id: name for name, _ in location_table.items()
}
