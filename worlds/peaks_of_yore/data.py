import os
import json

with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'r') as file:
    data = json.load(file)

full_location_table = data["locations"]
full_item_table = data["items"]