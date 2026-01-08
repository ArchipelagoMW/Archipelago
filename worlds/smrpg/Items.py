import typing

from BaseClasses import ItemClassification


class ItemData(typing.NamedTuple):
    name: str
    code: typing.Optional[int]
    classification: ItemClassification
    rando_name: str  # Internal randomizer name
    event: bool = False


# Filler items that we can freely toss multiples of in the pool
consumables = [
    "Mushroom", "Mid Mushroom", "Max Mushroom", "Honey Syrup", "Maple Syrup", "Royal Syrup", "Pick Me Up",
    "Able Juice", "Bracer", "Energizer", "Yoshi Ade", "Red Essence", "Kerokero Cola", "Yoshi Cookie",
    "Pure Water", "Sleepy Bomb", "Bad Mushroom", "Fire Bomb", "Ice Bomb", "Flower Tab", "Flower Jar",
    "Flower Box", "Yoshi Candy", "Froggie Drink", "Muku Cookie", "Elixir", "Megalixir", "Freshen Up",
    "Rock Candy", "Sheep Attack", "Carbo Cookie", "Fright Bomb", "Crystalline", "Power Blast",
    "Wilt Shroom", "Rotten Mush", "Moldy Mush", "Mushroom 2", "Shiny Stone",
]

coin_rewards = [
    "Five Coins", "Eight Coins", "Ten Coins", "Fifty Coins",
    "One Hundred Coins", "One Hundred Fifty Coins", "Frog Coin"
]

chest_rewards = [
    *coin_rewards, "Flower", "Recovery Mushroom", "You Missed!"
]

filler = [*consumables, *chest_rewards]

key_items = [
    "Temple Key", "Rare Frog Coin", "Cricket Pie", "Castle Key 1", "Castle Key 2", "Bambino Bomb",
    "Room Key", "Elder Key", "Shed Key", "Soprano Card", "Alto Card", "Tenor Card", "Seed", "Fertilizer",
    "Big Boo Flag", "Dry Bones Flag", "Greaper Flag", "Cricket Jam", "Bright Card"
]

# Not key items, but stuff that doesn't make sense to have in the pool multiple times
singleton_items = [
    *key_items, "Wallet", "Goodie Bag", "See Ya", "Earlier Times",
    "Lamb's Lure", "Mystery Egg", "Star Egg", "Signal Ring", "Lucky Jewel"
]

weapons = [
    "Hammer", "Froggie Stick", "Nok Nok Shell", "Punch Glove", "Finger Shot", "Cymbals",
    "Chomp", "Masher", "Chomp Shell", "Super Hammer", "Hand Gun", "Whomp Glove", "Slap Glove",
    "Troopa Shell", "Parasol", "Hurly Gloves", "Double Punch", "Ribbit Stick", "Spiked Link", "Mega Glove",
    "War Fan", "Hand Cannon", "Sticky Glove", "Ultra Hammer", "Super Slap", "Drill Claw", "Star Gun",
    "Sonic Cymbal", "Lazy Shell Weapon", "Frying Pan", "Lucky Hammer"
]

armor = [
    "Shirt", "Pants", "Thick Shirt",
    "Thick Pants", "Mega Shirt", "Mega Pants", "Work Pants", "Mega Cape", "Happy Shirt", "Happy Pants",
    "Happy Cape", "Happy Shell", "Polka Dress", "Sailor Shirt", "Sailor Pants", "Sailor Cape", "Nautica Dress",
    "Courage Shell", "Fuzzy Shirt", "Fuzzy Pants", "Fuzzy Cape", "Fuzzy Dress", "Fire Shirt", "Fire Pants",
    "Fire Cape", "Fire Shell", "Fire Dress", "Hero Shirt", "Prince Pants", "Star Cape", "Heal Shell",
    "Royal Dress", "Super Suit", "Lazy Shell Armor"
]

accessories = [
    "Zoom Shoes", "Safety Badge", "Jump Shoes",
    "Safety Ring", "Amulet", "Scrooge Ring", "Exp Booster", "Attack Scarf", "Rare Scarf",
    "B'tub Ring", "Antidote Pin", "Wake Up Pin", "Fearless Pin", "Trueform Pin", "Coin Trick",
    "Ghost Medal", "Jinx Belt", "Feather", "Troopa Pin", "Signal Ring", "Quartz Charm"
]

equipment = [*weapons, *armor, *accessories]

all_mundane_items = [*filler, *equipment]

boss_items = [
    "Star Piece", "Defeated!", "Star Road Restored!"
]
id = 0

item_table = dict()

for item in consumables:
    new_item = ItemData(item, id, ItemClassification.filler, item.replace(" ", "").replace("'", ""), False)
    item_table[item] = new_item
    id += 1

for item in chest_rewards:
    new_item = ItemData(item, id, ItemClassification.filler, item.replace(" ", "").replace("'", ""), False)
    item_table[item] = new_item
    id += 1

for item in weapons:
    new_item = ItemData(item, id, ItemClassification.useful, item.replace(" ", "").replace("'", ""), False)
    item_table[item] = new_item
    id += 1

for item in armor:
    new_item = ItemData(item, id, ItemClassification.useful, item.replace(" ", "").replace("'", ""), False)
    item_table[item] = new_item
    id += 1

for item in accessories:
    new_item = ItemData(item, id, ItemClassification.useful, item.replace(" ", "").replace("'", ""), False)
    item_table[item] = new_item
    id += 1

for item in singleton_items:
    if item in key_items:
        classification = ItemClassification.progression
    else:
        classification = ItemClassification.useful
    new_item = ItemData(item, id, classification, item.replace(" ", "").replace("'", ""), False)
    item_table[item] = new_item
    id += 1

for item in boss_items:
    new_item = ItemData(item, id, ItemClassification.progression, item.replace(" ", "").replace("'", ""), False)
    item_table[item] = new_item
    id += 1

item_table["Invincibility Star"] = ItemData("Invincibility Star", id, ItemClassification.useful, "InvincibilityStar", False)

original_item_list = {
    "Five Coins": 1,
    "Eight Coins": 1,
    "Flower": 32,
    "Recovery Mushroom": 18,
    "Honey Syrup": 1,
    "Flower Tab": 10,
    "Hammer": 1,
    "Ten Coins": 2,  # Figure out CoinsDoubleBig later
    "Frog Coin": 29,
    "Pick Me Up": 3,
    "Mushroom": 1,
    "Wake Up Pin": 1,
    "Kerokero Cola": 9,
    "Wallet": 1,
    "Trueform Pin": 1,
    "Nok Nok Shell": 1,
    "Froggie Stick": 1,
    "Lazy Shell Armor": 1,
    "Lazy Shell Weapon": 1,
    "Finger Shot": 1,
    "Red Essence": 5,
    "Flower Jar": 3,
    "Lucky Jewel": 1,
    "Mystery Egg": 1,
    "Frying Pan": 1,
    "One Hundred Fifty Coins": 3,
    "Rock Candy": 6,
    "Masher": 1,
    "Zoom Shoes": 1,
    "Goodie Bag": 1,
    "Chomp": 1,
    "Amulet": 1,
    "Flower Box": 1,
    "Max Mushroom": 5,
    "One Hundred Coins": 6,
    "Safety Ring": 1,
    "Royal Syrup": 5,
    "Safety Badge": 1,
    "Troopa Pin": 1,
    "Fifty Coins": 1,
    "Fire Bomb": 3,
    "Jinx Belt": 1,
    "Quartz Charm": 1,
    "Attack Scarf": 1,
    "Super Suit": 1,
    "Ghost Medal": 1,
    "Rare Scarf": 1,
    "Feather": 1,
    "Signal Ring": 1,
    "Fright Bomb": 1,
    "Ice Bomb": 1,
    "Sonic Cymbal": 1,
    "Super Slap": 1,
    "Star Gun": 1,
    "Ultra Hammer": 1,
    "Dry Bones Flag": 1,
    "Rare Frog Coin": 1,
    "Cricket Pie": 1,
    "Greaper Flag": 1,
    "Cricket Jam": 1,
    "Soprano Card": 1,
    "Alto Card": 1,
    "Tenor Card": 1,
    "Big Boo Flag": 1,
    "Bambino Bomb": 1,
    "Elder Key": 1,
    "Room Key": 1,
    "Bright Card": 1,
    "Shed Key": 1,
    "Temple Key": 1,
    "Seed": 1,
    "Castle Key 1": 1,
    "Castle Key 2": 1,
    "Fertilizer": 1,
    "You Missed!": 1,
}
