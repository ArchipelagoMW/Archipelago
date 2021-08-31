import json
import os

with open(os.path.join(os.path.dirname(__file__), 'games.json'), 'r') as file:
    game_table = json.loads(file.read())

lookup_id_to_name = {}
lookup_name_to_item = {}
lookup_name_to_id = {}
id = 626000
for game in game_table:
    lookup_id_to_name[id] = game["name"]
    lookup_name_to_item[game["name"]] = {"id": id,"name": game["name"],"progression": True,"game": game}
    lookup_name_to_id[game["name"]] = id
    id += 1

lookup_id_to_name[None] = "Victory"