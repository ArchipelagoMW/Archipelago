from typing import Dict, NamedTuple, Optional
from BaseClasses import Location
import typing
from .Regions import sd_regions


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class SDLocation(Location):
    game: str = "SilverDaze"

class SDLocationData(NamedTuple):
    region: str
    id: Optional[str] = None


location_table: Dict[str, SDLocationData] = {
    # Start Game
    "Ultima":                        SDLocationData("Geo_Room",             "Ultima"),
    "PinnJoin":                      SDLocationData("Geo_Room",             "PinnJoin"),
    "StarterHealToken1":             SDLocationData("Geo_Room",             "StarterHealToken1"),
    "StarterHealToken2":             SDLocationData("Geo_Room",             "StarterHealToken2"),
    # Grey Zone 1
    "GeoJoin":                       SDLocationData("Cotton",               "GeoJoin"),
    "Cotton2Chest1":                 SDLocationData("Cotton",               "Cotton2Chest1"),
    "Cotton3Chest1":                 SDLocationData("Cotton",               "Cotton3Chest1"),
    "YellowKey":                     SDLocationData("Cotton",               "YellowKey"),
    # Grey Zone 2
    "Hub2Chest1":                    SDLocationData("GreyHub2",             "Hub2Chest1"),
    # Red Zone 1
    "Red1Chest":                     SDLocationData("Red",                  "Red1Chest"),
    "Red3Chest":                     SDLocationData("Red",                  "Red3Chest"),
    # Red Zone 2
    "Red4Chest1":                    SDLocationData("Red2",                 "Red4Chest1"),
    "Red4Chest2":                    SDLocationData("Red2",                 "Red4Chest2"),
    "Red4Chest3":                    SDLocationData("Red2",                 "Red4Chest3"),
    "RedTower2Chest":                SDLocationData("Red2",                 "RedTower2Chest"),
    "RedTower4Chest":                SDLocationData("Red2",                 "RedTower4Chest"),
    "Nyx":                           SDLocationData("Red2",                 "Nyx"),
    "Kani":                          SDLocationData("Red2",                 "Kani"),
    "RedChasm1Chest":                SDLocationData("Red2",                 "RedChasm1Chest"),
    "RedChasm2Chest1":               SDLocationData("Red2",                 "RedChasm2Chest1"),
    "RedChasm2Chest2":               SDLocationData("Red2",                 "RedChasm2Chest2"),
    "RedChasmReunionChest":          SDLocationData("Red2",                 "RedChasmReunionChest"),
    "Red3_BackdoorChest":            SDLocationData("Red2",                 "Red3_BackdoorChest"),
    # Grey Zone Red Chest
    "Hub2Chest2":                    SDLocationData("Red2",                 "Hub2Chest2"),
    # Boss Drops
    "QuoDefender1":                  SDLocationData("Red",                  "QuoDefender1"),
    "QuoDefender2":                  SDLocationData("Red",                  "QuoDefender2"),
    "QuoDefender3":                  SDLocationData("Red",                  "QuoDefender3"),
    "Kingoose1":                     SDLocationData("Red2",                 "Kingoose1"),
    "Kingoose2":                     SDLocationData("Red2",                 "Kingoose2"),
    "Kingoose3":                     SDLocationData("Red2",                 "Kingoose3"),
    "Nyx1":                          SDLocationData("Red2",                 "Nyx1"),
    "Nyx2":                          SDLocationData("Red2",                 "Nyx2"),
    "Nyx3":                          SDLocationData("Red2",                 "Nyx3"),
    # Party Members
    "PinnMP3":                       SDLocationData("Cotton",               "PinnMP3"),
    "GeoMP3":                        SDLocationData("Cotton",               "GeoMP3"),
    "GeoWeapon1":                    SDLocationData("Cotton",               "GeoWeapon1"),
    "KaniMP3":                       SDLocationData("Red2",                 "KaniMP3"),
    "KaniWeapon1":                   SDLocationData("Red2",                 "KaniWeapon1"),
    "KaniWeapon2":                   SDLocationData("Red2",                 "KaniWeapon2"),
    "KaniWeapon3":                   SDLocationData("Red2",                 "KaniWeapon3"),
}

events_table = {
}