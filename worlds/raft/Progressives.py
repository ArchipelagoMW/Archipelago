import json
import os

lookup_item_to_progressive = {}
with open(os.path.join(os.path.dirname(__file__), 'progressives.json'), 'r') as file:
    lookup_item_to_progressive = json.loads(file.read())

progressive_item_list = {}
for item in lookup_item_to_progressive:
    progressiveName = lookup_item_to_progressive[item]
    if progressiveName not in progressive_item_list:
        progressive_item_list[progressiveName] = []
    progressive_item_list[progressiveName].append(item)