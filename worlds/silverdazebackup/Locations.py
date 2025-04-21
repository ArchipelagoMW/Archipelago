from typing import Dict, NamedTuple, Optional
from worlds.silverdaze.Rules import party
from worlds.silverdaze.Rules import key
from worlds.silverdaze.Rules import zone
from worlds.silverdaze.Rules import SDRules


class SDLocationData(NamedTuple):
    category: str
    rule: list = None
    id: Optional[str] = None

location_table: Dict[str, SDLocationData] = {
    # Start Game
    "Ultima":                        SDLocationData("Start Game",           [],   "Ultima"),
    "PinnJoin":                      SDLocationData("Start Game",           [],   "PinnJoin"),
    "StarterHealToken1":             SDLocationData("Start Game",           [],   "StarterHealToken1"),
    "StarterHealToken2":             SDLocationData("Start Game",           [],   "StarterHealToken2"),
    # Grey Zone 1
    "GeoJoin":                       SDLocationData("Grey Zone",            [party(1)],   "GeoJoin"),
    "Cotton2Chest1":                 SDLocationData("Grey Zone",            [party(1)],   "Cotton2Chest1"),
    "Cotton3Chest1":                 SDLocationData("Grey Zone",            [party(1)],   "Cotton3Chest1"),
    "YellowKey":                     SDLocationData("Grey Zone",            [party(1)],    "YellowKey"),
    # Grey Zone 2
    "Hub2Chest1":                    SDLocationData("Grey Zone 2",          [key('yellow')],   "Hub2Chest1"),
    # Red Zone 1
    "Red1Chest":                     SDLocationData("Red Zone",             [zone('red') and key('red')],   "Red1Chest"),
    "Red3Chest":                     SDLocationData("Red Zone",             [zone('red')],   "Red3Chest"),
    # Red Zone 2
    "Red4Chest1":                    SDLocationData("Red Zone 2",           [zone('red2')],   "Red4Chest1"),
    "Red4Chest2":                    SDLocationData("Red Zone 2",           [zone('red2')],   "Red4Chest2"),
    "Red4Chest3":                    SDLocationData("Red Zone 2",           [zone('red2')],   "Red4Chest3"),
    "RedTower2Chest":                SDLocationData("Red Zone 2",           [zone('red2')],   "RedTower2Chest"),
    "RedTower4Chest":                SDLocationData("Red Zone 2",           [zone('red2')],   "RedTower4Chest"),
    "Nyx":                           SDLocationData("Red Zone 2",           [zone('red2') and party(2)],   "Nyx"),
    "Kani":                          SDLocationData("Red Zone 2",           [zone('red2')],   "Kani"),
    "RedChasm1Chest":                SDLocationData("Red Zone 2",           [zone('red2')],   "RedChasm1Chest"),
    "RedChasm2Chest1":               SDLocationData("Red Zone 2",           [zone('red2') and key('red')],   "RedChasm2Chest1"),
    "RedChasm2Chest2":               SDLocationData("Red Zone 2",           [zone('red2')],   "RedChasm2Chest2"),
    "RedChasmReunionChest":          SDLocationData("Red Zone 2",           [zone('red2')],   "RedChasmReunionChest"),
    "Red3_BackdoorChest":            SDLocationData("Red Zone 2",           [zone('red2') and key('red')],   "Red3_BackdoorChest"),
    # Grey Zone Red Chest
    "Hub2Chest2":                    SDLocationData("Red Zone 2",           [zone('red2') and key('red')],   "Hub2Chest2"),
    # Boss Drops
    "QuoDefender1":                  SDLocationData("",                     [zone('red') and party(2)],   "QuoDefender1"),
    "QuoDefender2":                  SDLocationData("Boss",                 [zone('red') and party(2)],   "QuoDefender2"),
    "QuoDefender3":                  SDLocationData("Boss",                 [zone('red') and party(2)],   "QuoDefender3"),
    "Kingoose1":                     SDLocationData("Boss",                 [zone('red2') and party(2)],   "Kingoose1"),
    "Kingoose2":                     SDLocationData("Boss",                 [zone('red2') and party(2)],   "Kingoose2"),
    "Kingoose3":                     SDLocationData("Boss",                 [zone('red2') and party(2)],   "Kingoose3"),
    "Nyx1":                          SDLocationData("Boss",                 [zone('red2') and party(2)],   "Nyx1"),
    "Nyx2":                          SDLocationData("Boss",                 [zone('red2') and party(2)],   "Nyx2"),
    "Nyx3":                          SDLocationData("Boss",                 [zone('red2') and party(2)],   "Nyx3"),
    # Party Members
    "PinnMP3":                       SDLocationData("Party",                [party(1)],   "PinnMP3"),
    "GeoMP3":                        SDLocationData("Party",                [party(1)],   "GeoMP3"),
    "GeoWeapon1":                    SDLocationData("Party",                [party(1)],   "GeoWeapon1"),
    "KaniMP3":                       SDLocationData("Party",                [zone('red2')],   "KaniMP3"),
    "KaniWeapon1":                   SDLocationData("Party",                [zone('red2')],   "KaniWeapon1"),
    "KaniWeapon2":                   SDLocationData("Party",                [zone('red2')],   "KaniWeapon2"),
    "KaniWeapon3":                   SDLocationData("Party",                [zone('red2')],   "KaniWeapon3"),
}