from .classification import *
from .. import BadgeItemData

table: dict[str, BadgeItemData] = {
    "Trio Badge": BadgeItemData(0x78, 0, always_progression),
    "Basic Badge": BadgeItemData(0x79, 1, always_progression),
    "Insect Badge": BadgeItemData(0x7A, 2, always_progression),
    "Bolt Badge": BadgeItemData(0x7B, 3, always_progression),
    "Quake Badge": BadgeItemData(0x7C, 4, always_progression),
    "Jet Badge": BadgeItemData(0x7D, 5, always_progression),
    "Freeze Badge": BadgeItemData(0x7E, 6, always_progression),
    "Legend Badge": BadgeItemData(0x7F, 7, always_progression),
}
