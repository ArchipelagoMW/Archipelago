from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class KHCOMItem(Item):
    game: str = "Kingdom Hearts Chain of Memories"


class KHCOMItemData(NamedTuple):
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1


def get_items_by_category(category: str) -> Dict[str, KHCOMItemData]:
    item_dict: Dict[str, KHCOMItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict


item_table: Dict[str, KHCOMItemData] = {
    #Battle Cards
    "Bronze Card Pack":                 KHCOMItemData("Filler",             266_1001, ItemClassification.filler, weight=500),
    "Silver Card Pack":                 KHCOMItemData("Filler",             266_1002, ItemClassification.filler, weight=300),
    "Gold Card Pack":                   KHCOMItemData("Filler",             266_1003, ItemClassification.filler, weight=100),
    
    #Enemy Battle Cards
    "Enemy Card Shadow":                KHCOMItemData("Filler",             266_2001, ItemClassification.filler, weight=5),
    "Enemy Card Soldier":               KHCOMItemData("Filler",             266_2002, ItemClassification.filler, weight=5),
    "Enemy Card Large Body":            KHCOMItemData("Filler",             266_2003, ItemClassification.filler, weight=5),
    "Enemy Card Red Nocturne":          KHCOMItemData("Filler",             266_2004, ItemClassification.filler, weight=5),
    "Enemy Card Blue Rhapsody":         KHCOMItemData("Filler",             266_2005, ItemClassification.filler, weight=5),
    "Enemy Card Yellow Opera":          KHCOMItemData("Filler",             266_2006, ItemClassification.filler, weight=5),
    "Enemy Card Green Requiem":         KHCOMItemData("Filler",             266_2007, ItemClassification.filler, weight=5),
    "Enemy Card Powerwild":             KHCOMItemData("Filler",             266_2008, ItemClassification.filler, weight=5),
    "Enemy Card Bouncywild":            KHCOMItemData("Filler",             266_2009, ItemClassification.filler, weight=5),
    "Enemy Card Air Soldier":           KHCOMItemData("Filler",             266_2010, ItemClassification.filler, weight=5),
    "Enemy Card Bandit":                KHCOMItemData("Filler",             266_2011, ItemClassification.filler, weight=5),
    "Enemy Card Fat Bandit":            KHCOMItemData("Filler",             266_2012, ItemClassification.filler, weight=5),
    "Enemy Card Barrel Spider":         KHCOMItemData("Filler",             266_2013, ItemClassification.filler, weight=5),
    "Enemy Card Search Ghost":          KHCOMItemData("Filler",             266_2014, ItemClassification.filler, weight=5),
    "Enemy Card Sea Neon":              KHCOMItemData("Filler",             266_2015, ItemClassification.filler, weight=5),
    "Enemy Card Screwdriver":           KHCOMItemData("Filler",             266_2016, ItemClassification.filler, weight=5),
    "Enemy Card Aquatank":              KHCOMItemData("Filler",             266_2017, ItemClassification.filler, weight=5),
    "Enemy Card Wight Knight":          KHCOMItemData("Filler",             266_2018, ItemClassification.filler, weight=5),
    "Enemy Card Gargoyle":              KHCOMItemData("Filler",             266_2019, ItemClassification.filler, weight=5),
    "Enemy Card Pirate":                KHCOMItemData("Filler",             266_2020, ItemClassification.filler, weight=5),
    "Enemy Card Air Pirate":            KHCOMItemData("Filler",             266_2021, ItemClassification.filler, weight=5),
    "Enemy Card Darkball":              KHCOMItemData("Filler",             266_2022, ItemClassification.filler, weight=5),
    "Enemy Card Defender":              KHCOMItemData("Filler",             266_2023, ItemClassification.filler, weight=5),
    "Enemy Card Wyvern":                KHCOMItemData("Filler",             266_2024, ItemClassification.filler, weight=5),
    "Enemy Card Neoshadow":             KHCOMItemData("Filler",             266_2025, ItemClassification.filler, weight=5),
    "Enemy Card White Mushroom":        KHCOMItemData("Filler",             266_2026, ItemClassification.filler, weight=5),
    "Enemy Card Black Fungus":          KHCOMItemData("Filler",             266_2027, ItemClassification.filler, weight=5),
    "Enemy Card Creeper Plant":         KHCOMItemData("Filler",             266_2028, ItemClassification.filler, weight=5),
    "Enemy Card Tornado Step":          KHCOMItemData("Filler",             266_2029, ItemClassification.filler, weight=5),
    "Enemy Card Crescendo":             KHCOMItemData("Filler",             266_2030, ItemClassification.filler, weight=5),
    "Enemy Card Guard Armor":           KHCOMItemData("Filler",             266_2031, ItemClassification.filler, weight=5),
    "Enemy Card Parasite Cage":         KHCOMItemData("Filler",             266_2032, ItemClassification.filler, weight=5),
    "Enemy Card Trickmaster":           KHCOMItemData("Filler",             266_2033, ItemClassification.filler, weight=5),
    "Enemy Card Darkside":              KHCOMItemData("Filler",             266_2034, ItemClassification.filler, weight=5),
    "Enemy Card Card Soldier (Red)":    KHCOMItemData("Filler",             266_2035, ItemClassification.filler, weight=5),
    "Enemy Card Card Soldier (Black)":  KHCOMItemData("Filler",             266_2036, ItemClassification.filler, weight=5),
    "Enemy Card Hades":                 KHCOMItemData("Filler",             266_2037, ItemClassification.filler, weight=5),
    "Enemy Card Jafar":                 KHCOMItemData("Filler",             266_2039, ItemClassification.filler, weight=5),
    "Enemy Card Oogie Boogie":          KHCOMItemData("Filler",             266_2040, ItemClassification.filler, weight=5),
    "Enemy Card Ursula":                KHCOMItemData("Filler",             266_2041, ItemClassification.filler, weight=5),
    "Enemy Card Hook":                  KHCOMItemData("Filler",             266_2042, ItemClassification.filler, weight=5),
    "Enemy Card Dragon Maleficent":     KHCOMItemData("Filler",             266_2043, ItemClassification.filler, weight=5),
    "Enemy Card Riku":                  KHCOMItemData("Filler",             266_2044, ItemClassification.filler, weight=5),
    "Enemy Card Axel":                  KHCOMItemData("Filler",             266_2044, ItemClassification.filler, weight=5),
    "Enemy Card Larxene":               KHCOMItemData("Filler",             266_2045, ItemClassification.filler, weight=5),
    "Enemy Card Vexen":                 KHCOMItemData("Filler",             266_2046, ItemClassification.filler, weight=5),
    "Enemy Card Marluxia":              KHCOMItemData("Filler",             266_2047, ItemClassification.filler, weight=5),
    "Enemy Card Lexaeus":               KHCOMItemData("Filler",             266_2048, ItemClassification.filler, weight=5),
    "Enemy Card Ansem":                 KHCOMItemData("Filler",             266_2049, ItemClassification.filler, weight=5),
    
    #Gold Map Cards
   #"Key of Beginnings F01":            KHCOMItemData("Gold Map Cards",     266_3001, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F02":            KHCOMItemData("Gold Map Cards",     266_3002, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F03":            KHCOMItemData("Gold Map Cards",     266_3003, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F04":            KHCOMItemData("Gold Map Cards",     266_3004, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F05":            KHCOMItemData("Gold Map Cards",     266_3005, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F06":            KHCOMItemData("Gold Map Cards",     266_3006, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F07":            KHCOMItemData("Gold Map Cards",     266_3007, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F08":            KHCOMItemData("Gold Map Cards",     266_3008, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F09":            KHCOMItemData("Gold Map Cards",     266_3009, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F10":            KHCOMItemData("Gold Map Cards",     266_3010, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F11":            KHCOMItemData("Gold Map Cards",     266_3011, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F12":            KHCOMItemData("Gold Map Cards",     266_3012, ItemClassification.progression, 1,  1),
   #"Key of Beginnings F13":            KHCOMItemData("Gold Map Cards",     266_3013, ItemClassification.progression, 1,  1),
   #"Key of Guidance F01":              KHCOMItemData("Gold Map Cards",     266_3101, ItemClassification.progression, 1,  1),
   #"Key of Guidance F02":              KHCOMItemData("Gold Map Cards",     266_3102, ItemClassification.progression, 1,  1),
   #"Key of Guidance F03":              KHCOMItemData("Gold Map Cards",     266_3103, ItemClassification.progression, 1,  1),
   #"Key of Guidance F04":              KHCOMItemData("Gold Map Cards",     266_3104, ItemClassification.progression, 1,  1),
   #"Key of Guidance F05":              KHCOMItemData("Gold Map Cards",     266_3105, ItemClassification.progression, 1,  1),
   #"Key of Guidance F06":              KHCOMItemData("Gold Map Cards",     266_3106, ItemClassification.progression, 1,  1),
   #"Key of Guidance F07":              KHCOMItemData("Gold Map Cards",     266_3107, ItemClassification.progression, 1,  1),
   #"Key of Guidance F08":              KHCOMItemData("Gold Map Cards",     266_3108, ItemClassification.progression, 1,  1),
   #"Key of Guidance F09":              KHCOMItemData("Gold Map Cards",     266_3109, ItemClassification.progression, 1,  1),
   #"Key of Guidance F12":              KHCOMItemData("Gold Map Cards",     266_3112, ItemClassification.progression, 1,  1),
   #"Key to Truth F01":                 KHCOMItemData("Gold Map Cards",     266_3201, ItemClassification.progression, 1,  1),
   #"Key to Truth F02":                 KHCOMItemData("Gold Map Cards",     266_3202, ItemClassification.progression, 1,  1),
   #"Key to Truth F03":                 KHCOMItemData("Gold Map Cards",     266_3203, ItemClassification.progression, 1,  1),
   #"Key to Truth F04":                 KHCOMItemData("Gold Map Cards",     266_3204, ItemClassification.progression, 1,  1),
   #"Key to Truth F05":                 KHCOMItemData("Gold Map Cards",     266_3205, ItemClassification.progression, 1,  1),
   #"Key to Truth F06":                 KHCOMItemData("Gold Map Cards",     266_3206, ItemClassification.progression, 1,  1),
   #"Key to Truth F07":                 KHCOMItemData("Gold Map Cards",     266_3207, ItemClassification.progression, 1,  1),
   #"Key to Truth F08":                 KHCOMItemData("Gold Map Cards",     266_3208, ItemClassification.progression, 1,  1),
   #"Key to Truth F09":                 KHCOMItemData("Gold Map Cards",     266_3209, ItemClassification.progression, 1,  1),
    "Wonderland":                       KHCOMItemData("World Unlocks" ,     266_3002, ItemClassification.progression, 1,  1),
    "Olympus Coliseum":                 KHCOMItemData("World Unlocks" ,     266_3003, ItemClassification.progression, 1,  1),
    "Monstro":                          KHCOMItemData("World Unlocks" ,     266_3004, ItemClassification.progression, 1,  1),
    "Agrabah":                          KHCOMItemData("World Unlocks" ,     266_3005, ItemClassification.progression, 1,  1),
    "Halloween Town":                   KHCOMItemData("World Unlocks" ,     266_3006, ItemClassification.progression, 1,  1),
    "Atlantica":                        KHCOMItemData("World Unlocks" ,     266_3007, ItemClassification.progression, 1,  1),
    "Neverland":                        KHCOMItemData("World Unlocks" ,     266_3008, ItemClassification.progression, 1,  1),
    "Hollow Bastion":                   KHCOMItemData("World Unlocks" ,     266_3009, ItemClassification.progression, 1,  1),
    "100 Acre Wood":                    KHCOMItemData("World Unlocks" ,     266_3010, ItemClassification.progression, 1,  1),
    "Twilight Town":                    KHCOMItemData("World Unlocks" ,     266_3011, ItemClassification.progression, 1,  1),
    "Destiny Islands":                  KHCOMItemData("World Unlocks" ,     266_3012, ItemClassification.progression, 1,  1),
    "Castle Oblivion":                  KHCOMItemData("World Unlocks" ,     266_3013, ItemClassification.progression, 1,  1),
    "Key to Rewards F01":               KHCOMItemData("Gold Map Cards",     266_3301, ItemClassification.progression, 1,  1),
    "Key to Rewards F02":               KHCOMItemData("Gold Map Cards",     266_3302, ItemClassification.useful,      1,  1),
    "Key to Rewards F03":               KHCOMItemData("Gold Map Cards",     266_3303, ItemClassification.progression, 1,  1),
    "Key to Rewards F04":               KHCOMItemData("Gold Map Cards",     266_3304, ItemClassification.useful,      1,  1),
    "Key to Rewards F05":               KHCOMItemData("Gold Map Cards",     266_3305, ItemClassification.useful,      1,  1),
    "Key to Rewards F06":               KHCOMItemData("Gold Map Cards",     266_3306, ItemClassification.useful,      1,  1),
    "Key to Rewards F07":               KHCOMItemData("Gold Map Cards",     266_3307, ItemClassification.useful,      1,  1),
    "Key to Rewards F08":               KHCOMItemData("Gold Map Cards",     266_3308, ItemClassification.useful,      1,  1),
    "Key to Rewards F09":               KHCOMItemData("Gold Map Cards",     266_3309, ItemClassification.progression, 1,  1),
    "Key to Rewards F11":               KHCOMItemData("Gold Map Cards",     266_3311, ItemClassification.useful,      1,  1),
    "Key to Rewards F12":               KHCOMItemData("Gold Map Cards",     266_3312, ItemClassification.progression, 1,  1),
    "Key to Rewards F13":               KHCOMItemData("Gold Map Cards",     266_3313, ItemClassification.useful,      1,  1),

    #World Unlocks
    #"Wonderland":                      KHCOMItemData("World Cards",        266_4001, ItemClassification.progression, 1,  1),
    #"Olympus Coliseum":                KHCOMItemData("World Cards",        266_4002, ItemClassification.progression, 1,  1),
    #"Monstro":                         KHCOMItemData("World Cards",        266_4003, ItemClassification.progression, 1,  1),
    #"Agrabah":                         KHCOMItemData("World Cards",        266_4004, ItemClassification.progression, 1,  1),
    #"Halloween Town":                  KHCOMItemData("World Cards",        266_4005, ItemClassification.progression, 1,  1),
    #"Atlantica":                       KHCOMItemData("World Cards",        266_4006, ItemClassification.progression, 1,  1),
    #"Neverland":                       KHCOMItemData("World Cards",        266_4007, ItemClassification.progression, 1,  1),
    #"Hollow Bastion":                  KHCOMItemData("World Cards",        266_4008, ItemClassification.progression, 1,  1),
    #"100 Acre Wood":                   KHCOMItemData("World Cards",        266_4009, ItemClassification.progression, 1,  1),
    #"Twilight Town":                   KHCOMItemData("World Cards",        266_4010, ItemClassification.progression, 1,  1),
    #"Destiny Islands":                 KHCOMItemData("World Cards",        266_4011, ItemClassification.progression, 1,  1),
    #"Castle Oblivion":                 KHCOMItemData("World Cards",        266_4012, ItemClassification.progression, 1,  1),

    #Friend Cards
    "Donald":                           KHCOMItemData("Friend Cards",       266_5001, ItemClassification.progression, 1,  1),
    "Goofy":                            KHCOMItemData("Friend Cards",       266_5002, ItemClassification.progression, 1,  1),
    "Aladdin":                          KHCOMItemData("Friend Cards",       266_5003, ItemClassification.progression, 1,  1),
    "Ariel":                            KHCOMItemData("Friend Cards",       266_5004, ItemClassification.progression, 1,  1),
    "Beast":                            KHCOMItemData("Friend Cards",       266_5005, ItemClassification.progression, 1,  1),
    "Peter Pan":                        KHCOMItemData("Friend Cards",       266_5006, ItemClassification.progression, 1,  1),
    "Jack":                             KHCOMItemData("Friend Cards",       266_5007, ItemClassification.progression, 1,  1),
}

event_item_table: Dict[str, KHCOMItemData] = {
}
