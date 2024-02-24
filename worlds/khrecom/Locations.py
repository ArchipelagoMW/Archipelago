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
    
    "01F Exit Hall Axel I (Magic Cards Fire)":                           KHRECOMLocationData("Progression",  269_0101),
    "Traverse Town Room of Beginnings":                                  KHRECOMLocationData("Progression",  269_0102),
    "Traverse Town Room of Beginnings (Summon Cards Simba)":             KHRECOMLocationData("Progression",  269_0103),
    "Traverse Town Room of Guidance":                                    KHRECOMLocationData("Progression",  269_0104),
    "Traverse Town Room of Truth":                                       KHRECOMLocationData("Progression",  269_0105),
    "Traverse Town Room of Truth (Enemy Cards Guard Armor)":             KHRECOMLocationData("Progression",  269_0106),
    "Traverse Town Room of Rewards (Attack Cards Lionheart)":            KHRECOMLocationData("Progression",  269_0107),
    "Traverse Town Bounty (Attack Cards Maverick Flare)":                KHRECOMLocationData("Days"       ,  269_0108), #Days Location
    "Traverse Town Room of Rewards (Enemy Cards Saix)":                  KHRECOMLocationData("Days"       ,  269_0109), #Days Location
    
    "Wonderland Bounty (Magic Cards Stop)":                              KHRECOMLocationData("Progression",  269_0201),
    "Wonderland Field (Attack Cards Lady Luck)":                         KHRECOMLocationData("Progression",  269_0202),
    "Wonderland Room of Beginnings":                                     KHRECOMLocationData("Progression",  269_0203),
    "Wonderland Room of Beginnings (Enemy Cards Card Soldier)":          KHRECOMLocationData("Progression",  269_0204),
    "Wonderland Room of Guidance":                                       KHRECOMLocationData("Progression",  269_0205),
    "Wonderland Room of Truth":                                          KHRECOMLocationData("Progression",  269_0206),
    "Wonderland Room of Truth (Enemy Cards Trickmaster)":                KHRECOMLocationData("Progression",  269_0207),
    "Wonderland Room of Rewards (Enemy Cards Xemnas)":                   KHRECOMLocationData("Days"       ,  269_0208), #Days Location
    
    "Olympus Coliseum Field (Attack Card Olympia)":                      KHRECOMLocationData("Progression",  269_0301),
    "Olympus Coliseum Room of Beginnings":                               KHRECOMLocationData("Progression",  269_0302),
    "Olympus Coliseum Room of Guidance":                                 KHRECOMLocationData("Progression",  269_0303),
    "Olympus Coliseum Room of Guidance (Item Cards Hi-Potion)":          KHRECOMLocationData("Progression",  269_0304),
    "Olympus Coliseum Room of Truth":                                    KHRECOMLocationData("Progression",  269_0305),
    "Olympus Coliseum Room of Truth (Enemy Cards Hades)":                KHRECOMLocationData("Progression",  269_0306),
    "Olympus Coliseum Room of Truth (Summon Cards Cloud)":               KHRECOMLocationData("Progression",  269_0307),
    "Olympus Coliseum Room of Rewards (Attack Cards Metal Chocobo)":     KHRECOMLocationData("Progression",  269_0308),
    "Olympus Coliseum Room of Rewards (Attack Cards Total Eclipse)":     KHRECOMLocationData("Days"       ,  269_0309), #Days Location
    
    "Monstro Field (Attack Cards Wishing Star)":                         KHRECOMLocationData("Progression",  269_0401),
    "Monstro Room of Beginnings":                                        KHRECOMLocationData("Progression",  269_0402),
    "Monstro Room of Guidance":                                          KHRECOMLocationData("Progression",  269_0403),
    "Monstro Room of Guidance (Enemy Cards Parasite Cage)":              KHRECOMLocationData("Progression",  269_0404),
    "Monstro Room of Truth":                                             KHRECOMLocationData("Progression",  269_0405),
    "Monstro Room of Truth (Summon Cards Dumbo)":                        KHRECOMLocationData("Progression",  269_0406),
    "Monstro Room of Rewards (Enemy Cards Xaldin)":                      KHRECOMLocationData("Days"       ,  269_0407), #Days Location
    
    "Agrabah Bounty (Magic Cards Gravity)":                              KHRECOMLocationData("Progression",  269_0501),
    "Agrabah Field (Attack Cards Three Wishes)":                         KHRECOMLocationData("Progression",  269_0502),
    "Agrabah Room of Beginnings":                                        KHRECOMLocationData("Progression",  269_0503),
    "Agrabah Room of Guidance":                                          KHRECOMLocationData("Progression",  269_0504),
    "Agrabah Room of Guidance (Item Cards Ether)":                       KHRECOMLocationData("Progression",  269_0505),
    "Agrabah Room of Truth":                                             KHRECOMLocationData("Progression",  269_0506),
    "Agrabah Room of Truth (Enemy Cards Jafar)":                         KHRECOMLocationData("Progression",  269_0507),
    "Agrabah Room of Truth (Summon Cards Genie)":                        KHRECOMLocationData("Progression",  269_0508),
    "Agrabah Room of Rewards (Enemy Cards Luxord)":                      KHRECOMLocationData("Days"       ,  269_0509), #Days Location
    
    "Halloween Town Field (Attack Cards Pumpkinhead)":                   KHRECOMLocationData("Progression",  269_0601),
    "06F Exit Hall Larxene I (Magic Cards Thunder)":                     KHRECOMLocationData("Progression",  269_0602),
    "Halloween Town Room of Beginnings":                                 KHRECOMLocationData("Progression",  269_0603),
    "Halloween Town Room of Guidance":                                   KHRECOMLocationData("Progression",  269_0604),
    "Halloween Town Room of Truth":                                      KHRECOMLocationData("Progression",  269_0605),
    "Halloween Town Room of Truth (Enemy Cards Oogie Boogie)":           KHRECOMLocationData("Progression",  269_0606),
    "Halloween Town Room of Rewards (Attack Cards Bond of Flame)":       KHRECOMLocationData("Days"       ,  269_0607), #Days Location
    
    "Atlantica Field (Attack Cards Crabclaw)":                           KHRECOMLocationData("Progression",  269_0701),
    "07F Exit Hall Riku I (Magic Cards Aero)":                           KHRECOMLocationData("Progression",  269_0702),
    "Atlantica Room of Beginnings":                                      KHRECOMLocationData("Progression",  269_0703),
    "Atlantica Room of Guidance":                                        KHRECOMLocationData("Progression",  269_0704),
    "Atlantica Room of Truth":                                           KHRECOMLocationData("Progression",  269_0705),
    "Atlantica Room of Truth (Enemy Cards Ursula)":                      KHRECOMLocationData("Progression",  269_0706),
    "Atlantica Room of Rewards (Enemy Cards Demyx)":                     KHRECOMLocationData("Days"       ,  269_0707), #Days Location
    
    "Neverland Field (Attack Cards Fairy Harp)":                         KHRECOMLocationData("Progression",  269_0801),
    "Neverland Room of Beginnings":                                      KHRECOMLocationData("Progression",  269_0802),
    "Neverland Room of Guidance":                                        KHRECOMLocationData("Progression",  269_0803),
    "Neverland Room of Truth":                                           KHRECOMLocationData("Progression",  269_0804),
    "Neverland Room of Truth (Enemy Cards Hook)":                        KHRECOMLocationData("Progression",  269_0805),
    "Neverland Room of Truth (Summon Cards Tinker Bell)":                KHRECOMLocationData("Progression",  269_0806),
    "Neverland Room of Rewards (Attack Cards Midnight Roar)":            KHRECOMLocationData("Days"       ,  269_0807), #Days Location
    
    "Hollow Bastion Field (Attack Cards Divine Rose)":                   KHRECOMLocationData("Progression",  269_0901),
    "Hollow Bastion Room of Beginnings":                                 KHRECOMLocationData("Progression",  269_0902),
    "Hollow Bastion Room of Guidance":                                   KHRECOMLocationData("Progression",  269_0903),
    "Hollow Bastion Room of Truth":                                      KHRECOMLocationData("Progression",  269_0904),
    "Hollow Bastion Room of Truth (Enemy Cards Dragon Maleficent)":      KHRECOMLocationData("Progression",  269_0905),
    "Hollow Bastion Room of Rewards (Summon Cards Mushu)":               KHRECOMLocationData("Progression",  269_0906),
    "Hollow Bastion Room of Rewards (Enemy Cards Xigbar)":               KHRECOMLocationData("Days"       ,  269_0907), #Days Location
    
    "100 Acre Wood Clear (Summon Cards Bambi)":                          KHRECOMLocationData("Progression",  269_1001),
    "100 Acre Wood Bumble Rumble (Item Cards Elixir)":                   KHRECOMLocationData("Progression",  269_1002),
    "100 Acre Wood Whirlwind Plunge (Item Cards Mega-Ether)":            KHRECOMLocationData("Progression",  269_1003),
    "100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)":      KHRECOMLocationData("Progression",  269_1004),
    
   #"11F Exit Hall Riku III (Item Cards Mega-Potion)":                   KHRECOMLocationData("Progression",  269_1101),
    "Twilight Town Room of Beginnings":                                  KHRECOMLocationData("Progression",  269_1102),
    "Twilight Town Room of Beginnings (Enemy Cards Vexen)":              KHRECOMLocationData("Progression",  269_1103),
    "Twilight Town Room of Rewards (Enemy Cards Roxas)":                 KHRECOMLocationData("Days"       ,  269_1104), #Days Location
   #"Twilight Town Bounty (Enemy Cards Ansem)":                          KHRECOMLocationData("Days"       ,  269_1105), #Days Location
    
    "Destiny Islands Room of Guidance (Attack Cards Oathkeeper)":        KHRECOMLocationData("Progression",  269_1201),
    "12F Exit Hall Larxene II (Attack Cards Oblivion)":                  KHRECOMLocationData("Progression",  269_1202),
    "12F Exit Hall Larxene II (Enemy Cards Larxene)":                    KHRECOMLocationData("Progression",  269_1203),
    "12F Exit Hall Riku IV (Enemy Cards Riku)":                          KHRECOMLocationData("Progression",  269_1204),
    "Destiny Islands Room of Beginnings":                                KHRECOMLocationData("Progression",  269_1205),
    "Destiny Islands Room of Guidance":                                  KHRECOMLocationData("Progression",  269_1206),
    "Destiny Islands Room of Guidance (Enemy Cards Darkside)":           KHRECOMLocationData("Progression",  269_1207),
    "Destiny Islands Room of Rewards (Item Cards Megalixir)":            KHRECOMLocationData("Progression",  269_1208),
   #"Destiny Islands Bounty (Enemy Cards Zexion)":                       KHRECOMLocationData("Days"       ,  269_1209), #Days Location
    "Destiny Islands Room of Rewards (Attack Cards Two Become One)":     KHRECOMLocationData("Days"       ,  269_1210), #Days Location
    
    "Castle Oblivion Field Marluxia":                                    KHRECOMLocationData("Progression",  269_1301),
    "Castle Oblivion Room of Beginnings":                                KHRECOMLocationData("Progression",  269_1302),
    "Castle Oblivion Room of Beginnings (Enemy Cards Axel)":             KHRECOMLocationData("Progression",  269_1303),
   #"Castle Oblivion Bounty (Enemy Cards Lexaeus)":                      KHRECOMLocationData("Days"       ,  269_1304), #Days Location
    "Castle Oblivion Room of Rewards (Attack Cards Star Seeker)":        KHRECOMLocationData("Days"       ,  269_1305), #Days Location
    
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
    
    "Level 02 (Sleight Sliding Dash)":                                   KHRECOMLocationData("Progression",  269_1501),
    "Level 17 (Sleight Blitz)":                                          KHRECOMLocationData("Progression",  269_1502),
    "Level 07 (Sleight Stun Impact)":                                    KHRECOMLocationData("Progression",  269_1503),
    "Level 22 (Sleight Zantetsuken)":                                    KHRECOMLocationData("Progression",  269_1504),
    "Level 12 (Sleight Strike Raid)":                                    KHRECOMLocationData("Progression",  269_1505),
    "Level 27 (Sleight Sonic Blade)":                                    KHRECOMLocationData("Progression",  269_1506),
    "Level 42 (Sleight Ars Arcanum)":                                    KHRECOMLocationData("Progression",  269_1507),
    "Level 52 (Sleight Ragnarok)":                                       KHRECOMLocationData("Progression",  269_1508),
    "Castle Oblivion Entrance (Sleight Trinity Limit)":                  KHRECOMLocationData("Progression",  269_1509),
    "01F Exit Hall Axel I (Sleight Fira)":                               KHRECOMLocationData("Progression",  269_1510),
    "Starting Checks (Sleight Blizzara)":                                KHRECOMLocationData("Progression",  269_1511),
    "06F Exit Hall Larxene I (Sleight Thundara)":                        KHRECOMLocationData("Progression",  269_1512),
    "Starting Checks (Sleight Cura)":                                    KHRECOMLocationData("Progression",  269_1513),
    "Agrabah Bounty (Sleight Gravira)":                                  KHRECOMLocationData("Progression",  269_1514),
    "Wonderland Bounty (Sleight Stopra)":                                KHRECOMLocationData("Progression",  269_1515),
    "07F Exit Hall Riku I (Sleight Aerora)":                             KHRECOMLocationData("Progression",  269_1516),
    "01F Exit Hall Axel I (Sleight Firaga)":                             KHRECOMLocationData("Progression",  269_1517),
    "Starting Checks (Sleight Blizzaga)":                                KHRECOMLocationData("Progression",  269_1518),
    "06F Exit Hall Larxene I (Sleight Thundaga)":                        KHRECOMLocationData("Progression",  269_1519),
    "Starting Checks (Sleight Curaga)":                                  KHRECOMLocationData("Progression",  269_1520),
    "Agrabah Bounty (Sleight Graviga)":                                  KHRECOMLocationData("Progression",  269_1521),
    "Wonderland Bounty (Sleight Stopga)":                                KHRECOMLocationData("Progression",  269_1522),
    "07F Exit Hall Riku I (Sleight Aeroga)":                             KHRECOMLocationData("Progression",  269_1523),
    "Monstro Bounty (Sleight Fire Raid)":                                KHRECOMLocationData("Progression",  269_1524),
    "Olympus Coliseum Bounty (Sleight Blizzard Raid)":                   KHRECOMLocationData("Progression",  269_1525),
    "Neverland Room of Rewards (Sleight Thunder Raid)":                  KHRECOMLocationData("Progression",  269_1526),
    "Hollow Bastion Bounty (Sleight Reflect Raid)":                      KHRECOMLocationData("Progression",  269_1527),
    "Destiny Islands Bounty (Sleight Judgment)":                         KHRECOMLocationData("Progression",  269_1528),
    "100 Acre Wood Balloon Glider (Sleight Firaga Burst)":               KHRECOMLocationData("Progression",  269_1529),
    "Castle Oblivion Bounty (Sleight Raging Storm)":                     KHRECOMLocationData("Progression",  269_1530),
    "Level 57 (Sleight Mega Flare)":                                     KHRECOMLocationData("Progression",  269_1531),
    "10F Exit Hall Vexen I (Sleight Freeze)":                            KHRECOMLocationData("Progression",  269_1532),
    "Atlantica Bounty (Sleight Homing Blizzara)":                        KHRECOMLocationData("Progression",  269_1533),
    "Monstro Room of Rewards (Sleight Aqua Splash)":                     KHRECOMLocationData("Progression",  269_1534),
    "08F Exit Hall Riku II (Sleight Magnet Spiral)":                     KHRECOMLocationData("Progression",  269_1535),
    "Level 32 (Sleight Lethal Frame)":                                   KHRECOMLocationData("Progression",  269_1536),
    "Atlantica Bounty (Sleight Shock Impact)":                           KHRECOMLocationData("Progression",  269_1537),
    "Level 37 (Sleight Tornado)":                                        KHRECOMLocationData("Progression",  269_1538),
    "Atlantica Room of Rewards (Sleight Quake)":                         KHRECOMLocationData("Progression",  269_1539),
    "Twilight Town Bounty (Sleight Warpinator)":                         KHRECOMLocationData("Progression",  269_1540),
    "Agrabah Room of Rewards (Sleight Warp)":                            KHRECOMLocationData("Progression",  269_1541),
    "Halloween Town Room of Rewards (Sleight Bind)":                     KHRECOMLocationData("Progression",  269_1542),
    "100 Acre Wood Piglet (Sleight Confuse)":                            KHRECOMLocationData("Progression",  269_1543),
    "Halloween Town Entrance (Sleight Terror)":                          KHRECOMLocationData("Progression",  269_1544),
    "Wonderland Room of Rewards (Sleight Synchro)":                      KHRECOMLocationData("Progression",  269_1545),
    "Halloween Town Bounty (Sleight Gifted Miracle)":                    KHRECOMLocationData("Progression",  269_1546),
    "Neverland Bounty (Sleight Teleport)":                               KHRECOMLocationData("Progression",  269_1547),
    "Level 47 (Sleight Holy)":                                           KHRECOMLocationData("Progression",  269_1548),
    "Traverse Town Room of Beginnings (Sleight Proud Roar LV2)":         KHRECOMLocationData("Progression",  269_1549),
    "Traverse Town Room of Beginnings (Sleight Proud Roar LV3)":         KHRECOMLocationData("Progression",  269_1550),
    "Monstro Room of Truth (Sleight Splash LV2)":                        KHRECOMLocationData("Progression",  269_1551),
    "Monstro Room of Truth (Sleight Splash LV3)":                        KHRECOMLocationData("Progression",  269_1552),
    "100 Acre Wood Clear (Sleight Paradise LV2)":                        KHRECOMLocationData("Progression",  269_1553),
    "100 Acre Wood Clear (Sleight Paradise LV3)":                        KHRECOMLocationData("Progression",  269_1554),
    "100 Acre Wood Jump-a-Thon (Sleight Idyll Romp)":                    KHRECOMLocationData("Progression",  269_1555),
    "Hollow Bastion Room of Rewards (Sleight Flare Breath LV2)":         KHRECOMLocationData("Progression",  269_1556),
    "Hollow Bastion Room of Rewards (Sleight Flare Breath LV3)":         KHRECOMLocationData("Progression",  269_1557),
    "Agrabah Room of Truth (Sleight Showtime LV2)":                      KHRECOMLocationData("Progression",  269_1558),
    "Agrabah Room of Truth (Sleight Showtime LV3)":                      KHRECOMLocationData("Progression",  269_1559),
    "Neverland Room of Truth (Sleight Twinkle LV2)":                     KHRECOMLocationData("Progression",  269_1560),
    "Neverland Room of Truth (Sleight Twinkle LV3)":                     KHRECOMLocationData("Progression",  269_1561),
    "Olympus Coliseum Room of Truth (Sleight Cross-slash)":              KHRECOMLocationData("Progression",  269_1562),
    "Olympus Coliseum Room of Truth (Sleight Omnislash)":                KHRECOMLocationData("Progression",  269_1563),
    "100 Acre Wood Veggie Panic (Sleight Cross-slash+)":                 KHRECOMLocationData("Progression",  269_1564),
    "Starting Checks (Sleight Magic LV2)":                               KHRECOMLocationData("Progression",  269_1565),
    "Starting Checks (Sleight Magic LV3)":                               KHRECOMLocationData("Progression",  269_1566),
    "Twilight Town Room of Rewards (Sleight Stardust Blitz)":            KHRECOMLocationData("Progression",  269_1567),
    "Starting Checks (Sleight Goofy Tornado LV2)":                       KHRECOMLocationData("Progression",  269_1568),
    "Starting Checks (Sleight Goofy Tornado LV3)":                       KHRECOMLocationData("Progression",  269_1569),
    "Starting Checks (Sleight Goofy Smash)":                             KHRECOMLocationData("Progression",  269_1570),
    "Starting Checks (Sleight Wild Crush)":                              KHRECOMLocationData("Progression",  269_1571),
    "Agrabah Ally (Sleight Sandstorm LV2)":                              KHRECOMLocationData("Progression",  269_1572),
    "Agrabah Ally (Sleight Sandstorm LV3)":                              KHRECOMLocationData("Progression",  269_1573),
    "Halloween Town Entrance (Sleight Surprise! LV2)":                   KHRECOMLocationData("Progression",  269_1574),
    "Halloween Town Entrance (Sleight Surprise! LV3)":                   KHRECOMLocationData("Progression",  269_1575),
    "Atlantica Ally (Sleight Spiral Wave LV2)":                          KHRECOMLocationData("Progression",  269_1576),
    "Atlantica Ally (Sleight Spiral Wave LV3)":                          KHRECOMLocationData("Progression",  269_1577),
    "Neverland Ally (Sleight Hummingbird LV2)":                          KHRECOMLocationData("Progression",  269_1578),
    "Neverland Ally (Sleight Hummingbird LV3)":                          KHRECOMLocationData("Progression",  269_1579),
    "Hollow Ally (Sleight Furious Volley LV2)":                          KHRECOMLocationData("Progression",  269_1580),
    "Hollow Ally (Sleight Furious Volley LV3)":                          KHRECOMLocationData("Progression",  269_1581),
    "Traverse Town Room of Beginnings (Sleight Lucky Bounty LV2)":       KHRECOMLocationData("Progression",  269_1582),
    "Traverse Town Room of Beginnings (Sleight Lucky Bounty LV3)":       KHRECOMLocationData("Progression",  269_1583),

    
    "Final Marluxia":                                                    KHRECOMLocationData("Progression",  269_9999),
}

event_location_table: Dict[str, KHRECOMLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}