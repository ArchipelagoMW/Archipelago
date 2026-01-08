from typing import NamedTuple

from .constants import ItemType
from .sprites import Sprite


class ItemData(NamedTuple):
    type: ItemType  # Used for determining the memory address to write bits to as each go somewhere different
    acquisition: int  # Acquisition value (= message ID) of vanilla item
    bits: int
    sprite: Sprite
    message: str | None  # Custom message text if str; defer to basepatch if none
    sound: int


SOUND_ARMING_WEAPON = 0x84


item_data_table = {
    "Nothing":            ItemData(ItemType.CUSTOM,              0,      0, Sprite.Nothing,          "Nothing acquired.", SOUND_ARMING_WEAPON),

    "Energy Tank":        ItemData(ItemType.ENERGY_TANK,         1,      1, Sprite.EnergyTank,       None,                               0x87),
    "Missile Tank":       ItemData(ItemType.MISSILE_TANK,        2,      1, Sprite.MissileTank,      None,                SOUND_ARMING_WEAPON),
    "Super Missile Tank": ItemData(ItemType.SUPER_MISSILE_TANK,  4,      1, Sprite.SuperMissileTank, None,                SOUND_ARMING_WEAPON),
    "Power Bomb Tank":    ItemData(ItemType.POWER_BOMB_TANK,     6,      1, Sprite.PowerBombTank,    None,                SOUND_ARMING_WEAPON),

    "Long Beam":          ItemData(ItemType.BEAM,                8, 1 << 0, Sprite.LongBeam,         None,                               0xC9),
    "Charge Beam":        ItemData(ItemType.BEAM,                9, 1 << 4, Sprite.ChargeBeam,       None,                               0xF0),
    "Ice Beam":           ItemData(ItemType.BEAM,               10, 1 << 1, Sprite.IceBeam,          None,                               0xCA),
    "Wave Beam":          ItemData(ItemType.BEAM,               11, 1 << 2, Sprite.WaveBeam,         None,                               0xCC),
    "Plasma Beam":        ItemData(ItemType.BEAM,               12, 1 << 3, Sprite.PlasmaBeam,       "Plasma Beam",                      0xD0),
    "Bomb":               ItemData(ItemType.BEAM,               13, 1 << 7, Sprite.Bomb,             None,                               0xFF),

    "Varia Suit":         ItemData(ItemType.MAJOR,              14, 1 << 4, Sprite.VariaSuit,        None,                               0x7D),
    "Gravity Suit":       ItemData(ItemType.MAJOR,              15, 1 << 5, Sprite.GravitySuit,      "Gravity Suit",                     0x75),
    "Morph Ball":         ItemData(ItemType.MAJOR,              16, 1 << 6, Sprite.MorphBall,        None,                               0x77),
    "Speed Booster":      ItemData(ItemType.MAJOR,              17, 1 << 1, Sprite.SpeedBooster,     None,                               0x8D),
    "Hi-Jump":            ItemData(ItemType.MAJOR,              18, 1 << 0, Sprite.HiJump,           None,                               0x6A),
    "Screw Attack":       ItemData(ItemType.MAJOR,              19, 1 << 3, Sprite.ScrewAttack,      None,                               0x6C),
    "Space Jump":         ItemData(ItemType.MAJOR,              20, 1 << 2, Sprite.SpaceJump,        "Space Jump",                       0x6B),
    "Power Grip":         ItemData(ItemType.MAJOR,              21, 1 << 7, Sprite.PowerGrip,        None,                               0x7B),

    "Fully Powered Suit": ItemData(ItemType.CUSTOM,             32, 1 << 7, Sprite.FullyPoweredSuit, None,                              0x1D3),
    "Wall Jump":          ItemData(ItemType.CUSTOM,              0, 1 << 0, Sprite.WallJump,         "Wall Jump",                        0x76),
    "Spring Ball":        ItemData(ItemType.CUSTOM,              0, 1 << 1, Sprite.SpringBall,       "Spring Ball",                      0x70),

    "Metroid DNA":        ItemData(ItemType.METROID_DNA,         0,      1, Sprite.MetroidDNA,       None,                              0x172),  # Text handled in basepatch
}
