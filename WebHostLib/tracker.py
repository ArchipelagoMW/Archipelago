import collections

from flask import render_template
from werkzeug.exceptions import abort
import datetime
from uuid import UUID

from worlds.alttp import Items
from WebHostLib import app, cache, Room
from Utils import restricted_loads
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name

def get_alttp_id(item_name):
    return Items.item_table[item_name][2]


app.jinja_env.filters["location_name"] = lambda location: lookup_any_location_id_to_name.get(location, location)
app.jinja_env.filters['item_name'] = lambda id: lookup_any_item_id_to_name.get(id, id)

icons = {
    "Blue Shield": r"https://www.zeldadungeon.net/wiki/images/8/85/Fighters-Shield.png",
    "Red Shield": r"https://www.zeldadungeon.net/wiki/images/5/55/Fire-Shield.png",
    "Mirror Shield": r"https://www.zeldadungeon.net/wiki/images/8/84/Mirror-Shield.png",
    "Fighter Sword": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/4/40/SFighterSword.png?width=1920",
    "Master Sword": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/6/65/SMasterSword.png?width=1920",
    "Tempered Sword": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/9/92/STemperedSword.png?width=1920",
    "Golden Sword": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/2/28/SGoldenSword.png?width=1920",
    "Bow": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Bow_%26_Arrows_Sprite.png?version=5f85a70e6366bf473544ef93b274f74c",
    "Silver Bow": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/6/65/Bow.png?width=1920",
    "Green Mail": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/c/c9/SGreenTunic.png?width=1920",
    "Blue Mail": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/9/98/SBlueTunic.png?width=1920",
    "Red Mail": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/7/74/SRedTunic.png?width=1920",
    "Power Glove": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/f/f5/SPowerGlove.png?width=1920",
    "Titan Mitts": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/c/c1/STitanMitt.png?width=1920",
    "Progressive Sword":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/cc/ALttP_Master_Sword_Sprite.png?version=55869db2a20e157cd3b5c8f556097725",
    "Pegasus Boots":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ed/ALttP_Pegasus_Shoes_Sprite.png?version=405f42f97240c9dcd2b71ffc4bebc7f9",
    "Progressive Glove":
        r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/c/c1/STitanMitt.png?width=1920",
    "Flippers":
        r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/4/4c/ZoraFlippers.png?width=1920",
    "Moon Pearl":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/6/63/ALttP_Moon_Pearl_Sprite.png?version=d601542d5abcc3e006ee163254bea77e",
    "Progressive Bow":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Bow_%26_Arrows_Sprite.png?version=cfb7648b3714cccc80e2b17b2adf00ed",
    "Blue Boomerang":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/c3/ALttP_Boomerang_Sprite.png?version=96127d163759395eb510b81a556d500e",
    "Red Boomerang":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/b9/ALttP_Magical_Boomerang_Sprite.png?version=47cddce7a07bc3e4c2c10727b491f400",
    "Hookshot":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/2/24/Hookshot.png?version=c90bc8e07a52e8090377bd6ef854c18b",
    "Mushroom":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/35/ALttP_Mushroom_Sprite.png?version=1f1acb30d71bd96b60a3491e54bbfe59",
    "Magic Powder":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Powder_Sprite.png?version=c24e38effbd4f80496d35830ce8ff4ec",
    "Fire Rod":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d6/FireRod.png?version=6eabc9f24d25697e2c4cd43ddc8207c0",
    "Ice Rod":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d7/ALttP_Ice_Rod_Sprite.png?version=1f944148223d91cfc6a615c92286c3bc",
    "Bombos":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/8c/ALttP_Bombos_Medallion_Sprite.png?version=f4d6aba47fb69375e090178f0fc33b26",
    "Ether":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/3c/Ether.png?version=34027651a5565fcc5a83189178ab17b5",
    "Quake":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/56/ALttP_Quake_Medallion_Sprite.png?version=efd64d451b1831bd59f7b7d6b61b5879",
    "Lamp":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/6/63/ALttP_Lantern_Sprite.png?version=e76eaa1ec509c9a5efb2916698d5a4ce",
    "Hammer":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d1/ALttP_Hammer_Sprite.png?version=e0adec227193818dcaedf587eba34500",
    "Shovel":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/c4/ALttP_Shovel_Sprite.png?version=e73d1ce0115c2c70eaca15b014bd6f05",
    "Flute":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/db/Flute.png?version=ec4982b31c56da2c0c010905c5c60390",
    "Bug Catching Net":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/54/Bug-CatchingNet.png?version=4d40e0ee015b687ff75b333b968d8be6",
    "Book of Mudora":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/2/22/ALttP_Book_of_Mudora_Sprite.png?version=11e4632bba54f6b9bf921df06ac93744",
    "Bottle":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ef/ALttP_Magic_Bottle_Sprite.png?version=fd98ab04db775270cbe79fce0235777b",
    "Cane of Somaria":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e1/ALttP_Cane_of_Somaria_Sprite.png?version=8cc1900dfd887890badffc903bb87943",
    "Cane of Byrna":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Cane_of_Byrna_Sprite.png?version=758b607c8cbe2cf1900d42a0b3d0fb54",
    "Cape":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/1/1c/ALttP_Magic_Cape_Sprite.png?version=6b77f0d609aab0c751307fc124736832",
    "Magic Mirror":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Mirror_Sprite.png?version=e035dbc9cbe2a3bd44aa6d047762b0cc",
    "Triforce":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/4/4e/TriforceALttPTitle.png?version=dc398e1293177581c16303e4f9d12a48",
    "Small Key":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/f/f1/ALttP_Small_Key_Sprite.png?version=4f35d92842f0de39d969181eea03774e",
    "Big Key":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/33/ALttP_Big_Key_Sprite.png?version=136dfa418ba76c8b4e270f466fc12f4d",
    "Chest":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/7/73/ALttP_Treasure_Chest_Sprite.png?version=5f530ecd98dcb22251e146e8049c0dda",

    "Light World":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e7/ALttP_Soldier_Green_Sprite.png?version=d650d417934cd707a47e496489c268a6",
    "Dark World":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/9/94/ALttP_Moblin_Sprite.png?version=ebf50e33f4657c377d1606bcc0886ddc",
    "Hyrule Castle":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d3/ALttP_Ball_and_Chain_Trooper_Sprite.png?version=1768a87c06d29cc8e7ddd80b9fa516be",
    "Agahnims Tower":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/1/1e/ALttP_Agahnim_Sprite.png?version=365956e61b0c2191eae4eddbe591dab5",
    "Desert Palace":
        r"https://www.zeldadungeon.net/wiki/images/2/25/Lanmola-ALTTP-Sprite.png",
    "Eastern Palace":
        r"https://www.zeldadungeon.net/wiki/images/d/dc/RedArmosKnight.png",
    "Tower of Hera":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/3c/ALttP_Moldorm_Sprite.png?version=c588257bdc2543468e008a6b30f262a7",
    "Palace of Darkness":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ed/ALttP_Helmasaur_King_Sprite.png?version=ab8a4a1cfd91d4fc43466c56cba30022",
    "Swamp Palace":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/7/73/ALttP_Arrghus_Sprite.png?version=b098be3122e53f751b74f4a5ef9184b5",
    "Skull Woods":
        r"https://alttp-wiki.net/images/6/6a/Mothula.png",
    "Thieves Town":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/86/ALttP_Blind_the_Thief_Sprite.png?version=3833021bfcd112be54e7390679047222",
    "Ice Palace":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/33/ALttP_Kholdstare_Sprite.png?version=e5a1b0e8b2298e550d85f90bf97045c0",
    "Misery Mire":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/85/ALttP_Vitreous_Sprite.png?version=92b2e9cb0aa63f831760f08041d8d8d8",
    "Turtle Rock":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/9/91/ALttP_Trinexx_Sprite.png?version=0cc867d513952aa03edd155597a0c0be",
    "Ganons Tower":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/b9/ALttP_Ganon_Sprite.png?version=956f51f054954dfff53c1a9d4f929c74"
}

links = {"Bow": "Progressive Bow",
         "Silver Arrows": "Progressive Bow",
         "Silver Bow": "Progressive Bow",
         "Progressive Bow (Alt)": "Progressive Bow",
         "Bottle (Red Potion)": "Bottle",
         "Bottle (Green Potion)": "Bottle",
         "Bottle (Blue Potion)": "Bottle",
         "Bottle (Fairy)": "Bottle",
         "Bottle (Bee)": "Bottle",
         "Bottle (Good Bee)": "Bottle",
         "Fighter Sword": "Progressive Sword",
         "Master Sword": "Progressive Sword",
         "Tempered Sword": "Progressive Sword",
         "Golden Sword": "Progressive Sword",
         "Power Glove": "Progressive Glove",
         "Titans Mitts": "Progressive Glove"
         }

levels = {"Fighter Sword": 1,
          "Master Sword": 2,
          "Tempered Sword": 3,
          "Golden Sword": 4,
          "Power Glove": 1,
          "Titans Mitts": 2,
          "Bow": 1,
          "Silver Bow": 2}

multi_items = {get_alttp_id(name) for name in ("Progressive Sword", "Progressive Bow", "Bottle", "Progressive Glove")}
links = {get_alttp_id(key): get_alttp_id(value) for key, value in links.items()}
levels = {get_alttp_id(key): value for key, value in levels.items()}

tracking_names = ["Progressive Sword", "Progressive Bow", "Book of Mudora", "Hammer",
                  "Hookshot", "Magic Mirror", "Flute",
                  "Pegasus Boots", "Progressive Glove", "Flippers", "Moon Pearl", "Blue Boomerang",
                  "Red Boomerang", "Bug Catching Net", "Cape", "Shovel", "Lamp",
                  "Mushroom", "Magic Powder",
                  "Cane of Somaria", "Cane of Byrna", "Fire Rod", "Ice Rod", "Bombos", "Ether", "Quake",
                  "Bottle", "Triforce"]

default_locations = {
    'Light World': {1572864, 1572865, 60034, 1572867, 1572868, 60037, 1572869, 1572866, 60040, 59788, 60046, 60175,
                    1572880, 60049, 60178, 1572883, 60052, 60181, 1572885, 60055, 60184, 191256, 60058, 60187, 1572884,
                    1572886, 1572887, 1572906, 60202, 60205, 59824, 166320, 1010170, 60208, 60211, 60214, 60217, 59836,
                    60220, 60223, 59839, 1573184, 60226, 975299, 1573188, 1573189, 188229, 60229, 60232, 1573193,
                    1573194, 60235, 1573187, 59845, 59854, 211407, 60238, 59857, 1573185, 1573186, 1572882, 212328,
                    59881, 59761, 59890, 59770, 193020, 212605},
    'Dark World': {59776, 59779, 975237, 1572870, 60043, 1572881, 60190, 60193, 60196, 60199, 60840, 1573190, 209095,
                   1573192, 1573191, 60241, 60244, 60247, 60250, 59884, 59887, 60019, 60022, 60028, 60031},
    'Desert Palace': {1573216, 59842, 59851, 59791, 1573201, 59830},
    'Eastern Palace': {1573200, 59827, 59893, 59767, 59833, 59773},
    'Hyrule Castle': {60256, 60259, 60169, 60172, 59758, 59764, 60025, 60253},
    'Agahnims Tower': {60082, 60085},
    'Tower of Hera': {1573218, 59878, 59821, 1573202, 59896, 59899},
    'Swamp Palace': {60064, 60067, 60070, 59782, 59785, 60073, 60076, 60079, 1573204, 60061},
    'Thieves Town': {59905, 59908, 59911, 59914, 59917, 59920, 59923, 1573206},
    'Skull Woods': {59809, 59902, 59848, 59794, 1573205, 59800, 59803, 59806},
    'Ice Palace': {59872, 59875, 59812, 59818, 59860, 59797, 1573207, 59869},
    'Misery Mire': {60001, 60004, 60007, 60010, 60013, 1573208, 59866, 59998},
    'Turtle Rock': {59938, 59941, 59944, 1573209, 59947, 59950, 59953, 59956, 59926, 59929, 59932, 59935},
    'Palace of Darkness': {59968, 59971, 59974, 59977, 59980, 59983, 59986, 1573203, 59989, 59959, 59992, 59962, 59995,
                           59965},
    'Ganons Tower': {60160, 60163, 60166, 60088, 60091, 60094, 60097, 60100, 60103, 60106, 60109, 60112, 60115, 60118,
                     60121, 60124, 60127, 1573217, 60130, 60133, 60136, 60139, 60142, 60145, 60148, 60151, 60157},
    'Total': set()}

key_only_locations = {
    'Light World': set(),
    'Dark World': set(),
    'Desert Palace': {0x140031, 0x14002b, 0x140061, 0x140028},
    'Eastern Palace': {0x14005b, 0x140049},
    'Hyrule Castle': {0x140037, 0x140034, 0x14000d, 0x14003d},
    'Agahnims Tower': {0x140061, 0x140052},
    'Tower of Hera': set(),
    'Swamp Palace': {0x140019, 0x140016, 0x140013, 0x140010, 0x14000a},
    'Thieves Town': {0x14005e, 0x14004f},
    'Skull Woods': {0x14002e, 0x14001c},
    'Ice Palace': {0x140004, 0x140022, 0x140025, 0x140046},
    'Misery Mire': {0x140055, 0x14004c, 0x140064},
    'Turtle Rock': {0x140058, 0x140007},
    'Palace of Darkness': set(),
    'Ganons Tower': {0x140040, 0x140043, 0x14003a, 0x14001f},
    'Total': set()
}

key_locations = {"Desert Palace", "Eastern Palace", "Hyrule Castle", "Agahnims Tower", "Tower of Hera", "Swamp Palace",
                 "Thieves Town", "Skull Woods", "Ice Palace", "Misery Mire", "Turtle Rock", "Palace of Darkness",
                 "Ganons Tower"}

big_key_locations = {"Desert Palace", "Eastern Palace", "Tower of Hera", "Swamp Palace", "Thieves Town", "Skull Woods",
                     "Ice Palace", "Misery Mire", "Turtle Rock", "Palace of Darkness", "Ganons Tower"}
location_to_area = {}
for area, locations in default_locations.items():
    for location in locations:
        location_to_area[location] = area

for area, locations in key_only_locations.items():
    for location in locations:
        location_to_area[location] = area

checks_in_area = {area: len(checks) for area, checks in default_locations.items()}
checks_in_area["Total"] = 216

ordered_areas = ('Light World', 'Dark World', 'Hyrule Castle', 'Agahnims Tower', 'Eastern Palace', 'Desert Palace',
                 'Tower of Hera', 'Palace of Darkness', 'Swamp Palace', 'Skull Woods', 'Thieves Town', 'Ice Palace',
                 'Misery Mire', 'Turtle Rock', 'Ganons Tower', "Total")

tracking_ids = []

for item in tracking_names:
    tracking_ids.append(get_alttp_id(item))

small_key_ids = {}
big_key_ids = {}
ids_small_key = {}
ids_big_key = {}

for item_name, data in Items.item_table.items():
    if "Key" in item_name:
        area = item_name.split("(")[1][:-1]
        if "Small" in item_name:
            small_key_ids[area] = data[2]
            ids_small_key[data[2]] = area
        else:
            big_key_ids[area] = data[2]
            ids_big_key[data[2]] = area

from MultiServer import get_item_name_from_id, Context


def attribute_item(inventory, team, recipient, item):
    target_item = links.get(item, item)
    if item in levels:  # non-progressive
        inventory[team][recipient][target_item] = max(inventory[team][recipient][target_item], levels[item])
    else:
        inventory[team][recipient][target_item] += 1


def attribute_item_solo(inventory, item):
    """Adds item to inventory counter, converts everything to progressive."""
    target_item = links.get(item, item)
    if item in levels:  # non-progressive
        inventory[target_item] = max(inventory[target_item], levels[item])
    else:
        inventory[target_item] += 1


@app.template_filter()
def render_timedelta(delta: datetime.timedelta):
    hours, minutes = divmod(delta.total_seconds() / 60, 60)
    hours = str(int(hours))
    minutes = str(int(minutes)).zfill(2)
    return f"{hours}:{minutes}"


_multidata_cache = {}

def get_location_table(checks_table: dict) -> dict:
    loc_to_area = {}
    for area, locations in checks_table.items():
        if area == "Total":
            continue
        for location in locations:
            loc_to_area[location] = area
    return loc_to_area

def get_static_room_data(room: Room):
    result = _multidata_cache.get(room.seed.id, None)
    if result:
        return result
    multidata = Context._decompress(room.seed.multidata)
    # in > 100 players this can take a bit of time and is the main reason for the cache
    locations = multidata['locations']
    names = multidata["names"]
    seed_checks_in_area = checks_in_area.copy()

    use_door_tracker = False
    if "tags" in multidata:
        use_door_tracker = "DR" in multidata["tags"]
    if use_door_tracker:
        for area, checks in key_only_locations.items():
            seed_checks_in_area[area] += len(checks)
        seed_checks_in_area["Total"] = 249

    player_checks_in_area = {playernumber: {areaname: len(multidata["checks_in_area"][playernumber][areaname])
                                            if areaname != "Total" else multidata["checks_in_area"][playernumber]["Total"]
                                            for areaname in ordered_areas}
                             for playernumber in range(1, len(names[0]) + 1)}
    player_location_to_area = {playernumber: get_location_table(multidata["checks_in_area"][playernumber])
                               for playernumber in range(1, len(names[0]) + 1)}

    player_big_key_locations = {playernumber: set() for playernumber in range(1, len(names[0]) + 1)}
    player_small_key_locations = {playernumber: set() for playernumber in range(1, len(names[0]) + 1)}
    for loc_data in locations.values():
        for item_id, item_player in loc_data.values():
            if item_id in ids_big_key:
                player_big_key_locations[item_player].add(ids_big_key[item_id])
            elif item_id in ids_small_key:
                player_small_key_locations[item_player].add(ids_small_key[item_id])

    result = locations, names, use_door_tracker, player_checks_in_area, player_location_to_area, \
             player_big_key_locations, player_small_key_locations, multidata["precollected_items"], \
             multidata["games"]
    _multidata_cache[room.seed.id] = result
    return result


@app.route('/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
@cache.memoize(timeout=60)  # multisave is currently created at most every minute
def getPlayerTracker(tracker: UUID, tracked_team: int, tracked_player: int):
    # Team and player must be positive and greater than zero
    if tracked_team < 0 or tracked_player < 1:
        abort(404)

    room = Room.get(tracker=tracker)
    if not room:
        abort(404)

    # Collect seed information and pare it down to a single player
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, \
    player_big_key_locations, player_small_key_locations, precollected_items, games = get_static_room_data(room)
    player_name = names[tracked_team][tracked_player - 1]
    location_to_area = player_location_to_area[tracked_player]
    inventory = collections.Counter()
    checks_done = {loc_name: 0 for loc_name in default_locations}

    # Add starting items to inventory
    starting_items = precollected_items[tracked_player]
    if starting_items:
        for item_id in starting_items:
            attribute_item_solo(inventory, item_id)

    if room.multisave:
        multisave = restricted_loads(room.multisave)
    else:
        multisave = {}

    # Add items to player inventory
    for (ms_team, ms_player), locations_checked in multisave.get("location_checks", {}).items():
        # logging.info(f"{ms_team}, {ms_player}, {locations_checked}")
        # Skip teams and players not matching the request
        player_locations = locations[ms_player]
        if ms_team == tracked_team:
            # If the player does not have the item, do nothing
            for location in locations_checked:
                if location in player_locations:
                    item, recipient = player_locations[location]
                    if recipient == tracked_player: # a check done for the tracked player
                        attribute_item_solo(inventory, item)
                    if ms_player == tracked_player: # a check done by the tracked player
                        checks_done[location_to_area[location]] += 1
                        checks_done["Total"] += 1
    if games[tracked_player] == "A Link to the Past":
        # Note the presence of the triforce item
        game_state = multisave.get("client_game_state", {}).get((tracked_team, tracked_player), 0)
        if game_state == 30:
            inventory[106] = 1  # Triforce

        # Progressive items need special handling for icons and class
        progressive_items = {
            "Progressive Sword": 94,
            "Progressive Glove": 97,
            "Progressive Bow": 100,
            "Progressive Mail": 96,
            "Progressive Shield": 95,
        }
        progressive_names = {
            "Progressive Sword": [None, 'Fighter Sword', 'Master Sword', 'Tempered Sword', 'Golden Sword'],
            "Progressive Glove": [None, 'Power Glove', 'Titan Mitts'],
            "Progressive Bow": [None, "Bow", "Silver Bow"],
            "Progressive Mail": ["Green Mail", "Blue Mail", "Red Mail"],
            "Progressive Shield": [None, "Blue Shield", "Red Shield", "Mirror Shield"]
        }

        # Determine which icon to use
        display_data = {}
        for item_name, item_id in progressive_items.items():
            level = min(inventory[item_id], len(progressive_names[item_name])-1)
            display_name = progressive_names[item_name][level]
            acquired = True
            if not display_name:
                acquired = False
                display_name = progressive_names[item_name][level+1]
            base_name = item_name.split(maxsplit=1)[1].lower()
            display_data[base_name+"_acquired"] = acquired
            display_data[base_name+"_url"] = icons[display_name]


        # The single player tracker doesn't care about overworld, underworld, and total checks. Maybe it should?
        sp_areas = ordered_areas[2:15]

        return render_template("lttpTracker.html", inventory=inventory,
                               player_name=player_name, room=room, icons=icons, checks_done=checks_done,
                               checks_in_area=seed_checks_in_area[tracked_player], acquired_items={lookup_any_item_id_to_name[id] for id in inventory},
                               small_key_ids=small_key_ids, big_key_ids=big_key_ids, sp_areas=sp_areas,
                               key_locations=player_small_key_locations[tracked_player],
                               big_key_locations=player_big_key_locations[tracked_player],
                               **display_data)
    elif games[tracked_player] == "Minecraft": 
        minecraft_icons = {
            "Wooden Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d2/Wooden_Pickaxe_JE3_BE3.png",
            "Stone Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c4/Stone_Pickaxe_JE2_BE2.png",
            "Iron Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d1/Iron_Pickaxe_JE3_BE2.png",
            "Diamond Pickaxe": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e7/Diamond_Pickaxe_JE3_BE3.png",
            "Wooden Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d5/Wooden_Sword_JE2_BE2.png",
            "Stone Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b1/Stone_Sword_JE2_BE2.png",
            "Iron Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/8/8e/Iron_Sword_JE2_BE2.png",
            "Diamond Sword": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/44/Diamond_Sword_JE3_BE3.png",
            "Leather Tunic": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b7/Leather_Tunic_JE4_BE2.png",
            "Iron Chestplate": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Iron_Chestplate_JE2_BE2.png",
            "Diamond Chestplate": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e0/Diamond_Chestplate_JE3_BE2.png",
            "Iron Ingot": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png",
            "Block of Iron": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7e/Block_of_Iron_JE4_BE3.png",
            "Brewing Stand": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fa/Brewing_Stand.png",
            "Ender Pearl": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f6/Ender_Pearl_JE3_BE2.png",
            "Bucket": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Bucket_JE2_BE2.png",
            "Bow": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/ab/Bow_%28Pull_2%29_JE1_BE1.png",
            "Shield": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c6/Shield_JE2_BE1.png",
            "Red Bed": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/dc/Red_Bed_JE4_BE3.png",
            "Netherite Scrap": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/33/Netherite_Scrap_JE2_BE1.png",
            "Flint and Steel": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/94/Flint_and_Steel_JE4_BE2.png",
            "Enchanting Table": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Enchanting_Table.gif",
            "Fishing Rod": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7f/Fishing_Rod_JE2_BE2.png",
            "Campfire": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/91/Campfire_JE2_BE2.gif",
            "Water Bottle": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/75/Water_Bottle_JE2_BE2.png",
            "Dragon Head": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b6/Dragon_Head.png",
        }

        minecraft_location_ids = {
            "Story": [42073, 42080, 42081, 42023, 42082, 42027, 42039, 42085, 42002, 42009, 42010, 
                      42070, 42041, 42049, 42090, 42004, 42031, 42025, 42029, 42051, 42077, 42089],
            "Nether": [42017, 42044, 42069, 42058, 42034, 42060, 42066, 42076, 42064, 42071, 42021, 
                       42062, 42008, 42061, 42033, 42011, 42006, 42019, 42000, 42040, 42001, 42015, 42014],
            "The End": [42052, 42005, 42012, 42032, 42030, 42042, 42018, 42038, 42046],
            "Adventure": [42047, 42086, 42087, 42050, 42059, 42055, 42072, 42003, 42035, 42016, 42020, 
                          42048, 42054, 42068, 42043, 42074, 42075, 42024, 42026, 42037, 42045, 42056, 42088],
            "Husbandry": [42065, 42067, 42078, 42022, 42007, 42079, 42013, 42028, 
                          42036, 42057, 42063, 42053, 42083, 42084, 42091]
        }

        display_data = {}

        # Determine display for progressive items
        progressive_items = {
            "Progressive Tools": 45013,
            "Progressive Weapons": 45012,
            "Progressive Armor": 45014,
            "Progressive Resource Crafting": 45001
        }
        progressive_names = {
            "Progressive Tools": ["Wooden Pickaxe", "Stone Pickaxe", "Iron Pickaxe", "Diamond Pickaxe"],
            "Progressive Weapons": ["Wooden Sword", "Stone Sword", "Iron Sword", "Diamond Sword"],
            "Progressive Armor": ["Leather Tunic", "Iron Chestplate", "Diamond Chestplate"],
            "Progressive Resource Crafting": ["Iron Ingot", "Iron Ingot", "Block of Iron"]
        }
        for item_name, item_id in progressive_items.items():
            level = min(inventory[item_id], len(progressive_names[item_name])-1)
            display_name = progressive_names[item_name][level]
            base_name = item_name.split(maxsplit=1)[1].lower().replace(' ', '_')
            display_data[base_name+"_url"] = minecraft_icons[display_name]

        # Multi-items
        multi_items = {
            "3 Ender Pearls": 45029,
            "8 Netherite Scrap": 45015
        }
        for item_name, item_id in multi_items.items():
            base_name = item_name.split()[-1].lower()
            count = inventory[item_id]
            if count >= 0:
                display_data[base_name+"_count"] = count

        # Victory condition
        game_state = multisave.get("client_game_state", {}).get((tracked_team, tracked_player), 0)
        display_data['game_finished'] = game_state == 30

        # Turn location IDs into advancement tab counts
        checked_locations = multisave.get("location_checks", {}).get((tracked_team, tracked_player), set())
        lookup_name = lambda id: lookup_any_location_id_to_name[id]
        location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations} 
            for tab_name, tab_locations in minecraft_location_ids.items()}
        checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations]) 
            for tab_name, tab_locations in minecraft_location_ids.items()}
        checks_done['Total'] = len(checked_locations)
        checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in minecraft_location_ids.items()}
        checks_in_area['Total'] = sum(checks_in_area.values())

        return render_template("minecraftTracker.html", 
                               inventory=inventory, icons=minecraft_icons, acquired_items={lookup_any_item_id_to_name[id] for id in inventory if id in lookup_any_item_id_to_name},
                               player=tracked_player, team=tracked_team, room=room, player_name=player_name,
                               checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                               **display_data)

    else:
        checked_locations = multisave.get("location_checks", {}).get((tracked_team, tracked_player), set())
        player_received_items = {}
        for order_index, networkItem in enumerate(multisave.get('received_items', {}).get((tracked_team, tracked_player), [])):
            player_received_items[networkItem.item] = order_index + 1
        return render_template("genericTracker.html",
                               inventory=inventory,
                               player=tracked_player, team=tracked_team, room=room, player_name=player_name,
                               checked_locations=checked_locations, not_checked_locations=set(locations[tracked_player])-checked_locations,
                               received_items=player_received_items)

@app.route('/tracker/<suuid:tracker>')
@cache.memoize(timeout=60)  # multisave is currently created at most every minute
def getTracker(tracker: UUID):
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, player_big_key_locations, \
    player_small_key_locations, precollected_items, games = get_static_room_data(room)

    inventory = {teamnumber: {playernumber: collections.Counter() for playernumber in range(1, len(team) + 1)}
                 for teamnumber, team in enumerate(names)}

    checks_done = {teamnumber: {playernumber: {loc_name: 0 for loc_name in default_locations}
                                for playernumber in range(1, len(team) + 1)}
                   for teamnumber, team in enumerate(names)}

    hints = {team: set() for team in range(len(names))}
    if room.multisave:
        multisave = restricted_loads(room.multisave)
    else:
        multisave = {}
    if "hints" in multisave:
        for (team, slot), slot_hints in multisave["hints"].items():
            hints[team] |= set(slot_hints)

    for (team, player), locations_checked in multisave.get("location_checks", {}).items():
        player_locations = locations[player]
        if precollected_items:
            precollected = precollected_items[player]
            for item_id in precollected:
                attribute_item(inventory, team, player, item_id)
        for location in locations_checked:
            if location not in player_locations or location not in player_location_to_area[player]:
                continue

            item, recipient = player_locations[location]
            attribute_item(inventory, team, recipient, item)
            checks_done[team][player][player_location_to_area[player][location]] += 1
            checks_done[team][player]["Total"] += 1

    for (team, player), game_state in multisave.get("client_game_state", {}).items():
        if game_state == 30:
            inventory[team][player][106] = 1  # Triforce

    group_big_key_locations = set()
    group_key_locations = set()
    for player in range(1, len(names[0]) + 1):
        group_key_locations |= player_small_key_locations[player]
        group_big_key_locations |= player_big_key_locations[player]

    activity_timers = {}
    now = datetime.datetime.utcnow()
    for (team, player), timestamp in multisave.get("client_activity_timers", []):
        activity_timers[team, player] = now - datetime.datetime.utcfromtimestamp(timestamp)

    player_names = {}
    for team, names in enumerate(names):
        for player, name in enumerate(names, 1):
            player_names[(team, player)] = name
    long_player_names = player_names.copy()
    for (team, player), alias in multisave.get("name_aliases", {}).items():
        player_names[(team, player)] = alias
        long_player_names[(team, player)] = f"{alias} ({long_player_names[(team, player)]})"

    video = {}
    for (team, player), data in multisave.get("video", []):
        video[(team, player)] = data

    return render_template("tracker.html", inventory=inventory, get_item_name_from_id=get_item_name_from_id,
                           lookup_id_to_name=Items.lookup_id_to_name, player_names=player_names,
                           tracking_names=tracking_names, tracking_ids=tracking_ids, room=room, icons=icons,
                           multi_items=multi_items, checks_done=checks_done, ordered_areas=ordered_areas,
                           checks_in_area=seed_checks_in_area, activity_timers=activity_timers,
                           key_locations=group_key_locations, small_key_ids=small_key_ids, big_key_ids=big_key_ids,
                           video=video, big_key_locations=group_big_key_locations,
                           hints=hints, long_player_names = long_player_names)
