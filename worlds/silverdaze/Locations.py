from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Location
#Sawyer: Same as before, I'll be using Rogue Legacy as a base here.

class SDLocation(Location):
    game: str = "Silver Daze"


class SDLocationData(NamedTuple):
    category: str
    rule: list = None
    id: Optional[str] = None


def get_locations_by_category(category: str) -> Dict[str, SDLocationData]:
    location_dict: Dict[str, SDLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)

    return location_dict

def Party():
    return


location_table: Dict[str, SDLocationData] = {
    # Start Game
    "Ultima":                        SDLocationData("Start Game",           [],   "Ultima"),
    "PinnJoin":                      SDLocationData("Start Game",           [],   "PinnJoin"),
    "StarterHealToken1":             SDLocationData("Start Game",           [],   "StarterHealToken1"),
    "StarterHealToken2":             SDLocationData("Start Game",           [],   "StarterHealToken2"),
    # Grey Zone 1
    "GeoJoin":                       SDLocationData("Grey Zone",            [Party(1)],   "GeoJoin"),
    "Cotton2Chest1":                 SDLocationData("Grey Zone",            [],   "Cotton2Chest1"),
    "Cotton3Chest1":                 SDLocationData("Grey Zone",            [],   "Cotton3Chest1"),
    "YellowKey":                     SDLocationData("Grey Zone",            [],    "YellowKey"),
    # Grey Zone 2
    "Hub2Chest1":                    SDLocationData("Grey Zone 2",          [],   "Hub2Chest1"),
    # Red Zone 1
    "Red1Chest":                     SDLocationData("Red Zone",             [],   "Red1Chest"),
    "Red3Chest":                     SDLocationData("Red Zone",             [],   "Red3Chest"),
    # Red Zone 2
    "Red4Chest1":                    SDLocationData("Red Zone 2",           [],   "Red4Chest1"),
    "Red4Chest2":                    SDLocationData("Red Zone 2",           [],   "Red4Chest2"),
    "Red4Chest3":                    SDLocationData("Red Zone 2",           [],   "Red4Chest3"),
    "RedTower2Chest":                SDLocationData("Red Zone 2",           [],   "RedTower2Chest"),
    "RedTower4Chest":                SDLocationData("Red Zone 2",           [],   "RedTower4Chest"),
    "Nyx":                           SDLocationData("Red Zone 2",           [],   "Nyx"),
    "Kani":                          SDLocationData("Red Zone 2",           [],   "Kani"),
    "RedChasm1Chest":                SDLocationData("Red Zone 2",           [],   "RedChasm1Chest"),
    "RedChasm2Chest1":               SDLocationData("Red Zone 2",           [],   "RedChasm2Chest1"),
    "RedChasm2Chest2":               SDLocationData("Red Zone 2",           [],   "RedChasm2Chest2"),
    "RedChasmReunionChest":          SDLocationData("Red Zone 2",           [],   "RedChasmReunionChest"),
    "Red3_BackdoorChest":            SDLocationData("Red Zone 2",           [],   "Red3_BackdoorChest"),
    # Grey Zone Red Chest
    "Hub2Chest2":                    SDLocationData("Red Zone 2",           [],   "Hub2Chest2"),
    # Boss Drops
    "QuoDefender1":                  SDLocationData("",                 [],   "QuoDefender1"),
    "QuoDefender2":                  SDLocationData("Boss",                 [],   "QuoDefender2"),
    "QuoDefender3":                  SDLocationData("Boss",                 [],   "QuoDefender3"),
    "Kingoose1":                     SDLocationData("Boss",                 [],   "Kingoose1"),
    "Kingoose2":                     SDLocationData("Boss",                 [],   "Kingoose2"),
    "Kingoose3":                     SDLocationData("Boss",                 [],   "Kingoose3"),
    "Nyx1":                          SDLocationData("Boss",                 [],   "Nyx1"),
    "Nyx2":                          SDLocationData("Boss",                 [],   "Nyx2"),
    "Nyx3":                          SDLocationData("Boss",                 [],   "Nyx3"),
    # Party Members
    "PinnMP3":                       SDLocationData("Party",                [],   "PinnMP3"),
    "GeoMP3":                        SDLocationData("Party",                [],   "GeoMP3"),
    "GeoWeapon1":                    SDLocationData("Party",                [],   "GeoWeapon1"),
    "KaniMP3":                       SDLocationData("Party",                [],   "KaniMP3"),
    "KaniWeapon1":                   SDLocationData("Party",                [],   "KaniWeapon1"),
    "KaniWeapon2":                   SDLocationData("Party",                [],   "KaniWeapon2"),
    "KaniWeapon3":                   SDLocationData("Party",                [],   "KaniWeapon3"),
}
