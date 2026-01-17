from typing import Dict, Set
from BaseClasses import Location

class PlateUpLocation(Location):
    game = "plateup"

EXCLUDED_LOCATIONS: Set[int] = set()

FRANCHISE_LOCATION_DICT: Dict[str, int] = {}

# Base franchise day labels (first run, no suffix)
base_days = [
    "First Day", "Second Day", "Third Day", "Fourth Day", "Fifth Day",
    "Day 6", "Day 7", "Day 8", "Day 9", "Day 10", "Day 11", "Day 12",
    "Day 13", "Day 14", "Day 15", "Day 16", "Day 17", "Day 18", "Day 19", "Day 20"
]

base_stars = [
    ("First Star", 31),
    ("Second Star", 61),
    ("Third Star", 91),
    ("Fourth Star", 121),
    ("Fifth Star", 151),
]

for run in range(50):  # expanded from 10 to 50 runs
    # Original runs (0-9) keep legacy ID pattern for stability.
    # Runs >=10 shift forward by +10 * 100000 (i.e., +1,000,000) to avoid collisions
    # with dish location IDs in the 1010001-1150015 range (dish_id * 10000 + day).
    if run < 10:
        offset = (run + 1) * 100000
    else:
        # Skip over 1,010,000 to 1,150,015 dish range by adding 10 to run index in multiplier
        offset = (run + 11) * 100000  # run 10 -> 2,100,000; run 49 -> 6,000,000
    suffix = "" if run == 0 else f" After Franchised{' ' + str(run) if run > 1 else ''}"
    prefix = "Franchise - "

    for day_index, label in enumerate(base_days):
        name = f"{prefix}Complete {label}{suffix}"
        loc_id = offset + day_index + 1
        FRANCHISE_LOCATION_DICT[name] = loc_id

    for label, id_offset in base_stars:
        name = f"{prefix}{label}{suffix}"
        loc_id = offset + id_offset
        FRANCHISE_LOCATION_DICT[name] = loc_id

for i in range(1, 51):  # expanded from 10 to 50
    # Maintain legacy IDs up to 10 for stability, then jump to higher range to avoid dish collisions.
    if i <= 10:
        loc_id = 100000 * (i + 1)
    else:
        # Start at 2,200,000 for i=11 ( (11+11)*100000 ) matching offset schema above.
        loc_id = 100000 * (i + 11)
    name = f"Franchise {i} times"
    FRANCHISE_LOCATION_DICT[name] = loc_id

for day in range(16, 21):
    key = f"Franchise - Complete Day {day}"
    if key in FRANCHISE_LOCATION_DICT:
        EXCLUDED_LOCATIONS.add(FRANCHISE_LOCATION_DICT[key])

FRANCHISE_LOCATION_DICT["Lose a Run"] = 100000

# Mark any franchise days 16-20 across all runs as excluded to avoid placing important items there
for name, loc_id in FRANCHISE_LOCATION_DICT.items():
    if name.startswith("Franchise - Complete Day "):
        try:
            # Extract the numeric day immediately after "Complete Day "
            day_str = name.split("Complete Day ", 1)[1].split(" ")[0].strip()
            if day_str.isdigit() and int(day_str) >= 16:
                EXCLUDED_LOCATIONS.add(loc_id)
        except Exception:
            pass

DAY_LOCATION_DICT: Dict[str, int] = {
    "Lose a Run": 100000
}

# Day checks up to 1000
for i in range(1, 1001):
    # e.g. “Complete Day 1” => ID=110001
    day_loc_id = 110000 + i
    day_name = f"Complete Day {i}"
    DAY_LOCATION_DICT[day_name] = day_loc_id

# Star checks up to 334 (supports day goal up to 1000 days => ceil(1000/3) = 334)
for i in range(1, 335):
    # e.g. “Complete Star 1” => ID=120001
    star_loc_id = 120000 + i
    star_name = f"Complete Star {i}"
    DAY_LOCATION_DICT[star_name] = star_loc_id


dish_dictionary = {
    101: "Salad",
    102: "Steak",
    103: "Burger",
    104: "Coffee",
    105: "Pizza",
    106: "Dumplings",
    107: "Turkey",
    108: "Pie",
    109: "Cakes",
    110: "Spaghetti",
    111: "Fish",
    112: "Tacos",
    113: "Hot Dogs",
    114: "Breakfast",
    115: "Stir Fry",
    116: "Sandwiches",
    117: "Sundaes",
}

DISH_LOCATIONS: Dict[str, int] = {}
for dish_id, dish_name in dish_dictionary.items():
    for day in range(1, 16):
        loc_name = f"{dish_name} - Day {day}"
        loc_id = (dish_id * 10000) + day
        DISH_LOCATIONS[loc_name] = loc_id