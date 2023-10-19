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
    #Battle Cards Progression
    "Kingdom Key":           KHCOMLocationData("Progression", 267_1001),
    "Three Wishes":          KHCOMLocationData("Progression", 267_1002),
    "Crabclaw":              KHCOMLocationData("Progression", 267_1003),
    "Pumpkinhead":           KHCOMLocationData("Progression", 267_1004),
    "Fairy Harp":            KHCOMLocationData("Progression", 267_1005),
    "Wishing Star":          KHCOMLocationData("Progression", 267_1006),
    "Spellbinder":           KHCOMLocationData("Progression", 267_1007),
    "Metal Chocobo":         KHCOMLocationData("Progression", 267_1008),
    "Olympia":               KHCOMLocationData("Progression", 267_1009),
    "Lionheart":             KHCOMLocationData("Progression", 267_1010),
    "Lady Luck":             KHCOMLocationData("Progression", 267_1011),
    "Divine Rose":           KHCOMLocationData("Progression", 267_1012),
    "Oathkeeper":            KHCOMLocationData("Progression", 267_1013),
    "Oblivion":              KHCOMLocationData("Progression", 267_1014),
    "Diamond Dust":          KHCOMLocationData("Progression", 267_1015),
    "One Winged Angel":      KHCOMLocationData("Progression", 267_1016),
    "Fire":                  KHCOMLocationData("Progression", 267_1017),
    "Blizzard":              KHCOMLocationData("Progression", 267_1018),
    "Thunder":               KHCOMLocationData("Progression", 267_1019),
    "Cure":                  KHCOMLocationData("Progression", 267_1020),
    "Gravity":               KHCOMLocationData("Progression", 267_1021),
    "Stop":                  KHCOMLocationData("Progression", 267_1022),
    "Aero":                  KHCOMLocationData("Progression", 267_1023),
    "Simba":                 KHCOMLocationData("Progression", 267_1024),
    "Genie":                 KHCOMLocationData("Progression", 267_1025),
    "Bambi":                 KHCOMLocationData("Progression", 267_1026),
    "Dumbo":                 KHCOMLocationData("Progression", 267_1027),
    "Tinker Bell":           KHCOMLocationData("Progression", 267_1028),
    "Mushu":                 KHCOMLocationData("Progression", 267_1029),
    "Cloud":                 KHCOMLocationData("Progression", 267_1030),
    "Potion":                KHCOMLocationData("Progression", 267_1031),
    "Hi-Potion":             KHCOMLocationData("Progression", 267_1032),
    "Mega-Potion":           KHCOMLocationData("Progression", 267_1033),
    "Ether":                 KHCOMLocationData("Progression", 267_1034),
    "Mega-Ether":            KHCOMLocationData("Progression", 267_1035),
    "Elxir":                 KHCOMLocationData("Progression", 267_1036),
    "Megalixir":             KHCOMLocationData("Progression", 267_1037),
    "Guard Armor":           KHCOMLocationData("Progression", 267_1038),
    "Parasite Cage":         KHCOMLocationData("Progression", 267_1039),
    "Trickmaster":           KHCOMLocationData("Progression", 267_1040),
    "Darkside":              KHCOMLocationData("Progression", 267_1041),
    "Card Soldier (Red)":    KHCOMLocationData("Progression", 267_1042),
    "Hades":                 KHCOMLocationData("Progression", 267_1043),
    "Jafar":                 KHCOMLocationData("Progression", 267_1044),
    "Oogie Boogie":          KHCOMLocationData("Progression", 267_1045),
    "Ursula":                KHCOMLocationData("Progression", 267_1046),
    "Hook":                  KHCOMLocationData("Progression", 267_1047),
    "Dragon Maleficent":     KHCOMLocationData("Progression", 267_1048),
    "Riku":                  KHCOMLocationData("Progression", 267_1049),
    "Axel":                  KHCOMLocationData("Progression", 267_1050),
    "Larxene":               KHCOMLocationData("Progression", 267_1051),
    "Vexen":                 KHCOMLocationData("Progression", 267_1052),
    "Marluxia":              KHCOMLocationData("Progression", 267_1053),
    
    #Enemy Unlock
    "Shadow":                KHCOMLocationData("Enemy Unlock", 267_2001),
    "Soldier":               KHCOMLocationData("Enemy Unlock", 267_2002),
    "Large Body":            KHCOMLocationData("Enemy Unlock", 267_2003),
    "Red Nocturne":          KHCOMLocationData("Enemy Unlock", 267_2004),
    "Blue Rhapsody":         KHCOMLocationData("Enemy Unlock", 267_2005),
    "Yellow Opera":          KHCOMLocationData("Enemy Unlock", 267_2006),
    "Green Requiem":         KHCOMLocationData("Enemy Unlock", 267_2007),
    "Powerwild":             KHCOMLocationData("Enemy Unlock", 267_2008),
    "Bouncywild":            KHCOMLocationData("Enemy Unlock", 267_2009),
    "Air Soldier":           KHCOMLocationData("Enemy Unlock", 267_2010),
    "Bandit":                KHCOMLocationData("Enemy Unlock", 267_2011),
    "Fat Bandit":            KHCOMLocationData("Enemy Unlock", 267_2012),
    "Barrel Spider":         KHCOMLocationData("Enemy Unlock", 267_2013),
    "Search Ghost":          KHCOMLocationData("Enemy Unlock", 267_2014),
    "Sea Neon":              KHCOMLocationData("Enemy Unlock", 267_2015),
    "Screwdriver":           KHCOMLocationData("Enemy Unlock", 267_2016),
    "Aquatank":              KHCOMLocationData("Enemy Unlock", 267_2017),
    "Wight Knight":          KHCOMLocationData("Enemy Unlock", 267_2018),
    "Gargoyle":              KHCOMLocationData("Enemy Unlock", 267_2019),
    "Pirate":                KHCOMLocationData("Enemy Unlock", 267_2020),
    "Air Pirate":            KHCOMLocationData("Enemy Unlock", 267_2021),
    "Darkball":              KHCOMLocationData("Enemy Unlock", 267_2022),
    "Defender":              KHCOMLocationData("Enemy Unlock", 267_2023),
    "Wyvern":                KHCOMLocationData("Enemy Unlock", 267_2024),
    "Neoshadow":             KHCOMLocationData("Enemy Unlock", 267_2025),
    "White Mushroom":        KHCOMLocationData("Enemy Unlock", 267_2026),
    "Black Fungus":          KHCOMLocationData("Enemy Unlock", 267_2027),
    "Creeper Plant":         KHCOMLocationData("Enemy Unlock", 267_2028),
    "Tornado Step":          KHCOMLocationData("Enemy Unlock", 267_2029),
    "Crescendo":             KHCOMLocationData("Enemy Unlock", 267_2030),
    "Card Soldier (Black)":  KHCOMLocationData("Enemy Unlock", 267_2036),
    
    #Gold Map Cards Progression
    "Key of Beginnings F01": KHCOMLocationData("Progression", 267_4001),
    "Key of Beginnings F02": KHCOMLocationData("Progression", 267_4002),
    "Key of Beginnings F03": KHCOMLocationData("Progression", 267_4003),
    "Key of Beginnings F04": KHCOMLocationData("Progression", 267_4004),
    "Key of Beginnings F05": KHCOMLocationData("Progression", 267_4005),
    "Key of Beginnings F06": KHCOMLocationData("Progression", 267_4006),
    "Key of Beginnings F07": KHCOMLocationData("Progression", 267_4007),
    "Key of Beginnings F08": KHCOMLocationData("Progression", 267_4008),
    "Key of Beginnings F09": KHCOMLocationData("Progression", 267_4009),
    "Key of Beginnings F11": KHCOMLocationData("Progression", 267_4011),
    "Key of Beginnings F12": KHCOMLocationData("Progression", 267_4012),
    "Key of Beginnings F13": KHCOMLocationData("Progression", 267_4013),
    "Key of Guidance F01":   KHCOMLocationData("Progression", 267_4101),
    "Key of Guidance F02":   KHCOMLocationData("Progression", 267_4102),
    "Key of Guidance F03":   KHCOMLocationData("Progression", 267_4103),
    "Key of Guidance F04":   KHCOMLocationData("Progression", 267_4104),
    "Key of Guidance F05":   KHCOMLocationData("Progression", 267_4105),
    "Key of Guidance F06":   KHCOMLocationData("Progression", 267_4106),
    "Key of Guidance F07":   KHCOMLocationData("Progression", 267_4107),
    "Key of Guidance F08":   KHCOMLocationData("Progression", 267_4108),
    "Key of Guidance F09":   KHCOMLocationData("Progression", 267_4109),
    "Key of Guidance F12":   KHCOMLocationData("Progression", 267_4112),
    "Key to Truth F01":      KHCOMLocationData("Progression", 267_4201),
    "Key to Truth F02":      KHCOMLocationData("Progression", 267_4202),
    "Key to Truth F03":      KHCOMLocationData("Progression", 267_4203),
    "Key to Truth F04":      KHCOMLocationData("Progression", 267_4204),
    "Key to Truth F05":      KHCOMLocationData("Progression", 267_4205),
    "Key to Truth F06":      KHCOMLocationData("Progression", 267_4206),
    "Key to Truth F07":      KHCOMLocationData("Progression", 267_4207),
    "Key to Truth F08":      KHCOMLocationData("Progression", 267_4208),
    "Key to Truth F09":      KHCOMLocationData("Progression", 267_4209),
}

event_location_table: Dict[str, KHCOMLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}