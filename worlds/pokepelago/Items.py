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
item_data_table["Master Ball"]  = (ITEM_ID_OFFSET + 3001, ItemClassification.useful)
item_data_table["Pokedex"]      = (ITEM_ID_OFFSET + 3002, ItemClassification.useful)
item_data_table["Pokegear"]     = (ITEM_ID_OFFSET + 3003, ItemClassification.useful)

# Pokéballs
item_data_table["Ultra Ball"]   = (ITEM_ID_OFFSET + 3004, ItemClassification.filler)
item_data_table["Great Ball"]   = (ITEM_ID_OFFSET + 3005, ItemClassification.filler)
item_data_table["Net Ball"]     = (ITEM_ID_OFFSET + 3006, ItemClassification.filler)
item_data_table["Dusk Ball"]    = (ITEM_ID_OFFSET + 3007, ItemClassification.filler)
item_data_table["Repeat Ball"]  = (ITEM_ID_OFFSET + 3008, ItemClassification.filler)
item_data_table["Quick Ball"]   = (ITEM_ID_OFFSET + 3009, ItemClassification.filler)

# Medicine
item_data_table["Full Restore"] = (ITEM_ID_OFFSET + 3010, ItemClassification.filler)
item_data_table["Max Potion"]   = (ITEM_ID_OFFSET + 3011, ItemClassification.filler)
item_data_table["Revive"]       = (ITEM_ID_OFFSET + 3012, ItemClassification.filler)
item_data_table["Max Revive"]   = (ITEM_ID_OFFSET + 3013, ItemClassification.filler)
item_data_table["Full Heal"]    = (ITEM_ID_OFFSET + 3014, ItemClassification.filler)
item_data_table["Rare Candy"]   = (ITEM_ID_OFFSET + 3015, ItemClassification.filler)

# Key items / field use
item_data_table["Repel"]        = (ITEM_ID_OFFSET + 3016, ItemClassification.filler)
item_data_table["Super Repel"]  = (ITEM_ID_OFFSET + 3017, ItemClassification.filler)
item_data_table["Escape Rope"]  = (ITEM_ID_OFFSET + 3018, ItemClassification.filler)

# Joke / "nothing" item — purely thematic padding
item_data_table["Magikarp used Splash - but nothing happened!"] = (ITEM_ID_OFFSET + 3019, ItemClassification.filler)

# 4. Add Traps
# These are meant to hinder the player.
item_data_table["Small Shuffle Trap"] = (ITEM_ID_OFFSET + 4001, ItemClassification.trap)
item_data_table["Big Shuffle Trap"]   = (ITEM_ID_OFFSET + 4002, ItemClassification.trap)
item_data_table["Derpy Mon Trap"]     = (ITEM_ID_OFFSET + 4003, ItemClassification.trap)
item_data_table["Release Trap"]       = (ITEM_ID_OFFSET + 4004, ItemClassification.trap)

# 5. Region Pass items (Progression)
# One pass per game region. IDs: ITEM_ID_OFFSET + 5000 + region_index (8579000–8579009)
for _i, _region in enumerate(GAME_REGIONS):
    item_data_table[f"{_region} Pass"] = (ITEM_ID_OFFSET + 5000 + _i, ItemClassification.progression)

# 6. New gate progression items (6xxx range)
# These implement the new lock option systems: legendary gates, trade evolutions, baby Pokémon,
# fossil Pokémon, ultra beasts, paradox Pokémon, and stone-only evolutions.
_GATE_ITEMS = {
    "Gym Badge":       (ITEM_ID_OFFSET + 6000, ItemClassification.progression),  # progressive: 6/7/8 for legendary tiers
    "Link Cable":      (ITEM_ID_OFFSET + 6001, ItemClassification.progression),  # trade evolution gate
    "Daycare":         (ITEM_ID_OFFSET + 6002, ItemClassification.progression),  # baby Pokémon gate (progressive count)
    "Ultra Wormhole":  (ITEM_ID_OFFSET + 6003, ItemClassification.progression),  # ultra beast gate
    "Time Rift":       (ITEM_ID_OFFSET + 6004, ItemClassification.progression),  # paradox Pokémon gate
    "Fossil Restorer": (ITEM_ID_OFFSET + 6005, ItemClassification.progression),  # fossil Pokémon gate
    # Evolutionary stones (6010–6019) — gate stone-only evolved Pokémon
    "Fire Stone":      (ITEM_ID_OFFSET + 6010, ItemClassification.progression),
    "Water Stone":     (ITEM_ID_OFFSET + 6011, ItemClassification.progression),
    "Thunder Stone":   (ITEM_ID_OFFSET + 6012, ItemClassification.progression),
    "Leaf Stone":      (ITEM_ID_OFFSET + 6013, ItemClassification.progression),
    "Moon Stone":      (ITEM_ID_OFFSET + 6014, ItemClassification.progression),
    "Sun Stone":       (ITEM_ID_OFFSET + 6015, ItemClassification.progression),
    "Shiny Stone":     (ITEM_ID_OFFSET + 6016, ItemClassification.progression),
    "Dusk Stone":      (ITEM_ID_OFFSET + 6017, ItemClassification.progression),
    "Dawn Stone":      (ITEM_ID_OFFSET + 6018, ItemClassification.progression),
    "Ice Stone":       (ITEM_ID_OFFSET + 6019, ItemClassification.progression),
    # Cosmetic filler
    "Shiny Charm":     (ITEM_ID_OFFSET + 6020, ItemClassification.filler),
}
item_data_table.update(_GATE_ITEMS)

# Offsets exported for reference (client uses ITEM_ID_OFFSET + these to identify items)
GYM_BADGE_OFFSET = 6000
STONE_OFFSETS: dict = {
    "fire": 6010, "water": 6011, "thunder": 6012, "leaf": 6013, "moon": 6014,
    "sun": 6015, "shiny": 6016, "dusk": 6017, "dawn": 6018, "ice": 6019,
}
SHINY_TOKEN_OFFSET = 6020

# For backward compatibility with other files that might still use item_table (name -> id)
item_table = {name: data[0] for name, data in item_data_table.items()}
pokemon_names = [mon["name"] for mon in POKEMON_DATA]

class PokepelagoItem(Item):
    game: str = "Pokepelago"


# Maps filler category names (used by FillerWeights option) to the items they contain.
# Traps are excluded here — they are controlled separately by the trap_chance option.
FILLER_ITEM_CATEGORIES: dict = {
    "master_ball": ["Master Ball"],
    "pokeballs":   ["Ultra Ball", "Great Ball", "Net Ball", "Dusk Ball", "Repeat Ball", "Quick Ball"],
    "medicine":    ["Full Restore", "Max Potion", "Revive", "Max Revive", "Full Heal", "Rare Candy"],
    "key_items":   ["Repel", "Super Repel", "Escape Rope", "Pokedex", "Pokegear"],
    "splash":      ["Magikarp used Splash - but nothing happened!"],
}