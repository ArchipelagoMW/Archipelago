import os
import json

SONGS_PATH = os.path.join(os.path.dirname(__file__), "compiled_songs")

with open(os.path.join(SONGS_PATH, "catalog"), 'r') as infile:
    asset_ids = list(filter(lambda x: x, infile.read().split()))

weights = {}
for asset_id in asset_ids:
    with open(os.path.join(SONGS_PATH, f'{asset_id}.asset'), 'r') as infile:
        data = infile.read()
        if 'Xenogears' in data or 'Xenoblade' in data or 'Xenosaga' in data:
            weights[asset_id] = 0.6
        else:
            weights[asset_id] = 1

print(json.dumps(weights, indent=2))
