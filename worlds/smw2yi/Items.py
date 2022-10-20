from typing import Dict, Set, Tuple, NamedTuple

class ItemData(NamedTuple):
    category: str
    code: int
    count: int = 1
    progression: bool = False
    useful: bool = False
    trap: bool = False

item_table: Dict[str, ItemData] = {
    'Spring Ball': ItemData('Sprites', 16001, progression=True),
    'Large Spring Ball': ItemData('Sprites', 16002, progression=True),
    '! Switch': ItemData('Sprites', 16003, progression=True),
    'Dashed Platform': ItemData('Sprites', 16004, progression=True),
    'Dashed Stairs': ItemData('Sprites', 16005, progression=True),
    #'Spring Ball': ItemData('Sprites', 16006, progression=True),
    'Beanstalk': ItemData('Sprites', 16007, progression=True),
    'Helicopter': ItemData('Sprites', 16008, progression=True),
    'Mole Tank': ItemData('Sprites', 16009, progression=True),
    'Car': ItemData('Sprites', 16010, progression=True),
    'Submarine': ItemData('Sprites', 16011, progression=True),
    'Train': ItemData('Sprites', 16012, progression=True),
    'Arrow Wheel': ItemData('Sprites', 16013, progression=True),
    'Vanishing Arrow Wheel': ItemData('Sprites', 16014, progression=True),
    'Watermelons': ItemData('Sprites', 16015, progression=True),
    'Fire Melons': ItemData('Sprites', 16016, progression=True),
    'Ice Melons': ItemData('Sprites', 16017, progression=True),
    'Super Star': ItemData('Sprites', 16018, progression=True),
    'Flashing Eggs': ItemData('Sprites', 16019, progression=True),
    'Giant Eggs': ItemData('Sprites', 16020, progression=True),
    'Egg Launcher': ItemData('Sprites', 16021, progression=True),
    'Egg Plant': ItemData('Sprites', 16022, progression=True),
    'Chomp Rock': ItemData('Sprites', 16023, progression=True),
    'Poochy': ItemData('Sprites', 16024, progression=True),
    'Platform Ghost': ItemData('Sprites', 16025, progression=True),
    'Skis': ItemData('Sprites', 16026, progression=True),
    'Key': ItemData('Key', 16027, progression=True),
    'Middle Ring': ItemData('Sprites', 16028, progression=True),
    'Tulip': ItemData('Sprites', 16029, progression=True),
    'Bucket': ItemData('Sprites', 16030, progression=True),
    #Huffin Puffin: ItemData('Sprites', 16031)
    'Bonus 1': ItemData('Panels', 16031, progression=True),
    'Bonus 2': ItemData('Panels', 16032, useful=True),
    'Bonus 3': ItemData('Panels', 16033, useful=True),
    'Bonus 4': ItemData('Panels', 16034, progression=True),
    'Bonus 5': ItemData('Panels', 16035, useful=True),
    'Bonus 6': ItemData('Panels', 16036, useful=True),
    'Bonus Panels': ItemData('Panels', 16037, progression=True),
    'Extra Panels': ItemData('Panels', 16038, progression=True),
    'Extra 1': ItemData('Panels', 16039, progression=True),
    'Extra 2': ItemData('Panels', 16040, progression=True),
    'Extra 3': ItemData('Panels', 16041, progression=True),
    'Extra 4': ItemData('Panels', 16042, progression=True),
    'Extra 5': ItemData('Panels', 16043, progression=True),
    'Extra 6': ItemData('Panels', 16044, progression=True),
    'Egg Capacity Upgrade': ItemData('Abilities', 16045, 5, progression=True),
    #'Spikebreaker Eggs': ItemData('Abilities', 16046, progression=True),
    #'Flutter Jump': ItemData('Abilities', 16047, progression=True),
    #'Ground Pound': ItemData('Abilities', 16048, progression=True),
    #'Egg Strength Upgrade': ItemData('Abilities', 16049, progression=True),
    'Secret Lens': ItemData('Abilities', 16050, progression=True),
    #'Waterskipper Eggs': ItemData('Abilities), 16051, progression=True,
    #'Pushing': ItemData('Abilities'), 160522,
    'World 1 Gate': ItemData('Gates', 16051, progression=True),
    'World 2 Gate': ItemData('Gates', 16052, progression=True),
    'World 3 Gate': ItemData('Gates', 16053, progression=True),
    'World 4 Gate': ItemData('Gates', 16054, progression=True),
    'World 5 Gate': ItemData('Gates', 16055, progression=True),
    'World 6 Gate': ItemData('Gates', 16056, progression=True),
    'Anytime Egg': ItemData('Consumables', 16057),
    'Anywhere Pow': ItemData('Consumables', 16058),
    'Winged Cloud Maker': ItemData('Consumables', 16059),
    'Pocket Melon': ItemData('Consumables', 16060),
    'Pocket Fire Melon': ItemData('Consumables', 16061),
    'Pocket Ice Melon': ItemData('Consumables', 16062),
    'Magnifying Glass': ItemData('Consumables', 16063),
    '+10 Stars': ItemData('Consumables', 16064),
    '+20 Stars': ItemData('Consumables', 16065),
    #'World 1 Key': ItemData('Keys', 16066, 4, progression=True),
    #'World 2 Key': ItemData('Keys', 16067, 7, progression=True),
    #'World 3 Key': ItemData('Keys', 16068, 3, progression=True),
    #'World 4 Key': ItemData('Keys', 16069, 8, progression=True),
    #'World 5 Key': ItemData('Keys', 16070, 2, progression=True),
    #'World 6 Key': ItemData('Keys', 16071, 5, progression=True),
    '1-Up': ItemData('Consumables', 16072),
    '2-Up': ItemData('Consumables', 16073),
    '3-Up': ItemData('Consumables', 16074),
    '10-Up': ItemData('Consumables', 16075, 5, useful=True),
    'Fuzzy Trap': ItemData('Traps', 16076, trap=True),
    'Reversal Trap': ItemData('Traps', 16077, trap=True),
    'Darkness Trap': ItemData('Traps', 16078, trap=True),
    'Freeze Trap': ItemData('Traps', 16079, trap=True),
    '-10 Stars': ItemData('Traps', 16080, trap=True),
    '-20 Stars': ItemData('Traps', 16081, trap=True),
    'World Flag': ItemData('Goals', 16082, 0, progression=True)

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
    '-10 Stars',
    '-20 Stars'
)



def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        categories.setdefault(data.category, set()).add(name)

    return categories