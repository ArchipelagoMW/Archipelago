from typing import Dict, NamedTuple, Optional

from BaseClasses import Location
#Sawyer: Same as before, I'll be using Rogue Legacy as a base here.

class RLLocation(Location):
    game: str = "Silver Daze"


class SDLocationData(NamedTuple):
    category: str
    code: Optional[int] = None


def get_locations_by_category(category: str) -> Dict[str, SDLocationData]:
    location_dict: Dict[str, SDLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)

    return location_dict


location_table: Dict[str, SDLocationData] = {
    # Start Game
    "Ultima":                        SDLocationData("Start Game",   "Ultima"),
    "PinnJoin":                      SDLocationData("Start Game",   "PinnJoin"),
    "StarterHealToken1":             SDLocationData("Start Game",   "StarterHealToken1"),
    "StarterHealToken2":             SDLocationData("Start Game",   "StarterHealToken2"),
    # Grey Zone
    "GeoJoin":                       SDLocationData("Grey Zone",    "GeoJoin"),    
    "Cotton2Chest1":                 SDLocationData("Grey Zone",    "Cotton2Chest1"),    
    "Cotton3Chest1":                 SDLocationData("Grey Zone",    "Cotton3Chest1"),    
    "YellowKey":                     SDLocationData("Grey Zone",    "YellowKey"),    
    "Hub2Chest1":                    SDLocationData("Grey Zone",    "Hub2Chest1"),    
    "Hub2Chest2":                    SDLocationData("Grey Zone",    "Hub2Chest2"),    
    # Red Zone
    "Red1Chest":                     SDLocationData("Red Zone",     "Red1Chest"),      
    "Red3Chest":                     SDLocationData("Red Zone",     "Red3Chest"),      
    "Red4Chest1":                    SDLocationData("Red Zone",     "Red4Chest1"),      
    "Red4Chest2":                    SDLocationData("Red Zone",     "Red4Chest2"),      
    "Red4Chest3":                    SDLocationData("Red Zone",     "Red4Chest3"),      
    "RedTower2Chest":                SDLocationData("Red Zone",     "RedTower2Chest"),      
    "RedTower4Chest":                SDLocationData("Red Zone",     "RedTower4Chest"),      
    "Nyx":                           SDLocationData("Red Zone",     "Nyx"),      
    "Kani":                          SDLocationData("Red Zone",     "Kani"),      
    "RedChasm1Chest":                SDLocationData("Red Zone",     "RedChasm1Chest"),      
    "RedChasm2Chest1":               SDLocationData("Red Zone",     "RedChasm2Chest1"),      
    "RedChasm2Chest2":               SDLocationData("Red Zone",     "RedChasm2Chest2"),      
    "RedChasmReunionChest":          SDLocationData("Red Zone",     "RedChasmReunionChest"),      
    "Red3_BackdoorChest":            SDLocationData("Red Zone",     "Red3_BackdoorChest"),      
    # Boss Drops
    "QuoDefender1":                  SDLocationData("Boss",         "QuoDefender1"),        
    "QuoDefender2":                  SDLocationData("Boss",         "QuoDefender2"),        
    "QuoDefender3":                  SDLocationData("Boss",         "QuoDefender3"),          
    "Kingoose1":                     SDLocationData("Boss",         "Kingoose1"),          
    "Kingoose2":                     SDLocationData("Boss",         "Kingoose2"),          
    "Kingoose3":                     SDLocationData("Boss",         "Kingoose3"),          
    "Nyx1":                          SDLocationData("Boss",         "Nyx1"),          
    "Nyx2":                          SDLocationData("Boss",         "Nyx2"),          
    "Nyx3":                          SDLocationData("Boss",         "Nyx3"),          
    # Party Members
    "PinnMP3":                       SDLocationData("Boss",         "PinnMP3"),      
    "GeoMP3":                        SDLocationData("Boss",         "GeoMP3"),      
    "GeoWeapon1":                    SDLocationData("Boss",         "GeoWeapon1"),      
    "KaniMP3":                       SDLocationData("Boss",         "KaniMP3"),      
    "KaniWeapon1":                   SDLocationData("Boss",         "KaniWeapon1"),      
    "KaniWeapon2":                   SDLocationData("Boss",         "KaniWeapon2"),      
    "KaniWeapon3":                   SDLocationData("Boss",         "KaniWeapon3"),      
}
