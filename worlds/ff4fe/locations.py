import os.path
import pkgutil
from pkgutil import get_data
from typing import List

from BaseClasses import Location
from . import csvdb

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

    def __repr__(self):
        return self.name


all_locations: list[LocationData] = []

locationscsv = csvdb.CsvDb(pkgutil.get_data(__name__, "data/treasure.csvdb").decode().splitlines())

for location in locationscsv.create_view():
    if location.exclude != "":
        if location.exclude == "key":
            # Rat Tail and Ribbon chests are a little special in FE, as they're treasure chests but are considered
            # major reward locations.
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

minor_locations = [location for location in all_locations if location.major_slot == False]
minor_location_names = [location.name for location in minor_locations]

# This is actually a custom data table for the reward locations, mimicking the format of the treasure locations.
locationscsv = csvdb.CsvDb(pkgutil.get_data(__name__, "data/rewardslots.csvdb").decode().splitlines())

miab_slots = []

for location in locationscsv.create_view():
    # All reward locations are given their ID plus 512 so we can't confuse them with regular chests.
    new_location = LocationData("", location.world, location.area, int(location.fecode, 16) + 0x200, True)
    subname = f"{((' -- ' + location.spoilersubarea) if location.spoilersubarea != '' else '')}"
    new_location.name = (f"{location.spoilerarea}"
                         f"{subname}"
                         f" -- {location.spoilerdetail}")
    if "Monster in a Box" in new_location.name:
        miab_slots.append(new_location.name)
    all_locations.append(new_location)

major_locations = [location for location in all_locations if location.major_slot == True]
major_location_names = [location.name for location in major_locations]

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

# The name's a little unintuitive, I admit: this is the list of spots a restricted character _can't_ be.
restricted_character_locations = [
    "Starting Character 1",
    "Starting Character 2",
    *free_character_locations,
    "Baron Inn Character",
    "Mt. Hobs Character"
]

for location in character_slots:
    # Just like event reward locations, character locations get a constant added to separate them from treasures.
    all_locations.append(LocationData(location[0], location[1], location[2], location[3] + 0x200, True))

all_locations.append(LocationData("Objectives Status", "Overworld", "BaronTown", 0xEEEE, False))
all_locations.append(LocationData("Objective Reward", "Overworld", "BaronTown", 0xEEEF, False))

areas = []

area_groups: dict[str, list[str]] = dict()

area_correspondences: dict[str, list[str]] = {
    "BaronTown": ["Overworld", "Towns", "Baron Town"],
    "Mist": ["Overworld", "Towns", "Mist"],
    "Kaipo": ["Overworld", "Towns", "Kaipo"],
    "Silvera": ["Overworld", "Towns", "Silvera"],
    "ToroiaTown": ["Overworld", "Towns", "Toiroia Town"],
    "Agart": ["Overworld", "Towns", "Agart"],
    "BaronWeaponShop": ["Overworld", "Towns", "Baron Town"],
    "ChocoboForest": ["Overworld", "Towns", "Chocobo Forest"],
    "BaronCastle": ["Overworld", "Dungeons", "Baron Castle"],
    "Sewer": ["Overworld", "Dungeons", "Baron Castle"],
    "Damcyan": ["Overworld", "Towns", "Damcyan"],
    "Fabul": ["Overworld", "Towns", "Fabul"],
    "ToroiaCastle": ["Overworld", "Towns", "Toroia Castle"],
    "ToroiaTreasury": ["Overworld", "Towns", "Toroia Castle"],
    "Eblan": ["Overworld", "Dungeons", "Eblan Castle"],
    "MistCave": ["Overworld", "Dungeons", "Mist Cave"],
    "WateryPass": ["Overworld", "Dungeons", "Watery Pass"],
    "Waterfall": ["Overworld", "Dungeons", "Watery Pass"],
    "AntlionCave": ["Overworld", "Dungeons", "Antlion Cave"],
    "MountHobs": ["Overworld", "Dungeons", "Mount Hobs"],
    "MountOrdeals": ["Overworld", "Dungeons", "Mount Ordeals"],
    "CaveMagnes": ["Overworld", "Dungeons", "Cave Magnes"],
    "Zot": ["Overworld", "Dungeons", "Tower of Zot"],
    "UpperBabil": ["Overworld", "Dungeons", "Tower of Bab-il Upper"],
    "Giant": ["Overworld", "Moon", "Dungeons", "Giant of Bab-il"],
    "CaveEblan": ["Overworld", "Dungeons", "Cave Eblana"],
    "Smithy": ["Underworld", "Towns", "Smithy"],
    "Tomra": ["Underworld", "Towns", "Tomra"],
    "DwarfCastle": ["Underworld", "Towns", "Dwarf Castle"],
    "LowerBabil": ["Underworld", "Dungeons", "Tower of Bab-il", "Tower of Bab-il Lower"],
    "UpperBabilAfterFall": ["Overworld", "Dungeons", "Tower of Bab-il", "Tower of Bab-il Upper"],
    "CaveOfSummons": ["Underworld", "Dungeons", "Cave of Summons", "Land of Summons"],
    "Feymarch": ["Underworld", "Towns", "Dungeons", "Town of Monsters", "Land of Summons"],
    "SylvanCave": ["Underworld", "Dungeons", "Sylvan Cave"],
    "SealedCave": ["Underworld", "Dungeons", "Sealed Cave"],
    "BahamutCave": ["Moon", "Dungeons", "Cave Bahamut"],
    "LunarPath": ["Moon", "Dungeons", "Lunar Path"],
    "LunarCore": ["Moon", "Dungeons", "Lunar Subterrane"],
    "Adamant": ["Overworld", "Towns", "Adamant"],
    # These two are character-only locations, so they shouldn't get areas to exclude/prioritize
    "Mysidia": [],
    "LunarPalace": [],
}

for location in all_locations:
    if location.area not in areas:
        areas.append(location.area)
    area_names = area_correspondences[location.area]
    for area_name in area_names:
        if area_name not in area_groups.keys():
            area_groups[area_name] = []
        if location.name not in character_locations and "Objective" not in location.name:
            area_groups[area_name].append(location.name)

area_groups["MIABs"] = []
for location in miab_slots:
    area_groups["MIABs"].append(location)

for i in range(32):
    all_locations.append(LocationData(f"Objective {i + 1} Status", "Overworld", "BaronTown", 0xEE00 + i, False))


class Curve():
    tier1: int
    tier2: int
    tier3: int
    tier4: int
    tier5: int
    tier6: int
    tier7: int
    tier8: int

    def __init__(self, tier1: int, tier2: int, tier3: int, tier4: int, tier5: int, tier6: int, tier7: int, tier8: int):
        self.tier1 = tier1
        self.tier2 = tier2
        self.tier3 = tier3
        self.tier4 = tier4
        self.tier5 = tier5
        self.tier6 = tier6
        self.tier7 = tier7
        self.tier8 = tier8


areas_curves: dict[str, Curve] = {}

curves = csvdb.CsvDb(pkgutil.get_data(__name__, "data/curves.csvdb").decode().splitlines()).create_view()

for area in areas:
    area_curves = curves.find_one(lambda l: l.area == area)
    if area_curves is not None:
        areas_curves[area] = Curve(
            area_curves.tier1,
            area_curves.tier2,
            area_curves.tier3,
            area_curves.tier4,
            area_curves.tier5,
            area_curves.tier6,
            area_curves.tier7,
            area_curves.tier8)

def get_location_data(location_name: str):
    return [location for location in all_locations if location.name == location_name].pop()

