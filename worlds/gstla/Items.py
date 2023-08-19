from typing import List, NamedTuple, Dict, Optional
from enum import Enum, IntEnum
from BaseClasses import Item, ItemClassification, MultiWorld
from .Names.ItemName import ItemName
from .Names.LocationName import LocationName

class ElementType(IntEnum):
   Earth = 0
   Water = 1
   Fire = 2
   Air = 3

class ItemType(str, Enum):
   KeyItem = "key"
   Class = "class"
   Consumable = "consumables"
   Trade = "trade"
   Forgeable = "forgeable"
   Weapon = "weapon"
   Armor = "armor"
   Helm = "helm"
   Shield = "shield"
   Psyenergy = "psyenergy"
   PsyenergyItem = "psyenergy_item"
   Shirt = "shirt"
   Boots = "boots"
   Ring = "ring"
   Djinn = "djinn"
   Event = "event"



class ItemData(NamedTuple):
   ap_id: Optional[int]
   itemName: str
   progression: ItemClassification
   addr: int
   type: ItemType
   gstla_id: Optional[int]
   event_type: int = 131

class DjinItemData(ItemData):
    element: int
    stats_addr: int
    stats: List[int]

    def __new__(cls, ap_id, itemName, progression, addr, gstla_id, element, stats_addr, stats):
        self = super(ItemData, cls).__new__(cls, (ap_id, itemName, progression, addr, ItemType.Djinn, gstla_id, 1))
        self.element = element
        self.stats_addr = stats_addr
        self.stats = stats
        return self

class EventItemData(ItemData):
    location: str

    def __new__(cls, location, name):
        self = super(ItemData, cls).__new__(cls, (0, name, ItemClassification.progression, 0, ItemType.Event, 0, 0 ))
        self.location = location
        return self

class GSTLAItem(Item):
    game: str = "Golden Sun The Lost Age"

summon_list: List[ItemData] = [
    ItemData(400, ItemName.Moloch, ItemClassification.useful, 3859, ItemType.Psyenergy, 3859, 132),
    ItemData(401, ItemName.Daedalus, ItemClassification.useful, 3864, ItemType.Psyenergy, 3864, 132),
    ItemData(401, ItemName.Flora, ItemClassification.useful, 3858, ItemType.Psyenergy, 3858, 132),
    ItemData(401, ItemName.Ulysses, ItemClassification.useful, 3860, ItemType.Psyenergy, 3860, 132),
    ItemData(401, ItemName.Azul, ItemClassification.useful, 3865, ItemType.Psyenergy, 3865, 132),
    ItemData(401, ItemName.Zagan, ItemClassification.useful, 3856, ItemType.Psyenergy, 3856, 132),
    ItemData(401, ItemName.Megaera, ItemClassification.useful, 3857, ItemType.Psyenergy, 3857, 132),
    ItemData(401, ItemName.Haures, ItemClassification.useful, 3861, ItemType.Psyenergy, 3861, 132),
    ItemData(401, ItemName.Coatlicue, ItemClassification.useful, 3863, ItemType.Psyenergy, 3863, 132),
    ItemData(401, ItemName.Catastrophe, ItemClassification.useful, 3866, ItemType.Psyenergy, 3866, 132),
    ItemData(401, ItemName.Charon, ItemClassification.useful, 3867, ItemType.Psyenergy, 3867, 132),
    ItemData(401, ItemName.Iris, ItemClassification.useful, 3868, ItemType.Psyenergy, 3868, 132),
    ItemData(401, ItemName.Eclipse, ItemClassification.useful, 3862, ItemType.Psyenergy, 3862, 132)
]

psynergy_list: List[ItemData] = [
    ItemData(374, ItemName.Growth, ItemClassification.progression, 3596, ItemType.Psyenergy, 3596, 132),
    ItemData(375, ItemName.Whirlwind, ItemClassification.progression, 3662, ItemType.Psyenergy, 3662, 132),
    ItemData(376, ItemName.Parch, ItemClassification.progression, 3722, ItemType.Psyenergy, 3722, 132),
    ItemData(377, ItemName.Sand, ItemClassification.progression, 3723, ItemType.Psyenergy, 3723, 132),
    ItemData(378, ItemName.Mind_Read, ItemClassification.progression, 3725, ItemType.Psyenergy, 3725, 132),
    ItemData(379, ItemName.Reveal, ItemClassification.progression, 3728, ItemType.Psyenergy, 3728, 132),
    ItemData(380, ItemName.Blaze, ItemClassification.progression, 3738, ItemType.Psyenergy, 3738, 132)
]

psyenergy_as_item_list: List[ItemData] = [
   # ItemData(313, ItemName.Lash_Pebble, ItemClassification.progression, 738668, ItemType.PsyenergyItem, 738668, 1, 128),
   # ItemData(314, ItemName.Pound_Cube, ItemClassification.progression, 738712, ItemType.PsyenergyItem, 738712, 1, 128),
   # ItemData(315, ItemName.Orb_of_Force, ItemClassification.progression, 738756, ItemType.PsyenergyItem, 738756, 1, 128),
   # ItemData(316, ItemName.Douse_Drop, ItemClassification.progression, 738800, ItemType.PsyenergyItem, 738800, 1, 128),
   # ItemData(317, ItemName.Frost_Jewel, ItemClassification.progression, 738844, ItemType.PsyenergyItem, 738844, 1, 128),
   # ItemData(318, ItemName.Lifting_Gem, ItemClassification.progression, 738888, ItemType.PsyenergyItem, 738888, 1, 128),
   # ItemData(321, ItemName.Carry_Stone, ItemClassification.progression, 739020, ItemType.PsyenergyItem, 739020, 1, 128),
   # ItemData(322, ItemName.Catch_Beads, ItemClassification.progression, 739064, ItemType.PsyenergyItem, 739064, 1, 128),
   # ItemData(323, ItemName.Tremor_Bit, ItemClassification.progression, 739108, ItemType.PsyenergyItem, 739108, 1, 128),
   # ItemData(324, ItemName.Scoop_Gem, ItemClassification.progression, 739152, ItemType.PsyenergyItem, 739152, 1, 128),
   # ItemData(325, ItemName.Cyclone_Chip, ItemClassification.progression, 739196, ItemType.PsyenergyItem, 739196, 1, 128),
   # ItemData(326, ItemName.Burst_Brooch, ItemClassification.progression, 739328, ItemType.PsyenergyItem, 739328, 1, 128),
   # ItemData(327, ItemName.Grindstone, ItemClassification.progression, 739372, ItemType.PsyenergyItem, 739372, 1, 128),
   # ItemData(328, ItemName.Hover_Jade, ItemClassification.progression, 739416, ItemType.PsyenergyItem, 739416, 1, 128),
   # ItemData(329, ItemName.Teleport_Lapis, ItemClassification.progression, 739504, ItemType.PsyenergyItem, 739504, 1, 128)

    ItemData(313, ItemName.Lash_Pebble, ItemClassification.progression, 3717, ItemType.PsyenergyItem, 3717, 128),
    ItemData(314, ItemName.Pound_Cube, ItemClassification.progression, 3718, ItemType.PsyenergyItem, 3718, 128),
    ItemData(315, ItemName.Orb_of_Force, ItemClassification.progression, 3726, ItemType.PsyenergyItem, 3726, 128),
    ItemData(316, ItemName.Douse_Drop, ItemClassification.progression, 3617, ItemType.PsyenergyItem, 3617, 128),
    ItemData(317, ItemName.Frost_Jewel, ItemClassification.progression, 3608, ItemType.PsyenergyItem, 3608, 128),
    ItemData(318, ItemName.Lifting_Gem, ItemClassification.progression, 3727, ItemType.PsyenergyItem, 3727, 128),
    ItemData(321, ItemName.Carry_Stone, ItemClassification.progression, 3731, ItemType.PsyenergyItem, 3731, 128),
    ItemData(322, ItemName.Catch_Beads, ItemClassification.progression, 3732, ItemType.PsyenergyItem, 3732, 128),
    ItemData(323, ItemName.Tremor_Bit, ItemClassification.progression, 3719, ItemType.PsyenergyItem, 3719, 128),
    ItemData(324, ItemName.Scoop_Gem, ItemClassification.progression, 3720, ItemType.PsyenergyItem, 3720, 128),
    ItemData(325, ItemName.Cyclone_Chip, ItemClassification.progression, 3721, ItemType.PsyenergyItem, 3721, 128),
    ItemData(326, ItemName.Burst_Brooch, ItemClassification.progression, 3735, ItemType.PsyenergyItem, 3735, 131),
    ItemData(327, ItemName.Grindstone, ItemClassification.progression, 3736, ItemType.PsyenergyItem, 3736, 128),
    ItemData(328, ItemName.Hover_Jade, ItemClassification.progression, 3737, ItemType.PsyenergyItem, 3737, 128),
    ItemData(329, ItemName.Teleport_Lapis, ItemClassification.progression, 3740, ItemType.PsyenergyItem, 3740, 128)
]

base_djinn_index = 400

djinn_items: List[ItemData] =[
    DjinItemData(base_djinn_index, ItemName.Flint, ItemClassification.progression_skip_balancing, 16384000, 0, ElementType.Earth,
                814004, [8, 4, 3, 0, 0, 0]),
    DjinItemData(base_djinn_index + 1, ItemName.Granite, ItemClassification.progression_skip_balancing, 16384002, 1, ElementType.Earth,
                814016, [9, 0, 0, 2, 2, 1]),
    DjinItemData(base_djinn_index + 2, ItemName.Quartz, ItemClassification.progression_skip_balancing, 16384004, 2, ElementType.Earth,
                814028, [10, 3, 0, 0, 3, 0]),
    DjinItemData(base_djinn_index + 3, ItemName.Vine, ItemClassification.progression_skip_balancing, 16384006, 3, ElementType.Earth,
                814040, [12, 4, 0, 3, 0, 1]),
    DjinItemData(base_djinn_index + 4, ItemName.Sap, ItemClassification.progression_skip_balancing, 16384008, 4, ElementType.Earth,
                814052, [10, 0, 3, 0, 0, 1]),
    DjinItemData(base_djinn_index + 5, ItemName.Ground, ItemClassification.progression_skip_balancing, 16384010, 5, ElementType.Earth,
                814064, [9, 3, 0, 0, 3, 0]),
    DjinItemData(base_djinn_index + 6, ItemName.Bane, ItemClassification.progression_skip_balancing, 16384012, 6, ElementType.Earth,
                814076, [12, 0, 4, 0, 0, 0]),
    DjinItemData(base_djinn_index + 7, ItemName.Echo, ItemClassification.progression_skip_balancing, 16384014, 7, ElementType.Earth,
                814088, [9, 4, 3, 0, 0, 0]),
    DjinItemData(base_djinn_index + 8, ItemName.Iron, ItemClassification.progression_skip_balancing, 16384016, 8, ElementType.Earth,
                814100, [11, 0, 0, 2, 3, 0]),
    DjinItemData(base_djinn_index + 9, ItemName.Steel, ItemClassification.progression_skip_balancing, 16384018, 9, ElementType.Earth,
                814112, [9, 0, 4, 2, 0, 1]),
    DjinItemData(base_djinn_index + 10, ItemName.Mud, ItemClassification.progression_skip_balancing, 16384020, 10, ElementType.Earth,
                814124, [10, 4, 0, 0, 3, 0]),
    DjinItemData(base_djinn_index + 11, ItemName.Flower, ItemClassification.progression_skip_balancing, 16384022, 11, ElementType.Earth,
                814136, [12, 4, 0, 0, 0, 0]),
    DjinItemData(base_djinn_index + 12, ItemName.Meld, ItemClassification.progression_skip_balancing, 16384024, 12, ElementType.Earth,
                814148, [9, 0, 0, 0, 4, 1]),
    DjinItemData(base_djinn_index + 13, ItemName.Petra, ItemClassification.progression_skip_balancing, 16384026, 13, ElementType.Earth,
                814160, [11, 0, 0, 3, 0, 0]),
    DjinItemData(base_djinn_index + 14, ItemName.Salt, ItemClassification.progression_skip_balancing, 16384028, 14, ElementType.Earth,
                814172, [9, 5, 0, 0, 0, 1]),
    DjinItemData(base_djinn_index + 15, ItemName.Geode, ItemClassification.progression_skip_balancing, 16384030, 15, ElementType.Earth,
                814184, [12, 0, 6, 0, 0, 0]),
    DjinItemData(base_djinn_index + 16, ItemName.Mold, ItemClassification.progression_skip_balancing, 16384032, 16, ElementType.Earth,
                814196, [8, 0, 4, 0, 2, 1]),
    DjinItemData(base_djinn_index + 17, ItemName.Crystal, ItemClassification.progression_skip_balancing, 16384034, 17,
                ElementType.Earth, 814208, [10, 5, 0, 2, 0, 0]),

    DjinItemData(base_djinn_index + 18, ItemName.Fizz, ItemClassification.progression_skip_balancing, 16384036, 0, ElementType.Water,
                814328, [9, 4, 0, 3, 0, 0]),
    DjinItemData(base_djinn_index + 19, ItemName.Sleet, ItemClassification.progression_skip_balancing, 16384038, 1, ElementType.Water,
                814256, [12, 0, 3, 0, 0, 1]),
    DjinItemData(base_djinn_index + 20, ItemName.Mist, ItemClassification.progression_skip_balancing, 16384040, 2, ElementType.Water,
                814268, [11, 0, 4, 0, 0, 0]),
    DjinItemData(base_djinn_index + 21, ItemName.Spritz, ItemClassification.progression_skip_balancing, 16384042, 3, ElementType.Water,
                814280, [8, 4, 0, 0, 3, 0]),
    DjinItemData(base_djinn_index + 22, ItemName.Hail, ItemClassification.progression_skip_balancing, 16384044, 4, ElementType.Water,
                814292, [9, 0, 4, 0, 0, 1]),
    DjinItemData(base_djinn_index + 23, ItemName.Tonic, ItemClassification.progression_skip_balancing, 16384046, 5, ElementType.Water,
                814304, [8, 3, 0, 2, 0, 2]),
    DjinItemData(base_djinn_index + 24, ItemName.Dew, ItemClassification.progression_skip_balancing, 16384048, 6, ElementType.Water,
                814316, [13, 4, 0, 0, 4, 0]),
    DjinItemData(base_djinn_index + 25, ItemName.Fog, ItemClassification.progression_skip_balancing, 16384050, 7, ElementType.Water,
                814328, [9, 0, 0, 2, 2, 1]),
    DjinItemData(base_djinn_index + 26, ItemName.Sour, ItemClassification.progression_skip_balancing, 16384052, 8, ElementType.Water,
                814340, [8, 4, 3, 0, 0, 0]),
    DjinItemData(base_djinn_index + 27, ItemName.Spring, ItemClassification.progression_skip_balancing, 16384054, 9, ElementType.Water,
                814352, [11, 5, 0, 0, 0, 0]),
    DjinItemData(base_djinn_index + 28, ItemName.Shade, ItemClassification.progression_skip_balancing, 16384056, 10, ElementType.Water,
                814364, [9, 0, 0, 3, 0, 2]),
    DjinItemData(base_djinn_index + 29, ItemName.Chill, ItemClassification.progression_skip_balancing, 16384058, 11, ElementType.Water,
                814376, [10, 3, 0, 2, 0, 0]),
    DjinItemData(base_djinn_index + 30, ItemName.Steam, ItemClassification.progression_skip_balancing, 16384060, 12, ElementType.Water,
                814388, [10, 0, 5, 0, 0, 0]),
    DjinItemData(base_djinn_index + 31, ItemName.Rime, ItemClassification.progression_skip_balancing, 16384062, 13, ElementType.Water,
                814400, [10, 6, 0, 0, 0, 0]),
    DjinItemData(base_djinn_index + 32, ItemName.Gel, ItemClassification.progression_skip_balancing, 16384064, 14, ElementType.Water,
                814412, [9, 0, 5, 0, 2, 0]),
    DjinItemData(base_djinn_index + 33, ItemName.Eddy, ItemClassification.progression_skip_balancing, 16384066, 15, ElementType.Water,
                814424, [9, 0, 0, 0, 3, 2]),
    DjinItemData(base_djinn_index + 34, ItemName.Balm, ItemClassification.progression_skip_balancing, 16384068, 16, ElementType.Water,
                814436, [13, 4, 0, 0, 0, 2]),
    DjinItemData(base_djinn_index + 35, ItemName.Serac, ItemClassification.progression_skip_balancing, 16384070, 17, ElementType.Water,
                814448, [12, 0, 3, 0, 0, 0]),

    DjinItemData(base_djinn_index + 36, ItemName.Forge, ItemClassification.progression_skip_balancing, 16384072, 0, ElementType.Fire,
                814484, [10, 0, 2, 0, 2, 2]),
    DjinItemData(base_djinn_index + 37, ItemName.Fever, ItemClassification.progression_skip_balancing, 16384074, 1, ElementType.Fire,
                814496, [8, 0, 3, 0, 2, 0]),
    DjinItemData(base_djinn_index + 38, ItemName.Corona, ItemClassification.progression_skip_balancing, 16384076, 2, ElementType.Fire,
                814508, [12, 3, 0, 3, 0, 1]),
    DjinItemData(base_djinn_index + 39, ItemName.Scorch, ItemClassification.progression_skip_balancing, 16384078, 3, ElementType.Fire,
                814520, [8, 0, 3, 0, 0, 0]),
    DjinItemData(base_djinn_index + 40, ItemName.Ember, ItemClassification.progression_skip_balancing, 16384080, 4, ElementType.Fire,
                814532, [9, 4, 0, 2, 2, 0]),
    DjinItemData(base_djinn_index + 41, ItemName.Flash, ItemClassification.progression_skip_balancing, 16384082, 5, ElementType.Fire,
                814544, [14, 3, 0, 2, 0, 0]),
    DjinItemData(base_djinn_index + 42, ItemName.Torch, ItemClassification.progression_skip_balancing, 16384084, 6, ElementType.Fire,
                814556, [9, 0, 3, 0, 0, 1]),
    DjinItemData(base_djinn_index + 43, ItemName.Cannon, ItemClassification.progression_skip_balancing, 16384086, 7, ElementType.Fire,
                814568, [10, 0, 3, 0, 0, 0]),
    DjinItemData(base_djinn_index + 44, ItemName.Spark, ItemClassification.progression_skip_balancing, 16384088, 8, ElementType.Fire,
                814580, [11, 6, 0, 0, 0, 0]),
    DjinItemData(base_djinn_index + 45, ItemName.Kindle, ItemClassification.progression_skip_balancing, 16384090, 9, ElementType.Fire,
                814592, [8, 0, 5, 0, 0, 1]),
    DjinItemData(base_djinn_index + 46, ItemName.Char, ItemClassification.progression_skip_balancing, 16384092, 10, ElementType.Fire,
                814604, [9, 0, 2, 0, 2, 1]),
    DjinItemData(base_djinn_index + 47, ItemName.Coal, ItemClassification.progression_skip_balancing, 16384094, 11, ElementType.Fire,
                814616, [11, 3, 0, 0, 3, 0]),
    DjinItemData(base_djinn_index + 48, ItemName.Reflux, ItemClassification.progression_skip_balancing, 16384096, 12, ElementType.Fire,
                814628, [9, 0, 0, 3, 0, 2]),
    DjinItemData(base_djinn_index + 49, ItemName.Core, ItemClassification.progression_skip_balancing, 16384098, 13, ElementType.Fire,
                814640, [8, 0, 4, 2, 0, 0]),
    DjinItemData(base_djinn_index + 50, ItemName.Tinder, ItemClassification.progression_skip_balancing, 16384100, 14, ElementType.Fire,
                814652, [12, 5, 0, 0, 0, 0]),
    DjinItemData(base_djinn_index + 51, ItemName.Shine, ItemClassification.progression_skip_balancing, 16384102, 15, ElementType.Fire,
                814664, [9, 0, 3, 3, 2, 0]),
    DjinItemData(base_djinn_index + 52, ItemName.Fury, ItemClassification.progression_skip_balancing, 16384104, 16, ElementType.Fire,
                814676, [12, 4, 0, 0, 0, 0]),
    DjinItemData(base_djinn_index + 53, ItemName.Fugue, ItemClassification.progression_skip_balancing, 16384106, 17, ElementType.Fire,
                814688, [11, 4, 0, 2, 0, 0]),

    DjinItemData(base_djinn_index + 54, ItemName.Gust, ItemClassification.progression_skip_balancing, 16384108, 0, ElementType.Air,
                814724, [9, 0, 2, 0, 2, 0]),
    DjinItemData(base_djinn_index + 55, ItemName.Breeze, ItemClassification.progression_skip_balancing, 16384110, 1, ElementType.Air,
                814736, [12, 5, 0, 2, 0, 1]),
    DjinItemData(base_djinn_index + 56, ItemName.Zephyr, ItemClassification.progression_skip_balancing, 16384112, 2, ElementType.Air,
                814748, [11, 3, 0, 0, 2, 1]),
    DjinItemData(base_djinn_index + 57, ItemName.Smog, ItemClassification.progression_skip_balancing, 16384114, 3, ElementType.Air,
                814760, [9, 0, 3, 0, 0, 0]),
    DjinItemData(base_djinn_index + 58, ItemName.Kite, ItemClassification.progression_skip_balancing, 16384116, 4, ElementType.Air,
                814772, [8, 4, 0, 0, 3, 0]),
    DjinItemData(base_djinn_index + 59, ItemName.Squall, ItemClassification.progression_skip_balancing, 16384118, 5, ElementType.Air,
                814784, [10, 0, 5, 0, 0, 0]),
    DjinItemData(base_djinn_index + 60, ItemName.Luff, ItemClassification.progression_skip_balancing, 16384120, 6, ElementType.Air,
                814796, [11, 5, 0, 2, 0, 1]),
    DjinItemData(base_djinn_index + 61, ItemName.Breath, ItemClassification.progression_skip_balancing, 16384122, 7, ElementType.Air,
                814808, [9, 0, 0, 3, 4, 0]),
    DjinItemData(base_djinn_index + 62, ItemName.Blitz, ItemClassification.progression_skip_balancing, 16384124, 8, ElementType.Air,
                814820, [10, 4, 3, 0, 0, 0]),
    DjinItemData(base_djinn_index + 63, ItemName.Ether, ItemClassification.progression_skip_balancing, 16384126, 9, ElementType.Air,
                814832, [8, 4, 0, 0, 3, 2]),
    DjinItemData(base_djinn_index + 64, ItemName.Waft, ItemClassification.progression_skip_balancing, 16384128, 10, ElementType.Air,
                814844, [11, 0, 4, 0, 0, 0]),
    DjinItemData(base_djinn_index + 65, ItemName.Haze, ItemClassification.progression_skip_balancing, 16384130, 11, ElementType.Air,
                814856, [10, 0, 0, 2, 3, 2]),
    DjinItemData(base_djinn_index + 66, ItemName.Wheeze, ItemClassification.progression_skip_balancing, 16384132, 12, ElementType.Air,
                814868, [9, 3, 5, 0, 0, 0]),
    DjinItemData(base_djinn_index + 67, ItemName.Aroma, ItemClassification.progression_skip_balancing, 16384134, 13, ElementType.Air,
                814880, [11, 0, 0, 0, 3, 2]),
    DjinItemData(base_djinn_index + 68, ItemName.Whorl, ItemClassification.progression_skip_balancing, 16384136, 14, ElementType.Air,
                814892, [9, 0, 4, 2, 0, 0]),
    DjinItemData(base_djinn_index + 69, ItemName.Gasp, ItemClassification.progression_skip_balancing, 16384138, 15, ElementType.Air,
                814904, [12, 5, 0, 0, 0, 0]),
    DjinItemData(base_djinn_index + 70, ItemName.Lull, ItemClassification.progression_skip_balancing, 16384140, 16, ElementType.Air,
                814916, [11, 6, 0, 0, 0, 0]),
    DjinItemData(base_djinn_index + 71, ItemName.Gale, ItemClassification.progression_skip_balancing, 16384142, 17, ElementType.Air,
                814928, [10, 0, 0, 0, 5, 3])
]

unique_items: List[ItemData] = [
    ItemData(58, ItemName.Shamans_Rod, ItemClassification.progression, 732816, ItemType.KeyItem, 65, 128),
    ItemData(61, ItemName.Sea_Gods_Tear, ItemClassification.progression, 750108, ItemType.KeyItem, 458, 128),
    ItemData(50, ItemName.Right_Prong, ItemClassification.progression, 749272, ItemType.KeyItem, 439, 131),
    ItemData(58, ItemName.Healing_Fungus, ItemClassification.progression, 749668, ItemType.KeyItem, 448, 131),
    ItemData(58, ItemName.Black_Crystal, ItemClassification.progression, 740604, ItemType.KeyItem, 242, 128),
    ItemData(58, ItemName.Pretty_Stone, ItemClassification.progression, 749844, ItemType.Trade, 452, 128),
    ItemData(58, ItemName.Red_Cloth, ItemClassification.progression, 749888, ItemType.Trade, 453, 128),
    ItemData(58, ItemName.Milk, ItemClassification.progression, 749932, ItemType.Trade, 454, 128),
    ItemData(58, ItemName.Lil_Turtle, ItemClassification.progression, 749976, ItemType.Trade, 455, 128),
    ItemData(58, ItemName.Aquarius_Stone, ItemClassification.progression, 750020, ItemType.KeyItem, 456, 128),
    ItemData(58, ItemName.Left_Prong, ItemClassification.progression, 749316, ItemType.KeyItem, 440, 131),
    ItemData(58, ItemName.Dancing_Idol, ItemClassification.progression, 749800, ItemType.KeyItem, 451, 131),
    ItemData(58, ItemName.Center_Prong, ItemClassification.progression, 749360, ItemType.KeyItem, 441, 128),
    ItemData(58, ItemName.Magma_Ball, ItemClassification.progression, 750196, ItemType.KeyItem, 460, 128),
    ItemData(58, ItemName.Trident, ItemClassification.progression, 744300, ItemType.KeyItem, 326, 128),
    ItemData(58, ItemName.Blue_Key, ItemClassification.progression, 740692, ItemType.KeyItem, 244, 131),
    ItemData(58, ItemName.Red_Key, ItemClassification.progression, 740648, ItemType.KeyItem, 243, 131),
    ItemData(58, ItemName.Mars_Star, ItemClassification.progression, 739724, ItemType.KeyItem, 222, 128),
    ItemData(62, ItemName.Ruin_Key, ItemClassification.progression, 750152, ItemType.KeyItem, 459, 128),
    ItemData(371, ItemName.Mysterious_Card, ItemClassification.useful, 749448, ItemType.Class, 443, 128),
    ItemData(54, ItemName.Trainers_Whip, ItemClassification.useful, 749492, ItemType.Class, 444, 128),
    ItemData(58, ItemName.Tomegathericon, ItemClassification.useful, 749536, ItemType.Class, 445, 131),
    ItemData(58, ItemName.Laughing_Fungus, ItemClassification.filler, 749712, ItemType.KeyItem, 449, 131),
    ItemData(58, ItemName.Ixion_Mail, ItemClassification.useful, 744608, ItemType.Armor, 333, 128),
    ItemData(58, ItemName.Hypnos_Sword, ItemClassification.useful, 742716, ItemType.Weapon, 290, 128),
    ItemData(58, ItemName.Clarity_Circlet, ItemClassification.useful, 747292, ItemType.Helm, 394, 128),
    ItemData(58, ItemName.Fujin_Shield, ItemClassification.useful, 745708, ItemType.Shield, 358, 128),
    ItemData(58, ItemName.Storm_Brand, ItemClassification.useful, 742232, ItemType.Weapon, 279, 128),
    ItemData(58, ItemName.Bone, ItemClassification.filler, 740120, ItemType.KeyItem, 231, 128),
]

gear: List[ItemData] = [
    ItemData(51, ItemName.Rusty_Staff_Dracomace, ItemClassification.useful, 748656, ItemType.Forgeable, 425, 128),
    ItemData(51, ItemName.Rusty_Staff_GlowerStaff, ItemClassification.useful, 748700, ItemType.Forgeable, 426, 128),
    ItemData(51, ItemName.Rusty_Staff_GoblinsRod, ItemClassification.useful, 748744, ItemType.Forgeable, 427, 133),
    ItemData(58, ItemName.Rusty_Sword_CorsairsEdge, ItemClassification.useful, 748304, ItemType.Forgeable, 417, 131),
    ItemData(58, ItemName.Rusty_Sword_RobbersBlade, ItemClassification.useful, 748348, ItemType.Forgeable, 418, 128),
    ItemData(58, ItemName.Rusty_Sword_PiratesSabre, ItemClassification.useful, 748392, ItemType.Forgeable, 419, 133),
    ItemData(58, ItemName.Rusty_Sword_SoulBrand, ItemClassification.useful, 748436, ItemType.Forgeable, 420, 133),
    ItemData(58, ItemName.Rusty_Mace_HagboneMace, ItemClassification.useful, 748612, ItemType.Forgeable, 424, 133),
    ItemData(58, ItemName.Rusty_Mace_DemonMace, ItemClassification.useful, 748568, ItemType.Forgeable, 423, 128),
    ItemData(58, ItemName.Rusty_Axe_VikingAxe, ItemClassification.useful, 748524, ItemType.Forgeable, 422, 128),
    ItemData(58, ItemName.Rusty_Axe_CaptainsAxe, ItemClassification.useful, 748480, ItemType.Forgeable, 421, 133),

    ItemData(142, ItemName.Themis_Axe, ItemClassification.useful, 743200, ItemType.Weapon, 301, 128),
    ItemData(218, ItemName.Full_Metal_Vest, ItemClassification.useful, 744916, ItemType.Armor, 340, 128),
    ItemData(300, ItemName.Nurses_Cap, ItemClassification.useful, 746808, ItemType.Helm, 383, 128),
    ItemData(52, ItemName.Pirates_Sword, ItemClassification.useful, 742584, ItemType.Weapon, 287, 128),
    ItemData(53, ItemName.Guardian_Ring, ItemClassification.useful, 748172, ItemType.Ring, 414, 128),
    ItemData(55, ItemName.Blow_Mace, ItemClassification.useful, 743552, ItemType.Weapon, 309, 128),
    ItemData(58, ItemName.Thorn_Crown, ItemClassification.useful, 992684, ItemType.Helm, 384, 128),
    ItemData(58, ItemName.Unicorn_Ring, ItemClassification.useful, 992692, ItemType.Ring, 266, 128),
    ItemData(58, ItemName.Disk_Axe, ItemClassification.useful, 743156, ItemType.Weapon, 300, 128),
    ItemData(58, ItemName.Bone_Armlet, ItemClassification.useful, 746236, ItemType.Shield, 242, 128),
    ItemData(58, ItemName.Turtle_Boots, ItemClassification.useful, 741352, ItemType.Boots, 259, 128),
    ItemData(58, ItemName.Mist_Sabre, ItemClassification.useful, 742760, ItemType.Weapon, 291, 128),
    ItemData(58, ItemName.Festival_Coat, ItemClassification.useful, 745048, ItemType.Armor, 343, 13),
    ItemData(58, ItemName.Phantasmal_Mail, ItemClassification.useful, 744652, ItemType.Armor, 334, 128),
    ItemData(58, ItemName.Cloud_Brand, ItemClassification.useful, 742408, ItemType.Weapon, 283, 131),
    ItemData(58, ItemName.Iris_Robe, ItemClassification.useful, 745400, ItemType.Armor, 351, 128),
    ItemData(58, ItemName.Fire_Brand, ItemClassification.useful, 730264, ItemType.Weapon, 7, 128),
    ItemData(58, ItemName.Jesters_Armlet, ItemClassification.useful, 746280, ItemType.Shield, 371, 128),
    ItemData(58, ItemName.Lightning_Sword, ItemClassification.useful, 742320, ItemType.Weapon, 281, 128),
    ItemData(58, ItemName.Muni_Robe, ItemClassification.useful, 745312, ItemType.Armor, 349, 128),
    ItemData(58, ItemName.Thanatos_Mace, ItemClassification.useful, 743640, ItemType.Weapon, 311, 128),
    ItemData(58, ItemName.Viking_Helm, ItemClassification.useful, 746588, ItemType.Helm, 378, 128),
    ItemData(58, ItemName.Masamune, ItemClassification.useful, 731100, ItemType.Weapon, 26, 128),
    ItemData(58, ItemName.Spirit_Gloves, ItemClassification.useful, 746060, ItemType.Shield, 366, 128),
    ItemData(58, ItemName.Erinyes_Tunic, ItemClassification.useful, 745092, ItemType.Armor, 344, 128),
    ItemData(58, ItemName.Meditation_Rod, ItemClassification.useful, 743992, ItemType.Weapon, 319, 128),
    ItemData(58, ItemName.Phaetons_Blade, ItemClassification.useful, 742804, ItemType.Weapon, 292, 128),
    ItemData(58, ItemName.Alastors_Hood, ItemClassification.useful, 747028, ItemType.Helm, 388, 128),
    ItemData(58, ItemName.Sol_Blade, ItemClassification.useful, 730396, ItemType.Weapon, 10, 128),
    ItemData(58, ItemName.Valkyrie_Mail, ItemClassification.useful, 744740, ItemType.Armor, 336, 128)
]

test_items: List[ItemData] = [
    ItemData(2, ItemName.Herb, ItemClassification.filler, 737876, ItemType.Consumable, 180, 2),
    ItemData(20, ItemName.Smoke_Bomb, ItemClassification.filler, 739900, ItemType.Consumable, 226, 3),
    ItemData(21, ItemName.Sleep_Bomb, ItemClassification.filler, 739944, ItemType.Consumable, 227, 3),
    ItemData(8, ItemName.Psy_Crystal, ItemClassification.useful, 738140, ItemType.Consumable, 186, 131),
    ItemData(3, ItemName.Nut, ItemClassification.filler, 737920, ItemType.Consumable, 181, 128),
    ItemData(10, ItemName.Elixir, ItemClassification.filler, 738228, ItemType.Consumable, 188, 128),
    ItemData(17, ItemName.Mint, ItemClassification.useful, 738536, ItemType.Consumable, 195, 128),
    ItemData(9, ItemName.Antidote, ItemClassification.filler, 738184, ItemType.Consumable, 187, 128),
    ItemData(15, ItemName.Apple, ItemClassification.useful, 738448, ItemType.Consumable, 193, 128),
    ItemData(23, ItemName.Lucky_Medal, ItemClassification.filler, 740032, ItemType.Consumable, 229, 128),
    ItemData(12, ItemName.Mist_Potion, ItemClassification.useful, 738316, ItemType.Consumable, 190, 128),
    ItemData(56, ItemName.Hard_Nut, ItemClassification.useful, 738492, ItemType.Consumable, 194, 128),
    ItemData(57, ItemName.Apple, ItemClassification.useful, 738448, ItemType.Consumable, 193, 2),
    ItemData(58, ItemName.Power_Bread, ItemClassification.useful, 738360, ItemType.Consumable, 191, 128),
    ItemData(58, ItemName.Potion, ItemClassification.useful, 742496, ItemType.Consumable, 183, 128),
    ItemData(58, ItemName.Cookie, ItemClassification.useful, 738404, ItemType.Consumable, 192, 128),
    ItemData(58, ItemName.Vial, ItemClassification.filler, 737964, ItemType.Consumable, 182, 128),
    ItemData(58, ItemName.Tear_Stone, ItemClassification.useful, 748832, ItemType.Forgeable, 429, 128),
    ItemData(58, ItemName.Lucky_Pepper, ItemClassification.useful, 738580, ItemType.Consumable, 196, 2),
    ItemData(58, ItemName.Water_of_Life, ItemClassification.useful, 738272, ItemType.Consumable, 189, 128),
    ItemData(58, ItemName.Orihalcon, ItemClassification.useful, 749184, ItemType.Forgeable, 437, 128),
    ItemData(58, ItemName.Mythril_Silver, ItemClassification.useful, 749096, ItemType.Forgeable, 435, 128),
    ItemData(58, ItemName.Dark_Matter, ItemClassification.useful, 749140, ItemType.Forgeable, 436, 128),
    ItemData(58, ItemName.Bramble_Seed, ItemClassification.filler, 740516, ItemType.Consumable, 240, 131),
    ItemData(58, ItemName.Oil_Drop, ItemClassification.filler, 740428, ItemType.Consumable, 238, 128),
    ItemData(58, ItemName.Crystal_Powder, ItemClassification.filler, 740560, ItemType.Consumable, 241, 128),
    ItemData(58, ItemName.Star_Dust, ItemClassification.useful, 748876, ItemType.Forgeable, 430, 128),
    ItemData(58, ItemName.Sylph_Feather, ItemClassification.useful, 748920, ItemType.Forgeable, 431, 128),
    ItemData(58, ItemName.Dragon_Skin, ItemClassification.useful, 748964, ItemType.Forgeable, 432, 128),
    ItemData(58, ItemName.Weasels_Claw, ItemClassification.filler, 740472, ItemType.Consumable, 239, 3),
    ItemData(58, ItemName.Corn, ItemClassification.filler, 740208, ItemType.Consumable, 233, 3),
    ItemData(58, ItemName.Golem_Core, ItemClassification.useful, 749052, ItemType.Forgeable, 434, 128),
    ItemData(58, ItemName.Salamander_Tail, ItemClassification.useful, 749008, ItemType.Forgeable, 433, 128),
    ItemData(58, ItemName.Sacred_Feather, ItemClassification.filler, 740340, ItemType.Consumable, 236, 128),
]

events: List[EventItemData] = [
   EventItemData(LocationName.Lemurian_Ship_Engine, ItemName.Ship),
   EventItemData(LocationName.Mars_Lighthouse_Doom_Dragon, ItemName.Victory),
   EventItemData(LocationName.Gabombo_Statue, ItemName.Gabombo_Statue_Completed),
   EventItemData(LocationName.Gaia_Rock_Serpent, ItemName.Serpent_defeated),
   EventItemData(LocationName.SeaOfTime_Poseidon, ItemName.Poseidon_defeated),
   EventItemData(LocationName.Lemurian_Ship_Aqua_Hydra, ItemName.Aqua_Hydra_defeated),
   EventItemData(LocationName.Shaman_Village_Moapa, ItemName.Moapa_defeated),
   EventItemData(LocationName.Jupiter_Lighthouse_Aeri_Agatio_and_Karst, ItemName.Jupiter_Beacon_Lit),
   EventItemData(LocationName.Mars_Lighthouse_Flame_Dragons, ItemName.Flamedragons_defeated),
   EventItemData(LocationName.Alhafra_Briggs, ItemName.Briggs_defeated),
   EventItemData(LocationName.Alhafra_Prison_Briggs, ItemName.Briggs_escaped)
]

all_items: List[ItemData] = test_items + djinn_items + psyenergy_as_item_list + psynergy_list + summon_list + events + unique_items + gear
item_table: Dict[str, ItemData] = {item.itemName: item for item in all_items}
items_by_id: Dict[int, ItemData] = {item.ap_id: item for item in all_items}
pre_fillitems: List[Item] = []


def create_item(name: str, player :int) -> "Item":
    item = item_table[name]
    return GSTLAItem(item.itemName, item.progression, item.ap_id, player)


def create_events(multiworld: MultiWorld, player: int):
    for event in events:
        event_item = create_item(event.itemName, player)

        if event.location == LocationName.Lemurian_Ship_Engine and multiworld.starter_ship[player] == 0:
            multiworld.push_precollected(event_item)
            continue

        event_location = multiworld.get_location(event.location, player)
        event_location.place_locked_item(event_item)

def create_items(multiworld: MultiWorld, player: int):
    if multiworld.starter_ship[player] == 2:
        ap_location = multiworld.get_location(LocationName.Gabomba_Statue_Black_Crystal, player)
        ap_item = create_item(ItemName.Black_Crystal, player)
        ap_location.place_locked_item(ap_item)

    sum_locations = len(multiworld.get_unfilled_locations(player))

    for item in unique_items + psyenergy_as_item_list + psynergy_list:
        if multiworld.starter_ship[player] != 2 and item.itemName == ItemName.Black_Crystal:
            continue

        ap_item = create_item(item.itemName, player)
        multiworld.itempool.append(ap_item)
        sum_locations -= 1

    for item in djinn_items:
        ap_item = create_item(item.itemName, player)
        pre_fillitems.append(ap_item)
        sum_locations -= 1

    for item in gear + summon_list:
        ap_item = create_item(item.itemName, player)
        multiworld.itempool.append(ap_item)
        sum_locations -= 1

    for item in multiworld.random.choices(population=test_items, k=sum_locations):
        ap_item = create_item(item.itemName, player)
        multiworld.itempool.append(ap_item)

