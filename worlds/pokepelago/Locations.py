from BaseClasses import Location
from .data import POKEMON_DATA, GEN_1_TYPES

# Shifted away from item IDs (8574000) to prevent collisions.
LOCATION_ID_OFFSET = 8560000

# We create a dictionary of all the locations where items can be hidden.
location_table = {}

# 1. "Oak's Lab" Starting Locations (Free checks to kickstart the logic)
starting_locations = [
    "Oak's Parcel Delivery", "Pokedex Received", "Mom's Running Shoes", "Town Map Received",
    "Professor Oak's Advice", "Boulder Badge (Replica)", "Old Amber (Replica)", "Helix Fossil (Replica)",
]
for i, name in enumerate(starting_locations):
    location_table[name] = LOCATION_ID_OFFSET + 100_000 + i

# 2. Pokémon Guess Locations (The core grid)
for mon in POKEMON_DATA:
    location_table[f"Guess {mon['name']}"] = LOCATION_ID_OFFSET + mon["id"]

# 3. Global Milestone Locations (Rewards for total catches)
# Optimized Tapered milestones: Dense early (for randomizer stepping stones), sparse late (for sphere depth compression).
GLOBAL_MILESTONES = [1, 2, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 250, 400, 600, 800, 1000]
# Specific Max-Pokemon milestones (Gen-specific goals)
goal_milestones = [148, 248, 383, 490, 646, 718, 806, 895, 1022]
milestones = sorted(list(set(GLOBAL_MILESTONES + goal_milestones)))

for count in milestones:
    location_table[f"Guessed {count} Pokemon"] = LOCATION_ID_OFFSET + 10_000 + count

# 4. Type-Specific Milestones
# Calculate how many of each type exist.
type_counts = {t: 0 for t in GEN_1_TYPES}
for mon in POKEMON_DATA:
    for t in mon["types"]:
        if t in type_counts:
            type_counts[t] += 1

# Starters: Bulbasaur (Grass/Poison), Charmander (Fire), Squirtle (Water).
starter_type_counts = {
    "Grass": 1,
    "Poison": 1,
    "Fire": 1,
    "Water": 1
}

TYPE_MILESTONE_STEPS = [1, 2, 5, 10, 20, 35, 50]
milestone_steps = TYPE_MILESTONE_STEPS
for p_type in GEN_1_TYPES:
    # Max NEW catches = Total in type - starters in that type
    max_new = type_counts[p_type] - starter_type_counts.get(p_type, 0)
    for step in milestone_steps:
        if step <= max_new:
            location_table[f"Caught {step} {p_type} Pokemon"] = LOCATION_ID_OFFSET + 20_000 + (GEN_1_TYPES.index(p_type) * 1000) + step

class PokepelagoLocation(Location):
    game: str = "Pokepelago"