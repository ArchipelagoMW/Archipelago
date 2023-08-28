from itertools import groupby
from typing import Dict, List, Set, NamedTuple
from BaseClasses import ItemClassification


class TunicItemData(NamedTuple):
    classification: ItemClassification
    quantity_in_item_pool: int
    item_group: str = ""


item_table: Dict[str, TunicItemData] = {
    "Firecracker x2": TunicItemData(ItemClassification.filler, 3, "bombs"),
    "Firecracker x3": TunicItemData(ItemClassification.filler, 3, "bombs"),
    "Firecracker x4": TunicItemData(ItemClassification.filler, 3, "bombs"),
    "Firecracker x5": TunicItemData(ItemClassification.filler, 1, "bombs"),
    "Firecracker x6": TunicItemData(ItemClassification.filler, 2, "bombs"),
    "Fire Bomb x2": TunicItemData(ItemClassification.filler, 2, "bombs"),
    "Fire Bomb x3": TunicItemData(ItemClassification.filler, 1, "bombs"),
    "Ice Bomb x2": TunicItemData(ItemClassification.filler, 2, "bombs"),
    "Ice Bomb x3": TunicItemData(ItemClassification.filler, 2, "bombs"),
    "Ice Bomb x5": TunicItemData(ItemClassification.filler, 1, "bombs"),
    "Lure": TunicItemData(ItemClassification.filler, 4, "consumables"),
    "Lure x2": TunicItemData(ItemClassification.filler, 1, "consumables"),
    "Pepper x2": TunicItemData(ItemClassification.filler, 4, "consumables"),
    "Ivy x3": TunicItemData(ItemClassification.filler, 2, "consumables"),
    "Effigy": TunicItemData(ItemClassification.useful, 12, "money"),
    "HP Berry": TunicItemData(ItemClassification.filler, 2, "consumables"),
    "HP Berry x2": TunicItemData(ItemClassification.filler, 4, "consumables"),
    "HP Berry x3": TunicItemData(ItemClassification.filler, 2, "consumables"),
    "MP Berry": TunicItemData(ItemClassification.filler, 4, "consumables"),
    "MP Berry x2": TunicItemData(ItemClassification.filler, 2, "consumables"),
    "MP Berry x3": TunicItemData(ItemClassification.filler, 7, "consumables"),
    "Fairy": TunicItemData(ItemClassification.progression, 20),
    "Stick": TunicItemData(ItemClassification.progression, 1, "weapons"),
    "Sword": TunicItemData(ItemClassification.progression, 3, "weapons"),
    "Sword Upgrade": TunicItemData(ItemClassification.progression, 4, "weapons"),
    "Magic Wand": TunicItemData(ItemClassification.progression, 1, "weapons"),
    "Magic Dagger": TunicItemData(ItemClassification.progression, 1),
    "Magic Orb": TunicItemData(ItemClassification.progression, 1),
    "Hero's Laurels": TunicItemData(ItemClassification.progression, 1),
    "Lantern": TunicItemData(ItemClassification.progression, 1),
    "Shotgun": TunicItemData(ItemClassification.useful, 1, "weapons"),
    "Shield": TunicItemData(ItemClassification.useful, 1),
    "Dath Stone": TunicItemData(ItemClassification.useful, 1),
    "Hourglass": TunicItemData(ItemClassification.useful, 1),
    "Old House Key": TunicItemData(ItemClassification.progression, 1, "keys"),
    "Key": TunicItemData(ItemClassification.progression, 2, "keys"),
    "Fortress Vault Key": TunicItemData(ItemClassification.progression, 1, "keys"),
    "Flask Shard": TunicItemData(ItemClassification.useful, 12, "potions"),
    "Potion Flask": TunicItemData(ItemClassification.useful, 5, "potions"),
    "Golden Coin": TunicItemData(ItemClassification.progression, 17),
    "Card Slot": TunicItemData(ItemClassification.useful, 4),
    "Red Hexagon": TunicItemData(ItemClassification.progression_skip_balancing, 1, "hexagons"),
    "Green Hexagon": TunicItemData(ItemClassification.progression_skip_balancing, 1, "hexagons"),
    "Blue Hexagon": TunicItemData(ItemClassification.progression_skip_balancing, 1, "hexagons"),
    "Gold Hexagon": TunicItemData(ItemClassification.progression_skip_balancing, 30, "hexagons"),
    "ATT Offering": TunicItemData(ItemClassification.useful, 4, "offerings"),
    "DEF Offering": TunicItemData(ItemClassification.useful, 4, "offerings"),
    "Potion Offering": TunicItemData(ItemClassification.useful, 3, "offerings"),
    "HP Offering": TunicItemData(ItemClassification.useful, 6, "offerings"),
    "MP Offering": TunicItemData(ItemClassification.useful, 3, "offerings"),
    "SP Offering": TunicItemData(ItemClassification.useful, 2, "offerings"),
    "Hero Relic - ATT": TunicItemData(ItemClassification.useful, 1, "hero relics"),
    "Hero Relic - DEF": TunicItemData(ItemClassification.useful, 1, "hero relics"),
    "Hero Relic - HP": TunicItemData(ItemClassification.useful, 1, "hero relics"),
    "Hero Relic - MP": TunicItemData(ItemClassification.useful, 1, "hero relics"),
    "Hero Relic - POTION": TunicItemData(ItemClassification.useful, 1, "hero relics"),
    "Hero Relic - SP": TunicItemData(ItemClassification.useful, 1, "hero relics"),
    "Orange Peril Ring": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Tincture": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Scavenger Mask": TunicItemData(ItemClassification.progression, 1, "cards"),
    "Cyan Peril Ring": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Bracer": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Dagger Strap": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Inverted Ash": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Lucky Cup": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Magic Echo": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Anklet": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Muffling Bell": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Glass Cannon": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Perfume": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Louder Echo": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Aura's Gem": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Bone Card": TunicItemData(ItemClassification.useful, 1, "cards"),
    "Mr Mayor": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Secret Legend": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Sacred Geometry": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Vintage": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Just Some Pals": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Regal Weasel": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Spring Falls": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Power Up": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Back To Work": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Phonomath": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Dusty": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Forever Friend": TunicItemData(ItemClassification.useful, 1, "golden treasures"),
    "Money x1": TunicItemData(ItemClassification.filler, 3, "money"),
    "Money x10": TunicItemData(ItemClassification.filler, 1, "money"),
    "Money x15": TunicItemData(ItemClassification.filler, 10, "money"),
    "Money x16": TunicItemData(ItemClassification.filler, 1, "money"),
    "Money x20": TunicItemData(ItemClassification.filler, 17, "money"),
    "Money x25": TunicItemData(ItemClassification.filler, 14, "money"),
    "Money x30": TunicItemData(ItemClassification.filler, 4, "money"),
    "Money x32": TunicItemData(ItemClassification.filler, 4, "money"),
    "Money x40": TunicItemData(ItemClassification.filler, 3, "money"),
    "Money x48": TunicItemData(ItemClassification.filler, 1, "money"),
    "Money x50": TunicItemData(ItemClassification.filler, 7, "money"),
    "Money x64": TunicItemData(ItemClassification.filler, 1, "money"),
    "Money x100": TunicItemData(ItemClassification.useful, 5, "money"),
    "Money x128": TunicItemData(ItemClassification.useful, 3, "money"),
    "Money x200": TunicItemData(ItemClassification.useful, 1, "money"),
    "Money x255": TunicItemData(ItemClassification.useful, 1, "money"),
    "Pages 0-1": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 2-3": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 4-5": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 6-7": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 8-9": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 10-11": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 12-13": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 14-15": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 16-17": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 18-19": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 20-21": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 22-23": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 24-25 (Prayer)": TunicItemData(ItemClassification.progression, 1, "pages"),
    "Pages 26-27": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 28-29": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 30-31": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 32-33": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 34-35": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 36-37": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 38-39": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 40-41": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 42-43 (Holy Cross)": TunicItemData(ItemClassification.progression, 1, "pages"),
    "Pages 44-45": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 46-47": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 48-49": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 50-51": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
    "Pages 52-53 (Ice Rod)": TunicItemData(ItemClassification.progression, 1, "pages"),
    "Pages 54-55": TunicItemData(ItemClassification.progression_skip_balancing, 1, "pages"),
}


def item_is_filler(item_name: str) -> bool:
    return item_table[item_name].classification == ItemClassification.filler


def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


filler_items: List[str] = list(filter(item_is_filler, item_table.keys()))


item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_table, key=get_item_group), get_item_group)
}

# extra groups for the purpose of aliasing items
extra_groups: Dict[str, Set[str]] = {
    "laurels": {"Hero's Laurels"},
    "holy cross": {"Pages 42-43 (Holy Cross)"},
    "prayer": {"Pages 24-25 (Prayer)"},
    "ice rod": {"Pages 52-53 (Ice Rod)"},
    "melee weapons": {"Stick", "Sword"}
}

item_name_groups.update(extra_groups)
