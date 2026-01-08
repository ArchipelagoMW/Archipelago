import typing as t
from dataclasses import dataclass

from BaseClasses import ItemClassification

from .constants import AVItemType, AP_ID_BASE


@dataclass
class AVItemData:
    id: int
    name: str
    group_name: AVItemType
    ap_classification: ItemClassification
    is_default: bool

    def __post_init__(self):
        self.id += AP_ID_BASE


raw_item_data: t.Tuple[AVItemData] = (
    AVItemData(0, "Axiom Disruptor", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(1, "Data Bomb", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(2, "Firewall", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(3, "Inertial Pulse", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(4, "Ion Beam", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(5, "Lightning Gun", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(6, "Multi-Disruptor", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(7, "Reflector", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(8, "Shards", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(9, "Quantum Variegator", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(10, "Turbine Pulse", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(11, "Voranj", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(12, "Nova", AVItemType.WEAPON, ItemClassification.progression, True),
    AVItemData(13, "Tethered Charge", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(14, "Hypo-Atomizer", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(15, "Orbital Discharge", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(16, "Distortion Field", AVItemType.WEAPON, ItemClassification.progression, True),
    AVItemData(17, "FlameThrower", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(18, "Kilver", AVItemType.WEAPON, ItemClassification.progression, True),
    AVItemData(19, "Reverse Slicer", AVItemType.WEAPON, ItemClassification.progression, True),
    AVItemData(20, "Fat Beam", AVItemType.WEAPON, ItemClassification.progression, True),
    AVItemData(21, "Heat Seeker", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(22, "Scissor Beam", AVItemType.WEAPON, ItemClassification.progression_skip_balancing, True),
    AVItemData(23, "Address Disruptor 1", AVItemType.GLITCH, ItemClassification.progression, False),
    AVItemData(24, "Address Disruptor 2", AVItemType.GLITCH, ItemClassification.progression, False),
    AVItemData(25, "Laser Drill", AVItemType.DRILL, ItemClassification.progression, True),
    AVItemData(26, "Remote Drone", AVItemType.DRONE, ItemClassification.progression, False),
    AVItemData(27, "Address Bomb", AVItemType.GLITCH, ItemClassification.progression, False),
    AVItemData(28, "Grapple", AVItemType.MOVEMENT, ItemClassification.progression, True),
    AVItemData(29, "Field Disruptor", AVItemType.MOVEMENT, ItemClassification.progression, True),
    AVItemData(30, "Modified Lab Coat", AVItemType.COAT, ItemClassification.progression, False),
    AVItemData(31, "Trenchcoat", AVItemType.COAT, ItemClassification.progression, False),
    AVItemData(32, "Red Coat", AVItemType.COAT, ItemClassification.progression, False),
    AVItemData(33, "Sudran Key", AVItemType.KEY, ItemClassification.progression, True),
    AVItemData(34, "Enhanced Drone Launch", AVItemType.DRONE, ItemClassification.progression, False),
    AVItemData(35, "Drone Teleport", AVItemType.DRONE, ItemClassification.progression, True),
    AVItemData(36, "Passcode Tool", AVItemType.KEY, ItemClassification.progression, True),
    AVItemData(37, "Bioflux Accelerator 1", AVItemType.TENDRILS, ItemClassification.filler, True),
    AVItemData(38, "Bioflux Accelerator 2", AVItemType.TENDRILS, ItemClassification.filler, True),
    AVItemData(39, "Health Node", AVItemType.HEALTH_NODE, ItemClassification.useful, False),
    AVItemData(40, "Power Node", AVItemType.POWER_NODE, ItemClassification.useful, False),
    AVItemData(41, "Health Node Fragment", AVItemType.HEALTH_NODE_FRAGMENT, ItemClassification.useful, False),
    AVItemData(42, "Power Node Fragment", AVItemType.POWER_NODE_FRAGMENT, ItemClassification.useful, False),
    AVItemData(43, "Range Node", AVItemType.RANGE_NODE, ItemClassification.useful, False),
    AVItemData(44, "Size Node", AVItemType.SIZE_NODE, ItemClassification.useful, False),
    # Archipelago Progressive Items
    AVItemData(45, "Progressive Address Disruptor", AVItemType.GLITCH, ItemClassification.progression, False),
    AVItemData(46, "Progressive Coat", AVItemType.COAT, ItemClassification.progression, False),
    AVItemData(47, "Progressive Drone", AVItemType.DRONE, ItemClassification.progression, False),
)

item_data: t.Dict[str, AVItemData] = {data.name: data for data in raw_item_data}

ITEM_NAME_TO_ID: t.Dict[str, int] = {data.name: data.id for data in raw_item_data}
