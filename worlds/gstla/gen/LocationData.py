# This file was generated using jinja2 from a template. If this file needs
# to be changed, either change the template, or the code leveraging the template.
from typing import Callable, List, Dict, NamedTuple, Optional
from enum import Enum
from BaseClasses import Location, MultiWorld
from ItemNames import ItemName
from worlds.gstla.Locations import LocationType
from LocationNames import LocationName

#class LocationType(str, Enum):
#   Item = "Item"
#   Event = "Event"
#   Djinn = "Djinn"
#   Psyenergy = "Psyenergy"
#   Hidden = "Hidden"
#   Trade = "Trade"


def always_on(multiworld: MultiWorld, player: int) -> bool:
    return True

class LocationData(NamedTuple):
    flag: int
    id: Optional[int]
    addresses: int
    event_type: int
    vanilla_contents: int
    loc_type: LocationType = LocationType.Item
    event: bool = False
    included: Callable[[MultiWorld, int], bool] = always_on


class GSTLALocation(Location):
    game: str = "Golden Sun The Lost Age"

djinn_locations = [
LocationData(48, 0, 16384000, 128, 0, LocationType.Djinn), # Flint
LocationData(49, 1, 16384002, 128, 1, LocationType.Djinn), # Granite
LocationData(50, 2, 16384004, 128, 2, LocationType.Djinn), # Quartz
LocationData(51, 3, 16384006, 128, 3, LocationType.Djinn), # Vine
LocationData(52, 4, 16384008, 128, 4, LocationType.Djinn), # Sap
LocationData(53, 5, 16384010, 128, 5, LocationType.Djinn), # Ground
LocationData(54, 6, 16384012, 128, 6, LocationType.Djinn), # Bane
LocationData(55, 7, 16384014, 128, 7, LocationType.Djinn), # Echo
LocationData(56, 8, 16384016, 128, 8, LocationType.Djinn), # Iron
LocationData(57, 9, 16384018, 128, 9, LocationType.Djinn), # Steel
LocationData(58, 10, 16384020, 128, 10, LocationType.Djinn), # Mud
LocationData(59, 11, 16384022, 128, 11, LocationType.Djinn), # Flower
LocationData(60, 12, 16384024, 128, 12, LocationType.Djinn), # Meld
LocationData(61, 13, 16384026, 128, 13, LocationType.Djinn), # Petra
LocationData(62, 14, 16384028, 128, 14, LocationType.Djinn), # Salt
LocationData(63, 15, 16384030, 128, 15, LocationType.Djinn), # Geode
LocationData(64, 16, 16384032, 128, 16, LocationType.Djinn), # Mold
LocationData(65, 17, 16384034, 128, 17, LocationType.Djinn), # Crystal
LocationData(64, 0, 16384036, 128, 0, LocationType.Djinn), # Fizz
LocationData(65, 1, 16384038, 128, 1, LocationType.Djinn), # Sleet
LocationData(66, 2, 16384040, 128, 2, LocationType.Djinn), # Mist
LocationData(67, 3, 16384042, 128, 3, LocationType.Djinn), # Spritz
LocationData(68, 4, 16384044, 128, 4, LocationType.Djinn), # Hail
LocationData(69, 5, 16384046, 128, 5, LocationType.Djinn), # Tonic
LocationData(70, 6, 16384048, 128, 6, LocationType.Djinn), # Dew
LocationData(71, 7, 16384050, 128, 7, LocationType.Djinn), # Fog
LocationData(72, 8, 16384052, 128, 8, LocationType.Djinn), # Sour
LocationData(73, 9, 16384054, 128, 9, LocationType.Djinn), # Spring
LocationData(74, 10, 16384056, 128, 10, LocationType.Djinn), # Shade
LocationData(75, 11, 16384058, 128, 11, LocationType.Djinn), # Chill
LocationData(76, 12, 16384060, 128, 12, LocationType.Djinn), # Steam
LocationData(77, 13, 16384062, 128, 13, LocationType.Djinn), # Rime
LocationData(78, 14, 16384064, 128, 14, LocationType.Djinn), # Gel
LocationData(79, 15, 16384066, 128, 15, LocationType.Djinn), # Eddy
LocationData(80, 16, 16384068, 128, 16, LocationType.Djinn), # Balm
LocationData(81, 17, 16384070, 128, 17, LocationType.Djinn), # Serac
LocationData(80, 0, 16384072, 128, 0, LocationType.Djinn), # Forge
LocationData(81, 1, 16384074, 128, 1, LocationType.Djinn), # Fever
LocationData(82, 2, 16384076, 128, 2, LocationType.Djinn), # Corona
LocationData(83, 3, 16384078, 128, 3, LocationType.Djinn), # Scorch
LocationData(84, 4, 16384080, 128, 4, LocationType.Djinn), # Ember
LocationData(85, 5, 16384082, 128, 5, LocationType.Djinn), # Flash
LocationData(86, 6, 16384084, 128, 6, LocationType.Djinn), # Torch
LocationData(87, 7, 16384086, 128, 7, LocationType.Djinn), # Cannon
LocationData(88, 8, 16384088, 128, 8, LocationType.Djinn), # Spark
LocationData(89, 9, 16384090, 128, 9, LocationType.Djinn), # Kindle
LocationData(90, 10, 16384092, 128, 10, LocationType.Djinn), # Char
LocationData(91, 11, 16384094, 128, 11, LocationType.Djinn), # Coal
LocationData(92, 12, 16384096, 128, 12, LocationType.Djinn), # Reflux
LocationData(93, 13, 16384098, 128, 13, LocationType.Djinn), # Core
LocationData(94, 14, 16384100, 128, 14, LocationType.Djinn), # Tinder
LocationData(95, 15, 16384102, 128, 15, LocationType.Djinn), # Shine
LocationData(96, 16, 16384104, 128, 16, LocationType.Djinn), # Fury
LocationData(97, 17, 16384106, 128, 17, LocationType.Djinn), # Fugue
LocationData(96, 0, 16384108, 128, 0, LocationType.Djinn), # Gust
LocationData(97, 1, 16384110, 128, 1, LocationType.Djinn), # Breeze
LocationData(98, 2, 16384112, 128, 2, LocationType.Djinn), # Zephyr
LocationData(99, 3, 16384114, 128, 3, LocationType.Djinn), # Smog
LocationData(100, 4, 16384116, 128, 4, LocationType.Djinn), # Kite
LocationData(101, 5, 16384118, 128, 5, LocationType.Djinn), # Squall
LocationData(102, 6, 16384120, 128, 6, LocationType.Djinn), # Luff
LocationData(103, 7, 16384122, 128, 7, LocationType.Djinn), # Breath
LocationData(104, 8, 16384124, 128, 8, LocationType.Djinn), # Blitz
LocationData(105, 9, 16384126, 128, 9, LocationType.Djinn), # Ether
LocationData(106, 10, 16384128, 128, 10, LocationType.Djinn), # Waft
LocationData(107, 11, 16384130, 128, 11, LocationType.Djinn), # Haze
LocationData(108, 12, 16384132, 128, 12, LocationType.Djinn), # Wheeze
LocationData(109, 13, 16384134, 128, 13, LocationType.Djinn), # Aroma
LocationData(110, 14, 16384136, 128, 14, LocationType.Djinn), # Whorl
LocationData(111, 15, 16384138, 128, 15, LocationType.Djinn), # Gasp
LocationData(112, 16, 16384140, 128, 16, LocationType.Djinn), # Lull
LocationData(113, 17, 16384142, 128, 17, LocationType.Djinn), # Gale

]

summon_tablets = [
    LocationData(19, 19, 992068, 132, 3859, LocationType.Item), #Moloch
    LocationData(24, 24, 992212, 132, 3864, LocationType.Item), #Daedalus
    LocationData(18, 18, 992632, 132, 3858, LocationType.Item), #Flora
    LocationData(20, 20, 993424, 132, 3860, LocationType.Item), #Ulysses
    LocationData(25, 25, 994300, 132, 3865, LocationType.Item), #Azul
    LocationData(16, 16, 994844, 132, 3856, LocationType.Item), #Zagan
    LocationData(17, 17, 994856, 132, 3857, LocationType.Item), #Megaera
    LocationData(21, 21, 994868, 132, 3861, LocationType.Item), #Haures
    LocationData(23, 23, 994880, 132, 3863, LocationType.Item), #Coatlicue
    LocationData(26, 26, 994892, 132, 3866, LocationType.Item), #Catastrophe
    LocationData(27, 27, 994904, 132, 3867, LocationType.Item), #Charon
    LocationData(28, 28, 994916, 132, 3868, LocationType.Item), #Iris
    LocationData(2315, 2315, 16384198, 132, 3862, LocationType.Item), #Eclipse
    
]

psyenergy_locations = [
    LocationData(2260, 2260, 16384190, 132, 3728, LocationType.Psyenergy), # Reveal
    LocationData(2478, 2478, 16384192, 132, 3722, LocationType.Psyenergy), # Parch
    LocationData(2490, 2490, 16384194, 132, 3723, LocationType.Psyenergy), # Sand
    LocationData(2554, 2554, 16384196, 132, 3738, LocationType.Psyenergy), # Blaze
    LocationData(2, 2, 16384204, 132, 3725, LocationType.Psyenergy), # Mind Read
    LocationData(3, 3, 16384206, 132, 3662, LocationType.Psyenergy), # Whirlwind
    LocationData(4, 4, 16384208, 132, 3596, LocationType.Psyenergy), # Growth
    
]

events = [
    LocationData(0x778, None, LocationName.Mars_Lighthouse_Doom_Dragon, [0], 0, ItemName.Victory, LocationType.Event, True),
    LocationData(0x8AB, None, LocationName.Alhafra_Briggs, [0], 0, ItemName.Briggs_defeated, LocationType.Event, True),
    LocationData(0x97F, None, LocationName.Alhafra_Prison_Briggs, [0], 0, ItemName.Briggs_escaped, LocationType.Event, True),
    LocationData(0x8FF, None, LocationName.Gabombo_Statue, [0], 0, ItemName.Gabombo_Statue_Completed, LocationType.Event, True),
    LocationData(0x9EE, None, LocationName.Gaia_Rock_Serpent, [0], 0, ItemName.Serpent_defeated, LocationType.Event, True),
    # TODO: the emo tracker doesn't track this, so not sure what this is supposed to be?
    # TODO: is the flag 0x8DD?
    LocationData(0x8DD, None, LocationName.SeaOfTime_Poseidon, [0], 0, ItemName.Poseidon_defeated, LocationType.Event,True),
    LocationData(0x93F, None, LocationName.Lemurian_Ship_Aqua_Hydra, [0], 0, ItemName.Aqua_Hydra_defeated, LocationType.Event, True),
    LocationData(0x94D, None, LocationName.Shaman_Village_Moapa, [0], 0, ItemName.Moapa_defeated, LocationType.Event, True),
    LocationData(0xA21, None, LocationName.Jupiter_Lighthouse_Aeri_Agatio_and_Karst, [0], 0, ItemName.Jupiter_Beacon_Lit, LocationType.Event, True),
    LocationData(0xA4B, None, LocationName.Mars_Lighthouse_Flame_Dragons, [0], 0, ItemName.Flamedragons_defeated, LocationType.Event, True),
    LocationData(0x8DE, None, LocationName.Lemurian_Ship_Engine, [0], 0, ItemName.Ship, LocationType.Event, True)
]

the_rest = [
    LocationData(3841, 3841, 991776, 2, 180, LocationType.Hidden), # Daila Herb
    LocationData(3842, 3842, 991784, 3, 226, LocationType.Hidden), # Daila Smoke Bomb
    LocationData(3934, 3934, 991812, 131, 186, LocationType.Hidden), # Daila Psy Crystal
    LocationData(3858, 3858, 991824, 3, 229, LocationType.Hidden), # N Osenia Islet Lucky Medal
    LocationData(3843, 3843, 991832, 3, 227, LocationType.Hidden), # Daila Sleep Bomb
    LocationData(3844, 3844, 991840, 2, 32771, LocationType.Hidden), # Daila 3 coins
    LocationData(3845, 3845, 991848, 2, 32780, LocationType.Hidden), # Daila 12 coins
    LocationData(3846, 3846, 991860, 128, 443, LocationType.Item), # Kandorean Temple Mysterious Card
    LocationData(3696, 3696, 991872, 129, 0, LocationType.Item), # Kandorean Temple Mimic
    LocationData(3847, 3847, 991884, 128, 340, LocationType.Item), # Dehkan Plateau Full Metal Vest
    LocationData(3848, 3848, 991892, 128, 188, LocationType.Item), # Dehkan Plateau Elixir
    LocationData(3849, 3849, 991904, 128, 195, LocationType.Item), # Dehkan Plateau Mint
    LocationData(3850, 3850, 991916, 128, 301, LocationType.Item), # Dehkan Plateau Themis' Axe
    LocationData(3851, 3851, 991928, 128, 181, LocationType.Item), # Dehkan Plateau Nut
    LocationData(3852, 3852, 991940, 128, 383, LocationType.Item), # Madra Nurse's Cap
    LocationData(3853, 3853, 991948, 13, 187, LocationType.Hidden), # Madra Antidote
    LocationData(2328, 2328, 16384166, 128, 3721, LocationType.Item), # Madra Cyclone Chip
    LocationData(3854, 3854, 991968, 3, 226, LocationType.Hidden), # Madra Smoke Bomb
    LocationData(3855, 3855, 991976, 13, 32783, LocationType.Hidden), # Madra 15 coins
    LocationData(3856, 3856, 991984, 2, 227, LocationType.Hidden), # Madra Sleep Bomb
    LocationData(3857, 3857, 991996, 2, 188, LocationType.Hidden), # Madra Elixir
    LocationData(3859, 3859, 992008, 128, 193, LocationType.Item), # Madra Catacombs Apple
    LocationData(3906, 3906, 992016, 128, 190, LocationType.Item), # Madra Catacombs Mist Potion
    LocationData(3860, 3860, 992028, 128, 229, LocationType.Item), # Madra Catacombs Lucky Medal
    LocationData(3861, 3861, 992036, 128, 459, LocationType.Item), # Madra Catacombs Ruin Key
    LocationData(3862, 3862, 992060, 128, 3719, LocationType.Item), # Madra Catacombs Tremor Bit
    LocationData(3863, 3863, 992080, 128, 287, LocationType.Item), # Osenia Cliffs Pirate's Sword
    LocationData(3864, 3864, 992092, 128, 414, LocationType.Item), # Yampi Desert Guardian Ring
    LocationData(3865, 3865, 992104, 128, 187, LocationType.Item), # Yampi Desert Antidote
    LocationData(3977, 3977, 992128, 131, 33083, LocationType.Hidden), # Yampi Desert 315 coins
    LocationData(2190, 2190, 992140, 128, 229, LocationType.Item), # Yampi Desert Lucky Medal
    LocationData(3866, 3866, 992148, 128, 444, LocationType.Item), # Yampi Desert Trainer's Whip
    LocationData(3867, 3867, 992172, 128, 194, LocationType.Item), # Yampi Desert Hard Nut
    LocationData(3868, 3868, 992180, 128, 309, LocationType.Item), # Yampi Desert Blow Mace
    LocationData(3978, 3978, 992192, 128, 189, LocationType.Item), # Yampi Desert Cave Water of Life
    LocationData(3979, 3979, 992204, 131, 435, LocationType.Item), # Yampi Desert Cave Mythril Silver
    LocationData(3980, 3980, 992224, 128, 436, LocationType.Item), # Yampi Desert Cave Dark Matter
    LocationData(3981, 3981, 992232, 128, 437, LocationType.Item), # Yampi Desert Cave Orihalcon
    LocationData(3869, 3869, 992244, 128, 186, LocationType.Item), # Alhafra Psy Crystal
    LocationData(3870, 3870, 992252, 2, 227, LocationType.Hidden), # Alhafra Sleep Bomb
    LocationData(3871, 3871, 992260, 2, 229, LocationType.Hidden), # Alhafra Lucky Medal
    LocationData(3872, 3872, 992268, 13, 32800, LocationType.Hidden), # Alhafra 32 coins
    LocationData(3873, 3873, 992280, 2, 226, LocationType.Hidden), # Alhafra Smoke Bomb
    LocationData(3875, 3875, 992304, 3, 188, LocationType.Hidden), # Alhafra Elixir
    LocationData(3876, 3876, 992312, 2, 193, LocationType.Hidden), # Alhafra Apple
    LocationData(3877, 3877, 992324, 128, 32891, LocationType.Item), # Alhafran Cave 123 coins
    LocationData(3878, 3878, 992332, 128, 333, LocationType.Item), # Alhafran Cave Ixion Mail
    LocationData(3879, 3879, 992340, 128, 229, LocationType.Item), # Alhafran Cave Lucky Medal
    LocationData(3982, 3982, 992348, 2, 191, LocationType.Hidden), # Alhafran Cave Power Bread
    LocationData(3983, 3983, 992360, 128, 33545, LocationType.Item), # Alhafran Cave 777 coins
    LocationData(3984, 3984, 992368, 128, 183, LocationType.Item), # Alhafran Cave Potion
    LocationData(3985, 3985, 992376, 128, 186, LocationType.Item), # Alhafran Cave Psy Crystal
    LocationData(3880, 3880, 992388, 128, 32850, LocationType.Item), # Mikasalla 82 coins
    LocationData(3881, 3881, 992396, 13, 181, LocationType.Hidden), # Mikasalla Nut
    LocationData(3882, 3882, 992404, 3, 188, LocationType.Hidden), # Mikasalla Elixir
    LocationData(3883, 3883, 992416, 3, 196, LocationType.Hidden), # Mikasalla Lucky Pepper
    LocationData(3884, 3884, 992424, 2, 180, LocationType.Hidden), # Mikasalla Herb
    LocationData(3986, 3986, 992432, 2, 229, LocationType.Hidden), # E Tundaria Islet Lucky Medal
    LocationData(3885, 3885, 992444, 128, 290, LocationType.Item), # Garoh Hypnos' Sword
    LocationData(3886, 3886, 992456, 3, 181, LocationType.Hidden), # Garoh Nut
    LocationData(3887, 3887, 992464, 3, 226, LocationType.Hidden), # Garoh Smoke Bomb
    LocationData(3888, 3888, 992476, 2, 227, LocationType.Hidden), # Garoh Sleep Bomb
    LocationData(3889, 3889, 992484, 2, 188, LocationType.Hidden), # Garoh Elixir
    LocationData(3890, 3890, 992496, 128, 226, LocationType.Item), # Air's Rock Smoke Bomb
    LocationData(3891, 3891, 992504, 128, 192, LocationType.Item), # Air's Rock Cookie
    LocationData(3892, 3892, 992512, 128, 279, LocationType.Item), # Air's Rock Storm Brand
    LocationData(3697, 3697, 992520, 129, 1, LocationType.Item), # Air's Rock Mimic
    LocationData(3893, 3893, 992532, 128, 182, LocationType.Item), # Air's Rock Vial
    LocationData(3894, 3894, 992540, 128, 227, LocationType.Item), # Air's Rock Sleep Bomb
    LocationData(3895, 3895, 992552, 128, 358, LocationType.Item), # Air's Rock Fujin Shield
    LocationData(3896, 3896, 992564, 128, 182, LocationType.Item), # Air's Rock Vial
    LocationData(3897, 3897, 992584, 128, 394, LocationType.Item), # Air's Rock Clarity Circlet
    LocationData(3898, 3898, 992596, 128, 182, LocationType.Item), # Air's Rock Vial
    LocationData(3899, 3899, 992608, 128, 188, LocationType.Item), # Air's Rock Elixir
    LocationData(3900, 3900, 992620, 128, 186, LocationType.Item), # Air's Rock Psy Crystal
    LocationData(3901, 3901, 992644, 128, 33434, LocationType.Item), # Air's Rock 666 coins
    LocationData(3904, 3904, 992656, 131, 448, LocationType.Item), # Gondowan Cliffs Healing Fungus
    LocationData(3905, 3905, 992664, 131, 449, LocationType.Item), # Gondowan Cliffs Laughing Fungus
    LocationData(3907, 3907, 992672, 128, 227, LocationType.Item), # Gondowan Cliffs Sleep Bomb
    LocationData(3908, 3908, 992684, 128, 384, LocationType.Item), # Naribwe Thorn Crown
    LocationData(3909, 3909, 992692, 128, 266, LocationType.Item), # Naribwe Unicorn Ring
    LocationData(3910, 3910, 992700, 2, 188, LocationType.Hidden), # Naribwe Elixir
    LocationData(3911, 3911, 992712, 2, 32786, LocationType.Hidden), # Naribwe 18 coins
    LocationData(3912, 3912, 992720, 2, 227, LocationType.Hidden), # Naribwe Sleep Bomb
    LocationData(3913, 3913, 992732, 128, 191, LocationType.Item), # Kibombo Mountains Power Bread
    LocationData(3914, 3914, 992740, 128, 429, LocationType.Item), # Kibombo Mountains Tear Stone
    LocationData(3915, 3915, 992752, 128, 300, LocationType.Item), # Kibombo Mountains Disk Axe
    LocationData(3916, 3916, 992764, 13, 226, LocationType.Hidden), # Kibombo Mountains Smoke Bomb
    LocationData(3918, 3918, 992800, 2, 196, LocationType.Hidden), # Kibombo Lucky Pepper
    LocationData(3919, 3919, 992824, 2, 229, LocationType.Hidden), # Kibombo Lucky Medal
    LocationData(3920, 3920, 992832, 3, 181, LocationType.Hidden), # Kibombo Nut
    LocationData(3921, 3921, 992844, 128, 370, LocationType.Item), # Gabomba Statue Bone Armlet
    LocationData(3698, 3698, 992852, 129, 2, LocationType.Item), # Gabomba Statue Mimic
    LocationData(3922, 3922, 992864, 128, 188, LocationType.Item), # Gabomba Statue Elixir
    LocationData(3923, 3923, 992876, 131, 195, LocationType.Hidden), # Gabomba Catacombs Mint
    LocationData(3987, 3987, 992888, 131, 445, LocationType.Item), # Gabomba Catacombs Tomegathericon
    LocationData(3924, 3924, 992900, 128, 183, LocationType.Item), # Lemurian Ship Potion
    LocationData(3925, 3925, 992908, 3, 188, LocationType.Hidden), # Lemurian Ship Elixir
    LocationData(3926, 3926, 992916, 13, 187, LocationType.Hidden), # Lemurian Ship Antidote
    LocationData(3928, 3928, 992928, 128, 190, LocationType.Item), # Lemurian Ship Mist Potion
    LocationData(3927, 3927, 992936, 3, 238, LocationType.Hidden), # Lemurian Ship Oil Drop
    LocationData(3929, 3929, 992968, 128, 426, LocationType.Item), # Shrine of the Sea God Rusty Staff
    LocationData(2247, 2247, 992980, 131, 439, LocationType.Item), # Shrine of the Sea God Right Prong
    LocationData(3930, 3930, 992992, 3, 229, LocationType.Hidden), # W Indra Islet Lucky Medal
    LocationData(3931, 3931, 993016, 13, 229, LocationType.Hidden), # SE Angara Islet Lucky Medal
    LocationData(3932, 3932, 993028, 3, 229, LocationType.Hidden), # Sea of Time Islet Lucky Medal
    LocationData(3936, 3936, 993040, 131, 181, LocationType.Hidden), # Yallam Nut
    LocationData(3937, 3937, 993048, 2, 32784, LocationType.Hidden), # Yallam 16 coins
    LocationData(3938, 3938, 993056, 131, 187, LocationType.Hidden), # Yallam Antidote
    LocationData(3989, 3989, 993064, 128, 26, LocationType.Item), # Yallam Masamune
    LocationData(3990, 3990, 993076, 13, 188, LocationType.Hidden), # Yallam Elixir
    LocationData(3991, 3991, 993084, 3, 238, LocationType.Hidden), # Yallam Oil Drop
    LocationData(3992, 3992, 993096, 128, 192, LocationType.Item), # Taopo Swamp Cookie
    LocationData(3939, 3939, 993108, 131, 429, LocationType.Item), # Taopo Swamp Tear Stone
    LocationData(3940, 3940, 993116, 131, 429, LocationType.Item), # Taopo Swamp Tear Stone
    LocationData(3941, 3941, 993128, 128, 182, LocationType.Item), # Taopo Swamp Vial
    LocationData(3942, 3942, 993140, 131, 430, LocationType.Hidden), # Taopo Swamp Star Dust
    LocationData(3993, 3993, 993152, 131, 240, LocationType.Hidden), # Taopo Swamp Bramble Seed
    LocationData(3994, 3994, 993164, 131, 195, LocationType.Hidden), # Apojii Islands Mint
    LocationData(3995, 3995, 993172, 131, 180, LocationType.Hidden), # Apojii Islands Herb
    LocationData(3996, 3996, 993180, 2, 32950, LocationType.Hidden), # Apojii Islands 182 coins
    LocationData(3997, 3997, 993192, 3, 32800, LocationType.Hidden), # Apojii Islands 32 coins
    LocationData(3998, 3998, 993204, 131, 240, LocationType.Hidden), # Apojii Islands Bramble Seed
    LocationData(3944, 3944, 993216, 128, 181, LocationType.Item), # Aqua Rock Nut
    LocationData(3945, 3945, 993224, 128, 188, LocationType.Item), # Aqua Rock Elixir
    LocationData(3946, 3946, 993236, 128, 291, LocationType.Item), # Aqua Rock Mist Sabre
    LocationData(3947, 3947, 993244, 128, 238, LocationType.Item), # Aqua Rock Oil Drop
    LocationData(3948, 3948, 993256, 128, 189, LocationType.Item), # Aqua Rock Water of Life
    LocationData(3699, 3699, 993268, 129, 3, LocationType.Item), # Aqua Rock Mimic
    LocationData(3949, 3949, 993280, 128, 456, LocationType.Item), # Aqua Rock Aquarius Stone
    LocationData(3950, 3950, 993288, 128, 196, LocationType.Item), # Aqua Rock Lucky Pepper
    LocationData(3951, 3951, 993300, 128, 418, LocationType.Item), # Aqua Rock Rusty Sword
    LocationData(3952, 3952, 993312, 128, 241, LocationType.Item), # Aqua Rock Crystal Powder
    LocationData(3953, 3953, 993332, 128, 182, LocationType.Item), # Aqua Rock Vial
    LocationData(3954, 3954, 993344, 128, 429, LocationType.Item), # Aqua Rock Tear Stone
    LocationData(3999, 3999, 993360, 131, 187, LocationType.Hidden), # Izumo Antidote
    LocationData(4000, 4000, 993368, 131, 187, LocationType.Hidden), # Izumo Antidote
    LocationData(4001, 4001, 993376, 131, 229, LocationType.Hidden), # Izumo Lucky Medal
    LocationData(4002, 4002, 993384, 2, 188, LocationType.Hidden), # Izumo Elixir
    LocationData(4003, 4003, 993392, 2, 189, LocationType.Hidden), # Izumo Water of Life
    LocationData(4004, 4004, 993404, 2, 226, LocationType.Hidden), # Izumo Smoke Bomb
    LocationData(4005, 4005, 993412, 13, 343, LocationType.Hidden), # Izumo Festival Coat
    LocationData(4006, 4006, 993432, 128, 334, LocationType.Item), # Izumo Phantasmal Mail
    LocationData(3955, 3955, 993444, 128, 181, LocationType.Item), # Gaia Rock Nut
    LocationData(3956, 3956, 993456, 131, 451, LocationType.Item), # Gaia Rock Dancing Idol
    LocationData(3957, 3957, 993464, 128, 193, LocationType.Item), # Gaia Rock Apple
    LocationData(3700, 3700, 993476, 129, 4, LocationType.Item), # Gaia Rock Mimic
    LocationData(3958, 3958, 993484, 128, 423, LocationType.Item), # Gaia Rock Rusty Mace
    LocationData(3649, 3649, 993492, 131, 283, LocationType.Hidden), # Gaia Rock Cloud Brand
    LocationData(4008, 4008, 993504, 128, 259, LocationType.Item), # Islet Cave Turtle Boots
    LocationData(4009, 4009, 993512, 128, 425, LocationType.Item), # Islet Cave Rusty Staff
    LocationData(4010, 4010, 993524, 128, 378, LocationType.Item), # Champa Viking Helm
    LocationData(4011, 4011, 993532, 13, 226, LocationType.Hidden), # Champa Smoke Bomb
    LocationData(4012, 4012, 993540, 13, 32780, LocationType.Hidden), # Champa 12 coins
    LocationData(4013, 4013, 993548, 2, 229, LocationType.Hidden), # Champa Lucky Medal
    LocationData(4014, 4014, 993560, 13, 188, LocationType.Hidden), # Champa Elixir
    LocationData(4015, 4015, 993572, 3, 227, LocationType.Hidden), # Champa Sleep Bomb
    LocationData(4016, 4016, 993584, 128, 0, LocationType.Item), # Ankohl Ruins ???
    LocationData(4017, 4017, 993592, 128, 0, LocationType.Item), # Ankohl Ruins ???
    LocationData(4018, 4018, 993600, 128, 0, LocationType.Item), # Ankohl Ruins ???
    LocationData(4019, 4019, 993608, 128, 0, LocationType.Item), # Ankohl Ruins ???
    LocationData(4020, 4020, 993616, 128, 0, LocationType.Item), # Ankohl Ruins ???
    LocationData(4021, 4021, 993624, 128, 0, LocationType.Item), # Ankohl Ruins ???
    LocationData(3959, 3959, 993632, 128, 32978, LocationType.Item), # Ankohl Ruins 210 coins
    LocationData(3960, 3960, 993640, 128, 181, LocationType.Item), # Ankohl Ruins Nut
    LocationData(3961, 3961, 993652, 128, 241, LocationType.Item), # Ankohl Ruins Crystal Powder
    LocationData(3962, 3962, 993664, 128, 311, LocationType.Item), # Ankohl Ruins Thanatos Mace
    LocationData(3963, 3963, 993672, 128, 191, LocationType.Item), # Ankohl Ruins Power Bread
    LocationData(3964, 3964, 993680, 128, 349, LocationType.Item), # Ankohl Ruins Muni Robe
    LocationData(3965, 3965, 993692, 128, 33133, LocationType.Item), # Ankohl Ruins 365 coins
    LocationData(3966, 3966, 993700, 128, 431, LocationType.Item), # Ankohl Ruins Sylph Feather
    LocationData(3967, 3967, 993708, 128, 182, LocationType.Item), # Ankohl Ruins Vial
    LocationData(3903, 3903, 993720, 128, 183, LocationType.Item), # Ankohl Ruins Potion
    LocationData(3968, 3968, 993732, 131, 440, LocationType.Item), # Ankohl Ruins Left Prong
    LocationData(3969, 3969, 993744, 128, 431, LocationType.Item), # Tundaria Tower Sylph Feather
    LocationData(3970, 3970, 993752, 128, 229, LocationType.Item), # Tundaria Tower Lucky Medal
    LocationData(3971, 3971, 993760, 128, 182, LocationType.Item), # Tundaria Tower Vial
    LocationData(3972, 3972, 993768, 128, 281, LocationType.Item), # Tundaria Tower Lightning Sword
    LocationData(2373, 2373, 16384200, 128, 441, LocationType.Item), # Tundaria Tower Center Prong
    LocationData(3973, 3973, 993788, 128, 33133, LocationType.Item), # Tundaria Tower 365 coins
    LocationData(3974, 3974, 993796, 128, 195, LocationType.Item), # Tundaria Tower Mint
    LocationData(3975, 3975, 993808, 128, 194, LocationType.Item), # Tundaria Tower Hard Nut
    LocationData(3976, 3976, 993816, 128, 241, LocationType.Item), # Tundaria Tower Crystal Powder
    LocationData(2377, 2377, 993828, 131, 3735, LocationType.Item), # Tundaria Tower Burst Brooch
    LocationData(4025, 4025, 993864, 131, 229, LocationType.Hidden), # Lemuria Lucky Medal
    LocationData(4026, 4026, 993872, 131, 417, LocationType.Hidden), # Lemuria Rusty Sword
    LocationData(4027, 4027, 993880, 131, 194, LocationType.Hidden), # Lemuria Hard Nut
    LocationData(4028, 4028, 993888, 131, 231, LocationType.Hidden), # Lemuria Bone
    LocationData(4029, 4029, 993896, 131, 430, LocationType.Hidden), # Lemuria Star Dust
    LocationData(3943, 3943, 993916, 128, 3736, LocationType.Item), # Lemuria Grindstone
    LocationData(4031, 4031, 993924, 3, 229, LocationType.Hidden), # Lemuria Lucky Medal
    LocationData(4032, 4032, 993936, 128, 430, LocationType.Item), # Gondowan Settlement Star Dust
    LocationData(4033, 4033, 993948, 8, 229, LocationType.Hidden), # Gondowan Settlement Lucky Medal
    LocationData(4034, 4034, 993960, 128, 32934, LocationType.Item), # Hesperia Settlement 166 coins
    LocationData(4035, 4035, 993984, 128, 432, LocationType.Item), # SW Atteka Islet Dragon Skin
    LocationData(4036, 4036, 993996, 128, 182, LocationType.Item), # Atteka Inlet Vial
    LocationData(4037, 4037, 994016, 3, 191, LocationType.Hidden), # Contigo Power Bread
    LocationData(4038, 4038, 994024, 131, 233, LocationType.Item), # Contigo Corn
    LocationData(4039, 4039, 994032, 131, 240, LocationType.Hidden), # Contigo Bramble Seed
    LocationData(4040, 4040, 994044, 128, 366, LocationType.Item), # Shaman Village Spirit Gloves
    LocationData(4041, 4041, 994052, 2, 229, LocationType.Hidden), # Shaman Village Lucky Medal
    LocationData(4042, 4042, 994064, 3, 239, LocationType.Hidden), # Shaman Village Weasel's Claw
    LocationData(4043, 4043, 994072, 2, 188, LocationType.Hidden), # Shaman Village Elixir
    LocationData(4044, 4044, 994084, 2, 196, LocationType.Hidden), # Shaman Village Lucky Pepper
    LocationData(3935, 3935, 994096, 128, 194, LocationType.Item), # Shaman Village Hard Nut
    LocationData(4045, 4045, 994108, 128, 32929, LocationType.Item), # Treasure Isle 161 coins
    LocationData(4046, 4046, 994116, 128, 229, LocationType.Item), # Treasure Isle Lucky Medal
    LocationData(4047, 4047, 994124, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4048, 4048, 994132, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4049, 4049, 994140, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4050, 4050, 994148, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4051, 4051, 994160, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4052, 4052, 994168, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4053, 4053, 994176, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4054, 4054, 994184, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4055, 4055, 994192, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4056, 4056, 994200, 128, 0, LocationType.Item), # Treasure Isle ???
    LocationData(4057, 4057, 994208, 128, 33679, LocationType.Item), # Treasure Isle 911 coins
    LocationData(4058, 4058, 994216, 128, 186, LocationType.Item), # Treasure Isle Psy Crystal
    LocationData(4059, 4059, 994224, 128, 192, LocationType.Item), # Treasure Isle Cookie
    LocationData(4060, 4060, 994232, 128, 431, LocationType.Item), # Treasure Isle Sylph Feather
    LocationData(4061, 4061, 994240, 128, 422, LocationType.Item), # Treasure Isle Rusty Axe
    LocationData(4062, 4062, 994248, 128, 430, LocationType.Item), # Treasure Isle Star Dust
    LocationData(4063, 4063, 994260, 128, 371, LocationType.Item), # Treasure Isle Jester's Armlet
    LocationData(3701, 3701, 994268, 129, 5, LocationType.Item), # Treasure Isle Mimic
    LocationData(4064, 4064, 994280, 128, 7, LocationType.Item), # Treasure Isle Fire Brand
    LocationData(4065, 4065, 994288, 128, 351, LocationType.Item), # Treasure Isle Iris Robe
    LocationData(4066, 4066, 994312, 131, 195, LocationType.Hidden), # Jupiter Lighthouse Mint
    LocationData(4067, 4067, 994336, 128, 344, LocationType.Item), # Jupiter Lighthouse Erinyes Tunic
    LocationData(4068, 4068, 994348, 128, 183, LocationType.Item), # Jupiter Lighthouse Potion
    LocationData(4069, 4069, 994356, 128, 186, LocationType.Item), # Jupiter Lighthouse Psy Crystal
    LocationData(4070, 4070, 994368, 128, 319, LocationType.Item), # Jupiter Lighthouse Meditation Rod
    LocationData(4071, 4071, 994376, 131, 243, LocationType.Item), # Jupiter Lighthouse Red Key
    LocationData(3702, 3702, 994388, 129, 6, LocationType.Item), # Jupiter Lighthouse Mimic
    LocationData(4072, 4072, 994396, 131, 244, LocationType.Item), # Jupiter Lighthouse Blue Key
    LocationData(4073, 4073, 994404, 128, 190, LocationType.Item), # Jupiter Lighthouse Mist Potion
    LocationData(4074, 4074, 994412, 128, 33074, LocationType.Item), # Jupiter Lighthouse 306 coins
    LocationData(4075, 4075, 994424, 128, 189, LocationType.Item), # Jupiter Lighthouse Water of Life
    LocationData(4076, 4076, 994436, 128, 292, LocationType.Item), # Jupiter Lighthouse Phaeton's Blade
    LocationData(4077, 4077, 994448, 128, 238, LocationType.Item), # Magma Rock Oil Drop
    LocationData(4078, 4078, 994460, 128, 33151, LocationType.Item), # Magma Rock 383 coins
    LocationData(4079, 4079, 994468, 128, 433, LocationType.Item), # Magma Rock Salamander Tail
    LocationData(4080, 4080, 994480, 128, 229, LocationType.Item), # Magma Rock Lucky Medal
    LocationData(4081, 4081, 994492, 128, 190, LocationType.Item), # Magma Rock Mist Potion
    LocationData(4082, 4082, 994504, 128, 433, LocationType.Item), # Magma Rock Salamander Tail
    LocationData(4084, 4084, 994524, 128, 434, LocationType.Item), # Magma Rock Golem Core
    LocationData(3703, 3703, 994536, 129, 7, LocationType.Item), # Magma Rock Mimic
    LocationData(4085, 4085, 994548, 131, 435, LocationType.Hidden), # Loho Mythril Silver
    LocationData(4086, 4086, 994556, 131, 434, LocationType.Item), # Loho Golem Core
    LocationData(4087, 4087, 994564, 131, 434, LocationType.Hidden), # Loho Golem Core
    LocationData(4088, 4088, 994572, 3, 241, LocationType.Hidden), # Loho Crystal Powder
    LocationData(4089, 4089, 994584, 131, 436, LocationType.Item), # Prox Dark Matter
    LocationData(4090, 4090, 994592, 2, 192, LocationType.Hidden), # Prox Cookie
    LocationData(4091, 4091, 994604, 2, 183, LocationType.Hidden), # Prox Potion
    LocationData(4092, 4092, 994612, 13, 236, LocationType.Hidden), # Prox Sacred Feather
    LocationData(4093, 4093, 994624, 128, 193, LocationType.Item), # Mars Lighthouse Apple
    LocationData(4094, 4094, 994636, 128, 3740, LocationType.Item), # Mars Lighthouse Teleport Lapis
    LocationData(3704, 3704, 994644, 129, 8, LocationType.Item), # Mars Lighthouse Mimic
    LocationData(4095, 4095, 994656, 128, 388, LocationType.Item), # Mars Lighthouse Alastor's Hood
    LocationData(3584, 3584, 994668, 128, 437, LocationType.Item), # Mars Lighthouse Orihalcon
    LocationData(3585, 3585, 994680, 128, 336, LocationType.Item), # Mars Lighthouse Valkyrie Mail
    LocationData(3586, 3586, 994692, 128, 10, LocationType.Item), # Mars Lighthouse Sol Blade
    LocationData(3587, 3587, 994704, 128, 186, LocationType.Item), # Mars Lighthouse Psy Crystal
    LocationData(3588, 3588, 994716, 128, 432, LocationType.Item), # Contigo Dragon Skin
    LocationData(3589, 3589, 994728, 128, 436, LocationType.Item), # Anemos Inner Sanctum Dark Matter
    LocationData(3590, 3590, 994736, 128, 437, LocationType.Item), # Anemos Inner Sanctum Orihalcon
    LocationData(3674, 3674, 994832, 128, 188, LocationType.Item), # Shaman Village Elixir
    LocationData(3675, 3675, 994928, 133, 421, LocationType.Hidden), # Overworld Rusty Axe
    LocationData(3676, 3676, 994936, 133, 424, LocationType.Hidden), # Overworld Rusty Mace
    LocationData(3677, 3677, 994944, 133, 419, LocationType.Hidden), # Overworld Rusty Sword
    LocationData(3678, 3678, 994952, 133, 427, LocationType.Hidden), # Overworld Rusty Staff
    LocationData(3679, 3679, 994960, 133, 420, LocationType.Hidden), # Overworld Rusty Sword
    LocationData(2122, 2122, 16384160, 128, 3717, LocationType.Item), # Kandorean Temple Lash Pebble
    LocationData(2168, 2168, 16384162, 128, 3718, LocationType.Item), # Dehkan Plateau Pound Cube
    LocationData(2188, 2188, 16384164, 128, 3720, LocationType.Item), # Yampi Desert Scoop Gem
    LocationData(2381, 2381, 16384168, 128, 3737, LocationType.Item), # Shaman Village Hover Jade
    LocationData(2618, 2618, 16384170, 128, 222, LocationType.Item), # Mars Lighthouse Mars Star
    LocationData(2303, 2303, 16384172, 128, 242, LocationType.Item), # Gabomba Statue Black Crystal
    LocationData(2424, 2424, 16384174, 128, 326, LocationType.Item), # Champa Trident
    LocationData(2722, 2722, 16384176, 128, 452, LocationType.Trade), # E Tundaria Islet Pretty Stone
    LocationData(2724, 2724, 16384178, 128, 453, LocationType.Trade), # SE Angara Islet Red Cloth
    LocationData(2723, 2723, 16384180, 128, 454, LocationType.Trade), # N Osenia Islet Milk
    LocationData(2721, 2721, 16384182, 128, 455, LocationType.Trade), # W Indra Islet Li'l Turtle
    LocationData(2592, 2592, 16384186, 128, 458, LocationType.Item), # Daila Sea God's Tear
    LocationData(2553, 2553, 16384188, 128, 460, LocationType.Item), # Magma Rock Magma Ball
    LocationData(1, 1, 16384202, 128, 65, LocationType.Item), # Idejima Shaman's Rod
    LocationData(257, 257, 16384210, 128, 3731, LocationType.Item), # Contigo Carry Stone
    LocationData(258, 258, 16384212, 128, 3727, LocationType.Item), # Contigo Lifting Gem
    LocationData(259, 259, 16384214, 128, 3726, LocationType.Item), # Contigo Orb of Force
    LocationData(260, 260, 16384216, 128, 3732, LocationType.Item), # Contigo Catch Beads
    LocationData(261, 261, 16384218, 128, 3617, LocationType.Item), # Kibombo Douse Drop
    LocationData(262, 262, 16384220, 128, 3608, LocationType.Item), # Kibombo Frost Jewel
    
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

all_locations: List[LocationData] = djinn_locations + psyenergy_locations + summon_tablets + events
location_name_to_data: Dict[str, LocationData] = {location.name: location for location in all_locations if location.loc_type != LocationType.Event}
location_id_to_data: Dict[int, LocationData] = {location.id: location for location in all_locations if location.loc_type != LocationType.Event}
location_flag_to_data: Dict[int, LocationData] = {location.id: location for location in all_locations if location.loc_type != LocationType.Event}
location_type_to_data: Dict[str, List[LocationData]] = create_loctype_to_datamapping()