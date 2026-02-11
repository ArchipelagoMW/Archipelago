"""
Generates static data files from external sources
"""
import csv
import functools
import json
import os
import re

import bs4
import ratelimit
import requests
import yaml

NOT_IN_FISHING_GUIDE = [
    "Deep Velodyna Carp",
    "Appleseed",
    "Arrowhead Snail",
    "Astral Algae",
    "Babycray",
    "Chemically Rich Fish",
    "Chromatic Fish",
    "Copperscale",
    "Cosmic Sponge",
    "Crawling Cog",
    "Crimson Copperfish",
    "Dalan's Claw",
    "Dragon's Delight",
    "Dusk Scallop",
    "Elysian Nudibranch",
    "Elysian Stickleback",
    "Fatty Eel",
    "Fish Offering",
    "Fishy Fish",
    "Flagon Clam",
    "Fresh Seaweed",
    "Gigas Catfish",
    "Glowfish",
    "Granite Hardscale",
    "Grass Shrimp",
    "Greasy Strangler",
    "Invisible Catfish",
    "Karellian Fishy Fish",
    "Khaal Crab",
    "Leatherscale",
    "Magma Eel",
    "Meteoric Bonito",
    "Methane Puffer",
    "Moon Oyster",
    "Mossy Tortoise",
    "Nhaama's Claw",
    "Nondescript Fish",
    "Paraichthyoid",
    "Plump Trout",
    "Rainbow Killifish",
    "Saltwater Fish",
    "Seaweed Snapper",
    "Shimmershell",
    "Silky Cosmocoral",
    "Soggy Alien Kelp",
    "Spearhead Snail",
    "Spikefish",
    "Splendid Clawbow",
    "Splendid Cockle",
    "Splendid Diamondtongue",
    "Splendid Egg-bearing Trout",
    "Splendid Eryops",
    "Splendid Larva",
    "Splendid Magmatongue",
    "Splendid Mammoth Shellfish",
    "Splendid Night's Bass",
    "Splendid Pipira",
    "Splendid Piranha",
    "Splendid Pirarucu",
    "Splendid Poison Catfish",
    "Splendid Pondfrond",
    "Splendid Robber Crab",
    "Splendid Shellfish",
    "Splendid Silver Kitten",
    "Splendid Spiralshell",
    "Splendid Sponge",
    "Splendid Treescale",
    "Splendid Trout",
    "Stellar Herring",
    "Steppe Barramundi",
    "Steppe Sweetfish",
    "Sticky Fingers",
    "Sunshell",
    "Supremest Crustacean",
    "Water Fan",
    "Weird Fish",
    "Wildlife Sample",
    "Zagas A'khaal",
    # Splendid tools
    "Forgiven Melancholy",
    "Ronkan Bullion",
    "Allagan Hunter",
    "Petal Shell",
    "Flintstrike",
    "Pickled Pom",
    "Platinum Seahorse",
    "Clavekeeper",
    "Mirror Image",
    "Spangled Pirarucu",
    "Gold Dustfish",
    "Forgiven Melancholy",
    "Oil Slick",
    "Gonzalo's Grace",
    "Deadwood Shadow",
    "Golding",
    "Ronkan Bullion",
    "Little Bounty",
    "Saint Fathric's Face",

    # Treasure maps
    "Timeworn Kumbhiraskin Map",
]

@functools.lru_cache
def teamcraft_json(filename: str) -> dict | list:
    print(f"Fetching {filename}.json from Teamcraft repo")
    return requests.get(f"https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/refs/heads/staging/libs/data/src/lib/json/{filename}.json").json()

@functools.lru_cache
def datamining_csv(filename: str) -> list:
    print(f"Fetching {filename}.csv from datamining repo")
    text = requests.get(f"https://raw.githubusercontent.com/xivapi/ffxiv-datamining/refs/heads/master/csv/{filename}.csv").content.decode('utf-8-sig')
    lines = text.splitlines()
    data = {}
    names = []
    for line in csv.DictReader(lines):
        if line['key'] == '#':
            names = {v: k for k, v in line.items()}
            continue
        data[line['key']] = line
        for k, v in names.items():
            if k:
                data[line['key']][k] = line[v]
    return data

def find_fates(zone: str) -> list[str]:
    print('Finding fates for zone: ' + zone)
    url = f"https://ffxiv.consolegameswiki.com/mediawiki/api.php?action=ask&query=[[Category:Fates]]%20[[Located%20in::{zone}]]%20[[Is%20event%20fate::false]]|?Has%20FATE%20level|?Is retired content|sort%3DHas FATE level,&format=json&api_version=3"
    data = requests.get(url).json()
    fates = []
    for page in data["query"]["results"]:
        name = list(page.keys())[0]
        level = page[name]['printouts']['Has FATE level'][0]
        line = name.replace(',','') + "," + str(level) + ',' + zone
        if page[name]['printouts']['Is retired content']:
            continue
        fates.append(line)
    print(f"Found {len(fates)} fates for zone {zone}")
    offset = data.get('query-continue-offset')
    if offset:
        print("!!! More fates to fetch !!!")
    return fates

def load_all_fish():
    with open(data_path('fish.json'), 'r', newline='') as h:
        all_fish = json.load(h)
    return all_fish

# def find_fishing_spots() -> None:
#     baseurl = "https://ffxiv.consolegameswiki.com/mediawiki/api.php?action=ask&query=[[Category:Fishing_log]]|?Gives resource|?Has fishing log level|?Located in|?Bait used|sort=Has fishing log level|offset={0}&format=json&api_version=3"
#     offset = 0
#     fishing_spots = []
#     f = open(os.path.join(os.path.dirname(__file__), 'fishing_spots.csv'), 'w')
#     while offset is not None:
#         url = baseurl.format(offset)
#         print(f'fetching {url}')
#         data = requests.get(url).json()
#         for page in data["query"]["results"]:
#             name = list(page.keys())[0]
#             if name == 'Fishing Log':
#                 continue
#             level = page[name]['printouts']['Has fishing log level'][0]
#             fish = [f['fulltext'] for f in page[name]['printouts']['Gives resource']]
#             bait = [f['fulltext'] for f in page[name]['printouts']['Bait used']]
#             region = [f['fulltext'] for f in page[name]['printouts']['Located in']][0]
#             line = name + ',' + str(level) + ',' + region + ',"' + ','.join(fish) + '","' + ','.join(bait) + '"'
#             f.write(line + '\n')
#             fishing_spots.append(line)
#         offset = data.get('query-continue-offset')
#     f.close()

def load_bait_paths() -> dict[str, dict[str, list[str]]]:
    path = data_path('fish_bait.yaml')
    if os.path.exists(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def scrape_bell():
    all_fish = {}
    bait_paths = load_bait_paths()
    url = 'https://www.garlandtools.org/bell/fish.js'
    js = requests.get(url).text.replace('\n', ' ')
    data = re.findall(r'gt.bell.(\w+) = (.*?);', js)
    with open(data_path('bait.json'), 'r', newline='') as h:
        bait = json.load(h)

    bait.update(json.loads(data[0][1]))
    fish = json.loads(data[1][1])
    for f in fish:
        if f['zone'] == 'Eulmore - The Buttress':
            f['zone'] = 'Eulmore'
        if f['zone'] == 'The Diadem':
            continue
        name = f["name"]
        if name in NOT_IN_FISHING_GUIDE:
            continue
        if name not in all_fish:
            all_fish[name] = {
                'name': f['name'],
                'id': f['id'],
                'zones': {},
                'lvl': f['lvl'],
                'category': f['category'],
                'bigfish': f['rarity'] > 1,
                'folklore': f.get('folklore'),
                'timed': f.get('weather') or f.get('during'),
                }
        else:
            all_fish[name]['lvl'] = min(all_fish[name]['lvl'], f['lvl'])
        all_fish[name]['zones'][f['zone']] = [c[0] for c in f['baits']]
        bait_paths.setdefault(name, {})
        for c in f['baits']:
            if c[0] not in bait_paths[name].setdefault(f['zone'], []):
                bait_paths[name][f['zone']].append(c[0])

    with open(data_path('fish.json'), 'w', newline='') as h:
        json.dump(all_fish, h, indent=1)
    with open(data_path('bait.json'), 'w', newline='') as h:
        json.dump(bait, h, indent=1)
    with open(data_path('fish_bait.yaml'), 'w', newline='') as h:
        yaml.dump(bait_paths, h)

def lookup_item_name(id: int | str) -> str | bool:
    items = teamcraft_json('items')
    if str(id) not in items:
        return False
    return items[str(id)]['en']

def lookup_rarity(item_id: int) -> int:
    items = teamcraft_json('rarities')
    return items.get(str(item_id), 0)

def lookup_fish(id: int | str) -> dict:
    params = teamcraft_json('fish-parameter')
    fishdata = params[str(id)]
    fish = {
        'name': lookup_item_name(fishdata['itemId']),
        'id': int(id),
        'zones': {},
        'lvl': fishdata['level'],
    }
    # if fishdata.get('recordType'):
    #     fish['category'] = fishdata['recordType']  # I think this is the category
    bigfish = lookup_rarity(fishdata['itemId']) > 1
    if bigfish:
        fish['bigfish'] = True
    if fishdata.get('folklore'):
        fish['folklore'] = fishdata['folklore']
    timed = fishdata.get('timed') or fishdata.get('weathered') or fishdata.get('during')
    if timed:
        fish['timed'] = timed
    if fishdata.get('stars'):
        fishdata['stars'] = fishdata['stars']
    return fish

def scrape_teamcraft():
    all_fish = load_all_fish()
    fish_ids: list[int] = teamcraft_json('fishes')
    fish_ids.sort()
    for fish_id in fish_ids:
        fish = lookup_fish(fish_id)
        name = fish['name']
        if name is False:
            continue
        all_fish.setdefault(name, fish)
        if name in NOT_IN_FISHING_GUIDE:
            all_fish[name]['tribal'] = True

    for hole in teamcraft_json('fishing-spots'):
        zone = datamining_csv('PlaceName')[str(hole['placeId'])]
        place_name = zone['Name']
        for fish_id in hole['fishes']:
            name = lookup_item_name(fish_id)
            # if name in NOT_IN_FISHING_GUIDE:
            #     continue
            fish = lookup_fish(fish_id)
            all_fish.setdefault(name, fish)
            fish.setdefault('zones', {})
            all_fish[name]['zones'].setdefault(place_name, [])
    with open(data_path('fish.json'), 'w', newline='') as h:
        json.dump(all_fish, h, indent=1)


def tribal_fish():
    all_fish = load_all_fish()
    offset = 0
    url = "https://ffxiv.consolegameswiki.com/mediawiki/api.php?action=ask&query=[[Category:Seafood]]|?Has%20game%20description|offset={0}&format=json&api_version=3"
    while offset is not None:
        data = requests.get(url.format(offset)).json()
        for page in data["query"]["results"]:
            name = list(page.keys())[0]
            desc = page[name]['printouts']['Has game description'][0]
            if '※Only for use' in desc:
                if name in all_fish:
                    all_fish[name]['tribal'] = True
                # print(name)
            if '※Not included' in desc:
                if name in all_fish:
                    all_fish[name]['tribal'] = True
                    # print(name)
        offset = data.get('query-continue-offset')
    with open(data_path('fish.json'), 'w', newline='') as h:
        json.dump(all_fish, h, indent=1)

def combine_lists(a: list, b: list) -> list:
    return list(set(a + b))

def apply_bait() -> None:
    with open(data_path('bait.json'), 'r', newline='') as h:
        bait_data = json.load(h)
    zoneless = []
    baitless = []
    all_fish = load_all_fish()
    bait_paths = load_bait_paths()
    for name, fish in all_fish.items():
        if fish.get('tribal'):
            continue
        if 'The <Emphasis>Endeavor</Emphasis>' in fish['zones']:
            continue
        if 'Limsa Lominsa Lower Decks' in fish['zones']:
            fish['zones']['Limsa Lominsa'] = combine_lists(fish['zones'].get('Limsa Lominsa', []), fish['zones']['Limsa Lominsa Lower Decks'])
            del fish['zones']['Limsa Lominsa Lower Decks']
        if 'Limsa Lominsa Upper Decks' in fish['zones']:
            fish['zones']['Limsa Lominsa'] = combine_lists(fish['zones'].get('Limsa Lominsa', []), fish['zones']['Limsa Lominsa Upper Decks'])
            del fish['zones']['Limsa Lominsa Upper Decks']

        for zone, baits in bait_paths.get(name, {}).items():
            if len(baits) > 1 and 'Versatile Lure' in baits:
                baits.remove('Versatile Lure')
            if baits:
                fish['zones'][zone] = baits
            else:
                print(f"No bait for {name} in {zone}")
            for bait in baits:
                if bait not in bait_data:
                    bait_data[bait] = {
                        "name": bait,
                    }
        if not fish['zones']:
            # print(f"No zones for {name}")
            zoneless.append(name)
            continue
        all_bait = []
        for zone in fish['zones']:
            all_bait += fish['zones'][zone]
        if not all_bait:
            print(f"No bait for {name}")
            baitless.append(name)

    with open(data_path('fish.json'), 'w', newline='') as h:
        json.dump(all_fish, h, indent=1)
    with open(data_path('zoneless.yaml'), 'w', newline='') as h:
        yaml.dump(zoneless, h, indent=1)
    with open(data_path('baitless.yaml'), 'w', newline='') as h:
        yaml.dump(baitless, h, indent=1)
    with open(data_path('bait.json'), 'w', newline='') as h:
        json.dump(bait_data, h, indent=1)

def fill_missing_bait() -> None:
    with open(data_path('baitless.yaml'), 'r', newline='') as h:
        baitless = yaml.safe_load(h)
    updated = False
    # TODO: Carby Plushy has data for Big Fish, but not the normal fish
    # https://raw.githubusercontent.com/icykoneko/ff14-fish-tracker-app/refs/heads/master/private/fishData.yaml

    # Cat Became Hungry has all fish, but it's HTML and will need to be scraped with bs4
    # https://en.ff14angler.com/
    updated = scrape_cat(baitless) or updated
    # Console Games Wiki has everything, but it's inconsistent across pages and is only really useful if I want to hand-enter data

    if updated:
        apply_bait()

def scrape_cat(baitless) -> bool:
    if not baitless:
        return False
    updated = False
    soup = cat_region_table(10000)
    regions = [o['value'] for o in soup.find(id='select_region').children if isinstance(o, bs4.element.Tag)]

    spots_in_zones, spot_to_id = cat_get_spots(regions)

    all_fish = load_all_fish()
    bait_paths = load_bait_paths()

    for fish in baitless:
        if fish not in all_fish:
            print(f"Fish {fish} not found in fish.json")
            continue
        for zone in all_fish[fish]['zones']:
            # We need to figure out which spots to check, or just check them all
            if zone not in spots_in_zones:
                print(f"Zone '{zone}' not found in Cat Became Hungry")
                continue
            for spot in spots_in_zones[zone]:
                spot_id = spot_to_id[spot]
                data: dict[str, dict[str, float]] = cat_spot_data(spot_id)
                best = (None, 0)
                for bait, stats in data.items():
                    if fish in stats:
                        percent = float(stats[fish])
                        if percent > best[1]:
                            best = (bait, percent)
                if best[0]:
                    name = best[0].title()
                    if name in all_fish:
                        mooch = all_fish[name]['zones'].get(zone, [])
                        if not mooch:
                            print(f"Found mooch for {fish} in {zone}: {name} but no mooch data")
                            continue
                        name = mooch[0]
                    baits = all_fish[fish]['zones'].setdefault(zone, [])
                    if name not in baits:
                        baits.append(name)
                        print(f"Found bait for {fish} in {zone}: {name} ({best[1]}%)")
                        bait_paths.setdefault(fish, {}).setdefault(zone, []).append(name)
                        updated = True
                        with open(data_path('fish_bait.yaml'), 'w', newline='') as h:
                            yaml.dump(bait_paths, h)
    with open(data_path('fish.json'), 'w', newline='') as h:
        json.dump(all_fish, h, indent=1)
    return updated

def cat_get_spots(regions):
    spots_in_zones = {}
    spot_to_id = {}
    for region in regions:
        soup = cat_region_table(region)
        spots = soup.find('div', id='main_contents').find_all('table')[1]
        for spot in spots.find_all('tr'):
            if spot.find('a') is None:
                area_name = spot.string
                continue
            spot_id = spot.find('a')['href'].split('/')[-1]
            spot_name = spot.find('a').text
            spots_in_zones.setdefault(area_name, []).append(spot_name)
            spot_to_id[spot_name] = spot_id

    return spots_in_zones, spot_to_id

@functools.lru_cache(maxsize=None)
@ratelimit.sleep_and_retry
@ratelimit.limits(calls=2, period=5)
def cat_spot_data(spot_id) -> dict[str, dict[str, float]]:
    bait_data = {}
    print(f"Fetching spot {spot_id} from Cat Became Hungry")
    spot = requests.get(f'https://en.ff14angler.com/spot/{spot_id}')
    soup = bs4.BeautifulSoup(spot.text, 'html.parser')
    effective_bait = soup.find(id='effective_bait')
    if effective_bait is None:
        print(f"No effective bait found for spot {spot_id}")
        return bait_data
    rows = effective_bait.find_all('tr')
    headers = [a['title'] for a in rows[0].find_all('a')]
    for row in rows[1:]:
        cells = row.find_all('td')
        bait = (cells[0].find('a') or cells[0].find('span'))['title']  # Bait name
        bait_data[bait] = {}
        for i, cell in enumerate(cells[1:]):
            div = cell.find('div')
            if div is None:
                continue
            percent = float(div.find('canvas')['value'])
            # print(div['title'])
            # print(f"{bait}: {headers[i]} ({percent}%)")
            bait_data[bait][headers[i]] = percent

    return bait_data

@functools.lru_cache
@ratelimit.sleep_and_retry
@ratelimit.limits(calls=2, period=5)
def cat_region_table(spot_id):
    print(f"Fetching spot {spot_id} from Cat Became Hungry")
    spots = requests.get(f'https://en.ff14angler.com/?spot={spot_id}')
    soup = bs4.BeautifulSoup(spots.text, 'html.parser')
    return soup

def data_path(filename: str) -> str:
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)

def clean_fish():
    all_fish = load_all_fish()
    for fish in all_fish.values():
        to_remove = []
        for zone, baits in fish['zones'].items():
            if not baits:
                # print(f"Removing {zone} from {fish['name']}")
                to_remove.append(zone)
        for zone in to_remove:
            del fish['zones'][zone]
    with open(data_path('fish.json'), 'w', newline='') as h:
        json.dump(all_fish, h, indent=1)

def sort_fish():
    all_fish = load_all_fish()
    sorted_fish = dict(sorted(all_fish.items(), key=lambda item: item[1]['id']))
    with open(data_path('fish.json'), 'w', newline='') as h:
        json.dump(sorted_fish, h, indent=1)


if __name__ == "__main__":
    # scrape_bell()
    scrape_teamcraft()
    tribal_fish()
    apply_bait()
    fill_missing_bait()
    clean_fish()
    sort_fish()
