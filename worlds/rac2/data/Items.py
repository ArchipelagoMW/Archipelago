from dataclasses import dataclass
from abc import ABC

from typing import Callable, TYPE_CHECKING, Sequence, Optional, Dict, Set

if TYPE_CHECKING:
    from ..Rac2Interface import Rac2Interface


@dataclass
class ItemData(ABC):
    item_id: int
    name: str


def get_icon_id(item: ItemData) -> int:
    if isinstance(item, EquipmentData):
        return item.icon_id
    elif isinstance(item, CoordData):
        return 0xEA97  # Ship Icon
    elif item is PLATINUM_BOLT:
        return 0xEAA2  # PLat Bolt icon
    elif item is NANOTECH_BOOST:
        return 0xEA9E  # Plus Icon `+`
    else:
        return 0xEA75  # Question Mark icon `?`


@dataclass
class EquipmentData(ItemData):
    offset: int
    oclass_id: Optional[int] = 0x0047  # Wrench model
    icon_id: Optional[int] = 0xEA75    # Question Mark icon `?`

# Unreferenced equipment offsets:
#   - 00: ???
#   - 01: ???
#   - 04: "Hydro-Pack"
#   - 06: "Armor"
#   - 0A: "Wrench"
#   - 0B: ???
#   - 0F: Unused Weapon 1
#   - 21: ???
#   - 22: Unused Weapon 2
#   - 23: Unused Weapon 3
#   - 28: Unused Weapon 4
#   - 2F: "Megacorp Helmet
#   - 30: "Biker Helmet"
#   - 34: ???


# Gadgets/Items
HELI_PACK = EquipmentData(1, "Heli-Pack", 0x2, oclass_id=0x025F, icon_id=0xEA8D)
THRUSTER_PACK = EquipmentData(2, "Thruster-Pack", 0x3, oclass_id=0x0260, icon_id=0xEA7E)
MAPPER = EquipmentData(3, "Mapper", 0x5, oclass_id=0x1235, icon_id=0xEA9F)
ARMOR_MAGNETIZER = EquipmentData(4, "Armor Magnetizer", 0x7, oclass_id=0x112F, icon_id=0xEA9A)
LEVITATOR = EquipmentData(5, "Levitator", 0x8, oclass_id=0x096C, icon_id=0xEA90)
SWINGSHOT = EquipmentData(6, "Swingshot", 0xD, oclass_id=0x00D0, icon_id=0xEA8B)
GRAVITY_BOOTS = EquipmentData(7, "Gravity Boots", 0x13, oclass_id=0x00AD, icon_id=0xEA88)
GRIND_BOOTS = EquipmentData(8, "Grindboots", 0x14, oclass_id=0x00C3, icon_id=0xEA8C)
GLIDER = EquipmentData(9, "Glider", 0x15, icon_id=0xEA91)
DYNAMO = EquipmentData(10, "Dynamo", 0x24, oclass_id=0x0825, icon_id=0xEA7F)
ELECTROLYZER = EquipmentData(11, "Electrolyzer", 0x26, oclass_id=0x0870, icon_id=0xEA81)
THERMANATOR = EquipmentData(12, "Thermanator", 0x27, oclass_id=0x0FB0, icon_id=0xEA82)
TRACTOR_BEAM = EquipmentData(13, "Tractor Beam", 0x2E, oclass_id=0x00BC, icon_id=0xEA80)
QWARK_STATUETTE = EquipmentData(14, "Qwark Statuette", 0x31, icon_id=0xEA9C)
BOX_BREAKER = EquipmentData(15, "Box Breaker", 0x32, oclass_id=0x1238, icon_id=0xEAA1)
INFILTRATOR = EquipmentData(16, "Infiltrator", 0x33, oclass_id=0x0BD3, icon_id=0xEA83)
CHARGE_BOOTS = EquipmentData(17, "Charge Boots", 0x36, oclass_id=0x0E70, icon_id=0xEA89)
HYPNOMATIC = EquipmentData(18, "Hypnomatic", 0x37, oclass_id=0x0950, icon_id=0xEA84)


@dataclass
class WeaponData(EquipmentData):
    base_weapon_offset: int = None
    power: int = 0
    max_ammo: int = 0


# Weapons
CLANK_ZAPPER = WeaponData(
    101, "Clank Zapper", 0x09,
    oclass_id=0x0ED8, icon_id=0xEA99, power=0, max_ammo=30)
BOMB_GLOVE = WeaponData(
    102, "Bomb Glove", 0x0C,
    oclass_id=0x00C0, icon_id=0xEA79, power=4, max_ammo=40)
VISIBOMB_GUN = WeaponData(
    103, "Visibomb Gun", 0x0E,
    oclass_id=0x00A3, icon_id=0xEA7D, power=4, max_ammo=20)
SHEEPINATOR = WeaponData(
    104, "Sheepinator", 0x10,
    oclass_id=0x0A5D, icon_id=0xEA77, power=4)
DECOY_GLOVE = WeaponData(
    105, "Decoy Glove", 0x11,
    oclass_id=0x0232, icon_id=0xEA7B, power=0, max_ammo=20)
TESLA_CLAW = WeaponData(
    106, "Tesla Claw", 0x12,
    oclass_id=0x00B1, icon_id=0xEA7A, power=4, max_ammo=300)
CHOPPER = WeaponData(
    107, "Chopper", 0x16,
    oclass_id=0x0879, icon_id=0xEA66, power=4, max_ammo=35)
PULSE_RIFLE = WeaponData(
    108, "Pulse Rifle", 0x17,
    oclass_id=0x05CB, icon_id=0xEA68, power=5, max_ammo=8)
SEEKER_GUN = WeaponData(
    109, "Seeker Gun", 0x18,
    oclass_id=0x05CE, icon_id=0xEA6B, power=5, max_ammo=25)
HOVERBOMB_GUN = WeaponData(
    110, "Hoverbomb Gun", 0x19,
    oclass_id=0x0A5B, icon_id=0xEA72, power=9, max_ammo=10)
BLITZ_GUN = WeaponData(
    111, "Blitz Gun", 0x1A,
    oclass_id=0x05D1, icon_id=0xEA67, power=4, max_ammo=40)
MINIROCKET_TUBE = WeaponData(
    112, "Minirocket Tube", 0x1B,
    oclass_id=0x05CF, icon_id=0xEA70, power=7, max_ammo=20)
PLASMA_COIL = WeaponData(
    113, "Plasma Coil", 0x1C,
    oclass_id=0x0C4A, icon_id=0xEA71, power=8, max_ammo=10)
LAVA_GUN = WeaponData(
    114, "Lava Gun", 0x1D,
    oclass_id=0x05C9, icon_id=0xEA69, power=6, max_ammo=200)
LANCER = WeaponData(
    115, "Lancer", 0x1E,
    oclass_id=0x05D2, icon_id=0xEA64, power=3, max_ammo=200)
SYNTHENOID = WeaponData(
    116, "Synthenoid", 0x1F,
    oclass_id=0x0CB2, icon_id=0xEA6D, power=7, max_ammo=12)
SPIDERBOT_GLOVE = WeaponData(
    117, "Spiderbot Glove", 0x20,
    oclass_id=0x0907, icon_id=0xEA6E, power=4, max_ammo=8)
BOUNCER = WeaponData(
    118, "Bouncer", 0x25,
    oclass_id=0x0E14, icon_id=0xEA73, power=8, max_ammo=25)
MINITURRET_GLOVE = WeaponData(
    119, "Miniturret Glove", 0x29,
    oclass_id=0x0C5A, icon_id=0xEA6A, power=5, max_ammo=20)
GRAVITY_BOMB = WeaponData(
    120, "Gravity Bomb", 0x2A,
    oclass_id=0x0CE3, icon_id=0xEA65, power=3, max_ammo=8)
ZODIAC = WeaponData(
    121, "Zodiac", 0x2B,
    oclass_id=0x0EC8, icon_id=0xEA76, power=40, max_ammo=4)
RYNO_II = WeaponData(
    122, "RYNO II", 0x2C,
    oclass_id=0x0A67, icon_id=0xEA6C, power=40, max_ammo=100)
SHIELD_CHARGER = WeaponData(
    123, "Shield Charger", 0x2D,
    oclass_id=0x0A5C, icon_id=0xEA74, power=9, max_ammo=5)
WALLOPER = WeaponData(
    124, "Walloper", 0x35,
    oclass_id=0x00B4, icon_id=0xEA7C, power=4)

HEAVY_LANCER = WeaponData(
    125, "Heavy Lancer", 0x3C,
    oclass_id=0x0C05, icon_id=0xEA64, power=6, max_ammo=300, base_weapon_offset=LANCER.offset)
KILONOID = WeaponData(
    126, "Kilonoid", 0x3D,
    oclass_id=0x0B02, icon_id=0xEA6D, power=14, max_ammo=12, base_weapon_offset=SYNTHENOID.offset)
PLASMA_STORM = WeaponData(
    127, "Plasma Storm", 0x3E,
    oclass_id=0x05CA, icon_id=0xEA71, power=16, max_ammo=15, base_weapon_offset=PLASMA_COIL.offset)
METEOR_GUN = WeaponData(
    128, "Meteor Gun", 0x3F,
    oclass_id=0x0C59, icon_id=0xEA69, power=12, max_ammo=200, base_weapon_offset=LAVA_GUN.offset)
MEGATURRET_GLOVE = WeaponData(
    129, "Megaturret Glove", 0x40,
    oclass_id=0x0A65, icon_id=0xEA6A, power=10, max_ammo=20, base_weapon_offset=MINITURRET_GLOVE.offset)
MULTISTAR = WeaponData(
    130, "Multi-Star", 0x41,
    oclass_id=0x0AF6, icon_id=0xEA66, power=8, max_ammo=35, base_weapon_offset=CHOPPER.offset)
VAPORIZER = WeaponData(
    131, "Vaporizer", 0x42,
    oclass_id=0x0C04, icon_id=0xEA68, power=10, max_ammo=8, base_weapon_offset=PULSE_RIFLE.offset)
HK_22 = WeaponData(
    132, "HK-22", 0x43,
    oclass_id=0x0CEE, icon_id=0xEA6B, power=10, max_ammo=20, base_weapon_offset=SEEKER_GUN.offset)
BLITZ_CANNON = WeaponData(
    133, "Blitz Cannon", 0x44,
    oclass_id=0x0AF1, icon_id=0xEA67, power=8, max_ammo=40, base_weapon_offset=BLITZ_GUN.offset)
MEGAROCKET_CANNON = WeaponData(
    134, "Megarocket Cannon", 0x45,
    oclass_id=0x1004, icon_id=0xEA70, power=14, max_ammo=25, base_weapon_offset=MINIROCKET_TUBE.offset)
TETRABOMB_GUN = WeaponData(
    135, "Tetrabomb Gun", 0x46,
    oclass_id=0x0E2F, icon_id=0xEA72, power=18, max_ammo=10, base_weapon_offset=HOVERBOMB_GUN.offset)
MINI_NUKE = WeaponData(
    136, "Mini-Nuke", 0x47,
    oclass_id=0x0A5A, icon_id=0xEA65, power=6, max_ammo=8, base_weapon_offset=GRAVITY_BOMB.offset)
BLACK_SHEEPINATOR = WeaponData(
    137, "Black Sheepinator", 0x48,
    oclass_id=0x0EAD, icon_id=0xEA77, power=8, base_weapon_offset=SHEEPINATOR.offset)
CLANK_SHOCKER = WeaponData(
    138, "Clank Shocker", 0x49,
    oclass_id=0x0259, icon_id=0xEA99, power=0, max_ammo=10, base_weapon_offset=CLANK_ZAPPER.offset)
HEAVY_BOUNCER = WeaponData(
    139, "Heavy Bouncer", 0x4C,
    oclass_id=0x0E9E, icon_id=0xEA73, power=16, max_ammo=25, base_weapon_offset=BOUNCER.offset)
TESLA_BARRIER = WeaponData(
    140, "Tesla Barrier", 0x4D,
    oclass_id=0x1192, icon_id=0xEA74, power=18, max_ammo=5, base_weapon_offset=SHIELD_CHARGER.offset)
TANKBOT_GLOVE = WeaponData(
    141, "Tankbot Glove", 0x4E,
    oclass_id=0x0E7A, icon_id=0xEA6E, power=8, max_ammo=8, base_weapon_offset=SPIDERBOT_GLOVE.offset)

MEGA_HEAVY_LANCER = WeaponData(
    142, "Mega Heavy Lancer", 0x4F,
    oclass_id=0x0C05, icon_id=0xEA64, power=9, max_ammo=400, base_weapon_offset=LANCER.offset)
MEGA_MINI_NUKE = WeaponData(
    143, "Mega Mini-Nuke", 0x51,
    oclass_id=0x0A5A, icon_id=0xEA65, power=9, max_ammo=20, base_weapon_offset=GRAVITY_BOMB.offset)
MEGA_MULTISTAR = WeaponData(
    144, "Mega Multi-Star", 0x53,
    oclass_id=0x0AF6, icon_id=0xEA66, power=12, max_ammo=50, base_weapon_offset=CHOPPER.offset)
MEGA_HK_22 = WeaponData(
    145, "Mega HK-22", 0x55,
    oclass_id=0x0CEE, icon_id=0xEA6B, power=15, max_ammo=40, base_weapon_offset=SEEKER_GUN.offset)
MEGA_VAPORIZER = WeaponData(
    146, "Mega Vaporizer", 0x57,
    oclass_id=0x0C04, icon_id=0xEA68, power=15, max_ammo=12, base_weapon_offset=PULSE_RIFLE.offset)
MEGA_MEGATURRET_GLOVE = WeaponData(
    147, "Mega Megaturret Glove", 0x59,
    oclass_id=0x0A65, icon_id=0xEA6A, power=15, max_ammo=30, base_weapon_offset=MINITURRET_GLOVE.offset)
MEGA_BLITZ_CANNON = WeaponData(
    148, "Mega Blitz Cannon", 0x5B,
    oclass_id=0x0AF1, icon_id=0xEA67, power=12, max_ammo=50, base_weapon_offset=BLITZ_GUN.offset)
MEGA_KILONOID = WeaponData(
    149, "Mega Kilonoid", 0x5D,
    oclass_id=0x0B02, icon_id=0xEA6D, power=21, max_ammo=20, base_weapon_offset=SYNTHENOID.offset)
MEGA_METEOR_GUN = WeaponData(
    150, "Mega Meteor Gun", 0x5F,
    oclass_id=0x0C59, icon_id=0xEA69, power=18, max_ammo=300, base_weapon_offset=LAVA_GUN.offset)
MEGA_HEAVY_BOUNCER = WeaponData(
    151, "Mega Heavy Bouncer", 0x61,
    oclass_id=0x0E9E, icon_id=0xEA73, power=24, max_ammo=40, base_weapon_offset=BOUNCER.offset)
MEGA_MEGAROCKET_CANNON = WeaponData(
    152, "Mega Megarocket Cannon", 0x63,
    oclass_id=0x1004, icon_id=0xEA70, power=21, max_ammo=40, base_weapon_offset=MINIROCKET_TUBE.offset)
MEGA_PLASMA_STORM = WeaponData(
    153, "Mega Plasma Storm", 0x65,
    oclass_id=0x05CA, icon_id=0xEA71, power=24, max_ammo=25, base_weapon_offset=PLASMA_COIL.offset)
MEGA_TETRABOMB_GUN = WeaponData(
    154, "Mega Tetrabomb Gun", 0x67,
    oclass_id=0x0E2F, icon_id=0xEA72, power=27, max_ammo=15, base_weapon_offset=HOVERBOMB_GUN.offset)
MEGA_TANKBOT_GLOVE = WeaponData(
    155, "Mega Tankbot Glove", 0x69,
    oclass_id=0x0E7A, icon_id=0xEA6E, power=12, max_ammo=16, base_weapon_offset=SPIDERBOT_GLOVE.offset)
MEGA_TESLA_BARRIER = WeaponData(
    156, "Mega Tesla Barrier", 0x6B,
    oclass_id=0x1192, icon_id=0xEA74, power=27, max_ammo=10, base_weapon_offset=SHIELD_CHARGER.offset)
MEGA_TESLA_CLAW = WeaponData(
    157, "Mega Tesla Claw", 0x72,
    oclass_id=0x00B1, icon_id=0xEA7A, power=12, max_ammo=400, base_weapon_offset=TESLA_CLAW.offset)
MEGA_BOMB_GLOVE = WeaponData(
    158, "Mega Bomb Glove", 0x73,
    oclass_id=0x00C0, icon_id=0xEA79, power=12, max_ammo=60, base_weapon_offset=BOMB_GLOVE.offset)
MEGA_WALLOPER = WeaponData(
    159, "Mega Walloper", 0x74,
    oclass_id=0x00B4, icon_id=0xEA7C, power=12, base_weapon_offset=WALLOPER.offset)
MEGA_VISIBOMB_GUN = WeaponData(
    160, "Mega Visibomb Gun", 0x75,
    oclass_id=0x00A3, icon_id=0xEA7D, power=12, max_ammo=30, base_weapon_offset=VISIBOMB_GUN.offset)
MEGA_DECOY_GLOVE = WeaponData(
    161, "Mega Decoy Glove", 0x76,
    oclass_id=0x0232, icon_id=0xEA7B, power=0, max_ammo=30, base_weapon_offset=DECOY_GLOVE.offset)

ULTRA_HEAVY_LANCER = WeaponData(
    162, "Ultra Heavy Lancer", 0x50,
    oclass_id=0x0C05, icon_id=0xEA64, power=12, max_ammo=500, base_weapon_offset=LANCER.offset)
ULTRA_MINI_NUKE = WeaponData(
    163, "Ultra Mini-Nuke", 0x52,
    oclass_id=0x0A5A, icon_id=0xEA65, power=12, max_ammo=30, base_weapon_offset=GRAVITY_BOMB.offset)
ULTRA_MULTISTAR = WeaponData(
    164, "Ultra Multi-Star", 0x54,
    oclass_id=0x0AF6, icon_id=0xEA66, power=16, max_ammo=70, base_weapon_offset=CHOPPER.offset)
ULTRA_HK_22 = WeaponData(
    165, "Ultra HK-22", 0x56,
    oclass_id=0x0CEE, icon_id=0xEA6B, power=20, max_ammo=50, base_weapon_offset=SEEKER_GUN.offset)
ULTRA_VAPORIZER = WeaponData(
    166, "Ultra Vaporizer", 0x58,
    oclass_id=0x0C04, icon_id=0xEA68, power=20, max_ammo=20, base_weapon_offset=PULSE_RIFLE.offset)
ULTRA_MEGATURRET_GLOVE = WeaponData(
    167, "Ultra Megaturret Glove", 0x5A,
    oclass_id=0x0A65, icon_id=0xEA6A, power=20, max_ammo=50, base_weapon_offset=MINITURRET_GLOVE.offset)
ULTRA_BLITZ_CANNON = WeaponData(
    168, "Ultra Blitz Cannon", 0x5C,
    oclass_id=0x0AF1, icon_id=0xEA67, power=16, max_ammo=60, base_weapon_offset=BLITZ_GUN.offset)
ULTRA_KILONOID = WeaponData(
    169, "Ultra Kilonoid", 0x5E,
    oclass_id=0x0B02, icon_id=0xEA6D, power=28, max_ammo=40, base_weapon_offset=SYNTHENOID.offset)
ULTRA_METEOR_GUN = WeaponData(
    170, "Ultra Meteor Gun", 0x60,
    oclass_id=0x0C59, icon_id=0xEA69, power=24, max_ammo=400, base_weapon_offset=LAVA_GUN.offset)
ULTRA_HEAVY_BOUNCER = WeaponData(
    171, "Ultra Heavy Bouncer", 0x62,
    oclass_id=0x0E9E, icon_id=0xEA73, power=32, max_ammo=60, base_weapon_offset=BOUNCER.offset)
ULTRA_MEGAROCKET_CANNON = WeaponData(
    172, "Ultra Megarocket Cannon", 0x64,
    oclass_id=0x1004, icon_id=0xEA70, power=28, max_ammo=60, base_weapon_offset=MINIROCKET_TUBE.offset)
ULTRA_PLASMA_STORM = WeaponData(
    173, "Ultra Plasma Storm", 0x66,
    oclass_id=0x05CA, icon_id=0xEA71, power=32, max_ammo=50, base_weapon_offset=PLASMA_COIL.offset)
ULTRA_TETRABOMB_GUN = WeaponData(
    174, "Ultra Tetrabomb Gun", 0x68,
    oclass_id=0x0E2F, icon_id=0xEA72, power=36, max_ammo=25, base_weapon_offset=HOVERBOMB_GUN.offset)
ULTRA_TANKBOT_GLOVE = WeaponData(
    175, "Ultra Tankbot Glove", 0x6A,
    oclass_id=0x0E7A, icon_id=0xEA6E, power=16, max_ammo=24, base_weapon_offset=SPIDERBOT_GLOVE.offset)
ULTRA_TESLA_BARRIER = WeaponData(
    176, "Ultra Tesla Barrier", 0x6C,
    oclass_id=0x1192, icon_id=0xEA74, power=36, max_ammo=15, base_weapon_offset=SHIELD_CHARGER.offset)


@dataclass
class CoordData(ItemData):
    planet_number: int


# Coordinates
OOZLA_COORDS = CoordData(201, "Oozla Coordinates", 1)
MAKTAR_NEBULA_COORDS = CoordData(202, "Maktar Nebula Coordinates", 2)
ENDAKO_COORDS = CoordData(203, "Endako Coordinates", 3)
BARLOW_COORDS = CoordData(204, "Barlow Coordinates", 4)
FELTZIN_SYSTEM_COORDS = CoordData(205, "Feltzin System Coordinates", 5)
NOTAK_COORDS = CoordData(206, "Notak Coordinates", 6)
SIBERIUS_COORDS = CoordData(207, "Siberius Coordinates", 7)
TABORA_COORDS = CoordData(208, "Tabora Coordinates", 8)
DOBBO_COORDS = CoordData(209, "Dobbo Coordinates", 9)
HRUGIS_CLOUD_COORDS = CoordData(210, "Hrugis Cloud Coordinates", 10)
JOBA_COORDS = CoordData(211, "Joba Coordinates", 11)
TODANO_COORDS = CoordData(212, "Todano Coordinates", 12)
BOLDAN_COORDS = CoordData(213, "Boldan Coordinates", 13)
ARANOS_PRISON_COORDS = CoordData(214, "Aranos Prison Coordinates", 14)
GORN_COORDS = CoordData(215, "Gorn Coordinates", 15)
SNIVELAK_COORDS = CoordData(216, "Snivelak Coordinates", 16)
SMOLG_COORDS = CoordData(217, "Smolg Coordinates", 17)
DAMOSEL_COORDS = CoordData(218, "Damosel Coordinates", 18)
GRELBIN_COORDS = CoordData(219, "Grelbin Coordinates", 19)
YEEDIL_COORDS = CoordData(220, "Yeedil Coordinates", 20)


@dataclass
class CollectableData(ItemData):
    max_capacity: int = 0x7F


# Collectables
PLATINUM_BOLT = CollectableData(301, "Platinum Bolt", 40)
NANOTECH_BOOST = CollectableData(302, "Nanotech Boost", 10)
HYPNOMATIC_PART = CollectableData(303, "Hypnomatic Part", 3)
BOLT_PACK = CollectableData(304, "Bolt Pack")


@dataclass
class ProgressiveUpgradeData(ItemData):
    progressive_names: list[str]
    get_level_func: Callable[['Rac2Interface'], int]
    set_level_func: Callable[['Rac2Interface', int], bool]


WRENCH_UPGRADE = ProgressiveUpgradeData(401, "OmniWrench Upgrade", ["OmniWrench 10000", "OmniWrench 12000"],
                                        lambda interface: interface.get_wrench_level(),
                                        lambda interface, level: interface.set_wrench_level(level))

ARMOR_UPGRADE = ProgressiveUpgradeData(402, "Armor Upgrade", ["Tetrafiber Armor", "Duraplate Armor",
                                                              "Electrosteel Armor", "Carbonox Armor"],
                                       lambda interface: interface.get_armor_level(),
                                       lambda interface, level: interface.set_armor_level(level))

EQUIPMENT: Sequence[EquipmentData] = [
    HELI_PACK,
    THRUSTER_PACK,
    MAPPER,
    ARMOR_MAGNETIZER,
    LEVITATOR,
    SWINGSHOT,
    GRAVITY_BOOTS,
    GRIND_BOOTS,
    GLIDER,
    DYNAMO,
    ELECTROLYZER,
    THERMANATOR,
    TRACTOR_BEAM,
    QWARK_STATUETTE,
    BOX_BREAKER,
    INFILTRATOR,
    CHARGE_BOOTS,
    HYPNOMATIC,
]

# Keep in the correct order
MEGACORP_VENDOR_WEAPONS: Sequence[WeaponData] = [
    CHOPPER,
    BLITZ_GUN,
    PULSE_RIFLE,
    MINITURRET_GLOVE,
    SEEKER_GUN,
    SYNTHENOID,
    LAVA_GUN,
    BOUNCER,
    MINIROCKET_TUBE,
    SPIDERBOT_GLOVE,
    PLASMA_COIL,
    HOVERBOMB_GUN,
    SHIELD_CHARGER,
    ZODIAC,
    CLANK_ZAPPER,
]
# Keep in the correct order
GADGETRON_VENDOR_WEAPONS: Sequence[WeaponData] = [
    BOMB_GLOVE,
    VISIBOMB_GUN,
    TESLA_CLAW,
    DECOY_GLOVE,
    RYNO_II,
    WALLOPER,
]

LV1_WEAPONS: Sequence[WeaponData] = [
    CLANK_ZAPPER,           BOMB_GLOVE,                 VISIBOMB_GUN,               SHEEPINATOR,
    DECOY_GLOVE,            TESLA_CLAW,                 CHOPPER,                    PULSE_RIFLE,
    SEEKER_GUN,             HOVERBOMB_GUN,              BLITZ_GUN,                  MINIROCKET_TUBE,
    PLASMA_COIL,            LAVA_GUN,                   LANCER,                     SYNTHENOID,
    SPIDERBOT_GLOVE,        BOUNCER,                    MINITURRET_GLOVE,           GRAVITY_BOMB,
    ZODIAC,                 RYNO_II,                    SHIELD_CHARGER,             WALLOPER,
]
LV2_WEAPONS: Sequence[WeaponData] = [
    HEAVY_LANCER,           KILONOID,                   PLASMA_STORM,               METEOR_GUN,
    MEGATURRET_GLOVE,       MULTISTAR,                  VAPORIZER,                  HK_22,
    BLITZ_CANNON,           MEGAROCKET_CANNON,          TETRABOMB_GUN,              MINI_NUKE,
    BLACK_SHEEPINATOR,      CLANK_SHOCKER,              HEAVY_BOUNCER,              TESLA_BARRIER,
    TANKBOT_GLOVE,
]
LV3_WEAPONS: Sequence[WeaponData] = [
    MEGA_HEAVY_LANCER,      MEGA_MINI_NUKE,             MEGA_MULTISTAR,             MEGA_HK_22,
    MEGA_VAPORIZER,         MEGA_MEGATURRET_GLOVE,      MEGA_BLITZ_CANNON,          MEGA_KILONOID,
    MEGA_METEOR_GUN,        MEGA_HEAVY_BOUNCER,         MEGA_MEGAROCKET_CANNON,     MEGA_PLASMA_STORM,
    MEGA_TETRABOMB_GUN,     MEGA_TANKBOT_GLOVE,         MEGA_TESLA_BARRIER,         MEGA_TESLA_CLAW,
    MEGA_BOMB_GLOVE,        MEGA_WALLOPER,              MEGA_VISIBOMB_GUN,          MEGA_DECOY_GLOVE,
]
LV4_WEAPONS: Sequence[WeaponData] = [
    ULTRA_HEAVY_LANCER,     ULTRA_MINI_NUKE,            ULTRA_MULTISTAR,            ULTRA_HK_22,
    ULTRA_VAPORIZER,        ULTRA_MEGATURRET_GLOVE,     ULTRA_BLITZ_CANNON,         ULTRA_KILONOID,
    ULTRA_METEOR_GUN,       ULTRA_HEAVY_BOUNCER,        ULTRA_MEGAROCKET_CANNON,    ULTRA_PLASMA_STORM,
    ULTRA_TETRABOMB_GUN,    ULTRA_TANKBOT_GLOVE,        ULTRA_TESLA_BARRIER,
]
WEAPONS: Sequence[WeaponData] = [*LV1_WEAPONS, *LV2_WEAPONS, *LV3_WEAPONS, *LV4_WEAPONS]

COORDS: Sequence[CoordData] = [
    OOZLA_COORDS,
    MAKTAR_NEBULA_COORDS,
    ENDAKO_COORDS,
    BARLOW_COORDS,
    FELTZIN_SYSTEM_COORDS,
    NOTAK_COORDS,
    SIBERIUS_COORDS,
    TABORA_COORDS,
    DOBBO_COORDS,
    HRUGIS_CLOUD_COORDS,
    JOBA_COORDS,
    TODANO_COORDS,
    BOLDAN_COORDS,
    ARANOS_PRISON_COORDS,
    GORN_COORDS,
    SNIVELAK_COORDS,
    SMOLG_COORDS,
    DAMOSEL_COORDS,
    GRELBIN_COORDS,
    YEEDIL_COORDS,
]
STARTABLE_COORDS: Sequence[CoordData] = [
    OOZLA_COORDS,
    MAKTAR_NEBULA_COORDS,
    ENDAKO_COORDS,
    FELTZIN_SYSTEM_COORDS,
    NOTAK_COORDS,
    TODANO_COORDS,
]
COLLECTABLES: Sequence[CollectableData] = [
    PLATINUM_BOLT,
    NANOTECH_BOOST,
    HYPNOMATIC_PART,
    BOLT_PACK,
]
UPGRADES: Sequence[ProgressiveUpgradeData] = [
    WRENCH_UPGRADE,
    ARMOR_UPGRADE
]
ALL: Sequence[ItemData] = [*EQUIPMENT, *WEAPONS, *COORDS, *COLLECTABLES, *UPGRADES]
QUICK_SELECTABLE: Sequence[ItemData] = [
    *LV1_WEAPONS,
    SWINGSHOT,
    DYNAMO,
    THERMANATOR,
    TRACTOR_BEAM,
    HYPNOMATIC,
]


def from_id(item_id: int) -> ItemData:
    matching = [item for item in ALL if item.item_id == item_id]
    if len(matching) == 0:
        raise ValueError(f"No item data for item id '{item_id}'")
    assert len(matching) < 2, f"Multiple item data with id '{item_id}'. Please report."
    return matching[0]


def from_name(item_name: str) -> ItemData:
    matching = [item for item in ALL if item.name == item_name]
    if len(matching) == 0:
        raise ValueError(f"No item data for '{item_name}'")
    assert len(matching) < 2, f"Multiple item data with name '{item_name}'. Please report."
    return matching[0]


def from_offset(item_offset: int) -> EquipmentData:
    matching = [item for item in [*EQUIPMENT, *WEAPONS] if item.offset == item_offset]
    assert len(matching) > 0, f"No item data with offset '{item_offset}'."
    assert len(matching) < 2, f"Multiple item data with offset '{item_offset}'. Please report."
    return matching[0]


def coord_for_planet(number: int) -> CoordData:
    matching = [coord for coord in COORDS if coord.planet_number == number]
    assert len(matching) > 0, f"No coords for planet number '{number}'."
    assert len(matching) < 2, f"Multiple coords for planet number '{number}'. Please report."
    return matching[0]


def get_item_groups() -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {
        "Weapons": {w.name for w in WEAPONS},
        "Coordinates": {c.name for c in COORDS},
        "Equipment": {e.name for e in EQUIPMENT},
    }
    return groups
