from BaseClasses import Item, ItemClassification
from .data import POKEMON_DATA, GEN_1_TYPES, GAME_REGIONS

# A random high number to ensure our IDs don't overlap with other games
ITEM_ID_OFFSET = 8574000

# This table acts as the single source of truth for all items in the Pokepelago world.
# We map each item name to its unique ID and its classification (progression, useful, filler).
# This makes scaling the game easy: just add a new item here and the generator handles the rest.
item_data_table = {}

# 1. Add Pokémon Unlocks (Progression)
# These are required to catch a specific Pokémon and unlock its location path.
for i, mon in enumerate(POKEMON_DATA):
    item_data_table[f"{mon['name']} Unlock"] = (ITEM_ID_OFFSET + mon["id"], ItemClassification.progression)

# 2. Add Type Keys (Progression — client-side gating, AP ensures they're reachable early)
# No AP access rules use these; client checks them to determine which types are guessable.
for i, p_type in enumerate(GEN_1_TYPES):
    item_data_table[f"{p_type} Type Key"] = (ITEM_ID_OFFSET + 2000 + i, ItemClassification.progression)

# 3. Add Useful Items
# These help the player but aren't strictly required to finish the game.
item_data_table["Master Ball"] = (ITEM_ID_OFFSET + 3001, ItemClassification.useful)
item_data_table["Pokedex"] = (ITEM_ID_OFFSET + 3002, ItemClassification.useful)
item_data_table["Pokegear"] = (ITEM_ID_OFFSET + 3003, ItemClassification.useful)

# 4. Add Traps
# These are meant to hinder the player.
item_data_table["Small Shuffle Trap"] = (ITEM_ID_OFFSET + 4001, ItemClassification.trap)
item_data_table["Big Shuffle Trap"] = (ITEM_ID_OFFSET + 4002, ItemClassification.trap)
item_data_table["Derpy Mon Trap"] = (ITEM_ID_OFFSET + 4003, ItemClassification.trap)
item_data_table["Release Trap"] = (ITEM_ID_OFFSET + 4004, ItemClassification.trap)

# 5. Region Pass items (Progression)
# One pass per game region. IDs: ITEM_ID_OFFSET + 5000 + region_index (8579000–8579009)
for _i, _region in enumerate(GAME_REGIONS):
    item_data_table[f"{_region} Pass"] = (ITEM_ID_OFFSET + 5000 + _i, ItemClassification.progression)

# For backward compatibility with other files that might still use item_table (name -> id)
item_table = {name: data[0] for name, data in item_data_table.items()}
pokemon_names = [mon["name"] for mon in POKEMON_DATA]

class PokepelagoItem(Item):
    game: str = "Pokepelago"