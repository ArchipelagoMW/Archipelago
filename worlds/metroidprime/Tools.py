import json

# Initialize an empty dictionary
consolidated_dict = {}
data = {}
# Open and read the JSON fil e
with open("./data/RoomLoadouts.json", "r") as f:
    data = json.load(f)

# Iterate over each row in the data
for item in data:
    # Check if the room name is not in the dictionary
    name = list(item.keys())[0]
    items = list(item.values())[0]
    if name not in consolidated_dict:
        # Add it to the dictionary with the beam and item
        consolidated_dict[name] = []

    consolidated_dict[name] += [items]
    print(name, items)

with open("./data/ConsolidatedRoomLoadouts.json", "w") as f:
    json.dump(consolidated_dict, f, indent=4)
