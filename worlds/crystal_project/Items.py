from typing import Dict, Set, NamedTuple, Optional
from BaseClasses import ItemClassification

class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: ItemClassification
    amount: Optional[int] = 1

#Archipelago does not like it if an item has a code of 0, Crystal project starts its database
#Ids at 0, so we add an offset to the id of each item and remove that offset in the client
index_offset = 1

item_table: Dict[str, ItemData] = {
    #Jobs
    "Job - Warrior": ItemData("Job", 0 + index_offset, ItemClassification.progression),
    "Job - Monk": ItemData("Job", 5 + index_offset, ItemClassification.progression),
    "Job - Rogue": ItemData("Job", 2 + index_offset, ItemClassification.progression),
    "Job - Cleric": ItemData("Job", 4 + index_offset, ItemClassification.progression),
    "Job - Wizard": ItemData("Job", 3 + index_offset, ItemClassification.progression),
    "Job - Warlock": ItemData("Job", 14 + index_offset, ItemClassification.progression),
    "Job - Fencer": ItemData("Job", 1 + index_offset, ItemClassification.progression),
    "Job - Shaman": ItemData("Job", 8 + index_offset, ItemClassification.progression),
    "Job - Scholar": ItemData("Job", 13 + index_offset, ItemClassification.progression),
    "Job - Aegis": ItemData("Job", 10 + index_offset, ItemClassification.progression),
    "Job - Hunter": ItemData("Job", 7 + index_offset, ItemClassification.progression),
    "Job - Chemist": ItemData("Job", 17 + index_offset, ItemClassification.progression),
    "Job - Reaper": ItemData("Job", 6 + index_offset, ItemClassification.progression),
    "Job - Ninja": ItemData("Job", 18 + index_offset, ItemClassification.progression),
    "Job - Nomad": ItemData("Job", 12 + index_offset, ItemClassification.progression),
    "Job - Dervish": ItemData("Job", 11 + index_offset, ItemClassification.progression),
    "Job - Beatsmith": ItemData("Job", 9 + index_offset, ItemClassification.progression),
    "Job - Samurai": ItemData("Job", 20 + index_offset, ItemClassification.progression),
    "Job - Assassin": ItemData("Job", 19 + index_offset, ItemClassification.progression),
    "Job - Valkyrie": ItemData("Job", 15 + index_offset, ItemClassification.progression),
    "Job - Summoner": ItemData("Job", 21 + index_offset, ItemClassification.progression),
    "Job - Beastmaster": ItemData("Job", 23 + index_offset, ItemClassification.progression),
    "Job - Weaver": ItemData("Job", 16 + index_offset, ItemClassification.progression),
    "Job - Mimic": ItemData("Job", 22 + index_offset, ItemClassification.progression),

    #Consumables
    "Item - Tonic": ItemData("Item", 18 + index_offset, ItemClassification.filler, 0),
    "Item - Potion": ItemData("Item", 0 + index_offset, ItemClassification.filler, 0),
    "Item - Z-Potion": ItemData("Item", 102 + index_offset, ItemClassification.filler, 0),
    "Item - Tincture": ItemData("Item", 47 + index_offset, ItemClassification.filler, 0),
    "Item - Ether": ItemData("Item", 1 + index_offset, ItemClassification.filler, 0),
    "Item - Zether": ItemData("Item", 142 + index_offset, ItemClassification.filler, 0),
    "Item - Fenix Juice": ItemData("Item", 2 + index_offset, ItemClassification.filler, 0),
    "Item - Fenix Syrup": ItemData("Item", 145 + index_offset, ItemClassification.filler, 0),
    "Item - Nan's Stew'": ItemData("Item", 9 + index_offset, ItemClassification.filler, 0),
    "Item - Nan's Cocoa'": ItemData("Item", 8 + index_offset, ItemClassification.filler, 0),
    "Item - Nan's Secret Recipe": ItemData("Item", 54 + index_offset, ItemClassification.filler, 0),
    "Item - Nuts": ItemData("Item", 14 + index_offset, ItemClassification.filler, 0),
    "Item - Milk": ItemData("Item", 20 + index_offset, ItemClassification.progression, 0),
    "Item - Shoudu Stew": ItemData("Item", 132 + index_offset, ItemClassification.progression, 0),
    "Item - Sweet Pop Candy": ItemData("Item", 34 + index_offset, ItemClassification.filler, 0),
    "Item - Sour Pop Candy": ItemData("Item", 35 + index_offset, ItemClassification.filler, 0),
    "Item - Bitter Pop Candy": ItemData("Item", 171 + index_offset, ItemClassification.filler, 0),
    "Item - Rotten Salmon": ItemData("Item", 11 + index_offset, ItemClassification.progression, 0),
    "Item - Decent Cod": ItemData("Item", 38 + index_offset, ItemClassification.filler, 0),
    "Item - Fresh Salmon": ItemData("Item", 10 + index_offset, ItemClassification.filler, 0),
    "Item - Scroll": ItemData("Item", 263 + index_offset, ItemClassification.filler, 0),

    #Bag upgrades
    "Item - Tonic Pouch": ItemData("Item", 133 + index_offset, ItemClassification.useful, 21),
    "Item - Potion Pouch": ItemData("Item", 134 + index_offset, ItemClassification.useful, 19),
    "Item - Z-Potion Pouch": ItemData("Item", 143 + index_offset, ItemClassification.useful, 7),
    "Item - Tincture Pouch": ItemData("Item", 135 + index_offset, ItemClassification.useful, 16),
    "Item - Ether Pouch": ItemData("Item", 136 + index_offset, ItemClassification.useful, 15),
    "Item - Zether Pouch": ItemData("Item", 144 + index_offset, ItemClassification.useful, 7),
    "Item - Fenix Juice Pouch": ItemData("Item", 137 + index_offset, ItemClassification.useful, 8),
    "Item - Fenix Syrup Pouch": ItemData("Item", 146 + index_offset, ItemClassification.useful, 2),
    "Item - Nuts Sack": ItemData("Item", 184 + index_offset, ItemClassification.useful),
    "Item - Milk Bag": ItemData("Item", 138 + index_offset, ItemClassification.useful),
    "Item - Decent Cod Bag": ItemData("Item", 185 + index_offset, ItemClassification.useful),

    #Fishing
    "Item - Flimsy Rod": ItemData("Item", 55 + index_offset, ItemClassification.useful),
    "Item - Tough Rod": ItemData("Item", 150 + index_offset, ItemClassification.useful),
    "Item - Super Rod": ItemData("Item", 151 + index_offset, ItemClassification.useful),
    "Item - Plug Lure": ItemData("Item", 91 + index_offset, ItemClassification.useful),
    "Item - Fly Lure": ItemData("Item", 149 + index_offset, ItemClassification.useful),
    "Item - Jigging Lure": ItemData("Item", 97 + index_offset, ItemClassification.useful),

    #Ore
    "Item - Silver Ore": ItemData("Item", 3 + index_offset, ItemClassification.useful, 18),
    "Item - Silver Ingot": ItemData("Item", 67 + index_offset, ItemClassification.useful, 18),
    "Item - Silver Dust": ItemData("Item", 68 + index_offset, ItemClassification.useful, 18),
    "Item - Gold Ore": ItemData("Item", 4 + index_offset, ItemClassification.useful, 18),
    "Item - Gold Ingot": ItemData("Item", 69 + index_offset, ItemClassification.useful, 18),
    "Item - Gold Dust": ItemData("Item", 70 + index_offset, ItemClassification.useful, 18),
    "Item - Diamond Ore": ItemData("Item", 5 + index_offset, ItemClassification.useful, 18),
    "Item - Diamond Ingot": ItemData("Item", 71 + index_offset, ItemClassification.useful, 18),
    "Item - Diamond Dust": ItemData("Item", 72 + index_offset, ItemClassification.useful, 18),

    #Passes
    "Item - Quintar Pass": ItemData("Item", 7 + index_offset, ItemClassification.progression),
    "Item - Luxury Pass": ItemData("Item", 93 + index_offset, ItemClassification.progression),
    "Item - Luxury Pass V2": ItemData("Item", 148 + index_offset, ItemClassification.progression),
    "Item - Ferry Pass": ItemData("Item", 37 + index_offset, ItemClassification.progression),

    #Key Items
    "Item - Black Squirrel": ItemData("Item", 21 + index_offset, ItemClassification.progression, 3),
    "Item - Dog Bone": ItemData("Item", 6 + index_offset, ItemClassification.progression, 3),
    #TODO: Check clamshell count
    "Item - Clamshell": ItemData("Item", 16 + index_offset, ItemClassification.progression, 17),
    "Item - Digested Head": ItemData("Item", 17 + index_offset, ItemClassification.progression, 3),
    "Item - Lost Penguin": ItemData("Item", 24 + index_offset, ItemClassification.progression, 12),
    "Item - Elevator Part": ItemData("Item", 224 + index_offset, ItemClassification.progression, 17),
    "Item - Undersea Crab": ItemData("Item", 212 + index_offset, ItemClassification.progression, 15),
    "Item - West Lookout Token": ItemData("Item", 81 + index_offset, ItemClassification.progression),
    "Item - Central Lookout Token": ItemData("Item", 88 + index_offset, ItemClassification.progression),
    "Item - North Lookout Token": ItemData("Item", 131 + index_offset, ItemClassification.progression),
    "Item - Babel Quintar": ItemData("Item", 167 + index_offset, ItemClassification.progression),
    "Item - Quintar Shedding": ItemData("Item", 168 + index_offset, ItemClassification.progression, 12),
    "Item - Vermillion Book": ItemData("Item", 172 + index_offset, ItemClassification.progression),
    "Item - Viridian Book": ItemData("Item", 173 + index_offset, ItemClassification.progression),
    "Item - Cerulean Book": ItemData("Item", 174 + index_offset, ItemClassification.progression),
    "Item - Ancient Tablet A": ItemData("Item", 161 + index_offset, ItemClassification.filler),
    "Item - Ancient Tablet B": ItemData("Item", 162 + index_offset, ItemClassification.filler),
    "Item - Ancient Tablet C": ItemData("Item", 163 + index_offset, ItemClassification.filler),

    #Animal summons
    "Item - Quintar Flute": ItemData("Item", 39 + index_offset, ItemClassification.progression),
    "Item - Ibek Bell": ItemData("Item", 50 + index_offset, ItemClassification.progression),
    "Item - Owl Drum": ItemData("Item", 49 + index_offset, ItemClassification.progression),
    "Item - Salmon Violin": ItemData("Item", 48 + index_offset, ItemClassification.progression),
    "Item - Salmon Cello": ItemData("Item", 114 + index_offset, ItemClassification.progression),

    #Teleport items
    "Item - Home Point Stone": ItemData("Item", 19 + index_offset, ItemClassification.progression),
    "Item - Gaea Stone": ItemData("Item", 23 + index_offset, ItemClassification.progression),
    "Item - Mercury Stone": ItemData("Item", 13 + index_offset, ItemClassification.progression),
    "Item - Poseidon Stone": ItemData("Item", 57 + index_offset, ItemClassification.progression),
    "Item - Mars Stone": ItemData("Item", 59 + index_offset, ItemClassification.progression),
    "Item - Ganymede Stone": ItemData("Item", 65 + index_offset, ItemClassification.progression),
    "Item - Triton Stone": ItemData("Item", 66 + index_offset, ItemClassification.progression),
    "Item - Callisto Stone": ItemData("Item", 155 + index_offset, ItemClassification.progression),
    "Item - Europa Stone": ItemData("Item", 64 + index_offset, ItemClassification.progression),
    "Item - Dione Stone": ItemData("Item", 166 + index_offset, ItemClassification.progression),
    "Item - Neptune Stone": ItemData("Item", 208 + index_offset, ItemClassification.progression),
    "Item - New World Stone": ItemData("Item", 140 + index_offset, ItemClassification.progression),
    "Item - Old World Stone": ItemData("Item", 253 + index_offset, ItemClassification.progression),

    #Swords
    "Equipment - Short Sword": ItemData("Equipment", 0 + index_offset, ItemClassification.useful),
    "Equipment - Iron Sword": ItemData("Equipment", 11 + index_offset, ItemClassification.useful),
    "Equipment - Contract": ItemData("Equipment", 71 + index_offset, ItemClassification.useful),
    "Equipment - Help the Prince": ItemData("Equipment", 89 + index_offset, ItemClassification.useful),
    "Equipment - Craftwork Sword": ItemData("Equipment", 93 + index_offset, ItemClassification.useful),
    "Equipment - Broadsword": ItemData("Equipment", 12 + index_offset, ItemClassification.useful),
    "Equipment - Sharp Sword": ItemData("Equipment", 200 + index_offset, ItemClassification.useful),
    "Equipment - Razor Edge": ItemData("Equipment", 199 + index_offset, ItemClassification.useful),
    "Equipment - Silver Sword": ItemData("Equipment", 112 + index_offset, ItemClassification.useful),
    "Equipment - Artisan Sword": ItemData("Equipment", 157 + index_offset, ItemClassification.useful),
    "Equipment - Longsword": ItemData("Equipment", 378 + index_offset, ItemClassification.useful),
    "Equipment - Boomer Sword": ItemData("Equipment", 177 + index_offset, ItemClassification.useful),
    "Equipment - Digested Sword": ItemData("Equipment", 227 + index_offset, ItemClassification.useful),
    "Equipment - Scimitar": ItemData("Equipment", 379 + index_offset, ItemClassification.useful),
    "Equipment - Cutlass": ItemData("Equipment", 377 + index_offset, ItemClassification.useful),
    "Equipment - Cold Touch": ItemData("Equipment", 375 + index_offset, ItemClassification.useful),
    "Equipment - Burning Blade": ItemData("Equipment", 497 + index_offset, ItemClassification.useful),
    "Equipment - Gold Sword": ItemData("Equipment", 138 + index_offset, ItemClassification.useful),
    "Equipment - War Sword": ItemData("Equipment", 376 + index_offset, ItemClassification.useful),
    "Equipment - Bloodbind": ItemData("Equipment", 197 + index_offset, ItemClassification.useful),
    "Equipment - Temporal Blade": ItemData("Equipment", 525 + index_offset, ItemClassification.useful),
    "Equipment - Highland Blade": ItemData("Equipment", 370 + index_offset, ItemClassification.useful),
    "Equipment - Hydra Edge": ItemData("Equipment", 371 + index_offset, ItemClassification.useful),
    "Equipment - Defender": ItemData("Equipment", 380 + index_offset, ItemClassification.useful),
    "Equipment - Crystal Sword": ItemData("Equipment", 374 + index_offset, ItemClassification.useful),
    "Equipment - Conquest": ItemData("Equipment", 372 + index_offset, ItemClassification.useful),
    "Equipment - Flame Sword": ItemData("Equipment", 381 + index_offset, ItemClassification.useful),
    "Equipment - Master Sword": ItemData("Equipment", 248 + index_offset, ItemClassification.useful),
    "Equipment - Rune Sword": ItemData("Equipment", 382 + index_offset, ItemClassification.useful),
    "Equipment - Auduril": ItemData("Equipment", 270 + index_offset, ItemClassification.useful),
    "Equipment - Master Bigsword": ItemData("Equipment", 249 + index_offset, ItemClassification.useful),
    "Equipment - Training Sword": ItemData("Equipment", 532 + index_offset, ItemClassification.useful),
    "Equipment - Life Line": ItemData("Equipment", 302 + index_offset, ItemClassification.useful),
    "Equipment - Soul Keeper": ItemData("Equipment", 303 + index_offset, ItemClassification.useful),
    "Equipment - Crabs Claw": ItemData("Equipment", 411 + index_offset, ItemClassification.useful),
    "Equipment - Kings Guard": ItemData("Equipment", 316 + index_offset, ItemClassification.useful),
    "Equipment - Diamond Sword": ItemData("Equipment", 135 + index_offset, ItemClassification.useful),
    "Equipment - Balrog": ItemData("Equipment", 369 + index_offset, ItemClassification.useful),
    "Equipment - Oily Sword": ItemData("Equipment", 279 + index_offset, ItemClassification.useful),
}

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
