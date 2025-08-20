from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification

class SDItem(Item):
    game: str = "Silver Daze"

class ItemData(NamedTuple):
    code: int
    classification: ItemClassification = ItemClassification.filler
    category: str = 'Card'
    max_quantity: int = 1
    weight: int = 1

# Item groups for easy management

party_members = {
    "Pinn":                 ItemData(3001, ItemClassification.progression,  "Party"),
    "Geo":                  ItemData(3002, ItemClassification.progression,  "Party"),
    "Kani":                 ItemData(3003, ItemClassification.progression,  "Party"),
}

mp3s = {
    "Freddie Freeloader":   ItemData(1063,  ItemClassification.useful,      "MP3"),
    "Flossophy":            ItemData(1044,  ItemClassification.useful,      "MP3"),
    "Big Shot":             ItemData(1003,  ItemClassification.useful,      "MP3"),
    "Triage":               ItemData(1065,  ItemClassification.useful,      "MP3"),
    "The Sign":             ItemData(1045,  ItemClassification.useful,      "MP3"),
    "Wet Hands":            ItemData(1010,  ItemClassification.useful,      "MP3"),
    "Move":                 ItemData(1001,  ItemClassification.useful,      "MP3"),
    "Low Ride":             ItemData(1042,  ItemClassification.useful,      "MP3"),
    "Lost In Thought":      ItemData(1062,  ItemClassification.useful,      "MP3"),
}

# In Visual Studio Code or another IDE you can collapse the dict to hide the cards
cards = {
    "Ultima":               ItemData(352),
    "Finish Touch":         ItemData(42),
    "Valor Drive":          ItemData(25),
    "Sonic Boom":           ItemData(29),
    "Hopscotch":            ItemData(154),
    "CoffeBrek":            ItemData(155),
    "Fine Tune":            ItemData(256),
    "SmokeBreak":           ItemData(311),
    "PowerNap":             ItemData(72),
    "Flatten":              ItemData(18),
    "Dragon":               ItemData(31),
    "Variacut":             ItemData(30),
    "Morning Ray":          ItemData(7),
    "Zoner":                ItemData(304),
    "Cold As Ice":          ItemData(5),
    "Strife":               ItemData(6),
    "RATD":                 ItemData(4,     ItemClassification.useful,      "Card",     2),
}

keys = {
    "Yellow Key":           ItemData(2010,  ItemClassification.progression, "Key"),
    "Red Key":              ItemData(2014,  ItemClassification.progression, "Key"),
}

consumables = {
    "Heal Token":           ItemData(2002,       ItemClassification.filler, "Filler",   5),
    "Evade Token":          ItemData(2003,       ItemClassification.filler, "Filler",   1),
    "Hi-Heal Token":        ItemData(2004,       ItemClassification.filler, "Filler",   1),
    #Tent Token Here
    "Sneak Token":          ItemData(2006,       ItemClassification.filler, "Filler",   1),
}

item_table = {
    # This includes all entries in those other dicts in this one
    **party_members, 
    **cards,
    **mp3s,
    **keys,
    **consumables,
    
    #Events - Note that these are items!

    #Other Items
    #  "Sneak Token":          ItemData(2006,       ItemClassification.filler, "Filler",   1),
}

# Shorthands for rules

lookup_key_from_color = {
    "red": "Red Key",
    "orange": "Orange Key",
    "yellow": "Yellow Key",
    "green": "Green Key",
    "blue": "Blue Key",
    "purple": "Purple Key",
    "black": "Black Key"
}

def get_key_from_color(color:str) -> str:
    # Nat: This could be made to just color.lower().capitalize() then append " Key" 
    # and return, but we wanna prevent user errors in this house.
    color = color.lower()
    assert(color in lookup_key_from_color.keys()), f"Input '{color}' is not a valid key color."
    return lookup_key_from_color[color]