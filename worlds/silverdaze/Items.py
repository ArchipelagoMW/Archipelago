#Sawyer: We're gonna start by basing this off the RogueLegacy Items.py.
from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification
#Sawyer: I don't know what those above things do yet, but I think they're universal.

class SDItem(Item):
    game: str = "Silver Daze"


class SDItemData(NamedTuple):
#STR is String and INT is Integer, I think?
    category: str
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.useful
    max_quantity: int = 1
    weight: int = 1


def get_items_by_category(category: str) -> Dict[str, SDItemData]:
    item_dict: Dict[str, SDItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict


item_table: Dict[str, SDItemData] = {
    #Party Members
        "Pinn"                  SDItemData("Party",         3001,       ItemClassification.progression),
        "Geo"                   SDItemData("Party",         3002,       ItemClassification.progression),
        "Kani"                  SDItemData("Party",         3003,       ItemClassification.progression),
    #Cards
        "Ultima"                SDItemData("Card",          352),
        "Finish Touch"          SDItemData("Card",          42),
        "Valor Drive"           SDItemData("Card",          25),
        "Sonic Boom"            SDItemData("Card",          29),
        "Hopscotch"             SDItemData("Card",          154),
        "CoffeBrek"             SDItemData("Card",          155),
        "Fine Tune"             SDItemData("Card",          256),
        "SmokeBreak"            SDItemData("Card",          311),
        "PowerNap"              SDItemData("Card",          72),
        "Flatten"               SDItemData("Card",          18),
        "Dragon"                SDItemData("Card",          31),
        "Variacut"              SDItemData("Card",          30),
        "Morning Ray"           SDItemData("Card",          7),
        "Zoner"                 SDItemData("Card",          304),
        "Cold As Ice"           SDItemData("Card",          5),
        "Strife"                SDItemData("Card",          6,          ItemClassification.useful,          2),
        "RATD"                  SDItemData("Card",          4),
    #MP3s   
        "Freddie Freeloader"    SDItemData("MP3",           1063),
        "Flossophy"             SDItemData("MP3",           1044),
        "Big Shot"              SDItemData("MP3",           1003),
        "Triage"                SDItemData("MP3",           1065),
        "The Sign"              SDItemData("MP3",           1045),
        "Wet Hands"             SDItemData("MP3",           1010),
        "Move"                  SDItemData("MP3",           1001),
        "Low Ride"              SDItemData("MP3",           1042),
        "Lost In Thought"       SDItemData("MP3",           1062),
    #Keys   
        "Yellow Key"            SDItemData("Key",           2010,       ItemClassification.progression),
        "Red Key"               SDItemData("Key",           2014,       ItemClassification.progression),
    #Events
    
    #Consumables
        "Heal Token"            SDItemData("Consumable",    2002,       ItemClassification.filler,           5),
        "Hi-Heal Token"         SDItemData("Consumable",    2004,       ItemClassification.filler),
        "Evade Token"           SDItemData("Consumable",    2003,       ItemClassification.filler),
        "Sneak Token"           SDItemData("Consumable",    2003,       ItemClassification.filler),
    #Other (Probably Filler)
    
}
