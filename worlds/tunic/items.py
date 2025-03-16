from itertools import groupby
from typing import Dict, List, Set, NamedTuple, Optional
from BaseClasses import ItemClassification as IC


class TunicItemData(NamedTuple):
    classification: IC
    quantity_in_item_pool: int
    item_id_offset: int
    item_group: str = ""
    # classification if combat logic is on
    combat_ic: Optional[IC] = None


item_base_id = 509342400

item_table: Dict[str, TunicItemData] = {
    "Firecracker x2": TunicItemData(IC.filler, 3, 0, "Bombs"),
    "Firecracker x3": TunicItemData(IC.filler, 3, 1, "Bombs"),
    "Firecracker x4": TunicItemData(IC.filler, 3, 2, "Bombs"),
    "Firecracker x5": TunicItemData(IC.filler, 1, 3, "Bombs"),
    "Firecracker x6": TunicItemData(IC.filler, 2, 4, "Bombs"),
    "Fire Bomb x2": TunicItemData(IC.filler, 2, 5, "Bombs"),
    "Fire Bomb x3": TunicItemData(IC.filler, 1, 6, "Bombs"),
    "Ice Bomb x2": TunicItemData(IC.filler, 2, 7, "Bombs"),
    "Ice Bomb x3": TunicItemData(IC.filler, 2, 8, "Bombs"),
    "Ice Bomb x5": TunicItemData(IC.filler, 1, 9, "Bombs"),
    "Lure": TunicItemData(IC.filler, 4, 10, "Consumables"),
    "Lure x2": TunicItemData(IC.filler, 1, 11, "Consumables"),
    "Pepper x2": TunicItemData(IC.filler, 4, 12, "Consumables"),
    "Ivy x3": TunicItemData(IC.filler, 2, 13, "Consumables"),
    "Effigy": TunicItemData(IC.useful, 12, 14, "Money", combat_ic=IC.progression),
    "HP Berry": TunicItemData(IC.filler, 2, 15, "Consumables"),
    "HP Berry x2": TunicItemData(IC.filler, 4, 16, "Consumables"),
    "HP Berry x3": TunicItemData(IC.filler, 2, 17, "Consumables"),
    "MP Berry": TunicItemData(IC.filler, 4, 18, "Consumables"),
    "MP Berry x2": TunicItemData(IC.filler, 2, 19, "Consumables"),
    "MP Berry x3": TunicItemData(IC.filler, 7, 20, "Consumables"),
    "Fairy": TunicItemData(IC.progression, 20, 21),
    "Stick": TunicItemData(IC.progression | IC.useful, 1, 22, "Weapons"),
    "Sword": TunicItemData(IC.progression | IC.useful, 3, 23, "Weapons"),
    "Sword Upgrade": TunicItemData(IC.progression | IC.useful, 4, 24, "Weapons"),
    "Magic Wand": TunicItemData(IC.progression | IC.useful, 1, 25, "Weapons"),
    "Magic Dagger": TunicItemData(IC.progression | IC.useful, 1, 26),
    "Magic Orb": TunicItemData(IC.progression | IC.useful, 1, 27),
    "Hero's Laurels": TunicItemData(IC.progression | IC.useful, 1, 28),
    "Lantern": TunicItemData(IC.progression, 1, 29),
    "Gun": TunicItemData(IC.progression | IC.useful, 1, 30, "Weapons"),
    "Shield": TunicItemData(IC.useful, 1, 31, combat_ic=IC.progression | IC.useful),
    "Dath Stone": TunicItemData(IC.useful, 1, 32),
    "Torch": TunicItemData(IC.useful, 0, 156),
    "Hourglass": TunicItemData(IC.useful, 1, 33),
    "Old House Key": TunicItemData(IC.progression, 1, 34, "Keys"),
    "Key": TunicItemData(IC.progression, 2, 35, "Keys"),
    "Fortress Vault Key": TunicItemData(IC.progression, 1, 36, "Keys"),
    "Flask Shard": TunicItemData(IC.useful, 12, 37, combat_ic=IC.progression),
    "Potion Flask": TunicItemData(IC.useful, 5, 38, "Flask", combat_ic=IC.progression),
    "Golden Coin": TunicItemData(IC.progression, 17, 39),
    "Card Slot": TunicItemData(IC.useful, 4, 40),
    "Red Questagon": TunicItemData(IC.progression_skip_balancing, 1, 41, "Hexagons"),
    "Green Questagon": TunicItemData(IC.progression_skip_balancing, 1, 42, "Hexagons"),
    "Blue Questagon": TunicItemData(IC.progression_skip_balancing, 1, 43, "Hexagons"),
    "Gold Questagon": TunicItemData(IC.progression_skip_balancing, 0, 44, "Hexagons"),
    "ATT Offering": TunicItemData(IC.useful, 4, 45, "Offerings", combat_ic=IC.progression),
    "DEF Offering": TunicItemData(IC.useful, 4, 46, "Offerings", combat_ic=IC.progression),
    "Potion Offering": TunicItemData(IC.useful, 3, 47, "Offerings", combat_ic=IC.progression),
    "HP Offering": TunicItemData(IC.useful, 6, 48, "Offerings", combat_ic=IC.progression),
    "MP Offering": TunicItemData(IC.useful, 3, 49, "Offerings", combat_ic=IC.progression),
    "SP Offering": TunicItemData(IC.useful, 2, 50, "Offerings", combat_ic=IC.progression),
    "Hero Relic - ATT": TunicItemData(IC.progression_skip_balancing, 1, 51, "Hero Relics", combat_ic=IC.progression),
    "Hero Relic - DEF": TunicItemData(IC.progression_skip_balancing, 1, 52, "Hero Relics", combat_ic=IC.progression),
    "Hero Relic - HP": TunicItemData(IC.progression_skip_balancing, 1, 53, "Hero Relics", combat_ic=IC.progression),
    "Hero Relic - MP": TunicItemData(IC.progression_skip_balancing, 1, 54, "Hero Relics", combat_ic=IC.progression),
    "Hero Relic - POTION": TunicItemData(IC.progression_skip_balancing, 1, 55, "Hero Relics", combat_ic=IC.progression),
    "Hero Relic - SP": TunicItemData(IC.progression_skip_balancing, 1, 56, "Hero Relics", combat_ic=IC.progression),
    "Orange Peril Ring": TunicItemData(IC.useful, 1, 57, "Cards"),
    "Tincture": TunicItemData(IC.useful, 1, 58, "Cards"),
    "Scavenger Mask": TunicItemData(IC.progression, 1, 59, "Cards"),
    "Cyan Peril Ring": TunicItemData(IC.useful, 1, 60, "Cards"),
    "Bracer": TunicItemData(IC.useful, 1, 61, "Cards"),
    "Dagger Strap": TunicItemData(IC.useful, 1, 62, "Cards"),
    "Inverted Ash": TunicItemData(IC.useful, 1, 63, "Cards"),
    "Lucky Cup": TunicItemData(IC.useful, 1, 64, "Cards"),
    "Magic Echo": TunicItemData(IC.useful, 1, 65, "Cards"),
    "Anklet": TunicItemData(IC.useful, 1, 66, "Cards"),
    "Muffling Bell": TunicItemData(IC.useful, 1, 67, "Cards"),
    "Glass Cannon": TunicItemData(IC.useful, 1, 68, "Cards"),
    "Perfume": TunicItemData(IC.useful, 1, 69, "Cards"),
    "Louder Echo": TunicItemData(IC.useful, 1, 70, "Cards"),
    "Aura's Gem": TunicItemData(IC.useful, 1, 71, "Cards"),
    "Bone Card": TunicItemData(IC.useful, 1, 72, "Cards"),
    "Mr Mayor": TunicItemData(IC.useful, 1, 73, "Golden Treasures", combat_ic=IC.progression),
    "Secret Legend": TunicItemData(IC.useful, 1, 74, "Golden Treasures", combat_ic=IC.progression),
    "Sacred Geometry": TunicItemData(IC.useful, 1, 75, "Golden Treasures", combat_ic=IC.progression),
    "Vintage": TunicItemData(IC.useful, 1, 76, "Golden Treasures", combat_ic=IC.progression),
    "Just Some Pals": TunicItemData(IC.useful, 1, 77, "Golden Treasures", combat_ic=IC.progression),
    "Regal Weasel": TunicItemData(IC.useful, 1, 78, "Golden Treasures", combat_ic=IC.progression),
    "Spring Falls": TunicItemData(IC.useful, 1, 79, "Golden Treasures", combat_ic=IC.progression),
    "Power Up": TunicItemData(IC.useful, 1, 80, "Golden Treasures", combat_ic=IC.progression),
    "Back To Work": TunicItemData(IC.useful, 1, 81, "Golden Treasures", combat_ic=IC.progression),
    "Phonomath": TunicItemData(IC.useful, 1, 82, "Golden Treasures", combat_ic=IC.progression),
    "Dusty": TunicItemData(IC.useful, 1, 83, "Golden Treasures", combat_ic=IC.progression),
    "Forever Friend": TunicItemData(IC.useful, 1, 84, "Golden Treasures", combat_ic=IC.progression),
    "Fool Trap": TunicItemData(IC.trap, 0, 85),
    "Money x1": TunicItemData(IC.filler, 3, 86, "Money"),
    "Money x2": TunicItemData(IC.filler, 0, 152, "Money"),
    "Money x3": TunicItemData(IC.filler, 0, 153, "Money"),
    "Money x4": TunicItemData(IC.filler, 0, 154, "Money"),
    "Money x5": TunicItemData(IC.filler, 0, 155, "Money"),
    "Money x10": TunicItemData(IC.filler, 1, 87, "Money"),
    "Money x15": TunicItemData(IC.filler, 10, 88, "Money"),
    "Money x16": TunicItemData(IC.filler, 1, 89, "Money"),
    "Money x20": TunicItemData(IC.filler, 17, 90, "Money"),
    "Money x25": TunicItemData(IC.filler, 14, 91, "Money"),
    "Money x30": TunicItemData(IC.filler, 4, 92, "Money"),
    "Money x32": TunicItemData(IC.filler, 4, 93, "Money"),
    "Money x40": TunicItemData(IC.filler, 3, 94, "Money"),
    "Money x48": TunicItemData(IC.filler, 1, 95, "Money"),
    "Money x50": TunicItemData(IC.filler, 7, 96, "Money"),
    "Money x64": TunicItemData(IC.filler, 1, 97, "Money"),
    "Money x100": TunicItemData(IC.filler, 5, 98, "Money"),
    "Money x128": TunicItemData(IC.useful, 3, 99, "Money", combat_ic=IC.progression),
    "Money x200": TunicItemData(IC.useful, 1, 100, "Money", combat_ic=IC.progression),
    "Money x255": TunicItemData(IC.useful, 1, 101, "Money", combat_ic=IC.progression),
    "Pages 0-1": TunicItemData(IC.useful, 1, 102, "Pages"),
    "Pages 2-3": TunicItemData(IC.useful, 1, 103, "Pages"),
    "Pages 4-5": TunicItemData(IC.useful, 1, 104, "Pages"),
    "Pages 6-7": TunicItemData(IC.useful, 1, 105, "Pages"),
    "Pages 8-9": TunicItemData(IC.useful, 1, 106, "Pages"),
    "Pages 10-11": TunicItemData(IC.useful, 1, 107, "Pages"),
    "Pages 12-13": TunicItemData(IC.useful, 1, 108, "Pages"),
    "Pages 14-15": TunicItemData(IC.useful, 1, 109, "Pages"),
    "Pages 16-17": TunicItemData(IC.useful, 1, 110, "Pages"),
    "Pages 18-19": TunicItemData(IC.useful, 1, 111, "Pages"),
    "Pages 20-21": TunicItemData(IC.useful, 1, 112, "Pages"),
    "Pages 22-23": TunicItemData(IC.useful, 1, 113, "Pages"),
    "Pages 24-25 (Prayer)": TunicItemData(IC.progression | IC.useful, 1, 114, "Pages"),
    "Pages 26-27": TunicItemData(IC.useful, 1, 115, "Pages"),
    "Pages 28-29": TunicItemData(IC.useful, 1, 116, "Pages"),
    "Pages 30-31": TunicItemData(IC.useful, 1, 117, "Pages"),
    "Pages 32-33": TunicItemData(IC.useful, 1, 118, "Pages"),
    "Pages 34-35": TunicItemData(IC.useful, 1, 119, "Pages"),
    "Pages 36-37": TunicItemData(IC.useful, 1, 120, "Pages"),
    "Pages 38-39": TunicItemData(IC.useful, 1, 121, "Pages"),
    "Pages 40-41": TunicItemData(IC.useful, 1, 122, "Pages"),
    "Pages 42-43 (Holy Cross)": TunicItemData(IC.progression | IC.useful, 1, 123, "Pages"),
    "Pages 44-45": TunicItemData(IC.useful, 1, 124, "Pages"),
    "Pages 46-47": TunicItemData(IC.useful, 1, 125, "Pages"),
    "Pages 48-49": TunicItemData(IC.useful, 1, 126, "Pages"),
    "Pages 50-51": TunicItemData(IC.useful, 1, 127, "Pages"),
    "Pages 52-53 (Icebolt)": TunicItemData(IC.progression, 1, 128, "Pages"),
    "Pages 54-55": TunicItemData(IC.useful, 1, 129, "Pages"),
    "Ladders near Weathervane": TunicItemData(IC.progression, 0, 130, "Ladders"),
    "Ladders near Overworld Checkpoint": TunicItemData(IC.progression, 0, 131, "Ladders"),
    "Ladders near Patrol Cave": TunicItemData(IC.progression, 0, 132, "Ladders"),
    "Ladder near Temple Rafters": TunicItemData(IC.progression, 0, 133, "Ladders"),
    "Ladders near Dark Tomb": TunicItemData(IC.progression, 0, 134, "Ladders"),
    "Ladder to Quarry": TunicItemData(IC.progression, 0, 135, "Ladders"),
    "Ladders to West Bell": TunicItemData(IC.progression, 0, 136, "Ladders"),
    "Ladders in Overworld Town": TunicItemData(IC.progression, 0, 137, "Ladders"),
    "Ladder to Ruined Atoll": TunicItemData(IC.progression, 0, 138, "Ladders"),
    "Ladder to Swamp": TunicItemData(IC.progression, 0, 139, "Ladders"),
    "Ladders in Well": TunicItemData(IC.progression, 0, 140, "Ladders"),
    "Ladder in Dark Tomb": TunicItemData(IC.progression, 0, 141, "Ladders"),
    "Ladder to East Forest": TunicItemData(IC.progression, 0, 142, "Ladders"),
    "Ladders to Lower Forest": TunicItemData(IC.progression, 0, 143, "Ladders"),
    "Ladder to Beneath the Vault": TunicItemData(IC.progression, 0, 144, "Ladders"),
    "Ladders in Hourglass Cave": TunicItemData(IC.progression, 0, 145, "Ladders"),
    "Ladders in South Atoll": TunicItemData(IC.progression, 0, 146, "Ladders"),
    "Ladders to Frog's Domain": TunicItemData(IC.progression, 0, 147, "Ladders"),
    "Ladders in Library": TunicItemData(IC.progression, 0, 148, "Ladders"),
    "Ladders in Lower Quarry": TunicItemData(IC.progression, 0, 149, "Ladders"),
    "Ladders in Swamp": TunicItemData(IC.progression, 0, 150, "Ladders"),
    "Grass": TunicItemData(IC.filler, 0, 151),
}

# items to be replaced by fool traps
fool_tiers: List[List[str]] = [
    [],
    ["Money x1", "Money x10", "Money x15", "Money x16"],
    ["Money x1", "Money x10", "Money x15", "Money x16", "Money x20"],
    ["Money x1", "Money x10", "Money x15", "Money x16", "Money x20", "Money x25", "Money x30"],
]

# items we'll want the location of in slot data, for generating in-game hints
slot_data_item_names = [
    "Stick",
    "Sword",
    "Sword Upgrade",
    "Magic Dagger",
    "Magic Wand",
    "Magic Orb",
    "Hero's Laurels",
    "Lantern",
    "Gun",
    "Scavenger Mask",
    "Shield",
    "Dath Stone",
    "Hourglass",
    "Old House Key",
    "Fortress Vault Key",
    "Hero Relic - ATT",
    "Hero Relic - DEF",
    "Hero Relic - POTION",
    "Hero Relic - HP",
    "Hero Relic - SP",
    "Hero Relic - MP",
    "Pages 24-25 (Prayer)",
    "Pages 42-43 (Holy Cross)",
    "Pages 52-53 (Icebolt)",
    "Red Questagon",
    "Green Questagon",
    "Blue Questagon",
    "Gold Questagon",
]

combat_items: List[str] = [name for name, data in item_table.items()
                           if data.combat_ic and IC.progression in data.combat_ic]
combat_items.extend(["Stick", "Sword", "Sword Upgrade", "Magic Wand", "Hero's Laurels", "Gun"])

item_name_to_id: Dict[str, int] = {name: item_base_id + data.item_id_offset for name, data in item_table.items()}

filler_items: List[str] = [name for name, data in item_table.items() if data.classification == IC.filler and name != "Grass"]


def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_table, key=get_item_group), get_item_group) if group != ""
}

# extra groups for the purpose of aliasing items
extra_groups: Dict[str, Set[str]] = {
    "Laurels": {"Hero's Laurels"},
    "Orb": {"Magic Orb"},
    "Dagger": {"Magic Dagger"},
    "Wand": {"Magic Wand"},
    "Magic Rod": {"Magic Wand"},
    "Fire Rod": {"Magic Wand"},
    "Holy Cross": {"Pages 42-43 (Holy Cross)"},
    "Prayer": {"Pages 24-25 (Prayer)"},
    "Icebolt": {"Pages 52-53 (Icebolt)"},
    "Ice Rod": {"Pages 52-53 (Icebolt)"},
    "Melee Weapons": {"Stick", "Sword", "Sword Upgrade"},
    "Progressive Sword": {"Sword Upgrade"},
    "Abilities": {"Pages 24-25 (Prayer)", "Pages 42-43 (Holy Cross)", "Pages 52-53 (Icebolt)"},
    "Questagons": {"Red Questagon", "Green Questagon", "Blue Questagon", "Gold Questagon"},
    "Ladder to Atoll": {"Ladder to Ruined Atoll"},  # fuzzy matching made it hint Ladders in Well, now it won't
    "Ladders to Bell": {"Ladders to West Bell"},
    "Ladders to Well": {"Ladders in Well"},  # fuzzy matching decided Ladders in Well was Ladders to West Bell
    "Ladders in Atoll": {"Ladders in South Atoll"},
    "Ladders in Ruined Atoll": {"Ladders in South Atoll"},
    "Ladders in Town": {"Ladders in Overworld Town"},  # fuzzy matching decided this was Ladders in South Atoll
    "Ladder in Quarry": {"Ladders in Lower Quarry"},  # fuzzy matching decided this was Ladder to Quarry
}

item_name_groups.update(extra_groups)
