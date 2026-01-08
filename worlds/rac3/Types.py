from enum import IntEnum
from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification


class GameLocation(Location):
    game = "Ratchet and Clank 3 Up your Arsenal"


class GameItem(Item):
    game = "Ratchet and Clank 3 Up your Arsenal"


class WeaponType(IntEnum):
    SB = 1
    NL = 2
    N60 = 3
    PW = 4
    INF = 5
    SC = 6
    SH = 7
    AoD = 8
    FR = 9
    ANH = 10
    HSG = 11
    DBL = 12
    RI = 13
    QoR = 14
    RY3N0 = 15
    MTG = 16
    LG = 17
    TB = 18
    HB = 19
    PC = 20


class Multiplier(IntEnum):
    x1 = 1
    x2 = 2
    x4 = 3
    x6 = 4
    x8 = 5
    x10 = 6


multiplier_to_name = {
    Multiplier.x1: "x1",
    Multiplier.x2: "x2",
    Multiplier.x4: "x4",
    Multiplier.x6: "x6",
    Multiplier.x8: "x8",
    Multiplier.x10: "x10",
}
weapon_type_to_name = {
    WeaponType.SB: "Shock Blaster",
    WeaponType.NL: "Nitro Launcher",
    WeaponType.N60: "N60 Storm",
    WeaponType.PW: "Plasma Whip",
    WeaponType.INF: "Infector",
    WeaponType.SC: "Suck Cannon",
    WeaponType.SH: "Spitting Hydra",
    WeaponType.AoD: "Agents of Doom",
    WeaponType.FR: "Flux Rifle",
    WeaponType.ANH: "Annihilator",
    WeaponType.HSG: "Holo-Shield Glove",
    WeaponType.DBL: "Disk-Blade Gun",
    WeaponType.RI: "Rift Inducer",
    WeaponType.QoR: "Qwack-O-Ray",
    WeaponType.RY3N0: "RY3N0",
    WeaponType.MTG: "Mini-Turret Glove",
    WeaponType.LG: "Lava Gun",
    WeaponType.TB: "Shield Charger",
    WeaponType.HB: "Bouncer",
    WeaponType.PC: "Plasma Coil"
}

weapon_type_to_shortened_name = {
    WeaponType.SB: "SB",
    WeaponType.NL: "NL",
    WeaponType.N60: "N60",
    WeaponType.PW: "PW",
    WeaponType.INF: "INF",
    WeaponType.SC: "SC",
    WeaponType.SH: "SH",
    WeaponType.AoD: "AOD",
    WeaponType.FR: "FR",
    WeaponType.ANH: "ANH",
    WeaponType.HSG: "HSG",
    WeaponType.DBL: "DBL",
    WeaponType.RI: "RI",
    WeaponType.QoR: "QoR",
    WeaponType.RY3N0: "RY3N0",
    WeaponType.MTG: "MTG",
    WeaponType.LG: "LG",
    WeaponType.TB: "TB",
    WeaponType.HB: "HB",
    WeaponType.PC: "PC"

}


class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1


class EventData(NamedTuple):
    ap_code: None
    region: Optional[str]


class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
