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

    "F01 Traverse Town Entrance":                           KHCOMLocationData("Progression",  267_0101),
    "F01 Traverse Town Field (Black Fungus)":               KHCOMLocationData("Enemy Unlock", 267_0102),
    "F01 Traverse Town Field (Blizzard)":                   KHCOMLocationData("Progression",  267_0103),
    "F01 Traverse Town Field (Blue Rhapsody)":              KHCOMLocationData("Enemy Unlock", 267_0104),
    "F01 Traverse Town Field (Cure)":                       KHCOMLocationData("Progression",  267_0105),
    "F01 Traverse Town Field (Kingdom Key)":                KHCOMLocationData("Progression",  267_0106),
    "F01 Traverse Town Field (Potion)":                     KHCOMLocationData("Progression",  267_0107),
    "F01 Traverse Town Field (Red Nocturne)":               KHCOMLocationData("Enemy Unlock", 267_0108),
    "F01 Traverse Town Field (Shadow)":                     KHCOMLocationData("Enemy Unlock", 267_0109),
    "F01 Traverse Town Field (Soldier)":                    KHCOMLocationData("Enemy Unlock", 267_0110),
    "F01 Traverse Town Field (White Mushroom)":             KHCOMLocationData("Enemy Unlock", 267_0111),
    "F01 Traverse Town Post Floor (Fire)":                  KHCOMLocationData("Boss",         267_0112),
    "F01 Traverse Town Room of Beginnings":                 KHCOMLocationData("Progression",  267_0113),
    "F01 Traverse Town Room of Beginnings (Simba)":         KHCOMLocationData("Boss",         267_0114),
    "F01 Traverse Town Room of Guidance":                   KHCOMLocationData("Progression",  267_0115),
    "F01 Traverse Town Room of Rewards (Lionheart)":        KHCOMLocationData("Progression",  267_0116),
    "F01 Traverse Town Room of Truth (Guard Armor)":        KHCOMLocationData("Boss",         267_0117),
    
    "F02 Wonderland Bounty (Stop)":                         KHCOMLocationData("Progression",  267_0201),
    "F02 Wonderland Entrance":                              KHCOMLocationData("Progression",  267_0202),
    "F02 Wonderland Field (Card Soldier Black)":            KHCOMLocationData("Enemy Unlock", 267_0203),
    "F02 Wonderland Field (Creeper Plant)":                 KHCOMLocationData("Enemy Unlock", 267_0204),
    "F02 Wonderland Field (Crescendo)":                     KHCOMLocationData("Enemy Unlock", 267_0205),
    "F02 Wonderland Field (Large Body)":                    KHCOMLocationData("Enemy Unlock", 267_0206),
    "F02 Wonderland Field (Lady Luck)":                     KHCOMLocationData("Progression",  267_0207),
    "F02 Wonderland Room of Beginnings":                    KHCOMLocationData("Progression",  267_0208),
    "F02 Wonderland Room of Beginnings (Card Soldier Red)": KHCOMLocationData("Boss",         267_0209),
    "F02 Wonderland Room of Guidance":                      KHCOMLocationData("Progression",  267_0210),
    "F02 Wonderland Room of Truth (Trickmaster)":           KHCOMLocationData("Boss",         267_0211),
    
    "F03 Olympus Coliseum Entrance":                        KHCOMLocationData("Progression",  267_0301),
    "F03 Olympus Coliseum Field (Barrel Spider)":           KHCOMLocationData("Enemy Unlock", 267_0302),
    "F03 Olympus Coliseum Field (Bouncywild)":              KHCOMLocationData("Enemy Unlock", 267_0303),
    "F03 Olympus Coliseum Field (Olympia)":                 KHCOMLocationData("Progression",  267_0304),
    "F03 Olympus Coliseum Field (Powerwild)":               KHCOMLocationData("Enemy Unlock", 267_0305),
    "F03 Olympus Coliseum Room of Beginnings":              KHCOMLocationData("Progression",  267_0306),
    "F03 Olympus Coliseum Room of Guidance":                KHCOMLocationData("Progression",  267_0307),
    "F03 Olympus Coliseum Room of Guidance (Hi-Potion)":    KHCOMLocationData("Boss",         267_0308),
    "F03 Olympus Coliseum Room of Rewards (Metal Chocobo)": KHCOMLocationData("Progression",  267_0309),
    "F03 Olympus Coliseum Room of Truth (Cloud)":           KHCOMLocationData("Boss",         267_0310),
    "F03 Olympus Coliseum Room of Truth (Hades)":           KHCOMLocationData("Boss",         267_0311),
    
    "F04 Monstro Entrance":                                 KHCOMLocationData("Progression",  267_0401),
    "F04 Monstro Field (Air Soldier)":                      KHCOMLocationData("Enemy Unlock", 267_0402),
    "F04 Monstro Field (Green Requiem)":                    KHCOMLocationData("Enemy Unlock", 267_0403),
    "F04 Monstro Field (Search Ghost)":                     KHCOMLocationData("Enemy Unlock", 267_0404),
    "F04 Monstro Field (Tornado Step)":                     KHCOMLocationData("Enemy Unlock", 267_0405),
    "F04 Monstro Field (Wishing Star)":                     KHCOMLocationData("Progression",  267_0406),
    "F04 Monstro Field (Yellow Opera)":                     KHCOMLocationData("Enemy Unlock", 267_0407),
    "F04 Monstro Room of Beginnings":                       KHCOMLocationData("Progression",  267_0408),
    "F04 Monstro Room of Guidance":                         KHCOMLocationData("Progression",  267_0409),
    "F04 Monstro Room of Guidance (Parasite Cage)":         KHCOMLocationData("Boss",         267_0410),
    "F04 Monstro Room of Truth (Dumbo)":                    KHCOMLocationData("Boss",         267_0411),
    
    "F05 Agrabah Bounty (Gravity)":                         KHCOMLocationData("Progression",  267_0501),
    "F05 Agrabah Entrance":                                 KHCOMLocationData("Progression",  267_0502),
    "F05 Agrabah Field (Bandit)":                           KHCOMLocationData("Enemy Unlock", 267_0503),
    "F05 Agrabah Field (Fat Bandit)":                       KHCOMLocationData("Enemy Unlock", 267_0504),
    "F05 Agrabah Field (Three Wishes)":                     KHCOMLocationData("Progression",  267_0505),
    "F05 Agrabah Room of Beginnings":                       KHCOMLocationData("Progression",  267_0506),
    "F05 Agrabah Room of Guidance":                         KHCOMLocationData("Progression",  267_0507),
    "F05 Agrabah Room of Guidance (Ether)":                 KHCOMLocationData("Boss",         267_0508),
    "F05 Agrabah Room of Truth (Genie)":                    KHCOMLocationData("Boss",         267_0509),
    "F05 Agrabah Room of Truth (Jafar)":                    KHCOMLocationData("Boss",         267_0510),
    
    "F06 Halloween Town Entrance":                          KHCOMLocationData("Progression",  267_0601),
    "F06 Halloween Town Field (Gargoyle)":                  KHCOMLocationData("Enemy Unlock", 267_0602),
    "F06 Halloween Town Field (Pumpkinhead)":               KHCOMLocationData("Progression",  267_0603),
    "F06 Halloween Town Field (Wight Knight)":              KHCOMLocationData("Enemy Unlock", 267_0604),
    "F06 Halloween Town Post Floor (Thunder)":              KHCOMLocationData("Boss",         267_0605),
    "F06 Halloween Town Room of Beginnings":                KHCOMLocationData("Progression",  267_0606),
    "F06 Halloween Town Room of Guidance":                  KHCOMLocationData("Progression",  267_0607),
    "F06 Halloween Town Room of Truth (Oogie Boogie)":      KHCOMLocationData("Boss",         267_0608),
    
    "F07 Atlantica Entrance":                               KHCOMLocationData("Progression",  267_0701),
    "F07 Atlantica Field (Aquatank)":                       KHCOMLocationData("Enemy Unlock", 267_0702),
    "F07 Atlantica Field (Crabclaw)":                       KHCOMLocationData("Progression",  267_0703),
    "F07 Atlantica Field (Darkball)":                       KHCOMLocationData("Enemy Unlock", 267_0704),
    "F07 Atlantica Field (Screwdriver)":                    KHCOMLocationData("Enemy Unlock", 267_0705),
    "F07 Atlantica Field (Sea Neon)":                       KHCOMLocationData("Enemy Unlock", 267_0706),
    "F07 Atlantica Post Floor (Aero)":                      KHCOMLocationData("Progression",  267_0707),
    "F07 Atlantica Room of Beginnings":                     KHCOMLocationData("Progression",  267_0708),
    "F07 Atlantica Room of Guidance":                       KHCOMLocationData("Progression",  267_0709),
    "F07 Atlantica Room of Truth (Ursula)":                 KHCOMLocationData("Boss",         267_0710),
    
    "F08 Neverland Entrance":                               KHCOMLocationData("Progression",  267_0801),
    "F08 Neverland Field (Air Pirate)":                     KHCOMLocationData("Enemy Unlock", 267_0802),
    "F08 Neverland Field (Fairy Harp)":                     KHCOMLocationData("Progression",  267_0803),
    "F08 Neverland Field (Pirate)":                         KHCOMLocationData("Enemy Unlock", 267_0804),
    "F08 Neverland Room of Beginnings":                     KHCOMLocationData("Progression",  267_0805),
    "F08 Neverland Room of Guidance":                       KHCOMLocationData("Progression",  267_0806),
    "F08 Neverland Room of Truth (Hook)":                   KHCOMLocationData("Boss",         267_0807),
    "F08 Neverland Room of Truth (Tinker Bell)":            KHCOMLocationData("Boss",         267_0808),
    
    "F09 Hollow Bastion Entrance":                          KHCOMLocationData("Progression",  267_0901),
    "F09 Hollow Bastion Field (Defender)":                  KHCOMLocationData("Enemy Unlock", 267_0902),
    "F09 Hollow Bastion Field (Divine Rose)":               KHCOMLocationData("Progression",  267_0903),
    "F09 Hollow Bastion Field (Wizard)":                    KHCOMLocationData("Enemy Unlock", 267_0904),
    "F09 Hollow Bastion Field (Wyvern)":                    KHCOMLocationData("Enemy Unlock", 267_0905),
    "F09 Hollow Bastion Room of Beginnings":                KHCOMLocationData("Progression",  267_0906),
    "F09 Hollow Bastion Room of Guidance":                  KHCOMLocationData("Progression",  267_0907),
    "F09 Hollow Bastion Room of Rewards (Mushu)":           KHCOMLocationData("Progression",  267_0908),
    "F09 Hollow Bastion Room of Truth (Dragon Maleficent)": KHCOMLocationData("Boss",         267_0909),
    
    "F10 100 Acre Wood Complete (Bambi)":                   KHCOMLocationData("Progression",  267_1001),
    "F10 100 Acre Wood Owl (Spellbinder)":                  KHCOMLocationData("Progression",  267_1002),
    "F10 100 Acre Wood Post Floor (Mega-Ether)":            KHCOMLocationData("Boss",         267_1003),
    "F10 100 Acre Wood Roo (Elixir)":                       KHCOMLocationData("Boss",         267_1004),
    
    "F11 Twilight Town Entrance":                           KHCOMLocationData("Progression",  267_1101),
    "F11 Twilight Town Post Floor (Mega-Potion)":           KHCOMLocationData("Boss",         267_1102),
    "F11 Twilight Town Room of Beginnings (Vexen)":         KHCOMLocationData("Boss",         267_1103),
    
    "F12 Destiny Islands Entrance":                         KHCOMLocationData("Progression",  267_1201),
    #"F12 Destiny Islands Post Floor (Larxene)":             KHCOMLocationData("Boss",         267_1202),
    "F12 Destiny Islands Post Floor (Oathkeeper)":          KHCOMLocationData("Progression",  267_1203),
    #"F12 Destiny Islands Post Floor (Oblivion)":            KHCOMLocationData("Progression",  267_1204),
    "F12 Destiny Islands Post Floor (Riku)":                KHCOMLocationData("Boss",         267_1205),
    "F12 Destiny Islands Room of Beginnings":               KHCOMLocationData("Progression",  267_1206),
    "F12 Destiny Islands Room of Guidance (Darkside)":      KHCOMLocationData("Boss",         267_1207),
    "F12 Destiny Islands Room of Rewards (Megalixir)":      KHCOMLocationData("Progression",  267_1208),
    
    "F13 Castle Oblivion Entrance":                         KHCOMLocationData("Progression",  267_1301),
    "F13 Castle Oblivion Field (Neoshadow)":                KHCOMLocationData("Enemy Unlock", 267_1302),
    "F13 Castle Oblivion Post Floor (Marluxia)":            KHCOMLocationData("Boss",         267_1303),
    "F13 Castle Oblivion Post Marluxia (Diamond Dust)":     KHCOMLocationData("Progression",  267_1304),
    "F13 Castle Oblivion Post Marluxia (One-Winged Angel)": KHCOMLocationData("Progression",  267_1305),
    "F13 Castle Oblivion Room of Beginnings (Axel)":        KHCOMLocationData("Boss",         267_1306),
}

event_location_table: Dict[str, KHCOMLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}