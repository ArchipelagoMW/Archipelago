from typing import Dict, NamedTuple, Optional
import typing


from BaseClasses import Location


class KHCOMLocation(Location):
    game: str = "Kingdom Hearts Chain of Memories"


class KHCOMLocationData(NamedTuple):
    category: str
    code: Optional[int] = None


def get_locations_by_category(category: str) -> Dict[str, KHCOMLocationData]:
    location_dict: Dict[str, KHCOMLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)

    return location_dict


location_table: Dict[str, KHCOMLocationData] = {

    "Starting Checks (Attack Cards Kingdom Key)":                        KHCOMLocationData("Starting",     267_0001),
    "Starting Checks (Characters I Donald)":                             KHCOMLocationData("Starting",     267_0002),
    "Starting Checks (Characters I Goofy)":                              KHCOMLocationData("Starting",     267_0003),
    "Starting Checks (Characters I Jiminy Cricket)":                     KHCOMLocationData("Starting",     267_0004),
    "Starting Checks (Characters I Kairi)":                              KHCOMLocationData("Starting",     267_0005),
    "Starting Checks (Characters I Riku)":                               KHCOMLocationData("Starting",     267_0006),
    "Starting Checks (Characters I Sora)":                               KHCOMLocationData("Starting",     267_0007),
    "Starting Checks (Item Cards Potion)":                               KHCOMLocationData("Starting",     267_0008),
    "Starting Checks (Magic Cards Blizzard)":                            KHCOMLocationData("Starting",     267_0009),
    "Starting Checks (Magic Cards Cure)":                                KHCOMLocationData("Starting",     267_0010),
    
    "F01 Traverse Town Post Floor (Characters I Aerith)":                KHCOMLocationData("Boss",         267_0101),
    "F01 Traverse Town Post Floor (Characters I Axel)":                  KHCOMLocationData("Boss",         267_0102),
    "F01 Traverse Town Post Floor (Characters I Cid)":                   KHCOMLocationData("Boss",         267_0103),
    "F01 Traverse Town Post Floor (Characters I Leon)":                  KHCOMLocationData("Boss",         267_0104),
    "F01 Traverse Town Post Floor (Characters I Yuffie)":                KHCOMLocationData("Boss",         267_0105),
    "F01 Traverse Town Post Floor (Magic Cards Fire)":                   KHCOMLocationData("Boss",         267_0106),
    "F01 Traverse Town Post Floor (Story Sora's Tale I)":                KHCOMLocationData("Boss",         267_0107),
    "F01 Traverse Town Post Floor (Story Traverse Town)":                KHCOMLocationData("Boss",         267_0108),
    "F01 Traverse Town Room of Beginnings (Characters I Simba)":         KHCOMLocationData("Progression",  267_0109),
    "F01 Traverse Town Room of Beginnings (Magic Cards Simba)":          KHCOMLocationData("Progression",  267_0110),
    "F01 Traverse Town Room of Rewards (Attack Cards Lionheart)":        KHCOMLocationData("Progression",  267_0111),
    "F01 Traverse Town Room of Truth (The Heartless Guard Armor)":       KHCOMLocationData("Boss",         267_0112),
    
    "F02 Wonderland Bounty (Magic Cards Stop)":                          KHCOMLocationData("Progression",  267_0201),
    "F02 Wonderland Field (Attack Cards Lady Luck)":                     KHCOMLocationData("Progression",  267_0202),
    "F02 Wonderland Post Floor (Characters II Alice)":                   KHCOMLocationData("Boss",         267_0203),
    "F02 Wonderland Post Floor (Characters II Card of Hearts)":          KHCOMLocationData("Boss",         267_0204),
    "F02 Wonderland Post Floor (Characters II Card of Spades)":          KHCOMLocationData("Boss",         267_0205),
    "F02 Wonderland Post Floor (Characters II The Cheshire Cat)":        KHCOMLocationData("Boss",         267_0206),
    "F02 Wonderland Post Floor (Characters II The Queen of Hearts)":     KHCOMLocationData("Boss",         267_0207),
    "F02 Wonderland Post Floor (Characters II The White Rabbit)":        KHCOMLocationData("Boss",         267_0208),
    "F02 Wonderland Post Floor (Story Wonderland)":                      KHCOMLocationData("Boss",         267_0209),
    "F02 Wonderland Room of Truth (The Heartless Trickmaster)":          KHCOMLocationData("Boss",         267_0210),
    
    "F03 Olympus Coliseum Field (Attack Cards Olympia)":                 KHCOMLocationData("Progression",  267_0301),
    "F03 Olympus Coliseum Post Floor (Characters I Cloud)":              KHCOMLocationData("Boss",         267_0302),
    "F03 Olympus Coliseum Post Floor (Characters II Hades)":             KHCOMLocationData("Boss",         267_0303),
    "F03 Olympus Coliseum Post Floor (Characters II Philoctetes)":       KHCOMLocationData("Boss",         267_0304),
    "F03 Olympus Coliseum Post Floor (Characters II Hercules)":          KHCOMLocationData("Boss",         267_0305),
    "F03 Olympus Coliseum Post Floor (Story Olympus Coliseum)":          KHCOMLocationData("Boss",         267_0306),
    "F03 Olympus Coliseum Room of Guidance (Item Cards Hi-Potion)":      KHCOMLocationData("Boss",         267_0307),
    "F03 Olympus Coliseum Room of Rewards (Attack Card Metal Chocobo)":  KHCOMLocationData("Progression",  267_0308),
    "F03 Olympus Coliseum Room of Truth (Magic Cards Cloud)":            KHCOMLocationData("Boss",         267_0309),
    
    "F04 Monstro Field (Wishing Star)":                                  KHCOMLocationData("Progression",  267_0401),
    "F04 Monstro Post Floor (Characters II Geppetto)":                   KHCOMLocationData("Boss",         267_0402),
    "F04 Monstro Post Floor (Characters II Pinocchio)":                  KHCOMLocationData("Boss",         267_0403),
    "F04 Monstro Post Floor (Story Monstro)":                            KHCOMLocationData("Boss",         267_0404),
    "F04 Monstro Room of Guidance (The Heartless Parasite Cage)":        KHCOMLocationData("Boss",         267_0405),
    "F04 Monstro Room of Truth (Characters I Dumbo)":                    KHCOMLocationData("Boss",         267_0406),
    "F04 Monstro Room of Truth (Magic Cards Dumbo)":                     KHCOMLocationData("Boss",         267_0407),
    
    "F05 Agrabah Bounty (Magic Cards Gravity)":                          KHCOMLocationData("Progression",  267_0501),
    "F05 Agrabah Field (Attack Cards Three Wishes)":                     KHCOMLocationData("Progression",  267_0502),
    "F05 Agrabah Post Floor (Characters II Aladdin)":                    KHCOMLocationData("Boss",         267_0503),
    "F05 Agrabah Post Floor (Characters II Genie)":                      KHCOMLocationData("Boss",         267_0504),
    "F05 Agrabah Post Floor (Characters II Iago)":                       KHCOMLocationData("Boss",         267_0505),
    "F05 Agrabah Post Floor (Characters II Jafar)":                      KHCOMLocationData("Boss",         267_0506),
    "F05 Agrabah Post Floor (Characters II Jafar-Genie)":                KHCOMLocationData("Boss",         267_0507),
    "F05 Agrabah Post Floor (Characters II Jasmine)":                    KHCOMLocationData("Boss",         267_0508),
    "F05 Agrabah Post Floor (Story Agrabah)":                            KHCOMLocationData("Boss",         267_0509),
    "F05 Agrabah Room of Guidance (Item Cards Ether)":                   KHCOMLocationData("Boss",         267_0510),
    "F05 Agrabah Room of Truth (Magic Cards Genie)":                     KHCOMLocationData("Boss",         267_0511),
    
    "F06 Halloween Town Field (Attack Cards Pumpkinhead)":               KHCOMLocationData("Progression",  267_0601),
    "F06 Halloween Town Post Floor (Characters II Dr. Finkelstein)":     KHCOMLocationData("Boss",         267_0602),
    "F06 Halloween Town Post Floor (Characters II Jack)":                KHCOMLocationData("Boss",         267_0603),
    "F06 Halloween Town Post Floor (Characters II Oogie Boogie)":        KHCOMLocationData("Boss",         267_0604),
    "F06 Halloween Town Post Floor (Characters II Sally)":               KHCOMLocationData("Boss",         267_0605),
    "F06 Halloween Town Post Floor (Magic Cards Thunder)":               KHCOMLocationData("Boss",         267_0606),
    "F06 Halloween Town Post Floor (Story Halloween Town)":              KHCOMLocationData("Boss",         267_0607),
    "F06 Halloween Town Post Floor (Story Sora's Tale II)":              KHCOMLocationData("Boss",         267_0608),
    
    "F07 Atlantica Field (Crabclaw)":                                    KHCOMLocationData("Progression",  267_0701),
    "F07 Atlantica Post Floor (Characters II Ariel)":                    KHCOMLocationData("Boss",         267_0702),
    "F07 Atlantica Post Floor (Characters II Flounder)":                 KHCOMLocationData("Boss",         267_0703),
    "F07 Atlantica Post Floor (Characters II Ursula)":                   KHCOMLocationData("Boss",         267_0704),
    "F07 Atlantica Post Floor (Characters II Sebastion)":                KHCOMLocationData("Boss",         267_0705),
    "F07 Atlantica Post Floor (Story Atlantica)":                        KHCOMLocationData("Boss",         267_0706),
    "F07 Atlantica Post Floor (Magic Cards Aero)":                       KHCOMLocationData("Boss",         267_0707),
    
    "F08 Neverland Field (Attack Cards Fairy Harp)":                     KHCOMLocationData("Progression",  267_0801),
    "F08 Neverland Post Floor (Characters II Hook)":                     KHCOMLocationData("Boss",         267_0802),
    "F08 Neverland Post Floor (Characters II Peter Pan)":                KHCOMLocationData("Boss",         267_0803),
    "F08 Neverland Post Floor (Characters II Tinker Bell)":              KHCOMLocationData("Boss",         267_0804),
    "F08 Neverland Post Floor (Characters II Wendy)":                    KHCOMLocationData("Boss",         267_0805),
    "F08 Neverland Post Floor (Story Neverland)":                        KHCOMLocationData("Boss",         267_0806),
    "F08 Neverland Room of Truth (Magic Cards Tinker Bell)":             KHCOMLocationData("Boss",         267_0807),
    
    "F09 Hollow Bastion Field (Attack Cards Divine Rose)":               KHCOMLocationData("Progression",  267_0901),
    "F09 Hollow Bastion Post Floor (Characters II Belle)":               KHCOMLocationData("Boss",         267_0902),
    "F09 Hollow Bastion Post Floor (Characters II Dragon Maleficent)":   KHCOMLocationData("Boss",         267_0903),
    "F09 Hollow Bastion Post Floor (Characters II Maleficent)":          KHCOMLocationData("Boss",         267_0904),
    "F09 Hollow Bastion Post Floor (Characters II The Beast)":           KHCOMLocationData("Boss",         267_0905),
    "F09 Hollow Bastion Post Floor (Story Hollow Bastion)":              KHCOMLocationData("Boss",         267_0906),
    "F09 Hollow Bastion Post Floor (Story Sora's Tale III)":             KHCOMLocationData("Boss",         267_0907),
    "F09 Hollow Bastion Room of Rewards (Characters I Mushu)":           KHCOMLocationData("Progression",  267_0908),
    "F09 Hollow Bastion Room of Rewards (Magic Cards Mushu)":            KHCOMLocationData("Progression",  267_0909),
    
    "F10 100 Acre Wood Complete (Characters I Bambi)":                   KHCOMLocationData("Progression",  267_1001),
    "F10 100 Acre Wood Complete (Magic Cards Bambi)":                    KHCOMLocationData("Progression",  267_1002),
    "F10 100 Acre Wood Field Scene Owl (Attack Cards Spellbinder)":      KHCOMLocationData("Progression",  267_1003),
    "F10 100 Acre Wood Field Scene Eeyore (Characters II Eeyore)":       KHCOMLocationData("Progression",  267_1004),
    "F10 100 Acre Wood Field Scene Owl (Characters II Owl)":             KHCOMLocationData("Progression",  267_1005),
    "F10 100 Acre Wood Field Scene Piglet (Characters II Piglet)":       KHCOMLocationData("Progression",  267_1006),
    "F10 100 Acre Wood Field Scene Rabbit (Characters II Rabbit)":       KHCOMLocationData("Progression",  267_1007),
    "F10 100 Acre Wood Field Scene Roo (Characters II Roo)":             KHCOMLocationData("Progression",  267_1008),
    "F10 100 Acre Wood Field Scene Tigger (Characters II Tigger)":       KHCOMLocationData("Progression",  267_1009),
    "F10 100 Acre Wood Post Floor (Characters II Vexen)":                KHCOMLocationData("Boss",         267_1010),
    "F10 100 Acre Wood Post Floor (Characters II Winnie the Pooh)":      KHCOMLocationData("Progression",  267_1011),
    "F10 100 Acre Wood Post Floor (Item Cards Mega-Ether)":              KHCOMLocationData("Boss",         267_1012),
    "F10 100 Acre Wood Post Floor (Story 100 Acre Wood)":                KHCOMLocationData("Progression",  267_1013),
    "F10 100 Acre Wood Field Scene Roo (Item Cards Elixir)":             KHCOMLocationData("Progression",  267_1014),
    
    "F11 Twilight Town Post Floor (Item Cards Mega-Potion)":             KHCOMLocationData("Boss",         267_1101),
    "F11 Twilight Town Post Floor (Story Twilight Town)":                KHCOMLocationData("Boss",         267_1102),
    
    "F12 Destiny Islands Post Floor (Attack Cards Oathkeeper)":          KHCOMLocationData("Boss",         267_1201),
    "F12 Destiny Islands Post Floor (Characters I Selphie)":             KHCOMLocationData("Boss",         267_1202),
    "F12 Destiny Islands Post Floor (Characters I Tidus)":               KHCOMLocationData("Boss",         267_1203),
    "F12 Destiny Islands Post Floor (Characters I Wakka)":               KHCOMLocationData("Boss",         267_1204),
    "F12 Destiny Islands Post Floor (Characters I Riku Replica)":        KHCOMLocationData("Boss",         267_1205),
    "F12 Destiny Islands Post Floor (Characters I Namine)":              KHCOMLocationData("Boss",         267_1206),
    "F12 Destiny Islands Post Floor (Story Destiny Islands)":            KHCOMLocationData("Boss",         267_1207),
    "F12 Destiny Islands Post Floor (Story Sora's Tale IV)":             KHCOMLocationData("Boss",         267_1208),
    "F12 Destiny Islands Room of Truth (The Heartless Darkside)":        KHCOMLocationData("Boss",         267_1209),
    #"F12 Destiny Islands Post Floor (Attack Cards Oblivion)":           KHCOMLocationData("Boss",         267_1210),
    "F12 Destiny Islands Room of Rewards (Item Cards Megalixir)":        KHCOMLocationData("Progression",  267_1211),
                                                                         
    "F13 Castle Oblivion Event (Characters I Marluxia)":                 KHCOMLocationData("Progression",  267_1301),
    "F13 Castle Oblivion Post Floor (Story Castle Oblivion)":            KHCOMLocationData("Boss",         267_1302),
    "F13 Castle Oblivion Post Marluxia (Attack Cards Diamond Dust)":     KHCOMLocationData("Boss",         267_1303),
    "F13 Castle Oblivion Post Marluxia (Attack Cards One-Winged Angel)": KHCOMLocationData("Boss",         267_1304),
    
    "Heartless Air Pirate":                                              KHCOMLocationData("Progression",  267_1401),
    "Heartless Air Soldier":                                             KHCOMLocationData("Progression",  267_1402),
    "Heartless Aquatank":                                                KHCOMLocationData("Progression",  267_1403),
    "Heartless Bandit":                                                  KHCOMLocationData("Progression",  267_1404),
    "Heartless Barrel Spider":                                           KHCOMLocationData("Progression",  267_1405),
    "Heartless Black Fungus":                                            KHCOMLocationData("Progression",  267_1406),
    "Heartless Blue Rhapsody":                                           KHCOMLocationData("Progression",  267_1407),
    "Heartless Bouncywild":                                              KHCOMLocationData("Progression",  267_1408),
    "Heartless Creeper Plant":                                           KHCOMLocationData("Progression",  267_1409),
    "Heartless Crescendo":                                               KHCOMLocationData("Progression",  267_1410),
    "Heartless Darkball":                                                KHCOMLocationData("Progression",  267_1411),
    "Heartless Defender":                                                KHCOMLocationData("Progression",  267_1412),
    "Heartless Fat Bandit":                                              KHCOMLocationData("Progression",  267_1413),
    "Heartless Gargoyle":                                                KHCOMLocationData("Progression",  267_1414),
    "Heartless Green Requiem":                                           KHCOMLocationData("Progression",  267_1415),
    "Heartless Large Body":                                              KHCOMLocationData("Progression",  267_1416),
    "Heartless Neoshadow":                                               KHCOMLocationData("Progression",  267_1417),
    "Heartless Pirate":                                                  KHCOMLocationData("Progression",  267_1418),
    "Heartless Powerwild":                                               KHCOMLocationData("Progression",  267_1419),
    "Heartless Red Nocturne":                                            KHCOMLocationData("Progression",  267_1420),
    "Heartless Screwdiver":                                              KHCOMLocationData("Progression",  267_1421),
    "Heartless Sea Neon":                                                KHCOMLocationData("Progression",  267_1422),
    "Heartless Search Ghost":                                            KHCOMLocationData("Progression",  267_1423),
    "Heartless Shadow":                                                  KHCOMLocationData("Progression",  267_1424),
    "Heartless Soldier":                                                 KHCOMLocationData("Progression",  267_1425),
    "Heartless Tornado Step":                                            KHCOMLocationData("Progression",  267_1426),
    "Heartless White Mushroom":                                          KHCOMLocationData("Progression",  267_1427),
    "Heartless Wight Knight":                                            KHCOMLocationData("Progression",  267_1428),
    "Heartless Wizard":                                                  KHCOMLocationData("Progression",  267_1429),
    "Heartless Wyvern":                                                  KHCOMLocationData("Progression",  267_1430),
    "Heartless Yellow Opera":                                            KHCOMLocationData("Progression",  267_1431),
}

event_location_table: Dict[str, KHCOMLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}