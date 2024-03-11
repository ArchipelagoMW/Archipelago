from typing import Dict, Set, Tuple, NamedTuple, Optional

class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: str
    amount: Optional[int] = 1

item_table: Dict[str, ItemData] = {
    '! Switch': ItemData('Items', 0x302050, "progression"),
    'Dashed Platform': ItemData('Items', 0x302051, "progression"),
    'Dashed Stairs': ItemData('Items', 0x302052, "progression"),
    'Beanstalk': ItemData('Items', 0x302053, "progression"),
    'Helicopter Morph': ItemData('Morphs', 0x302054, "progression"),
    'Spring Ball': ItemData('Items', 0x302055, "progression"),
    'Large Spring Ball': ItemData('Items', 0x302056, "progression"),
    'Arrow Wheel': ItemData('Items', 0x302057, "progression"),
    'Vanishing Arrow Wheel': ItemData('Items', 0x302058, "progression"),
    'Mole Tank Morph': ItemData('Morphs', 0x302059, "progression"),
    'Watermelon': ItemData('Items', 0x30205A, "progression"),
    'Ice Melon': ItemData('Items', 0x30205B, "progression"),
    'Fire Melon': ItemData('Items', 0x30205C, "progression"),
    'Super Star': ItemData('Items', 0x30205D, "progression"),
    'Car Morph': ItemData('Morphs', 0x30205E, "progression"),
    'Flashing Eggs': ItemData('Items', 0x30205F, "progression"),
    'Giant Eggs': ItemData('Items', 0x302060, "progression"),
    'Egg Launcher': ItemData('Items', 0x302061, "progression"),
    'Egg Plant': ItemData('Items', 0x302062, "progression"),
    'Submarine Morph': ItemData('Morphs', 0x302063, "progression"),
    'Chomp Rock': ItemData('Items', 0x302064, "progression"),
    'Poochy': ItemData('Items', 0x302065, "progression"),
    'Platform Ghost': ItemData('Items', 0x302066, "progression"),
    'Skis': ItemData('Items', 0x302067, "progression"),
    'Train Morph': ItemData('Morphs', 0x302068, "progression"),
    'Key': ItemData('Items', 0x302069, "progression"),
    'Middle Ring': ItemData('Items', 0x30206A, "progression"),
    'Bucket': ItemData('Items', 0x30206B, "progression"),
    'Tulip': ItemData('Items', 0x30206C, "progression"),
    'Egg Capacity Upgrade': ItemData('Items', 0x30206D, "progression", 5),
    'Secret Lens': ItemData('Items', 0x302081, "progression"),

    'World 1 Gate': ItemData('Gates', 0x30206E, "progression"),
    'World 2 Gate': ItemData('Gates', 0x30206F, "progression"),
    'World 3 Gate': ItemData('Gates', 0x302070, "progression"),
    'World 4 Gate': ItemData('Gates', 0x302071, "progression"),
    'World 5 Gate': ItemData('Gates', 0x302072, "progression"),
    'World 6 Gate': ItemData('Gates', 0x302073, "progression"),

    'Extra 1': ItemData('Panels', 0x302074, "progression"),
    'Extra 2': ItemData('Panels', 0x302075, "progression"),
    'Extra 3': ItemData('Panels', 0x302076, "progression"),
    'Extra 4': ItemData('Panels', 0x302077, "progression"),
    'Extra 5': ItemData('Panels', 0x302078, "progression"),
    'Extra 6': ItemData('Panels', 0x302079, "progression"),
    'Extra Panels': ItemData('Panels', 0x30207A, "progression"),

    'Bonus 1': ItemData('Panels', 0x30207B, "progression"),
    'Bonus 2': ItemData('Panels', 0x30207C, "progression"),
    'Bonus 3': ItemData('Panels', 0x30207D, "progression"),
    'Bonus 4': ItemData('Panels', 0x30207E, "progression"),
    'Bonus 5': ItemData('Panels', 0x30207F, "progression"),
    'Bonus 6': ItemData('Panels', 0x302080, "progression"),
    'Bonus Panels': ItemData('Panels', 0x302082, "progression"),

    'Anytime Egg': ItemData('Consumable', 0x302083, "useful", 0),
    'Anywhere Pow': ItemData('Consumable', 0x302084, "filler", 0),
    'Winged Cloud Maker': ItemData('Consumable', 0x302085, "filler", 0),
    'Pocket Melon': ItemData('Consumable', 0x302086, "filler", 0),
    'Pocket Fire Melon': ItemData('Consumable', 0x302087, "filler", 0),
    'Pocket Ice Melon': ItemData('Consumable', 0x302088, "filler", 0),
    'Magnifying Glass': ItemData('Consumable', 0x302089, "filler", 0),
    '+10 Stars': ItemData('Consumable', 0x30208A, "useful", 0),
    '+20 Stars': ItemData('Consumable', 0x30208B, "useful", 0),
    '1-Up': ItemData('Lives', 0x30208C, "filler", 0),
    '2-Up': ItemData('Lives', 0x30208D, "filler", 0),
    '3-Up': ItemData('Lives', 0x30208E, "filler", 0),
    '10-Up': ItemData('Lives', 0x30208F, "useful", 5),
    'Bonus Consumables': ItemData('Events', None, "progression", 0),
    'Bandit Consumables': ItemData('Events', None, "progression", 0),
    'Bandit Watermelons': ItemData('Events', None, "progression", 0),

    'Fuzzy Trap': ItemData('Traps', 0x302090, "trap", 0),
    'Reversal Trap': ItemData('Traps', 0x302091, "trap", 0),
    'Darkness Trap': ItemData('Traps', 0x302092, "trap", 0),
    'Freeze Trap': ItemData('Traps', 0x302093, "trap", 0),

    'Boss Clear': ItemData('Events', None, "progression", 0),
    'Piece of Luigi': ItemData('Items', 0x302095, "progression", 0),
    'Saved Baby Luigi': ItemData('Events', None, "progression", 0)
}

filler_items: Tuple[str, ...] = (
    'Anytime Egg',
    'Anywhere Pow',
    'Winged Cloud Maker',
    'Pocket Melon',
    'Pocket Fire Melon',
    'Pocket Ice Melon',
    'Magnifying Glass',
    '+10 Stars',
    '+20 Stars',
    '1-Up',
    '2-Up',
    '3-Up'
)

trap_items: Tuple[str, ...] = (
    'Fuzzy Trap',
    'Reversal Trap',
    'Darkness Trap',
    'Freeze Trap'
)

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
