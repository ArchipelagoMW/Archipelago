from BaseClasses import Item
from dataclasses import dataclass
from typing import Sequence, Dict, Set


@dataclass
class ItemData(Item):
    item_id: int
    name: str


HELI_PACK = ItemData(2, "Heli Pack")
THRUSTER_PACK = ItemData(3, "Thruster Pack")
HYDRO_PACK = ItemData(4, "Hydro Pack")
SONIC_SUMMONER = ItemData(5, "Sonic Summoner")
O2_MASK = ItemData(6, "O2 Mask")
PILOTS_HELMET = ItemData(7, "Pilots Helmet")
SUCK_CANNON = ItemData(9, "Suck_cannon")
BOMB_GLOVE = ItemData(10, "Bomb_glove")
DEVASTATOR = ItemData(11, "Devastator")
SWINGSHOT = ItemData(12, "Swingshot")
VISIBOMB = ItemData(13, "Visibomb")
TAUNTER = ItemData(14, "Taunter")
BLASTER = ItemData(15, "Blaster")
PYROCITOR = ItemData(16, "Pyrocitor")
MINE_GLOVE = ItemData(17, "Mine_glove")
WALLOPER = ItemData(18, "Walloper")
TESLA_CLAW = ItemData(19, "Tesla_claw")
GLOVE_OF_DOOM = ItemData(20, "Glove_of_doom")
MORPH_O_RAY = ItemData(21, "Morph_o_ray")
HYDRODISPLACER = ItemData(22, "Hydrodisplacer")
RYNO = ItemData(23, "RYNO")
DRONE_DEVICE = ItemData(24, "Drone_device")
DECOY_GLOVE = ItemData(25, "Decoy_glove")
TRESPASSER = ItemData(26, "Trespasser")
METAL_DETECTOR = ItemData(27, "Metal Detector")
MAGNEBOOTS = ItemData(28, "Magneboots")
GRINDBOOTS = ItemData(29, "Grindboots")
HOVERBOARD = ItemData(30, "Hoverboard")
HOLOGUISE = ItemData(31, "Hologuise")
PDA = ItemData(32, "PDA")
MAP_O_MATIC = ItemData(33, "Map O Matic")
BOLT_GRABBER = ItemData(34, "Bolt Grabber")
PERSUADER = ItemData(35, "Persuader")

ZOOMERATOR = ItemData(48, "Zoomerator")
RARITANIUM = ItemData(49, "Raritanium")
CODEBOT = ItemData(50, "Codebot")
PREMIUM_NANOTECH = ItemData(52, "Premium_nanotech")
ULTRA_NANOTECH = ItemData(53, "Ultra_nanotech")

NOVALIS_INFOBOT = ItemData(101, "Novalis")
ARIDIA_INFOBOT = ItemData(102, "Aridia")
KERWAN_INFOBOT = ItemData(103, "Kerwan")
EUDORA_INFOBOT = ItemData(104, "Eudora")
RILGAR_INFOBOT = ItemData(105, "Rilgar")
BLARG_INFOBOT = ItemData(106, "Blarg")
UMBRIS_INFOBOT = ItemData(107, "Umbris")
BATALIA_INFOBOT = ItemData(108, "Batalia")
GASPAR_INFOBOT = ItemData(109, "Gaspar")
ORXON_INFOBOT = ItemData(110, "Orxon")
POKITARU_INFOBOT = ItemData(111, "Pokitaru")
HOVEN_INFOBOT = ItemData(112, "Hoven")
GEMLIK_INFOBOT = ItemData(113, "Gemlik")
OLTANIS_INFOBOT = ItemData(114, "Oltanis")
QUARTU_INFOBOT = ItemData(115, "Quartu")
KALEBO_INFOBOT = ItemData(116, "Kalebo III")
FLEET_INFOBOT = ItemData(117, "Drek's Fleet")
VELDIN_INFOBOT = ItemData(118, "Veldin")


@dataclass
class CollectableData(ItemData):
    max_capacity: int = 0x7F


# Collectables
GOLD_BOLT = CollectableData(301, "Gold Bolt", 40)

EQUIPMENT: Sequence[ItemData] = [
    HELI_PACK,
    THRUSTER_PACK,
    HYDRO_PACK,
    SONIC_SUMMONER,
    O2_MASK,
    PILOTS_HELMET,
    TAUNTER,
    HYDRODISPLACER,
    TRESPASSER,
    METAL_DETECTOR,
    MAGNEBOOTS,
    GRINDBOOTS,
    HOVERBOARD,
    HOLOGUISE,
    PDA,
    MAP_O_MATIC,
    BOLT_GRABBER,
    PERSUADER,
    ZOOMERATOR,
    RARITANIUM,
    CODEBOT,
    PREMIUM_NANOTECH,
    ULTRA_NANOTECH,
    SWINGSHOT,
    DRONE_DEVICE,
]

WEAPONS: Sequence[ItemData] = [
    SUCK_CANNON,
    BOMB_GLOVE,
    DEVASTATOR,
    VISIBOMB,
    BLASTER,
    PYROCITOR,
    MINE_GLOVE,
    WALLOPER,
    TESLA_CLAW,
    GLOVE_OF_DOOM,
    MORPH_O_RAY,
    RYNO,
    DECOY_GLOVE,
]

PLANETS: Sequence[ItemData] = [
    NOVALIS_INFOBOT,
    ARIDIA_INFOBOT,
    KERWAN_INFOBOT,
    EUDORA_INFOBOT,
    RILGAR_INFOBOT,
    BLARG_INFOBOT,
    UMBRIS_INFOBOT,
    BATALIA_INFOBOT,
    GASPAR_INFOBOT,
    ORXON_INFOBOT,
    POKITARU_INFOBOT,
    HOVEN_INFOBOT,
    GEMLIK_INFOBOT,
    OLTANIS_INFOBOT,
    QUARTU_INFOBOT,
    KALEBO_INFOBOT,
    FLEET_INFOBOT,
    VELDIN_INFOBOT,
]

COLLECTABLES: Sequence[CollectableData] = [
    GOLD_BOLT
]

EQUIPMENT_AND_WEAPONS: Sequence[ItemData] = [*EQUIPMENT, *WEAPONS]

ALL: Sequence[ItemData] = [*EQUIPMENT, *WEAPONS, *PLANETS, *COLLECTABLES, ]


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


def get_item_groups() -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = {
        "Weapons": {w.name for w in WEAPONS},
        "Infobots": {c.name for c in PLANETS},
        "Equipment": {e.name for e in EQUIPMENT},
    }
    return groups
