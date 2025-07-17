# This file was generated using jinja2 from a template. If this file needs
# to be changed, either change the template, or the code leveraging the template.
from typing import Callable, List, Dict, NamedTuple, Optional
from enum import Enum, IntFlag, auto
from BaseClasses import MultiWorld
from .LocationNames import loc_names_by_id

class LocationType(str, Enum):
   Item = "Item"
   Event = "Event"
   Djinn = "Djinn"
   Psyenergy = "Psyenergy"
   Hidden = "Hidden"
   Trade = "Trade"
   Character = "Character"

def always_on(multiworld: MultiWorld, player: int) -> bool:
    return True

class LocationRestriction(IntFlag):
    NONE = 0
    NoEmpty = auto()
    NoMimic = auto()
    NoSummon = auto()
    NoMoney = auto()

class InternalLocationData(NamedTuple):
    rando_flag: int
    flag: int
    id: Optional[int]
    ap_id: int
    addresses: List[int]
    event_type: int
    vanilla_contents: int
    is_key: bool
    is_major: bool
    loc_type: LocationType = LocationType.Item
    restrictions: LocationRestriction = 0
    event: bool = False
    included: Callable[[MultiWorld, int], bool] = always_on

djinn_locations = [
InternalLocationData(48, 48, 16384000, 16384000,
        [16384000], 128, 0, True, True, LocationType.Djinn), # Flint
InternalLocationData(49, 49, 16384002, 16384002,
        [16384002], 128, 1, True, True, LocationType.Djinn), # Granite
InternalLocationData(50, 50, 16384004, 16384004,
        [16384004], 128, 2, True, True, LocationType.Djinn), # Quartz
InternalLocationData(51, 51, 16384006, 16384006,
        [16384006], 128, 3, True, True, LocationType.Djinn), # Vine
InternalLocationData(52, 52, 16384008, 16384008,
        [16384008], 128, 4, True, True, LocationType.Djinn), # Sap
InternalLocationData(53, 53, 16384010, 16384010,
        [16384010], 128, 5, True, True, LocationType.Djinn), # Ground
InternalLocationData(54, 54, 16384012, 16384012,
        [16384012], 128, 6, True, True, LocationType.Djinn), # Bane
InternalLocationData(55, 55, 16384014, 16384014,
        [16384014], 128, 7, True, True, LocationType.Djinn), # Echo
InternalLocationData(56, 56, 16384016, 16384016,
        [16384016], 128, 8, True, True, LocationType.Djinn), # Iron
InternalLocationData(57, 57, 16384018, 16384018,
        [16384018], 128, 9, True, True, LocationType.Djinn), # Steel
InternalLocationData(58, 58, 16384020, 16384020,
        [16384020], 128, 10, True, True, LocationType.Djinn), # Mud
InternalLocationData(59, 59, 16384022, 16384022,
        [16384022], 128, 11, True, True, LocationType.Djinn), # Flower
InternalLocationData(60, 60, 16384024, 16384024,
        [16384024], 128, 12, True, True, LocationType.Djinn), # Meld
InternalLocationData(61, 61, 16384026, 16384026,
        [16384026], 128, 13, True, True, LocationType.Djinn), # Petra
InternalLocationData(62, 62, 16384028, 16384028,
        [16384028], 128, 14, True, True, LocationType.Djinn), # Salt
InternalLocationData(63, 63, 16384030, 16384030,
        [16384030], 128, 15, True, True, LocationType.Djinn), # Geode
InternalLocationData(64, 64, 16384032, 16384032,
        [16384032], 128, 16, True, True, LocationType.Djinn), # Mold
InternalLocationData(65, 65, 16384034, 16384034,
        [16384034], 128, 17, True, True, LocationType.Djinn), # Crystal
InternalLocationData(68, 68, 16384036, 16384036,
        [16384036], 128, 0, True, True, LocationType.Djinn), # Fizz
InternalLocationData(69, 69, 16384038, 16384038,
        [16384038], 128, 1, True, True, LocationType.Djinn), # Sleet
InternalLocationData(70, 70, 16384040, 16384040,
        [16384040], 128, 2, True, True, LocationType.Djinn), # Mist
InternalLocationData(71, 71, 16384042, 16384042,
        [16384042], 128, 3, True, True, LocationType.Djinn), # Spritz
InternalLocationData(72, 72, 16384044, 16384044,
        [16384044], 128, 4, True, True, LocationType.Djinn), # Hail
InternalLocationData(73, 73, 16384046, 16384046,
        [16384046], 128, 5, True, True, LocationType.Djinn), # Tonic
InternalLocationData(74, 74, 16384048, 16384048,
        [16384048], 128, 6, True, True, LocationType.Djinn), # Dew
InternalLocationData(75, 75, 16384050, 16384050,
        [16384050], 128, 7, True, True, LocationType.Djinn), # Fog
InternalLocationData(76, 76, 16384052, 16384052,
        [16384052], 128, 8, True, True, LocationType.Djinn), # Sour
InternalLocationData(77, 77, 16384054, 16384054,
        [16384054], 128, 9, True, True, LocationType.Djinn), # Spring
InternalLocationData(78, 78, 16384056, 16384056,
        [16384056], 128, 10, True, True, LocationType.Djinn), # Shade
InternalLocationData(79, 79, 16384058, 16384058,
        [16384058], 128, 11, True, True, LocationType.Djinn), # Chill
InternalLocationData(80, 80, 16384060, 16384060,
        [16384060], 128, 12, True, True, LocationType.Djinn), # Steam
InternalLocationData(81, 81, 16384062, 16384062,
        [16384062], 128, 13, True, True, LocationType.Djinn), # Rime
InternalLocationData(82, 82, 16384064, 16384064,
        [16384064], 128, 14, True, True, LocationType.Djinn), # Gel
InternalLocationData(83, 83, 16384066, 16384066,
        [16384066], 128, 15, True, True, LocationType.Djinn), # Eddy
InternalLocationData(84, 84, 16384068, 16384068,
        [16384068], 128, 16, True, True, LocationType.Djinn), # Balm
InternalLocationData(85, 85, 16384070, 16384070,
        [16384070], 128, 17, True, True, LocationType.Djinn), # Serac
InternalLocationData(88, 88, 16384072, 16384072,
        [16384072], 128, 0, True, True, LocationType.Djinn), # Forge
InternalLocationData(89, 89, 16384074, 16384074,
        [16384074], 128, 1, True, True, LocationType.Djinn), # Fever
InternalLocationData(90, 90, 16384076, 16384076,
        [16384076], 128, 2, True, True, LocationType.Djinn), # Corona
InternalLocationData(91, 91, 16384078, 16384078,
        [16384078], 128, 3, True, True, LocationType.Djinn), # Scorch
InternalLocationData(92, 92, 16384080, 16384080,
        [16384080], 128, 4, True, True, LocationType.Djinn), # Ember
InternalLocationData(93, 93, 16384082, 16384082,
        [16384082], 128, 5, True, True, LocationType.Djinn), # Flash
InternalLocationData(94, 94, 16384084, 16384084,
        [16384084], 128, 6, True, True, LocationType.Djinn), # Torch
InternalLocationData(95, 95, 16384086, 16384086,
        [16384086], 128, 7, True, True, LocationType.Djinn), # Cannon
InternalLocationData(96, 96, 16384088, 16384088,
        [16384088], 128, 8, True, True, LocationType.Djinn), # Spark
InternalLocationData(97, 97, 16384090, 16384090,
        [16384090], 128, 9, True, True, LocationType.Djinn), # Kindle
InternalLocationData(98, 98, 16384092, 16384092,
        [16384092], 128, 10, True, True, LocationType.Djinn), # Char
InternalLocationData(99, 99, 16384094, 16384094,
        [16384094], 128, 11, True, True, LocationType.Djinn), # Coal
InternalLocationData(100, 100, 16384096, 16384096,
        [16384096], 128, 12, True, True, LocationType.Djinn), # Reflux
InternalLocationData(101, 101, 16384098, 16384098,
        [16384098], 128, 13, True, True, LocationType.Djinn), # Core
InternalLocationData(102, 102, 16384100, 16384100,
        [16384100], 128, 14, True, True, LocationType.Djinn), # Tinder
InternalLocationData(103, 103, 16384102, 16384102,
        [16384102], 128, 15, True, True, LocationType.Djinn), # Shine
InternalLocationData(104, 104, 16384104, 16384104,
        [16384104], 128, 16, True, True, LocationType.Djinn), # Fury
InternalLocationData(105, 105, 16384106, 16384106,
        [16384106], 128, 17, True, True, LocationType.Djinn), # Fugue
InternalLocationData(108, 108, 16384108, 16384108,
        [16384108], 128, 0, True, True, LocationType.Djinn), # Gust
InternalLocationData(109, 109, 16384110, 16384110,
        [16384110], 128, 1, True, True, LocationType.Djinn), # Breeze
InternalLocationData(110, 110, 16384112, 16384112,
        [16384112], 128, 2, True, True, LocationType.Djinn), # Zephyr
InternalLocationData(111, 111, 16384114, 16384114,
        [16384114], 128, 3, True, True, LocationType.Djinn), # Smog
InternalLocationData(112, 112, 16384116, 16384116,
        [16384116], 128, 4, True, True, LocationType.Djinn), # Kite
InternalLocationData(113, 113, 16384118, 16384118,
        [16384118], 128, 5, True, True, LocationType.Djinn), # Squall
InternalLocationData(114, 114, 16384120, 16384120,
        [16384120], 128, 6, True, True, LocationType.Djinn), # Luff
InternalLocationData(115, 115, 16384122, 16384122,
        [16384122], 128, 7, True, True, LocationType.Djinn), # Breath
InternalLocationData(116, 116, 16384124, 16384124,
        [16384124], 128, 8, True, True, LocationType.Djinn), # Blitz
InternalLocationData(117, 117, 16384126, 16384126,
        [16384126], 128, 9, True, True, LocationType.Djinn), # Ether
InternalLocationData(118, 118, 16384128, 16384128,
        [16384128], 128, 10, True, True, LocationType.Djinn), # Waft
InternalLocationData(119, 119, 16384130, 16384130,
        [16384130], 128, 11, True, True, LocationType.Djinn), # Haze
InternalLocationData(120, 120, 16384132, 16384132,
        [16384132], 128, 12, True, True, LocationType.Djinn), # Wheeze
InternalLocationData(121, 121, 16384134, 16384134,
        [16384134], 128, 13, True, True, LocationType.Djinn), # Aroma
InternalLocationData(122, 122, 16384136, 16384136,
        [16384136], 128, 14, True, True, LocationType.Djinn), # Whorl
InternalLocationData(123, 123, 16384138, 16384138,
        [16384138], 128, 15, True, True, LocationType.Djinn), # Gasp
InternalLocationData(124, 124, 16384140, 16384140,
        [16384140], 128, 16, True, True, LocationType.Djinn), # Lull
InternalLocationData(125, 125, 16384142, 16384142,
        [16384142], 128, 17, True, True, LocationType.Djinn), # Gale

]

summon_tablets = [
    InternalLocationData(19, 19, 19, 992068, [992068],
            132, 3859, True, True,
            LocationType.Item, LocationRestriction(0)), #Moloch
    InternalLocationData(24, 24, 24, 992212, [992212],
            132, 3864, True, True,
            LocationType.Item, LocationRestriction(0)), #Daedalus
    InternalLocationData(18, 18, 18, 992632, [992632],
            132, 3858, True, True,
            LocationType.Item, LocationRestriction(0)), #Flora
    InternalLocationData(20, 20, 20, 993424, [993424],
            132, 3860, True, True,
            LocationType.Item, LocationRestriction(0)), #Ulysses
    InternalLocationData(25, 25, 25, 994300, [994300],
            132, 3865, True, True,
            LocationType.Item, LocationRestriction(0)), #Azul
    InternalLocationData(16, 16, 16, 994844, [994844],
            132, 3856, True, True,
            LocationType.Item, LocationRestriction(0)), #Zagan
    InternalLocationData(17, 17, 17, 994856, [994856],
            132, 3857, True, True,
            LocationType.Item, LocationRestriction(0)), #Megaera
    InternalLocationData(21, 21, 21, 994868, [994868],
            132, 3861, True, True,
            LocationType.Item, LocationRestriction(0)), #Haures
    InternalLocationData(23, 23, 23, 994880, [994880],
            132, 3863, True, True,
            LocationType.Item, LocationRestriction(0)), #Coatlicue
    InternalLocationData(26, 26, 26, 994892, [994892],
            132, 3866, True, True,
            LocationType.Item, LocationRestriction(0)), #Catastrophe
    InternalLocationData(27, 27, 27, 994904, [994904],
            132, 3867, True, True,
            LocationType.Item, LocationRestriction(0)), #Charon
    InternalLocationData(28, 28, 28, 994916, [994916],
            132, 3868, True, True,
            LocationType.Item, LocationRestriction(0)), #Iris
    InternalLocationData(2315, 2315, 2315, 16384198, [16384198],
            132, 3862, True, True,
            LocationType.Item, LocationRestriction(8)), #Eclipse
    
]

psyenergy_locations = [
    InternalLocationData(2260, 2260, 2260, 16384190, [16384190],
        132, 3728, True, True, LocationType.Psyenergy,
        LocationRestriction(11)), # Reveal
    InternalLocationData(2478, 2478, 2478, 16384192, [16384192],
        132, 3722, True, True, LocationType.Psyenergy,
        LocationRestriction(11)), # Parch
    InternalLocationData(2490, 2490, 2490, 16384194, [16384194],
        132, 3723, True, True, LocationType.Psyenergy,
        LocationRestriction(11)), # Sand
    InternalLocationData(2554, 2554, 2554, 16384196, [16384196],
        132, 3738, True, True, LocationType.Psyenergy,
        LocationRestriction(11)), # Blaze
    InternalLocationData(2, 6, 2, 16384204, [16384204],
        132, 3725, True, True, LocationType.Psyenergy,
        LocationRestriction(15)), # Mind Read
    InternalLocationData(3, 6, 3, 16384206, [16384206],
        132, 3662, True, True, LocationType.Psyenergy,
        LocationRestriction(15)), # Whirlwind
    InternalLocationData(4, 4, 4, 16384208, [16384208],
        132, 3596, True, True, LocationType.Psyenergy,
        LocationRestriction(15)), # Growth
    
]

events = [
    InternalLocationData(1912, 1912, 5001, 5001, [0], 0,
        5001, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Lighthouse - Doom Dragon Fight Victory
    InternalLocationData(2219, 2219, 5002, 5002, [0], 0,
        5002, True, True, LocationType.Event, LocationRestriction(7), True), # Alhafra Briggs Briggs defeated
    InternalLocationData(2431, 2431, 5003, 5003, [0], 0,
        5003, True, True, LocationType.Event, LocationRestriction(7), True), # Alhafra Prison Briggs Briggs escaped
    InternalLocationData(2303, 2303, 5004, 5004, [0], 0,
        5004, True, True, LocationType.Event, LocationRestriction(7), True), # Gabomba Statue Gabomba Statue Completed
    InternalLocationData(2542, 2542, 5005, 5005, [0], 0,
        5005, True, True, LocationType.Event, LocationRestriction(7), True), # Gaia Rock - Serpent Fight Serpent defeated
    InternalLocationData(2269, 2269, 5006, 5006, [0], 0,
        5006, True, True, LocationType.Event, LocationRestriction(7), True), # Sea of Time - Poseidon fight Poseidon defeated
    InternalLocationData(2367, 2367, 5007, 5007, [0], 0,
        5007, True, True, LocationType.Event, LocationRestriction(7), True), # Lemurian Ship - Aqua Hydra fight Aqua Hydra defeated
    InternalLocationData(2381, 2381, 5008, 5008, [0], 0,
        5008, True, True, LocationType.Event, LocationRestriction(7), True), # Shaman Village - Moapa fight Moapa defeated
    InternalLocationData(2593, 2593, 5009, 5009, [0], 0,
        5009, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter_Lighthouse Aeri - Agatio and Karst fight Jupiter Beacon Lit
    InternalLocationData(2635, 2635, 5010, 5010, [0], 0,
        5010, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Lighthouse - Flame Dragons fight Flame Dragons - defeated
    InternalLocationData(2270, 2270, 5011, 5011, [0], 0,
        5011, True, True, LocationType.Event, LocationRestriction(7), True), # Lemurian Ship - Engine Room Ship
    InternalLocationData(2271, 2271, 5012, 5012, [0], 0,
        5012, True, True, LocationType.Event, LocationRestriction(7), True), # Contigo - Wings of Anemos Wings of Anemos
    
    InternalLocationData(1545, 1545, 6002, 6002, [0], 0,
        6002, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1546, 1546, 6003, 6003, [0], 0,
        6003, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1547, 1547, 6004, 6004, [0], 0,
        6004, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1548, 1548, 6005, 6005, [0], 0,
        6005, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1549, 1549, 6006, 6006, [0], 0,
        6006, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1550, 1550, 6007, 6007, [0], 0,
        6007, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1551, 1551, 6008, 6008, [0], 0,
        6008, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1552, 1552, 6009, 6009, [0], 0,
        6009, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1553, 1553, 6010, 6010, [0], 0,
        6010, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1554, 1554, 6011, 6011, [0], 0,
        6011, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1555, 1555, 6012, 6012, [0], 0,
        6012, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1556, 1556, 6013, 6013, [0], 0,
        6013, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1557, 1557, 6014, 6014, [0], 0,
        6014, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1558, 1558, 6015, 6015, [0], 0,
        6015, True, True, LocationType.Event, LocationRestriction(7), True), # Venus Djinni
    InternalLocationData(1559, 1559, 6016, 6016, [0], 0,
        6016, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1560, 1560, 6017, 6017, [0], 0,
        6017, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1561, 1561, 6018, 6018, [0], 0,
        6018, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1562, 1562, 6019, 6019, [0], 0,
        6019, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1563, 1563, 6020, 6020, [0], 0,
        6020, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1564, 1564, 6021, 6021, [0], 0,
        6021, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1565, 1565, 6022, 6022, [0], 0,
        6022, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1566, 1566, 6023, 6023, [0], 0,
        6023, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1567, 1567, 6024, 6024, [0], 0,
        6024, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1568, 1568, 6025, 6025, [0], 0,
        6025, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1569, 1569, 6026, 6026, [0], 0,
        6026, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1570, 1570, 6027, 6027, [0], 0,
        6027, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1571, 1571, 6028, 6028, [0], 0,
        6028, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1572, 1572, 6029, 6029, [0], 0,
        6029, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1573, 1573, 6030, 6030, [0], 0,
        6030, True, True, LocationType.Event, LocationRestriction(7), True), # Mercury Djinni
    InternalLocationData(1574, 1574, 6031, 6031, [0], 0,
        6031, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1575, 1575, 6032, 6032, [0], 0,
        6032, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1576, 1576, 6033, 6033, [0], 0,
        6033, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1577, 1577, 6034, 6034, [0], 0,
        6034, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1578, 1578, 6035, 6035, [0], 0,
        6035, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1579, 1579, 6036, 6036, [0], 0,
        6036, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1580, 1580, 6037, 6037, [0], 0,
        6037, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1581, 1581, 6038, 6038, [0], 0,
        6038, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1582, 1582, 6039, 6039, [0], 0,
        6039, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1583, 1583, 6040, 6040, [0], 0,
        6040, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1584, 1584, 6041, 6041, [0], 0,
        6041, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1585, 1585, 6042, 6042, [0], 0,
        6042, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1586, 1586, 6043, 6043, [0], 0,
        6043, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1587, 1587, 6044, 6044, [0], 0,
        6044, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Djinni
    InternalLocationData(1588, 1588, 6045, 6045, [0], 0,
        6045, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1589, 1589, 6046, 6046, [0], 0,
        6046, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1590, 1590, 6047, 6047, [0], 0,
        6047, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1591, 1591, 6048, 6048, [0], 0,
        6048, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1592, 1592, 6049, 6049, [0], 0,
        6049, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1593, 1593, 6050, 6050, [0], 0,
        6050, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1594, 1594, 6051, 6051, [0], 0,
        6051, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1595, 1595, 6052, 6052, [0], 0,
        6052, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1596, 1596, 6053, 6053, [0], 0,
        6053, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1597, 1597, 6054, 6054, [0], 0,
        6054, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1598, 1598, 6055, 6055, [0], 0,
        6055, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1599, 1599, 6056, 6056, [0], 0,
        6056, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1600, 1600, 6057, 6057, [0], 0,
        6057, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1601, 1601, 6058, 6058, [0], 0,
        6058, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1602, 1602, 6059, 6059, [0], 0,
        6059, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter Djinni
    InternalLocationData(1604, 1604, 6061, 6061, [0], 0,
        6061, True, True, LocationType.Event, LocationRestriction(7), True), # Ruffian
    InternalLocationData(1605, 1605, 6062, 6062, [0], 0,
        6062, True, True, LocationType.Event, LocationRestriction(7), True), # Ruffian 2
    InternalLocationData(1606, 1606, 6063, 6063, [0], 0,
        6063, True, True, LocationType.Event, LocationRestriction(7), True), # Ruffian 3
    InternalLocationData(1607, 1607, 6064, 6064, [0], 0,
        6064, True, True, LocationType.Event, LocationRestriction(7), True), # Punch Ant
    InternalLocationData(1608, 1608, 6065, 6065, [0], 0,
        6065, True, True, LocationType.Event, LocationRestriction(7), True), # Flash Ant
    InternalLocationData(1609, 1609, 6066, 6066, [0], 0,
        6066, True, True, LocationType.Event, LocationRestriction(7), True), # Numb Ant
    InternalLocationData(1610, 1610, 6067, 6067, [0], 0,
        6067, True, True, LocationType.Event, LocationRestriction(7), True), # Chestbeater
    InternalLocationData(1611, 1611, 6068, 6068, [0], 0,
        6068, True, True, LocationType.Event, LocationRestriction(7), True), # Wild Gorilla
    InternalLocationData(1612, 1612, 6069, 6069, [0], 0,
        6069, True, True, LocationType.Event, LocationRestriction(7), True), # Crazy Gorilla
    InternalLocationData(1613, 1613, 6070, 6070, [0], 0,
        6070, True, True, LocationType.Event, LocationRestriction(7), True), # King Scorpion
    InternalLocationData(1614, 1614, 6071, 6071, [0], 0,
        6071, True, True, LocationType.Event, LocationRestriction(7), True), # Devil Scorpion
    InternalLocationData(1615, 1615, 6072, 6072, [0], 0,
        6072, True, True, LocationType.Event, LocationRestriction(7), True), # Sand Scorpion
    InternalLocationData(1616, 1616, 6073, 6073, [0], 0,
        6073, True, True, LocationType.Event, LocationRestriction(7), True), # Briggs
    InternalLocationData(1617, 1617, 6074, 6074, [0], 0,
        6074, True, True, LocationType.Event, LocationRestriction(7), True), # Sea Fighter
    InternalLocationData(1618, 1618, 6075, 6075, [0], 0,
        6075, True, True, LocationType.Event, LocationRestriction(7), True), # Champa 2
    InternalLocationData(1619, 1619, 6076, 6076, [0], 0,
        6076, True, True, LocationType.Event, LocationRestriction(7), True), # Champa 3
    InternalLocationData(1620, 1620, 6077, 6077, [0], 0,
        6077, True, True, LocationType.Event, LocationRestriction(7), True), # Cuttle
    InternalLocationData(1621, 1621, 6078, 6078, [0], 0,
        6078, True, True, LocationType.Event, LocationRestriction(7), True), # Calamar
    InternalLocationData(1622, 1622, 6079, 6079, [0], 0,
        6079, True, True, LocationType.Event, LocationRestriction(7), True), # Man o' War
    InternalLocationData(1623, 1623, 6080, 6080, [0], 0,
        6080, True, True, LocationType.Event, LocationRestriction(7), True), # Aqua Jelly
    InternalLocationData(1624, 1624, 6081, 6081, [0], 0,
        6081, True, True, LocationType.Event, LocationRestriction(7), True), # Aqua Hydra
    InternalLocationData(1625, 1625, 6082, 6082, [0], 0,
        6082, True, True, LocationType.Event, LocationRestriction(7), True), # Hydra
    InternalLocationData(1626, 1626, 6083, 6083, [0], 0,
        6083, True, True, LocationType.Event, LocationRestriction(7), True), # Pyrodra
    InternalLocationData(1627, 1627, 6084, 6084, [0], 0,
        6084, True, True, LocationType.Event, LocationRestriction(7), True), # Serpent
    InternalLocationData(1628, 1628, 6085, 6085, [0], 0,
        6085, True, True, LocationType.Event, LocationRestriction(7), True), # Serpent
    InternalLocationData(1629, 1629, 6086, 6086, [0], 0,
        6086, True, True, LocationType.Event, LocationRestriction(7), True), # Serpent
    InternalLocationData(1630, 1630, 6087, 6087, [0], 0,
        6087, True, True, LocationType.Event, LocationRestriction(7), True), # Serpent
    InternalLocationData(1631, 1631, 6088, 6088, [0], 0,
        6088, True, True, LocationType.Event, LocationRestriction(7), True), # Serpent
    InternalLocationData(1632, 1632, 6089, 6089, [0], 0,
        6089, True, True, LocationType.Event, LocationRestriction(7), True), # Serpent 6
    InternalLocationData(1633, 1633, 6090, 6090, [0], 0,
        6090, True, True, LocationType.Event, LocationRestriction(7), True), # Serpent 7
    InternalLocationData(1634, 1634, 6091, 6091, [0], 0,
        6091, True, True, LocationType.Event, LocationRestriction(7), True), # Avimander
    InternalLocationData(1635, 1635, 6092, 6092, [0], 0,
        6092, True, True, LocationType.Event, LocationRestriction(7), True), # Macetail
    InternalLocationData(1636, 1636, 6093, 6093, [0], 0,
        6093, True, True, LocationType.Event, LocationRestriction(7), True), # Bombander
    InternalLocationData(1637, 1637, 6094, 6094, [0], 0,
        6094, True, True, LocationType.Event, LocationRestriction(7), True), # Poseidon
    InternalLocationData(1638, 1638, 6095, 6095, [0], 0,
        6095, True, True, LocationType.Event, LocationRestriction(7), True), # Poseidon
    InternalLocationData(1639, 1639, 6096, 6096, [0], 0,
        6096, True, True, LocationType.Event, LocationRestriction(7), True), # Poseidon 3
    InternalLocationData(1640, 1640, 6097, 6097, [0], 0,
        6097, True, True, LocationType.Event, LocationRestriction(7), True), # Moapa
    InternalLocationData(1641, 1641, 6098, 6098, [0], 0,
        6098, True, True, LocationType.Event, LocationRestriction(7), True), # Moapa
    InternalLocationData(1642, 1642, 6099, 6099, [0], 0,
        6099, True, True, LocationType.Event, LocationRestriction(7), True), # Moapa
    InternalLocationData(1643, 1643, 6100, 6100, [0], 0,
        6100, True, True, LocationType.Event, LocationRestriction(7), True), # Knight
    InternalLocationData(1644, 1644, 6101, 6101, [0], 0,
        6101, True, True, LocationType.Event, LocationRestriction(7), True), # Knight
    InternalLocationData(1645, 1645, 6102, 6102, [0], 0,
        6102, True, True, LocationType.Event, LocationRestriction(7), True), # Knight 3
    InternalLocationData(1646, 1646, 6103, 6103, [0], 0,
        6103, True, True, LocationType.Event, LocationRestriction(7), True), # Agatio
    InternalLocationData(1647, 1647, 6104, 6104, [0], 0,
        6104, True, True, LocationType.Event, LocationRestriction(7), True), # Agatio
    InternalLocationData(1648, 1648, 6105, 6105, [0], 0,
        6105, True, True, LocationType.Event, LocationRestriction(7), True), # Agatio
    InternalLocationData(1649, 1649, 6106, 6106, [0], 0,
        6106, True, True, LocationType.Event, LocationRestriction(7), True), # Karst
    InternalLocationData(1650, 1650, 6107, 6107, [0], 0,
        6107, True, True, LocationType.Event, LocationRestriction(7), True), # Karst
    InternalLocationData(1651, 1651, 6108, 6108, [0], 0,
        6108, True, True, LocationType.Event, LocationRestriction(7), True), # Karst
    InternalLocationData(1653, 1653, 6110, 6110, [0], 0,
        6110, True, True, LocationType.Event, LocationRestriction(7), True), # Wild Wolf
    InternalLocationData(1654, 1654, 6111, 6111, [0], 0,
        6111, True, True, LocationType.Event, LocationRestriction(7), True), # Dire Wolf
    InternalLocationData(1655, 1655, 6112, 6112, [0], 0,
        6112, True, True, LocationType.Event, LocationRestriction(7), True), # White Wolf
    InternalLocationData(1656, 1656, 6113, 6113, [0], 0,
        6113, True, True, LocationType.Event, LocationRestriction(7), True), # Angle Worm
    InternalLocationData(1657, 1657, 6114, 6114, [0], 0,
        6114, True, True, LocationType.Event, LocationRestriction(7), True), # Fire Worm
    InternalLocationData(1658, 1658, 6115, 6115, [0], 0,
        6115, True, True, LocationType.Event, LocationRestriction(7), True), # Chimera Worm
    InternalLocationData(1659, 1659, 6116, 6116, [0], 0,
        6116, True, True, LocationType.Event, LocationRestriction(7), True), # MiniGoblin
    InternalLocationData(1660, 1660, 6117, 6117, [0], 0,
        6117, True, True, LocationType.Event, LocationRestriction(7), True), # Alec Goblin
    InternalLocationData(1661, 1661, 6118, 6118, [0], 0,
        6118, True, True, LocationType.Event, LocationRestriction(7), True), # Baboon Goblin
    InternalLocationData(1662, 1662, 6119, 6119, [0], 0,
        6119, True, True, LocationType.Event, LocationRestriction(7), True), # Momonga
    InternalLocationData(1663, 1663, 6120, 6120, [0], 0,
        6120, True, True, LocationType.Event, LocationRestriction(7), True), # Squirrelfang
    InternalLocationData(1664, 1664, 6121, 6121, [0], 0,
        6121, True, True, LocationType.Event, LocationRestriction(7), True), # Momangler
    InternalLocationData(1665, 1665, 6122, 6122, [0], 0,
        6122, True, True, LocationType.Event, LocationRestriction(7), True), # Kobold
    InternalLocationData(1841, 1841, 6298, 6298, [0], 0,
        6298, True, True, LocationType.Event, LocationRestriction(7), True), # Kobold
    InternalLocationData(1666, 1666, 6123, 6123, [0], 0,
        6123, True, True, LocationType.Event, LocationRestriction(7), True), # Wargold
    InternalLocationData(1667, 1667, 6124, 6124, [0], 0,
        6124, True, True, LocationType.Event, LocationRestriction(7), True), # Kobold King
    InternalLocationData(1668, 1668, 6125, 6125, [0], 0,
        6125, True, True, LocationType.Event, LocationRestriction(7), True), # Mad Plant
    InternalLocationData(1669, 1669, 6126, 6126, [0], 0,
        6126, True, True, LocationType.Event, LocationRestriction(7), True), # Mad Plant
    InternalLocationData(1670, 1670, 6127, 6127, [0], 0,
        6127, True, True, LocationType.Event, LocationRestriction(7), True), # Mad Plant
    InternalLocationData(1671, 1671, 6128, 6128, [0], 0,
        6128, True, True, LocationType.Event, LocationRestriction(7), True), # Mad Plant
    InternalLocationData(1672, 1672, 6129, 6129, [0], 0,
        6129, True, True, LocationType.Event, LocationRestriction(7), True), # Mad Plant
    InternalLocationData(1673, 1673, 6130, 6130, [0], 0,
        6130, True, True, LocationType.Event, LocationRestriction(7), True), # Emu
    InternalLocationData(1674, 1674, 6131, 6131, [0], 0,
        6131, True, True, LocationType.Event, LocationRestriction(7), True), # Talon Runner
    InternalLocationData(1675, 1675, 6132, 6132, [0], 0,
        6132, True, True, LocationType.Event, LocationRestriction(7), True), # Winged Runner
    InternalLocationData(1676, 1676, 6133, 6133, [0], 0,
        6133, True, True, LocationType.Event, LocationRestriction(7), True), # Mummy
    InternalLocationData(1677, 1677, 6134, 6134, [0], 0,
        6134, True, True, LocationType.Event, LocationRestriction(7), True), # Foul Mummy
    InternalLocationData(1678, 1678, 6135, 6135, [0], 0,
        6135, True, True, LocationType.Event, LocationRestriction(7), True), # Grave Wight
    InternalLocationData(1679, 1679, 6136, 6136, [0], 0,
        6136, True, True, LocationType.Event, LocationRestriction(7), True), # Wyvern Chick
    InternalLocationData(1680, 1680, 6137, 6137, [0], 0,
        6137, True, True, LocationType.Event, LocationRestriction(7), True), # Pteranodon
    InternalLocationData(1681, 1681, 6138, 6138, [0], 0,
        6138, True, True, LocationType.Event, LocationRestriction(7), True), # Winged Lizard
    InternalLocationData(1682, 1682, 6139, 6139, [0], 0,
        6139, True, True, LocationType.Event, LocationRestriction(7), True), # Wolfkin Cub
    InternalLocationData(1683, 1683, 6140, 6140, [0], 0,
        6140, True, True, LocationType.Event, LocationRestriction(7), True), # Wolfkin
    InternalLocationData(1684, 1684, 6141, 6141, [0], 0,
        6141, True, True, LocationType.Event, LocationRestriction(7), True), # Skinwalker
    InternalLocationData(1685, 1685, 6142, 6142, [0], 0,
        6142, True, True, LocationType.Event, LocationRestriction(7), True), # Dino
    InternalLocationData(1686, 1686, 6143, 6143, [0], 0,
        6143, True, True, LocationType.Event, LocationRestriction(7), True), # Dinox
    InternalLocationData(1687, 1687, 6144, 6144, [0], 0,
        6144, True, True, LocationType.Event, LocationRestriction(7), True), # Dinosaurus
    InternalLocationData(1688, 1688, 6145, 6145, [0], 0,
        6145, True, True, LocationType.Event, LocationRestriction(7), True), # Assassin
    InternalLocationData(1689, 1689, 6146, 6146, [0], 0,
        6146, True, True, LocationType.Event, LocationRestriction(7), True), # Slayer
    InternalLocationData(1690, 1690, 6147, 6147, [0], 0,
        6147, True, True, LocationType.Event, LocationRestriction(7), True), # Dark Murder
    InternalLocationData(1691, 1691, 6148, 6148, [0], 0,
        6148, True, True, LocationType.Event, LocationRestriction(7), True), # Doomsayer
    InternalLocationData(1692, 1692, 6149, 6149, [0], 0,
        6149, True, True, LocationType.Event, LocationRestriction(7), True), # Lich
    InternalLocationData(1777, 1777, 6234, 6234, [0], 0,
        6234, True, True, LocationType.Event, LocationRestriction(7), True), # Lich
    InternalLocationData(1693, 1693, 6150, 6150, [0], 0,
        6150, True, True, LocationType.Event, LocationRestriction(7), True), # Bane Wight
    InternalLocationData(1694, 1694, 6151, 6151, [0], 0,
        6151, True, True, LocationType.Event, LocationRestriction(7), True), # Pixie
    InternalLocationData(1695, 1695, 6152, 6152, [0], 0,
        6152, True, True, LocationType.Event, LocationRestriction(7), True), # Faery
    InternalLocationData(1696, 1696, 6153, 6153, [0], 0,
        6153, True, True, LocationType.Event, LocationRestriction(7), True), # Weird Nypmh
    InternalLocationData(1697, 1697, 6154, 6154, [0], 0,
        6154, True, True, LocationType.Event, LocationRestriction(7), True), # Wood Walker
    InternalLocationData(1698, 1698, 6155, 6155, [0], 0,
        6155, True, True, LocationType.Event, LocationRestriction(7), True), # Elder Wood
    InternalLocationData(1699, 1699, 6156, 6156, [0], 0,
        6156, True, True, LocationType.Event, LocationRestriction(7), True), # Estre Wood
    InternalLocationData(1700, 1700, 6157, 6157, [0], 0,
        6157, True, True, LocationType.Event, LocationRestriction(7), True), # Star Magician
    InternalLocationData(1701, 1701, 6158, 6158, [0], 0,
        6158, True, True, LocationType.Event, LocationRestriction(7), True), # Dark Wizard
    InternalLocationData(1702, 1702, 6159, 6159, [0], 0,
        6159, True, True, LocationType.Event, LocationRestriction(7), True), # Evil Shaman
    InternalLocationData(1703, 1703, 6160, 6160, [0], 0,
        6160, True, True, LocationType.Event, LocationRestriction(7), True), # Urchin Beast
    InternalLocationData(1704, 1704, 6161, 6161, [0], 0,
        6161, True, True, LocationType.Event, LocationRestriction(7), True), # Needle Egg
    InternalLocationData(1705, 1705, 6162, 6162, [0], 0,
        6162, True, True, LocationType.Event, LocationRestriction(7), True), # Sea Hedgehog
    InternalLocationData(1706, 1706, 6163, 6163, [0], 0,
        6163, True, True, LocationType.Event, LocationRestriction(7), True), # Conch Shell
    InternalLocationData(1707, 1707, 6164, 6164, [0], 0,
        6164, True, True, LocationType.Event, LocationRestriction(7), True), # Spiral Shell
    InternalLocationData(1708, 1708, 6165, 6165, [0], 0,
        6165, True, True, LocationType.Event, LocationRestriction(7), True), # Poison Shell
    InternalLocationData(1709, 1709, 6166, 6166, [0], 0,
        6166, True, True, LocationType.Event, LocationRestriction(7), True), # Merman
    InternalLocationData(1710, 1710, 6167, 6167, [0], 0,
        6167, True, True, LocationType.Event, LocationRestriction(7), True), # Gillman
    InternalLocationData(1711, 1711, 6168, 6168, [0], 0,
        6168, True, True, LocationType.Event, LocationRestriction(7), True), # Gillman Lord
    InternalLocationData(1712, 1712, 6169, 6169, [0], 0,
        6169, True, True, LocationType.Event, LocationRestriction(7), True), # Sea Dragon
    InternalLocationData(1713, 1713, 6170, 6170, [0], 0,
        6170, True, True, LocationType.Event, LocationRestriction(7), True), # Turtle Dragon
    InternalLocationData(1714, 1714, 6171, 6171, [0], 0,
        6171, True, True, LocationType.Event, LocationRestriction(7), True), # Ocean Dragon
    InternalLocationData(1715, 1715, 6172, 6172, [0], 0,
        6172, True, True, LocationType.Event, LocationRestriction(7), True), # Seabird
    InternalLocationData(1716, 1716, 6173, 6173, [0], 0,
        6173, True, True, LocationType.Event, LocationRestriction(7), True), # Seafowl
    InternalLocationData(1717, 1717, 6174, 6174, [0], 0,
        6174, True, True, LocationType.Event, LocationRestriction(7), True), # Great Seagull
    InternalLocationData(1718, 1718, 6175, 6175, [0], 0,
        6175, True, True, LocationType.Event, LocationRestriction(7), True), # Roc
    InternalLocationData(1719, 1719, 6176, 6176, [0], 0,
        6176, True, True, LocationType.Event, LocationRestriction(7), True), # Raptor
    InternalLocationData(1720, 1720, 6177, 6177, [0], 0,
        6177, True, True, LocationType.Event, LocationRestriction(7), True), # Fell Raptor
    InternalLocationData(1721, 1721, 6178, 6178, [0], 0,
        6178, True, True, LocationType.Event, LocationRestriction(7), True), # Wyvern
    InternalLocationData(1722, 1722, 6179, 6179, [0], 0,
        6179, True, True, LocationType.Event, LocationRestriction(7), True), # Sky Dragon
    InternalLocationData(1723, 1723, 6180, 6180, [0], 0,
        6180, True, True, LocationType.Event, LocationRestriction(7), True), # Winged Dragon
    InternalLocationData(1724, 1724, 6181, 6181, [0], 0,
        6181, True, True, LocationType.Event, LocationRestriction(7), True), # Phoenix
    InternalLocationData(1725, 1725, 6182, 6182, [0], 0,
        6182, True, True, LocationType.Event, LocationRestriction(7), True), # Fire Bird
    InternalLocationData(1726, 1726, 6183, 6183, [0], 0,
        6183, True, True, LocationType.Event, LocationRestriction(7), True), # Wonder Bird
    InternalLocationData(1727, 1727, 6184, 6184, [0], 0,
        6184, True, True, LocationType.Event, LocationRestriction(7), True), # Blue Dragon
    InternalLocationData(1728, 1728, 6185, 6185, [0], 0,
        6185, True, True, LocationType.Event, LocationRestriction(7), True), # Cruel Dragon
    InternalLocationData(1729, 1729, 6186, 6186, [0], 0,
        6186, True, True, LocationType.Event, LocationRestriction(7), True), # Dragon
    InternalLocationData(1730, 1730, 6187, 6187, [0], 0,
        6187, True, True, LocationType.Event, LocationRestriction(7), True), # Flame Dragon
    InternalLocationData(1731, 1731, 6188, 6188, [0], 0,
        6188, True, True, LocationType.Event, LocationRestriction(7), True), # Flame Dragon
    InternalLocationData(1732, 1732, 6189, 6189, [0], 0,
        6189, True, True, LocationType.Event, LocationRestriction(7), True), # Fire Dragon
    InternalLocationData(1733, 1733, 6190, 6190, [0], 0,
        6190, True, True, LocationType.Event, LocationRestriction(7), True), # Minotaurus
    InternalLocationData(1734, 1734, 6191, 6191, [0], 0,
        6191, True, True, LocationType.Event, LocationRestriction(7), True), # Minos Warrior
    InternalLocationData(1735, 1735, 6192, 6192, [0], 0,
        6192, True, True, LocationType.Event, LocationRestriction(7), True), # Minos Knight
    InternalLocationData(1736, 1736, 6193, 6193, [0], 0,
        6193, True, True, LocationType.Event, LocationRestriction(7), True), # Gressil
    InternalLocationData(1737, 1737, 6194, 6194, [0], 0,
        6194, True, True, LocationType.Event, LocationRestriction(7), True), # Little Death
    InternalLocationData(1738, 1738, 6195, 6195, [0], 0,
        6195, True, True, LocationType.Event, LocationRestriction(7), True), # MiniDeath
    InternalLocationData(1739, 1739, 6196, 6196, [0], 0,
        6196, True, True, LocationType.Event, LocationRestriction(7), True), # Red Demon
    InternalLocationData(1740, 1740, 6197, 6197, [0], 0,
        6197, True, True, LocationType.Event, LocationRestriction(7), True), # Lesser Demon
    InternalLocationData(1741, 1741, 6198, 6198, [0], 0,
        6198, True, True, LocationType.Event, LocationRestriction(7), True), # Mad Demon
    InternalLocationData(1742, 1742, 6199, 6199, [0], 0,
        6199, True, True, LocationType.Event, LocationRestriction(7), True), # Aka Manah
    InternalLocationData(1743, 1743, 6200, 6200, [0], 0,
        6200, True, True, LocationType.Event, LocationRestriction(7), True), # Druj
    InternalLocationData(1744, 1744, 6201, 6201, [0], 0,
        6201, True, True, LocationType.Event, LocationRestriction(7), True), # Aeshma
    InternalLocationData(1745, 1745, 6202, 6202, [0], 0,
        6202, True, True, LocationType.Event, LocationRestriction(7), True), # Valukar
    InternalLocationData(1746, 1746, 6203, 6203, [0], 0,
        6203, True, True, LocationType.Event, LocationRestriction(7), True), # Valukar
    InternalLocationData(1747, 1747, 6204, 6204, [0], 0,
        6204, True, True, LocationType.Event, LocationRestriction(7), True), # Valukar
    InternalLocationData(1748, 1748, 6205, 6205, [0], 0,
        6205, True, True, LocationType.Event, LocationRestriction(7), True), # Living Armor
    InternalLocationData(1749, 1749, 6206, 6206, [0], 0,
        6206, True, True, LocationType.Event, LocationRestriction(7), True), # Puppet Warrior
    InternalLocationData(1750, 1750, 6207, 6207, [0], 0,
        6207, True, True, LocationType.Event, LocationRestriction(7), True), # Estre Baron
    InternalLocationData(1751, 1751, 6208, 6208, [0], 0,
        6208, True, True, LocationType.Event, LocationRestriction(7), True), # Ghost Army
    InternalLocationData(1752, 1752, 6209, 6209, [0], 0,
        6209, True, True, LocationType.Event, LocationRestriction(7), True), # Soul Army
    InternalLocationData(1753, 1753, 6210, 6210, [0], 0,
        6210, True, True, LocationType.Event, LocationRestriction(7), True), # Spirit Army
    InternalLocationData(1754, 1754, 6211, 6211, [0], 0,
        6211, True, True, LocationType.Event, LocationRestriction(7), True), # Dullahan
    InternalLocationData(1755, 1755, 6212, 6212, [0], 0,
        6212, True, True, LocationType.Event, LocationRestriction(7), True), # Dullahan
    InternalLocationData(1756, 1756, 6213, 6213, [0], 0,
        6213, True, True, LocationType.Event, LocationRestriction(7), True), # Dullahan
    InternalLocationData(1757, 1757, 6214, 6214, [0], 0,
        6214, True, True, LocationType.Event, LocationRestriction(7), True), # Sentinel
    InternalLocationData(1758, 1758, 6215, 6215, [0], 0,
        6215, True, True, LocationType.Event, LocationRestriction(7), True), # Sentinel
    InternalLocationData(1759, 1759, 6216, 6216, [0], 0,
        6216, True, True, LocationType.Event, LocationRestriction(7), True), # Sentinel
    InternalLocationData(1760, 1760, 6217, 6217, [0], 0,
        6217, True, True, LocationType.Event, LocationRestriction(7), True), # Vermin
    InternalLocationData(1761, 1761, 6218, 6218, [0], 0,
        6218, True, True, LocationType.Event, LocationRestriction(7), True), # Vermin
    InternalLocationData(1762, 1762, 6219, 6219, [0], 0,
        6219, True, True, LocationType.Event, LocationRestriction(7), True), # Mad Vermin
    InternalLocationData(1763, 1763, 6220, 6220, [0], 0,
        6220, True, True, LocationType.Event, LocationRestriction(7), True), # Bat
    InternalLocationData(1764, 1764, 6221, 6221, [0], 0,
        6221, True, True, LocationType.Event, LocationRestriction(7), True), # Bat
    InternalLocationData(1765, 1765, 6222, 6222, [0], 0,
        6222, True, True, LocationType.Event, LocationRestriction(7), True), # Rabid Bat
    InternalLocationData(1766, 1766, 6223, 6223, [0], 0,
        6223, True, True, LocationType.Event, LocationRestriction(7), True), # Giant Bat
    InternalLocationData(1767, 1767, 6224, 6224, [0], 0,
        6224, True, True, LocationType.Event, LocationRestriction(7), True), # Wild Mushroom
    InternalLocationData(1768, 1768, 6225, 6225, [0], 0,
        6225, True, True, LocationType.Event, LocationRestriction(7), True), # Wild Mushroom
    InternalLocationData(1769, 1769, 6226, 6226, [0], 0,
        6226, True, True, LocationType.Event, LocationRestriction(7), True), # Death Cap
    InternalLocationData(1770, 1770, 6227, 6227, [0], 0,
        6227, True, True, LocationType.Event, LocationRestriction(7), True), # Slime
    InternalLocationData(1771, 1771, 6228, 6228, [0], 0,
        6228, True, True, LocationType.Event, LocationRestriction(7), True), # Slime
    InternalLocationData(1772, 1772, 6229, 6229, [0], 0,
        6229, True, True, LocationType.Event, LocationRestriction(7), True), # Ooze
    InternalLocationData(1773, 1773, 6230, 6230, [0], 0,
        6230, True, True, LocationType.Event, LocationRestriction(7), True), # Slime Beast
    InternalLocationData(1774, 1774, 6231, 6231, [0], 0,
        6231, True, True, LocationType.Event, LocationRestriction(7), True), # Ghost
    InternalLocationData(1775, 1775, 6232, 6232, [0], 0,
        6232, True, True, LocationType.Event, LocationRestriction(7), True), # Ghost Mage
    InternalLocationData(1776, 1776, 6233, 6233, [0], 0,
        6233, True, True, LocationType.Event, LocationRestriction(7), True), # Horned Ghost
    InternalLocationData(1778, 1778, 6235, 6235, [0], 0,
        6235, True, True, LocationType.Event, LocationRestriction(7), True), # Zombie
    InternalLocationData(1904, 1904, 6361, 6361, [0], 0,
        6361, True, True, LocationType.Event, LocationRestriction(7), True), # Zombie
    InternalLocationData(1779, 1779, 6236, 6236, [0], 0,
        6236, True, True, LocationType.Event, LocationRestriction(7), True), # Undead
    InternalLocationData(1780, 1780, 6237, 6237, [0], 0,
        6237, True, True, LocationType.Event, LocationRestriction(7), True), # Wight
    InternalLocationData(1781, 1781, 6238, 6238, [0], 0,
        6238, True, True, LocationType.Event, LocationRestriction(7), True), # Bandit
    InternalLocationData(1921, 1921, 6378, 6378, [0], 0,
        6378, True, True, LocationType.Event, LocationRestriction(7), True), # Bandit
    InternalLocationData(1782, 1782, 6239, 6239, [0], 0,
        6239, True, True, LocationType.Event, LocationRestriction(7), True), # Thief
    InternalLocationData(1922, 1922, 6379, 6379, [0], 0,
        6379, True, True, LocationType.Event, LocationRestriction(7), True), # Thief
    InternalLocationData(1783, 1783, 6240, 6240, [0], 0,
        6240, True, True, LocationType.Event, LocationRestriction(7), True), # Brigand
    InternalLocationData(1784, 1784, 6241, 6241, [0], 0,
        6241, True, True, LocationType.Event, LocationRestriction(7), True), # Skeleton
    InternalLocationData(1785, 1785, 6242, 6242, [0], 0,
        6242, True, True, LocationType.Event, LocationRestriction(7), True), # Bone Fighter
    InternalLocationData(1786, 1786, 6243, 6243, [0], 0,
        6243, True, True, LocationType.Event, LocationRestriction(7), True), # Skull Warrior
    InternalLocationData(1787, 1787, 6244, 6244, [0], 0,
        6244, True, True, LocationType.Event, LocationRestriction(7), True), # Will Head
    InternalLocationData(1788, 1788, 6245, 6245, [0], 0,
        6245, True, True, LocationType.Event, LocationRestriction(7), True), # Death Head
    InternalLocationData(1789, 1789, 6246, 6246, [0], 0,
        6246, True, True, LocationType.Event, LocationRestriction(7), True), # Willowisp
    InternalLocationData(1790, 1790, 6247, 6247, [0], 0,
        6247, True, True, LocationType.Event, LocationRestriction(7), True), # Rat
    InternalLocationData(1791, 1791, 6248, 6248, [0], 0,
        6248, True, True, LocationType.Event, LocationRestriction(7), True), # Armored Rat
    InternalLocationData(1792, 1792, 6249, 6249, [0], 0,
        6249, True, True, LocationType.Event, LocationRestriction(7), True), # Plated Rat
    InternalLocationData(1793, 1793, 6250, 6250, [0], 0,
        6250, True, True, LocationType.Event, LocationRestriction(7), True), # Rat Soldier
    InternalLocationData(1794, 1794, 6251, 6251, [0], 0,
        6251, True, True, LocationType.Event, LocationRestriction(7), True), # Rat Fighter
    InternalLocationData(1795, 1795, 6252, 6252, [0], 0,
        6252, True, True, LocationType.Event, LocationRestriction(7), True), # Rat Warrior
    InternalLocationData(1796, 1796, 6253, 6253, [0], 0,
        6253, True, True, LocationType.Event, LocationRestriction(7), True), # Drone Bee
    InternalLocationData(1797, 1797, 6254, 6254, [0], 0,
        6254, True, True, LocationType.Event, LocationRestriction(7), True), # Fighter Bee
    InternalLocationData(1798, 1798, 6255, 6255, [0], 0,
        6255, True, True, LocationType.Event, LocationRestriction(7), True), # Warrior Bee
    InternalLocationData(1799, 1799, 6256, 6256, [0], 0,
        6256, True, True, LocationType.Event, LocationRestriction(7), True), # Troll
    InternalLocationData(1800, 1800, 6257, 6257, [0], 0,
        6257, True, True, LocationType.Event, LocationRestriction(7), True), # Cave Troll
    InternalLocationData(1801, 1801, 6258, 6258, [0], 0,
        6258, True, True, LocationType.Event, LocationRestriction(7), True), # Brutal Troll
    InternalLocationData(1802, 1802, 6259, 6259, [0], 0,
        6259, True, True, LocationType.Event, LocationRestriction(7), True), # Spider
    InternalLocationData(1803, 1803, 6260, 6260, [0], 0,
        6260, True, True, LocationType.Event, LocationRestriction(7), True), # Tarantula
    InternalLocationData(1804, 1804, 6261, 6261, [0], 0,
        6261, True, True, LocationType.Event, LocationRestriction(7), True), # Recluse
    InternalLocationData(1805, 1805, 6262, 6262, [0], 0,
        6262, True, True, LocationType.Event, LocationRestriction(7), True), # Gnome
    InternalLocationData(1806, 1806, 6263, 6263, [0], 0,
        6263, True, True, LocationType.Event, LocationRestriction(7), True), # Gnome Mage
    InternalLocationData(1807, 1807, 6264, 6264, [0], 0,
        6264, True, True, LocationType.Event, LocationRestriction(7), True), # Gnome Wizard
    InternalLocationData(1808, 1808, 6265, 6265, [0], 0,
        6265, True, True, LocationType.Event, LocationRestriction(7), True), # Ghoul
    InternalLocationData(1809, 1809, 6266, 6266, [0], 0,
        6266, True, True, LocationType.Event, LocationRestriction(7), True), # Fiendish Ghoul
    InternalLocationData(1810, 1810, 6267, 6267, [0], 0,
        6267, True, True, LocationType.Event, LocationRestriction(7), True), # Cannibal Ghoul
    InternalLocationData(1811, 1811, 6268, 6268, [0], 0,
        6268, True, True, LocationType.Event, LocationRestriction(7), True), # Mauler
    InternalLocationData(1812, 1812, 6269, 6269, [0], 0,
        6269, True, True, LocationType.Event, LocationRestriction(7), True), # Ravager
    InternalLocationData(1813, 1813, 6270, 6270, [0], 0,
        6270, True, True, LocationType.Event, LocationRestriction(7), True), # Grisly
    InternalLocationData(1814, 1814, 6271, 6271, [0], 0,
        6271, True, True, LocationType.Event, LocationRestriction(7), True), # Harpy
    InternalLocationData(1815, 1815, 6272, 6272, [0], 0,
        6272, True, True, LocationType.Event, LocationRestriction(7), True), # Virago
    InternalLocationData(1816, 1816, 6273, 6273, [0], 0,
        6273, True, True, LocationType.Event, LocationRestriction(7), True), # Harridan
    InternalLocationData(1817, 1817, 6274, 6274, [0], 0,
        6274, True, True, LocationType.Event, LocationRestriction(7), True), # Siren
    InternalLocationData(1818, 1818, 6275, 6275, [0], 0,
        6275, True, True, LocationType.Event, LocationRestriction(7), True), # Succubus
    InternalLocationData(1819, 1819, 6276, 6276, [0], 0,
        6276, True, True, LocationType.Event, LocationRestriction(7), True), # Nightmare
    InternalLocationData(1820, 1820, 6277, 6277, [0], 0,
        6277, True, True, LocationType.Event, LocationRestriction(7), True), # Mole
    InternalLocationData(1821, 1821, 6278, 6278, [0], 0,
        6278, True, True, LocationType.Event, LocationRestriction(7), True), # Mad Mole
    InternalLocationData(1822, 1822, 6279, 6279, [0], 0,
        6279, True, True, LocationType.Event, LocationRestriction(7), True), # Mole Mage
    InternalLocationData(1823, 1823, 6280, 6280, [0], 0,
        6280, True, True, LocationType.Event, LocationRestriction(7), True), # Dirge
    InternalLocationData(1824, 1824, 6281, 6281, [0], 0,
        6281, True, True, LocationType.Event, LocationRestriction(7), True), # Foul Dirge
    InternalLocationData(1825, 1825, 6282, 6282, [0], 0,
        6282, True, True, LocationType.Event, LocationRestriction(7), True), # Vile Dirge
    InternalLocationData(1826, 1826, 6283, 6283, [0], 0,
        6283, True, True, LocationType.Event, LocationRestriction(7), True), # Ape
    InternalLocationData(1827, 1827, 6284, 6284, [0], 0,
        6284, True, True, LocationType.Event, LocationRestriction(7), True), # Killer Ape
    InternalLocationData(1828, 1828, 6285, 6285, [0], 0,
        6285, True, True, LocationType.Event, LocationRestriction(7), True), # Dirty Ape
    InternalLocationData(1829, 1829, 6286, 6286, [0], 0,
        6286, True, True, LocationType.Event, LocationRestriction(7), True), # Grub
    InternalLocationData(1830, 1830, 6287, 6287, [0], 0,
        6287, True, True, LocationType.Event, LocationRestriction(7), True), # Worm
    InternalLocationData(1831, 1831, 6288, 6288, [0], 0,
        6288, True, True, LocationType.Event, LocationRestriction(7), True), # Acid Maggot
    InternalLocationData(1832, 1832, 6289, 6289, [0], 0,
        6289, True, True, LocationType.Event, LocationRestriction(7), True), # Orc
    InternalLocationData(1833, 1833, 6290, 6290, [0], 0,
        6290, True, True, LocationType.Event, LocationRestriction(7), True), # Orc Captain
    InternalLocationData(1834, 1834, 6291, 6291, [0], 0,
        6291, True, True, LocationType.Event, LocationRestriction(7), True), # Orc Lord
    InternalLocationData(1835, 1835, 6292, 6292, [0], 0,
        6292, True, True, LocationType.Event, LocationRestriction(7), True), # Salamander
    InternalLocationData(1836, 1836, 6293, 6293, [0], 0,
        6293, True, True, LocationType.Event, LocationRestriction(7), True), # Earth Lizard
    InternalLocationData(1837, 1837, 6294, 6294, [0], 0,
        6294, True, True, LocationType.Event, LocationRestriction(7), True), # Thunder Lizard
    InternalLocationData(1838, 1838, 6295, 6295, [0], 0,
        6295, True, True, LocationType.Event, LocationRestriction(7), True), # Manticore
    InternalLocationData(1839, 1839, 6296, 6296, [0], 0,
        6296, True, True, LocationType.Event, LocationRestriction(7), True), # Magicore
    InternalLocationData(1840, 1840, 6297, 6297, [0], 0,
        6297, True, True, LocationType.Event, LocationRestriction(7), True), # Manticore King
    InternalLocationData(1842, 1842, 6299, 6299, [0], 0,
        6299, True, True, LocationType.Event, LocationRestriction(7), True), # Goblin
    InternalLocationData(1843, 1843, 6300, 6300, [0], 0,
        6300, True, True, LocationType.Event, LocationRestriction(7), True), # Hobgoblin
    InternalLocationData(1844, 1844, 6301, 6301, [0], 0,
        6301, True, True, LocationType.Event, LocationRestriction(7), True), # Gargoyle
    InternalLocationData(1845, 1845, 6302, 6302, [0], 0,
        6302, True, True, LocationType.Event, LocationRestriction(7), True), # Clay Gargoyle
    InternalLocationData(1846, 1846, 6303, 6303, [0], 0,
        6303, True, True, LocationType.Event, LocationRestriction(7), True), # Ice Gargoyle
    InternalLocationData(1847, 1847, 6304, 6304, [0], 0,
        6304, True, True, LocationType.Event, LocationRestriction(7), True), # Gryphon
    InternalLocationData(1848, 1848, 6305, 6305, [0], 0,
        6305, True, True, LocationType.Event, LocationRestriction(7), True), # Wild Gryphon
    InternalLocationData(1849, 1849, 6306, 6306, [0], 0,
        6306, True, True, LocationType.Event, LocationRestriction(7), True), # Wise Gryphon
    InternalLocationData(1850, 1850, 6307, 6307, [0], 0,
        6307, True, True, LocationType.Event, LocationRestriction(7), True), # Golem
    InternalLocationData(1851, 1851, 6308, 6308, [0], 0,
        6308, True, True, LocationType.Event, LocationRestriction(7), True), # Earth Golem
    InternalLocationData(1852, 1852, 6309, 6309, [0], 0,
        6309, True, True, LocationType.Event, LocationRestriction(7), True), # Grand Golem
    InternalLocationData(1853, 1853, 6310, 6310, [0], 0,
        6310, True, True, LocationType.Event, LocationRestriction(7), True), # Dread Hound
    InternalLocationData(1854, 1854, 6311, 6311, [0], 0,
        6311, True, True, LocationType.Event, LocationRestriction(7), True), # Cerberus
    InternalLocationData(1855, 1855, 6312, 6312, [0], 0,
        6312, True, True, LocationType.Event, LocationRestriction(7), True), # Fenrir
    InternalLocationData(1856, 1856, 6313, 6313, [0], 0,
        6313, True, True, LocationType.Event, LocationRestriction(7), True), # Stone Soldier
    InternalLocationData(1857, 1857, 6314, 6314, [0], 0,
        6314, True, True, LocationType.Event, LocationRestriction(7), True), # Boulder Beast
    InternalLocationData(1858, 1858, 6315, 6315, [0], 0,
        6315, True, True, LocationType.Event, LocationRestriction(7), True), # Raging Rock
    InternalLocationData(1859, 1859, 6316, 6316, [0], 0,
        6316, True, True, LocationType.Event, LocationRestriction(7), True), # Chimera
    InternalLocationData(1860, 1860, 6317, 6317, [0], 0,
        6317, True, True, LocationType.Event, LocationRestriction(7), True), # Chimera Mage
    InternalLocationData(1861, 1861, 6318, 6318, [0], 0,
        6318, True, True, LocationType.Event, LocationRestriction(7), True), # Grand Chimera
    InternalLocationData(1862, 1862, 6319, 6319, [0], 0,
        6319, True, True, LocationType.Event, LocationRestriction(7), True), # Amaze
    InternalLocationData(1863, 1863, 6320, 6320, [0], 0,
        6320, True, True, LocationType.Event, LocationRestriction(7), True), # Amaze
    InternalLocationData(1864, 1864, 6321, 6321, [0], 0,
        6321, True, True, LocationType.Event, LocationRestriction(7), True), # Creeper
    InternalLocationData(1865, 1865, 6322, 6322, [0], 0,
        6322, True, True, LocationType.Event, LocationRestriction(7), True), # Spirit
    InternalLocationData(1866, 1866, 6323, 6323, [0], 0,
        6323, True, True, LocationType.Event, LocationRestriction(7), True), # Lizard Man
    InternalLocationData(1867, 1867, 6324, 6324, [0], 0,
        6324, True, True, LocationType.Event, LocationRestriction(7), True), # Lizard Fighter
    InternalLocationData(1868, 1868, 6325, 6325, [0], 0,
        6325, True, True, LocationType.Event, LocationRestriction(7), True), # Lizard King
    InternalLocationData(1869, 1869, 6326, 6326, [0], 0,
        6326, True, True, LocationType.Event, LocationRestriction(7), True), # Ant Lion
    InternalLocationData(1870, 1870, 6327, 6327, [0], 0,
        6327, True, True, LocationType.Event, LocationRestriction(7), True), # Roach
    InternalLocationData(1871, 1871, 6328, 6328, [0], 0,
        6328, True, True, LocationType.Event, LocationRestriction(7), True), # Doodle Bug
    InternalLocationData(1872, 1872, 6329, 6329, [0], 0,
        6329, True, True, LocationType.Event, LocationRestriction(7), True), # Toadonpa
    InternalLocationData(1873, 1873, 6330, 6330, [0], 0,
        6330, True, True, LocationType.Event, LocationRestriction(7), True), # Poison Toad
    InternalLocationData(1874, 1874, 6331, 6331, [0], 0,
        6331, True, True, LocationType.Event, LocationRestriction(7), True), # Devil Frog
    InternalLocationData(1875, 1875, 6332, 6332, [0], 0,
        6332, True, True, LocationType.Event, LocationRestriction(7), True), # Living Statue
    InternalLocationData(1876, 1876, 6333, 6333, [0], 0,
        6333, True, True, LocationType.Event, LocationRestriction(7), True), # Hydros Statue
    InternalLocationData(1877, 1877, 6334, 6334, [0], 0,
        6334, True, True, LocationType.Event, LocationRestriction(7), True), # Azart
    InternalLocationData(1878, 1878, 6335, 6335, [0], 0,
        6335, True, True, LocationType.Event, LocationRestriction(7), True), # Azart
    InternalLocationData(1918, 1918, 6375, 6375, [0], 0,
        6375, True, True, LocationType.Event, LocationRestriction(7), True), # Azart
    InternalLocationData(1879, 1879, 6336, 6336, [0], 0,
        6336, True, True, LocationType.Event, LocationRestriction(7), True), # Satrage
    InternalLocationData(1880, 1880, 6337, 6337, [0], 0,
        6337, True, True, LocationType.Event, LocationRestriction(7), True), # Satrage
    InternalLocationData(1919, 1919, 6376, 6376, [0], 0,
        6376, True, True, LocationType.Event, LocationRestriction(7), True), # Satrage
    InternalLocationData(1881, 1881, 6338, 6338, [0], 0,
        6338, True, True, LocationType.Event, LocationRestriction(7), True), # Navampa
    InternalLocationData(1882, 1882, 6339, 6339, [0], 0,
        6339, True, True, LocationType.Event, LocationRestriction(7), True), # Navampa
    InternalLocationData(1920, 1920, 6377, 6377, [0], 0,
        6377, True, True, LocationType.Event, LocationRestriction(7), True), # Navampa
    InternalLocationData(1883, 1883, 6340, 6340, [0], 0,
        6340, True, True, LocationType.Event, LocationRestriction(7), True), # Tret
    InternalLocationData(1884, 1884, 6341, 6341, [0], 0,
        6341, True, True, LocationType.Event, LocationRestriction(7), True), # Kraken
    InternalLocationData(1885, 1885, 6342, 6342, [0], 0,
        6342, True, True, LocationType.Event, LocationRestriction(7), True), # Tornado Lizard
    InternalLocationData(1886, 1886, 6343, 6343, [0], 0,
        6343, True, True, LocationType.Event, LocationRestriction(7), True), # Storm Lizard
    InternalLocationData(1887, 1887, 6344, 6344, [0], 0,
        6344, True, True, LocationType.Event, LocationRestriction(7), True), # Tempest Lizard
    InternalLocationData(1888, 1888, 6345, 6345, [0], 0,
        6345, True, True, LocationType.Event, LocationRestriction(7), True), # Mystery Man
    InternalLocationData(1889, 1889, 6346, 6346, [0], 0,
        6346, True, True, LocationType.Event, LocationRestriction(7), True), # Saturos
    InternalLocationData(1890, 1890, 6347, 6347, [0], 0,
        6347, True, True, LocationType.Event, LocationRestriction(7), True), # Saturos
    InternalLocationData(1891, 1891, 6348, 6348, [0], 0,
        6348, True, True, LocationType.Event, LocationRestriction(7), True), # Mystery Woman
    InternalLocationData(1892, 1892, 6349, 6349, [0], 0,
        6349, True, True, LocationType.Event, LocationRestriction(7), True), # Menardi
    InternalLocationData(1893, 1893, 6350, 6350, [0], 0,
        6350, True, True, LocationType.Event, LocationRestriction(7), True), # Fusion Dragon
    InternalLocationData(1894, 1894, 6351, 6351, [0], 0,
        6351, True, True, LocationType.Event, LocationRestriction(7), True), # Deadbeard
    InternalLocationData(1895, 1895, 6352, 6352, [0], 0,
        6352, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1896, 1896, 6353, 6353, [0], 0,
        6353, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1897, 1897, 6354, 6354, [0], 0,
        6354, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1898, 1898, 6355, 6355, [0], 0,
        6355, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1899, 1899, 6356, 6356, [0], 0,
        6356, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1900, 1900, 6357, 6357, [0], 0,
        6357, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1901, 1901, 6358, 6358, [0], 0,
        6358, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1902, 1902, 6359, 6359, [0], 0,
        6359, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1903, 1903, 6360, 6360, [0], 0,
        6360, True, True, LocationType.Event, LocationRestriction(7), True), # Mimic
    InternalLocationData(1905, 1905, 6362, 6362, [0], 0,
        6362, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1906, 1906, 6363, 6363, [0], 0,
        6363, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1907, 1907, 6364, 6364, [0], 0,
        6364, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1908, 1908, 6365, 6365, [0], 0,
        6365, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1909, 1909, 6366, 6366, [0], 0,
        6366, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1910, 1910, 6367, 6367, [0], 0,
        6367, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1911, 1911, 6368, 6368, [0], 0,
        6368, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1912, 1912, 6369, 6369, [0], 0,
        6369, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1913, 1913, 6370, 6370, [0], 0,
        6370, True, True, LocationType.Event, LocationRestriction(7), True), # Doom Dragon
    InternalLocationData(1914, 1914, 6371, 6371, [0], 0,
        6371, True, True, LocationType.Event, LocationRestriction(7), True), # Refresh Ball
    InternalLocationData(1915, 1915, 6372, 6372, [0], 0,
        6372, True, True, LocationType.Event, LocationRestriction(7), True), # Thunder Ball
    InternalLocationData(1916, 1916, 6373, 6373, [0], 0,
        6373, True, True, LocationType.Event, LocationRestriction(7), True), # Anger Ball
    InternalLocationData(1917, 1917, 6374, 6374, [0], 0,
        6374, True, True, LocationType.Event, LocationRestriction(7), True), # Guardian Ball
    
]

the_rest = [
    InternalLocationData(3841, 3841, 3841, 991776,
        [991776, 991796], 2, 180, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila Herb
    InternalLocationData(3842, 3842, 3842, 991784,
        [991784, 991804], 3, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila Smoke Bomb
    InternalLocationData(3934, 3934, 3934, 991812,
        [991812], 131, 186, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila Psy Crystal
    InternalLocationData(3858, 3858, 3858, 991824,
        [991824], 3, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # N Osenia Islet Lucky Medal
    InternalLocationData(3843, 3843, 3843, 991832,
        [991832], 3, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila Sleep Bomb
    InternalLocationData(3844, 3844, 3844, 991840,
        [991840], 2, 32771, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila 3 coins
    InternalLocationData(3845, 3845, 3845, 991848,
        [991848], 2, 32780, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila 12 coins
    InternalLocationData(3846, 3846, 3846, 991860,
        [991860], 128, 443, True, True,
        LocationType.Item, LocationRestriction(0)), # Kandorean Temple Mysterious Card
    InternalLocationData(3696, 3696, 3696, 991872,
        [991872], 129, 0, False, False,
        LocationType.Item, LocationRestriction(3)), # Kandorean Temple Mimic
    InternalLocationData(3847, 3847, 3847, 991884,
        [991884], 128, 340, False, True,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Full Metal Vest
    InternalLocationData(3848, 3848, 3848, 991892,
        [991892], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Elixir
    InternalLocationData(3849, 3849, 3849, 991904,
        [991904], 128, 195, False, False,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Mint
    InternalLocationData(3850, 3850, 3850, 991916,
        [991916], 128, 301, False, True,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Themis' Axe
    InternalLocationData(3851, 3851, 3851, 991928,
        [991928], 128, 181, False, False,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Nut
    InternalLocationData(3852, 3852, 3852, 991940,
        [991940], 128, 383, False, True,
        LocationType.Item, LocationRestriction(0)), # Madra Nurse's Cap
    InternalLocationData(3853, 3853, 3853, 991948,
        [991948], 13, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra Antidote
    InternalLocationData(2328, 2328, 2328, 16384166,
        [16384166, 991956], 128, 3721, True, True,
        LocationType.Item, LocationRestriction(11)), # Madra Cyclone Chip
    InternalLocationData(3854, 3854, 3854, 991968,
        [991968], 3, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra Smoke Bomb
    InternalLocationData(3855, 3855, 3855, 991976,
        [991976], 13, 32783, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra 15 coins
    InternalLocationData(3856, 3856, 3856, 991984,
        [991984], 2, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra Sleep Bomb
    InternalLocationData(3857, 3857, 3857, 991996,
        [991996], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra Elixir
    InternalLocationData(3859, 3859, 3859, 992008,
        [992008], 128, 193, False, False,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Apple
    InternalLocationData(3906, 3906, 3906, 992016,
        [992016], 128, 190, False, False,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Mist Potion
    InternalLocationData(3860, 3860, 3860, 992028,
        [992028], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Lucky Medal
    InternalLocationData(3861, 3861, 3861, 992036,
        [992036, 992048], 128, 459, True, True,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Ruin Key
    InternalLocationData(3862, 3862, 3862, 992060,
        [992060], 128, 3719, True, True,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Tremor Bit
    InternalLocationData(3863, 3863, 3863, 992080,
        [992080], 128, 287, False, True,
        LocationType.Item, LocationRestriction(0)), # Osenia Cliffs Pirate's Sword
    InternalLocationData(3864, 3864, 3864, 992092,
        [992092], 128, 414, False, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Guardian Ring
    InternalLocationData(3865, 3865, 3865, 992104,
        [992104], 128, 187, False, False,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Antidote
    InternalLocationData(3977, 3977, 3977, 992128,
        [992128], 131, 33083, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yampi Desert 315 coins
    InternalLocationData(2190, 2190, 2190, 992140,
        [992140], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Lucky Medal
    InternalLocationData(3866, 3866, 3866, 992148,
        [992148], 128, 444, True, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Trainer's Whip
    InternalLocationData(3867, 3867, 3867, 992172,
        [992172], 128, 194, False, False,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Hard Nut
    InternalLocationData(3868, 3868, 3868, 992180,
        [992180], 128, 309, False, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Blow Mace
    InternalLocationData(3978, 3978, 3978, 992192,
        [992192], 128, 189, False, False,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Cave Water of Life
    InternalLocationData(3979, 3979, 3979, 992204,
        [992204], 131, 435, False, True,
        LocationType.Item, LocationRestriction(3)), # Yampi Desert Cave Mythril Silver
    InternalLocationData(3980, 3980, 3980, 992224,
        [992224], 128, 436, False, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Cave Dark Matter
    InternalLocationData(3981, 3981, 3981, 992232,
        [992232], 128, 437, False, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Cave Orihalcon
    InternalLocationData(3869, 3869, 3869, 992244,
        [992244], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafra Psy Crystal
    InternalLocationData(3870, 3870, 3870, 992252,
        [992252], 2, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Sleep Bomb
    InternalLocationData(3871, 3871, 3871, 992260,
        [992260], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Lucky Medal
    InternalLocationData(3872, 3872, 3872, 992268,
        [992268], 13, 32800, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra 32 coins
    InternalLocationData(3873, 3873, 3873, 992280,
        [992280], 2, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Smoke Bomb
    InternalLocationData(3875, 3875, 3875, 992304,
        [992304], 3, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Elixir
    InternalLocationData(3876, 3876, 3876, 992312,
        [992312], 2, 193, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Apple
    InternalLocationData(3877, 3877, 3877, 992324,
        [992324], 128, 32891, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave 123 coins
    InternalLocationData(3878, 3878, 3878, 992332,
        [992332], 128, 333, False, True,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave Ixion Mail
    InternalLocationData(3879, 3879, 3879, 992340,
        [992340], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave Lucky Medal
    InternalLocationData(3982, 3982, 3982, 992348,
        [992348], 2, 191, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafran Cave Power Bread
    InternalLocationData(3983, 3983, 3983, 992360,
        [992360], 128, 33545, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave 777 coins
    InternalLocationData(3984, 3984, 3984, 992368,
        [992368], 128, 183, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave Potion
    InternalLocationData(3985, 3985, 3985, 992376,
        [992376], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave Psy Crystal
    InternalLocationData(3880, 3880, 3880, 992388,
        [992388], 128, 32850, False, False,
        LocationType.Item, LocationRestriction(0)), # Mikasalla 82 coins
    InternalLocationData(3881, 3881, 3881, 992396,
        [992396], 13, 181, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Mikasalla Nut
    InternalLocationData(3882, 3882, 3882, 992404,
        [992404], 3, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Mikasalla Elixir
    InternalLocationData(3883, 3883, 3883, 992416,
        [992416], 3, 196, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Mikasalla Lucky Pepper
    InternalLocationData(3884, 3884, 3884, 992424,
        [992424], 2, 180, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Mikasalla Herb
    InternalLocationData(3986, 3986, 3986, 992432,
        [992432], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # E Tundaria Islet Lucky Medal
    InternalLocationData(3885, 3885, 3885, 992444,
        [992444], 128, 290, False, True,
        LocationType.Item, LocationRestriction(0)), # Garoh Hypnos' Sword
    InternalLocationData(3886, 3886, 3886, 992456,
        [992456], 3, 181, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Garoh Nut
    InternalLocationData(3887, 3887, 3887, 992464,
        [992464], 3, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Garoh Smoke Bomb
    InternalLocationData(3888, 3888, 3888, 992476,
        [992476], 2, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Garoh Sleep Bomb
    InternalLocationData(3889, 3889, 3889, 992484,
        [992484], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Garoh Elixir
    InternalLocationData(3890, 3890, 3890, 992496,
        [992496], 128, 226, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Smoke Bomb
    InternalLocationData(3891, 3891, 3891, 992504,
        [992504], 128, 192, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Cookie
    InternalLocationData(3892, 3892, 3892, 992512,
        [992512], 128, 279, False, True,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Storm Brand
    InternalLocationData(3697, 3697, 3697, 992520,
        [992520], 129, 1, False, False,
        LocationType.Item, LocationRestriction(3)), # Air's Rock Mimic
    InternalLocationData(3893, 3893, 3893, 992532,
        [992532], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Vial
    InternalLocationData(3894, 3894, 3894, 992540,
        [992540], 128, 227, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Sleep Bomb
    InternalLocationData(3895, 3895, 3895, 992552,
        [992552], 128, 358, False, True,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Fujin Shield
    InternalLocationData(3896, 3896, 3896, 992564,
        [992564], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Vial
    InternalLocationData(3897, 3897, 3897, 992584,
        [992584], 128, 394, False, True,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Clarity Circlet
    InternalLocationData(3898, 3898, 3898, 992596,
        [992596], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Vial
    InternalLocationData(3899, 3899, 3899, 992608,
        [992608], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Elixir
    InternalLocationData(3900, 3900, 3900, 992620,
        [992620], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Psy Crystal
    InternalLocationData(3901, 3901, 3901, 992644,
        [992644], 128, 33434, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock 666 coins
    InternalLocationData(3904, 3904, 3904, 992656,
        [992656], 131, 448, True, True,
        LocationType.Item, LocationRestriction(3)), # Gondowan Cliffs Healing Fungus
    InternalLocationData(3905, 3905, 3905, 992664,
        [992664], 131, 449, True, True,
        LocationType.Item, LocationRestriction(3)), # Gondowan Cliffs Laughing Fungus
    InternalLocationData(3907, 3907, 3907, 992672,
        [992672], 128, 227, False, False,
        LocationType.Item, LocationRestriction(0)), # Gondowan Cliffs Sleep Bomb
    InternalLocationData(3908, 3908, 3908, 992684,
        [992684], 128, 384, False, True,
        LocationType.Item, LocationRestriction(0)), # Naribwe Thorn Crown
    InternalLocationData(3909, 3909, 3909, 992692,
        [992692], 128, 266, False, True,
        LocationType.Item, LocationRestriction(0)), # Naribwe Unicorn Ring
    InternalLocationData(3910, 3910, 3910, 992700,
        [992700], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Naribwe Elixir
    InternalLocationData(3911, 3911, 3911, 992712,
        [992712], 2, 32786, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Naribwe 18 coins
    InternalLocationData(3912, 3912, 3912, 992720,
        [992720], 2, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Naribwe Sleep Bomb
    InternalLocationData(3913, 3913, 3913, 992732,
        [992732], 128, 191, False, False,
        LocationType.Item, LocationRestriction(0)), # Kibombo Mountains Power Bread
    InternalLocationData(3914, 3914, 3914, 992740,
        [992740], 128, 429, False, True,
        LocationType.Item, LocationRestriction(0)), # Kibombo Mountains Tear Stone
    InternalLocationData(3915, 3915, 3915, 992752,
        [992752], 128, 300, False, True,
        LocationType.Item, LocationRestriction(0)), # Kibombo Mountains Disk Axe
    InternalLocationData(3916, 3916, 3916, 992764,
        [992764], 13, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Kibombo Mountains Smoke Bomb
    InternalLocationData(3918, 3918, 3918, 992800,
        [992800, 992812], 2, 196, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Kibombo Lucky Pepper
    InternalLocationData(3919, 3919, 3919, 992824,
        [992824], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Kibombo Lucky Medal
    InternalLocationData(3920, 3920, 3920, 992832,
        [992832], 3, 181, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Kibombo Nut
    InternalLocationData(3921, 3921, 3921, 992844,
        [992844], 128, 370, False, True,
        LocationType.Item, LocationRestriction(0)), # Gabomba Statue Bone Armlet
    InternalLocationData(3698, 3698, 3698, 992852,
        [992852], 129, 2, False, False,
        LocationType.Item, LocationRestriction(3)), # Gabomba Statue Mimic
    InternalLocationData(3922, 3922, 3922, 992864,
        [992864], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Gabomba Statue Elixir
    InternalLocationData(3923, 3923, 3923, 992876,
        [992876], 131, 195, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Gabomba Catacombs Mint
    InternalLocationData(3987, 3987, 3987, 992888,
        [992888], 131, 445, True, True,
        LocationType.Item, LocationRestriction(3)), # Gabomba Catacombs Tomegathericon
    InternalLocationData(3924, 3924, 3924, 992900,
        [992900], 128, 183, False, False,
        LocationType.Item, LocationRestriction(0)), # Lemurian Ship Potion
    InternalLocationData(3925, 3925, 3925, 992908,
        [992908], 3, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemurian Ship Elixir
    InternalLocationData(3926, 3926, 3926, 992916,
        [992916], 13, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemurian Ship Antidote
    InternalLocationData(3928, 3928, 3928, 992928,
        [992928], 128, 190, False, False,
        LocationType.Item, LocationRestriction(2)), # Lemurian Ship Mist Potion
    InternalLocationData(3927, 3927, 3927, 992936,
        [992936, 992944], 3, 238, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemurian Ship Oil Drop
    InternalLocationData(3929, 3929, 3929, 992968,
        [992968], 128, 426, False, True,
        LocationType.Item, LocationRestriction(0)), # Shrine of the Sea God Rusty Staff
    InternalLocationData(2247, 2247, 2247, 992980,
        [992980], 131, 439, True, True,
        LocationType.Item, LocationRestriction(3)), # Shrine of the Sea God Right Prong
    InternalLocationData(3930, 3930, 3930, 992992,
        [992992], 3, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # W Indra Islet Lucky Medal
    InternalLocationData(3931, 3931, 3931, 993016,
        [993016], 13, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # SE Angara Islet Lucky Medal
    InternalLocationData(3932, 3932, 3932, 993028,
        [993028], 3, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Sea of Time Islet Lucky Medal
    InternalLocationData(3936, 3936, 3936, 993040,
        [993040], 131, 181, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam Nut
    InternalLocationData(3937, 3937, 3937, 993048,
        [993048], 2, 32784, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam 16 coins
    InternalLocationData(3938, 3938, 3938, 993056,
        [993056], 131, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam Antidote
    InternalLocationData(3989, 3989, 3989, 993064,
        [993064], 128, 26, False, True,
        LocationType.Item, LocationRestriction(0)), # Yallam Masamune
    InternalLocationData(3990, 3990, 3990, 993076,
        [993076], 13, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam Elixir
    InternalLocationData(3991, 3991, 3991, 993084,
        [993084], 3, 238, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam Oil Drop
    InternalLocationData(3992, 3992, 3992, 993096,
        [993096], 128, 192, False, False,
        LocationType.Item, LocationRestriction(0)), # Taopo Swamp Cookie
    InternalLocationData(3939, 3939, 3939, 993108,
        [993108], 131, 429, False, True,
        LocationType.Item, LocationRestriction(3)), # Taopo Swamp Tear Stone
    InternalLocationData(3940, 3940, 3940, 993116,
        [993116], 131, 429, False, True,
        LocationType.Item, LocationRestriction(3)), # Taopo Swamp Tear Stone
    InternalLocationData(3941, 3941, 3941, 993128,
        [993128], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Taopo Swamp Vial
    InternalLocationData(3942, 3942, 3942, 993140,
        [993140], 131, 430, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Taopo Swamp Star Dust
    InternalLocationData(3993, 3993, 3993, 993152,
        [993152], 131, 240, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Taopo Swamp Bramble Seed
    InternalLocationData(3994, 3994, 3994, 993164,
        [993164], 131, 195, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands Mint
    InternalLocationData(3995, 3995, 3995, 993172,
        [993172], 131, 180, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands Herb
    InternalLocationData(3996, 3996, 3996, 993180,
        [993180], 2, 32950, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands 182 coins
    InternalLocationData(3997, 3997, 3997, 993192,
        [993192], 3, 32800, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands 32 coins
    InternalLocationData(3998, 3998, 3998, 993204,
        [993204], 131, 240, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands Bramble Seed
    InternalLocationData(3944, 3944, 3944, 993216,
        [993216], 128, 181, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Nut
    InternalLocationData(3945, 3945, 3945, 993224,
        [993224], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Elixir
    InternalLocationData(3946, 3946, 3946, 993236,
        [993236], 128, 291, False, True,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Mist Sabre
    InternalLocationData(3947, 3947, 3947, 993244,
        [993244], 128, 238, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Oil Drop
    InternalLocationData(3948, 3948, 3948, 993256,
        [993256], 128, 189, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Water of Life
    InternalLocationData(3699, 3699, 3699, 993268,
        [993268], 129, 3, False, False,
        LocationType.Item, LocationRestriction(3)), # Aqua Rock Mimic
    InternalLocationData(3949, 3949, 3949, 993280,
        [993280], 128, 456, True, True,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Aquarius Stone
    InternalLocationData(3950, 3950, 3950, 993288,
        [993288], 128, 196, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Lucky Pepper
    InternalLocationData(3951, 3951, 3951, 993300,
        [993300], 128, 418, False, True,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Rusty Sword
    InternalLocationData(3952, 3952, 3952, 993312,
        [993312], 128, 241, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Crystal Powder
    InternalLocationData(3953, 3953, 3953, 993332,
        [993332], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Vial
    InternalLocationData(3954, 3954, 3954, 993344,
        [993344], 128, 429, False, True,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Tear Stone
    InternalLocationData(3999, 3999, 3999, 993360,
        [993360], 131, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Antidote
    InternalLocationData(4000, 4000, 4000, 993368,
        [993368], 131, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Antidote
    InternalLocationData(4001, 4001, 4001, 993376,
        [993376], 131, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Lucky Medal
    InternalLocationData(4002, 4002, 4002, 993384,
        [993384], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Elixir
    InternalLocationData(4003, 4003, 4003, 993392,
        [993392], 2, 189, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Water of Life
    InternalLocationData(4004, 4004, 4004, 993404,
        [993404], 2, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Smoke Bomb
    InternalLocationData(4005, 4005, 4005, 993412,
        [993412], 13, 343, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Festival Coat
    InternalLocationData(4006, 4006, 4006, 993432,
        [993432], 128, 334, False, True,
        LocationType.Item, LocationRestriction(0)), # Izumo Phantasmal Mail
    InternalLocationData(3955, 3955, 3955, 993444,
        [993444], 128, 181, False, False,
        LocationType.Item, LocationRestriction(0)), # Gaia Rock Nut
    InternalLocationData(3956, 3956, 3956, 993456,
        [993456], 131, 451, True, True,
        LocationType.Item, LocationRestriction(3)), # Gaia Rock Dancing Idol
    InternalLocationData(3957, 3957, 3957, 993464,
        [993464], 128, 193, False, False,
        LocationType.Item, LocationRestriction(0)), # Gaia Rock Apple
    InternalLocationData(3700, 3700, 3700, 993476,
        [993476], 129, 4, False, False,
        LocationType.Item, LocationRestriction(3)), # Gaia Rock Mimic
    InternalLocationData(3958, 3958, 3958, 993484,
        [993484], 128, 423, False, True,
        LocationType.Item, LocationRestriction(0)), # Gaia Rock Rusty Mace
    InternalLocationData(3649, 3649, 3649, 993492,
        [993492], 131, 283, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Gaia Rock Cloud Brand
    InternalLocationData(4008, 4008, 4008, 993504,
        [993504], 128, 259, False, True,
        LocationType.Item, LocationRestriction(0)), # Islet Cave Turtle Boots
    InternalLocationData(4009, 4009, 4009, 993512,
        [993512], 128, 425, False, True,
        LocationType.Item, LocationRestriction(0)), # Islet Cave Rusty Staff
    InternalLocationData(4010, 4010, 4010, 993524,
        [993524], 128, 378, False, True,
        LocationType.Item, LocationRestriction(0)), # Champa Viking Helm
    InternalLocationData(4011, 4011, 4011, 993532,
        [993532], 13, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa Smoke Bomb
    InternalLocationData(4012, 4012, 4012, 993540,
        [993540], 13, 32780, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa 12 coins
    InternalLocationData(4013, 4013, 4013, 993548,
        [993548], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa Lucky Medal
    InternalLocationData(4014, 4014, 4014, 993560,
        [993560], 13, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa Elixir
    InternalLocationData(4015, 4015, 4015, 993572,
        [993572], 3, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa Sleep Bomb
    InternalLocationData(4016, 4016, 4016, 993584,
        [993584], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    InternalLocationData(4017, 4017, 4017, 993592,
        [993592], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    InternalLocationData(4018, 4018, 4018, 993600,
        [993600], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    InternalLocationData(4019, 4019, 4019, 993608,
        [993608], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    InternalLocationData(4020, 4020, 4020, 993616,
        [993616], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    InternalLocationData(4021, 4021, 4021, 993624,
        [993624], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    InternalLocationData(3959, 3959, 3959, 993632,
        [993632], 128, 32978, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins 210 coins
    InternalLocationData(3960, 3960, 3960, 993640,
        [993640], 128, 181, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Nut
    InternalLocationData(3961, 3961, 3961, 993652,
        [993652], 128, 241, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Crystal Powder
    InternalLocationData(3962, 3962, 3962, 993664,
        [993664], 128, 311, False, True,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Thanatos Mace
    InternalLocationData(3963, 3963, 3963, 993672,
        [993672], 128, 191, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Power Bread
    InternalLocationData(3964, 3964, 3964, 993680,
        [993680], 128, 349, False, True,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Muni Robe
    InternalLocationData(3965, 3965, 3965, 993692,
        [993692], 128, 33133, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins 365 coins
    InternalLocationData(3966, 3966, 3966, 993700,
        [993700], 128, 431, False, True,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Sylph Feather
    InternalLocationData(3967, 3967, 3967, 993708,
        [993708], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Vial
    InternalLocationData(3903, 3903, 3903, 993720,
        [993720], 128, 183, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Potion
    InternalLocationData(3968, 3968, 3968, 993732,
        [993732], 131, 440, True, True,
        LocationType.Item, LocationRestriction(3)), # Ankohl Ruins Left Prong
    InternalLocationData(3969, 3969, 3969, 993744,
        [993744], 128, 431, False, True,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Sylph Feather
    InternalLocationData(3970, 3970, 3970, 993752,
        [993752], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Lucky Medal
    InternalLocationData(3971, 3971, 3971, 993760,
        [993760], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Vial
    InternalLocationData(3972, 3972, 3972, 993768,
        [993768], 128, 281, False, True,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Lightning Sword
    InternalLocationData(2373, 2373, 2373, 16384200,
        [16384200, 993776], 128, 441, True, True,
        LocationType.Item, LocationRestriction(11)), # Tundaria Tower Center Prong
    InternalLocationData(3973, 3973, 3973, 993788,
        [993788], 128, 33133, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower 365 coins
    InternalLocationData(3974, 3974, 3974, 993796,
        [993796], 128, 195, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Mint
    InternalLocationData(3975, 3975, 3975, 993808,
        [993808], 128, 194, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Hard Nut
    InternalLocationData(3976, 3976, 3976, 993816,
        [993816], 128, 241, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Crystal Powder
    InternalLocationData(2377, 2377, 2377, 993828,
        [993828], 131, 3735, True, True,
        LocationType.Item, LocationRestriction(3)), # Tundaria Tower Burst Brooch
    InternalLocationData(4025, 4025, 4025, 993864,
        [993864], 131, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Lucky Medal
    InternalLocationData(4026, 4026, 4026, 993872,
        [993872], 131, 417, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Rusty Sword
    InternalLocationData(4027, 4027, 4027, 993880,
        [993880], 131, 194, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Hard Nut
    InternalLocationData(4028, 4028, 4028, 993888,
        [993888], 131, 231, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Bone
    InternalLocationData(4029, 4029, 4029, 993896,
        [993896], 131, 430, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Star Dust
    InternalLocationData(3943, 3943, 3943, 993916,
        [993916], 128, 3736, True, True,
        LocationType.Item, LocationRestriction(0)), # Lemuria Grindstone
    InternalLocationData(4031, 4031, 4031, 993924,
        [993924], 3, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Lucky Medal
    InternalLocationData(4032, 4032, 4032, 993936,
        [993936], 128, 430, False, True,
        LocationType.Item, LocationRestriction(0)), # Gondowan Settlement Star Dust
    InternalLocationData(4033, 4033, 4033, 993948,
        [993948], 8, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Gondowan Settlement Lucky Medal
    InternalLocationData(4034, 4034, 4034, 993960,
        [993960], 128, 32934, False, False,
        LocationType.Item, LocationRestriction(0)), # Hesperia Settlement 166 coins
    InternalLocationData(4035, 4035, 4035, 993984,
        [993984], 128, 432, False, True,
        LocationType.Item, LocationRestriction(0)), # SW Atteka Islet Dragon Skin
    InternalLocationData(4036, 4036, 4036, 993996,
        [993996], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Atteka Inlet Vial
    InternalLocationData(4037, 4037, 4037, 994016,
        [994016], 3, 191, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Contigo Power Bread
    InternalLocationData(4038, 4038, 4038, 994024,
        [994024], 131, 233, False, False,
        LocationType.Item, LocationRestriction(3)), # Contigo Corn
    InternalLocationData(4039, 4039, 4039, 994032,
        [994032], 131, 240, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Contigo Bramble Seed
    InternalLocationData(4040, 4040, 4040, 994044,
        [994044], 128, 366, False, True,
        LocationType.Item, LocationRestriction(0)), # Shaman Village Spirit Gloves
    InternalLocationData(4041, 4041, 4041, 994052,
        [994052], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Shaman Village Lucky Medal
    InternalLocationData(4042, 4042, 4042, 994064,
        [994064], 3, 239, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Shaman Village Weasel's Claw
    InternalLocationData(4043, 4043, 4043, 994072,
        [994072], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Shaman Village Elixir
    InternalLocationData(4044, 4044, 4044, 994084,
        [994084], 2, 196, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Shaman Village Lucky Pepper
    InternalLocationData(3935, 3935, 3935, 994096,
        [994096], 128, 194, False, False,
        LocationType.Item, LocationRestriction(0)), # Shaman Village Hard Nut
    InternalLocationData(4045, 4045, 4045, 994108,
        [994108], 128, 32929, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle 161 coins
    InternalLocationData(4046, 4046, 4046, 994116,
        [994116], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Lucky Medal
    InternalLocationData(4047, 4047, 4047, 994124,
        [994124], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4048, 4048, 4048, 994132,
        [994132], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4049, 4049, 4049, 994140,
        [994140], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4050, 4050, 4050, 994148,
        [994148], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4051, 4051, 4051, 994160,
        [994160], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4052, 4052, 4052, 994168,
        [994168], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4053, 4053, 4053, 994176,
        [994176], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4054, 4054, 4054, 994184,
        [994184], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4055, 4055, 4055, 994192,
        [994192], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4056, 4056, 4056, 994200,
        [994200], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    InternalLocationData(4057, 4057, 4057, 994208,
        [994208], 128, 33679, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle 911 coins
    InternalLocationData(4058, 4058, 4058, 994216,
        [994216], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Psy Crystal
    InternalLocationData(4059, 4059, 4059, 994224,
        [994224], 128, 192, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Cookie
    InternalLocationData(4060, 4060, 4060, 994232,
        [994232], 128, 431, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Sylph Feather
    InternalLocationData(4061, 4061, 4061, 994240,
        [994240], 128, 422, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Rusty Axe
    InternalLocationData(4062, 4062, 4062, 994248,
        [994248], 128, 430, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Star Dust
    InternalLocationData(4063, 4063, 4063, 994260,
        [994260], 128, 371, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Jester's Armlet
    InternalLocationData(3701, 3701, 3701, 994268,
        [994268], 129, 5, False, False,
        LocationType.Item, LocationRestriction(3)), # Treasure Isle Mimic
    InternalLocationData(4064, 4064, 4064, 994280,
        [994280], 128, 7, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Fire Brand
    InternalLocationData(4065, 4065, 4065, 994288,
        [994288], 128, 351, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Iris Robe
    InternalLocationData(4066, 4066, 4066, 994312,
        [994312], 131, 195, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Jupiter Lighthouse Mint
    InternalLocationData(4067, 4067, 4067, 994336,
        [994336], 128, 344, False, True,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Erinyes Tunic
    InternalLocationData(4068, 4068, 4068, 994348,
        [994348], 128, 183, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Potion
    InternalLocationData(4069, 4069, 4069, 994356,
        [994356], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Psy Crystal
    InternalLocationData(4070, 4070, 4070, 994368,
        [994368], 128, 319, False, True,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Meditation Rod
    InternalLocationData(4071, 4071, 4071, 994376,
        [994376], 131, 243, True, True,
        LocationType.Item, LocationRestriction(3)), # Jupiter Lighthouse Red Key
    InternalLocationData(3702, 3702, 3702, 994388,
        [994388], 129, 6, False, False,
        LocationType.Item, LocationRestriction(3)), # Jupiter Lighthouse Mimic
    InternalLocationData(4072, 4072, 4072, 994396,
        [994396], 131, 244, True, True,
        LocationType.Item, LocationRestriction(3)), # Jupiter Lighthouse Blue Key
    InternalLocationData(4073, 4073, 4073, 994404,
        [994404], 128, 190, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Mist Potion
    InternalLocationData(4074, 4074, 4074, 994412,
        [994412], 128, 33074, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse 306 coins
    InternalLocationData(4075, 4075, 4075, 994424,
        [994424], 128, 189, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Water of Life
    InternalLocationData(4076, 4076, 4076, 994436,
        [994436], 128, 292, False, True,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Phaeton's Blade
    InternalLocationData(4077, 4077, 4077, 994448,
        [994448], 128, 238, False, False,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Oil Drop
    InternalLocationData(4078, 4078, 4078, 994460,
        [994460], 128, 33151, False, False,
        LocationType.Item, LocationRestriction(0)), # Magma Rock 383 coins
    InternalLocationData(4079, 4079, 4079, 994468,
        [994468], 128, 433, False, True,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Salamander Tail
    InternalLocationData(4080, 4080, 4080, 994480,
        [994480], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Lucky Medal
    InternalLocationData(4081, 4081, 4081, 994492,
        [994492], 128, 190, False, False,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Mist Potion
    InternalLocationData(4082, 4082, 4082, 994504,
        [994504], 128, 433, False, True,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Salamander Tail
    InternalLocationData(4084, 4084, 4084, 994524,
        [994524], 128, 434, False, True,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Golem Core
    InternalLocationData(3703, 3703, 3703, 994536,
        [994536], 129, 7, False, False,
        LocationType.Item, LocationRestriction(3)), # Magma Rock Mimic
    InternalLocationData(4085, 4085, 4085, 994548,
        [994548], 131, 435, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Loho Mythril Silver
    InternalLocationData(4086, 4086, 4086, 994556,
        [994556], 131, 434, False, True,
        LocationType.Item, LocationRestriction(3)), # Loho Golem Core
    InternalLocationData(4087, 4087, 4087, 994564,
        [994564], 131, 434, False, True,
        LocationType.Item, LocationRestriction(3)), # Loho Golem Core
    InternalLocationData(4088, 4088, 4088, 994572,
        [994572], 3, 241, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Loho Crystal Powder
    InternalLocationData(4089, 4089, 4089, 994584,
        [994584], 131, 436, False, True,
        LocationType.Item, LocationRestriction(3)), # Prox Dark Matter
    InternalLocationData(4090, 4090, 4090, 994592,
        [994592], 2, 192, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Prox Cookie
    InternalLocationData(4091, 4091, 4091, 994604,
        [994604], 2, 183, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Prox Potion
    InternalLocationData(4092, 4092, 4092, 994612,
        [994612], 13, 236, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Prox Sacred Feather
    InternalLocationData(4093, 4093, 4093, 994624,
        [994624], 128, 193, False, False,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Apple
    InternalLocationData(4094, 4094, 4094, 994636,
        [994636], 128, 3740, True, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Teleport Lapis
    InternalLocationData(3704, 3704, 3704, 994644,
        [994644], 129, 8, False, False,
        LocationType.Item, LocationRestriction(3)), # Mars Lighthouse Mimic
    InternalLocationData(4095, 4095, 4095, 994656,
        [994656], 128, 388, False, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Alastor's Hood
    InternalLocationData(3584, 3584, 3584, 994668,
        [994668], 128, 437, False, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Orihalcon
    InternalLocationData(3585, 3585, 3585, 994680,
        [994680], 128, 336, False, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Valkyrie Mail
    InternalLocationData(3586, 3586, 3586, 994692,
        [994692], 128, 10, False, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Sol Blade
    InternalLocationData(3587, 3587, 3587, 994704,
        [994704], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Psy Crystal
    InternalLocationData(3588, 3588, 3588, 994716,
        [994716], 128, 432, False, True,
        LocationType.Item, LocationRestriction(0)), # Contigo Dragon Skin
    InternalLocationData(3589, 3589, 3589, 994728,
        [994728], 128, 436, False, True,
        LocationType.Item, LocationRestriction(0)), # Anemos Inner Sanctum Dark Matter
    InternalLocationData(3590, 3590, 3590, 994736,
        [994736], 128, 437, False, True,
        LocationType.Item, LocationRestriction(0)), # Anemos Inner Sanctum Orihalcon
    InternalLocationData(3674, 3674, 3674, 994832,
        [994832], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Shaman Village Elixir
    InternalLocationData(3675, 3675, 3675, 994928,
        [994928], 133, 421, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Axe
    InternalLocationData(3676, 3676, 3676, 994936,
        [994936], 133, 424, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Mace
    InternalLocationData(3677, 3677, 3677, 994944,
        [994944], 133, 419, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Sword
    InternalLocationData(3678, 3678, 3678, 994952,
        [994952], 133, 427, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Staff
    InternalLocationData(3679, 3679, 3679, 994960,
        [994960], 133, 420, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Sword
    InternalLocationData(2122, 2122, 2122, 16384160,
        [16384160], 128, 3717, True, True,
        LocationType.Item, LocationRestriction(11)), # Kandorean Temple Lash Pebble
    InternalLocationData(2168, 2168, 2168, 16384162,
        [16384162], 128, 3718, True, True,
        LocationType.Item, LocationRestriction(11)), # Dehkan Plateau Pound Cube
    InternalLocationData(2188, 2188, 2188, 16384164,
        [16384164], 128, 3720, True, True,
        LocationType.Item, LocationRestriction(11)), # Yampi Desert Scoop Gem
    InternalLocationData(2381, 2381, 2381, 16384168,
        [16384168], 128, 3737, True, True,
        LocationType.Item, LocationRestriction(11)), # Shaman Village Hover Jade
    InternalLocationData(2618, 2618, 2618, 16384170,
        [16384170], 128, 222, True, True,
        LocationType.Item, LocationRestriction(11)), # Mars Lighthouse Mars Star
    InternalLocationData(2303, 2303, 2303, 16384172,
        [16384172], 128, 242, True, True,
        LocationType.Item, LocationRestriction(11)), # Gabomba Statue Black Crystal
    InternalLocationData(2424, 2424, 2424, 16384174,
        [16384174], 128, 326, True, True,
        LocationType.Item, LocationRestriction(11)), # Champa Trident
    InternalLocationData(2722, 2722, 2722, 16384176,
        [16384176], 128, 452, True, True,
        LocationType.Trade, LocationRestriction(11)), # E Tundaria Islet Pretty Stone
    InternalLocationData(2724, 2724, 2724, 16384178,
        [16384178], 128, 453, True, True,
        LocationType.Trade, LocationRestriction(11)), # SE Angara Islet Red Cloth
    InternalLocationData(2723, 2723, 2723, 16384180,
        [16384180], 128, 454, True, True,
        LocationType.Trade, LocationRestriction(11)), # N Osenia Islet Milk
    InternalLocationData(2721, 2721, 2721, 16384182,
        [16384182], 128, 455, True, True,
        LocationType.Trade, LocationRestriction(11)), # W Indra Islet Li'l Turtle
    InternalLocationData(2592, 2592, 2592, 16384186,
        [16384186], 128, 458, True, True,
        LocationType.Item, LocationRestriction(11)), # Daila Sea God's Tear
    InternalLocationData(2553, 2553, 2553, 16384188,
        [16384188], 128, 460, True, True,
        LocationType.Item, LocationRestriction(11)), # Magma Rock Magma Ball
    InternalLocationData(1, 4, 1, 16384202,
        [16384202], 128, 65, True, True,
        LocationType.Item, LocationRestriction(15)), # Idejima Shaman's Rod
    InternalLocationData(257, 3, 257, 16384210,
        [16384210], 128, 3731, True, True,
        LocationType.Item, LocationRestriction(14)), # Contigo Carry Stone
    InternalLocationData(258, 2, 258, 16384212,
        [16384212], 128, 3727, True, True,
        LocationType.Item, LocationRestriction(14)), # Contigo Lifting Gem
    InternalLocationData(259, 1, 259, 16384214,
        [16384214], 128, 3726, True, True,
        LocationType.Item, LocationRestriction(14)), # Contigo Orb of Force
    InternalLocationData(260, 0, 260, 16384216,
        [16384216], 128, 3732, True, True,
        LocationType.Item, LocationRestriction(14)), # Contigo Catch Beads
    InternalLocationData(261, 7, 261, 16384218,
        [16384218], 128, 3617, True, True,
        LocationType.Item, LocationRestriction(12)), # Kibombo Douse Drop
    InternalLocationData(262, 7, 262, 16384220,
        [16384220], 128, 3608, True, True,
        LocationType.Item, LocationRestriction(12)), # Kibombo Frost Jewel
    InternalLocationData(3328, 3328, 3328, 16384384,
        [16384384], 132, 3328, True, True,
        LocationType.Character, LocationRestriction(11)), # Contigo Isaac
    InternalLocationData(3329, 3329, 3329, 16384386,
        [16384386], 132, 3329, True, True,
        LocationType.Character, LocationRestriction(11)), # Contigo Garet
    InternalLocationData(3330, 3330, 3330, 16384388,
        [16384388], 132, 3330, True, True,
        LocationType.Character, LocationRestriction(11)), # Contigo Ivan
    InternalLocationData(3331, 3331, 3331, 16384390,
        [16384390], 132, 3331, True, True,
        LocationType.Character, LocationRestriction(11)), # Contigo Mia
    InternalLocationData(3333, 3333, 3333, 16384392,
        [16384392], 132, 3333, True, True,
        LocationType.Character, LocationRestriction(11)), # Idejima Jenna
    InternalLocationData(3334, 3334, 3334, 16384394,
        [16384394], 132, 3334, True, True,
        LocationType.Character, LocationRestriction(11)), # Idejima Sheba
    InternalLocationData(3335, 3335, 3335, 16384396,
        [16384396], 132, 3335, True, True,
        LocationType.Character, LocationRestriction(11)), # Kibombo Piers
    
]


#def create_loctype_to_datamapping() -> Dict[str, List[InternalLocationData]]:
#    """Creates a dictionary mapping LocationType to a list of all locations
#    of that type
#    """
#    types: Dict[str, List[InternalLocationData]] = {}
#    for idx, data in enumerate(all_locations):
#        if data.loc_type not in types:
#            types[data.loc_type] = []
#        types[data.loc_type].append(data)
#    return types

all_locations: List[InternalLocationData] = djinn_locations + psyenergy_locations + summon_tablets + events + the_rest
#location_name_to_data: Dict[str, InternalLocationData] = {loc_names_by_id[location.ap_id]: location for location in all_locations if location.loc_type != LocationType.Event}
location_id_to_data: Dict[int, InternalLocationData] = {location.ap_id: location for location in all_locations if location.loc_type != LocationType.Event}
assert len(all_locations) == len(location_id_to_data) + len(events)
#location_type_to_data: Dict[str, List[InternalLocationData]] = create_loctype_to_datamapping()