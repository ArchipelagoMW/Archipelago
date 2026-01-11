class ItemData:
    name: str
    game_id: int

    def __init__(self, name: str, game_id: int):
        self.name = name
        self.game_id = game_id

    def __repr__(self):
        return f"{self.name} ({hex(self.game_id)})"

all_item_data = []

gear_item_names = [
    "Dagger", "Mythril Knife", "Blind Knife", "Mage Masher", "Platina Dagger", "Main Gauche", "orichalcum",
    "Assassin Dagger", "Air Knife", "Zorlin Shape",

    "Hidden Knife", "Ninja Knife", "Short Edge", "Ninja Edge", "Spell Edge", "Sasuke Knife", "Iga Knife", "Koga Knife",

    "Broad Sword", "Long Sword", "Iron Sword", "Mythril Sword", "Blood Sword", "Coral Sword", "Ancient Sword",
    "Sleep Sword", "Platinum Sword", "Diamond Sword", "Ice Brand", "Rune Blade", "Nagrarock", "Materia Blade",

    "Defender", "Save the Queen", "Excalibur", "Ragnarok", "Chaos Blade",

    "Asura Knife", "Koutetsu Knife", "Bizzen Boat", "Murasame", "Heaven's Cloud", "Kiyomori", "Muramasa",
    "Kikuichimoji", "Masamune", "Chirijiraden",

    "Battle Axe", "Giant Axe", "Slasher",

    "Rod", "Thunder Rod", "Flame Rod", "Ice Rod", "Poison Rod", "Wizard Rod", "Dragon Rod", "Faith Rod",

    "Oak Staff", "White Staff", "Healing Staff", "Rainbow Staff", "Wizard Staff", "Gold Staff", "Mace of Zeus",
    "Sage Staff",

    "Flail", "Flame Whip", "Morning Star", "Scorpion Tail",

    "Romanda Gun", "Mythril Gun", "Stone Gun", "Blaze Gun", "Glacier Gun", "Blast Gun",

    "Bow Gun", "Night Killer", "Cross Bow", "Poison Bow", "Hunting Bow", "Gastrafitis",

    "Long Bow", "Silver Bow", "Ice Bow", "Lightning Bow", "Windslash Bow", "Mythril Bow", "Ultimus Bow", "Yoichi Bow",
    "Perseus Bow",

    "Ramia Harp", "Bloody Strings", "Fairy Harp",

    "Battle Dict", "Monster Dict", "Papyrus Plate", "Madlemgen",

    "Javelin", "Spear", "Mythril Spear", "Partisan", "Oberisk", "Holy Lance", "Dragon Whisker", "Javelin 2",

    "Cypress Rod", "Battle Bamboo", "Musk Rod", "Iron Fan", "Gokuu Rod", "Ivory Rod", "Octagon Rod", "Whale Whisker",

    "C Bag", "FS Bag", "P Bag", "H Bag",

    "Persia", "Cashmere", "Ryozan Silk",

    "Shuriken", "Magic Shuriken", "Yagyu Darkness", "Fire Ball", "Water Ball", "Lightning Ball",
    
    "Escutcheon", "Buckler", "Bronze Shield", "Round Shield", "Mythril Shield", "Gold Shield", "Ice Shield",
    "Flame Shield", "Aegis Shield", "Diamond Shield", "Platina Shield", "Crystal Shield", "Genji Shield",
    "Kaiser Plate", "Venetian Shield", "Escutcheon 2",

    "Leather Helmet", "Bronze Helmet", "Iron Helmet", "Barbuta", "Mythril Helmet", "Gold Helmet", "Cross Helmet",
    "Diamond Helmet", "Platina Helmet", "Circlet", "Crystal Helmet", "Genji Helmet", "Grand Helmet",

    "Leather Hat", "Feather Hat", "Red Hood", "Headgear", "Triangle Hat", "Green Beret", "Twist Headband",
    "Holy Miter", "Black Hood", "Golden Hairpin", "Flash Hat", "Thief Hat",

    "Cachusha", "Barette", "Ribbon",

    "Leather Armor", "Linen Cuirass", "Bronze Armor", "Chain Mail", "Mythril Armor", "Plate Mail", "Gold Armor",
    "Diamond Armor", "Platina Armor", "Carabini Mail", "Crystal Mail", "Genji Armor", "Reflect Mail", "Maximillian",

    "Clothes", "Leather Outfit", "Leather Vest", "Chain Vest", "Mythril Vest", "Adaman Vest", "Wizard Outfit",
    "Brigadine", "Judo Outfit", "Power Sleeve", "Earth Clothes", "Secret Clothes", "Black Costume", "Rubber Costume",

    "Linen Robe", "Silk Robe", "Wizard Robe", "Chameleon Robe", "White Robe", "Black Robe", "Light Robe",
    "Robe of Lords",

    "Battle Boots", "Spike Shoes", "Germinas Boots", "Rubber Shoes", "Feather Boots", "Sprint Shoes", "Red Shoes",

    "Power Wrist", "Genji Gauntlet", "Magic Gauntlet", "Bracer",

    "Reflect Ring", "Defense Ring", "Magic Ring", "Cursed Ring", "Angel Ring",

    "Diamond Armlet", "Jade Armlet", "108 Gems", "N-Kai Armlet", "Defense Armlet",

    "Small Mantle", "Leather Mantle", "Wizard Mantle", "Elf Mantle", "Dracula Mantle", "Feather Mantle",
    "Vanish Mantle",

    "Chantage", "Cherche", "Setiemson", "Salty Rage",

    "Potion", "Hi-Potion", "X-Potion", "Ether", "Hi-Ether", "Elixir", "Antidote", "Eye Drop", "Echo Grass",
    "Maiden's Kiss", "Soft", "Holy Water", "Remedy", "Phoenix Down"
]


for index, item_name in enumerate(gear_item_names, start=1):
    all_item_data.append(ItemData(item_name, index))

item_data_lookup = {item.name: item for item in all_item_data}

zodiac_stone_names = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
    "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces", "Serpentarius",
]

world_map_pass_names = [
    "Gallione Pass", "Lesalia Pass", "Fovoham Pass", "Lionel Pass", "Zeltennia Pass", "Limberry Pass", "Murond Pass"
]

job_names = [
    "Squire", "Chemist", "Knight", "Archer", "Monk", "Thief", "Lancer", "Geomancer", "Samurai", "Ninja", "Dancer",
    "Priest", "Wizard", "Oracle", "Time Mage", "Mediator", "Summoner", "Calculator", "Bard", "Mime"
]

earned_job_names = [job for job in job_names if job != "Squire"]

shop_levels = []

for i in range(14):
    shop_levels.append("Progressive Shop Level")

major_item_names = [
    *zodiac_stone_names, *world_map_pass_names, *job_names, "Progressive Shop Level", "Progressive Ramza Job Form"
]

nonbalanced_major_item_names = [*job_names, "Progressive Shop Level"]

ramza_job_levels = [
    "Progressive Ramza Job Form", "Progressive Ramza Job Form"
]


special_character_names = [
    "Boco", "Rad", "Alicia", "Lavian", "Agrias", "Mustadio", "Rafa",
    "Malak", "Beowulf", "Reis (Dragon)", "Reis (Human)", "Orlandu",
    "Worker 8", "Cloud", "Meliadoul", "Byblos"
]

rare_item_names = [
    "Zorlin Shape", "Sasuke Knife", "Iga Knife", "Koga Knife", "Nagrarock", "Materia Blade", "Defender",
    "Save the Queen", "Excalibur", "Ragnarok", "Chaos Blade", "Masamune", "Chirijiraden", "Faith Rod", "Healing Staff",
    "Mace of Zeus", "Sage Staff", "Scorpion Tail", "Stone Gun", "Blaze Gun", "Glacier Gun", "Blast Gun",
    "Ultimus Bow", "Yoichi Bow", "Perseus Bow", "Fairy Harp", "Madlemgen", "Holy Lance", "Dragon Whisker",
    "Javelin 2", "Ivory Rod", "Whale Whisker", "FS Bag", "Ryozan Silk", "Genji Shield", "Kaiser Plate",
    "Venetian Shield", "Escutcheon 2", "Grand Helmet", "Genji Helmet", "Cachusha", "Barette", "Ribbon",
    "Genji Armor", "Maximillian", "Secret Clothes", "Rubber Costume", "Robe of Lords", "Genji Gauntlet",
    "Cursed Ring", "Vanish Mantle", "Chantage", "Cherche", "Salty Rage", "Setiemson"
]

gil_item_names = [
    "Bonus Gil: l i t t l e  m o n e y",
    "Bonus Gil: m o r e  m o n e y",
    "Bonus Gil: l o t s  o f  m o n e y"
]

gil_item_names_weighted = [
    "Bonus Gil: l i t t l e  m o n e y",
    "Bonus Gil: l i t t l e  m o n e y",
    "Bonus Gil: l i t t l e  m o n e y",
    "Bonus Gil: l i t t l e  m o n e y",
    "Bonus Gil: m o r e  m o n e y",
    "Bonus Gil: m o r e  m o n e y",
    "Bonus Gil: m o r e  m o n e y",
    "Bonus Gil: l o t s  o f  m o n e y",
    "Bonus Gil: l o t s  o f  m o n e y"
]

gil_item_sizes = [
    {
        "Bonus Gil: l i t t l e  m o n e y": 1000,
        "Bonus Gil: m o r e  m o n e y": 5000,
        "Bonus Gil: l o t s  o f  m o n e y": 20000
    },
    {
        "Bonus Gil: l i t t l e  m o n e y": 2000,
        "Bonus Gil: m o r e  m o n e y": 10000,
        "Bonus Gil: l o t s  o f  m o n e y": 40000
    },
    {
        "Bonus Gil: l i t t l e  m o n e y": 4000,
        "Bonus Gil: m o r e  m o n e y": 20000,
        "Bonus Gil: l o t s  o f  m o n e y": 80000
    }
]

jp_item_names = [
    "Small JP Boon", "Medium JP Boon", "Large JP Boon"
]

jp_item_names_weighted = [
    "Small JP Boon", "Small JP Boon", "Small JP Boon", "Small JP Boon",
    "Medium JP Boon", "Medium JP Boon", "Medium JP Boon",
    "Large JP Boon", "Large JP Boon",
]

jp_item_sizes = [
    {"Small JP Boon": 25, "Medium JP Boon": 50, "Large JP Boon": 125},
    {"Small JP Boon": 50, "Medium JP Boon": 100, "Large JP Boon": 250},
    {"Small JP Boon": 100, "Medium JP Boon": 200, "Large JP Boon": 500}
]

useful_item_names = [
    *rare_item_names, *special_character_names, *jp_item_names
]

shop_item_names = [
    item for item in gear_item_names if item not in useful_item_names
]

filler_item_names = [
    *shop_item_names, *gil_item_names, *jp_item_names
]

all_item_names = [
    *major_item_names, *special_character_names, *gear_item_names, *gil_item_names, *jp_item_names
]
