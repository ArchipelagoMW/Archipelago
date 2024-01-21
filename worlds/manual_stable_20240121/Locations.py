from BaseClasses import Location
from .Data import location_table
from .Game import starting_index
from .hooks.Locations import before_location_table_processed

location_table = before_location_table_processed(location_table)

######################
# Generate location lookups
######################

count = starting_index + 500 # 500 each for items and locations
custom_victory_location = {}
victory_key = None

# add sequential generated ids to the lists
for key, _ in enumerate(location_table):
    if "victory" in location_table[key] and location_table[key]["victory"]:
        custom_victory_location = location_table[key]
        victory_key = key # store the victory location to be removed later

        continue

    location_table[key]["id"] = count

    if not "region" in location_table[key]:
        location_table[key]["region"] = "Manual" # all locations are in the same region for Manual

    count += 1

if victory_key is not None:
    location_table.pop(victory_key)

# Add the game completion location, which will have the Victory item assigned to it automatically
location_table.append({
    "id": count + 1,
    "name": "__Manual Game Complete__",
    "region": custom_victory_location["region"] if "region" in custom_victory_location else "Manual",
    "requires": custom_victory_location["requires"] if "requires" in custom_victory_location else []
    # "category": custom_victory_location["category"] if "category" in custom_victory_location else []
})

location_id_to_name = {}
location_name_to_location = {}
location_name_groups = {}

for item in location_table:
    location_id_to_name[item["id"]] = item["name"]
    location_name_to_location[item["name"]] = item

    for c in item.get("category", []):
        if c not in location_name_groups:
            location_name_groups[c] = []
        location_name_groups[c].append(item["name"])


# location_id_to_name[None] = "__Manual Game Complete__"
location_name_to_id = {name: id for id, name in location_id_to_name.items()}

######################
# Location classes
######################


class ManualLocation(Location):
    game = "Manual"
