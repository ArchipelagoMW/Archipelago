from BaseClasses import Location
from .Data import location_table
from .Game import starting_index
from .hooks.Locations import before_location_table_processed

location_table = before_location_table_processed(location_table)

######################
# Generate location lookups
######################

count = starting_index + 500 # 500 each for items and locations
victory_names: list[str] = []

# add sequential generated ids to the lists
for key, _ in enumerate(location_table):
    if "victory" in location_table[key] and location_table[key]["victory"]:
        victory_names.append(location_table[key]["name"])

    location_table[key]["id"] = count

    if not "region" in location_table[key]:
        location_table[key]["region"] = "Manual" # all locations are in the same region for Manual

    count += 1

if not victory_names:
    # Add the game completion location, which will have the Victory item assigned to it automatically
    location_table.append({
        "id": count + 1,
        "name": "__Manual Game Complete__",
        "region": "Manual",
        "requires": []
        # "category": custom_victory_location["category"] if "category" in custom_victory_location else []
    })
    victory_names.append("__Manual Game Complete__")

location_id_to_name: dict[int, str] = {}
location_name_to_location: dict[str, dict] = {}
location_name_groups: dict[str, list[str]] = {}

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
