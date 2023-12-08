from typing import Dict, NamedTuple, Optional
import typing


from BaseClasses import Location


class KHRECOMLocation(Location):
    game: str = "Kingdom Hearts Chain of Memories"


class KHRECOMLocationData(NamedTuple):
    category: str
    code: Optional[int] = None


def get_locations_by_category(category: str) -> Dict[str, KHRECOMLocationData]:
    location_dict: Dict[str, KHRECOMLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)

    return location_dict


location_table: Dict[str, KHRECOMLocationData] = {
    "Starting Checks (Attack Cards Kingdom Key)":                        KHRECOMLocationData("Starting",     269_0001),
    "Starting Checks (Item Cards Potion)":                               KHRECOMLocationData("Starting",     269_0002),
    "Starting Checks (Magic Cards Blizzard)":                            KHRECOMLocationData("Starting",     269_0003),
    "Starting Checks (Magic Cards Cure)":                                KHRECOMLocationData("Starting",     269_0004),
    
    "Traverse Town Post Floor (Magic Cards Fire)":                       KHRECOMLocationData("Progression",  269_0101),
    "Traverse Town Room of Beginnings":                                  KHRECOMLocationData("Progression",  269_0102),
    "Traverse Town Room of Beginnings (Summon Cards Simba)":             KHRECOMLocationData("Progression",  269_0103),
    "Traverse Town Room of Guidance":                                    KHRECOMLocationData("Progression",  269_0104),
    "Traverse Town Room of Truth":                                       KHRECOMLocationData("Progression",  269_0105),
    "Traverse Town Room of Truth (Enemy Cards Guard Armor)":             KHRECOMLocationData("Progression",  269_0106),
    "Traverse Town Room of Rewards (Attack Cards Lionheart)":            KHRECOMLocationData("Progression",  269_0107),
    
    "Wonderland Bounty (Magic Cards Stop)":                              KHRECOMLocationData("Progression",  269_0201),
    "Wonderland Field (Attack Cards Lady Luck)":                         KHRECOMLocationData("Progression",  269_0202),
    "Wonderland Room of Beginnings":                                     KHRECOMLocationData("Progression",  269_0203),
    "Wonderland Room of Beginnings (Enemy Cards Card Soldier)":          KHRECOMLocationData("Progression",  269_0204),
    "Wonderland Room of Guidance":                                       KHRECOMLocationData("Progression",  269_0205),
    "Wonderland Room of Truth":                                          KHRECOMLocationData("Progression",  269_0206),
    "Wonderland Room of Truth (Enemy Cards Trickmaster)":                KHRECOMLocationData("Progression",  269_0207),
    
    "Olympus Coliseum Field (Attack Card Olympia)":                      KHRECOMLocationData("Progression",  269_0301),
    "Olympus Coliseum Room of Beginnings":                               KHRECOMLocationData("Progression",  269_0302),
    "Olympus Coliseum Room of Guidance":                                 KHRECOMLocationData("Progression",  269_0303),
    "Olympus Coliseum Room of Guidance (Item Cards Hi-Potion)":          KHRECOMLocationData("Progression",  269_0304),
    "Olympus Coliseum Room of Truth":                                    KHRECOMLocationData("Progression",  269_0305),
    "Olympus Coliseum Room of Truth (Enemy Cards Hades)":                KHRECOMLocationData("Progression",  269_0306),
    "Olympus Coliseum Room of Truth (Summon Cards Cloud)":               KHRECOMLocationData("Progression",  269_0307),
    "Olympus Coliseum Room of Rewards (Attack Cards Metal Chocobo)":     KHRECOMLocationData("Progression",  269_0308),
    
    "Monstro Field (Attack Cards Wishing Star)":                         KHRECOMLocationData("Progression",  269_0401),
    "Monstro Room of Beginnings":                                        KHRECOMLocationData("Progression",  269_0402),
    "Monstro Room of Guidance":                                          KHRECOMLocationData("Progression",  269_0403),
    "Monstro Room of Guidance (Enemy Cards Parasite Cage)":              KHRECOMLocationData("Progression",  269_0404),
    "Monstro Room of Truth":                                             KHRECOMLocationData("Progression",  269_0405),
    "Monstro Room of Truth (Summon Cards Dumbo)":                        KHRECOMLocationData("Progression",  269_0406),
    
    "Agrabah Bounty (Magic Cards Gravity)":                              KHRECOMLocationData("Progression",  269_0501),
    "Agrabah Field (Attack Cards Three Wishes)":                         KHRECOMLocationData("Progression",  269_0502),
    "Agrabah Room of Beginnings":                                        KHRECOMLocationData("Progression",  269_0503),
    "Agrabah Room of Guidance":                                          KHRECOMLocationData("Progression",  269_0504),
    "Agrabah Room of Guidance (Item Cards Ether)":                       KHRECOMLocationData("Progression",  269_0505),
    "Agrabah Room of Truth":                                             KHRECOMLocationData("Progression",  269_0506),
    "Agrabah Room of Truth (Enemy Cards Jafar)":                         KHRECOMLocationData("Progression",  269_0507),
    "Agrabah Room of Truth (Summon Cards Genie)":                        KHRECOMLocationData("Progression",  269_0508),
    
    "Halloween Town Field (Attack Cards Pumpkinhead)":                   KHRECOMLocationData("Progression",  269_0601),
    "Halloween Town Post Floor (Magic Cards Thunder)":                   KHRECOMLocationData("Progression",  269_0602),
    "Halloween Town Room of Beginnings":                                 KHRECOMLocationData("Progression",  269_0603),
    "Halloween Town Room of Guidance":                                   KHRECOMLocationData("Progression",  269_0604),
    "Halloween Town Room of Truth":                                      KHRECOMLocationData("Progression",  269_0605),
    "Halloween Town Room of Truth (Enemy Cards Oogie Boogie)":           KHRECOMLocationData("Progression",  269_0606),
    
    "Atlantica Field (Attack Cards Crabclaw)":                           KHRECOMLocationData("Progression",  269_0701),
    "Atlantica Post Floor (Magic Cards Aero)":                           KHRECOMLocationData("Progression",  269_0702),
    "Atlantica Room of Beginnings":                                      KHRECOMLocationData("Progression",  269_0703),
    "Atlantica Room of Guidance":                                        KHRECOMLocationData("Progression",  269_0704),
    "Atlantica Room of Truth":                                           KHRECOMLocationData("Progression",  269_0705),
    "Atlantica Room of Truth (Enemy Cards Ursula)":                      KHRECOMLocationData("Progression",  269_0706),
    
    "Neverland Field (Attack Cards Fairy Harp)":                         KHRECOMLocationData("Progression",  269_0801),
    "Neverland Room of Beginnings":                                      KHRECOMLocationData("Progression",  269_0802),
    "Neverland Room of Guidance":                                        KHRECOMLocationData("Progression",  269_0803),
    "Neverland Room of Truth":                                           KHRECOMLocationData("Progression",  269_0804),
    "Neverland Room of Truth (Enemy Cards Hook)":                        KHRECOMLocationData("Progression",  269_0805),
    "Neverland Room of Truth (Summon Cards Tinker Bell)":                KHRECOMLocationData("Progression",  269_0806),
    
    "Hollow Bastion Field (Attack Cards Divine Rose)":                   KHRECOMLocationData("Progression",  269_0901),
    "Hollow Bastion Room of Beginnings":                                 KHRECOMLocationData("Progression",  269_0902),
    "Hollow Bastion Room of Guidance":                                   KHRECOMLocationData("Progression",  269_0903),
    "Hollow Bastion Room of Truth":                                      KHRECOMLocationData("Progression",  269_0904),
    "Hollow Bastion Room of Truth (Enemy Cards Dragon Maleficent)":      KHRECOMLocationData("Progression",  269_0905),
    "Hollow Bastion Room of Rewards (Summon Cards Mushu)":               KHRECOMLocationData("Progression",  269_0906),
    
    "100 Acre Wood Clear (Summon Cards Bambi)":                          KHRECOMLocationData("Progression",  269_1001),
    "100 Acre Wood Mini Game Bumble Rumble (Item Cards Elixir)":         KHRECOMLocationData("Progression",  269_1002),
    "100 Acre Wood Mini Game Whirlwind Plunge (Item Cards Mega-Ether)":  KHRECOMLocationData("Progression",  269_1003),
    "100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)":      KHRECOMLocationData("Progression",  269_1004),
    
    "Twilight Town Post Floor (Item Cards Mega-Potion)":                 KHRECOMLocationData("Progression",  269_1101),
    "Twilight Town Room of Beginnings":                                  KHRECOMLocationData("Progression",  269_1102),
    "Twilight Town Room of Beginnings (Enemy Cards Vexen)":              KHRECOMLocationData("Progression",  269_1103),
    
    "Destiny Islands Post Floor (Attack Cards Oathkeeper)":              KHRECOMLocationData("Progression",  269_1201),
    "Destiny Islands Post Floor (Attack Cards Oblivion)":                KHRECOMLocationData("Progression",  269_1202),
    "Destiny Islands Post Floor (Enemy Cards Larxene)":                  KHRECOMLocationData("Progression",  269_1203),
    "Destiny Islands Post Floor (Enemy Cards Riku)":                     KHRECOMLocationData("Progression",  269_1204),
    "Destiny Islands Room of Beginnings":                                KHRECOMLocationData("Progression",  269_1205),
    "Destiny Islands Room of Guidance":                                  KHRECOMLocationData("Progression",  269_1206),
    "Destiny Islands Room of Guidance (Enemy Cards Darkside)":           KHRECOMLocationData("Progression",  269_1207),
    "Destiny Islands Room of Rewards (Item Cards Megalixir)":            KHRECOMLocationData("Progression",  269_1208),
    
    "Castle Oblivion Field Marluxia":                                    KHRECOMLocationData("Progression",  269_1301),
    "Castle Oblivion Room of Beginnings":                                KHRECOMLocationData("Progression",  269_1302),
    "Castle Oblivion Room of Beginnings (Enemy Cards Axel)":             KHRECOMLocationData("Progression",  269_1303),
    
    "Heartless Air Pirate":                                              KHRECOMLocationData("Progression",  269_1401),
    "Heartless Air Soldier":                                             KHRECOMLocationData("Progression",  269_1402),
    "Heartless Aquatank":                                                KHRECOMLocationData("Progression",  269_1403),
    "Heartless Bandit":                                                  KHRECOMLocationData("Progression",  269_1404),
    "Heartless Barrel Spider":                                           KHRECOMLocationData("Progression",  269_1405),
    "Heartless Black Fungus":                                            KHRECOMLocationData("Progression",  269_1406),
    "Heartless Blue Rhapsody":                                           KHRECOMLocationData("Progression",  269_1407),
    "Heartless Bouncywild":                                              KHRECOMLocationData("Progression",  269_1408),
    "Heartless Creeper Plant":                                           KHRECOMLocationData("Progression",  269_1409),
    "Heartless Crescendo":                                               KHRECOMLocationData("Progression",  269_1410),
    "Heartless Darkball":                                                KHRECOMLocationData("Progression",  269_1411),
    "Heartless Defender":                                                KHRECOMLocationData("Progression",  269_1412),
    "Heartless Fat Bandit":                                              KHRECOMLocationData("Progression",  269_1413),
    "Heartless Gargoyle":                                                KHRECOMLocationData("Progression",  269_1414),
    "Heartless Green Requiem":                                           KHRECOMLocationData("Progression",  269_1415),
    "Heartless Large Body":                                              KHRECOMLocationData("Progression",  269_1416),
    "Heartless Neoshadow":                                               KHRECOMLocationData("Progression",  269_1417),
    "Heartless Pirate":                                                  KHRECOMLocationData("Progression",  269_1418),
    "Heartless Powerwild":                                               KHRECOMLocationData("Progression",  269_1419),
    "Heartless Red Nocturne":                                            KHRECOMLocationData("Progression",  269_1420),
    "Heartless Screwdiver":                                              KHRECOMLocationData("Progression",  269_1421),
    "Heartless Sea Neon":                                                KHRECOMLocationData("Progression",  269_1422),
    "Heartless Search Ghost":                                            KHRECOMLocationData("Progression",  269_1423),
    "Heartless Shadow":                                                  KHRECOMLocationData("Progression",  269_1424),
    "Heartless Soldier":                                                 KHRECOMLocationData("Progression",  269_1425),
    "Heartless Tornado Step":                                            KHRECOMLocationData("Progression",  269_1426),
    "Heartless White Mushroom":                                          KHRECOMLocationData("Progression",  269_1427),
    "Heartless Wight Knight":                                            KHRECOMLocationData("Progression",  269_1428),
    "Heartless Wizard":                                                  KHRECOMLocationData("Progression",  269_1429),
    "Heartless Wyvern":                                                  KHRECOMLocationData("Progression",  269_1430),
    "Heartless Yellow Opera":                                            KHRECOMLocationData("Progression",  269_1431),
}

event_location_table: Dict[str, KHRECOMLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}