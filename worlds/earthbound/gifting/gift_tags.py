from dataclasses import dataclass
from typing import List

gift_qualities = {
    "Super Plush Bear": {"MeatShield": 3},
    "Cracked Bat": {"Weapon": 0.07},
    "Tee Ball Bat": {"Weapon": 0.14},
    "Sand Lot Bat": {"Weapon": 0.27},
    "Minor League Bat": {"Weapon": 0.48},
    "Mr. Baseball Bat": {"Weapon": 0.70},
    "Big League Bat": {"Weapon": 0.90},
    "Hall of Fame Bat": {"Weapon": 1.14},
    "Magicant Bat": {"Weapon": 1.48},
    "Legendary Bat": {"Weapon": 2.03},
    "Gutsy Bat": {"Weapon": 4.0},
    "Casey Bat": {"Weapon": 0.1},
    "T-Rex's Bat": {"Weapon": 0.88},
    "Ultimate Bat": {"Weapon": 1.25},

    "Fry Pan": {"Weapon": 0.24},
    "Thick Fry Pan": {"Weapon": 0.48},
    "Deluxe Fry Pan": {"Weapon": 0.73},
    "Chef's Fry Pan": {"Weapon": 0.97},
    "Non-Stick Frypan": {"Weapon": 1.19},
    "French Fry Pan": {"Weapon": 1.46},
    "Holy Fry Pan": {"Weapon": 1.90},
    "Magic Frypan": {"Weapon": 2.5},

    "Pop Gun": {"Weapon": 0.25},
    "Stun Gun": {"Weapon": 0.34},
    "Toy Air Gun": {"Weapon": 0.50},
    "Magnum Air Gun": {"Weapon": 0.57},
    "Zip Gun": {"Weapon": 0.63},
    "Laser Gun": {"Weapon": 0.76},
    "Hyper Beam": {"Weapon": 0.92},
    "Double Beam": {"Weapon": 1.04},
    "Crusher Beam": {"Weapon": 1.14},
    "Spectrum Beam": {"Weapon": 1.24},
    "Death Ray": {"Weapon": 1.42},
    "Baddest Beam": {"Weapon": 1.55},
    "Moon Beam Gun": {"Weapon": 1.74},
    "Gaia Beam": {"Weapon": 1.98},
    "Sword of Kings": {"Weapon": 2.00},

    "Bag of Fries": {"Heal": 0.24},
    "Banana": {"Heal": 0.22},
    "Bean Croquette": {"Heal": 0.42},
    "Beef Jerky": {"Heal": 1.50},
    "Boiled Egg": {"Heal": 0.42},
    "Bowl of Rice Gruel": {"Heal": 2.16},
    "Brain Food Lunch": {"Heal": 3.00, "Mana": 1.42},
    "Bread Roll": {"Heal": 0.30},
    "Calorie Stick": {"Heal": 0.60},
    "Can of Fruit Juice": {"Heal": 0.06},
    "Chef's Special": {"Heal": 2.16},
    "Cookie": {"Heal": 0.06},
    "Croissant": {"Heal": 0.60},
    "Cup of Coffee": {"Heal": 0.12},
    "Cup of Noodles": {"Heal": 0.42},
    "Double Burger": {"Heal": 0.96},
    "Fresh Egg": {"Heal": 0.84},
    "Hamburger": {"Heal": 0.48},
    "Kabob": {"Heal": 1.26},
    "Kraken Soup": {"Heal": 9.99},
    "Large Pizza": {"Heal": 2.40},
    "Lucky Sandwich": {"Heal": 0.60, "Mana": 0.57},
    "Luxury Jerky": {"Heal": 3.00},
    "Mammoth Burger": {"Heal": 2.05},
    "Molokheiya Soup": {"Heal": 0.84},
    "Pasta di Summers": {"Heal": 1.10},
    "Peanut Cheese Bar": {"Heal": 1.00},
    "Picnic Lunch": {"Heal": 0.80},
    "Piggy Jelly": {"Heal": 3.00},
    "Pizza": {"Heal": 1.20},
    "Plain Roll": {"Heal": 0.80},
    "Plain Yogurt": {"Heal": 1.60},
    "Popsicle": {"Heal": 0.18},
    "Protein Drink": {"Heal": 0.80},
    "Royal Iced Tea": {"Heal": 0.60},
    "Repel Sandwich": {"Heal": 0.06},
    "Repel Superwich": {"Heal": 0.06},
    "Spicy Jerky": {"Heal": 2.52},
    "Trout Yogurt": {"Heal": 0.30},
    "Hand-Aid": {"Heal": 9.99},

    "Cold Remedy": {"Cure": 0.10},
    "Vial of Serum": {"Cure": 0.25},
    "Wet Towel": {"Cure": 0.50},
    "Refreshing Herb": {"Cure": 1.00},
    "Secret Herb": {"Cure": 2.00, "Life": 0.50},
    "Horn of Life": {"Cure": 3.00, "Life": 1.00},
    "Cup of Lifenoodles": {"Cure": 3.00, "Life": 1.00},

    "Bottle of Water": {"Mana": 0.28},
    "Bottle of DXwater": {"Mana": 1.14},
    "Magic Pudding": {"Mana": 1.14},
    "Magic Tart": {"Mana": 0.57},
    "Magic Truffle": {"Mana": 2.28},
    "PSI Caramel": {"Mana": 0.57},

    "Cheap Bracelet": {"Armor": 0.12},
    "Copper Bracelet": {"Armor": 0.25},
    "Silver Bracelet": {"Armor": 0.37},
    "Gold Bracelet": {"Armor": 0.75},
    "Platinum Band": {"Armor": 1.00},
    "Diamond Band": {"Armor": 1.25},
    "Pixie's Bracelet": {"Armor": 1.50},
    "Cherub's Band": {"Armor": 1.75},
    "Goddess Band": {"Armor": 2.00},
    "Bracer of Kings": {"Armor": 0.87, "Fire": 0.50},

    "Ribbon": {"Armor": 0.35},
    "Red Ribbon": {"Armor": 0.43},
    "Defense Ribbon": {"Armor": 0.70},
    "Talisman Ribbon": {"Armor": 1.05},
    "Saturn Ribbon": {"Armor": 1.57},
    "Goddess Ribbon": {"Armor": 1.92},

    "Yo-yo": {"Weapon": 0.06},
    "Slingshot": {"Weapon": 0.12},
    "Bionic Slingshot": {"Weapon": 0.32},
    "Trick Yo-yo": {"Weapon": 0.46},
    "Combat Yo-yo": {"Weapon": 0.54},

    "Travel Charm": {"AntiNumb": 0.25},
    "Great Charm": {"Armor": 0.01, "AntiNumb": 0.50},
    "Crystal Charm": {"Armor": 0.02, "AntiNumb": 1.00},
    "Rabbit's Foot": {"Armor": 0.03, "AntiNumb": 1.00, "Speed": 2.00},

    "Flame Pendant": {"Armor": 1.00, "Fire": 1.00},
    "Rain Pendant": {"Armor": 1.00, "Ice": 1.00},
    "Night Pendant": {"Armor": 1.00, "Light": 1.00},
    "Sea Pendant": {"Armor": 2.00, "Fire": 1.00, "Ice": 1.00, "Light": 1.00},
    "Star Pendant": {"Armor": 3.00, "Fire": 1.00, "Ice": 1.00, "Light": 1.00, "AntiNumb": 1.00},
    "Earth Pendant": {"Armor": 1.50, "Fire": 0.50, "Ice": 0.50, "Light": 0.50},
    "Cloak of Kings": {"Armor": 0.50},

    "Shield Killer": {"Neutralizing": 0.50},
    "Neutralizer": {"Neutralizing": 1.00},
    "HP-Sucker": {"Draining": 0.50},
    "Hungry HP-Sucker": {"Draining": 1.00},

    "Baseball Cap": {"Armor": 0.13},
    "Holmes Hat": {"Armor": 0.27},
    "Mr. Baseball Cap": {"Armor": 0.16},
    "Hard Hat": {"Armor": 0.41},
    "Coin of Slumber": {"Armor": 0.83},
    "Coin of Defense": {"Armor": 1.11},
    "Lucky Coin": {"Armor": 1.38},
    "Talisman Coin": {"Armor": 1.66},
    "Shiny Coin": {"Armor": 1.94},
    "Souvenir Coin": {"Armor": 2.22},
    "Coin of Silence": {"Armor": 1.25},
    "Mr. Saturn Coin": {"Armor": 1.30},
    "Diadem of Kngs": {"Armor": 0.50, "Fire": 0.25, "Ice": 0.25, "Light": 0.25, "AntiNumb": 0.25}
} 


@dataclass
class EarthBoundGift:
    name: str
    value: int
    traits: list[str]


def make_trait(trait: str, name: str) -> dict[str, str | int]:
    if name in gift_qualities and trait in gift_qualities[name]:
        quality = gift_qualities[name][trait]
    else:
        quality = None

    if quality:
        return {"trait": trait, "quality": quality}
    else:
        return {"trait": trait}


def make_default_traits(traits: list[str], name: str) -> list[dict[str, str | int]]:
    return [make_trait(trait, name) for trait in traits]


def create_gift(name: str, value: int, traits: list[str]) -> EarthBoundGift:
    """Create a Gift with the specified tag and values."""
    return EarthBoundGift(name, value, make_default_traits(traits, name))


gift_properties = {
    2: create_gift("Teddy Bear", 178, ["Toy", "Doll"]),

    3: create_gift("Super Plush Bear", 1198, ["Toy", "Doll"]),

    4: create_gift("Broken Machine", 0, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    5: create_gift("Broken Gadget", 109, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    6: create_gift("Broken Air Gun", 0, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    7: create_gift("Broken Spray Can", 189, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    8: create_gift("Broken Laser", 0, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    9: create_gift("Broken Iron", 149, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    10: create_gift("Broken Pipe", 149, ["Broken", "Machine", "Metal", "Material", "Resource", "Pipe", "Trash"]),

    11: create_gift("Broken Cannon", 218, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    12: create_gift("Broken Tube", 0, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    13: create_gift("Broken Bazooka", 0, ["Broken", "Machine", "Metal", "Material", "Resource", "Weapon", "Trash"]),

    14: create_gift("Broken Trumpet", 0, ["Broken", "Machine", "Metal", "Material", "Resource", "Instrument",
                                          "Trash"]),

    15: create_gift("Broken Harmonica", 0, ["Broken", "Machine", "Metal", "Material", "Resource", "Instrument",
                                            "Trash"]),

    16: create_gift("Broken Antenna", 0, ["Broken", "Machine", "Metal", "Material", "Resource", "Trash"]),

    17: create_gift("Cracked Bat", 18, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    18: create_gift("Tee Ball Bat", 48, ["MeleeWeapon", "Metal", "Toy", "Weapon"]),

    19: create_gift("Sand Lot Bat", 98, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    20: create_gift("Minor League Bat", 399, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    21: create_gift("Mr. Baseball Bat", 498, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    22: create_gift("Big League Bat", 3080, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    23: create_gift("Hall of Fame Bat", 1880, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    24: create_gift("Magicant Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Dreamlike"]),

    25: create_gift("Legendary Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Legendary"]),

    26: create_gift("Gutsy Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon", "Guts"]),

    27: create_gift("Casey Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    28: create_gift("Fry Pan", 0, ["MeleeWeapon", "Metal", "Tool", "Weapon"]),

    29: create_gift("Thick Fry Pan", 0, ["MeleeWeapon", "Metal", "Tool", "Weapon"]),

    30: create_gift("Deluxe Fry Pan", 0, ["MeleeWeapon", "Metal", "Tool", "Weapon"]),

    31: create_gift("Chef's Fry Pan", 0, ["MeleeWeapon", "Metal", "Tool", "Weapon"]),

    32: create_gift("French Fry Pan", 0, ["MeleeWeapon", "Metal", "Tool", "Weapon"]),

    33: create_gift("Magic Fry Pan", 0, ["MeleeWeapon", "Metal", "Tool", "Weapon"]),

    34: create_gift("Holy Fry Pan", 0, ["MeleeWeapon", "Metal", "Tool", "Weapon"]),

    35: create_gift("Sword of Kings", 0, ["Weapon"]),

    36: create_gift("Pop Gun", 0, ["RangedWeapon", "Toy", "Weapon"]),

    37: create_gift("Stun Gun", 0, ["RangedWeapon", "Weapon"]),

    38: create_gift("Toy Air Gun", 0, ["RangedWeapon", "Toy", "Weapon"]),

    39: create_gift("Magnum Air Gun", 0, ["RangedWeapon", "Toy", "Weapon"]),

    40: create_gift("Zip Gun", 0, ["RangedWeapon", "Toy", "Weapon"]),

    41: create_gift("Laser Gun", 0, ["RangedWeapon", "Beam", "Weapon"]),

    42: create_gift("Hyper Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),

    43: create_gift("Crusher Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),
    
    44: create_gift("Spectrum Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),

    45: create_gift("Death Ray", 0, ["RangedWeapon", "Beam", "Weapon"]),

    46: create_gift("Baddest Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),

    47: create_gift("Moon Beam Gun", 0, ["RangedWeapon", "Beam", "Weapon"]),

    48: create_gift("Gaia Beam", 0, ["RangedWeapon", "Beam", "Weapon"]),

    49: create_gift("Yo-yo", 0, ["RangedWeapon", "Toy", "Weapon"]),

    50: create_gift("Slingshot", 0, ["RangedWeapon", "Toy", "Weapon"]),

    51: create_gift("Bionic Slingshot", 0, ["RangedWeapon", "Toy", "Weapon"]),

    52: create_gift("Trick Yo-yo", 0, ["RangedWeapon", "Toy", "Weapon"]),

    53: create_gift("Combat Yo-yo", 0, ["RangedWeapon", "Toy", "Weapon"]),

    54: create_gift("Travel Charm", 0, ["Jewelry"]),

    55: create_gift("Great Charm", 0, ["Jewelry", "Defense", "Armor"]),

    56: create_gift("Crystal Charm", 0, ["Jewelry", "Defense", "Armor", "Crystal"]),

    57: create_gift("Rabbit's Foot", 0, ["Armor", "Jewelry", "Defense", "Speed"]),

    58: create_gift("Flame Pendant", 0, ["Armor", "Jewelry", "Defense", "Fire"]),

    59: create_gift("Rain Pendant", 0, ["Armor", "Jewelry", "Defense", "Water"]),

    60: create_gift("Night Pendant", 0, ["Armor", "Jewelry", "Defense", "Light"]),

    61: create_gift("Sea Pendant", 0, ["Armor", "Jewelry", "Defense", "Light", "Fire", "Water"]),

    62: create_gift("Star Pendant", 0, ["Armor", "Jewelry", "Defense", "Light", "Fire", "Water"]),

    63: create_gift("Cloak of Kings", 0, ["Armor", "Jewelry", "Defense"]),

    64: create_gift("Cheap Bracelet", 0, ["Armor", "Jewelry", "Defense", "Plastic"]),

    65: create_gift("Copper Bracelet", 0, ["Armor", "Jewelry", "Defense", "Copper"]),

    66: create_gift("Silver Bracelet", 0, ["Armor", "Jewelry", "Defense", "Silver"]),

    67: create_gift("Gold Bracelet", 0, ["Armor", "Jewelry", "Defense", "Gold"]),

    68: create_gift("Platinum Band", 0, ["Armor", "Jewelry", "Defense", "Platinum"]),

    69: create_gift("Diamond Band", 0, ["Armor", "Jewelry", "Defense", "Diamond"]),

    70: create_gift("Pixie's Bracelet", 0, ["Armor", "Jewelry", "Defense"]),

    71: create_gift("Cherub's Band", 0, ["Armor", "Jewelry", "Defense"]),

    72: create_gift("Goddess Band", 0, ["Armor", "Jewelry", "Defense"]),

    73: create_gift("Bracer of Kings", 0, ["Armor", "Jewelry", "Defense", "Fire"]),

    74: create_gift("Baseball Cap", 0, ["Armor", "Baseball", "Defense", "Hat"]),

    75: create_gift("Holmes Hat", 0, ["Armor", "Defense", "Hat"]),

    76: create_gift("Mr. Baseball Cap", 0, ["Armor", "Defense", "Hat", "Baseball"]),

    77: create_gift("Hard Hat", 0, ["Armor", "Defense", "Hat"]),

    78: create_gift("Ribbon", 0, ["Armor", "Cloth", "Defense"]),

    79: create_gift("Red Ribbon", 0, ["Armor", "Cloth", "Defense", "Red"]),

    80: create_gift("Goddess Ribbon", 0, ["Armor", "Cloth", "Defense"]),

    81: create_gift("Coin of Slumber", 0, ["Armor", "Defense"]),

    82: create_gift("Coin of Defense", 0, ["Armor", "Defense"]),

    83: create_gift("Lucky Coin", 0, ["Armor", "Defense", "Luck"]),

    84: create_gift("Talisman Coin", 0, ["Armor", "Defense"]),

    85: create_gift("Shiny Coin", 0, ["Armor", "Defense"]),

    86: create_gift("Souvenir Coin", 0, ["Armor", "Defense"]),

    87: create_gift("Diadem of Kings", 0, ["Armor", "Jewelry", "Defense", "Fire", "Water", "Light"]),

    88: create_gift("Cookie", 7, ["Confectionary", "Comsumable", "Heal", "Food"]),

    89: create_gift("Bag of Fries", 8, ["FastFood", "Comsumable", "Heal", "Food"]),

    90: create_gift("Hamburger", 14, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Meat"]),

    91: create_gift("Boiled Egg", 0, ["Egg", "Comsumable", "Heal", "Food", "White"]),

    92: create_gift("Fresh Egg", 0, ["Egg", "Comsumable", "Heal", "Food", "White"]),

    93: create_gift("Picnic Lunch", 24, ["Comsumable", "Heal", "Food"]),

    94: create_gift("Pasta di Summers", 0, ["Pasta", "Comsumable", "Heal", "Food", "Cooking"]),

    95: create_gift("Pizza", 0, ["Comsumable", "Heal", "Food"]),

    96: create_gift("Chef's Special", 0, ["Comsumable", "Heal", "Food"]),

    97: create_gift("Large Pizza", 0, ["Comsumable", "Heal", "Food"]),

    98: create_gift("PSI Caramel", 0, ["Comsumable", "Mana", "Food", "Candy"]),

    99: create_gift("Magic Truffle", 0, ["Comsumable", "Mana", "Food", "Candy"]),

    100: create_gift("Brain Food Lunch", 0, ["Comsumable", "Mana", "Food", "Heal", "ExoticFood"]),

    101: create_gift("Rock Candy", 0, ["Comsumable", "Candy", "Food", "Buff"]),

    102: create_gift("Croissant", 0, ["Comsumable", "Food", "Heal", "Bread"]),

    103: create_gift("Bread Roll", 0, ["Comsumable", "Food", "Heal", "Bread"]),

    106: create_gift("Can of Fruit Juice", 0, ["Comsumable", "Heal", "Drink", "Liquid", "Fruit", "Juice"]),

    107: create_gift("Royal Iced Tea", 0, ["Comsumable", "Heal", "Drink", "Liquid"]),

    108: create_gift("Protein Drink", 0, ["Comsumable", "Heal", "Drink", "Liquid"]),

    109: create_gift("Kraken Soup", 0, ["Comsumable", "Heal", "Food", "Liquid", "Cooking"]),

    110: create_gift("Bottle of Water", 0, ["Comsumable", "Mana", "Drink", "Liquid", "Water"]),

    111: create_gift("Cold Remedy", 0, ["Comsumable", "Medicine", "Drink", "Liquid", "Cure"]),

    112: create_gift("Vial of Serum", 0, ["Comsumable", "Medicine", "Drink", "Liquid", "Cure"]),

    113: create_gift("IQ Capsule", 0, ["Comsumable", "Medicine", "IQ", "Buff"]),

    114: create_gift("Guts Capsule", 0, ["Comsumable", "Medicine", "Guts", "Buff"]),

    115: create_gift("Speed Capsule", 0, ["Comsumable", "Medicine", "Speed", "Buff"]),

    116: create_gift("Vital Capsule", 0, ["Comsumable", "Medicine", "Buff", "Life"]),

    117: create_gift("Luck Capsule", 0, ["Comsumable", "Medicine", "Buff", "Luck"]),

    118: create_gift("Ketchup Packet", 0, ["Comsumable", "Heal", "Food", "Condiment", "Red"]),

    119: create_gift("Sugar Packet", 0, ["Comsumable", "Heal", "Food", "Condiment", "White"]),

    120: create_gift("Tin of Cocoa", 0, ["Comsumable", "Heal", "Food", "Condiment", "Brown", "Chocolate"]),

    121: create_gift("Carton of Cream", 0, ["Comsumable", "Heal", "Food", "Condiment", "White", "Liquid"]),

    122: create_gift("Sprig of Parsley", 0, ["Comsumable", "Heal", "Food", "Condiment", "Green", "Plant"]),

    123: create_gift("Jar of Hot Sauce", 0, ["Comsumable", "Heal", "Food", "Condiment", "Orange", "Spicy"]),

    124: create_gift("Salt Packet", 0, ["Comsumable", "Heal", "Food", "Condiment", "White", "Salted"]),

    126: create_gift("Jar of Delisauce", 0, ["Comsumable", "Heal", "Food", "Condiment", "Green"]),

    127: create_gift("Wet Towel", 0, ["Comsumable", "Cure"]),

    128: create_gift("Refreshing Herb", 0, ["Comsumable", "Cure", "Food", "Herb"]),

    129: create_gift("Secret Herb", 0, ["Comsumable", "Cure", "Food", "Life", "Herb"]),

    130: create_gift("Horn of Life", 0, ["Comsumable", "Cure", "Life"]),

    131: create_gift("Counter-PSI Unit", 0, ["Machine", "Electronics", "Metal"]),

    132: create_gift("Shield Killer", 0, ["Machine", "Electronics", "Metal", "Neutralizing"]),

    133: create_gift("Bazooka", 0, ["Machine", "Weapon", "Electronics", "Explosive", "RangedWeapon"]),

    134: create_gift("Heavy Bazooka", 0, ["Machine", "Weapon", "Electronics", "Explosive", "RangedWeapon"]),

    135: create_gift("HP-Sucker", 0, ["Machine", "Draining", "Electronics"]),

    136: create_gift("Hungry HP-Sucker", 0, ["Machine", "Draining", "Electronics"]),

    137: create_gift("Xterminator Spray", 0, ["Can", "Metal", "Insect", "Weapon", "Chemicals"]),

    138: create_gift("Slime Generator", 0, ["Machine", "Slime", "Electronics"]),

    140: create_gift("Ruler", 0, ["Long", "Wood", "Trash", "IQ"]),

    141: create_gift("Snake Bag", 0, ["Animal", "Container", "Throwing"]),

    142: create_gift("Mummy Wrap", 0, ["Ancient", "Paper", "Weapon", "Throwing", "Consumable"]),

    143: create_gift("Protractor", 0, ["Metal", "Trash", "IQ"]),

    144: create_gift("Bottle Rocket", 0, ["Weapon", "Explosive", "Rocket", "Fireworks", "Consumable"]),

    145: create_gift("Big Bottle Rocket", 0, ["Weapon", "Explosive", "Rocket", "Fireworks", "Consumable"]),

    146: create_gift("Multi Bottle Rocket", 0, ["Weapon", "Explosive", "Rocket", "Fireworks", "Consumable"]),

    147: create_gift("Bomb", 0, ["Weapon", "Explosive", "Throwing", "Consumable", "Bomb"]),

    148: create_gift("Super Bomb", 0, ["Weapon", "Explosive", "Throwing", "Consumable", "Bomb"]),

    149: create_gift("Insecticide Spray", 0, ["Can", "Metal", "Insect", "Weapon", "Consumable", "Chemicals"]),

    150: create_gift("Rust Promoter", 0, ["Can", "Metal", "Rusting", "Weapon", "Consumable", "Chemicals"]),

    151: create_gift("Rust Promoter DX", 0, ["Can", "Metal", "Rusting", "Weapon", "Consumable", "Chemicals", "Insect"]),

    152: create_gift("Pair of Dirty Socks", 0, ["Consumable", "Throwing", "Stinky", "Clothing"]),

    153: create_gift("Stag Beetle", 0, ["Consumable", "Throwing", "Animal", "Insect"]),

    154: create_gift("Toothbrush", 0, ["Consumable", "Tool"]),

    155: create_gift("Handbag Strap", 0, ["Consumable", "Weapon", "Throwing", "Leather"]),

    156: create_gift("Pharaoh's Curse", 0, ["Consumable", "Weapon", "Throwing", "Goo", "Slime", "Poison", "Chemicals"]),

    157: create_gift("Defense Shower", 0, ["Can", "Machine", "Chemicals", "Buff", "Defense", "Liquid"]),

    159: create_gift("Sudden Guts Pill", 0, ["Consumable", "Guts", "Buff"]),

    160: create_gift("Bag of Dragonite", 0, ["Consumable", "Weapon", "Powder"]),

    161: create_gift("Defense Spray", 0, ["Can", "Consumable", "Chemicals", "Buff", "Defense", "Liquid"]),

    165: create_gift("Picture Postcard", 0, ["Paper", "Trash"]),

    168: create_gift("Chick", 0, ["Animal", "Yellow", "Chicken"]),

    169: create_gift("Chicken", 0, ["Animal", "White", "Chicken"]),

    186: create_gift("Meteotite", 0, ["Mineral", "Artifact", "Brown", "Gem"]),

    188: create_gift("Hand-Aid", 0, ["Consumable", "Heal", "Cloth"]),

    189: create_gift("Trout Yogurt", 0, ["Consumable", "Heal", "Food", "Fish", "Dairy"]),

    190: create_gift("Banana", 0, ["Consumable", "Heal", "Food", "Fruit", "Yellow"]),

    191: create_gift("Calorie Stick", 0, ["Consumable", "Heal", "Food", "Jerky"]),

    194: create_gift("Earth Pendant", 0, ["Armor", "Jewelry", "Fire", "Ice", "Light"]),

    195: create_gift("Neutralizer", 0, ["Machine", "Electronics", "Metal", "Neutralizing"]),

    198: create_gift("Gelato de Resort", 0, ["Consumable", "Food", "Heal", "Dairy", "FrozenFood"]),

    199: create_gift("Snake", 0, ["Animal", "Weapon", "Throwing", "Consumable"]),

    200: create_gift("Viper", 0, ["Animal", "Weapon", "Throwing", "Poison", "Consumable"]),

    201: create_gift("Brain Stone", 0, ["Stone", "Mineral", "Trash"]),

    207: create_gift("Magic Tart", 0, ["Food", "Consumable", "Mana", "Confectionary"]),

    209: create_gift("Monkey's Love", 0, ["Weapon", "Animal"]),

    212: create_gift("T-Rex's Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    213: create_gift("Big League Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    214: create_gift("Ultimate Bat", 0, ["MeleeWeapon", "Wood", "Baseball", "Toy", "Weapon"]),

    215: create_gift("Double Beam", 0, ["RangedWeapon", "Gun", "Beam", "Weapon"]),

    216: create_gift("Platinum Band", 0, ["Armor", "Defense", "Platinum", "Jewelry"]),

    217: create_gift("Diamond Band", 0, ["Armor", "Defense", "Diamond", "Jewelry"]),

    218: create_gift("Defense Ribbon", 0, ["Armor", "Cloth", "Defense"]),

    219: create_gift("Talisman Ribbon", 0, ["Armor", "Cloth", "Defense"]),

    220: create_gift("Saturn Ribbon", 0, ["Armor", "Cloth", "Defense"]),

    221: create_gift("Coin of Silence", 0, ["Armor", "Defense"]),

    222: create_gift("Charm Coin", 0, ["Armor", "Defense"]),

    223: create_gift("Cup of Noodles", 0, ["Food", "Consumable", "Heal", "FastFood", "Pasta"]),

    224: create_gift("Repel Sandwich", 0, ["Food", "Consumable", "Heal", "Repellant", "Sandwich"]),

    225: create_gift("Repel Superwich", 0, ["Food", "Consumable", "Heal", "Repellant", "Sandwich"]),

    226: create_gift("Lucky Sandwich", 0, ["Food", "Consumable", "Heal", "Luck", "Mana", "Sandwich"]),

    232: create_gift("Cup of Coffee", 0, ["Drink", "Consumable", "Heal", "Liquid", "Coffee"]),

    233: create_gift("Double Burger", 0, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Meat"]),

    234: create_gift("Peanut Cheese Bar", 0, ["Comsumable", "Heal", "Food", "Candy", "ExoticFood"]),

    235: create_gift("Piggy Jelly", 0, ["Comsumable", "Heal", "Food", "ExoticFood", "Gelatin", "Jelly"]),

    236: create_gift("Bowl of Rice Gruel", 0, ["Comsumable", "Heal", "Food", "Cooking", "ExoticFood", "Liquid"]),

    237: create_gift("Bean Croquette", 0, ["Comsumable", "Heal", "Food", "Cooking", "ExoticFood"]),

    238: create_gift("Molokheiya Soup", 0, ["Comsumable", "Heal", "Food", "Cooking", "ExoticFood", "Vegetable",
                                            "Liquid"]),

    239: create_gift("Plain Roll", 0, ["Comsumable", "Heal", "Food", "Bread"]),

    240: create_gift("Kabob", 0, ["Comsumable", "Heal", "Food", "ExoticFood", "Meat"]),

    241: create_gift("Plain Yogurt", 0, ["Comsumable", "Heal", "Food", "Slime", "Dairy"]),

    242: create_gift("Beef Jerky", 0, ["Comsumable", "Heal", "Food", "Meat", "Dried", "Jerky"]),

    243: create_gift("Mammoth Burger", 0, ["FastFood", "Comsumable", "Heal", "Food", "Beef", "Meat"]),

    244: create_gift("Spicy Jerky", 0, ["Comsumable", "Heal", "Food", "Meat", "Dried", "Jerky", "Spicy"]),

    245: create_gift("Luxury Jerky", 0, ["Comsumable", "Heal", "Food", "Meat", "Dried", "Jerky", "Luxury"]),

    246: create_gift("Bottle of DXwater", 0, ["Comsumable", "Mana", "Drink", "Liquid", "Water"]),

    247: create_gift("Magic Pudding", 0, ["Comsumable", "Mana", "Food", "Candy"]),

    248: create_gift("Non-Stick Frypan", 0, ["MeleeWeapon", "Metal", "Tool", "Weapon"]),

    249: create_gift("Mr. Saturn Coin", 0, ["Armor", "Defense"]),

    250: create_gift("Meteornium", 0, ["Mineral", "Artifact", "SpaceMineral"]),

    251: create_gift("Popsicle", 0, ["Consumable", "Food", "Heal", "FrozenFood"]),

    252: create_gift("Cup of Lifenoodles", 0, ["Consumable", "Food", "Cure", "Life", "Pasta"])
    # Todo; separate traits for GoodWeapon and BadWeapon
    # Todo; Satus heals should be Medicine, Cure
}
