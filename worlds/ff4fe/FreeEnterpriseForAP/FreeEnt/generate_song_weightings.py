import os
import json
import pkgutil

SONGS_PATH = os.path.join(__file__, "compiled_songs")

with pkgutil.get_data(__name__, SONGS_PATH + "/catalog").decode().splitlines() as infile:
    asset_ids = list(filter(lambda x: x, infile.read().split()))

weights = {}
for asset_id in asset_ids:
    with pkgutil.get_data(__name__, SONGS_PATH + f'/{asset_id}.asset').decode().splitlines() as infile:
        data = infile.read()
        if 'Xenogears' in data or 'Xenoblade' in data or 'Xenosaga' in data:
            weights[asset_id] = 0.6
        else:
            weights[asset_id] = 1

print(json.dumps(weights, indent=2))
