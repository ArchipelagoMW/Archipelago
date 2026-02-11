from typing import Optional
from BaseClasses import Item, ItemClassification
from enum import Enum

from worlds.mindustry.Shared import MINDUSTRY_BASE_ID


"""This class (ItemType) might need to be renamed and have its content changed for something more useful?"""
class ItemType(Enum):
    """
    Indicate to the multi-world the item usefulness
    """
    TRAP = 0
    """Non-item event with negative effect"""
    EVENT = 1
    """Non-item event"""
    USEFUL = 2
    """Item that are useful for progression"""
    NECESSARY = 3
    """Item that are necessary for progression"""
    JUNK = 4
    """Item that are not useful or necessary for progression"""

class ItemGroup(Enum):
    """
    Used to group items, Item are grouped by their location in the building UI
    """
    TURRET = 0
    EXTRACTION = 1
    BELT = 2
    CONDUIT = 3
    ENERGY = 4
    WALL = 5
    INDUSTRY = 6
    FACTORY = 7
    LOGIC = 8
    MISC = 9
    UNIT = 10
    RESSOURCES = 11
    SECTOR = 12
    FILLER = 13

class ItemPlanet(Enum):
    """
    Used to group items by planet
    """
    EREKIR = 0
    SERPULO = 1
    ALL = 2


class MindustryItem(Item):
    """
    A single item in the Mindustry game.
    """
    game: str = "Mindustry"
    """The name of the game"""

    def __init__(self, name: str, classification: ItemClassification,
                 code: Optional[int], player: int):
        """
        Initialisation of the Item
        :param name: The name of the item
        :param classification: If the item is usefull or not
        :param code: The ID of the item (if None, it is an event)
        :param player: The ID of the player in the multiworld
        """
        super().__init__(name, classification, code, player)


class ItemData:
    """
    Data of an item
    """
    id: int
    item_planet: ItemPlanet
    type: ItemType
    group: ItemGroup
    count: int

    def __init__(self, id: int, planet: ItemPlanet, type: ItemType, group: ItemGroup, count:int):
        """
        Initialisation of the item data
        @param id: The ID of the item
        @param planet: The planet of the item
        @param type: The type of item
        @param group: The type of item
        """
        self.id = id
        self.item_planet = planet
        self.type = type
        self.group = group
        self.count = count

"""Information table for every item that is not an event."""
item_table = {
    #Serpulo and Erekir

    #"Thorium": ItemData(MINDUSTRY_BASE_ID + 169, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Surge Alloy": ItemData(MINDUSTRY_BASE_ID + 170, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Phase Fabric": ItemData(MINDUSTRY_BASE_ID + 171, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),

    #Serpulo

    #"Conveyor": ItemData(MINDUSTRY_BASE_ID + 0, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.BELT, 1),
    "Junction": ItemData(MINDUSTRY_BASE_ID + 1, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Router": ItemData(MINDUSTRY_BASE_ID + 2, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Launch Pad": ItemData(MINDUSTRY_BASE_ID + 3, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Distributor": ItemData(MINDUSTRY_BASE_ID + 4, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Sorter": ItemData(MINDUSTRY_BASE_ID + 5, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Inverted Sorter": ItemData(MINDUSTRY_BASE_ID + 6, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Overflow Gate": ItemData(MINDUSTRY_BASE_ID + 7, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Underflow Gate": ItemData(MINDUSTRY_BASE_ID + 8, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Container": ItemData(MINDUSTRY_BASE_ID + 9, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Unloader": ItemData(MINDUSTRY_BASE_ID + 10, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Vault": ItemData(MINDUSTRY_BASE_ID + 11, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Bridge Conveyor": ItemData(MINDUSTRY_BASE_ID + 12, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Titanium Conveyor": ItemData(MINDUSTRY_BASE_ID + 13, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Phase Conveyor": ItemData(MINDUSTRY_BASE_ID + 14, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Mass Driver": ItemData(MINDUSTRY_BASE_ID + 15, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Payload Conveyor": ItemData(MINDUSTRY_BASE_ID + 16, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Payload Router": ItemData(MINDUSTRY_BASE_ID + 17, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Armored Conveyor": ItemData(MINDUSTRY_BASE_ID + 18, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Plastanium Conveyor": ItemData(MINDUSTRY_BASE_ID + 19, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Core: Foundation": ItemData(MINDUSTRY_BASE_ID + 20, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Core: Nucleus": ItemData(MINDUSTRY_BASE_ID + 21, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    #"Mechanical Drill": ItemData(MINDUSTRY_BASE_ID + 22, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.EXTRACTION, 1),
    "Mechanical Pump": ItemData(MINDUSTRY_BASE_ID + 23, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.CONDUIT, 1),
    "Conduit": ItemData(MINDUSTRY_BASE_ID + 24, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.CONDUIT, 1),
    "Liquid Junction": ItemData(MINDUSTRY_BASE_ID + 25, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Liquid Router": ItemData(MINDUSTRY_BASE_ID + 26, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Liquid Container": ItemData(MINDUSTRY_BASE_ID + 27, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Liquid Tank": ItemData(MINDUSTRY_BASE_ID + 28, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Bridge Conduit": ItemData(MINDUSTRY_BASE_ID + 29, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Pulse Conduit": ItemData(MINDUSTRY_BASE_ID + 30, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Phase Conduit": ItemData(MINDUSTRY_BASE_ID + 31, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Plated Conduit": ItemData(MINDUSTRY_BASE_ID + 32, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Rotary Pump": ItemData(MINDUSTRY_BASE_ID + 33, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Impulse Pump": ItemData(MINDUSTRY_BASE_ID + 34, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Graphite Press": ItemData(MINDUSTRY_BASE_ID + 35, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Pneumatic Drill": ItemData(MINDUSTRY_BASE_ID + 36, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.EXTRACTION, 1),
    "Cultivator": ItemData(MINDUSTRY_BASE_ID + 37, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.EXTRACTION, 1),
    "Laser Drill": ItemData(MINDUSTRY_BASE_ID + 38, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.EXTRACTION, 1),
    "Airblast Drill": ItemData(MINDUSTRY_BASE_ID + 39, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.EXTRACTION, 1),
    "Water Extractor": ItemData(MINDUSTRY_BASE_ID + 40, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.EXTRACTION, 1),
    "Oil Extractor": ItemData(MINDUSTRY_BASE_ID + 41, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.EXTRACTION, 1),
    "Pyratite Mixer": ItemData(MINDUSTRY_BASE_ID + 42, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Blast Mixer": ItemData(MINDUSTRY_BASE_ID + 43, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Silicon Smelter": ItemData(MINDUSTRY_BASE_ID + 44, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Spore Press": ItemData(MINDUSTRY_BASE_ID + 45, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Coal Centrifuge": ItemData(MINDUSTRY_BASE_ID + 46, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Multi-Press": ItemData(MINDUSTRY_BASE_ID + 47, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Silicon Crucible": ItemData(MINDUSTRY_BASE_ID + 48, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Plastanium Compressor": ItemData(MINDUSTRY_BASE_ID + 49, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Phase Weaver": ItemData(MINDUSTRY_BASE_ID + 50, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Kiln": ItemData(MINDUSTRY_BASE_ID + 51, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Pulverizer": ItemData(MINDUSTRY_BASE_ID + 52, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Incinerator": ItemData(MINDUSTRY_BASE_ID + 53, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Melter": ItemData(MINDUSTRY_BASE_ID + 54, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Surge Smelter": ItemData(MINDUSTRY_BASE_ID + 55, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Separator": ItemData(MINDUSTRY_BASE_ID + 56, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Disassembler": ItemData(MINDUSTRY_BASE_ID + 57, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Cryofluid Mixer": ItemData(MINDUSTRY_BASE_ID + 58, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Micro Processor": ItemData(MINDUSTRY_BASE_ID + 59, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Switch": ItemData(MINDUSTRY_BASE_ID + 60, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Message": ItemData(MINDUSTRY_BASE_ID + 61, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Logic Display": ItemData(MINDUSTRY_BASE_ID + 62, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Large Logic Display": ItemData(MINDUSTRY_BASE_ID + 63, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Memory Cell": ItemData(MINDUSTRY_BASE_ID + 64, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Memory Bank": ItemData(MINDUSTRY_BASE_ID + 65, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Logic Processor": ItemData(MINDUSTRY_BASE_ID + 66, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Hyper Processor": ItemData(MINDUSTRY_BASE_ID + 67, ItemPlanet.SERPULO, ItemType.JUNK, ItemGroup.LOGIC, 1),
    "Illuminator": ItemData(MINDUSTRY_BASE_ID + 68, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Combustion Generator": ItemData(MINDUSTRY_BASE_ID + 69, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.ENERGY, 1),
    "Power Node": ItemData(MINDUSTRY_BASE_ID + 70, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Large Power Node": ItemData(MINDUSTRY_BASE_ID + 71, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Battery Diode": ItemData(MINDUSTRY_BASE_ID + 72, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Surge Tower": ItemData(MINDUSTRY_BASE_ID + 73, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Battery": ItemData(MINDUSTRY_BASE_ID + 74, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Large Battery": ItemData(MINDUSTRY_BASE_ID + 75, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Mender": ItemData(MINDUSTRY_BASE_ID + 76, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Mend Projector": ItemData(MINDUSTRY_BASE_ID + 77, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Force Projector": ItemData(MINDUSTRY_BASE_ID + 78, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Overdrive Projector": ItemData(MINDUSTRY_BASE_ID + 79, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Overdrive Dome": ItemData(MINDUSTRY_BASE_ID + 80, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Repair Point": ItemData(MINDUSTRY_BASE_ID + 81, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    "Repair Turret": ItemData(MINDUSTRY_BASE_ID + 82, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    "Steam Generator": ItemData(MINDUSTRY_BASE_ID + 83, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Thermal Generator": ItemData(MINDUSTRY_BASE_ID + 84, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Differential Generator": ItemData(MINDUSTRY_BASE_ID + 85, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Thorium Reactor": ItemData(MINDUSTRY_BASE_ID + 86, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Impact Reactor": ItemData(MINDUSTRY_BASE_ID + 87, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "RTG Generator": ItemData(MINDUSTRY_BASE_ID + 88, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Solar Panel": ItemData(MINDUSTRY_BASE_ID + 89, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Large Solar Panel": ItemData(MINDUSTRY_BASE_ID + 90, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    #"Duo": ItemData(MINDUSTRY_BASE_ID + 91, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.TURRET, 1),
    #"Copper Wall": ItemData(MINDUSTRY_BASE_ID + 92, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.WALL, 1),
    "Large Copper Wall": ItemData(MINDUSTRY_BASE_ID + 93, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Titanium Wall": ItemData(MINDUSTRY_BASE_ID + 94, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Titanium Wall": ItemData(MINDUSTRY_BASE_ID + 95, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Door": ItemData(MINDUSTRY_BASE_ID + 96, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Door": ItemData(MINDUSTRY_BASE_ID + 97, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Plastanium Wall": ItemData(MINDUSTRY_BASE_ID + 98, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Plastanium Wall": ItemData(MINDUSTRY_BASE_ID + 99, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Thorium Wall": ItemData(MINDUSTRY_BASE_ID + 100, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Thorium Wall": ItemData(MINDUSTRY_BASE_ID + 101, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Surge Wall": ItemData(MINDUSTRY_BASE_ID + 102, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Surge Wall": ItemData(MINDUSTRY_BASE_ID + 103, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Phase Wall": ItemData(MINDUSTRY_BASE_ID + 104, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Phase Wall": ItemData(MINDUSTRY_BASE_ID + 105, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.WALL, 1),
    #"Scatter": ItemData(MINDUSTRY_BASE_ID + 106, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.TURRET, 1),
    "Hail": ItemData(MINDUSTRY_BASE_ID + 107, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Salvo": ItemData(MINDUSTRY_BASE_ID + 108, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Swarmer": ItemData(MINDUSTRY_BASE_ID + 109, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Cyclone": ItemData(MINDUSTRY_BASE_ID + 110, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Spectre": ItemData(MINDUSTRY_BASE_ID + 111, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Ripple": ItemData(MINDUSTRY_BASE_ID + 112, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Fuse": ItemData(MINDUSTRY_BASE_ID + 113, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Scorch": ItemData(MINDUSTRY_BASE_ID + 114, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Arc": ItemData(MINDUSTRY_BASE_ID + 115, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Wave": ItemData(MINDUSTRY_BASE_ID + 116, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Parallax": ItemData(MINDUSTRY_BASE_ID + 117, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Segment": ItemData(MINDUSTRY_BASE_ID + 118, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Tsunami": ItemData(MINDUSTRY_BASE_ID + 119, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Lancer": ItemData(MINDUSTRY_BASE_ID + 120, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Meltdown": ItemData(MINDUSTRY_BASE_ID + 121, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Foreshadow": ItemData(MINDUSTRY_BASE_ID + 122, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Shock Mine": ItemData(MINDUSTRY_BASE_ID + 123, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Ground Factory": ItemData(MINDUSTRY_BASE_ID + 124, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.FACTORY, 1),
    #"Dagger": ItemData(MINDUSTRY_BASE_ID + 125, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 1),
    "Progressive Offensive Ground Unit": ItemData(MINDUSTRY_BASE_ID + 126, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Progressive Support Ground Unit": ItemData(MINDUSTRY_BASE_ID + 127, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Progressive Insectoid Ground Unit": ItemData(MINDUSTRY_BASE_ID + 128, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Air Factory": ItemData(MINDUSTRY_BASE_ID + 129, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.FACTORY, 1),
    #"Flare": ItemData(MINDUSTRY_BASE_ID + 130, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 1),
    "Progressive Offensive Air Unit": ItemData(MINDUSTRY_BASE_ID + 131, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Progressive Support Air Unit": ItemData(MINDUSTRY_BASE_ID + 132, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Naval Factory": ItemData(MINDUSTRY_BASE_ID + 133, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.FACTORY, 1),
    #"Risso": ItemData(MINDUSTRY_BASE_ID + 134, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 1),
    "Progressive Offensive Naval Unit": ItemData(MINDUSTRY_BASE_ID + 135, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Progressive Support Naval Unit": ItemData(MINDUSTRY_BASE_ID + 136, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Progressive Reconstructor": ItemData(MINDUSTRY_BASE_ID + 137, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.FACTORY, 4),
    #"Frozen Forest": ItemData(MINDUSTRY_BASE_ID + 138, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"The Craters": ItemData(MINDUSTRY_BASE_ID + 139, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Ruinous Shores": ItemData(MINDUSTRY_BASE_ID + 140, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Windswept Islands": ItemData(MINDUSTRY_BASE_ID + 141, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Tar Fields": ItemData(MINDUSTRY_BASE_ID + 142, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Impact 0078": ItemData(MINDUSTRY_BASE_ID + 143, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Desolate Rift": ItemData(MINDUSTRY_BASE_ID + 144, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Planetary Launch Terminal": ItemData(MINDUSTRY_BASE_ID + 145, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Extraction Outpost": ItemData(MINDUSTRY_BASE_ID + 146, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Salt Flats": ItemData(MINDUSTRY_BASE_ID + 147, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Coastline": ItemData(MINDUSTRY_BASE_ID + 148, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Naval Fortress": ItemData(MINDUSTRY_BASE_ID + 149, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Overgrowth": ItemData(MINDUSTRY_BASE_ID + 150, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Biomass Synthesis Facility": ItemData(MINDUSTRY_BASE_ID + 151, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Stained Mountains": ItemData(MINDUSTRY_BASE_ID + 152, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Fungal Pass": ItemData(MINDUSTRY_BASE_ID + 153, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Nuclear Production Complex": ItemData(MINDUSTRY_BASE_ID + 154, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.SECTOR, 1),
    #"Lead": ItemData(MINDUSTRY_BASE_ID + 155, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Titanium": ItemData(MINDUSTRY_BASE_ID + 156, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Cryofluid": ItemData(MINDUSTRY_BASE_ID + 157, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Metaglass": ItemData(MINDUSTRY_BASE_ID + 158, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Scrap": ItemData(MINDUSTRY_BASE_ID + 159, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Slag": ItemData(MINDUSTRY_BASE_ID + 160, ItemPlanet.SERPULO, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Coal": ItemData(MINDUSTRY_BASE_ID + 161, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Graphite": ItemData(MINDUSTRY_BASE_ID + 162, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Silicon": ItemData(MINDUSTRY_BASE_ID + 163, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Pyratite": ItemData(MINDUSTRY_BASE_ID + 164, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Blast Compound": ItemData(MINDUSTRY_BASE_ID + 165, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Spore Pod": ItemData(MINDUSTRY_BASE_ID + 166, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Oil": ItemData(MINDUSTRY_BASE_ID + 167, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    #"Plastanium": ItemData(MINDUSTRY_BASE_ID + 168, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.RESSOURCES, 1),
    "Progressive Drills Serpulo": ItemData(MINDUSTRY_BASE_ID + 172, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.EXTRACTION, 3),
    "Progressive Generators Serpulo": ItemData(MINDUSTRY_BASE_ID + 173, ItemPlanet.SERPULO, ItemType.NECESSARY, ItemGroup.ENERGY, 7),


    #Erekir
    #"Duct": ItemData(MINDUSTRY_BASE_ID + 200, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.BELT, 1),
    "Duct Router": ItemData(MINDUSTRY_BASE_ID + 201, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Duct Bridge": ItemData(MINDUSTRY_BASE_ID + 202, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Armored Duct": ItemData(MINDUSTRY_BASE_ID + 203, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Surge Conveyor": ItemData(MINDUSTRY_BASE_ID + 204, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Surge Router": ItemData(MINDUSTRY_BASE_ID + 205, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Unit Cargo Loader": ItemData(MINDUSTRY_BASE_ID + 206, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Unit Cargo Unload Point": ItemData(MINDUSTRY_BASE_ID + 207, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Overflow Duct": ItemData(MINDUSTRY_BASE_ID + 208, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Underflow Duct": ItemData(MINDUSTRY_BASE_ID + 209, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Duct Unloader": ItemData(MINDUSTRY_BASE_ID + 210, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Reinforced Container": ItemData(MINDUSTRY_BASE_ID + 211, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.MISC, 1),
    "Reinforced Vault": ItemData(MINDUSTRY_BASE_ID + 212, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Reinforced Message": ItemData(MINDUSTRY_BASE_ID + 213, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.LOGIC, 1),
    "Canvas": ItemData(MINDUSTRY_BASE_ID + 214, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.LOGIC, 1),

    "Reinforced Payload Conveyor": ItemData(MINDUSTRY_BASE_ID + 215, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Payload Mass Driver": ItemData(MINDUSTRY_BASE_ID + 216, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.BELT, 1),
    "Payload Loader": ItemData(MINDUSTRY_BASE_ID + 217, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.BELT, 1),
    "Payload Unloader": ItemData(MINDUSTRY_BASE_ID + 218, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.BELT, 1),
    "Large Payload Mass Driver": ItemData(MINDUSTRY_BASE_ID + 219, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.BELT, 1),
    "Constructor": ItemData(MINDUSTRY_BASE_ID + 220, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    "Deconstructor": ItemData(MINDUSTRY_BASE_ID + 221, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    "Large Constructor": ItemData(MINDUSTRY_BASE_ID + 222, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    "Large Deconstructor": ItemData(MINDUSTRY_BASE_ID + 223, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    "Reinforced Payload Router": ItemData(MINDUSTRY_BASE_ID + 224, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),

    #"Plasma Bore": ItemData(MINDUSTRY_BASE_ID + 225, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.EXTRACTION, 1),
    "Impact Drill": ItemData(MINDUSTRY_BASE_ID + 226, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.EXTRACTION, 1),
    "Large Plasma Bore": ItemData(MINDUSTRY_BASE_ID + 227, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.EXTRACTION, 1),
    "Eruption Drill": ItemData(MINDUSTRY_BASE_ID + 228, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.EXTRACTION, 1),

    #"Turbine Condenser": ItemData(MINDUSTRY_BASE_ID + 229, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    #"Beam Node": ItemData(MINDUSTRY_BASE_ID + 230, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Vent Condenser": ItemData(MINDUSTRY_BASE_ID + 231, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Chemical Combustion Chamber": ItemData(MINDUSTRY_BASE_ID + 232, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.ENERGY, 1),
    "Pyrolysis Generator": ItemData(MINDUSTRY_BASE_ID + 233, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Flux Reactor": ItemData(MINDUSTRY_BASE_ID + 234, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Neoplasia Reactor": ItemData(MINDUSTRY_BASE_ID + 235, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.ENERGY, 1),
    "Beam Tower": ItemData(MINDUSTRY_BASE_ID + 236, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.ENERGY, 1),
    "Regen Projector": ItemData(MINDUSTRY_BASE_ID + 237, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Build Tower": ItemData(MINDUSTRY_BASE_ID + 238, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Shockwave Tower": ItemData(MINDUSTRY_BASE_ID + 239, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Reinforced Conduit": ItemData(MINDUSTRY_BASE_ID + 240, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.CONDUIT, 1),
    "Reinforced Pump": ItemData(MINDUSTRY_BASE_ID + 241, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.EXTRACTION, 1),
    "Reinforced Liquid Junction": ItemData(MINDUSTRY_BASE_ID + 242, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Reinforced Bridge Conduit": ItemData(MINDUSTRY_BASE_ID + 243, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Reinforced Liquid Router": ItemData(MINDUSTRY_BASE_ID + 244, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Reinforced Liquid Container": ItemData(MINDUSTRY_BASE_ID + 245, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    "Reinforced Liquid Tank": ItemData(MINDUSTRY_BASE_ID + 246, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.CONDUIT, 1),
    #"Cliff Crusher": ItemData(MINDUSTRY_BASE_ID + 247, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.EXTRACTION, 1),
    #"Silicon Arc Furnace": ItemData(MINDUSTRY_BASE_ID + 248, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Electrolyzer": ItemData(MINDUSTRY_BASE_ID + 249, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Oxidation Chamber": ItemData(MINDUSTRY_BASE_ID + 250, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Surge Crucible": ItemData(MINDUSTRY_BASE_ID + 251, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Heat Redirector": ItemData(MINDUSTRY_BASE_ID + 252, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Electric Heater": ItemData(MINDUSTRY_BASE_ID + 253, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Slag Heater": ItemData(MINDUSTRY_BASE_ID + 254, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Atmospheric Concentrator": ItemData(MINDUSTRY_BASE_ID + 255, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Cyanogen Synthesizer": ItemData(MINDUSTRY_BASE_ID + 256, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Carbide Crucible": ItemData(MINDUSTRY_BASE_ID + 257, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Phase Synthesizer": ItemData(MINDUSTRY_BASE_ID + 258, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.INDUSTRY, 1),
    "Phase Heater": ItemData(MINDUSTRY_BASE_ID + 259, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Heat Router": ItemData(MINDUSTRY_BASE_ID + 260, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),
    "Slag Incinerator": ItemData(MINDUSTRY_BASE_ID + 261, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.INDUSTRY, 1),

    #"Breach": ItemData(MINDUSTRY_BASE_ID + 262, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.TURRET, 1),
    #"Beryllium Wall": ItemData(MINDUSTRY_BASE_ID + 263, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Beryllium Wall": ItemData(MINDUSTRY_BASE_ID + 264, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Tungsten Wall": ItemData(MINDUSTRY_BASE_ID + 265, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Tungsten Wall": ItemData(MINDUSTRY_BASE_ID + 266, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Blast Door": ItemData(MINDUSTRY_BASE_ID + 267, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Reinforced Surge Wall": ItemData(MINDUSTRY_BASE_ID + 268, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Reinforced Surge Wall": ItemData(MINDUSTRY_BASE_ID + 269, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Shielded Wall": ItemData(MINDUSTRY_BASE_ID + 270, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Carbide Wall": ItemData(MINDUSTRY_BASE_ID + 271, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Large Carbide Wall": ItemData(MINDUSTRY_BASE_ID + 272, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.WALL, 1),
    "Diffuse": ItemData(MINDUSTRY_BASE_ID + 273, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Sublimate": ItemData(MINDUSTRY_BASE_ID + 274, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Afflict": ItemData(MINDUSTRY_BASE_ID + 275, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Titan": ItemData(MINDUSTRY_BASE_ID + 276, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Lustre": ItemData(MINDUSTRY_BASE_ID + 277, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Smite": ItemData(MINDUSTRY_BASE_ID + 278, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Disperse": ItemData(MINDUSTRY_BASE_ID + 279, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Scathe": ItemData(MINDUSTRY_BASE_ID + 280, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Malign": ItemData(MINDUSTRY_BASE_ID + 281, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),
    "Radar": ItemData(MINDUSTRY_BASE_ID + 282, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.TURRET, 1),

    "Core: Citadel": ItemData(MINDUSTRY_BASE_ID + 283, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.MISC, 1),
    "Core: Acropolis": ItemData(MINDUSTRY_BASE_ID + 284, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.MISC, 1),

    #"Tank Fabricator": ItemData(MINDUSTRY_BASE_ID + 285, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    #"Stell": ItemData(MINDUSTRY_BASE_ID + 286, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    "Unit Repair Tower": ItemData(MINDUSTRY_BASE_ID + 287, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    "Ship Fabricator": ItemData(MINDUSTRY_BASE_ID + 288, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.FACTORY, 1),
    #"Elude": ItemData(MINDUSTRY_BASE_ID + 289, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.UNIT, 1),
    "Mech Fabricator": ItemData(MINDUSTRY_BASE_ID + 290, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.FACTORY, 1),
    #"Merui": ItemData(MINDUSTRY_BASE_ID + 291, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.UNIT, 1),
    "Tank Refabricator": ItemData(MINDUSTRY_BASE_ID + 292, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.FACTORY, 1),
    #"Locus": ItemData(MINDUSTRY_BASE_ID + 293, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    "Mech Refrabricator": ItemData(MINDUSTRY_BASE_ID + 294, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.FACTORY, 1),
    #"Cleroi": ItemData(MINDUSTRY_BASE_ID + 295, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    "Ship Refabricator": ItemData(MINDUSTRY_BASE_ID + 296, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.FACTORY, 1),
    #"Avert": ItemData(MINDUSTRY_BASE_ID + 297, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    "Prime Refabricator": ItemData(MINDUSTRY_BASE_ID + 298, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    #"Precept": ItemData(MINDUSTRY_BASE_ID + 299, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    #"Anthicus": ItemData(MINDUSTRY_BASE_ID + 300, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    #"Obviate": ItemData(MINDUSTRY_BASE_ID + 301, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    "Tank Assembler": ItemData(MINDUSTRY_BASE_ID + 302, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    #"Vanquish": ItemData(MINDUSTRY_BASE_ID + 303, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    #"Conquer": ItemData(MINDUSTRY_BASE_ID + 304, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    "Ship Assembler": ItemData(MINDUSTRY_BASE_ID + 305, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    #"Quell": ItemData(MINDUSTRY_BASE_ID + 306, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    #"Disrupt": ItemData(MINDUSTRY_BASE_ID + 307, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    "Mech Assembler": ItemData(MINDUSTRY_BASE_ID + 308, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.FACTORY, 1),
    #"Tecta": ItemData(MINDUSTRY_BASE_ID + 309, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    #"Collaris": ItemData(MINDUSTRY_BASE_ID + 310, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),
    "Basic Assembler Module": ItemData(MINDUSTRY_BASE_ID + 311, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.UNIT, 1),

    #"Aegis": ItemData(MINDUSTRY_BASE_ID + 312, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Lake": ItemData(MINDUSTRY_BASE_ID + 313, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Intersect": ItemData(MINDUSTRY_BASE_ID + 314, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Atlas": ItemData(MINDUSTRY_BASE_ID + 315, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Split": ItemData(MINDUSTRY_BASE_ID + 316, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Basin": ItemData(MINDUSTRY_BASE_ID + 317, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Marsh": ItemData(MINDUSTRY_BASE_ID + 318, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Ravine": ItemData(MINDUSTRY_BASE_ID + 319, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Caldera": ItemData(MINDUSTRY_BASE_ID + 320, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Stronghold": ItemData(MINDUSTRY_BASE_ID + 321, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Crevice": ItemData(MINDUSTRY_BASE_ID + 322, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Siege": ItemData(MINDUSTRY_BASE_ID + 323, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Crossroads": ItemData(MINDUSTRY_BASE_ID + 324, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Karst": ItemData(MINDUSTRY_BASE_ID + 325, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Origin": ItemData(MINDUSTRY_BASE_ID + 326, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
    #"Peaks": ItemData(MINDUSTRY_BASE_ID + 327, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.SECTOR, 1),
#
    #"Oxide": ItemData(MINDUSTRY_BASE_ID + 328, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Ozone": ItemData(MINDUSTRY_BASE_ID + 329, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Hydrogen": ItemData(MINDUSTRY_BASE_ID + 330, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Nitrogen": ItemData(MINDUSTRY_BASE_ID + 331, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Cyanogen": ItemData(MINDUSTRY_BASE_ID + 332, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Neoplasm": ItemData(MINDUSTRY_BASE_ID + 333, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Tungsten": ItemData(MINDUSTRY_BASE_ID + 334, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Slag": ItemData(MINDUSTRY_BASE_ID + 335, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Arkycite": ItemData(MINDUSTRY_BASE_ID + 336, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Carbide": ItemData(MINDUSTRY_BASE_ID + 337, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Thorium Erekir": ItemData(MINDUSTRY_BASE_ID + 338, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Phase Fabric Erekir": ItemData(MINDUSTRY_BASE_ID + 339, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),
    #"Surge Alloy Erekir": ItemData(MINDUSTRY_BASE_ID + 340, ItemPlanet.EREKIR, ItemType.USEFUL, ItemGroup.RESSOURCES, 1),

    "Progressive Tanks": ItemData(MINDUSTRY_BASE_ID + 341, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.UNIT, 4),
    "Progressive Ships": ItemData(MINDUSTRY_BASE_ID + 342, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Progressive Mechs": ItemData(MINDUSTRY_BASE_ID + 343, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.UNIT, 5),
    "Progressive Drills Erekir": ItemData(MINDUSTRY_BASE_ID + 344, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.UNIT, 3),
    "Progressive Generators Erekir": ItemData(MINDUSTRY_BASE_ID + 345, ItemPlanet.EREKIR, ItemType.NECESSARY, ItemGroup.UNIT, 4),

    #Filler Items
    "A fistful of nothing...": ItemData(MINDUSTRY_BASE_ID + 700, ItemPlanet.ALL, ItemType.JUNK, ItemGroup.FILLER, 1)
}
