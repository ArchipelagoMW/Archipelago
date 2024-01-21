from BaseClasses import Item
from .Data import item_table, progressive_item_table
from .Game import filler_item_name, starting_index
from .hooks.Items import before_item_table_processed, before_progressive_item_table_processed

item_table = before_item_table_processed(item_table)
progressive_item_table = before_progressive_item_table_processed(progressive_item_table)

######################
# Generate item lookups
######################

item_id_to_name: dict[int, str] = {}
item_name_to_item: dict[str, dict] = {}
item_name_groups: dict[str, str] = {}
advancement_item_names: set[str] = set()
lastItemId = -1

count = starting_index

# add the filler item to the list of items for lookup
if filler_item_name:
    item_table.append({
        "name": filler_item_name
    })

# add sequential generated ids to the lists
for key, val in enumerate(item_table):
    item_table[key]["id"] = count
    item_table[key]["progression"] = val["progression"] if "progression" in val else False
    count += 1

for item in item_table:
    item_name = item["name"]
    item_id_to_name[item["id"]] = item_name
    item_name_to_item[item_name] = item
    if item["progression"]:
        advancement_item_names.add(item_name)

    if item["id"] is not None:
        lastItemId = max(lastItemId, item["id"])

    for c in item.get("category", []):
        if c not in item_name_groups:
            item_name_groups[c] = []
        item_name_groups[c].append(item_name)

progressive_item_list = {}

for item in progressive_item_table:
    progressiveName = progressive_item_table[item]
    if progressiveName not in progressive_item_list:
        progressive_item_list[progressiveName] = []
    progressive_item_list[progressiveName].append(item)

for progressiveItemName in progressive_item_list.keys():
    lastItemId += 1
    generatedItem = {}
    generatedItem["id"] = lastItemId
    generatedItem["name"] = progressiveItemName
    generatedItem["progression"] = item_name_to_item[progressive_item_list[progressiveItemName][0]]["progression"]
    item_name_to_item[progressiveItemName] = generatedItem
    item_id_to_name[lastItemId] = progressiveItemName

item_id_to_name[None] = "__Victory__"
item_name_to_id = {name: id for id, name in item_id_to_name.items()}


######################
# Item classes
######################


class ManualItem(Item):
    game = "Manual"
