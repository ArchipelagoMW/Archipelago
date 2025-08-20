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
        5001, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Lighthouse - Doom Dragon Doom Dragon Defeated
    InternalLocationData(2219, 2219, 5002, 5002, [0], 0,
        5002, True, True, LocationType.Event, LocationRestriction(7), True), # Alhafra Briggs Briggs defeated
    InternalLocationData(2431, 2431, 5003, 5003, [0], 0,
        5003, True, True, LocationType.Event, LocationRestriction(7), True), # Alhafra Prison Briggs Briggs escaped
    InternalLocationData(2303, 2303, 5004, 5004, [0], 0,
        5004, True, True, LocationType.Event, LocationRestriction(7), True), # Gabomba Statue Ritual Gabomba Statue Completed
    InternalLocationData(2542, 2542, 5005, 5005, [0], 0,
        5005, True, True, LocationType.Event, LocationRestriction(7), True), # Gaia Rock - Serpent Serpent defeated
    InternalLocationData(1637, 1637, 5006, 5006, [0], 0,
        5006, True, True, LocationType.Event, LocationRestriction(7), True), # Sea of Time - Poseidon Poseidon defeated
    InternalLocationData(2367, 2367, 5007, 5007, [0], 0,
        5007, True, True, LocationType.Event, LocationRestriction(7), True), # Lemurian Ship - Aqua Hydra Aqua Hydra defeated
    InternalLocationData(2381, 2381, 5008, 5008, [0], 0,
        5008, True, True, LocationType.Event, LocationRestriction(7), True), # Shaman Village - Moapa Moapa defeated
    InternalLocationData(2593, 2593, 5009, 5009, [0], 0,
        5009, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter_Lighthouse Aeri - Agatio and Karst Jupiter Beacon Lit
    InternalLocationData(2635, 2635, 5010, 5010, [0], 0,
        5010, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Lighthouse - Flame Dragons Flame Dragons - defeated
    InternalLocationData(2270, 2270, 5011, 5011, [0], 0,
        5011, True, True, LocationType.Event, LocationRestriction(7), True), # Lemurian Ship - Engine Room Ship
    InternalLocationData(2271, 2271, 5012, 5012, [0], 0,
        5012, True, True, LocationType.Event, LocationRestriction(7), True), # Contigo - Wings of Anemos Wings of Anemos
    InternalLocationData(1610, 1610, 5013, 5013, [0], 0,
        5013, True, True, LocationType.Event, LocationRestriction(7), True), # Kandorean Temple - Chestbeaters Chestbeaters defeated
    InternalLocationData(1613, 1613, 5014, 5014, [0], 0,
        5014, True, True, LocationType.Event, LocationRestriction(7), True), # Yampi Desert - King Scorpion King Scorpion defeated
    InternalLocationData(1634, 1634, 5015, 5015, [0], 0,
        5015, True, True, LocationType.Event, LocationRestriction(7), True), # Champa - Avimander Avimander defeated
    InternalLocationData(1700, 1700, 5016, 5016, [0], 0,
        5016, True, True, LocationType.Event, LocationRestriction(7), True), # Treasure Isle - Star Magician Star Magician defeated
    InternalLocationData(1757, 1757, 5017, 5017, [0], 0,
        5017, True, True, LocationType.Event, LocationRestriction(7), True), # Islet Cave - Sentinel Sentinel defeated
    InternalLocationData(1745, 1745, 5018, 5018, [0], 0,
        5018, True, True, LocationType.Event, LocationRestriction(7), True), # Yampi Desert Cave - Valukar Valukar defeated
    InternalLocationData(1754, 1754, 5019, 5019, [0], 0,
        5019, True, True, LocationType.Event, LocationRestriction(7), True), # Anemos Inner Sanctum - Dullahan Dullahan defeated
    InternalLocationData(2593, 2593, 5020, 5020, [0], 0,
        5020, True, True, LocationType.Event, LocationRestriction(7), True), # Contigo - Reunion Reunion
    InternalLocationData(1, 1, 5021, 5021, [0], 0,
        5021, True, True, LocationType.Event, LocationRestriction(7), True), # Victory Event Victory
    InternalLocationData(2655, 2655, 5022, 5022, [0], 0,
        5022, True, True, LocationType.Event, LocationRestriction(7), True), # Loho - Ship Cannon Ship Cannon
    InternalLocationData(2608, 2608, 5023, 5023, [0], 0,
        5023, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Lighthouse - Heated Mars Lighthouse Heated
    
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