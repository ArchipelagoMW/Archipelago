from typing import Dict, Set, Tuple, NamedTuple, Optional

class ItemData(NamedTuple):
    category: str
    code: int
    classification: str
    amount: Optional[int] = 1

item_table: Dict[str, ItemData] = {
    'Silver Sword': ItemData('Swords', 0x5A1000, "progression"),
    'Fire Sword': ItemData('Swords', 0x5A1001, "progression"),
    'Ice Sword': ItemData('Swords', 0x5A1002, "progression"),
    'Thunder Sword': ItemData('Swords', 0x5A1003, "progression"),
    'Crystal Sword': ItemData('Swords', 0x5A1004, "progression"),
    'Power Sword': ItemData('Swords', 0x5A1005, "progression"),
    'Light Sword': ItemData('Swords', 0x5A1006, "progression", 0),
    'Dagger': ItemData('Projectiles', 0x5A1007, "progression"),
    'Fireballs': ItemData('Projectiles', 0x5A1008, "progression"),
    'Boomerang': ItemData('Projectiles', 0x5A1009, "progression", 0),
    'Ax': ItemData('Projectiles', 0x5A100A, "progression"),
    'Shovel': ItemData('Items', 0x5A100B, "progression"),

    'Fire Armor': ItemData('Armor', 0x5A100C, "progression"),
    'Ice Armor': ItemData('Armor', 0x5A100D, "progression"),
    'Aqua Armor': ItemData('Armor', 0x5A100E, "progression"),
    'Light Armor': ItemData('Armor', 0x5A100F, "progression", 0),

    'Fire Shield': ItemData('Shields', 0x5A1010, "useful"),
    'Ice Shield': ItemData('Shields', 0x5A1011, "useful"),
    'Aqua Shield': ItemData('Shields', 0x5A1012, "useful"),
    'Light Shield': ItemData('Shields', 0x5A1013, "useful", 0),

    'Wand': ItemData('Equipment', 0x5A1014, "progression"),
    'Ice Bell': ItemData('Equipment', 0x5A1015, "progression"),
    'Sun Ring': ItemData('Equipment', 0x5A1016, "progression"),
    'Power Fan': ItemData('Equipment', 0x5A1017, "progression"),
    'Elven Flute': ItemData('Equipment', 0x5A1018, "progression"),
    'Sky Bell': ItemData('Equipment', 0x5A1019, "progression"),
    'Light Stone': ItemData('Equipment', 0x5A101A, "progression"),
    'Sun Stone': ItemData('Equipment', 0x5A101B, "progression"),
    'Star Stone': ItemData('Equipment', 0x5A101C, "progression"),
    'Aqua Stone': ItemData('Equipment', 0x5A101D, "progression"),
    'Moon Stone': ItemData('Equipment', 0x5A101E, "progression"),

    'Light Spell': ItemData('Spells', 0x5A101F, "progression"),
    'Star Spell': ItemData('Spells', 0x5A1020, "progression"),
    'Sun Spell': ItemData('Spells', 0x5A1021, "progression"),
    'Aqua Spell': ItemData('Spells', 0x5A1022, "progression"),
    'Moon Spell': ItemData('Spells', 0x5A1023, "progression"),

    'Shove': ItemData('Skills', 0x5A1024, "progression"),
    'Up Jab': ItemData('Skills', 0x5A1025, "progression"),
    'Down Jab': ItemData('Skills', 0x5A1026, "progression"),

    'Life Bottle': ItemData('Upgrades', 0x5A1027, "progression", 9),
    'Magic Bottle': ItemData('Upgrades', 0x5A1028, "useful", 13),

    '500 Coins': ItemData('Coins', 0x5A1029, "progression", 2),
    '1000 Coins': ItemData('Coins', 0x5A102A, "progression", 5),
    '2000 Coins': ItemData('Coins', 0x5A102B, "progression", 3),
    '5000 Coins': ItemData('Coins', 0x5A102C, "progression", 1),

    'Light Switch': ItemData('Events', None, "progression", 0),
    'Sun Switch': ItemData('Events', None, "progression", 0),
    'Star Switch': ItemData('Events', None, "progression", 0),
    'Aqua Switch': ItemData('Events', None, "progression", 0),
    'Moon Switch': ItemData('Events', None, "progression", 0),
    'Puka-Puka Drained': ItemData('Events', None, "progression", 0),
    'Tina': ItemData('Events', None, "progression", 0),
    'Boa-Hiya Shortcut Open': ItemData('Events', None, "progression", 0),
    'Sala-Hiya Shortcut Open': ItemData('Events', None, "progression", 0),
    'Sala-Puka Shortcut Open': ItemData('Events', None, "progression", 0),
    'Fuwa-Poka Shortcut Open': ItemData('Events', None, "progression", 0),
    'Fuwa-Puka Shortcut Open': ItemData('Events', None, "progression", 0),

    'Light Gate Lowered': ItemData('Events', None, "progression", 0),
    'Sun Gate Lowered': ItemData('Events', None, "progression", 0),
    'Star Gate Lowered': ItemData('Events', None, "progression", 0),
    'Aqua Gate Lowered': ItemData('Events', None, "progression", 0),
    'Moon Gate Lowered': ItemData('Events', None, "progression", 0),
}

filler_items: Tuple[str, ...] = (
    '500 Coins',
    '1000 Coins',
    '2000 Coins',
    '5000 Coins',
    'Life Bottle',
    'Magic Bottle'
)

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
