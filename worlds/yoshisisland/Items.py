from typing import Dict, Set, Tuple, NamedTuple, Optional

class ItemData(NamedTuple):
    category: str
    code: int
    amount: Optional[int] = 1
    progression: bool = False
    progression_skip_balancing: bool = False
    useful: bool = False
    trap: bool = False

item_table: Dict[str, ItemData] = {
    '! Switch': ItemData('Items', 0x302050, progression=True),
    'Dashed Platform': ItemData('Items', 0x302051, progression=True),
    'Dashed Stairs': ItemData('Items', 0x302052, progression=True),
    'Beanstalk': ItemData('Items', 0x302053, progression=True),
    'Helicopter Morph': ItemData('Morphs', 0x302054, progression=True),
    'Spring Ball': ItemData('Items', 0x302055, progression=True),
    'Large Spring Ball': ItemData('Items', 0x302056, progression=True),
    'Arrow Wheel': ItemData('Items', 0x302057, progression=True),
    'Vanishing Arrow Wheel': ItemData('Items', 0x302058, progression=True),
    'Mole Tank Morph': ItemData('Morphs', 0x302059, progression=True),
    'Watermelon': ItemData('Items', 0x30205A, progression=True),
    'Ice Melon': ItemData('Items', 0x30205B, progression=True),
    'Fire Melon': ItemData('Items', 0x30205C, progression=True),
    'Super Star': ItemData('Items', 0x30205D, progression=True),
    'Car Morph': ItemData('Morphs', 0x30205E, progression=True),
    'Flashing Eggs': ItemData('Items', 0x30205F, progression=True),
    'Giant Eggs': ItemData('Items', 0x302060, progression=True),
    'Egg Launcher': ItemData('Items', 0x302061, progression=True),
    'Egg Plant': ItemData('Items', 0x302062, progression=True),
    'Submarine Morph': ItemData('Morphs', 0x302063, progression=True),
    'Chomp Rock': ItemData('Items', 0x302064, progression=True),
    'Poochy': ItemData('Items', 0x302065, progression=True),
    'Platform Ghost': ItemData('Items', 0x302066, progression=True),
    'Skis': ItemData('Items', 0x302067, progression=True),
    'Train Morph': ItemData('Morphs', 0x302068, progression=True),
    'Key': ItemData('Items', 0x302069, progression=True),
    'Middle Ring': ItemData('Items', 0x30206A, progression=True),
    'Bucket': ItemData('Items', 0x30206B, progression=True),
    'Tulip': ItemData('Items', 0x30206C, progression=True),
    'Egg Capacity Upgrade': ItemData('Items', 0x30206D, 5, progression=True),
    'Secret Lens': ItemData('Items', 0x302081, progression=True),

    'World 1 Gate': ItemData('Gates', 0x30206E, progression=True),
    'World 2 Gate': ItemData('Gates', 0x30206F, progression=True),
    'World 3 Gate': ItemData('Gates', 0x302070, progression=True),
    'World 4 Gate': ItemData('Gates', 0x302071, progression=True),
    'World 5 Gate': ItemData('Gates', 0x302072, progression=True),
    'World 6 Gate': ItemData('Gates', 0x302073, progression=True),

    'Extra 1': ItemData('Panels', 0x302074, progression=True),
    'Extra 2': ItemData('Panels', 0x302075, progression=True),
    'Extra 3': ItemData('Panels', 0x302076, progression=True),
    'Extra 4': ItemData('Panels', 0x302077, progression=True),
    'Extra 5': ItemData('Panels', 0x302078, progression=True),
    'Extra 6': ItemData('Panels', 0x302079, progression=True),
    'Extra Panels': ItemData('Panels', 0x30207A, progression=True),

    'Bonus 1': ItemData('Panels', 0x30207B, progression=True),
    'Bonus 2': ItemData('Panels', 0x30207C, progression=True),
    'Bonus 3': ItemData('Panels', 0x30207D, progression=True),
    'Bonus 4': ItemData('Panels', 0x30207E, progression=True),
    'Bonus 5': ItemData('Panels', 0x30207F, progression=True),
    'Bonus 6': ItemData('Panels', 0x302080, progression=True),
    'Bonus Panels': ItemData('Panels', 0x302082, progression=True),

    'Anytime Egg': ItemData('Consumable', 0x302083, 0, useful=True),
    'Anywhere Pow': ItemData('Consumable', 0x302084, 0),
    'Winged Cloud Maker': ItemData('Consumable', 0x302085, 0),
    'Pocket Melon': ItemData('Consumable', 0x302086, 0),
    'Pocket Fire Melon': ItemData('Consumable', 0x302087, 0),
    'Pocket Ice Melon': ItemData('Consumable', 0x302088, 0),
    'Magnifying Glass': ItemData('Consumable', 0x302089, 0),
    '+10 Stars': ItemData('Consumable', 0x30208A, 0, useful=True),
    '+20 Stars': ItemData('Consumable', 0x30208B, 0, useful=True),
    '1-Up': ItemData('Lives', 0x30208C, 0),
    '2-Up': ItemData('Lives', 0x30208D, 0),
    '3-Up': ItemData('Lives', 0x30208E, 0),
    '10-Up': ItemData('Lives', 0x30208F, 5, useful=True),
    'Bonus Consumables': ItemData('Events', None, 0, progression=True),
    'Bandit Consumables': ItemData('Events', None, 0, progression=True),
    'Bandit Watermelons': ItemData('Events', None, 0, progression=True),

    'Fuzzy Trap': ItemData('Traps', 0x302090, 0, trap=True),
    'Reversal Trap': ItemData('Traps', 0x302091, 0, trap=True),
    'Darkness Trap': ItemData('Traps', 0x302092, 0, trap=True),
    'Freeze Trap': ItemData('Traps', 0x302093, 0, trap=True),

    'Boss Clear': ItemData('Events', None, 0, progression=True),
    'Piece of Luigi': ItemData('Items', 0x302095, 0, progression=True),
    'Saved Baby Luigi': ItemData('Events', None, 0, progression=True)
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
