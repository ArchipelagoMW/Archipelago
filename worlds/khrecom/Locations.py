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
    "Agrabah Field (Attack Cards Three Wishes)":                         KHRECOMLocationData("Progression",  269_0002),
    "Atlantica Field (Attack Cards Crabclaw)":                           KHRECOMLocationData("Progression",  269_0003),
    "Halloween Town Field (Attack Cards Pumpkinhead)":                   KHRECOMLocationData("Progression",  269_0004),
    "Neverland Field (Attack Cards Fairy Harp)":                         KHRECOMLocationData("Progression",  269_0005),
    "Monstro Field (Attack Cards Wishing Star)":                         KHRECOMLocationData("Progression",  269_0006),
    "100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)":      KHRECOMLocationData("Progression",  269_0007),
    "Olympus Coliseum Room of Rewards (Attack Cards Metal Chocobo)":     KHRECOMLocationData("Progression",  269_0008),
    "Olympus Coliseum Field (Attack Card Olympia)":                      KHRECOMLocationData("Progression",  269_0009),
    "Traverse Town Room of Rewards (Attack Cards Lionheart)":            KHRECOMLocationData("Progression",  269_0010),
    "Wonderland Field (Attack Cards Lady Luck)":                         KHRECOMLocationData("Progression",  269_0011),
    "Hollow Bastion Field (Attack Cards Divine Rose)":                   KHRECOMLocationData("Progression",  269_0012),
    "Destiny Islands Room of Guidance (Attack Cards Oathkeeper)":        KHRECOMLocationData("Progression",  269_0013),
    "12F Exit Hall Larxene II (Attack Cards Oblivion)":                  KHRECOMLocationData("Progression",  269_0014),
    "Castle Oblivion Room of Rewards (Attack Cards Star Seeker)":        KHRECOMLocationData("Days"       ,  269_0018), #Days Location
    "Olympus Coliseum Room of Rewards (Attack Cards Total Eclipse)":     KHRECOMLocationData("Days"       ,  269_0019), #Days Location
    "Neverland Room of Rewards (Attack Cards Midnight Roar)":            KHRECOMLocationData("Days"       ,  269_0020), #Days Location
    "Traverse Town Bounty (Attack Cards Maverick Flare)":                KHRECOMLocationData("Days"       ,  269_0021), #Days Location
    "Destiny Islands Room of Rewards (Attack Cards Two Become One)":     KHRECOMLocationData("Days"       ,  269_0022), #Days Location
    "Halloween Town Room of Rewards (Attack Cards Bond of Flame)":       KHRECOMLocationData("Days"       ,  269_0023), #Days Location
    "01F Exit Hall Axel I (Magic Cards Fire)":                           KHRECOMLocationData("Progression",  269_0024),
    "Starting Checks (Magic Cards Blizzard)":                            KHRECOMLocationData("Starting",     269_0025),
    "06F Exit Hall Larxene I (Magic Cards Thunder)":                     KHRECOMLocationData("Progression",  269_0026),
    "Starting Checks (Magic Cards Cure)":                                KHRECOMLocationData("Starting",     269_0027),
    "Agrabah Bounty (Magic Cards Gravity)":                              KHRECOMLocationData("Progression",  269_0028),
    "Wonderland Bounty (Magic Cards Stop)":                              KHRECOMLocationData("Progression",  269_0029),
    "07F Exit Hall Riku I (Magic Cards Aero)":                           KHRECOMLocationData("Progression",  269_0030),
    "Traverse Town Room of Beginnings (Summon Cards Simba)":             KHRECOMLocationData("Progression",  269_0031),
    "Agrabah Room of Truth (Summon Cards Genie)":                        KHRECOMLocationData("Progression",  269_0032),
    "100 Acre Wood Clear (Summon Cards Bambi)":                          KHRECOMLocationData("Progression",  269_0033),
    "Monstro Room of Truth (Summon Cards Dumbo)":                        KHRECOMLocationData("Progression",  269_0034),
    "Neverland Room of Truth (Summon Cards Tinker Bell)":                KHRECOMLocationData("Progression",  269_0035),
    "Hollow Bastion Room of Rewards (Summon Cards Mushu)":               KHRECOMLocationData("Progression",  269_0036),
    "Olympus Coliseum Room of Truth (Summon Cards Cloud)":               KHRECOMLocationData("Progression",  269_0037),
    "Starting Checks (Item Cards Potion)":                               KHRECOMLocationData("Starting",     269_0038),
    "Olympus Coliseum Room of Guidance (Item Cards Hi-Potion)":          KHRECOMLocationData("Progression",  269_0039),
   #"11F Exit Hall Riku III (Item Cards Mega-Potion)":                   KHRECOMLocationData("Progression",  269_0040),
    "Agrabah Room of Guidance (Item Cards Ether)":                       KHRECOMLocationData("Progression",  269_0041),
    "100 Acre Wood Whirlwind Plunge (Item Cards Mega-Ether)":            KHRECOMLocationData("Progression",  269_0042),
    "100 Acre Wood Bumble Rumble (Item Cards Elixir)":                   KHRECOMLocationData("Progression",  269_0043),
    "Destiny Islands Room of Rewards (Item Cards Megalixir)":            KHRECOMLocationData("Progression",  269_0044),
    "Traverse Town Room of Truth (Enemy Cards Guard Armor)":             KHRECOMLocationData("Progression",  269_0083),
    "Olympus Coliseum Room of Truth (Enemy Cards Hades)":                KHRECOMLocationData("Progression",  269_0084),
    "Wonderland Room of Truth (Enemy Cards Trickmaster)":                KHRECOMLocationData("Progression",  269_0085),
    "Agrabah Room of Truth (Enemy Cards Jafar)":                         KHRECOMLocationData("Progression",  269_0086),
    "Atlantica Room of Truth (Enemy Cards Ursula)":                      KHRECOMLocationData("Progression",  269_0087),
    "Halloween Town Room of Truth (Enemy Cards Oogie Boogie)":           KHRECOMLocationData("Progression",  269_0088),
    "Monstro Room of Guidance (Enemy Cards Parasite Cage)":              KHRECOMLocationData("Progression",  269_0089),
    "Neverland Room of Truth (Enemy Cards Hook)":                        KHRECOMLocationData("Progression",  269_0090),
    "Hollow Bastion Room of Truth (Enemy Cards Dragon Maleficent)":      KHRECOMLocationData("Progression",  269_0091),
    "Destiny Islands Room of Guidance (Enemy Cards Darkside)":           KHRECOMLocationData("Progression",  269_0092),
    "12F Exit Hall Riku IV (Enemy Cards Riku)":                          KHRECOMLocationData("Progression",  269_0093),
    "Wonderland Room of Beginnings (Enemy Cards Card Soldier)":          KHRECOMLocationData("Progression",  269_0094),
   #"Twilight Town Bounty (Enemy Cards Ansem)":                          KHRECOMLocationData("Days"       ,  269_0095), #RR
    "Wonderland Room of Rewards (Enemy Cards Xemnas)":                   KHRECOMLocationData("Days"       ,  269_0096), #Days Location
    "Hollow Bastion Room of Rewards (Enemy Cards Xigbar)":               KHRECOMLocationData("Days"       ,  269_0097), #Days Location
    "Monstro Room of Rewards (Enemy Cards Xaldin)":                      KHRECOMLocationData("Days"       ,  269_0098), #Days Location
    "Twilight Town Room of Beginnings (Enemy Cards Vexen)":              KHRECOMLocationData("Progression",  269_0099),
   #"Castle Oblivion Bounty (Enemy Cards Lexaeus)":                      KHRECOMLocationData("Days"       ,  269_0100), #RR
   #"Destiny Islands Bounty (Enemy Cards Zexion)":                       KHRECOMLocationData("Days"       ,  269_0101), #RR
    "Traverse Town Room of Rewards (Enemy Cards Saix)":                  KHRECOMLocationData("Days"       ,  269_0102), #Days Location
    "Castle Oblivion Room of Beginnings (Enemy Cards Axel)":             KHRECOMLocationData("Progression",  269_0103),
    "Atlantica Room of Rewards (Enemy Cards Demyx)":                     KHRECOMLocationData("Days"       ,  269_0104), #Days Location
    "Agrabah Room of Rewards (Enemy Cards Luxord)":                      KHRECOMLocationData("Days"       ,  269_0105), #Days Location
    "Castle Oblivion Field Marluxia":                                    KHRECOMLocationData("Progression",  269_0106),
    "12F Exit Hall Larxene II (Enemy Cards Larxene)":                    KHRECOMLocationData("Progression",  269_0107),
    "Twilight Town Room of Rewards (Enemy Cards Roxas)":                 KHRECOMLocationData("Days"       ,  269_0108), #Days Location
    
    "Traverse Town Room of Beginnings":                                  KHRECOMLocationData("Progression",  269_1001),
    "Traverse Town Room of Guidance":                                    KHRECOMLocationData("Progression",  269_1002),
    "Traverse Town Room of Truth":                                       KHRECOMLocationData("Progression",  269_1003),
    "Agrabah Room of Beginnings":                                        KHRECOMLocationData("Progression",  269_1004),
    "Agrabah Room of Guidance":                                          KHRECOMLocationData("Progression",  269_1005),
    "Agrabah Room of Truth":                                             KHRECOMLocationData("Progression",  269_1006),
    "Olympus Coliseum Room of Beginnings":                               KHRECOMLocationData("Progression",  269_1007),
    "Olympus Coliseum Room of Guidance":                                 KHRECOMLocationData("Progression",  269_1008),
    "Olympus Coliseum Room of Truth":                                    KHRECOMLocationData("Progression",  269_1009),
    "Wonderland Room of Beginnings":                                     KHRECOMLocationData("Progression",  269_1010),
    "Wonderland Room of Guidance":                                       KHRECOMLocationData("Progression",  269_1011),
    "Wonderland Room of Truth":                                          KHRECOMLocationData("Progression",  269_1012),
    "Monstro Room of Beginnings":                                        KHRECOMLocationData("Progression",  269_1010),
    "Monstro Room of Guidance":                                          KHRECOMLocationData("Progression",  269_1011),
    "Monstro Room of Truth":                                             KHRECOMLocationData("Progression",  269_1012),
    "Halloween Town Room of Beginnings":                                 KHRECOMLocationData("Progression",  269_1013),
    "Halloween Town Room of Guidance":                                   KHRECOMLocationData("Progression",  269_1014),
    "Halloween Town Room of Truth":                                      KHRECOMLocationData("Progression",  269_1015),
    "Atlantica Room of Beginnings":                                      KHRECOMLocationData("Progression",  269_1016),
    "Atlantica Room of Guidance":                                        KHRECOMLocationData("Progression",  269_1017),
    "Atlantica Room of Truth":                                           KHRECOMLocationData("Progression",  269_1018),
    "Neverland Room of Beginnings":                                      KHRECOMLocationData("Progression",  269_1019),
    "Neverland Room of Guidance":                                        KHRECOMLocationData("Progression",  269_1020),
    "Neverland Room of Truth":                                           KHRECOMLocationData("Progression",  269_1021),
    "Hollow Bastion Room of Beginnings":                                 KHRECOMLocationData("Progression",  269_1022),
    "Hollow Bastion Room of Guidance":                                   KHRECOMLocationData("Progression",  269_1023),
    "Hollow Bastion Room of Truth":                                      KHRECOMLocationData("Progression",  269_1024),
    "Twilight Town Room of Beginnings":                                  KHRECOMLocationData("Progression",  269_1028),
    "Destiny Islands Room of Beginnings":                                KHRECOMLocationData("Progression",  269_1031),
    "Destiny Islands Room of Guidance":                                  KHRECOMLocationData("Progression",  269_1032),
    "Castle Oblivion Room of Beginnings":                                KHRECOMLocationData("Progression",  269_1034),
    
    "Heartless Air Pirate":                                              KHRECOMLocationData("Progression",  269_1101),
    "Heartless Air Soldier":                                             KHRECOMLocationData("Progression",  269_1102),
    "Heartless Aquatank":                                                KHRECOMLocationData("Progression",  269_1103),
    "Heartless Bandit":                                                  KHRECOMLocationData("Progression",  269_1104),
    "Heartless Barrel Spider":                                           KHRECOMLocationData("Progression",  269_1105),
    "Heartless Black Fungus":                                            KHRECOMLocationData("Progression",  269_1106),
    "Heartless Blue Rhapsody":                                           KHRECOMLocationData("Progression",  269_1107),
    "Heartless Bouncywild":                                              KHRECOMLocationData("Progression",  269_1108),
    "Heartless Creeper Plant":                                           KHRECOMLocationData("Progression",  269_1109),
    "Heartless Crescendo":                                               KHRECOMLocationData("Progression",  269_1110),
    "Heartless Darkball":                                                KHRECOMLocationData("Progression",  269_1111),
    "Heartless Defender":                                                KHRECOMLocationData("Progression",  269_1112),
    "Heartless Fat Bandit":                                              KHRECOMLocationData("Progression",  269_1113),
    "Heartless Gargoyle":                                                KHRECOMLocationData("Progression",  269_1114),
    "Heartless Green Requiem":                                           KHRECOMLocationData("Progression",  269_1115),
    "Heartless Large Body":                                              KHRECOMLocationData("Progression",  269_1116),
    "Heartless Neoshadow":                                               KHRECOMLocationData("Progression",  269_1117),
    "Heartless Pirate":                                                  KHRECOMLocationData("Progression",  269_1118),
    "Heartless Powerwild":                                               KHRECOMLocationData("Progression",  269_1119),
    "Heartless Red Nocturne":                                            KHRECOMLocationData("Progression",  269_1120),
    "Heartless Screwdiver":                                              KHRECOMLocationData("Progression",  269_1121),
    "Heartless Sea Neon":                                                KHRECOMLocationData("Progression",  269_1122),
    "Heartless Search Ghost":                                            KHRECOMLocationData("Progression",  269_1123),
    "Heartless Shadow":                                                  KHRECOMLocationData("Progression",  269_1124),
    "Heartless Soldier":                                                 KHRECOMLocationData("Progression",  269_1125),
    "Heartless Tornado Step":                                            KHRECOMLocationData("Progression",  269_1126),
    "Heartless White Mushroom":                                          KHRECOMLocationData("Progression",  269_1127),
    "Heartless Wight Knight":                                            KHRECOMLocationData("Progression",  269_1128),
    "Heartless Wizard":                                                  KHRECOMLocationData("Progression",  269_1129),
    "Heartless Wyvern":                                                  KHRECOMLocationData("Progression",  269_1130),
    "Heartless Yellow Opera":                                            KHRECOMLocationData("Progression",  269_1131),
    
    "Level 02 (Sleight Sliding Dash)":                                   KHRECOMLocationData("Progression",  269_1201),
    "Level 17 (Sleight Blitz)":                                          KHRECOMLocationData("Progression",  269_1202),
    "Level 07 (Sleight Stun Impact)":                                    KHRECOMLocationData("Progression",  269_1203),
    "Level 22 (Sleight Zantetsuken)":                                    KHRECOMLocationData("Progression",  269_1204),
    "Level 12 (Sleight Strike Raid)":                                    KHRECOMLocationData("Progression",  269_1205),
    "Level 27 (Sleight Sonic Blade)":                                    KHRECOMLocationData("Progression",  269_1206),
    "Level 42 (Sleight Ars Arcanum)":                                    KHRECOMLocationData("Progression",  269_1207),
    "Level 52 (Sleight Ragnarok)":                                       KHRECOMLocationData("Progression",  269_1208),
    "Castle Oblivion Entrance (Sleight Trinity Limit)":                  KHRECOMLocationData("Progression",  269_1209),
    "01F Exit Hall Axel I (Sleight Fira)":                               KHRECOMLocationData("Progression",  269_1210),
    "Starting Checks (Sleight Blizzara)":                                KHRECOMLocationData("Progression",  269_1211),
    "06F Exit Hall Larxene I (Sleight Thundara)":                        KHRECOMLocationData("Progression",  269_1212),
    "Starting Checks (Sleight Cura)":                                    KHRECOMLocationData("Progression",  269_1213),
    "Agrabah Bounty (Sleight Gravira)":                                  KHRECOMLocationData("Progression",  269_1214),
    "Wonderland Bounty (Sleight Stopra)":                                KHRECOMLocationData("Progression",  269_1215),
    "07F Exit Hall Riku I (Sleight Aerora)":                             KHRECOMLocationData("Progression",  269_1216),
    "01F Exit Hall Axel I (Sleight Firaga)":                             KHRECOMLocationData("Progression",  269_1217),
    "Starting Checks (Sleight Blizzaga)":                                KHRECOMLocationData("Progression",  269_1218),
    "06F Exit Hall Larxene I (Sleight Thundaga)":                        KHRECOMLocationData("Progression",  269_1219),
    "Starting Checks (Sleight Curaga)":                                  KHRECOMLocationData("Progression",  269_1220),
    "Agrabah Bounty (Sleight Graviga)":                                  KHRECOMLocationData("Progression",  269_1221),
    "Wonderland Bounty (Sleight Stopga)":                                KHRECOMLocationData("Progression",  269_1222),
    "07F Exit Hall Riku I (Sleight Aeroga)":                             KHRECOMLocationData("Progression",  269_1223),
    "Monstro Bounty (Sleight Fire Raid)":                                KHRECOMLocationData("Progression",  269_1224),
    "Olympus Coliseum Bounty (Sleight Blizzard Raid)":                   KHRECOMLocationData("Progression",  269_1225),
    "Neverland Room of Rewards (Sleight Thunder Raid)":                  KHRECOMLocationData("Progression",  269_1226),
    "Hollow Bastion Bounty (Sleight Reflect Raid)":                      KHRECOMLocationData("Progression",  269_1227),
    "Destiny Islands Bounty (Sleight Judgment)":                         KHRECOMLocationData("Progression",  269_1228),
    "100 Acre Wood Balloon Glider (Sleight Firaga Burst)":               KHRECOMLocationData("Progression",  269_1229),
    "Castle Oblivion Bounty (Sleight Raging Storm)":                     KHRECOMLocationData("Progression",  269_1230),
    "Level 57 (Sleight Mega Flare)":                                     KHRECOMLocationData("Progression",  269_1231),
    "10F Exit Hall Vexen I (Sleight Freeze)":                            KHRECOMLocationData("Progression",  269_1232),
    "Atlantica Bounty (Sleight Homing Blizzara)":                        KHRECOMLocationData("Progression",  269_1233),
    "Monstro Room of Rewards (Sleight Aqua Splash)":                     KHRECOMLocationData("Progression",  269_1234),
    "08F Exit Hall Riku II (Sleight Magnet Spiral)":                     KHRECOMLocationData("Progression",  269_1235),
    "Level 32 (Sleight Lethal Frame)":                                   KHRECOMLocationData("Progression",  269_1236),
    "Atlantica Bounty (Sleight Shock Impact)":                           KHRECOMLocationData("Progression",  269_1237),
    "Level 37 (Sleight Tornado)":                                        KHRECOMLocationData("Progression",  269_1238),
    "Atlantica Room of Rewards (Sleight Quake)":                         KHRECOMLocationData("Progression",  269_1239),
    "Twilight Town Bounty (Sleight Warpinator)":                         KHRECOMLocationData("Progression",  269_1240),
    "Agrabah Room of Rewards (Sleight Warp)":                            KHRECOMLocationData("Progression",  269_1241),
    "Halloween Town Room of Rewards (Sleight Bind)":                     KHRECOMLocationData("Progression",  269_1242),
    "100 Acre Wood Piglet (Sleight Confuse)":                            KHRECOMLocationData("Progression",  269_1243),
    "Halloween Town Entrance (Sleight Terror)":                          KHRECOMLocationData("Progression",  269_1244),
    "Wonderland Room of Rewards (Sleight Synchro)":                      KHRECOMLocationData("Progression",  269_1245),
    "Halloween Town Bounty (Sleight Gifted Miracle)":                    KHRECOMLocationData("Progression",  269_1246),
    "Neverland Bounty (Sleight Teleport)":                               KHRECOMLocationData("Progression",  269_1247),
    "Level 47 (Sleight Holy)":                                           KHRECOMLocationData("Progression",  269_1248),
    "Traverse Town Room of Beginnings (Sleight Proud Roar LV2)":         KHRECOMLocationData("Progression",  269_1249),
    "Traverse Town Room of Beginnings (Sleight Proud Roar LV3)":         KHRECOMLocationData("Progression",  269_1250),
    "Monstro Room of Truth (Sleight Splash LV2)":                        KHRECOMLocationData("Progression",  269_1251),
    "Monstro Room of Truth (Sleight Splash LV3)":                        KHRECOMLocationData("Progression",  269_1252),
    "100 Acre Wood Clear (Sleight Paradise LV2)":                        KHRECOMLocationData("Progression",  269_1253),
    "100 Acre Wood Clear (Sleight Paradise LV3)":                        KHRECOMLocationData("Progression",  269_1254),
    "100 Acre Wood Jump-a-Thon (Sleight Idyll Romp)":                    KHRECOMLocationData("Progression",  269_1255),
    "Hollow Bastion Room of Rewards (Sleight Flare Breath LV2)":         KHRECOMLocationData("Progression",  269_1256),
    "Hollow Bastion Room of Rewards (Sleight Flare Breath LV3)":         KHRECOMLocationData("Progression",  269_1257),
    "Agrabah Room of Truth (Sleight Showtime LV2)":                      KHRECOMLocationData("Progression",  269_1258),
    "Agrabah Room of Truth (Sleight Showtime LV3)":                      KHRECOMLocationData("Progression",  269_1259),
    "Neverland Room of Truth (Sleight Twinkle LV2)":                     KHRECOMLocationData("Progression",  269_1260),
    "Neverland Room of Truth (Sleight Twinkle LV3)":                     KHRECOMLocationData("Progression",  269_1261),
    "Olympus Coliseum Room of Truth (Sleight Cross-slash)":              KHRECOMLocationData("Progression",  269_1262),
    "Olympus Coliseum Room of Truth (Sleight Omnislash)":                KHRECOMLocationData("Progression",  269_1263),
    "100 Acre Wood Veggie Panic (Sleight Cross-slash+)":                 KHRECOMLocationData("Progression",  269_1264),
    "Starting Checks (Sleight Magic LV2)":                               KHRECOMLocationData("Progression",  269_1265),
    "Starting Checks (Sleight Magic LV3)":                               KHRECOMLocationData("Progression",  269_1266),
    "Twilight Town Room of Rewards (Sleight Stardust Blitz)":            KHRECOMLocationData("Progression",  269_1267),
    "Starting Checks (Sleight Goofy Tornado LV2)":                       KHRECOMLocationData("Progression",  269_1268),
    "Starting Checks (Sleight Goofy Tornado LV3)":                       KHRECOMLocationData("Progression",  269_1269),
    "Starting Checks (Sleight Goofy Smash)":                             KHRECOMLocationData("Progression",  269_1270),
    "Starting Checks (Sleight Wild Crush)":                              KHRECOMLocationData("Progression",  269_1271),
    "Agrabah Ally (Sleight Sandstorm LV2)":                              KHRECOMLocationData("Progression",  269_1272),
    "Agrabah Ally (Sleight Sandstorm LV3)":                              KHRECOMLocationData("Progression",  269_1273),
    "Halloween Town Ally (Sleight Surprise! LV2)":                       KHRECOMLocationData("Progression",  269_1274),
    "Halloween Town Ally (Sleight Surprise! LV3)":                       KHRECOMLocationData("Progression",  269_1275),
    "Atlantica Ally (Sleight Spiral Wave LV2)":                          KHRECOMLocationData("Progression",  269_1276),
    "Atlantica Ally (Sleight Spiral Wave LV3)":                          KHRECOMLocationData("Progression",  269_1277),
    "Neverland Ally (Sleight Hummingbird LV2)":                          KHRECOMLocationData("Progression",  269_1278),
    "Neverland Ally (Sleight Hummingbird LV3)":                          KHRECOMLocationData("Progression",  269_1279),
    "Hollow Bastion Ally (Sleight Furious Volley LV2)":                  KHRECOMLocationData("Progression",  269_1280),
    "Hollow Bastion Ally (Sleight Furious Volley LV3)":                  KHRECOMLocationData("Progression",  269_1281),
    "Traverse Town Room of Beginnings (Sleight Lucky Bounty LV2)":       KHRECOMLocationData("Progression",  269_1282),
    "Traverse Town Room of Beginnings (Sleight Lucky Bounty LV3)":       KHRECOMLocationData("Progression",  269_1283),

    "Final Marluxia":                                                    KHRECOMLocationData("Progression",  269_9999),
}

event_location_table: Dict[str, KHRECOMLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}