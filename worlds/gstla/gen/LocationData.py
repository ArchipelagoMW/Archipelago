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

class LocationData(NamedTuple):
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
LocationData(48, 48, 16384000, 16384000,
        [16384000], 128, 0, True, True, LocationType.Djinn), # Flint
LocationData(49, 49, 16384002, 16384002,
        [16384002], 128, 1, True, True, LocationType.Djinn), # Granite
LocationData(50, 50, 16384004, 16384004,
        [16384004], 128, 2, True, True, LocationType.Djinn), # Quartz
LocationData(51, 51, 16384006, 16384006,
        [16384006], 128, 3, True, True, LocationType.Djinn), # Vine
LocationData(52, 52, 16384008, 16384008,
        [16384008], 128, 4, True, True, LocationType.Djinn), # Sap
LocationData(53, 53, 16384010, 16384010,
        [16384010], 128, 5, True, True, LocationType.Djinn), # Ground
LocationData(54, 54, 16384012, 16384012,
        [16384012], 128, 6, True, True, LocationType.Djinn), # Bane
LocationData(55, 55, 16384014, 16384014,
        [16384014], 128, 7, True, True, LocationType.Djinn), # Echo
LocationData(56, 56, 16384016, 16384016,
        [16384016], 128, 8, True, True, LocationType.Djinn), # Iron
LocationData(57, 57, 16384018, 16384018,
        [16384018], 128, 9, True, True, LocationType.Djinn), # Steel
LocationData(58, 58, 16384020, 16384020,
        [16384020], 128, 10, True, True, LocationType.Djinn), # Mud
LocationData(59, 59, 16384022, 16384022,
        [16384022], 128, 11, True, True, LocationType.Djinn), # Flower
LocationData(60, 60, 16384024, 16384024,
        [16384024], 128, 12, True, True, LocationType.Djinn), # Meld
LocationData(61, 61, 16384026, 16384026,
        [16384026], 128, 13, True, True, LocationType.Djinn), # Petra
LocationData(62, 62, 16384028, 16384028,
        [16384028], 128, 14, True, True, LocationType.Djinn), # Salt
LocationData(63, 63, 16384030, 16384030,
        [16384030], 128, 15, True, True, LocationType.Djinn), # Geode
LocationData(64, 64, 16384032, 16384032,
        [16384032], 128, 16, True, True, LocationType.Djinn), # Mold
LocationData(65, 65, 16384034, 16384034,
        [16384034], 128, 17, True, True, LocationType.Djinn), # Crystal
LocationData(68, 68, 16384036, 16384036,
        [16384036], 128, 0, True, True, LocationType.Djinn), # Fizz
LocationData(69, 69, 16384038, 16384038,
        [16384038], 128, 1, True, True, LocationType.Djinn), # Sleet
LocationData(70, 70, 16384040, 16384040,
        [16384040], 128, 2, True, True, LocationType.Djinn), # Mist
LocationData(71, 71, 16384042, 16384042,
        [16384042], 128, 3, True, True, LocationType.Djinn), # Spritz
LocationData(72, 72, 16384044, 16384044,
        [16384044], 128, 4, True, True, LocationType.Djinn), # Hail
LocationData(73, 73, 16384046, 16384046,
        [16384046], 128, 5, True, True, LocationType.Djinn), # Tonic
LocationData(74, 74, 16384048, 16384048,
        [16384048], 128, 6, True, True, LocationType.Djinn), # Dew
LocationData(75, 75, 16384050, 16384050,
        [16384050], 128, 7, True, True, LocationType.Djinn), # Fog
LocationData(76, 76, 16384052, 16384052,
        [16384052], 128, 8, True, True, LocationType.Djinn), # Sour
LocationData(77, 77, 16384054, 16384054,
        [16384054], 128, 9, True, True, LocationType.Djinn), # Spring
LocationData(78, 78, 16384056, 16384056,
        [16384056], 128, 10, True, True, LocationType.Djinn), # Shade
LocationData(79, 79, 16384058, 16384058,
        [16384058], 128, 11, True, True, LocationType.Djinn), # Chill
LocationData(80, 80, 16384060, 16384060,
        [16384060], 128, 12, True, True, LocationType.Djinn), # Steam
LocationData(81, 81, 16384062, 16384062,
        [16384062], 128, 13, True, True, LocationType.Djinn), # Rime
LocationData(82, 82, 16384064, 16384064,
        [16384064], 128, 14, True, True, LocationType.Djinn), # Gel
LocationData(83, 83, 16384066, 16384066,
        [16384066], 128, 15, True, True, LocationType.Djinn), # Eddy
LocationData(84, 84, 16384068, 16384068,
        [16384068], 128, 16, True, True, LocationType.Djinn), # Balm
LocationData(85, 85, 16384070, 16384070,
        [16384070], 128, 17, True, True, LocationType.Djinn), # Serac
LocationData(88, 88, 16384072, 16384072,
        [16384072], 128, 0, True, True, LocationType.Djinn), # Forge
LocationData(89, 89, 16384074, 16384074,
        [16384074], 128, 1, True, True, LocationType.Djinn), # Fever
LocationData(90, 90, 16384076, 16384076,
        [16384076], 128, 2, True, True, LocationType.Djinn), # Corona
LocationData(91, 91, 16384078, 16384078,
        [16384078], 128, 3, True, True, LocationType.Djinn), # Scorch
LocationData(92, 92, 16384080, 16384080,
        [16384080], 128, 4, True, True, LocationType.Djinn), # Ember
LocationData(93, 93, 16384082, 16384082,
        [16384082], 128, 5, True, True, LocationType.Djinn), # Flash
LocationData(94, 94, 16384084, 16384084,
        [16384084], 128, 6, True, True, LocationType.Djinn), # Torch
LocationData(95, 95, 16384086, 16384086,
        [16384086], 128, 7, True, True, LocationType.Djinn), # Cannon
LocationData(96, 96, 16384088, 16384088,
        [16384088], 128, 8, True, True, LocationType.Djinn), # Spark
LocationData(97, 97, 16384090, 16384090,
        [16384090], 128, 9, True, True, LocationType.Djinn), # Kindle
LocationData(98, 98, 16384092, 16384092,
        [16384092], 128, 10, True, True, LocationType.Djinn), # Char
LocationData(99, 99, 16384094, 16384094,
        [16384094], 128, 11, True, True, LocationType.Djinn), # Coal
LocationData(100, 100, 16384096, 16384096,
        [16384096], 128, 12, True, True, LocationType.Djinn), # Reflux
LocationData(101, 101, 16384098, 16384098,
        [16384098], 128, 13, True, True, LocationType.Djinn), # Core
LocationData(102, 102, 16384100, 16384100,
        [16384100], 128, 14, True, True, LocationType.Djinn), # Tinder
LocationData(103, 103, 16384102, 16384102,
        [16384102], 128, 15, True, True, LocationType.Djinn), # Shine
LocationData(104, 104, 16384104, 16384104,
        [16384104], 128, 16, True, True, LocationType.Djinn), # Fury
LocationData(105, 105, 16384106, 16384106,
        [16384106], 128, 17, True, True, LocationType.Djinn), # Fugue
LocationData(108, 108, 16384108, 16384108,
        [16384108], 128, 0, True, True, LocationType.Djinn), # Gust
LocationData(109, 109, 16384110, 16384110,
        [16384110], 128, 1, True, True, LocationType.Djinn), # Breeze
LocationData(110, 110, 16384112, 16384112,
        [16384112], 128, 2, True, True, LocationType.Djinn), # Zephyr
LocationData(111, 111, 16384114, 16384114,
        [16384114], 128, 3, True, True, LocationType.Djinn), # Smog
LocationData(112, 112, 16384116, 16384116,
        [16384116], 128, 4, True, True, LocationType.Djinn), # Kite
LocationData(113, 113, 16384118, 16384118,
        [16384118], 128, 5, True, True, LocationType.Djinn), # Squall
LocationData(114, 114, 16384120, 16384120,
        [16384120], 128, 6, True, True, LocationType.Djinn), # Luff
LocationData(115, 115, 16384122, 16384122,
        [16384122], 128, 7, True, True, LocationType.Djinn), # Breath
LocationData(116, 116, 16384124, 16384124,
        [16384124], 128, 8, True, True, LocationType.Djinn), # Blitz
LocationData(117, 117, 16384126, 16384126,
        [16384126], 128, 9, True, True, LocationType.Djinn), # Ether
LocationData(118, 118, 16384128, 16384128,
        [16384128], 128, 10, True, True, LocationType.Djinn), # Waft
LocationData(119, 119, 16384130, 16384130,
        [16384130], 128, 11, True, True, LocationType.Djinn), # Haze
LocationData(120, 120, 16384132, 16384132,
        [16384132], 128, 12, True, True, LocationType.Djinn), # Wheeze
LocationData(121, 121, 16384134, 16384134,
        [16384134], 128, 13, True, True, LocationType.Djinn), # Aroma
LocationData(122, 122, 16384136, 16384136,
        [16384136], 128, 14, True, True, LocationType.Djinn), # Whorl
LocationData(123, 123, 16384138, 16384138,
        [16384138], 128, 15, True, True, LocationType.Djinn), # Gasp
LocationData(124, 124, 16384140, 16384140,
        [16384140], 128, 16, True, True, LocationType.Djinn), # Lull
LocationData(125, 125, 16384142, 16384142,
        [16384142], 128, 17, True, True, LocationType.Djinn), # Gale

]

summon_tablets = [
    LocationData(19, 19, 19, 992068, [992068],
            132, 3859, True, True,
            LocationType.Item, LocationRestriction(0)), #Moloch
    LocationData(24, 24, 24, 992212, [992212],
            132, 3864, True, True,
            LocationType.Item, LocationRestriction(0)), #Daedalus
    LocationData(18, 18, 18, 992632, [992632],
            132, 3858, True, True,
            LocationType.Item, LocationRestriction(0)), #Flora
    LocationData(20, 20, 20, 993424, [993424],
            132, 3860, True, True,
            LocationType.Item, LocationRestriction(0)), #Ulysses
    LocationData(25, 25, 25, 994300, [994300],
            132, 3865, True, True,
            LocationType.Item, LocationRestriction(0)), #Azul
    LocationData(16, 16, 16, 994844, [994844],
            132, 3856, True, True,
            LocationType.Item, LocationRestriction(0)), #Zagan
    LocationData(17, 17, 17, 994856, [994856],
            132, 3857, True, True,
            LocationType.Item, LocationRestriction(0)), #Megaera
    LocationData(21, 21, 21, 994868, [994868],
            132, 3861, True, True,
            LocationType.Item, LocationRestriction(0)), #Haures
    LocationData(23, 23, 23, 994880, [994880],
            132, 3863, True, True,
            LocationType.Item, LocationRestriction(0)), #Coatlicue
    LocationData(26, 26, 26, 994892, [994892],
            132, 3866, True, True,
            LocationType.Item, LocationRestriction(0)), #Catastrophe
    LocationData(27, 27, 27, 994904, [994904],
            132, 3867, True, True,
            LocationType.Item, LocationRestriction(0)), #Charon
    LocationData(28, 28, 28, 994916, [994916],
            132, 3868, True, True,
            LocationType.Item, LocationRestriction(0)), #Iris
    LocationData(2315, 2315, 2315, 16384198, [16384198],
            132, 3862, True, True,
            LocationType.Item, LocationRestriction(8)), #Eclipse
    
]

psyenergy_locations = [
    LocationData(2260, 2260, 2260, 16384190, [16384190],
        132, 3728, True, True, LocationType.Psyenergy,
        LocationRestriction(11)), # Reveal
    LocationData(2478, 2478, 2478, 16384192, [16384192],
        132, 3722, True, True, LocationType.Psyenergy,
        LocationRestriction(11)), # Parch
    LocationData(2490, 2490, 2490, 16384194, [16384194],
        132, 3723, True, True, LocationType.Psyenergy,
        LocationRestriction(11)), # Sand
    LocationData(2554, 2554, 2554, 16384196, [16384196],
        132, 3738, True, True, LocationType.Psyenergy,
        LocationRestriction(11)), # Blaze
    LocationData(2, 6, 2, 16384204, [16384204],
        132, 3725, True, True, LocationType.Psyenergy,
        LocationRestriction(15)), # Mind Read
    LocationData(3, 6, 3, 16384206, [16384206],
        132, 3662, True, True, LocationType.Psyenergy,
        LocationRestriction(15)), # Whirlwind
    LocationData(4, 4, 4, 16384208, [16384208],
        132, 3596, True, True, LocationType.Psyenergy,
        LocationRestriction(15)), # Growth
    
]

events = [
    LocationData(1912, 1912, 5001, 5001, [0], 0,
        5001, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Lighthouse - Doom Dragon Fight Victory
    LocationData(2219, 2219, 5002, 5002, [0], 0,
        5002, True, True, LocationType.Event, LocationRestriction(7), True), # Alhafra Briggs Briggs defeated
    LocationData(2431, 2431, 5003, 5003, [0], 0,
        5003, True, True, LocationType.Event, LocationRestriction(7), True), # Alhafra Prison Briggs Briggs escaped
    LocationData(2303, 2303, 5004, 5004, [0], 0,
        5004, True, True, LocationType.Event, LocationRestriction(7), True), # Gabomba Statue Gabomba Statue Completed
    LocationData(2542, 2542, 5005, 5005, [0], 0,
        5005, True, True, LocationType.Event, LocationRestriction(7), True), # Gaia Rock - Serpent Fight Serpent defeated
    LocationData(2269, 2269, 5006, 5006, [0], 0,
        5006, True, True, LocationType.Event, LocationRestriction(7), True), # Sea of Time - Poseidon fight Poseidon defeated
    LocationData(2367, 2367, 5007, 5007, [0], 0,
        5007, True, True, LocationType.Event, LocationRestriction(7), True), # Lemurian Ship - Aqua Hydra fight Aqua Hydra defeated
    LocationData(2381, 2381, 5008, 5008, [0], 0,
        5008, True, True, LocationType.Event, LocationRestriction(7), True), # Shaman Village - Moapa fight Moapa defeated
    LocationData(2593, 2593, 5009, 5009, [0], 0,
        5009, True, True, LocationType.Event, LocationRestriction(7), True), # Jupiter_Lighthouse Aeri - Agatio and Karst fight Jupiter Beacon Lit
    LocationData(2635, 2635, 5010, 5010, [0], 0,
        5010, True, True, LocationType.Event, LocationRestriction(7), True), # Mars Lighthouse - Flame Dragons fight Flame Dragons - defeated
    LocationData(2270, 2270, 5011, 5011, [0], 0,
        5011, True, True, LocationType.Event, LocationRestriction(7), True), # Lemurian Ship - Engine Room Ship
    LocationData(2271, 2271, 5012, 5012, [0], 0,
        5012, True, True, LocationType.Event, LocationRestriction(7), True), # Contigo - Wings of Anemos Wings of Anemos
    
]

the_rest = [
    LocationData(3841, 3841, 3841, 991776,
        [991776, 991796], 2, 180, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila Herb
    LocationData(3842, 3842, 3842, 991784,
        [991784, 991804], 3, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila Smoke Bomb
    LocationData(3934, 3934, 3934, 991812,
        [991812], 131, 186, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila Psy Crystal
    LocationData(3858, 3858, 3858, 991824,
        [991824], 3, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # N Osenia Islet Lucky Medal
    LocationData(3843, 3843, 3843, 991832,
        [991832], 3, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila Sleep Bomb
    LocationData(3844, 3844, 3844, 991840,
        [991840], 2, 32771, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila 3 coins
    LocationData(3845, 3845, 3845, 991848,
        [991848], 2, 32780, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Daila 12 coins
    LocationData(3846, 3846, 3846, 991860,
        [991860], 128, 443, True, True,
        LocationType.Item, LocationRestriction(0)), # Kandorean Temple Mysterious Card
    LocationData(3696, 3696, 3696, 991872,
        [991872], 129, 0, False, False,
        LocationType.Item, LocationRestriction(3)), # Kandorean Temple Mimic
    LocationData(3847, 3847, 3847, 991884,
        [991884], 128, 340, False, True,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Full Metal Vest
    LocationData(3848, 3848, 3848, 991892,
        [991892], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Elixir
    LocationData(3849, 3849, 3849, 991904,
        [991904], 128, 195, False, False,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Mint
    LocationData(3850, 3850, 3850, 991916,
        [991916], 128, 301, False, True,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Themis' Axe
    LocationData(3851, 3851, 3851, 991928,
        [991928], 128, 181, False, False,
        LocationType.Item, LocationRestriction(0)), # Dehkan Plateau Nut
    LocationData(3852, 3852, 3852, 991940,
        [991940], 128, 383, False, True,
        LocationType.Item, LocationRestriction(0)), # Madra Nurse's Cap
    LocationData(3853, 3853, 3853, 991948,
        [991948], 13, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra Antidote
    LocationData(2328, 2328, 2328, 16384166,
        [16384166, 991956], 128, 3721, True, True,
        LocationType.Item, LocationRestriction(11)), # Madra Cyclone Chip
    LocationData(3854, 3854, 3854, 991968,
        [991968], 3, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra Smoke Bomb
    LocationData(3855, 3855, 3855, 991976,
        [991976], 13, 32783, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra 15 coins
    LocationData(3856, 3856, 3856, 991984,
        [991984], 2, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra Sleep Bomb
    LocationData(3857, 3857, 3857, 991996,
        [991996], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Madra Elixir
    LocationData(3859, 3859, 3859, 992008,
        [992008], 128, 193, False, False,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Apple
    LocationData(3906, 3906, 3906, 992016,
        [992016], 128, 190, False, False,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Mist Potion
    LocationData(3860, 3860, 3860, 992028,
        [992028], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Lucky Medal
    LocationData(3861, 3861, 3861, 992036,
        [992036, 992048], 128, 459, True, True,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Ruin Key
    LocationData(3862, 3862, 3862, 992060,
        [992060], 128, 3719, True, True,
        LocationType.Item, LocationRestriction(0)), # Madra Catacombs Tremor Bit
    LocationData(3863, 3863, 3863, 992080,
        [992080], 128, 287, False, True,
        LocationType.Item, LocationRestriction(0)), # Osenia Cliffs Pirate's Sword
    LocationData(3864, 3864, 3864, 992092,
        [992092], 128, 414, False, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Guardian Ring
    LocationData(3865, 3865, 3865, 992104,
        [992104], 128, 187, False, False,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Antidote
    LocationData(3977, 3977, 3977, 992128,
        [992128], 131, 33083, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yampi Desert 315 coins
    LocationData(2190, 2190, 2190, 992140,
        [992140], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Lucky Medal
    LocationData(3866, 3866, 3866, 992148,
        [992148], 128, 444, True, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Trainer's Whip
    LocationData(3867, 3867, 3867, 992172,
        [992172], 128, 194, False, False,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Hard Nut
    LocationData(3868, 3868, 3868, 992180,
        [992180], 128, 309, False, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Blow Mace
    LocationData(3978, 3978, 3978, 992192,
        [992192], 128, 189, False, False,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Cave Water of Life
    LocationData(3979, 3979, 3979, 992204,
        [992204], 131, 435, False, True,
        LocationType.Item, LocationRestriction(3)), # Yampi Desert Cave Mythril Silver
    LocationData(3980, 3980, 3980, 992224,
        [992224], 128, 436, False, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Cave Dark Matter
    LocationData(3981, 3981, 3981, 992232,
        [992232], 128, 437, False, True,
        LocationType.Item, LocationRestriction(0)), # Yampi Desert Cave Orihalcon
    LocationData(3869, 3869, 3869, 992244,
        [992244], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafra Psy Crystal
    LocationData(3870, 3870, 3870, 992252,
        [992252], 2, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Sleep Bomb
    LocationData(3871, 3871, 3871, 992260,
        [992260], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Lucky Medal
    LocationData(3872, 3872, 3872, 992268,
        [992268], 13, 32800, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra 32 coins
    LocationData(3873, 3873, 3873, 992280,
        [992280], 2, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Smoke Bomb
    LocationData(3875, 3875, 3875, 992304,
        [992304], 3, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Elixir
    LocationData(3876, 3876, 3876, 992312,
        [992312], 2, 193, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafra Apple
    LocationData(3877, 3877, 3877, 992324,
        [992324], 128, 32891, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave 123 coins
    LocationData(3878, 3878, 3878, 992332,
        [992332], 128, 333, False, True,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave Ixion Mail
    LocationData(3879, 3879, 3879, 992340,
        [992340], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave Lucky Medal
    LocationData(3982, 3982, 3982, 992348,
        [992348], 2, 191, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Alhafran Cave Power Bread
    LocationData(3983, 3983, 3983, 992360,
        [992360], 128, 33545, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave 777 coins
    LocationData(3984, 3984, 3984, 992368,
        [992368], 128, 183, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave Potion
    LocationData(3985, 3985, 3985, 992376,
        [992376], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Alhafran Cave Psy Crystal
    LocationData(3880, 3880, 3880, 992388,
        [992388], 128, 32850, False, False,
        LocationType.Item, LocationRestriction(0)), # Mikasalla 82 coins
    LocationData(3881, 3881, 3881, 992396,
        [992396], 13, 181, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Mikasalla Nut
    LocationData(3882, 3882, 3882, 992404,
        [992404], 3, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Mikasalla Elixir
    LocationData(3883, 3883, 3883, 992416,
        [992416], 3, 196, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Mikasalla Lucky Pepper
    LocationData(3884, 3884, 3884, 992424,
        [992424], 2, 180, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Mikasalla Herb
    LocationData(3986, 3986, 3986, 992432,
        [992432], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # E Tundaria Islet Lucky Medal
    LocationData(3885, 3885, 3885, 992444,
        [992444], 128, 290, False, True,
        LocationType.Item, LocationRestriction(0)), # Garoh Hypnos' Sword
    LocationData(3886, 3886, 3886, 992456,
        [992456], 3, 181, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Garoh Nut
    LocationData(3887, 3887, 3887, 992464,
        [992464], 3, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Garoh Smoke Bomb
    LocationData(3888, 3888, 3888, 992476,
        [992476], 2, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Garoh Sleep Bomb
    LocationData(3889, 3889, 3889, 992484,
        [992484], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Garoh Elixir
    LocationData(3890, 3890, 3890, 992496,
        [992496], 128, 226, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Smoke Bomb
    LocationData(3891, 3891, 3891, 992504,
        [992504], 128, 192, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Cookie
    LocationData(3892, 3892, 3892, 992512,
        [992512], 128, 279, False, True,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Storm Brand
    LocationData(3697, 3697, 3697, 992520,
        [992520], 129, 1, False, False,
        LocationType.Item, LocationRestriction(3)), # Air's Rock Mimic
    LocationData(3893, 3893, 3893, 992532,
        [992532], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Vial
    LocationData(3894, 3894, 3894, 992540,
        [992540], 128, 227, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Sleep Bomb
    LocationData(3895, 3895, 3895, 992552,
        [992552], 128, 358, False, True,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Fujin Shield
    LocationData(3896, 3896, 3896, 992564,
        [992564], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Vial
    LocationData(3897, 3897, 3897, 992584,
        [992584], 128, 394, False, True,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Clarity Circlet
    LocationData(3898, 3898, 3898, 992596,
        [992596], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Vial
    LocationData(3899, 3899, 3899, 992608,
        [992608], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Elixir
    LocationData(3900, 3900, 3900, 992620,
        [992620], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock Psy Crystal
    LocationData(3901, 3901, 3901, 992644,
        [992644], 128, 33434, False, False,
        LocationType.Item, LocationRestriction(0)), # Air's Rock 666 coins
    LocationData(3904, 3904, 3904, 992656,
        [992656], 131, 448, True, True,
        LocationType.Item, LocationRestriction(3)), # Gondowan Cliffs Healing Fungus
    LocationData(3905, 3905, 3905, 992664,
        [992664], 131, 449, True, True,
        LocationType.Item, LocationRestriction(3)), # Gondowan Cliffs Laughing Fungus
    LocationData(3907, 3907, 3907, 992672,
        [992672], 128, 227, False, False,
        LocationType.Item, LocationRestriction(0)), # Gondowan Cliffs Sleep Bomb
    LocationData(3908, 3908, 3908, 992684,
        [992684], 128, 384, False, True,
        LocationType.Item, LocationRestriction(0)), # Naribwe Thorn Crown
    LocationData(3909, 3909, 3909, 992692,
        [992692], 128, 266, False, True,
        LocationType.Item, LocationRestriction(0)), # Naribwe Unicorn Ring
    LocationData(3910, 3910, 3910, 992700,
        [992700], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Naribwe Elixir
    LocationData(3911, 3911, 3911, 992712,
        [992712], 2, 32786, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Naribwe 18 coins
    LocationData(3912, 3912, 3912, 992720,
        [992720], 2, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Naribwe Sleep Bomb
    LocationData(3913, 3913, 3913, 992732,
        [992732], 128, 191, False, False,
        LocationType.Item, LocationRestriction(0)), # Kibombo Mountains Power Bread
    LocationData(3914, 3914, 3914, 992740,
        [992740], 128, 429, False, True,
        LocationType.Item, LocationRestriction(0)), # Kibombo Mountains Tear Stone
    LocationData(3915, 3915, 3915, 992752,
        [992752], 128, 300, False, True,
        LocationType.Item, LocationRestriction(0)), # Kibombo Mountains Disk Axe
    LocationData(3916, 3916, 3916, 992764,
        [992764], 13, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Kibombo Mountains Smoke Bomb
    LocationData(3918, 3918, 3918, 992800,
        [992800, 992812], 2, 196, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Kibombo Lucky Pepper
    LocationData(3919, 3919, 3919, 992824,
        [992824], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Kibombo Lucky Medal
    LocationData(3920, 3920, 3920, 992832,
        [992832], 3, 181, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Kibombo Nut
    LocationData(3921, 3921, 3921, 992844,
        [992844], 128, 370, False, True,
        LocationType.Item, LocationRestriction(0)), # Gabomba Statue Bone Armlet
    LocationData(3698, 3698, 3698, 992852,
        [992852], 129, 2, False, False,
        LocationType.Item, LocationRestriction(3)), # Gabomba Statue Mimic
    LocationData(3922, 3922, 3922, 992864,
        [992864], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Gabomba Statue Elixir
    LocationData(3923, 3923, 3923, 992876,
        [992876], 131, 195, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Gabomba Catacombs Mint
    LocationData(3987, 3987, 3987, 992888,
        [992888], 131, 445, True, True,
        LocationType.Item, LocationRestriction(3)), # Gabomba Catacombs Tomegathericon
    LocationData(3924, 3924, 3924, 992900,
        [992900], 128, 183, False, False,
        LocationType.Item, LocationRestriction(0)), # Lemurian Ship Potion
    LocationData(3925, 3925, 3925, 992908,
        [992908], 3, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemurian Ship Elixir
    LocationData(3926, 3926, 3926, 992916,
        [992916], 13, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemurian Ship Antidote
    LocationData(3928, 3928, 3928, 992928,
        [992928], 128, 190, False, False,
        LocationType.Item, LocationRestriction(2)), # Lemurian Ship Mist Potion
    LocationData(3927, 3927, 3927, 992936,
        [992936, 992944], 3, 238, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemurian Ship Oil Drop
    LocationData(3929, 3929, 3929, 992968,
        [992968], 128, 426, False, True,
        LocationType.Item, LocationRestriction(0)), # Shrine of the Sea God Rusty Staff
    LocationData(2247, 2247, 2247, 992980,
        [992980], 131, 439, True, True,
        LocationType.Item, LocationRestriction(3)), # Shrine of the Sea God Right Prong
    LocationData(3930, 3930, 3930, 992992,
        [992992], 3, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # W Indra Islet Lucky Medal
    LocationData(3931, 3931, 3931, 993016,
        [993016], 13, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # SE Angara Islet Lucky Medal
    LocationData(3932, 3932, 3932, 993028,
        [993028], 3, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Sea of Time Islet Lucky Medal
    LocationData(3936, 3936, 3936, 993040,
        [993040], 131, 181, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam Nut
    LocationData(3937, 3937, 3937, 993048,
        [993048], 2, 32784, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam 16 coins
    LocationData(3938, 3938, 3938, 993056,
        [993056], 131, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam Antidote
    LocationData(3989, 3989, 3989, 993064,
        [993064], 128, 26, False, True,
        LocationType.Item, LocationRestriction(0)), # Yallam Masamune
    LocationData(3990, 3990, 3990, 993076,
        [993076], 13, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam Elixir
    LocationData(3991, 3991, 3991, 993084,
        [993084], 3, 238, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Yallam Oil Drop
    LocationData(3992, 3992, 3992, 993096,
        [993096], 128, 192, False, False,
        LocationType.Item, LocationRestriction(0)), # Taopo Swamp Cookie
    LocationData(3939, 3939, 3939, 993108,
        [993108], 131, 429, False, True,
        LocationType.Item, LocationRestriction(3)), # Taopo Swamp Tear Stone
    LocationData(3940, 3940, 3940, 993116,
        [993116], 131, 429, False, True,
        LocationType.Item, LocationRestriction(3)), # Taopo Swamp Tear Stone
    LocationData(3941, 3941, 3941, 993128,
        [993128], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Taopo Swamp Vial
    LocationData(3942, 3942, 3942, 993140,
        [993140], 131, 430, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Taopo Swamp Star Dust
    LocationData(3993, 3993, 3993, 993152,
        [993152], 131, 240, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Taopo Swamp Bramble Seed
    LocationData(3994, 3994, 3994, 993164,
        [993164], 131, 195, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands Mint
    LocationData(3995, 3995, 3995, 993172,
        [993172], 131, 180, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands Herb
    LocationData(3996, 3996, 3996, 993180,
        [993180], 2, 32950, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands 182 coins
    LocationData(3997, 3997, 3997, 993192,
        [993192], 3, 32800, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands 32 coins
    LocationData(3998, 3998, 3998, 993204,
        [993204], 131, 240, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Apojii Islands Bramble Seed
    LocationData(3944, 3944, 3944, 993216,
        [993216], 128, 181, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Nut
    LocationData(3945, 3945, 3945, 993224,
        [993224], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Elixir
    LocationData(3946, 3946, 3946, 993236,
        [993236], 128, 291, False, True,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Mist Sabre
    LocationData(3947, 3947, 3947, 993244,
        [993244], 128, 238, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Oil Drop
    LocationData(3948, 3948, 3948, 993256,
        [993256], 128, 189, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Water of Life
    LocationData(3699, 3699, 3699, 993268,
        [993268], 129, 3, False, False,
        LocationType.Item, LocationRestriction(3)), # Aqua Rock Mimic
    LocationData(3949, 3949, 3949, 993280,
        [993280], 128, 456, True, True,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Aquarius Stone
    LocationData(3950, 3950, 3950, 993288,
        [993288], 128, 196, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Lucky Pepper
    LocationData(3951, 3951, 3951, 993300,
        [993300], 128, 418, False, True,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Rusty Sword
    LocationData(3952, 3952, 3952, 993312,
        [993312], 128, 241, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Crystal Powder
    LocationData(3953, 3953, 3953, 993332,
        [993332], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Vial
    LocationData(3954, 3954, 3954, 993344,
        [993344], 128, 429, False, True,
        LocationType.Item, LocationRestriction(0)), # Aqua Rock Tear Stone
    LocationData(3999, 3999, 3999, 993360,
        [993360], 131, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Antidote
    LocationData(4000, 4000, 4000, 993368,
        [993368], 131, 187, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Antidote
    LocationData(4001, 4001, 4001, 993376,
        [993376], 131, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Lucky Medal
    LocationData(4002, 4002, 4002, 993384,
        [993384], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Elixir
    LocationData(4003, 4003, 4003, 993392,
        [993392], 2, 189, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Water of Life
    LocationData(4004, 4004, 4004, 993404,
        [993404], 2, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Smoke Bomb
    LocationData(4005, 4005, 4005, 993412,
        [993412], 13, 343, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Izumo Festival Coat
    LocationData(4006, 4006, 4006, 993432,
        [993432], 128, 334, False, True,
        LocationType.Item, LocationRestriction(0)), # Izumo Phantasmal Mail
    LocationData(3955, 3955, 3955, 993444,
        [993444], 128, 181, False, False,
        LocationType.Item, LocationRestriction(0)), # Gaia Rock Nut
    LocationData(3956, 3956, 3956, 993456,
        [993456], 131, 451, True, True,
        LocationType.Item, LocationRestriction(3)), # Gaia Rock Dancing Idol
    LocationData(3957, 3957, 3957, 993464,
        [993464], 128, 193, False, False,
        LocationType.Item, LocationRestriction(0)), # Gaia Rock Apple
    LocationData(3700, 3700, 3700, 993476,
        [993476], 129, 4, False, False,
        LocationType.Item, LocationRestriction(3)), # Gaia Rock Mimic
    LocationData(3958, 3958, 3958, 993484,
        [993484], 128, 423, False, True,
        LocationType.Item, LocationRestriction(0)), # Gaia Rock Rusty Mace
    LocationData(3649, 3649, 3649, 993492,
        [993492], 131, 283, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Gaia Rock Cloud Brand
    LocationData(4008, 4008, 4008, 993504,
        [993504], 128, 259, False, True,
        LocationType.Item, LocationRestriction(0)), # Islet Cave Turtle Boots
    LocationData(4009, 4009, 4009, 993512,
        [993512], 128, 425, False, True,
        LocationType.Item, LocationRestriction(0)), # Islet Cave Rusty Staff
    LocationData(4010, 4010, 4010, 993524,
        [993524], 128, 378, False, True,
        LocationType.Item, LocationRestriction(0)), # Champa Viking Helm
    LocationData(4011, 4011, 4011, 993532,
        [993532], 13, 226, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa Smoke Bomb
    LocationData(4012, 4012, 4012, 993540,
        [993540], 13, 32780, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa 12 coins
    LocationData(4013, 4013, 4013, 993548,
        [993548], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa Lucky Medal
    LocationData(4014, 4014, 4014, 993560,
        [993560], 13, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa Elixir
    LocationData(4015, 4015, 4015, 993572,
        [993572], 3, 227, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Champa Sleep Bomb
    LocationData(4016, 4016, 4016, 993584,
        [993584], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    LocationData(4017, 4017, 4017, 993592,
        [993592], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    LocationData(4018, 4018, 4018, 993600,
        [993600], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    LocationData(4019, 4019, 4019, 993608,
        [993608], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    LocationData(4020, 4020, 4020, 993616,
        [993616], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    LocationData(4021, 4021, 4021, 993624,
        [993624], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins ???
    LocationData(3959, 3959, 3959, 993632,
        [993632], 128, 32978, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins 210 coins
    LocationData(3960, 3960, 3960, 993640,
        [993640], 128, 181, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Nut
    LocationData(3961, 3961, 3961, 993652,
        [993652], 128, 241, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Crystal Powder
    LocationData(3962, 3962, 3962, 993664,
        [993664], 128, 311, False, True,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Thanatos Mace
    LocationData(3963, 3963, 3963, 993672,
        [993672], 128, 191, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Power Bread
    LocationData(3964, 3964, 3964, 993680,
        [993680], 128, 349, False, True,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Muni Robe
    LocationData(3965, 3965, 3965, 993692,
        [993692], 128, 33133, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins 365 coins
    LocationData(3966, 3966, 3966, 993700,
        [993700], 128, 431, False, True,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Sylph Feather
    LocationData(3967, 3967, 3967, 993708,
        [993708], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Vial
    LocationData(3903, 3903, 3903, 993720,
        [993720], 128, 183, False, False,
        LocationType.Item, LocationRestriction(0)), # Ankohl Ruins Potion
    LocationData(3968, 3968, 3968, 993732,
        [993732], 131, 440, True, True,
        LocationType.Item, LocationRestriction(3)), # Ankohl Ruins Left Prong
    LocationData(3969, 3969, 3969, 993744,
        [993744], 128, 431, False, True,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Sylph Feather
    LocationData(3970, 3970, 3970, 993752,
        [993752], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Lucky Medal
    LocationData(3971, 3971, 3971, 993760,
        [993760], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Vial
    LocationData(3972, 3972, 3972, 993768,
        [993768], 128, 281, False, True,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Lightning Sword
    LocationData(2373, 2373, 2373, 16384200,
        [16384200, 993776], 128, 441, True, True,
        LocationType.Item, LocationRestriction(11)), # Tundaria Tower Center Prong
    LocationData(3973, 3973, 3973, 993788,
        [993788], 128, 33133, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower 365 coins
    LocationData(3974, 3974, 3974, 993796,
        [993796], 128, 195, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Mint
    LocationData(3975, 3975, 3975, 993808,
        [993808], 128, 194, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Hard Nut
    LocationData(3976, 3976, 3976, 993816,
        [993816], 128, 241, False, False,
        LocationType.Item, LocationRestriction(0)), # Tundaria Tower Crystal Powder
    LocationData(2377, 2377, 2377, 993828,
        [993828], 131, 3735, True, True,
        LocationType.Item, LocationRestriction(3)), # Tundaria Tower Burst Brooch
    LocationData(4025, 4025, 4025, 993864,
        [993864], 131, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Lucky Medal
    LocationData(4026, 4026, 4026, 993872,
        [993872], 131, 417, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Rusty Sword
    LocationData(4027, 4027, 4027, 993880,
        [993880], 131, 194, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Hard Nut
    LocationData(4028, 4028, 4028, 993888,
        [993888], 131, 231, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Bone
    LocationData(4029, 4029, 4029, 993896,
        [993896], 131, 430, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Star Dust
    LocationData(3943, 3943, 3943, 993916,
        [993916], 128, 3736, True, True,
        LocationType.Item, LocationRestriction(0)), # Lemuria Grindstone
    LocationData(4031, 4031, 4031, 993924,
        [993924], 3, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Lemuria Lucky Medal
    LocationData(4032, 4032, 4032, 993936,
        [993936], 128, 430, False, True,
        LocationType.Item, LocationRestriction(0)), # Gondowan Settlement Star Dust
    LocationData(4033, 4033, 4033, 993948,
        [993948], 8, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Gondowan Settlement Lucky Medal
    LocationData(4034, 4034, 4034, 993960,
        [993960], 128, 32934, False, False,
        LocationType.Item, LocationRestriction(0)), # Hesperia Settlement 166 coins
    LocationData(4035, 4035, 4035, 993984,
        [993984], 128, 432, False, True,
        LocationType.Item, LocationRestriction(0)), # SW Atteka Islet Dragon Skin
    LocationData(4036, 4036, 4036, 993996,
        [993996], 128, 182, False, False,
        LocationType.Item, LocationRestriction(0)), # Atteka Inlet Vial
    LocationData(4037, 4037, 4037, 994016,
        [994016], 3, 191, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Contigo Power Bread
    LocationData(4038, 4038, 4038, 994024,
        [994024], 131, 233, False, False,
        LocationType.Item, LocationRestriction(3)), # Contigo Corn
    LocationData(4039, 4039, 4039, 994032,
        [994032], 131, 240, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Contigo Bramble Seed
    LocationData(4040, 4040, 4040, 994044,
        [994044], 128, 366, False, True,
        LocationType.Item, LocationRestriction(0)), # Shaman Village Spirit Gloves
    LocationData(4041, 4041, 4041, 994052,
        [994052], 2, 229, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Shaman Village Lucky Medal
    LocationData(4042, 4042, 4042, 994064,
        [994064], 3, 239, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Shaman Village Weasel's Claw
    LocationData(4043, 4043, 4043, 994072,
        [994072], 2, 188, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Shaman Village Elixir
    LocationData(4044, 4044, 4044, 994084,
        [994084], 2, 196, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Shaman Village Lucky Pepper
    LocationData(3935, 3935, 3935, 994096,
        [994096], 128, 194, False, False,
        LocationType.Item, LocationRestriction(0)), # Shaman Village Hard Nut
    LocationData(4045, 4045, 4045, 994108,
        [994108], 128, 32929, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle 161 coins
    LocationData(4046, 4046, 4046, 994116,
        [994116], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Lucky Medal
    LocationData(4047, 4047, 4047, 994124,
        [994124], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4048, 4048, 4048, 994132,
        [994132], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4049, 4049, 4049, 994140,
        [994140], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4050, 4050, 4050, 994148,
        [994148], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4051, 4051, 4051, 994160,
        [994160], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4052, 4052, 4052, 994168,
        [994168], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4053, 4053, 4053, 994176,
        [994176], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4054, 4054, 4054, 994184,
        [994184], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4055, 4055, 4055, 994192,
        [994192], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4056, 4056, 4056, 994200,
        [994200], 128, 0, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle ???
    LocationData(4057, 4057, 4057, 994208,
        [994208], 128, 33679, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle 911 coins
    LocationData(4058, 4058, 4058, 994216,
        [994216], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Psy Crystal
    LocationData(4059, 4059, 4059, 994224,
        [994224], 128, 192, False, False,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Cookie
    LocationData(4060, 4060, 4060, 994232,
        [994232], 128, 431, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Sylph Feather
    LocationData(4061, 4061, 4061, 994240,
        [994240], 128, 422, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Rusty Axe
    LocationData(4062, 4062, 4062, 994248,
        [994248], 128, 430, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Star Dust
    LocationData(4063, 4063, 4063, 994260,
        [994260], 128, 371, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Jester's Armlet
    LocationData(3701, 3701, 3701, 994268,
        [994268], 129, 5, False, False,
        LocationType.Item, LocationRestriction(3)), # Treasure Isle Mimic
    LocationData(4064, 4064, 4064, 994280,
        [994280], 128, 7, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Fire Brand
    LocationData(4065, 4065, 4065, 994288,
        [994288], 128, 351, False, True,
        LocationType.Item, LocationRestriction(0)), # Treasure Isle Iris Robe
    LocationData(4066, 4066, 4066, 994312,
        [994312], 131, 195, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Jupiter Lighthouse Mint
    LocationData(4067, 4067, 4067, 994336,
        [994336], 128, 344, False, True,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Erinyes Tunic
    LocationData(4068, 4068, 4068, 994348,
        [994348], 128, 183, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Potion
    LocationData(4069, 4069, 4069, 994356,
        [994356], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Psy Crystal
    LocationData(4070, 4070, 4070, 994368,
        [994368], 128, 319, False, True,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Meditation Rod
    LocationData(4071, 4071, 4071, 994376,
        [994376], 131, 243, True, True,
        LocationType.Item, LocationRestriction(3)), # Jupiter Lighthouse Red Key
    LocationData(3702, 3702, 3702, 994388,
        [994388], 129, 6, False, False,
        LocationType.Item, LocationRestriction(3)), # Jupiter Lighthouse Mimic
    LocationData(4072, 4072, 4072, 994396,
        [994396], 131, 244, True, True,
        LocationType.Item, LocationRestriction(3)), # Jupiter Lighthouse Blue Key
    LocationData(4073, 4073, 4073, 994404,
        [994404], 128, 190, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Mist Potion
    LocationData(4074, 4074, 4074, 994412,
        [994412], 128, 33074, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse 306 coins
    LocationData(4075, 4075, 4075, 994424,
        [994424], 128, 189, False, False,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Water of Life
    LocationData(4076, 4076, 4076, 994436,
        [994436], 128, 292, False, True,
        LocationType.Item, LocationRestriction(0)), # Jupiter Lighthouse Phaeton's Blade
    LocationData(4077, 4077, 4077, 994448,
        [994448], 128, 238, False, False,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Oil Drop
    LocationData(4078, 4078, 4078, 994460,
        [994460], 128, 33151, False, False,
        LocationType.Item, LocationRestriction(0)), # Magma Rock 383 coins
    LocationData(4079, 4079, 4079, 994468,
        [994468], 128, 433, False, True,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Salamander Tail
    LocationData(4080, 4080, 4080, 994480,
        [994480], 128, 229, False, False,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Lucky Medal
    LocationData(4081, 4081, 4081, 994492,
        [994492], 128, 190, False, False,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Mist Potion
    LocationData(4082, 4082, 4082, 994504,
        [994504], 128, 433, False, True,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Salamander Tail
    LocationData(4084, 4084, 4084, 994524,
        [994524], 128, 434, False, True,
        LocationType.Item, LocationRestriction(0)), # Magma Rock Golem Core
    LocationData(3703, 3703, 3703, 994536,
        [994536], 129, 7, False, False,
        LocationType.Item, LocationRestriction(3)), # Magma Rock Mimic
    LocationData(4085, 4085, 4085, 994548,
        [994548], 131, 435, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Loho Mythril Silver
    LocationData(4086, 4086, 4086, 994556,
        [994556], 131, 434, False, True,
        LocationType.Item, LocationRestriction(3)), # Loho Golem Core
    LocationData(4087, 4087, 4087, 994564,
        [994564], 131, 434, False, True,
        LocationType.Item, LocationRestriction(3)), # Loho Golem Core
    LocationData(4088, 4088, 4088, 994572,
        [994572], 3, 241, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Loho Crystal Powder
    LocationData(4089, 4089, 4089, 994584,
        [994584], 131, 436, False, True,
        LocationType.Item, LocationRestriction(3)), # Prox Dark Matter
    LocationData(4090, 4090, 4090, 994592,
        [994592], 2, 192, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Prox Cookie
    LocationData(4091, 4091, 4091, 994604,
        [994604], 2, 183, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Prox Potion
    LocationData(4092, 4092, 4092, 994612,
        [994612], 13, 236, False, False,
        LocationType.Hidden, LocationRestriction(3)), # Prox Sacred Feather
    LocationData(4093, 4093, 4093, 994624,
        [994624], 128, 193, False, False,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Apple
    LocationData(4094, 4094, 4094, 994636,
        [994636], 128, 3740, True, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Teleport Lapis
    LocationData(3704, 3704, 3704, 994644,
        [994644], 129, 8, False, False,
        LocationType.Item, LocationRestriction(3)), # Mars Lighthouse Mimic
    LocationData(4095, 4095, 4095, 994656,
        [994656], 128, 388, False, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Alastor's Hood
    LocationData(3584, 3584, 3584, 994668,
        [994668], 128, 437, False, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Orihalcon
    LocationData(3585, 3585, 3585, 994680,
        [994680], 128, 336, False, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Valkyrie Mail
    LocationData(3586, 3586, 3586, 994692,
        [994692], 128, 10, False, True,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Sol Blade
    LocationData(3587, 3587, 3587, 994704,
        [994704], 128, 186, False, False,
        LocationType.Item, LocationRestriction(0)), # Mars Lighthouse Psy Crystal
    LocationData(3588, 3588, 3588, 994716,
        [994716], 128, 432, False, True,
        LocationType.Item, LocationRestriction(0)), # Contigo Dragon Skin
    LocationData(3589, 3589, 3589, 994728,
        [994728], 128, 436, False, True,
        LocationType.Item, LocationRestriction(0)), # Anemos Inner Sanctum Dark Matter
    LocationData(3590, 3590, 3590, 994736,
        [994736], 128, 437, False, True,
        LocationType.Item, LocationRestriction(0)), # Anemos Inner Sanctum Orihalcon
    LocationData(3674, 3674, 3674, 994832,
        [994832], 128, 188, False, False,
        LocationType.Item, LocationRestriction(0)), # Shaman Village Elixir
    LocationData(3675, 3675, 3675, 994928,
        [994928], 133, 421, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Axe
    LocationData(3676, 3676, 3676, 994936,
        [994936], 133, 424, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Mace
    LocationData(3677, 3677, 3677, 994944,
        [994944], 133, 419, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Sword
    LocationData(3678, 3678, 3678, 994952,
        [994952], 133, 427, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Staff
    LocationData(3679, 3679, 3679, 994960,
        [994960], 133, 420, False, True,
        LocationType.Hidden, LocationRestriction(3)), # Overworld Rusty Sword
    LocationData(2122, 2122, 2122, 16384160,
        [16384160], 128, 3717, True, True,
        LocationType.Item, LocationRestriction(11)), # Kandorean Temple Lash Pebble
    LocationData(2168, 2168, 2168, 16384162,
        [16384162], 128, 3718, True, True,
        LocationType.Item, LocationRestriction(11)), # Dehkan Plateau Pound Cube
    LocationData(2188, 2188, 2188, 16384164,
        [16384164], 128, 3720, True, True,
        LocationType.Item, LocationRestriction(11)), # Yampi Desert Scoop Gem
    LocationData(2381, 2381, 2381, 16384168,
        [16384168], 128, 3737, True, True,
        LocationType.Item, LocationRestriction(11)), # Shaman Village Hover Jade
    LocationData(2618, 2618, 2618, 16384170,
        [16384170], 128, 222, True, True,
        LocationType.Item, LocationRestriction(11)), # Mars Lighthouse Mars Star
    LocationData(2303, 2303, 2303, 16384172,
        [16384172], 128, 242, True, True,
        LocationType.Item, LocationRestriction(11)), # Gabomba Statue Black Crystal
    LocationData(2424, 2424, 2424, 16384174,
        [16384174], 128, 326, True, True,
        LocationType.Item, LocationRestriction(11)), # Champa Trident
    LocationData(2722, 2722, 2722, 16384176,
        [16384176], 128, 452, True, True,
        LocationType.Trade, LocationRestriction(11)), # E Tundaria Islet Pretty Stone
    LocationData(2724, 2724, 2724, 16384178,
        [16384178], 128, 453, True, True,
        LocationType.Trade, LocationRestriction(11)), # SE Angara Islet Red Cloth
    LocationData(2723, 2723, 2723, 16384180,
        [16384180], 128, 454, True, True,
        LocationType.Trade, LocationRestriction(11)), # N Osenia Islet Milk
    LocationData(2721, 2721, 2721, 16384182,
        [16384182], 128, 455, True, True,
        LocationType.Trade, LocationRestriction(11)), # W Indra Islet Li'l Turtle
    LocationData(2592, 2592, 2592, 16384186,
        [16384186], 128, 458, True, True,
        LocationType.Item, LocationRestriction(11)), # Daila Sea God's Tear
    LocationData(2553, 2553, 2553, 16384188,
        [16384188], 128, 460, True, True,
        LocationType.Item, LocationRestriction(11)), # Magma Rock Magma Ball
    LocationData(1, 4, 1, 16384202,
        [16384202], 128, 65, True, True,
        LocationType.Item, LocationRestriction(15)), # Idejima Shaman's Rod
    LocationData(257, 3, 257, 16384210,
        [16384210], 128, 3731, True, True,
        LocationType.Item, LocationRestriction(14)), # Contigo Carry Stone
    LocationData(258, 2, 258, 16384212,
        [16384212], 128, 3727, True, True,
        LocationType.Item, LocationRestriction(14)), # Contigo Lifting Gem
    LocationData(259, 1, 259, 16384214,
        [16384214], 128, 3726, True, True,
        LocationType.Item, LocationRestriction(14)), # Contigo Orb of Force
    LocationData(260, 0, 260, 16384216,
        [16384216], 128, 3732, True, True,
        LocationType.Item, LocationRestriction(14)), # Contigo Catch Beads
    LocationData(261, 7, 261, 16384218,
        [16384218], 128, 3617, True, True,
        LocationType.Item, LocationRestriction(12)), # Kibombo Douse Drop
    LocationData(262, 7, 262, 16384220,
        [16384220], 128, 3608, True, True,
        LocationType.Item, LocationRestriction(12)), # Kibombo Frost Jewel
    LocationData(3328, 3328, 3328, 16384384,
        [16384384], 132, 3328, True, True,
        LocationType.Character, LocationRestriction(11)), # Contigo Isaac
    LocationData(3329, 3329, 3329, 16384386,
        [16384386], 132, 3329, True, True,
        LocationType.Character, LocationRestriction(11)), # Contigo Garet
    LocationData(3330, 3330, 3330, 16384388,
        [16384388], 132, 3330, True, True,
        LocationType.Character, LocationRestriction(11)), # Contigo Ivan
    LocationData(3331, 3331, 3331, 16384390,
        [16384390], 132, 3331, True, True,
        LocationType.Character, LocationRestriction(11)), # Contigo Mia
    LocationData(3333, 3333, 3333, 16384392,
        [16384392], 132, 3333, True, True,
        LocationType.Character, LocationRestriction(11)), # Idejima Jenna
    LocationData(3334, 3334, 3334, 16384394,
        [16384394], 132, 3334, True, True,
        LocationType.Character, LocationRestriction(11)), # Idejima Sheba
    LocationData(3335, 3335, 3335, 16384396,
        [16384396], 132, 3335, True, True,
        LocationType.Character, LocationRestriction(11)), # Kibombo Piers
    
]


def create_loctype_to_datamapping() -> Dict[str, List[LocationData]]:
    """Creates a dictionary mapping LocationType to a list of all locations
    of that type
    """
    types: Dict[str, List[LocationData]] = {}
    for idx, data in enumerate(all_locations):
        if data.loc_type not in types:
            types[data.loc_type] = []
        types[data.loc_type].append(data)
    return types

all_locations: List[LocationData] = djinn_locations + psyenergy_locations + summon_tablets + events + the_rest
location_name_to_data: Dict[str, LocationData] = {loc_names_by_id[location.ap_id]: location for location in all_locations if location.loc_type != LocationType.Event}
location_id_to_data: Dict[int, LocationData] = {location.ap_id: location for location in all_locations if location.loc_type != LocationType.Event}
assert len(all_locations) == len(location_id_to_data) + len(events)
location_type_to_data: Dict[str, List[LocationData]] = create_loctype_to_datamapping()