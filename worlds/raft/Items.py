import json
import os

def createResourcePackName(amount: int, itemName: str):
    return "Resource Pack: " + str(amount) + " " + itemName

with open(os.path.join(os.path.dirname(__file__), 'items.json'), 'r') as file:
    item_table = json.loads(file.read())
with open(os.path.join(os.path.dirname(__file__), 'progressives.json'), 'r') as file:
    progressive_table = json.loads(file.read())
with open(os.path.join(os.path.dirname(__file__), 'resourcepacks.json'), 'r') as file:
    resourcepack_items = json.loads(file.read())

lookup_id_to_name = {}
lookup_name_to_item = {}

lastItemId = -1
for item in item_table:
    item_name = item["name"]
    lookup_id_to_name[item["id"]] = item_name
    lookup_name_to_item[item_name] = item
    lastItemId = max(lastItemId, item["id"])

progressive_item_list = {}
for item in progressive_table:
    progressiveName = progressive_table[item]
    if progressiveName not in progressive_item_list:
        progressive_item_list[progressiveName] = []
    progressive_item_list[progressiveName].append(item)

for progressiveItemName in progressive_item_list.keys():
    lastItemId += 1
    generatedItem = {}
    generatedItem["id"] = lastItemId
    generatedItem["name"] = progressiveItemName
    generatedItem["progression"] = lookup_name_to_item[progressive_item_list[progressiveItemName][0]]["progression"]
    lookup_name_to_item[progressiveItemName] = generatedItem
    lookup_id_to_name[lastItemId] = progressiveItemName

# Generate resource pack items
for packItem in resourcepack_items:
    for i in range(1, 16): # 1-15
        lastItemId += 1
        rpName = createResourcePackName(i, packItem)
        generatedItem = {}
        generatedItem["id"] = lastItemId
        generatedItem["name"] = rpName
        generatedItem["progression"] = False
        lookup_name_to_item[rpName] = generatedItem
        lookup_id_to_name[lastItemId] = rpName

lookup_id_to_name[None] = "Victory"
lookup_name_to_id = {name: id for id, name in lookup_id_to_name.items()}