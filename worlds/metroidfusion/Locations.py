import pkgutil
import json
from enum import IntEnum

from BaseClasses import Location, ItemClassification
from .Items import mars_name_to_ap_name, major_jingles
from .data.locations import fusion_regions
from .data.logic.Requirement import Requirement
from .data.logic import topologies
from .data.major_locations import boss_locations
from .data.minor_locations import extended_boss_locations


class MetroidFusionLocation(Location):
    game = "Metroid Fusion"
    logic_rule: list[list[str]]

class LocationData:
    name: str
    mars_id: tuple[int, int]
    major: bool
    requirements: list[Requirement]
    ap_id: int
    source_name: str
    room_location: tuple[int, int]
    room_name: str

    def __init__(self, name: str, major: bool, ap_id: int):
        self.name = name
        self.major = major
        self.ap_id = ap_id

    def to_json(self, item: str, item_sprite: str, item_classification: ItemClassification):
        ap_name = mars_name_to_ap_name[item]
        if ap_name in major_jingles or (item_classification & ItemClassification.progression and ap_name != "Energy Tank"):
            jingle = "Major"
        else:
            jingle = "Minor"
        if self.major:
            return {
                "Source": self.source_name,
                "Item": item,
                "Jingle": jingle
            }
        else:
            return {
                "Area": self.mars_id[0],
                "Room": self.mars_id[1],
                "BlockX": self.room_location[0],
                "BlockY": self.room_location[1],
                "Item": item,
                "ItemSprite": item_sprite,
                "Jingle": jingle
            }

    def __repr__(self):
        return self.name

def build_item_message(item_name: str, player_name: str):
    return {
        "Languages": {
            "English": f"Found {player_name}'s\n{item_name}",
        },
        "Kind": "CustomMessage"
    }

def build_shiny_item_message(item_name: str):
    return {
        "Languages": {
            "English": f"Found a Shiny {item_name}!\nIt's shiny, so it's special.",
        },
        "Kind": "CustomMessage"
    }


def populate_json_data(location_data: LocationData):
    file = pkgutil.get_data(__name__, "data/new_locations.json").decode()
    json_data = json.loads(file)
    locations = json_data["MajorLocations"]
    for location in locations:
        if location["room_name"] == location_data.name:
            location_data.source_name = location["Source"]
    locations = json_data["MinorLocations"]
    for location in locations:
        if location["room_name"] == location_data.name:
            location_data.mars_id = location["Area"], location["Room"]
            location_data.room_location = location["BlockX"], location["BlockY"]

file = pkgutil.get_data(__name__, "data/new_locations.json").decode()
json_data = json.loads(file)
locations = json_data["MinorLocations"]

all_locations: list[LocationData] = []
location_ids: dict[str, int] = dict()
major_location_names: list[str] = []

ap_id = 1
for region in fusion_regions:
    for location in region.locations:
        location_data = LocationData(location.name, location.major, ap_id)
        location_data.requirements = location.requirements
        populate_json_data(location_data)
        all_locations.append(location_data)
        if location.major:
            major_location_names.append(location.name)
        ap_id += 1


shinespark_locations = [
    "Sector 1 (SRX) -- Charge Core Arena -- Upper Item",
    "Sector 1 (SRX) -- Watering Hole",
    "Sector 2 (TRO) -- Zazabi Speedway -- Lower Item",
    "Sector 2 (TRO) -- Zazabi Speedway -- Upper Item",
    "Sector 3 (PYR) -- Fiery Storage -- Upper Item",
    "Sector 3 (PYR) -- Deserted Runway",
    "Sector 3 (PYR) -- Garbage Chute -- Lower Item",
    "Sector 3 (PYR) -- Garbage Chute -- Upper Item",
    "Sector 5 (ARC) -- Training Aerie -- Left Item",
    "Sector 4 (AQA) -- Aquarium Kago Storage -- Right Item",
    "Sector 5 (ARC) -- Training Aerie -- Left Item",
    "Sector 5 (ARC) -- Flooded Airlock to Sector 4 (AQA)",
    "Sector 6 (NOC) -- Pillar Highway",
    "Sector 6 (NOC) -- Spaceboost Alley -- Lower Item",
    "Sector 6 (NOC) -- Spaceboost Alley -- Upper Item",
    "Main Deck -- Restricted Airlock"
]

main_deck_locations = [
    "Main Deck -- Cubby Hole",
    "Main Deck -- Genesis Speedway",
    "Main Deck -- Quarantine Bay",
    "Main Deck -- Station Entrance",
    "Main Deck -- Sub-Zero Containment",
    "Main Deck -- Operations Ventilation",
    "Main Deck -- Operations Ventilation Storage",
    "Main Deck -- Arachnus Arena -- Upper Item",
    "Main Deck -- Attic",
    "Main Deck -- Arachnus Arena -- Core X",
    "Main Deck -- Operations Deck Data Room",
    "Main Deck -- Habitation Deck -- Animals",
    "Main Deck -- Habitation Deck -- Lower Item",
    "Main Deck -- Main Elevator Cache",
    "Main Deck -- Silo Catwalk",
    "Main Deck -- Silo Scaffolding",
    "Main Deck -- Yakuza Arena",
    "Main Deck -- Auxiliary Power Station",
    "Main Deck -- Nexus Storage"
]

sector_1_locations = [
    "Sector 1 (SRX) -- Antechamber",
    "Sector 1 (SRX) -- Atmospheric Stabilizer Northeast",
    "Sector 1 (SRX) -- Hornoad Hole",
    "Sector 1 (SRX) -- Wall Jump Tutorial",
    "Sector 1 (SRX) -- Lava Lake -- Lower Item",
    "Sector 1 (SRX) -- Lava Lake -- Upper Left Item",
    "Sector 1 (SRX) -- Lava Lake -- Upper Right Item",
    "Sector 1 (SRX) -- Stabilizer Storage",
    "Sector 1 (SRX) -- Charge Core Arena -- Core X",
    "Sector 1 (SRX) -- Charge Core Arena -- Upper Item",
    "Sector 1 (SRX) -- Watering Hole",
    "Sector 1 (SRX) -- Crab Rave",
    "Sector 1 (SRX) -- Animorphs Cache",
    "Sector 1 (SRX) -- Ridley Arena",
    "Sector 1 (SRX) -- Ripper Maze"
]

sector_2_locations = [
    "Sector 2 (TRO) -- Crumble City -- Lower Item",
    "Sector 2 (TRO) -- Crumble City -- Upper Item",
    "Sector 2 (TRO) -- Data Courtyard",
    "Sector 2 (TRO) -- Data Room",
    "Sector 2 (TRO) -- Kago Room",
    "Sector 2 (TRO) -- Level 1 Security Room",
    "Sector 2 (TRO) -- Lobby Cache",
    "Sector 2 (TRO) -- Zoro Zig-Zag",
    "Sector 2 (TRO) -- Cultivation Station",
    "Sector 2 (TRO) -- Oasis",
    "Sector 2 (TRO) -- Oasis Storage",
    "Sector 2 (TRO) -- Ripper Tower -- Lower Item",
    "Sector 2 (TRO) -- Ripper Tower -- Upper Item",
    "Sector 2 (TRO) -- Zazabi Arena",
    "Sector 2 (TRO) -- Zazabi Arena Access",
    "Sector 2 (TRO) -- Zazabi Speedway -- Lower Item",
    "Sector 2 (TRO) -- Zazabi Speedway -- Upper Item",
    "Sector 2 (TRO) -- Dessgeega Dorm",
    "Sector 2 (TRO) -- Nettori Arena",
    "Sector 2 (TRO) -- Overgrown Cache",
    "Sector 2 (TRO) -- Puyo Palace"
]

sector_3_locations = [
    "Sector 3 (PYR) -- Fiery Storage -- Lower Item",
    "Sector 3 (PYR) -- Fiery Storage -- Upper Item",
    "Sector 3 (PYR) -- Glass Tube to Sector 5 (ARC)",
    "Sector 3 (PYR) -- Level 2 Security Room",
    "Sector 3 (PYR) -- Security Access",
    "Sector 3 (PYR) -- Namihe's Lair",
    "Sector 3 (PYR) -- Processing Access",
    "Sector 3 (PYR) -- Lava Maze",
    "Sector 3 (PYR) -- Main Boiler Control Room -- Boiler",
    "Sector 3 (PYR) -- Main Boiler Control Room -- Core X",
    "Sector 3 (PYR) -- Bob's Abode",
    "Sector 3 (PYR) -- Data Room",
    "Sector 3 (PYR) -- Geron's Treasure",
    "Sector 3 (PYR) -- Alcove -- Lower Item",
    "Sector 3 (PYR) -- Alcove -- Upper Item",
    "Sector 3 (PYR) -- Deserted Runway",
    "Sector 3 (PYR) -- Sova Processing -- Left Item",
    "Sector 3 (PYR) -- Sova Processing -- Right Item",
    "Sector 3 (PYR) -- Garbage Chute -- Lower Item",
    "Sector 3 (PYR) -- Garbage Chute -- Upper Item"
]

sector_4_locations = [
    "Sector 4 (AQA) -- Drain Pipe",
    "Sector 4 (AQA) -- Reservoir East",
    "Sector 4 (AQA) -- Broken Bridge",
    "Sector 4 (AQA) -- C-Cache",
    "Sector 4 (AQA) -- Reservoir Vault -- Lower Item",
    "Sector 4 (AQA) -- Reservoir Vault -- Upper Item",
    "Sector 4 (AQA) -- Serris Arena",
    "Sector 4 (AQA) -- Pump Control Unit",
    "Sector 4 (AQA) -- Cargo Hold to Sector 5 (ARC)",
    "Sector 4 (AQA) -- Waterway",
    "Sector 4 (AQA) -- Aquarium Pirate Tank",
    "Sector 4 (AQA) -- Cheddar Bay",
    "Sector 4 (AQA) -- Yard Firing Range",
    "Sector 4 (AQA) -- Sanctuary Cache",
    "Sector 4 (AQA) -- Level 4 Security Room",
    "Sector 4 (AQA) -- Aquarium Kago Storage -- Left Item",
    "Sector 4 (AQA) -- Aquarium Kago Storage -- Right Item",
    "Sector 4 (AQA) -- Data Room"
]

sector_5_locations = [
    "Sector 5 (ARC) -- Gerubus Gully",
    "Sector 5 (ARC) -- Magic Box",
    "Sector 5 (ARC) -- Training Aerie -- Left Item",
    "Sector 5 (ARC) -- Training Aerie -- Right Item",
    "Sector 5 (ARC) -- Ripper Road",
    "Sector 5 (ARC) -- E-Tank Mimic Den",
    "Sector 5 (ARC) -- Level 3 Security Room",
    "Sector 5 (ARC) -- Ripper's Treasure",
    "Sector 5 (ARC) -- Security Shaft East",
    "Sector 5 (ARC) -- Transmutation Trial",
    "Sector 5 (ARC) -- Data Room",
    "Sector 5 (ARC) -- Crow's Nest",
    "Sector 5 (ARC) -- Flooded Airlock to Sector 4 (AQA)",
    "Sector 5 (ARC) -- Mini-Fridge",
    "Sector 5 (ARC) -- Nightmare Hub",
    "Sector 5 (ARC) -- Ruined Break Room",
    "Sector 5 (ARC) -- Nightmare Arena",
    "Sector 5 (ARC) -- Nightmare Nook"
]

sector_6_locations = [
    "Sector 6 (NOC) -- Entrance Lobby",
    "Sector 6 (NOC) -- Catacombs",
    "Sector 6 (NOC) -- Missile Mimic Lodge",
    "Sector 6 (NOC) -- Pillar Highway",
    "Sector 6 (NOC) -- Vault",
    "Sector 6 (NOC) -- Spaceboost Alley -- Lower Item",
    "Sector 6 (NOC) -- Spaceboost Alley -- Upper Item",
    "Sector 6 (NOC) -- X-B.O.X. Arena",
    "Sector 6 (NOC) -- X-B.O.X. Garage -- Lower Item",
    "Sector 6 (NOC) -- X-B.O.X. Garage -- Upper Item",
    "Main Deck -- Restricted Airlock",
    "Sector 6 (NOC) -- Zozoro Wine Cellar",
    "Sector 6 (NOC) -- Varia Core-X Arena",
    "Sector 6 (NOC) -- Twin Caverns West -- Lower Item",
    "Sector 6 (NOC) -- Twin Caverns West -- Upper Item"
]

location_groups = {
    "ShinesparkLocations": shinespark_locations,
    "MajorLocations": major_location_names,
    "BossLocations": boss_locations,
    "BossLocationsExtended": [*boss_locations, *extended_boss_locations],
    "MainDeckLocations": main_deck_locations,
    "Sector1Locations": sector_1_locations,
    "Sector2Locations": sector_2_locations,
    "Sector3Locations": sector_3_locations,
    "Sector4Locations": sector_4_locations,
    "Sector5Locations": sector_5_locations,
    "Sector6Locations": sector_6_locations
}


class ERGroups(IntEnum):
    TUBE_LEFT = 0
    TUBE_RIGHT = 1
    ELEVATOR_TOP = 2
    ELEVATOR_BOTTOM = 3
    STATIC = 5

def get_location_data_by_name(name: str):
    return [location for location in all_locations if location.name == name].pop()
