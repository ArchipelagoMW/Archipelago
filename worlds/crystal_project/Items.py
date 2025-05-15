from typing import Dict, Set, Tuple, NamedTuple, Optional, List
from BaseClasses import ItemClassification

class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: ItemClassification
    #Amount found in each region type; added together for each set you're including
    beginnerAmount: Optional[int] = 1
    advancedAmount: Optional[int] = 0
    expertAmount: Optional[int] = 0
    endGameAmount: Optional[int] = 0

class Job(NamedTuple):
    name: str
    id: int

#Archipelago does not like it if an item has a code of 0, Crystal project starts its database
#Ids at 0, so we add an offset to the id of each item and remove that offset in the client
job_index_offset = 1
item_index_offset = 101
equipment_index_offset = 1001
summon_index_offset = 10001
scholar_index_offset = 100001

item_table: Dict[str, ItemData] = {
    #Jobs
    "Job - Warrior": ItemData("Job", 0 + job_index_offset, ItemClassification.progression),
    "Job - Monk": ItemData("Job", 5 + job_index_offset, ItemClassification.progression),
    "Job - Rogue": ItemData("Job", 2 + job_index_offset, ItemClassification.progression),
    "Job - Cleric": ItemData("Job", 4 + job_index_offset, ItemClassification.progression),
    "Job - Wizard": ItemData("Job", 3 + job_index_offset, ItemClassification.progression),
    "Job - Warlock": ItemData("Job", 14 + job_index_offset, ItemClassification.progression),
    "Job - Fencer": ItemData("Job", 1 + job_index_offset, ItemClassification.progression),
    "Job - Shaman": ItemData("Job", 8 + job_index_offset, ItemClassification.progression),
    "Job - Scholar": ItemData("Job", 13 + job_index_offset, ItemClassification.progression), #requirement for Grans subbasement
    "Job - Aegis": ItemData("Job", 10 + job_index_offset, ItemClassification.progression),
    "Job - Hunter": ItemData("Job", 7 + job_index_offset, ItemClassification.progression),
    "Job - Chemist": ItemData("Job", 17 + job_index_offset, ItemClassification.progression),
    "Job - Reaper": ItemData("Job", 6 + job_index_offset, ItemClassification.progression),
    "Job - Ninja": ItemData("Job", 18 + job_index_offset, ItemClassification.progression),
    "Job - Nomad": ItemData("Job", 12 + job_index_offset, ItemClassification.progression),
    "Job - Dervish": ItemData("Job", 11 + job_index_offset, ItemClassification.progression),
    "Job - Beatsmith": ItemData("Job", 9 + job_index_offset, ItemClassification.progression),
    "Job - Samurai": ItemData("Job", 20 + job_index_offset, ItemClassification.progression),
    "Job - Assassin": ItemData("Job", 19 + job_index_offset, ItemClassification.progression),
    "Job - Valkyrie": ItemData("Job", 15 + job_index_offset, ItemClassification.progression),
    "Job - Summoner": ItemData("Job", 21 + job_index_offset, ItemClassification.progression), #Required for summon fights if we add them to locations; only job checked by NPCs
    "Job - Beastmaster": ItemData("Job", 23 + job_index_offset, ItemClassification.progression),
    "Job - Weaver": ItemData("Job", 16 + job_index_offset, ItemClassification.progression),
    "Job - Mimic": ItemData("Job", 22 + job_index_offset, ItemClassification.progression),

    #Consumables
    "Item - Tonic": ItemData("Item", 18 + item_index_offset, ItemClassification.filler, 0),
    "Item - Potion": ItemData("Item", 0 + item_index_offset, ItemClassification.filler, 0),
    "Item - Z-Potion": ItemData("Item", 102 + item_index_offset, ItemClassification.filler, 0),
    "Item - Tincture": ItemData("Item", 47 + item_index_offset, ItemClassification.filler, 0),
    "Item - Ether": ItemData("Item", 1 + item_index_offset, ItemClassification.filler, 0),
    "Item - Zether": ItemData("Item", 142 + item_index_offset, ItemClassification.filler, 0),
    "Item - Fenix Juice": ItemData("Item", 2 + item_index_offset, ItemClassification.filler, 0),
    "Item - Fenix Syrup": ItemData("Item", 145 + item_index_offset, ItemClassification.filler, 0),
    "Item - Nans Stew": ItemData("Item", 9 + item_index_offset, ItemClassification.filler, 0),
    "Item - Nans Cocoa": ItemData("Item", 8 + item_index_offset, ItemClassification.filler, 0),
    "Item - Nans Secret Recipe": ItemData("Item", 54 + item_index_offset, ItemClassification.filler, 0),
    "Item - Nuts": ItemData("Item", 14 + item_index_offset, ItemClassification.filler, 0),
    "Item - Milk": ItemData("Item", 20 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Thirsty Lad, Poko Poko Desert, Advanced Regions
    "Item - Shoudu Stew": ItemData("Item", 132 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Foreign Foodie, Sara Sara Bazaar, Advanced Regions
    "Item - Sweet Pop Candy": ItemData("Item", 34 + item_index_offset, ItemClassification.filler, 0),
    "Item - Sour Pop Candy": ItemData("Item", 35 + item_index_offset, ItemClassification.filler, 0),
    "Item - Bitter Pop Candy": ItemData("Item", 171 + item_index_offset, ItemClassification.filler, 0),
    "Item - Rotten Salmon": ItemData("Item", 11 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Fish Merchant, Sara Sara Bazaar, Advanced Regions
    "Item - Decent Cod": ItemData("Item", 38 + item_index_offset, ItemClassification.filler, 0),
    "Item - Fresh Salmon": ItemData("Item", 10 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Fish Merchant, Sara Sara Bazaar, Advanced Regions
    "Item - Scroll": ItemData("Item", 263 + item_index_offset, ItemClassification.filler, 0),

    #Bag upgrades
    "Item - Tonic Pouch": ItemData("Item", 133 + item_index_offset, ItemClassification.useful, 9, 7, 1, 0), #17
    "Item - Potion Pouch": ItemData("Item", 134 + item_index_offset, ItemClassification.useful, 0, 5, 8, 0), #13
    "Item - Z-Potion Pouch": ItemData("Item", 143 + item_index_offset, ItemClassification.useful, 1, 0, 2, 1), #5
    "Item - Tincture Pouch": ItemData("Item", 135 + item_index_offset, ItemClassification.useful, 6, 6, 2, 0), #14
    "Item - Ether Pouch": ItemData("Item", 136 + item_index_offset, ItemClassification.useful, 0, 6, 5, 0), #11
    "Item - Zether Pouch": ItemData("Item", 144 + item_index_offset, ItemClassification.useful, 0, 1, 1, 3), #5
    "Item - Fenix Juice Pouch": ItemData("Item", 137 + item_index_offset, ItemClassification.useful, 1, 1, 0, 0), #2
    "Item - Fenix Syrup Pouch": ItemData("Item", 146 + item_index_offset, ItemClassification.useful, 0, 2, 0, 0), #2
    "Item - Nuts Sack": ItemData("Item", 184 + item_index_offset, ItemClassification.useful, 0, 1), #Capital Sequoia, Advanced Zones
    "Item - Milk Bag": ItemData("Item", 138 + item_index_offset, ItemClassification.useful, 0, 1), #Poko Poko Desert, Advanced Zones
    "Item - Decent Cod Bag": ItemData("Item", 185 + item_index_offset, ItemClassification.useful, 0, 0, 1), #Shoudu Province, Expert Zones

    #Fishing
    "Item - Flimsy Rod": ItemData("Item", 55 + item_index_offset, ItemClassification.useful),
    "Item - Tough Rod": ItemData("Item", 150 + item_index_offset, ItemClassification.useful),
    "Item - Super Rod": ItemData("Item", 151 + item_index_offset, ItemClassification.useful),
    "Item - Plug Lure": ItemData("Item", 91 + item_index_offset, ItemClassification.useful),
    "Item - Fly Lure": ItemData("Item", 149 + item_index_offset, ItemClassification.useful),
    "Item - Jigging Lure": ItemData("Item", 97 + item_index_offset, ItemClassification.useful),

    #Ore
    "Item - Silver Ore": ItemData("Item", 3 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Capital Blacksmith, Capital Sequoia, Advanced Regions
    "Item - Silver Ingot": ItemData("Item", 67 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Capital Blacksmith, Capital Sequoia, Advanced Regions
    "Item - Silver Dust": ItemData("Item", 68 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Capital Blacksmith, Capital Sequoia, Advanced Regions
    "Item - Gold Ore": ItemData("Item", 4 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Armorer in Sara Sara Bazaar and Weaponsmith in Shoudu Province, Advanced Regions
    "Item - Gold Ingot": ItemData("Item", 69 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Armorer in Sara Sara Bazaar and Weaponsmith in Shoudu Province, Advanced Regions
    "Item - Gold Dust": ItemData("Item", 70 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Armorer in Sara Sara Bazaar and Weaponsmith in Shoudu Province, Advanced Regions
    "Item - Diamond Ore": ItemData("Item", 5 + item_index_offset, ItemClassification.useful, 0, 0, 18), #Used by Armorer in Tall Tall Heights and Weaponsmith in Jidamba Tangle, Expert Regions
    "Item - Diamond Ingot": ItemData("Item", 71 + item_index_offset, ItemClassification.useful, 0, 0, 18), #Used by Armorer in Tall Tall Heights and Weaponsmith in Jidamba Tangle, Expert Regions
    "Item - Diamond Dust": ItemData("Item", 72 + item_index_offset, ItemClassification.useful, 0, 0, 18), #Used by Armorer in Tall Tall Heights and Weaponsmith in Jidamba Tangle, Expert Regions

    #Keys
    "Item - Gardeners Key": ItemData("Item", 31 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Sequoia, Advanced Regions
    "Item - Courtyard Key": ItemData("Item", 33 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Sequoia (Courtyard), Advanced Regions
    "Item - Luxury Key": ItemData("Item", 36 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Sequoia, Advanced Regions
    "Item - Cell Key": ItemData("Item", 40 + item_index_offset, ItemClassification.progression, 0, 7), #Turn-in: Capital Jail, Advanced Regions
    "Item - South Wing Key": ItemData("Item", 41 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Jail, Advanced Regions
    "Item - East Wing Key": ItemData("Item", 42 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Jail, Advanced Regions
    "Item - West Wing Key": ItemData("Item", 43 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Jail, Advanced Regions
    "Item - Dark Wing Key": ItemData("Item", 44 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Jail, Advanced Regions
    "Item - Room 1 Key": ItemData("Item", 32 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Sara Sara Bazaar, Advanced Regions
    "Item - Pyramid Key": ItemData("Item", 60 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Poko Poko Desert (unlocks Ancient Reservoir), Advanced Regions
    "Item - Tram Key": ItemData("Item", 95 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Continental Tram (unlocks connection between Continental Tram and Sara Sara Bazaar), Expert Regions
    "Item - Small Key": ItemData("Item", 29 + item_index_offset, ItemClassification.progression, 0, 0, 4), #Turn-in: Beaurior Rock, Expert Regions
    "Item - Boss Key": ItemData("Item", 30 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Beaurior Rock, Expert Regions
    "Item - Ice Cell Key": ItemData("Item", 156 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Northern Cave, Expert Regions
    "Item - Red Door Key": ItemData("Item", 169 + item_index_offset, ItemClassification.progression, 0, 0, 3), #Turn-in: Slip Glide Ride, Expert Regions
    "Item - Ice Puzzle Key": ItemData("Item", 160 + item_index_offset, ItemClassification.progression, 0, 0, 6), #Turn-in: Sequoia Athenaeum, Expert Regions
    "Item - Foliage Key": ItemData("Item", 141 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Jidamba Tangle (unlocks Jidamba Eaclaneya), Expert Regions
    "Item - Cave Key": ItemData("Item", 118 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Jidamba Tangle (unlocks Jidamba Eaclaneya), Expert Regions
    "Item - Canopy Key": ItemData("Item", 116 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Jidamba Tangle (unlocks Jidamba Eaclaneya), Expert Regions
    "Item - Rampart Key": ItemData("Item", 175 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Castle Ramparts, Expert Regions
    "Item - Forgotten Key": ItemData("Item", 192 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: The Deep Sea, Expert Regions
    "Item - Skeleton Key": ItemData("Item", 147 + item_index_offset, ItemClassification.progression), #Everyone's best friend

    #Passes
    #"Item - Quintar Pass": ItemData("Item", 7 + item_index_offset, ItemClassification.progression), (now part of Progressive Quintar Flute)
    "Item - Progressive Luxury Pass": ItemData("Item", 93 + item_index_offset, ItemClassification.progression, 0, 2), #Luxury Pass ID 93; Luxury Pass V2 148; Turn-in: Capital Sequoia, Advanced Regions
    "Item - Ferry Pass": ItemData("Item", 37 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Sara Sara Bazaar (unlocks connection to Shoudu Province), Expert Regions

    #Key Items
    "Item - Black Squirrel": ItemData("Item", 21 + item_index_offset, ItemClassification.progression, 4), #Turn-in: Spawning Meadows, Beginner Regions
    "Item - Dog Bone": ItemData("Item", 6 + item_index_offset, ItemClassification.progression, 3), #Turn-in: Delende, Beginner Regions
    # Number of clamshells is set dynamically based on your Clamshells in pool variable
    "Item - Clamshell": ItemData("Item", 16 + item_index_offset, ItemClassification.progression, 0), #Turn-in: Seaside Cliffs, Beginner Regions
    "Item - Digested Head": ItemData("Item", 17 + item_index_offset, ItemClassification.progression, 0, 3), #Turn-in: Capital Sequoia, Advanced Regions
    "Item - Lost Penguin": ItemData("Item", 24 + item_index_offset, ItemClassification.progression, 0, 12), #Turn-in: Capital Sequoia, Advanced Regions
    "Item - Elevator Part": ItemData("Item", 224 + item_index_offset, ItemClassification.progression, 0, 0, 10), #Turn-in: Shoudu Province, Expert Regions
    "Item - Undersea Crab": ItemData("Item", 212 + item_index_offset, ItemClassification.progression, 0, 0, 15), #Turn-in: The Deep Sea, Expert Regions
    "Item - West Lookout Token": ItemData("Item", 81 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Sara Sara Bazaar, Advanced Regions
    "Item - Central Lookout Token": ItemData("Item", 88 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Sara Sara Bazaar, Advanced Regions
    "Item - North Lookout Token": ItemData("Item", 131 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Sara Sara Bazaar, Advanced Regions
    "Item - Babel Quintar": ItemData("Item", 167 + item_index_offset, ItemClassification.useful), #I don't know if we'll be adding any checks that require you to speak Quintar tbh
    #"Item - Quintar Shedding": ItemData("Item", 168 + item_index_offset, ItemClassification.filler, 0), #12
    "Item - Crag Demon Horn": ItemData("Item", 197 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Jojo Sewers, Advanced Regions
    "Item - Vermillion Book": ItemData("Item", 172 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Tall Tall Heights (unlocks Sequoia Athenaeum), Expert Regions
    "Item - Viridian Book": ItemData("Item", 173 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Tall Tall Heights (Sequoia Athenaeum), Expert Regions
    "Item - Cerulean Book": ItemData("Item", 174 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Tall Tall Heights (Sequoia Athenaeum), Expert Regions
    "Item - Ancient Tablet A": ItemData("Item", 161 + item_index_offset, ItemClassification.filler, 0, 0, 0, 1),
    "Item - Ancient Tablet B": ItemData("Item", 162 + item_index_offset, ItemClassification.filler, 0, 0, 0, 1),
    "Item - Ancient Tablet C": ItemData("Item", 163 + item_index_offset, ItemClassification.filler, 0, 0, 0, 1),
    "Item - Treasure Finder": ItemData("Item", 196 + item_index_offset, ItemClassification.useful),
    "Item - Progressive Level Cap": ItemData("Item", 500 + item_index_offset, ItemClassification.progression, 0),

    #Animal mount summons
    "Item - Progressive Quintar Flute": ItemData("Item", 39 + item_index_offset, ItemClassification.progression, 3), #Quintar Pass ID 7 & Quintar Flute ID 39 & Quintar Ocarina 115
    "Item - Ibek Bell": ItemData("Item", 50 + item_index_offset, ItemClassification.progression),
    "Item - Owl Drum": ItemData("Item", 49 + item_index_offset, ItemClassification.progression),
    "Item - Progressive Salmon Violin": ItemData("Item", 48 + item_index_offset, ItemClassification.progression, 2), #Salmon Violin ID 48 & Salmon Cello ID 114

    #Teleport items (shards not included since they are stones but worse)
    "Item - Home Point Stone": ItemData("Item", 19 + item_index_offset, ItemClassification.useful), #Starter pack
    "Item - Gaea Stone": ItemData("Item", 23 + item_index_offset, ItemClassification.progression, 0, 1), #Teleport to Capital Sequoia, Advanced Regions
    "Item - Mercury Stone": ItemData("Item", 13 + item_index_offset, ItemClassification.progression), #Teleport to Beginner Regions
    "Item - Poseidon Stone": ItemData("Item", 57 + item_index_offset, ItemClassification.progression, 0, 1), #Teleport to Salmon River, Advanced Regions
    "Item - Mars Stone": ItemData("Item", 59 + item_index_offset, ItemClassification.progression, 0, 1), #Teleport to Poko Poko Desert, Advanced Regions
    "Item - Ganymede Stone": ItemData("Item", 65 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to above Shoudu Province, Expert Regions
    "Item - Triton Stone": ItemData("Item", 66 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to Tall Tall Heights, Expert Regions
    "Item - Callisto Stone": ItemData("Item", 155 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to Lands End, Expert Regions
    "Item - Europa Stone": ItemData("Item", 64 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to Jidamba Tangle, Expert Regions
    "Item - Dione Stone": ItemData("Item", 166 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to above Quintar Reserve, Expert Regions
    "Item - Neptune Stone": ItemData("Item", 208 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to The Deep Sea, Expert Regions
    "Item - New World Stone": ItemData("Item", 140 + item_index_offset, ItemClassification.progression), #End-Game Regions (not excluded by region bc affected by player goals)
    "Item - Old World Stone": ItemData("Item", 253 + item_index_offset, ItemClassification.progression), #End-Game Regions (not excluded by region bc affected by player goals)

    #Weapons
    #Swords
    #"Equipment - Short Sword": ItemData("Equipment", 0 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Iron Sword": ItemData("Equipment", 11 + equipment_index_offset, ItemClassification.useful), #Tier 1 1H, Delende, Beginner Zones
    "Equipment - Contract": ItemData("Equipment", 71 + equipment_index_offset, ItemClassification.useful), #Tier 1 1H, Mercury Shrine, Beginner Zones
    "Equipment - Help the Prince": ItemData("Equipment", 89 + equipment_index_offset, ItemClassification.useful), #Tier 1 1H, Trial Caves/Skumparadise, Beginner Zones
    "Equipment - Craftwork Sword": ItemData("Equipment", 93 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1 1H, Capital Sequoia, Advanced Zones
    "Equipment - Broadsword": ItemData("Equipment", 12 + equipment_index_offset, ItemClassification.useful), #Tier 1 2H, Yamagawa M.A., Beginner Zones
    "Equipment - Sharp Sword": ItemData("Equipment", 200 + equipment_index_offset, ItemClassification.useful), #Tier 2 1H, Skumparadise, Beginner Zones
    #"Equipment - Razor Edge": ItemData("Equipment", 199 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Silver Sword": ItemData("Equipment", 112 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Sword": ItemData("Equipment", 157 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Longsword": ItemData("Equipment", 378 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Boomer Sword": ItemData("Equipment", 177 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 2H, Boomer Society, Advanced Zones
    #"Equipment - Digested Sword": ItemData("Equipment", 227 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Scimitar": ItemData("Equipment", 379 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Cutlass": ItemData("Equipment", 377 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 1H, Shoudu Province, Expert Zones
    "Equipment - Cold Touch": ItemData("Equipment", 375 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 1H, Beaurior Rock, Expert Zones
    #"Equipment - Burning Blade": ItemData("Equipment", 497 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Gold Sword": ItemData("Equipment", 138 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - War Sword": ItemData("Equipment", 376 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Bloodbind": ItemData("Equipment", 197 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 2H, Salmon River, Advanced Zones
    "Equipment - Temporal Blade": ItemData("Equipment", 525 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 2H, Beaurior Volcano, Expert Zones
    #"Equipment - Highland Blade": ItemData("Equipment", 370 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Hydra Edge": ItemData("Equipment", 371 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Defender": ItemData("Equipment", 380 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 1H, Lands End, Expert Zones
    #"Equipment - Crystal Sword": ItemData("Equipment", 374 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Conquest": ItemData("Equipment", 372 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 1H, Castle Ramparts, Expert Zones
    "Equipment - Flame Sword": ItemData("Equipment", 381 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 1H, Jidamba Eaclaneya, Expert Zones
    #"Equipment - Master Sword": ItemData("Equipment", 248 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Rune Sword": ItemData("Equipment", 382 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 2H, Castle Ramparts, Expert Zones
    #"Equipment - Auduril": ItemData("Equipment", 270 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Master Bigsword": ItemData("Equipment", 249 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Training Sword": ItemData("Equipment", 532 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Life Line": ItemData("Equipment", 302 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Soul Keeper": ItemData("Equipment", 303 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 1H, The Deep Sea, Expert Zones
    "Equipment - Crabs Claw": ItemData("Equipment", 411 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 1H, The Deep Sea, Expert Zones
    "Equipment - Kings Guard": ItemData("Equipment", 316 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 1H, Castle Sequoia, End-Game Zones
    #"Equipment - Diamond Sword": ItemData("Equipment", 135 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Balrog": ItemData("Equipment", 369 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Oily Sword": ItemData("Equipment", 279 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 2H, Castle Sequoia, End-Game Zones

    #Axes
    #"Equipment - Hand Axe": ItemData("Equipment", 55 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Axe": ItemData("Equipment", 94 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1 1H, Capital Sequoia, Advanced Zones
    "Equipment - Cleaver": ItemData("Equipment", 2 + equipment_index_offset, ItemClassification.useful), #Tier 1 2H, Spawning Meadows, Beginner Zones
    #"Equipment - Chopper": ItemData("Equipment", 66 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Hunting Axe": ItemData("Equipment", 187 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 1H, Rolling Quintar Fields, Advanced Zones
    #"Equipment - Silver Axe": ItemData("Equipment", 104 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Stone Splitter": ItemData("Equipment", 201 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Broadaxe": ItemData("Equipment", 383 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Axe": ItemData("Equipment", 158 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Hatchet": ItemData("Equipment", 386 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 1H, Poko Poko Desert, Advanced Zones
    #"Equipment - Axe of Light": ItemData("Equipment", 387 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Gold Axe": ItemData("Equipment", 139 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - War Axe": ItemData("Equipment", 384 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Berserker Axe": ItemData("Equipment", 390 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Gaia Axe": ItemData("Equipment", 385 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 2H, Shoudu Province, Expert Zones
    #"Equipment - Master Axe": ItemData("Equipment", 251 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Ancient Axe": ItemData("Equipment", 391 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Master Bigaxe": ItemData("Equipment", 250 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Aphotic Edge": ItemData("Equipment", 388 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 1H, The Sequoia, End-Game Zones
    #"Equipment - Diamond Axe": ItemData("Equipment", 136 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Decapitator": ItemData("Equipment", 280 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 2H, Castle Sequoia, End-Game Zones
    "Equipment - Ragebringer": ItemData("Equipment", 274 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 2H, Capital Sequoia, Advanced Zones

    #Daggers
    #"Equipment - Dirk": ItemData("Equipment", 3 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Stabbers": ItemData("Equipment", 63 + equipment_index_offset, ItemClassification.useful), #Tier 1 Regular, Spawning Meadows, Beginner Zones
    #"Equipment - Fishgutter": ItemData("Equipment", 77 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Poisonkiss": ItemData("Equipment", 40 + equipment_index_offset, ItemClassification.useful), #Tier 1 Regular, Pale Grotto, Beginner Zones
    #"Equipment - Shank": ItemData("Equipment", 60 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Dagger": ItemData("Equipment", 95 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1 Regular, Capital Sequoia, Advanced Zones
    "Equipment - Tanto": ItemData("Equipment", 192 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Ninja, Okimoto N.S., Advanced Zones
    "Equipment - Butterfly": ItemData("Equipment", 203 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Ninja, Okimoto N.S., Advanced Zones
    #"Equipment - Kris": ItemData("Equipment", 202 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Ambush Knife": ItemData("Equipment", 184 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Regular, Greenshire Reprise, Advanced Zones
    #"Equipment - Rondel": ItemData("Equipment", 204 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Silver Dagger": ItemData("Equipment", 113 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Dagger": ItemData("Equipment", 159 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Parry Knife": ItemData("Equipment", 397 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Ninja, Salmon River, Advanced Zones
    #"Equipment - Janbiya": ItemData("Equipment", 392 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Sai": ItemData("Equipment", 396 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Kodachi": ItemData("Equipment", 400 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Butter Cutter": ItemData("Equipment", 198 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Regular, Poko Poko Desert, Advanced Zones
    "Equipment - Soul Kris": ItemData("Equipment", 305 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Regular, Shoudu Province, Expert Zones
    #"Equipment - Gouger": ItemData("Equipment", 61 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Fanged Knife": ItemData("Equipment", 526 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Cinquedea": ItemData("Equipment", 393 + equipment_index_offset, ItemClassification.useful), #from Delende fisher; Tier 3 Regular, Delende, Beginner Zones
    #"Equipment - Gold Dagger": ItemData("Equipment", 140 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Kowakizashi": ItemData("Equipment", 398 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Bone Knife": ItemData("Equipment", 395 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Poignard": ItemData("Equipment", 394 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Flamespike": ItemData("Equipment", 72 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 Regular, Jidamba Tangle, Expert Zones
    #"Equipment - Master Dagger": ItemData("Equipment", 269 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Sange": ItemData("Equipment", 317 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 Ninja, The Sequoia, End-Game Zones
    "Equipment - Yasha": ItemData("Equipment", 318 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Ninja, Shoudu Province, Expert Zones
    #"Equipment - Legend Spike": ItemData("Equipment", 315 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Eclipse": ItemData("Equipment", 41 + equipment_index_offset, ItemClassification.useful), Capital Sequoia shady shop guy
    #"Equipment - Mage Masher": ItemData("Equipment", 282 + equipment_index_offset, ItemClassification.useful), Capital Sequoia shady shop guy
    "Equipment - Mages Pike": ItemData("Equipment", 306 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 Regular, The New World, End-Game Zones
    #"Equipment - Diamond Dagger": ItemData("Equipment", 137 + equipment_index_offset, ItemClassification.useful),
    
    #Rapiers
    #"Equipment - Rapier": ItemData("Equipment", 73 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Stinger": ItemData("Equipment", 1 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Toothpick": ItemData("Equipment", 42 + equipment_index_offset, ItemClassification.useful), #Tier 1, Pale Grotto, Beginner Zones
    "Equipment - Craftwork Rapier": ItemData("Equipment", 96 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - Estoc": ItemData("Equipment", 207 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Scarlette": ItemData("Equipment", 206 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Fish Skewer": ItemData("Equipment", 175 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Sara Sara Bazaar, Advanced Zones
    #"Equipment - Silver Rapier": ItemData("Equipment", 114 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Rapier": ItemData("Equipment", 73 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Dueller": ItemData("Equipment", 10 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Poko Poko Desert, Advanced Zones
    #"Equipment - Vulture": ItemData("Equipment", 402 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Falcon Dance": ItemData("Equipment", 408 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Fleuret": ItemData("Equipment", 404 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    #"Equipment - Gold Rapier": ItemData("Equipment", 141 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Epee": ItemData("Equipment", 405 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Windsong": ItemData("Equipment", 407 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, The Chalice of Tar, Expert Zones
    #"Equipment - Master Rapier": ItemData("Equipment", 252 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Nightingale": ItemData("Equipment", 401 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Castle Sequoia, End-Game Zones
    "Equipment - Chartreuse": ItemData("Equipment", 403 + equipment_index_offset, ItemClassification.useful), #Tier 5, Delende, Beginner Zones
    "Equipment - Murgleys": ItemData("Equipment", 406 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5, The Open Sea, Expert Zones
    #"Equipment - Diamond Rapier": ItemData("Equipment", 142 + equipment_index_offset, ItemClassification.useful),
    
    #Katanas
    "Equipment - Craftwork Katana": ItemData("Equipment", 97 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a katana as a treat)
    "Equipment - Tachi": ItemData("Equipment", 399 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Okimoto N.S., Advanced Zones
    #"Equipment - Silver Katana": ItemData("Equipment", 115 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Katana": ItemData("Equipment", 161 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Nansen": ItemData("Equipment", 363 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Mitsutada": ItemData("Equipment", 22 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Hitofuri": ItemData("Equipment", 364 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Kokaiji": ItemData("Equipment", 23 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Gold Katana": ItemData("Equipment", 143 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Hokuken": ItemData("Equipment", 588 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Tomokirimaru": ItemData("Equipment", 366 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Ichimonji": ItemData("Equipment", 362 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Master Katana": ItemData("Equipment", 253 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Muramasa": ItemData("Equipment", 367 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Shoudu Province, Expert Zones
    #"Equipment - Diamond Katana": ItemData("Equipment", 144 + equipment_index_offset, ItemClassification.useful),

    #Spears
    #"Equipment - Short Spear": ItemData("Equipment", 4 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Spear": ItemData("Equipment", 98 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a spear as a treat)
    #"Equipment - Javelin": ItemData("Equipment", 205 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Skewer": ItemData("Equipment", 190 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Cobblestone Crag, Advanced Zones
    "Equipment - Prodder": ItemData("Equipment", 183 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Sequoia, Advanced Zones
    #"Equipment - Silver Spear": ItemData("Equipment", 116 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Spear": ItemData("Equipment", 162 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Trident": ItemData("Equipment", 409 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Salmon River, Advanced Zones
    #"Equipment - Wind Lance": ItemData("Equipment", 410 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Halberd": ItemData("Equipment", 418 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Beaurior Rock, Expert Zones
    #"Equipment - Gold Spear": ItemData("Equipment", 145 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Voulge": ItemData("Equipment", 419 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Radiance": ItemData("Equipment", 417 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Northern Cave, Expert Zones
    "Equipment - Partizan": ItemData("Equipment", 416 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    #"Equipment - Master Spear": ItemData("Equipment", 254 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Incursier": ItemData("Equipment", 563 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Royal Guard": ItemData("Equipment", 275 + equipment_index_offset, ItemClassification.useful,0, 0, 0, 1), #Tier 5, Castle Sequoia, End-Game Zones
    #"Equipment - Gungnir": ItemData("Equipment", 304 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Diamond Spear": ItemData("Equipment", 146 + equipment_index_offset, ItemClassification.useful),
    
    #Scythes
    "Equipment - Battle Scythe": ItemData("Equipment", 6 + equipment_index_offset, ItemClassification.useful), #Tier 1, Proving Meadows, Beginner Zones
    "Equipment - Craftwork Scythe": ItemData("Equipment", 99 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - War Scythe": ItemData("Equipment", 208 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Wind Sickle": ItemData("Equipment", 413 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Silver Scythe": ItemData("Equipment", 117 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Scythe": ItemData("Equipment", 163 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Thresher": ItemData("Equipment", 294 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Grim Scythe": ItemData("Equipment", 293 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Ancient Reservoir, Advanced Zones
    #"Equipment - Great Thresher": ItemData("Equipment", 295 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Frost Reaper": ItemData("Equipment", 414 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Tall Tall Heights, Expert Zones
    #"Equipment - Gold Scythe": ItemData("Equipment", 147 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Ember Scythe": ItemData("Equipment", 589 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Gravedigger": ItemData("Equipment", 415 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Shoudu Province, Expert Zones
    "Equipment - Wind Thresher": ItemData("Equipment", 590 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Quintar Mausoleum, Expert Zones
    #"Equipment - Master Scythe": ItemData("Equipment", 255 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Adjudicator": ItemData("Equipment", 245 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Twilight": ItemData("Equipment", 412 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Arctic Chill": ItemData("Equipment", 556 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Diamond Scythe": ItemData("Equipment", 148 + equipment_index_offset, ItemClassification.useful),

    #Bows
    "Equipment - Craftwork Bow": ItemData("Equipment", 105 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a bow as a treat)
    #"Equipment - Short Bow": ItemData("Equipment", 7 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Hunting Bow": ItemData("Equipment", 181 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Rolling Quintar Fields, Advanced Zones
    #"Equipment - Long Bow": ItemData("Equipment", 209 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Silver Bow": ItemData("Equipment", 118 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Bow": ItemData("Equipment", 164 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Battle Bow": ItemData("Equipment", 297 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Composite Bow": ItemData("Equipment", 296 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Habins Bow": ItemData("Equipment", 222 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Razor Bow": ItemData("Equipment", 298 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Elven Bow": ItemData("Equipment", 421 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Gold Bow": ItemData("Equipment", 149 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Spore Shooter": ItemData("Equipment", 180 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - War Bow": ItemData("Equipment", 300 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Siege Bow": ItemData("Equipment", 301 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Rune Bow": ItemData("Equipment", 299 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    #"Equipment - Master Bow": ItemData("Equipment", 256 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Panakeia": ItemData("Equipment", 530 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artemis": ItemData("Equipment", 281 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Dream Hunter": ItemData("Equipment", 420 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Castle Sequoia, End-Game Zones
    #"Equipment - Diamond Bow": ItemData("Equipment", 150 + equipment_index_offset, ItemClassification.useful),

    #Staves
    #"Equipment - Short Staff": ItemData("Equipment", 5 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Cedar Staff": ItemData("Equipment", 62 + equipment_index_offset, ItemClassification.useful), #Tier 1 Regular, Spawning Meadows, Beginner Zones
    #"Equipment - Gnarled Root": ItemData("Equipment", 15 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Staff": ItemData("Equipment", 100 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1 Regular, Capital Sequoia, Advanced Zones
    "Equipment - Bone Smasher": ItemData("Equipment", 14 + equipment_index_offset, ItemClassification.useful), #Tier 1 Beating, Delende, Beginner Zones
    "Equipment - Iron Rod": ItemData("Equipment", 426 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Beating, Capital Jail, Advanced Zones
    #"Equipment - Quarterstaff": ItemData("Equipment", 210 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Walking Stick": ItemData("Equipment", 188 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Regular, Cobblestone Crag, Advanced Zones
    #"Equipment - Maplewood": ItemData("Equipment", 211 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Silver Staff": ItemData("Equipment", 119 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Staff": ItemData("Equipment", 165 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Knockout Stick": ItemData("Equipment", 335 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Beating, Sara Sara Bazaar, Advanced Zones
    #"Equipment - Skullbasher": ItemData("Equipment", 427 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Future Sight": ItemData("Equipment", 561 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Battle Staff": ItemData("Equipment", 67 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Digested Staff": ItemData("Equipment", 228 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Nature's Gift'": ItemData("Equipment", 423 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Life Jewel": ItemData("Equipment", 422 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Regular, Overpass (Dione Shrine), Advanced (Expert) Zones
    #"Equipment - Gold Staff": ItemData("Equipment", 151 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - War Staff": ItemData("Equipment", 428 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Apprentice": ItemData("Equipment", 424 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 Regular, Northern Cave, Expert Zones
    "Equipment - Sages Walker": ItemData("Equipment", 425 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 Regular, Slip Glide Ride, Expert Zones
    #"Equipment - Master Staff": ItemData("Equipment", 257 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Beats Stick": ItemData("Equipment", 289 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Staff of Balance": ItemData("Equipment", 290 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Regular, Jidamba Eaclaneya, Expert Zones
    "Equipment - Judgement": ItemData("Equipment", 429 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 Regular, Ancient Labyrinth, End-Game Zones
    #"Equipment - Diamond Staff": ItemData("Equipment", 152 + equipment_index_offset, ItemClassification.useful),

    #Wands
    #"Equipment - Ash Wand": ItemData("Equipment", 8 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Cedar Wand": ItemData("Equipment", 13 + equipment_index_offset, ItemClassification.useful), #Tier 1, Spawning Meadows, Beginner Zones
    #"Equipment - Oak Wand": ItemData("Equipment", 16 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Torch": ItemData("Equipment", 64 + equipment_index_offset, ItemClassification.useful), #Tier 1, Draft Shaft Conduit, Beginner Zones
    #"Equipment - Ink Stick": ItemData("Equipment", 80 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Wand": ItemData("Equipment", 101 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - Soul Wand": ItemData("Equipment", 213 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Static Rod": ItemData("Equipment", 189 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Quintar Nest, Advanced Zones
    #"Equipment - Maple Wand": ItemData("Equipment", 212 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Silver Wand": ItemData("Equipment", 120 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Wand": ItemData("Equipment", 166 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Storm Rod": ItemData("Equipment", 267 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Sara Sara Bazaar, Advanced Zones
    #"Equipment - Baton": ItemData("Equipment", 434 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Cursegiver": ItemData("Equipment", 432 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, The Undercity, Expert Zones
    #"Equipment - Effigy": ItemData("Equipment", 433 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Gold Wand": ItemData("Equipment", 153 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Rune Wand": ItemData("Equipment", 435 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Lands End, Expert Zones
    #"Equipment - Sentinel Rod": ItemData("Equipment", 431 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Stardust Wand": ItemData("Equipment", 430 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Eaclaneya, Expert Zones
    #"Equipment - Master Wand": ItemData("Equipment", 258 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Aura Focus": ItemData("Equipment", 278 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Paladin Wand": ItemData("Equipment", 276 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, The Deep Sea, Expert Zones
    #"Equipment - Obelisk": ItemData("Equipment", 307 + equipment_index_offset, ItemClassification.useful),  #black market shop (Z14_hobo shop)
    "Equipment - Flameseeker": ItemData("Equipment", 358 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Jidamba Eaclaneya, Expert Zones
    #"Equipment - Diamond Wand": ItemData("Equipment", 154 + equipment_index_offset, ItemClassification.useful),

    #Books
    #"Equipment - Moby Dick": ItemData("Equipment", 51 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Orylei": ItemData("Equipment", 65 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Pages": ItemData("Equipment", 102 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a book as a treat)
    #"Equipment - Encyclopedia": ItemData("Equipment", 214 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Gospel": ItemData("Equipment", 194 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Boomer Society, Advanced Zones
    "Equipment - Paypirbak": ItemData("Equipment", 223 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Salmon Pass, Advanced Zones
    "Equipment - Art of War": ItemData("Equipment", 224 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Okimoto N.S., Advanced Zones
    #"Equipment - Silver Pages": ItemData("Equipment", 121 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Pages": ItemData("Equipment", 167 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Grimoire": ItemData("Equipment", 438 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Blank Pages": ItemData("Equipment", 437 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Sara Sara Beach, Advanced Zones
    "Equipment - Tome of Light": ItemData("Equipment", 439 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Beaurior Volcano, Expert Zones
    #"Equipment - Hydrology": ItemData("Equipment", 441 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Gold Pages": ItemData("Equipment", 155 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Dark Gospel": ItemData("Equipment", 440 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Beaurior Volcano, Expert Zones
    #"Equipment - Divination": ItemData("Equipment", 442 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Malifice": ItemData("Equipment", 443 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Shoudu Province, Expert Zones
    #"Equipment - Master Pages": ItemData("Equipment", 259 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Codex": ItemData("Equipment", 436 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Diamond Pages": ItemData("Equipment", 156 + equipment_index_offset, ItemClassification.useful),

    #Armor
    #Shields
    #"Equipment - Buckler": ItemData("Equipment", 44 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Stout Shield": ItemData("Equipment", 45 + equipment_index_offset, ItemClassification.useful), #Tier 1, Spawning Meadows, Beginner Zones
    "Equipment - Iron Guard": ItemData("Equipment", 68 + equipment_index_offset, ItemClassification.useful), #Tier 1, Yamagawa M.A., Beginner Zones
    "Equipment - Stalwart Shield": ItemData("Equipment", 88 + equipment_index_offset, ItemClassification.useful), #Tier 1, Trial Caves/Skumparadise, Beginner Zones
    "Equipment - Craftwork Shield": ItemData("Equipment", 506 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - Vanguard": ItemData("Equipment", 111 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Duelling Shield": ItemData("Equipment", 215 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Lucky Platter": ItemData("Equipment", 103 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Pipeline, Advanced Zones
    "Equipment - Boomer Shield": ItemData("Equipment", 178 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Boomer Society, Advanced Zones
    #"Equipment - Silver Shield": ItemData("Equipment", 507 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Shield": ItemData("Equipment", 168 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Cross Shield": ItemData("Equipment", 444 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Brass Cross": ItemData("Equipment", 448 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Blood Shield": ItemData("Equipment", 560 + equipment_index_offset, ItemClassification.useful),
    "Equipment - The Immovable": ItemData("Equipment", 451 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    #"Equipment - Cross Guard": ItemData("Equipment", 446 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Mages Platter": ItemData("Equipment", 452 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Salmon River, Advanced Zones
    #"Equipment - Gold Shield": ItemData("Equipment", 447 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Bulkwark": ItemData("Equipment", 449 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Flame Guard": ItemData("Equipment", 450 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Wizards Wall": ItemData("Equipment", 453 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Shoudu Province, Expert Zones
    #"Equipment - Master Shield": ItemData("Equipment", 260 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Turtle Shell": ItemData("Equipment", 445 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Tower Shield": ItemData("Equipment", 344 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Jidamba Tangle, Expert Zones
    "Equipment - Nomads Guard": ItemData("Equipment", 288 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Continental Tram, Expert Zones
    #"Equipment - Ether Shield": ItemData("Equipment", 277 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Mirror Shield": ItemData("Equipment", 246 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Ancient Labyrinth, End-Game Zones
    #"Equipment - Diamond Shield": ItemData("Equipment", 237 + equipment_index_offset, ItemClassification.useful),

    #Heavy Head
    #"Equipment - Chain Helm": ItemData("Equipment", 25 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Sturdy Helm": ItemData("Equipment", 26 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Storm Helm": ItemData("Equipment", 74 + equipment_index_offset, ItemClassification.useful), #Tier 1, Pale Grotto, Beginner Zones
    #"Equipment - Copper Helm": ItemData("Equipment", 69 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Helm": ItemData("Equipment", 508 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - Bronze Helm": ItemData("Equipment", 106 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Scale Helm": ItemData("Equipment", 128 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Iron Helm": ItemData("Equipment", 125 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Jojo Sewers, Advanced Zones
    "Equipment - Battle Helm": ItemData("Equipment", 132 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Jail, Advanced Zones
    #"Equipment - Silver Helm": ItemData("Equipment", 509 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Helm": ItemData("Equipment", 169 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Orion Barbut": ItemData("Equipment", 465 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Iron Barbut": ItemData("Equipment", 468 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Horned Helm": ItemData("Equipment", 464 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    #"Equipment - Gold Helm": ItemData("Equipment", 469 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Cross Helm": ItemData("Equipment", 466 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Insignia Helm": ItemData("Equipment", 470 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Tall Tall Heights, Expert Zones
    "Equipment - Demon Helm": ItemData("Equipment", 467 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    #"Equipment - Master Helm": ItemData("Equipment", 261 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Guts Busby": ItemData("Equipment", 308 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Raid Helm": ItemData("Equipment", 471 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Spellsword Helm": ItemData("Equipment", 292 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Sequoia Athenaeum, Expert Zones
    #"Equipment - Diamond Helm": ItemData("Equipment", 236 + equipment_index_offset, ItemClassification.useful),

    #Heavy Body
    #"Equipment - Breastplate": ItemData("Equipment", 18 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Ring Mail": ItemData("Equipment", 28 + equipment_index_offset, ItemClassification.useful), #Tier 1, Pale Grotto, Beginner Zones
    #"Equipment - Copper Suit": ItemData("Equipment", 29 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Plate of Wolf": ItemData("Equipment", 84 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Underpass, Advanced Zones
    "Equipment - Craftwork Mail": ItemData("Equipment", 510 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - Bronze Suit": ItemData("Equipment", 107 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Scale Mail": ItemData("Equipment", 127 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Iron Armor": ItemData("Equipment", 126 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Jojo Sewers, Advanced Zones
    "Equipment - Battleplate": ItemData("Equipment", 43 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Jail, Advanced Zones
    #"Equipment - Silver Mail": ItemData("Equipment", 511 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Mail": ItemData("Equipment", 170 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Orion Armor": ItemData("Equipment", 455 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Plate of Tiger": ItemData("Equipment", 129 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Plate Mail": ItemData("Equipment", 460 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Knights Plate": ItemData("Equipment", 456 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, The Undercity, Expert Zones
    "Equipment - Bone Mail": ItemData("Equipment", 462 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    #"Equipment - Gold Mail": ItemData("Equipment", 459 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Sky Armor": ItemData("Equipment", 461 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Shoudu Province, Expert Zones
    "Equipment - Plate of Lion": ItemData("Equipment", 130 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Slip Glide Ride, Expert Zones
    #"Equipment - Dragon Mail": ItemData("Equipment", 457 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Demon Plate": ItemData("Equipment", 458 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    #"Equipment - Master Mail": ItemData("Equipment", 262 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Construct Mail": ItemData("Equipment", 272 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Guardian Angel": ItemData("Equipment", 291 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Plate of Whale": ItemData("Equipment", 131 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5, The Open Sea, Expert Zones
    "Equipment - Lunar Mail": ItemData("Equipment", 463 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, The New World, End-Game Zones
    #"Equipment - Diamond Mail": ItemData("Equipment", 235 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Warrior Mail": ItemData("Equipment", 533 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Warlock Mail": ItemData("Equipment", 534 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Aegis Mail": ItemData("Equipment", 536 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Reaper Mail": ItemData("Equipment", 535 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Samurai Mail": ItemData("Equipment", 538 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Valkyrie Mail": ItemData("Equipment", 537 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Beastmaster Mail": ItemData("Equipment", 557 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Mimic Mail": ItemData("Equipment", 548 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    
    #Medium Head
    #"Equipment - Leather Cap": ItemData("Equipment", 24 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Beret": ItemData("Equipment", 27 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Storm Cap": ItemData("Equipment", 75 + equipment_index_offset, ItemClassification.useful), #Tier 1, Seaside Cliffs, Beginner Zones
    "Equipment - Headgear": ItemData("Equipment", 30 + equipment_index_offset, ItemClassification.useful), #Tier 1, Seaside Cliffs, Beginner Zones
    "Equipment - Craftwork Cap": ItemData("Equipment", 512 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - Rugged Hat": ItemData("Equipment", 219 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Spore Blocker": ItemData("Equipment", 195 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Rolling Quintar Fields, Advanced Zones
    #"Equipment - Vikings Hat": ItemData("Equipment", 220 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Silver Cap": ItemData("Equipment", 513 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Cap": ItemData("Equipment", 171 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Combat Band": ItemData("Equipment", 483 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Red Cap": ItemData("Equipment", 233 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Ancient Reservoir, Advanced Zones
    #"Equipment - Bandana": ItemData("Equipment", 484 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Suitor Hat": ItemData("Equipment", 485 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    #"Equipment - Gold Cap": ItemData("Equipment", 520 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Red Hat": ItemData("Equipment", 480 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Pirate Hat": ItemData("Equipment", 481 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Ice fisher in Tall Tall Heights; Tier 4, Tall Tall Heights, Expert Zones
    #"Equipment - Tall, Tall Hat": ItemData("Equipment", 486 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Master Cap": ItemData("Equipment", 263 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Battle Band": ItemData("Equipment", 345 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, The Sequoia, End-Game Zones
    "Equipment - Captains Hat": ItemData("Equipment", 482 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5, Sara Sara Bazaar, Advanced Zones
    #"Equipment - Red Headgear": ItemData("Equipment", 487 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Diamond Cap": ItemData("Equipment", 238 + equipment_index_offset, ItemClassification.useful),

    #Medium Body
    #"Equipment - Leather Outfit": ItemData("Equipment", 17 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Studded Armor": ItemData("Equipment", 35 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Leather Mail": ItemData("Equipment", 36 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Vest": ItemData("Equipment", 514 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a medium body as a treat)
    #"Equipment - Chain Vest": ItemData("Equipment", 217 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Combat Vest": ItemData("Equipment", 218 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Smelly Gi": ItemData("Equipment", 268 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Jojo Sewers, Advanced Zones
    "Equipment - Training Gi": ItemData("Equipment", 229 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Okimoto N.S., Advanced Zones
    "Equipment - Tuxedo": ItemData("Equipment", 176 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Sequoia, Advanced Zones
    #"Equipment - Silver Vest": ItemData("Equipment", 515 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Vest": ItemData("Equipment", 172 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Power Vest": ItemData("Equipment", 472 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Red Coat": ItemData("Equipment", 57 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Ancient Reservoir, Advanced Zones
    #"Equipment - Drifters Vest": ItemData("Equipment", 474 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Bandage Wrap": ItemData("Equipment", 558 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Gaia Vest": ItemData("Equipment", 473 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Brigandine": ItemData("Equipment", 477 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, The Undercity, Expert Zones
    #"Equipment - Gold Vest": ItemData("Equipment", 521 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Onion Gi": ItemData("Equipment", 475 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Martial Vest": ItemData("Equipment", 478 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Judo Gi": ItemData("Equipment", 479 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Tall Tall Heights, Expert Zones
    #"Equipment - Master Vest": ItemData("Equipment", 264 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Quintar Pelt": ItemData("Equipment", 493 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Shadow Gi": ItemData("Equipment", 347 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Shoudu Province, Expert Zones
    #"Equipment - Rex Vest": ItemData("Equipment", 476 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Slime Coat": ItemData("Equipment", 524 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Diamond Vest": ItemData("Equipment", 239 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Monk Vest": ItemData("Equipment", 539 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Rogue Vest": ItemData("Equipment", 540 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Fencer Vest": ItemData("Equipment", 541 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Hunter Vest": ItemData("Equipment", 542 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Ninja Vest": ItemData("Equipment", 543 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Nomad Vest": ItemData("Equipment", 544 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Beatsmith Vest": ItemData("Equipment", 545 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Assassin Vest": ItemData("Equipment", 546 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones

    #Light Head
    #"Equipment - Hemp Hood": ItemData("Equipment", 31 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Cotton Hood": ItemData("Equipment", 32 + equipment_index_offset, ItemClassification.useful), #Tier 1, Delende, Beginner Zones
    "Equipment - Storm Hood": ItemData("Equipment", 76 + equipment_index_offset, ItemClassification.useful), #Tier 1, Delende, Beginner Zones
    #"Equipment - Holy Hat": ItemData("Equipment", 33 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Craftwork Crown": ItemData("Equipment", 516 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - Silk Hat": ItemData("Equipment", 110 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Circlet": ItemData("Equipment", 133 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Quintar Sanctum, Advanced Zones
    #"Equipment - Holy Miter": ItemData("Equipment", 109 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Woven Hood": ItemData("Equipment", 122 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Jail, Advanced Zones
    #"Equipment - Silver Crown": ItemData("Equipment", 517 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Crown": ItemData("Equipment", 173 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Clerics Hood": ItemData("Equipment", 341 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Wizards Hat": ItemData("Equipment", 340 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Fairys Crown": ItemData("Equipment", 352 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Quilted Hat": ItemData("Equipment", 353 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Blood Hat": ItemData("Equipment", 559 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Plague Mask": ItemData("Equipment", 342 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Guard Crown": ItemData("Equipment", 356 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Beaurior Rock, Expert Zones
    #"Equipment - Gold Crown": ItemData("Equipment", 522 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Bronze Hairpin": ItemData("Equipment", 34 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tall Tall Heights fisher; Tier 4, Tall Tall Heights, Expert Zones
    #"Equipment - Regen Crown": ItemData("Equipment", 343 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Ravens Hood": ItemData("Equipment", 348 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Celestial Crown": ItemData("Equipment", 52 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Eaclaneya, Expert Zones
    #"Equipment - Master Crown": ItemData("Equipment", 265 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Pointy Hat": ItemData("Equipment", 531 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, The Deep Sea, Expert Zones
    "Equipment - Vita Crown": ItemData("Equipment", 271 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Ancient Labyrinth, End-Game Zones
    #"Equipment - Pact Crown": ItemData("Equipment", 350 + equipment_index_offset, ItemClassification.useful),  #black market shop (Z14_hobo shop)
    "Equipment - Protector": ItemData("Equipment", 354 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Castle Sequoia, End-Game Zones
    #"Equipment - Diamond Crown": ItemData("Equipment", 240 + equipment_index_offset, ItemClassification.useful),

    #Light Body
    #"Equipment - Hemp Robe": ItemData("Equipment", 19 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Cotton Robe": ItemData("Equipment", 20 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Mages Robe": ItemData("Equipment", 21 + equipment_index_offset, ItemClassification.useful), #Tier 1, Delende, Beginner Zones
    "Equipment - Swimmers Top": ItemData("Equipment", 81 + equipment_index_offset, ItemClassification.useful), #Tier 1, Seaside Cliffs, Beginner Zones
    "Equipment - Craftwork Robe": ItemData("Equipment", 518 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    #"Equipment - Priest Garb": ItemData("Equipment", 216 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Dress": ItemData("Equipment", 134 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Quintar Sanctum, Advanced Zones
    #"Equipment - Silk Shirt": ItemData("Equipment", 108 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Woven Shirt": ItemData("Equipment", 230 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Jail, Advanced Zones
    #"Equipment - Silver Cape": ItemData("Equipment", 519 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Artisan Shirt": ItemData("Equipment", 174 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Wizards Robe": ItemData("Equipment", 124 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Clerics Robe": ItemData("Equipment", 123 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Cosplay Garb": ItemData("Equipment", 336 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Sturdy Cape": ItemData("Equipment", 359 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Shelter Dress": ItemData("Equipment", 357 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Beaurior Rock, Expert Zones
    #"Equipment - Gold Robe": ItemData("Equipment", 523 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Winter Cape": ItemData("Equipment", 325 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Blue Cape": ItemData("Equipment", 360 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Lands End, Expert Zones
    "Equipment - Seekers Garb": ItemData("Equipment", 324 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Slip Glide Ride, Expert Zones
    "Equipment - Ravens Cloak": ItemData("Equipment", 349 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    #"Equipment - Master Cape": ItemData("Equipment", 266 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Archmage Vest": ItemData("Equipment", 337 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Ancient Labyrinth, End-Game Zones
    #"Equipment - Saviors Cape": ItemData("Equipment", 338 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Assassins Cloak": ItemData("Equipment", 273 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, The Depths, End-Game Zones
    "Equipment - Stealth Cape": ItemData("Equipment", 319 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, The Sequoia, End-Game Zones
    #"Equipment - Shell Gown": ItemData("Equipment", 355 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Diamond Robe": ItemData("Equipment", 241 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Cleric Robe": ItemData("Equipment", 547 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Wizard Robe": ItemData("Equipment", 549 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Shaman Robe": ItemData("Equipment", 550 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Scholar Robe": ItemData("Equipment", 551 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Chemist Robe": ItemData("Equipment", 552 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Dervish Robe": ItemData("Equipment", 553 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Weaver Robe": ItemData("Equipment", 554 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Summoner Robe": ItemData("Equipment", 555 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones

    #Accessories
    "Equipment - Fervor Charm": ItemData("Equipment", 48 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Delende, Beginner Zones
    "Equipment - Dodge Charm": ItemData("Equipment", 39 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Soiled Den, Beginner Zones
    "Equipment - Earring": ItemData("Equipment", 79 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Delende, Beginner Zones
    "Equipment - Bracer": ItemData("Equipment", 70 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Delende and Seaside Cliffs, Beginner Zones
    "Equipment - Jewel of Defense": ItemData("Equipment", 50 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Seaside Cliffs, Beginner Zones
    "Equipment - Scope Bit": ItemData("Equipment", 226 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Seaside Cliffs and Quintar Nest, Beginner Zones
    "Equipment - Protect Amulet": ItemData("Equipment", 49 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Delende, Beginner Zones
    #"Equipment - Wasps Stinger": ItemData("Equipment", 86 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Gem Ring": ItemData("Equipment", 332 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Earth Bangle": ItemData("Equipment", 82 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Water Bangle": ItemData("Equipment", 83 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Looters Ring": ItemData("Equipment", 54 + equipment_index_offset, ItemClassification.useful), #Tier 1 Unique, Delende and Greenshire Reprise, Beginner Zones
    "Equipment - Burglars Glove": ItemData("Equipment", 53 + equipment_index_offset, ItemClassification.useful), #Tier 1 Unique, Spawning Meadows and Proving Meadows, Beginner Zones
    "Equipment - Torpid Cuffs": ItemData("Equipment", 331 + equipment_index_offset, ItemClassification.useful), #Tier 1 Unique, Yamagawa M.A., Beginner Zones
    "Equipment - Squirrel Dung": ItemData("Equipment", 85 + equipment_index_offset, ItemClassification.useful), #Tier 1 Unique, Spawning Meadows, Beginner Zones
    "Equipment - Fang Pendant": ItemData("Equipment", 196 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Shop (Capital), Capital Sequoia, Advanced Zones
    "Equipment - Mana Ring": ItemData("Equipment", 38 + equipment_index_offset, ItemClassification.useful), #Tier 2 Shop (Capital), Skumparadise, Beginner Zones
    "Equipment - Awake Ring": ItemData("Equipment", 87 + equipment_index_offset, ItemClassification.useful), #Tier 2 Shop (Capital), Skumparadise, Beginner Zones
    #"Equipment - Prayer Beads": ItemData("Equipment", 186 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Shell Amulet": ItemData("Equipment", 179 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Shop (Capital), Greenshire Reprise, Advanced Zones
    #"Equipment - Samurais Glove": ItemData("Equipment", 185 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Magic Finder": ItemData("Equipment", 323 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Loot, Okimoto N.S., Advanced Zones
    "Equipment - Learners Pin": ItemData("Equipment", 492 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Unique, Capital Sequoia, Advanced Zones
    "Equipment - Givers Ring": ItemData("Equipment", 182 + equipment_index_offset, ItemClassification.useful, 0, 1),#Tier 2 Unique, Capital Sequoia, Advanced Zones
    "Equipment - Aggro Band": ItemData("Equipment", 505 + equipment_index_offset, ItemClassification.useful, 0, 1), #Delende fisher; Tier 2 Unique, Delende, Advanced Zones
    #"Equipment - Hemoring": ItemData("Equipment", 56 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Float Shoes": ItemData("Equipment", 193 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Unique, Okimoto N.S. and Lake Delende, Advanced Zones
    #"Equipment - Hope Cross": ItemData("Equipment", 225 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Defense Shifter": ItemData("Equipment", 191 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Shop (Sara Sara), Ancient Reservoir, Advanced Zones
    "Equipment - Resist Shifter": ItemData("Equipment", 221 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Shop (Sara Sara), Ancient Reservoir, Advanced Zones
    #"Equipment - Casters Ring": ItemData("Equipment", 9 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Fearsome Ring": ItemData("Equipment", 504 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Crit Fang": ItemData("Equipment", 502 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Dancing Shoes": ItemData("Equipment", 333 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Bulk Belt": ItemData("Equipment", 243 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Poison Talon": ItemData("Equipment", 334 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - First Strike Mitt": ItemData("Equipment", 501 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Menders Ring": ItemData("Equipment", 529 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Kitsune Mask": ItemData("Equipment", 503 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Pact Ring": ItemData("Equipment", 496 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Scope Specs": ItemData("Equipment", 562 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Loot, Poko Poko Desert, Advanced Zones
    #"Equipment - Loot Finder": ItemData("Equipment", 326 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Quiet Shoes": ItemData("Equipment", 495 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Knicked Knackers": ItemData("Equipment", 232 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Unique, Shoudu Province, Expert Zones
    "Equipment - Looters Pin": ItemData("Equipment", 231 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Unique, Shoudu Province, Expert Zones
    "Equipment - Acrobat Shoes": ItemData("Equipment", 320 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Unique, Shoudu Province, Expert Zones
    #"Equipment - Bone Trophy": ItemData("Equipment", 37 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Gusto Fang": ItemData("Equipment", 47 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Beads of Defense": ItemData("Equipment", 328 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 4 Shop (Tall Tall), Castle Sequoia, End-Game Zones
    #"Equipment - Winter Mitten": ItemData("Equipment", 322 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Glasses": ItemData("Equipment", 327 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tall Tall Heights fisher; Tier 4 Unique, Tall Tall Heights, Expert Zones
    "Equipment - Gusto Charm": ItemData("Equipment", 46 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tall Tall Heights fisher; Tier 4 Unique, Tall Tall Heights, Expert Zones
    "Equipment - Muggers Glove": ItemData("Equipment", 309 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 Unique, Shoudu Province, Expert Zones
    "Equipment - Fursuit": ItemData("Equipment", 490 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #crafted but i think its funny; Tier 5 Crafting, Quintar Reserve, Expert Zones
    #"Equipment - Snow Pendant": ItemData("Equipment", 528 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Ogre Ball": ItemData("Equipment", 78 + equipment_index_offset, ItemClassification.useful),
    "Equipment - Sanity Ring": ItemData("Equipment", 330 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5 Unique, The Open Sea, Expert Zones
    "Equipment - Undead Ring": ItemData("Equipment", 491 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Unique, Quintar Reserve, Expert Zones
    "Equipment - Fairys Ring": ItemData("Equipment", 329 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5 Unique, The Open Sea, Expert Zones
    "Equipment - Oven Mitt": ItemData("Equipment", 321 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Unique, The Deep Sea, Expert Zones
    "Equipment - Autumns Oath": ItemData("Equipment", 234 + equipment_index_offset, ItemClassification.useful), #Tier 5 Unique, Yamagawa M.A., Beginner Zones
    "Equipment - Springs Oath": ItemData("Equipment", 489 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 Unique, Overpass (Okimoto N.S.), Advanced Zones
    "Equipment - Lucky Socks": ItemData("Equipment", 498 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 Unique, Capital Sequoia, Advanced Zones
    "Equipment - Lucky Briefs": ItemData("Equipment", 499 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 Unique, Capital Sequoia, Advanced Zones
    "Equipment - Tall Stand Ring": ItemData("Equipment", 244 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Unique, Shoudu Province, Expert Zones
    "Equipment - Nomads Emblem": ItemData("Equipment", 287 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5 Unique, The Open Sea, Expert Zones
    #"Equipment - Lockon Lense": ItemData("Equipment", 373 + equipment_index_offset, ItemClassification.useful), Quintar Enthusiast battle drop
    "Equipment - Red Hairpin": ItemData("Equipment", 247 + equipment_index_offset, ItemClassification.useful), #Delende fisher;  #Tier 5 Unique, Delende, Beginner Zones
    "Equipment - Stone of Jodan": ItemData("Equipment", 286 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 Unique, Jojo Sewers, Advanced Zones
    "Equipment - Ribbon": ItemData("Equipment", 346 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Unique, Shoudu Province, Expert Zones
    "Equipment - Hand of Midas": ItemData("Equipment", 494 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 Unique, The Sequoia, End-Game Zones
    #"Equipment - Ghendolfs Ring": ItemData("Equipment", 242 + equipment_index_offset, ItemClassification.useful),
    #"Equipment - Master Material": ItemData("Equipment", 284 + equipment_index_offset, ItemClassification.useful),

    #Progressive Equipment
    #the highest equipment id is 590 so these ids start at 600
    "Equipment - Progressive 1H Sword": ItemData("Equipment", 600 + equipment_index_offset, ItemClassification.useful, 4, 1, 7, 1), #1H Sword IDs 11, 71, 89, 93, 200, 377, 375, 380, 372, 381, 303, 411, 316
    "Equipment - Progressive 2H Sword": ItemData("Equipment", 601 + equipment_index_offset, ItemClassification.useful, 1, 2, 2, 1), # 2H Sword IDs 12, 177, 197, 525, 382, 279
    "Equipment - Progressive 1H Axe": ItemData("Equipment", 602 + equipment_index_offset, ItemClassification.useful, 0, 3, 0, 1), # 1H Axe IDs 94, 187, 386, 388
    "Equipment - Progressive 2H Axe": ItemData("Equipment", 603 + equipment_index_offset, ItemClassification.useful, 1, 1, 1, 1), # 2H Axe IDs 2, 385, 280, 274
    "Equipment - Progressive Dagger": ItemData("Equipment", 604 + equipment_index_offset, ItemClassification.useful, 3, 3, 2, 1), # Dagger IDs 63, 40, 95, 184, 198, 305, 393, 72, 306
    "Equipment - Progressive Ninja Dagger": ItemData("Equipment", 605 + equipment_index_offset, ItemClassification.useful, 0, 3, 1, 1), # Ninja Dagger IDs 192, 203, 397, 317, 318
    "Equipment - Progressive Rapier": ItemData("Equipment", 606 + equipment_index_offset, ItemClassification.useful, 2, 3, 3, 1), # Rapier IDs 42, 96, 175, 10, 404, 407, 401, 403, 406
    "Equipment - Progressive Katana": ItemData("Equipment", 607 + equipment_index_offset, ItemClassification.useful, 1, 1, 1, 0), # Katana IDs 97, 399, 367
    "Equipment - Progressive Spear": ItemData("Equipment", 608 + equipment_index_offset, ItemClassification.useful, 1, 3, 3, 1), # Spear IDs 98, 190, 183, 409, 418, 417, 416, 275
    "Equipment - Progressive Scythe": ItemData("Equipment", 609 + equipment_index_offset, ItemClassification.useful, 1, 2, 3, 0), # Scythe IDs 6, 99, 293, 414, 415, 590
    "Equipment - Progressive Bow": ItemData("Equipment", 610 + equipment_index_offset, ItemClassification.useful, 1, 1, 2, 1), # Bow IDs 105, 181, 301, 299, 420
    "Equipment - Progressive Staff": ItemData("Equipment", 611 + equipment_index_offset, ItemClassification.useful, 1, 2, 4, 1), # Staff IDs 62, 100, 188, 422, 424, 425, 290, 429
    "Equipment - Progressive Beating Staff": ItemData("Equipment", 612 + equipment_index_offset, ItemClassification.useful, 1, 2, 0, 0), # Beating Staff IDs 14, 426, 335
    "Equipment - Progressive Wand": ItemData("Equipment", 613 + equipment_index_offset, ItemClassification.useful, 2, 3, 5, 0), # Wand IDs 13, 64, 101, 189, 267, 432, 435, 430, 276, 358
    "Equipment - Progressive Book": ItemData("Equipment", 614 + equipment_index_offset, ItemClassification.useful, 1, 4, 3, 0), # Book IDs 102, 194, 223, 224, 437, 439, 440, 443
    "Equipment - Progressive Shield": ItemData("Equipment", 615 + equipment_index_offset, ItemClassification.useful, 3, 4, 5, 1), # Shield IDs 45, 68, 88, 506, 103, 178, 451, 452, 450, 453, 344, 288, 246
    "Equipment - Progressive Heavy Head": ItemData("Equipment", 616 + equipment_index_offset, ItemClassification.useful, 1, 3, 4, 0), # Heavy Head IDs 74, 508, 125, 132, 464, 470, 467, 292
    "Equipment - Progressive Heavy Body": ItemData("Equipment", 617 + equipment_index_offset, ItemClassification.useful, 1, 4, 14, 1), # Heavy Body IDs 28, 84, 510, 126, 43, 456, 462, 461, 130, 458, 131, 463, 533, 534, 536, 535, 538, 537, 557, 548
    "Equipment - Progressive Medium Head": ItemData("Equipment", 618 + equipment_index_offset, ItemClassification.useful, 2, 4, 2, 1), # Medium Head IDs 75, 30, 512, 195, 233, 485, 481, 345, 482
    "Equipment - Progressive Medium Body": ItemData("Equipment", 619 + equipment_index_offset, ItemClassification.useful, 1, 4, 12, 0), # Medium Body IDs 514, 268, 229, 176, 57, 473, 477, 479, 347, 539, 540, 541, 542, 543, 544, 545, 546
    "Equipment - Progressive Light Head": ItemData("Equipment", 620 + equipment_index_offset, ItemClassification.useful, 2, 3, 6, 2), # Light Head IDs 32, 76, 516, 133, 122, 342, 356, 34, 348, 52, 531, 271, 354
    "Equipment - Progressive Light Body": ItemData("Equipment", 621 + equipment_index_offset, ItemClassification.useful, 2, 3, 12, 3), # Light Body IDs 21, 81, 518, 134, 230, 357, 360, 324, 349, 337, 273, 319, 547, 549, 550, 551, 552, 553, 554, 555

    #Maps
    "Item - Spawning Meadows Map": ItemData("Item", 73 + item_index_offset, ItemClassification.useful),
    "Item - Delende Map": ItemData("Item", 74 + item_index_offset, ItemClassification.useful),
    "Item - Pale Grotto Map": ItemData("Item", 75 + item_index_offset, ItemClassification.useful),
    "Item - Seaside Cliffs Map": ItemData("Item", 76 + item_index_offset, ItemClassification.useful),
    "Item - Draft Shaft Conduit Map": ItemData("Item", 77 + item_index_offset, ItemClassification.useful),
    "Item - Proving Meadows Map": ItemData("Item", 78 + item_index_offset, ItemClassification.useful),
    "Item - Soiled Den Map": ItemData("Item", 79 + item_index_offset, ItemClassification.useful),
    "Item - Yamagawa M.A. Map": ItemData("Item", 80 + item_index_offset, ItemClassification.useful),
    "Item - Skumparadise Map": ItemData("Item", 82 + item_index_offset, ItemClassification.useful),
    "Item - Capital Courtyard Map": ItemData("Item", 83 + item_index_offset, ItemClassification.useful),
    "Item - Capital Sequoia Map": ItemData("Item", 84 + item_index_offset, ItemClassification.useful),
    "Item - Jojo Sewers Map": ItemData("Item", 85 + item_index_offset, ItemClassification.useful),
    "Item - Greenshire Reprise Map": ItemData("Item", 86 + item_index_offset, ItemClassification.useful),
    "Item - Mercury Shrine Map": ItemData("Item", 87 + item_index_offset, ItemClassification.useful),
    "Item - Boomer Society Map": ItemData("Item", 89 + item_index_offset, ItemClassification.useful),
    "Item - Rolling Quintar Fields Map": ItemData("Item", 90 + item_index_offset, ItemClassification.useful),
    "Item - Quintar Nest Map": ItemData("Item", 92 + item_index_offset, ItemClassification.useful),
    "Item - Capital Jail Map": ItemData("Item", 94 + item_index_offset, ItemClassification.useful),
    "Item - Cobblestone Crag Map": ItemData("Item", 96 + item_index_offset, ItemClassification.useful),
    "Item - Okimoto N.S. Map": ItemData("Item", 98 + item_index_offset, ItemClassification.useful),
    "Item - Salmon Pass Map": ItemData("Item", 99 + item_index_offset, ItemClassification.useful),
    "Item - Salmon River Map": ItemData("Item", 100 + item_index_offset, ItemClassification.useful),
    "Item - Poseidon Shrine Map": ItemData("Item", 101 + item_index_offset, ItemClassification.useful),
    "Item - Poko Poko Desert Map": ItemData("Item", 103 + item_index_offset, ItemClassification.useful),
    "Item - Sara Sara Bazaar Map": ItemData("Item", 104 + item_index_offset, ItemClassification.useful),
    "Item - Sara Sara Beach Map": ItemData("Item", 105 + item_index_offset, ItemClassification.useful),
    "Item - Ancient Reservoir Map": ItemData("Item", 106 + item_index_offset, ItemClassification.useful),
    "Item - Shoudu Province Map": ItemData("Item", 107 + item_index_offset, ItemClassification.useful),
    "Item - The Undercity Map": ItemData("Item", 108 + item_index_offset, ItemClassification.useful),
    "Item - Beaurior Volcano Map": ItemData("Item", 109 + item_index_offset, ItemClassification.useful),
    "Item - Beaurior Rock Map": ItemData("Item", 110 + item_index_offset, ItemClassification.useful),
    "Item - The Sequoia Map": ItemData("Item", 111 + item_index_offset, ItemClassification.useful),
    "Item - Tall Tall Heights Map": ItemData("Item", 112 + item_index_offset, ItemClassification.useful),
    "Item - Slip Glide Ride Map": ItemData("Item", 113 + item_index_offset, ItemClassification.useful),
    "Item - Ganymede Shrine Map": ItemData("Item", 117 + item_index_offset, ItemClassification.useful),
    "Item - Quintar Reserve Map": ItemData("Item", 119 + item_index_offset, ItemClassification.useful),
    "Item - Quintar Sanctum Map": ItemData("Item", 120 + item_index_offset, ItemClassification.useful),
    "Item - Lake Delende Map": ItemData("Item", 121 + item_index_offset, ItemClassification.useful),
    "Item - Jidamba Tangle Map": ItemData("Item", 122 + item_index_offset, ItemClassification.useful),
    "Item - Jidamba Eaclaneya Map": ItemData("Item", 123 + item_index_offset, ItemClassification.useful),
    "Item - The Deep Sea Map": ItemData("Item", 124 + item_index_offset, ItemClassification.useful),
    "Item - The New World Map": ItemData("Item", 125 + item_index_offset, ItemClassification.useful),
    "Item - Continental Tram Map": ItemData("Item", 126 + item_index_offset, ItemClassification.useful),
    "Item - Castle Ramparts Map": ItemData("Item", 127 + item_index_offset, ItemClassification.useful),
    "Item - Salmon Bay Map": ItemData("Item", 128 + item_index_offset, ItemClassification.useful),
    "Item - Lands End Map": ItemData("Item", 130 + item_index_offset, ItemClassification.useful),
    "Item - Capital Pipeline Map": ItemData("Item", 170 + item_index_offset, ItemClassification.useful),
    "Item - Northern Cave Map": ItemData("Item", 194 + item_index_offset, ItemClassification.useful),
    "Item - The Depths Map": ItemData("Item", 195 + item_index_offset, ItemClassification.useful),
    "Item - The Open Sea Map": ItemData("Item", 198 + item_index_offset, ItemClassification.useful),
    "Item - Dione Shrine Map": ItemData("Item", 199 + item_index_offset, ItemClassification.useful),
    "Item - Neptune Shrine Map": ItemData("Item", 206 + item_index_offset, ItemClassification.useful),
    "Item - Castle Sequoia Map": ItemData("Item", 209 + item_index_offset, ItemClassification.useful),
    "Item - Ancient Labyrinth Map": ItemData("Item", 210 + item_index_offset, ItemClassification.useful),
    "Item - Quintar Mausoleum Map": ItemData("Item", 211 + item_index_offset, ItemClassification.useful),
    "Item - Basement Map": ItemData("Item", 213 + item_index_offset, ItemClassification.useful),
    "Item - Trial Caves Map": ItemData("Item", 214 + item_index_offset, ItemClassification.useful),
    "Item - Overpass Map": ItemData("Item", 215 + item_index_offset, ItemClassification.useful),
    "Item - Underpass Map": ItemData("Item", 216 + item_index_offset, ItemClassification.useful),
    "Item - River Cats Ego Map": ItemData("Item", 217 + item_index_offset, ItemClassification.useful),
    "Item - Northern Stretch Map": ItemData("Item", 218 + item_index_offset, ItemClassification.useful),
    "Item - Eastern Chasm Map": ItemData("Item", 219 + item_index_offset, ItemClassification.useful),
    "Item - Sequoia Athenaeum Map": ItemData("Item", 220 + item_index_offset, ItemClassification.useful),
    "Item - The Chalice of Tar Map": ItemData("Item", 221 + item_index_offset, ItemClassification.useful),
    "Item - Flyers Crag Map": ItemData("Item", 222 + item_index_offset, ItemClassification.useful),
    "Item - Flyers Lookout Map": ItemData("Item", 223 + item_index_offset, ItemClassification.useful),
    "Item - Jade Cavern Map": ItemData("Item", 228 + item_index_offset, ItemClassification.useful),
    "Item - The Old World Map": ItemData("Item", 254 + item_index_offset, ItemClassification.useful),

    #Currency
    #"Currency": ItemData("Currency", 0 + index_offset, ItemClassification.filler),

    #Summons
    "Summon - Shaku": ItemData("Summon", 223 + summon_index_offset, ItemClassification.useful),
    "Summon - Pamoa": ItemData("Summon", 224 + summon_index_offset, ItemClassification.useful),
    "Summon - Guaba": ItemData("Summon", 225 + summon_index_offset, ItemClassification.useful),
    "Summon - Niltsi": ItemData("Summon", 226 + summon_index_offset, ItemClassification.useful),
    "Summon - Ioske": ItemData("Summon", 227 + summon_index_offset, ItemClassification.useful),
    "Summon - Coyote": ItemData("Summon", 228 + summon_index_offset, ItemClassification.useful),
    # "Summon - Pinga": ItemData("Summon", 230 + summon_index_offset, ItemClassification.useful), (commented out bc you start with Pinga as a summoner)
    "Summon - Tira": ItemData("Summon", 231 + summon_index_offset, ItemClassification.useful),
    "Summon - Juses": ItemData("Summon", 232 + summon_index_offset, ItemClassification.useful),
    "Summon - Pah": ItemData("Summon", 234 + summon_index_offset, ItemClassification.useful),

    #Monster Abilities for Scholar
    "Scholar - Roost": ItemData("Scholar", 25 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Lucky Dice": ItemData("Scholar", 70 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Sun Bath": ItemData("Scholar", 101 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Sleep Aura": ItemData("Scholar", 186 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Regenerate": ItemData("Scholar", 197 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Reverse Polarity": ItemData("Scholar", 198 + scholar_index_offset, ItemClassification.progression), #left in pool so you can merc Gran
    "Scholar - Barrier": ItemData("Scholar", 199 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - MP Sickle": ItemData("Scholar", 200 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Adrenaline": ItemData("Scholar", 202 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Fire Breath": ItemData("Scholar", 205 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Explode": ItemData("Scholar", 206 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Whirlwind": ItemData("Scholar", 207 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Atmoshear": ItemData("Scholar", 213 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Build Life": ItemData("Scholar", 245 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Aero": ItemData("Scholar", 264 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Insult": ItemData("Scholar", 363 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Infusion": ItemData("Scholar", 364 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Overload": ItemData("Scholar", 365 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Reflection": ItemData("Scholar", 366 + scholar_index_offset, ItemClassification.useful, 0, 1),
    "Scholar - Lifegiver": ItemData("Scholar", 376 + scholar_index_offset, ItemClassification.useful, 0, 1),
}

progressive_equipment: Tuple[str, ...] = (
    "Equipment - Progressive 1H Sword",
    "Equipment - Progressive 2H Sword",
    "Equipment - Progressive 1H Axe",
    "Equipment - Progressive 2H Axe",
    "Equipment - Progressive Dagger",
    "Equipment - Progressive Ninja Dagger",
    "Equipment - Progressive Rapier",
    "Equipment - Progressive Katana",
    "Equipment - Progressive Spear",
    "Equipment - Progressive Scythe",
    "Equipment - Progressive Bow",
    "Equipment - Progressive Staff",
    "Equipment - Progressive Beating Staff",
    "Equipment - Progressive Wand",
    "Equipment - Progressive Book",
    "Equipment - Progressive Shield",
    "Equipment - Progressive Heavy Head",
    "Equipment - Progressive Heavy Body",
    "Equipment - Progressive Medium Head", 
    "Equipment - Progressive Medium Body", 
    "Equipment - Progressive Light Head",
    "Equipment - Progressive Light Body",
    )

non_progressive_equipment: Tuple[str, ...] = (
    #Weapons
    #Swords
    #"Equipment - Short Sword",
    "Equipment - Iron Sword",
    "Equipment - Contract",
    "Equipment - Help the Prince",
    "Equipment - Craftwork Sword",
    "Equipment - Broadsword",
    "Equipment - Sharp Sword",
    #"Equipment - Razor Edge",
    #"Equipment - Silver Sword",
    #"Equipment - Artisan Sword",
    #"Equipment - Longsword",
    "Equipment - Boomer Sword",
    #"Equipment - Digested Sword",
    #"Equipment - Scimitar",
    "Equipment - Cutlass",
    "Equipment - Cold Touch",
    #"Equipment - Burning Blade",
    #"Equipment - Gold Sword",
    #"Equipment - War Sword",
    "Equipment - Bloodbind",
    "Equipment - Temporal Blade",
    #"Equipment - Highland Blade",
    #"Equipment - Hydra Edge",
    "Equipment - Defender",
    #"Equipment - Crystal Sword",
    "Equipment - Conquest",
    "Equipment - Flame Sword",
    #"Equipment - Master Sword",
    "Equipment - Rune Sword",
    #"Equipment - Auduril",
    #"Equipment - Master Bigsword",
    #"Equipment - Training Sword",
    #"Equipment - Life Line",
    "Equipment - Soul Keeper",
    "Equipment - Crabs Claw",
    "Equipment - Kings Guard",
    #"Equipment - Diamond Sword",
    #"Equipment - Balrog",
    "Equipment - Oily Sword",

    #Axes
    #"Equipment - Hand Axe",
    "Equipment - Craftwork Axe",
    "Equipment - Cleaver",
    #"Equipment - Chopper",
    "Equipment - Hunting Axe",
    #"Equipment - Silver Axe",
    #"Equipment - Stone Splitter",
    #"Equipment - Broadaxe",
    #"Equipment - Artisan Axe",
    "Equipment - Hatchet",
    #"Equipment - Axe of Light",
    #"Equipment - Gold Axe",
    #"Equipment - War Axe",
    #"Equipment - Berserker Axe",
    "Equipment - Gaia Axe",
    #"Equipment - Master Axe",
    #"Equipment - Ancient Axe",
    #"Equipment - Master Bigaxe",
    "Equipment - Aphotic Edge",
    #"Equipment - Diamond Axe",
    "Equipment - Decapitator",
    "Equipment - Ragebringer",

    #Daggers
    #"Equipment - Dirk",
    "Equipment - Stabbers",
    #"Equipment - Fishgutter",
    "Equipment - Poisonkiss",
    #"Equipment - Shank",
    "Equipment - Craftwork Dagger",
    "Equipment - Tanto",
    "Equipment - Butterfly",
    #"Equipment - Kris",
    "Equipment - Ambush Knife",
    #"Equipment - Rondel",
    #"Equipment - Silver Dagger",
    #"Equipment - Artisan Dagger",
    "Equipment - Parry Knife",
    #"Equipment - Janbiya",
    #"Equipment - Sai",
    #"Equipment - Kodachi",
    "Equipment - Butter Cutter",
    "Equipment - Soul Kris",
    #"Equipment - Gouger",
    #"Equipment - Fanged Knife",
    "Equipment - Cinquedea",
    #"Equipment - Gold Dagger",
    #"Equipment - Kowakizashi",
    #"Equipment - Bone Knife",
    #"Equipment - Poignard",
    "Equipment - Flamespike",
    #"Equipment - Master Dagger",
    "Equipment - Sange",
    "Equipment - Yasha",
    #"Equipment - Legend Spike",
    #"Equipment - Eclipse",
    #"Equipment - Mage Masher",
    "Equipment - Mages Pike",
    #"Equipment - Diamond Dagger",

    #Rapiers
    #"Equipment - Rapier",
    #"Equipment - Stinger",
    "Equipment - Toothpick",
    "Equipment - Craftwork Rapier",
    #"Equipment - Estoc",
    #"Equipment - Scarlette",
    "Equipment - Fish Skewer",
    #"Equipment - Silver Rapier",
    #"Equipment - Artisan Rapier",
    "Equipment - Dueller",
    #"Equipment - Vulture",
    #"Equipment - Falcon Dance",
    "Equipment - Fleuret",
    #"Equipment - Gold Rapier",
    #"Equipment - Epee",
    "Equipment - Windsong",
    #"Equipment - Master Rapier",
    "Equipment - Nightingale",
    "Equipment - Chartreuse",
    "Equipment - Murgleys",
    #"Equipment - Diamond Rapier",

    #Katanas
    "Equipment - Craftwork Katana",
    "Equipment - Tachi",
    #"Equipment - Silver Katana",
    #"Equipment - Artisan Katana",
    #"Equipment - Nansen",
    #"Equipment - Mitsutada",
    #"Equipment - Hitofuri",
    #"Equipment - Kokaiji",
    #"Equipment - Gold Katana",
    #"Equipment - Hokuken",
    #"Equipment - Tomokirimaru",
    #"Equipment - Ichimonji",
    #"Equipment - Master Katana",
    "Equipment - Muramasa",
    #"Equipment - Diamond Katana",

    #Spears
    #"Equipment - Short Spear",
    "Equipment - Craftwork Spear",
    #"Equipment - Javelin",
    "Equipment - Skewer",
    "Equipment - Prodder",
    #"Equipment - Silver Spear",
    #"Equipment - Artisan Spear",
    "Equipment - Trident",
    #"Equipment - Wind Lance",
    "Equipment - Halberd",
    #"Equipment - Gold Spear",
    #"Equipment - Voulge",
    "Equipment - Radiance",
    "Equipment - Partizan",
    #"Equipment - Master Spear",
    #"Equipment - Incursier",
    "Equipment - Royal Guard",
    #"Equipment - Gungnir",
    #"Equipment - Diamond Spear",

    #Scythes
    "Equipment - Battle Scythe",
    "Equipment - Craftwork Scythe",
    #"Equipment - War Scythe",
    #"Equipment - Wind Sickle",
    #"Equipment - Silver Scythe",
    #"Equipment - Artisan Scythe",
    #"Equipment - Thresher",
    "Equipment - Grim Scythe",
    #"Equipment - Great Thresher",
    "Equipment - Frost Reaper",
    #"Equipment - Gold Scythe",
    #"Equipment - Ember Scythe",
    "Equipment - Gravedigger",
    "Equipment - Wind Thresher",
    #"Equipment - Master Scythe",
    #"Equipment - Adjudicator",
    #"Equipment - Twilight",
    #"Equipment - Arctic Chill",
    #"Equipment - Diamond Scythe",

    #Bows
    "Equipment - Craftwork Bow",
    #"Equipment - Short Bow",
    "Equipment - Hunting Bow",
    #"Equipment - Long Bow",
    #"Equipment - Silver Bow",
    #"Equipment - Artisan Bow",
    #"Equipment - Battle Bow",
    #"Equipment - Composite Bow",
    #"Equipment - Habins Bow",
    #"Equipment - Razor Bow",
    #"Equipment - Elven Bow",
    #"Equipment - Gold Bow",
    #"Equipment - Spore Shooter",
    #"Equipment - War Bow",
    "Equipment - Siege Bow",
    "Equipment - Rune Bow",
    #"Equipment - Master Bow",
    #"Equipment - Panakeia",
    #"Equipment - Artemis",
    "Equipment - Dream Hunter",
    #"Equipment - Diamond Bow",

    #Staves
    #"Equipment - Short Staff",
    "Equipment - Cedar Staff",
    #"Equipment - Gnarled Root",
    "Equipment - Craftwork Staff",
    "Equipment - Bone Smasher",
    "Equipment - Iron Rod",
    #"Equipment - Quarterstaff",
    "Equipment - Walking Stick",
    #"Equipment - Maplewood",
    #"Equipment - Silver Staff",
    #"Equipment - Artisan Staff",
    "Equipment - Knockout Stick",
    #"Equipment - Skullbasher",
    #"Equipment - Future Sight",
    #"Equipment - Battle Staff",
    #"Equipment - Digested Staff",
    #"Equipment - Nature's Gift",
    "Equipment - Life Jewel",
    #"Equipment - Gold Staff",
    #"Equipment - War Staff",
    "Equipment - Apprentice",
    "Equipment - Sages Walker",
    #"Equipment - Master Staff",
    #"Equipment - Beats Stick",
    "Equipment - Staff of Balance",
    "Equipment - Judgement",
    #"Equipment - Diamond Staff",

    #Wands
    #"Equipment - Ash Wand",
    "Equipment - Cedar Wand",
    #"Equipment - Oak Wand",
    "Equipment - Torch",
    #"Equipment - Ink Stick",
    "Equipment - Craftwork Wand",
    #"Equipment - Soul Wand",
    "Equipment - Static Rod",
    #"Equipment - Maple Wand",
    #"Equipment - Silver Wand",
    #"Equipment - Artisan Wand",
    "Equipment - Storm Rod",
    #"Equipment - Baton",
    "Equipment - Cursegiver",
    #"Equipment - Effigy",
    #"Equipment - Gold Wand",
    "Equipment - Rune Wand",
    #"Equipment - Sentinel Rod",
    "Equipment - Stardust Wand",
    #"Equipment - Master Wand",
    #"Equipment - Aura Focus",
    "Equipment - Paladin Wand",
    #"Equipment - Obelisk",
    "Equipment - Flameseeker",
    #"Equipment - Diamond Wand",

    #Books
    #"Equipment - Moby Dick",
    #"Equipment - Orylei",
    "Equipment - Craftwork Pages",
    #"Equipment - Encyclopedia",
    "Equipment - Gospel",
    "Equipment - Paypirbak",
    "Equipment - Art of War",
    #"Equipment - Silver Pages",
    #"Equipment - Artisan Pages",
    #"Equipment - Grimoire",
    "Equipment - Blank Pages",
    "Equipment - Tome of Light",
    #"Equipment - Hydrology",
    #"Equipment - Gold Pages",
    "Equipment - Dark Gospel",
    #"Equipment - Divination",
    "Equipment - Malifice",
    #"Equipment - Master Pages",
    #"Equipment - Codex",
    #"Equipment - Diamond Pages",

    #Armor
    #Shields
    #"Equipment - Buckler",
    "Equipment - Stout Shield",
    "Equipment - Iron Guard",
    "Equipment - Stalwart Shield",
    "Equipment - Craftwork Shield",
    #"Equipment - Vanguard",
    #"Equipment - Duelling Shield",
    "Equipment - Lucky Platter",
    "Equipment - Boomer Shield",
    #"Equipment - Silver Shield",
    #"Equipment - Artisan Shield",
    #"Equipment - Cross Shield",
    #"Equipment - Brass Cross",
    #"Equipment - Blood Shield",
    "Equipment - The Immovable",
    #"Equipment - Cross Guard",
    "Equipment - Mages Platter",
    #"Equipment - Gold Shield",
    #"Equipment - Bulkwark",
    "Equipment - Flame Guard",
    "Equipment - Wizards Wall",
    #"Equipment - Master Shield",
    #"Equipment - Turtle Shell",
    "Equipment - Tower Shield",
    "Equipment - Nomads Guard",
    #"Equipment - Ether Shield",
    "Equipment - Mirror Shield",
    #"Equipment - Diamond Shield",

    #Heavy Head
    #"Equipment - Chain Helm",
    #"Equipment - Sturdy Helm",
    "Equipment - Storm Helm",
    #"Equipment - Copper Helm",
    "Equipment - Craftwork Helm",
    #"Equipment - Bronze Helm",
    #"Equipment - Scale Helm",
    "Equipment - Iron Helm",
    "Equipment - Battle Helm",
    #"Equipment - Silver Helm",
    #"Equipment - Artisan Helm",
    #"Equipment - Orion Barbut",
    #"Equipment - Iron Barbut",
    "Equipment - Horned Helm",
    #"Equipment - Gold Helm",
    #"Equipment - Cross Helm",
    "Equipment - Insignia Helm",
    "Equipment - Demon Helm",
    #"Equipment - Master Helm",
    #"Equipment - Guts Busby",
    #"Equipment - Raid Helm",
    "Equipment - Spellsword Helm",
    #"Equipment - Diamond Helm",

    #Heavy Body
    #"Equipment - Breastplate",
    "Equipment - Ring Mail",
    #"Equipment - Copper Suit",
    "Equipment - Plate of Wolf",
    "Equipment - Craftwork Mail",
    #"Equipment - Bronze Suit",
    #"Equipment - Scale Mail",
    "Equipment - Iron Armor",
    "Equipment - Battleplate",
    #"Equipment - Silver Mail",
    #"Equipment - Artisan Mail",
    #"Equipment - Orion Armor",
    #"Equipment - Plate of Tiger",
    #"Equipment - Plate Mail",
    "Equipment - Knights Plate",
    "Equipment - Bone Mail",
    #"Equipment - Gold Mail",
    "Equipment - Sky Armor",
    "Equipment - Plate of Lion",
    #"Equipment - Dragon Mail",
    "Equipment - Demon Plate",
    #"Equipment - Master Mail",
    #"Equipment - Construct Mail",
    #"Equipment - Guardian Angel",
    "Equipment - Plate of Whale",
    "Equipment - Lunar Mail",
    #"Equipment - Diamond Mail",
    "Equipment - Warrior Mail",
    "Equipment - Warlock Mail",
    "Equipment - Aegis Mail",
    "Equipment - Reaper Mail",
    "Equipment - Samurai Mail",
    "Equipment - Valkyrie Mail",
    "Equipment - Beastmaster Mail",
    "Equipment - Mimic Mail",

    #Medium Head
    #"Equipment - Leather Cap",
    #"Equipment - Beret",
    "Equipment - Storm Cap",
    "Equipment - Headgear",
    "Equipment - Craftwork Cap",
    #"Equipment - Rugged Hat",
    "Equipment - Spore Blocker",
    #"Equipment - Vikings Hat",
    #"Equipment - Silver Cap",
    #"Equipment - Artisan Cap",
    #"Equipment - Combat Band",
    "Equipment - Red Cap",
    #"Equipment - Bandana",
    "Equipment - Suitor Hat",
    #"Equipment - Gold Cap",
    #"Equipment - Red Hat",
    "Equipment - Pirate Hat",
    #"Equipment - Tall, Tall Hat",
    #"Equipment - Master Cap",
    "Equipment - Battle Band",
    "Equipment - Captains Hat",
    #"Equipment - Red Headgear",
    #"Equipment - Diamond Cap",

    #Medium Body
    #"Equipment - Leather Outfit",
    #"Equipment - Studded Armor",
    #"Equipment - Leather Mail",
    "Equipment - Craftwork Vest",
    #"Equipment - Chain Vest",
    #"Equipment - Combat Vest",
    "Equipment - Smelly Gi",
    "Equipment - Training Gi",
    "Equipment - Tuxedo",
    #"Equipment - Silver Vest",
    #"Equipment - Artisan Vest",
    #"Equipment - Power Vest",
    "Equipment - Red Coat",
    #"Equipment - Drifters Vest",
    #"Equipment - Bandage Wrap",
    "Equipment - Gaia Vest",
    "Equipment - Brigandine",
    #"Equipment - Gold Vest",
    #"Equipment - Onion Gi",
    #"Equipment - Martial Vest",
    "Equipment - Judo Gi",
    #"Equipment - Master Vest",
    #"Equipment - Quintar Pelt",
    "Equipment - Shadow Gi",
    #"Equipment - Rex Vest",
    #"Equipment - Slime Coat",
    #"Equipment - Diamond Vest",
    "Equipment - Monk Vest",
    "Equipment - Rogue Vest",
    "Equipment - Fencer Vest",
    "Equipment - Hunter Vest",
    "Equipment - Ninja Vest",
    "Equipment - Nomad Vest",
    "Equipment - Beatsmith Vest",
    "Equipment - Assassin Vest",

    #Light Head
    #"Equipment - Hemp Hood",
    "Equipment - Cotton Hood",
    "Equipment - Storm Hood",
    #"Equipment - Holy Hat",
    "Equipment - Craftwork Crown",
    #"Equipment - Silk Hat",
    "Equipment - Circlet",
    #"Equipment - Holy Miter",
    "Equipment - Woven Hood",
    #"Equipment - Silver Crown",
    #"Equipment - Artisan Crown",
    #"Equipment - Clerics Hood",
    #"Equipment - Wizards Hat",
    #"Equipment - Fairys Crown",
    #"Equipment - Quilted Hat",
    #"Equipment - Blood Hat",
    "Equipment - Plague Mask",
    "Equipment - Guard Crown",
    #"Equipment - Gold Crown",
    "Equipment - Bronze Hairpin",
    #"Equipment - Regen Crown",
    "Equipment - Ravens Hood",
    "Equipment - Celestial Crown",
    #"Equipment - Master Crown",
    "Equipment - Pointy Hat",
    "Equipment - Vita Crown",
    #"Equipment - Pact Crown",
    "Equipment - Protector",
    #"Equipment - Diamond Crown",

    #Light Body
    #"Equipment - Hemp Robe",
    #"Equipment - Cotton Robe",
    "Equipment - Mages Robe",
    "Equipment - Swimmers Top",
    "Equipment - Craftwork Robe",
    #"Equipment - Priest Garb",
    "Equipment - Dress",
    #"Equipment - Silk Shirt",
    "Equipment - Woven Shirt",
    #"Equipment - Silver Cape",
    #"Equipment - Artisan Shirt",
    #"Equipment - Wizards Robe",
    #"Equipment - Clerics Robe",
    #"Equipment - Cosplay Garb",
    #"Equipment - Sturdy Cape",
    "Equipment - Shelter Dress",
    #"Equipment - Gold Robe",
    #"Equipment - Winter Cape",
    "Equipment - Blue Cape",
    "Equipment - Seekers Garb",
    "Equipment - Ravens Cloak",
    #"Equipment - Master Cape",
    "Equipment - Archmage Vest",
    #"Equipment - Saviors Cape",
    "Equipment - Assassins Cloak",
    "Equipment - Stealth Cape",
    #"Equipment - Shell Gown",
    #"Equipment - Diamond Robe",
    "Equipment - Cleric Robe",
    "Equipment - Wizard Robe",
    "Equipment - Shaman Robe",
    "Equipment - Scholar Robe",
    "Equipment - Chemist Robe",
    "Equipment - Dervish Robe",
    "Equipment - Weaver Robe",
    "Equipment - Summoner Robe",
    
    #Accessories not progressive
)

optional_scholar_abilities: Tuple[str, ...] = (
    "Scholar - Roost",
    "Scholar - Lucky Dice",
    "Scholar - Sun Bath",
    "Scholar - Sleep Aura",
    "Scholar - Regenerate",
    #"Scholar - Reverse Polarity" leaving this one always in the pool so you can merc Gran
    "Scholar - Barrier",
    "Scholar - MP Sickle",
    "Scholar - Adrenaline",
    "Scholar - Fire Breath",
    "Scholar - Explode",
    "Scholar - Whirlwind",
    "Scholar - Atmoshear",
    "Scholar - Build Life",
    "Scholar - Aero",
    "Scholar - Insult",
    "Scholar - Infusion",
    "Scholar - Overload",
    "Scholar - Reflection",
    "Scholar - Lifegiver"
)

job_list: Tuple[Job, ...] = (
    Job("Job - Warrior", 0),
    Job("Job - Monk", 5),
    Job("Job - Rogue", 2),
    Job("Job - Cleric", 4),
    Job("Job - Wizard", 3),
    Job("Job - Warlock", 14),
    Job("Job - Fencer", 1),
    Job("Job - Shaman", 8),
    Job("Job - Scholar", 13),
    Job("Job - Aegis", 10),
    Job("Job - Hunter", 7),
    Job("Job - Chemist", 17),
    Job("Job - Reaper", 6),
    Job("Job - Ninja", 18),
    Job("Job - Nomad", 12),
    Job("Job - Dervish", 11),
    Job("Job - Beatsmith", 9),
    Job("Job - Samurai", 20),
    Job("Job - Assassin", 19),
    Job("Job - Valkyrie", 15),
    Job("Job - Summoner", 21),
    Job("Job - Beastmaster", 23),
    Job("Job - Weaver", 16),
    Job("Job - Mimic", 22),
)

filler_items: Tuple[str, ...] = (
    "Item - Tonic",
    "Item - Potion",
    "Item - Z-Potion",
    "Item - Tincture",
    "Item - Ether",
    "Item - Zether",
    "Item - Fenix Juice",
    "Item - Fenix Syrup",
    "Item - Nans Stew",
    "Item - Nans Cocoa",
    "Item - Nans Secret Recipe",
    "Item - Nuts",
    "Item - Milk",
    "Item - Sweet Pop Candy",
    "Item - Sour Pop Candy",
    "Item - Bitter Pop Candy",
    "Item - Decent Cod",
    "Item - Fresh Salmon",
    "Item - Scroll",
    # add currency?
)

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories

def get_random_starting_jobs(self, count:int) -> List[Job]:
    return self.random.sample(job_list, count)
