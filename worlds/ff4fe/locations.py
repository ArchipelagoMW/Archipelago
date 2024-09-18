import os.path
import pkgutil
from pkgutil import get_data
from typing import List

from BaseClasses import Location
from .FreeEnterpriseForAP.FreeEnt import csvdb

class FF4FELocation(Location):
    game = 'Final Fantasy IV Free Enterprise'
    surface = ""
    area = ""

class LocationData():
    name: str
    surface: str
    area: str
    fe_id: int
    major_slot: bool

    def __init__(self, name, surface, area, fe_id, major_slot):
        self.name = name
        self.surface = surface
        self.area = area
        self.fe_id = fe_id
        self.major_slot = major_slot


    def to_json(self):
        return {
            "name": self.name
        }


all_locations: list[LocationData] = []

locationscsv = csvdb.CsvDb(pkgutil.get_data(__name__, "FreeEnterpriseForAP/FreeEnt/assets/db/treasure.csvdb").decode().splitlines())

miab_count = 0

for location in locationscsv.create_view():
    if location.exclude != "":
        if location.exclude == "key":
            new_location = LocationData("", location.world, location.area, int(location.flag, 16), True)
            if location.world == "Underworld":  # Rat Tail location
                new_location.name = f"Town of Monsters -- B4F (first area) -- Rat Tail"
            if location.world == "Moon":  # Ribbon location
                if location.x == "2":  # Left Ribbon
                    new_location.name = f"Lunar Subterrane -- B7 (right room) -- Ribbon Left"
                else:  # Right Ribbon
                    new_location.name = f"Lunar Subterrane -- B7 (right room) -- Ribbon Right"
            all_locations.append(new_location)
        continue
    new_location = LocationData("", location.world, location.area, int(location.flag, 16), False)
    subname = f"{((' -- ' + location.spoilersubarea) if location.spoilersubarea != '' else '')}"
    new_location.name = (f"{location.spoilerarea}"
                         f"{subname}"
                         f" -- {location.spoilerdetail}")
    all_locations.append(new_location)

locationscsv = csvdb.CsvDb(pkgutil.get_data(__name__, "FreeEnterpriseForAP/FreeEnt/assets/db/rewardslots.csvdb").decode().splitlines())

for location in locationscsv.create_view():
    new_location = LocationData("", location.world, location.area, int(location.fecode, 16) + 0x200, True)
    subname = f"{((' -- ' + location.spoilersubarea) if location.spoilersubarea != '' else '')}"
    new_location.name = (f"{location.spoilerarea}"
                         f"{subname}"
                         f" -- {location.spoilerdetail}")
    all_locations.append(new_location)

character_slots = [
    ("Starting Character 1", "Overworld", "BaronTown", 0x01),
    ("Starting Character 2", "Overworld", "BaronTown", 0x02),
    ("Mist Character", "Overworld", "Mist", 0x03),
    ("Watery Pass Character", "Overworld", "WateryPass", 0x04),
    ("Damcyan Character", "Overworld", "Damcyan", 0x05),
    ("Kaipo Character", "Overworld", "Kaipo", 0x06),
    ("Mt. Hobs Character", "Overworld", "MountHobs", 0x07),
    ("Mysidia Character 1", "Overworld", "Mysidia", 0x08),
    ("Mysidia Character 2", "Overworld", "Mysidia", 0x09),
    ("Mt. Ordeals Character", "Overworld", "MountOrdeals", 0x0A),
    ("Baron Inn Character", "Overworld", "BaronWeaponShop", 0x0D),
    ("Baron Castle Character", "Overworld", "BaronCastle", 0x0E),
    ("Tower of Zot Character 1", "Overworld", "Zot", 0x0F),
    ("Tower of Zot Character 2", "Overworld", "Zot", 0x10),
    ("Dwarf Castle Character", "Underworld", "DwarfCastle", 0x11),
    ("Cave Eblana Character", "Underworld", "CaveEblan", 0x12),
    ("Lunar Palace Character", "Moon", "LunarPalace", 0x13),
    ("Giant of Bab-il Character", "Moon", "Giant", 0x14)
]

character_locations = [location[0] for location in character_slots]

free_character_locations = [
    "Watery Pass Character",
    "Damcyan Character",
    "Mysidia Character 1",
    "Mysidia Character 2",
    "Mt. Ordeals Character",
]

earned_character_locations = [
    "Mist Character",
    "Kaipo Character",
    "Mt. Hobs Character",
    "Baron Inn Character",
    "Baron Castle Character",
    "Tower of Zot Character 1",
    "Tower of Zot Character 2",
    "Dwarf Castle Character",
    "Cave Eblana Character",
    "Lunar Palace Character",
    "Giant of Bab-il Character"
]

restricted_character_locations = [
    "Starting Character 1",
    "Starting Character 2",
    *free_character_locations,
    "Baron Inn Character",
    "Mt. Hobs Character"
]

for location in character_slots:
    all_locations.append(LocationData(location[0], location[1], location[2], location[3] + 0x200, True))

all_locations.append(LocationData("Objectives Status", "Overworld", "BaronTown", 0xEEEE, False))
all_locations.append(LocationData("Objective Reward", "Overworld", "BaronTown", 0xEEEF, False))

mutually_exclusive_slots = [
    ["Starting Character 1", "Starting Character 2"],
    ["Mysidia Character 1", "Mysidia Character 2"],
    ["Tower of Zot Character 1", "Tower of Zot Character 2"]
]

areas = []

for location in all_locations:
    if location.area not in areas:
        areas.append(location.area)

for i in range(32):
    all_locations.append(LocationData(f"Objective {i + 1} Status", "Overworld", "BaronTown", 0xEE00 + i, False))
