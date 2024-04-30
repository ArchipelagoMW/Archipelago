"""
Classes and functions related to AP items for Pokemon Emerald
"""
from typing import Dict, FrozenSet, Optional

from BaseClasses import Item, ItemClassification

from .data import BASE_OFFSET, data


class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[reverse_offset_item_value(code)].tags


def offset_item_value(item_value: int) -> int:
    """
    Returns the AP item id (code) for a given item value
    """
    return item_value + BASE_OFFSET


def reverse_offset_item_value(item_id: int) -> int:
    """
    Returns the item value for a given AP item id (code)
    """
    return item_id - BASE_OFFSET


def create_item_label_to_code_map() -> Dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    label_to_code_map: Dict[str, int] = {}
    for item_value, attributes in data.items.items():
        label_to_code_map[attributes.label] = offset_item_value(item_value)

    return label_to_code_map


ITEM_GROUPS = {
    "Badges": {
        "Stone Badge", "Knuckle Badge",
        "Dynamo Badge", "Heat Badge",
        "Balance Badge", "Feather Badge",
        "Mind Badge", "Rain Badge",
    },
    "HMs": {
        "HM01 Cut", "HM02 Fly",
        "HM03 Surf", "HM04 Strength",
        "HM05 Flash", "HM06 Rock Smash",
        "HM07 Waterfall", "HM08 Dive",
    },
    "HM01": {"HM01 Cut"},
    "HM02": {"HM02 Fly"},
    "HM03": {"HM03 Surf"},
    "HM04": {"HM04 Strength"},
    "HM05": {"HM05 Flash"},
    "HM06": {"HM06 Rock Smash"},
    "HM07": {"HM07 Waterfall"},
    "HM08": {"HM08 Dive"},
    },
    "TMs": { #This will probly not do anything if the TM is obtained from a npc like in the location group "Gym TMs" ?
        "TM01",
        "TM02",
        "TM03", #Sootopolis Gym - TM03 from Juan
        "TM04", #Mossdeep Gym - TM04 from Tate and Liza
        "TM05", #Route 114 - TM05 from Roaring Man
        "TM06",
        "TM07",
        "TM08", #Dewford Gym - TM08 from Brawly
        "TM09", #Route 104 - TM09 from Boy
        "TM10", #Fortree City - TM10 from Hidden Power Lady
        "TM11",
        "TM12",
        "TM13",
        "TM14",
        "TM15",
        "TM16",
        "TM17",
        "TM18",
        "TM19", #Route 123 - TM19 from Girl near Berries
        "TM20",
        "TM21", #Pacifidlog Town - TM21 from Man in House
        "TM22",
        "TM23",
        "TM24", #Mauville City - TM24 from Wattson
        "TM25",
        "TM26",
        "TM27", #Fallarbor Town - TM27 from Cozmo &/ Pacifidlog Town - TM27 from Man in House
        "TM28", #Route 114 - TM28 from Fossil Maniac's Brother
        "TM29",
        "TM30",
        "TM31", #Sootopolis City - TM31 from Black Belt in House
        "TM32",
        "TM33",
        "TM34", #Mauville Gym - TM34 from Wattson
        "TM35",
        "TM36", #Dewford Town - TM36 from Sludge Bomb Man
        "TM37",
        "TM38",
        "TM39", #Rustboro Gym - TM39 from Roxanne
        "TM40", #Fortree Gym - TM40 from Winona
        "TM41", #Slateport City - TM41 from Sailor in Battle Tent
        "TM42", #Petalburg Gym - TM42 from Norman
        "TM43",
        "TM44", #Lilycove City - TM44 from Man in House
        "TM45", #Verdanturf Town - TM45 from Woman in Battle Tent
        "TM46", #Oceanic Museum - TM46 from Aqua Grunt in Museum
        "TM47", #Granite Cave 1F - TM47 from Steven
        "TM48",
        "TM49", #SS Tidal - TM49 from Thief
        "TM50", #Lavaridge Gym - TM50 from Flannery
    },
    "Battle Items": {
        "Dire Hit",
        "Guard Spec",
        "X Accuracy",
        "X Attack",
        "X Defend",
        "X Special",
        "X Speed",
    },
    "Consumables": {
        "Antidote",
        "Awakening",
        "Berry Juice", #not a berry
        "Burn Heal",
        "Elixir",
        "Energy Powder",
        "Energy Root",
        "Escape Rope",
        "Ether",
        "Fresh Water",
        "Fluffy Tail",
        "Full Heal",
        "Full Restore",
        "Heal Powder",
        "Hyper Potion",
        "Ice Heal",
        "Lava Cookie",
        "Lemonade",
        "Max Elixir",
        "Max Ether",
        "Max Potion",
        "Max Repel",
        "Max Revive",
        "Moomoo Milk",
        "Paralyze Heal",
        "Potion",
        "Rare Candy",
        "Repel",
        "Revival Herb",
        "Revive",
        "Sacred Ash",
        "Soda Pop",
        "Super Potion",
        "Super Repel",
        "Black Flute",
        "Blue Flute",
        "Red Flute",
        "White Flute",
        "Yellow Flute",
        "Poke Doll",
    },
    "Vitamins": {
        "Calcium",
        "Carbos",
        "HP Up",
        "Iron",
        "PP Max",
        "PP Up",
        "Protein",
        "Zinc",
    },
    "Key Items": { # All Tickets, Keys etc
        "Acro Bike",
        "Aurora Ticket",
        "Basement Key",
        "Coin Case",
        "Contest Pass",
        "Devon Goods",
        "Devon Scope",
        "Eon Ticket",
        "Go Goggles",
        "Good Rod",
        "Itemfinder",
        "Letter",
        "Magma Emblem",
        "Mach Bike",
        "Meteorite",
        "Mystic Ticket",
        "Old Sea Map",
        "Old Rod",
        "Powder Jar",
        "Pokeblock Case",
        "Room 1 Key",
        "Room 2 Key",
        "Room 4 Key",
        "Room 6 Key",
        "Super Rod",
        "S.S. Ticket",
        "Scanner",
        "Storage Key",
        "Wailmer Pail",
    },
    "Bikes": {
        "Acro Bike",
        "Mach Bike",
    },
    "Fishing Rods": {
        "Old Rod",
        "Good Rod",
        "Super Rod",
    },
    "Keys": {
        "Basement Key",
        "Storage Key",
        "Room 1 Key",
        "Room 2 Key",
        "Room 4 Key",
        "Room 6 Key",
    },
    "Tickets": {
        "Aurora Ticket",
        "Eon Ticket",
        "Mystic Ticket",
        "S.S. Ticket",
        "Old Sea Map", #think this act as a ticket?
    },
    "Fossils": { #These are not considered key items from gen4 and onwards
        "Root Fossil",
        "Claw Fossil",
    },
    "Poke Balls": {
        "Dive Ball",
        "Great Ball",
        "Luxury Ball",
        "Master Ball",
        "Nest Ball",
        "Net Ball",
        "Poke Ball",
        "Premier Ball",
        "Repeat Ball",
        "Safari Ball",
        "Timer Ball",
        "Ultra Ball",
    },
    "Mails": {
        "Bead Mail",
        "Dream Mail",
        "Fab Mail",
        "Glitter Mail",
        "Harbor Mail",
        "Mech Mail",
        "Orange Mail",
        "Retro Mail",
        "Shadow Mail",
        "Tropic Mail",
        "Wave Mail",
        "Wood Mail",
    },
    "Evolution Stones": {
        "Fire Stone",
        "Leaf Stone",
        "Moon Stone",
        "Sun Stone",
        "Thunder Stone",
        "Water Stone",
    },
    "Berries": { #So many berries, 42
        "Aguav Berry",
        "Apicot Berry",
        "Aspear Berry",
        "Belue Berry",
        "Bluk Berry",
        "Cheri Berry",
        "Chesto Berry",
        "Cornn Berry",
        "Durin Berry",
        "Figy Berry",
        "Ganlon Berry",
        "Grepa Berry",
        "Hondew Berry",
        "Iapapa Berry",
        "Kelpsy Berry",
        "Lansat Berry",
        "Leppa Berry",
        "Liechi Berry",
        "Lum Berry",
        "Mago Berry",
        "Magost Berry",
        "Nanab Berry",
        "Nomel Berry",
        "Oran Berry",
        "Pamtre Berry",
        "Pecha Berry",
        "Persim Berry",
        "Petaya Berry",
        "Pinap Berry",
        "Pomeg Berry",
        "Qualot Berry",
        "Rabuta Berry",
        "Rawst Berry",
        "Razz Berry",
        "Salac Berry",
        "Sitrus Berry",
        "Spelon Berry",
        "Starf Berry",
        "Tamato Berry",
        "Watmel Berry",
        "Wepear Berry",
        "Wiki Berry",
    },
    "Held items": { 
        "Amulet Coin",
        "Black Belt",
        "Black Glasses",
        "Blue Scarf",
        "Bright Powder",
        "Charcoal",
        "Choice Band",
        "Cleanse Tag",
        "Deep Sea Scale",
        "Deep Sea Tooth",
        "Dragon Fang",
        "Dragon Scale",
        "Everstone",
        "Exp. Share",
        "Focus Band",
        "Green Scarf",
        "Up-Grade",
        "Hard Stone",
        "King's Rock",
        "Lax Incense",
        "Leftovers",
        "Light Ball",
        "Lucky Egg",
        "Lucky Punch",
        "Macho Brace",
        "Magnet",
        "Mental Herb",
        "Metal Coat",
        "Metal Powder",
        "Miracle Seed",
        "Mystic Water",
        "Never-Melt Ice",
        "Pink Scarf",
        "Poison Barb",
        "Quick Claw",
        "Red Scarf",
        "Scope Lens",
        "Sea Incense",
        "Sharp Beak",
        "Shell Bell",
        "Silk Scarf",
        "Silver Powder",
        "Smoke Ball",
        "Soft Sand",
        "Soot Sack",
        "Soothe Bell",
        "Soul Dew",
        "Spell Tag",
        "Stick",
        "Thick Club",
        "Twisted Spoon",
        "White Herb",
        "Yellow Scarf",
    },
    "Filler Items": { #for sorting etc items that don't fit anywhere else
        "Big Mushroom",
        "Big Pearl",
        "Blue Shard",
        "Green Shard",
        "Heart Scale",
        "Nugget",
        "Pearl",
        "Red Shard",
        "Shoal Salt",
        "Shoal Shell",
        "Star Piece",
        "Stardust",
        "Tiny Mushroom",
        "Yellow Shard",
    } 
}


def get_item_classification(item_code: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[reverse_offset_item_value(item_code)].classification
