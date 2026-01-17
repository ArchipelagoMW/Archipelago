from . import Rom

espers = Rom.espers

characters = Rom.characters

items = list(Rom.item_name_id.keys())
""" inventory items """
item_name_weight = {v[0]: v[1] for _k, v in Rom.item_id_name_weight.items()}
""" call .get(item) to get the chest item tier weight """

all_items = [*espers, *characters, *items]
""" espers, characters, and inventory items """

item_table = {name: index for index, name in enumerate(all_items)}

good_items = [
    'Marvel Shoes',
    'Cat Hood',
    'Snow Muffler',
    'Gem Box',
    'ValiantKnife',
    'Fixed Dice',
    'Offering',
    'Ragnarok Sword',
    'Minerva',
    'Exp. Egg',
    'Illumina',
    'Paladin Shld',
    "Pearl Lance",
    "Aura Lance",
    "Magus Rod",
    "Aegis Shld",
    "Flame Shld",
    "Ice Shld",
    "Thunder Shld",
    "Genji Shld",
    "Force Shld",
    "Red Cap",
    "Genji Helmet",
    "Force Armor",
    "Genji Armor",
    "BehemothSuit",
    "Economizer",
    "Genji Glove",
    "Dragon Horn"
]

stronger_items = [
    "ValiantKnife",
    "Illumina",
    "Ragnarok",
    "Atma Weapon",
    "Aura Lance",
    "Fixed Dice",
    "Flame Shld",
    "Ice Shld",
    "Thunder Shld",
    "Paladin Shld",
    "Force Shld",
    "Cat Hood",
    "Force Armor",
    "Minerva",
    "BehemothSuit",
    "Snow Muffler",
    "Genji Glove",
    "Offering",
    "Dragon Horn",
    "Exp. Egg",
]

premium_items = [
    "ValiantKnife",
    "Illumina",
    "Ragnarok",
    "Atma Weapon",
    "Fixed Dice",
    "Flame Shld",
    "Ice Shld",
    "Thunder Shld",
    "Paladin Shld",
    "Minerva",
    "Genji Glove",
    "Offering",
    "Exp. Egg",
]
