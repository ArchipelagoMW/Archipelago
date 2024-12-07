# python -m worlds.dark_souls_3.detailed_location_descriptions \
#     worlds/dark_souls_3/detailed_location_descriptions.py
#
# This script downloads the static randomizer's descriptions for each location and adds them to
# the location documentation.

from collections import defaultdict
import html
import os
import re
import requests
import yaml

from .Locations import location_dictionary


location_re = re.compile(r'^([A-Z0-9]+): (.*?)(?:$| - )')

if __name__ == '__main__':
    # TODO: update this to the main branch of the main randomizer once Archipelago support is merged
    url = 'https://raw.githubusercontent.com/nex3/SoulsRandomizers/archipelago-server/dist/Base/annotations.txt'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Got {response.status_code} when downloading static randomizer locations")
    annotations = yaml.load(response.text, Loader=yaml.Loader)

    static_to_archi_regions = {
        area['Name']: area['Archipelago']
        for area in annotations['Areas']
    }

    descriptions_by_key = {slot['Key']: slot['Text'] for slot in annotations['Slots']}

    # A map from (region, item name) pairs to all the descriptions that match those pairs.
    descriptions_by_location = defaultdict(list)

    # A map from item names to all the descriptions for those item names.
    descriptions_by_item = defaultdict(list)

    for slot in annotations['Slots']:
        region = static_to_archi_regions[slot['Area']]
        for item in slot['DebugText']:
            name = item.split(" - ")[0]
            descriptions_by_location[(region, name)].append(slot['Text'])
            descriptions_by_item[name].append(slot['Text'])
    counts_by_location = {
        location: len(descriptions) for (location, descriptions) in descriptions_by_location.items()
    }

    location_names_to_descriptions = {}
    for location in location_dictionary.values():
        if location.ap_code is None: continue
        if location.static:
            location_names_to_descriptions[location.name] = descriptions_by_key[location.static]
            continue

        match = location_re.match(location.name)
        if not match:
            raise Exception(f"Location name \"{location.name}\" doesn't match expected format.")

        item_candidates = descriptions_by_item[match[2]]
        if len(item_candidates) == 1:
            location_names_to_descriptions[location.name] = item_candidates[0]
            continue

        key = (match[1], match[2])
        if key not in descriptions_by_location:
            raise Exception(f'No static randomizer location found matching "{match[1]}: {match[2]}".')

        candidates = descriptions_by_location[key]
        if len(candidates) == 0:
            raise Exception(
                f'There are only {counts_by_location[key]} locations in the static randomizer ' +
                f'matching "{match[1]}: {match[2]}", but there are more in Archipelago.'
            )

        location_names_to_descriptions[location.name] = candidates.pop(0)

    table = "<table><tr><th>Location name</th><th>Detailed description</th>\n"
    for (name, description) in sorted(
        location_names_to_descriptions.items(),
        key = lambda pair: pair[0]
    ):
        table += f"<tr><td>{html.escape(name)}</td><td>{html.escape(description)}</td></tr>\n"
    table += "</table>\n"

    with open(
        os.path.join(os.path.dirname(__file__), 'docs/locations_en.md'),
        'r+',
        encoding='utf-8'
    ) as f:
        original = f.read()
        start_flag = "<!-- begin location table -->\n"
        start = original.index(start_flag) + len(start_flag)
        end = original.index("<!-- end location table -->")

        f.seek(0)
        f.write(original[:start] + table + original[end:])
        f.truncate()

    print("Updated docs/locations_en.md!")
