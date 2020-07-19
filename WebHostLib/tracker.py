import collections

from flask import render_template
from werkzeug.exceptions import abort
import datetime
import logging
from uuid import UUID

import Items
from WebHostLib import app, cache, Room


def get_id(item_name):
    return Items.item_table[item_name][3]


icons = {
    "Progressive Sword":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/cc/ALttP_Master_Sword_Sprite.png?version=55869db2a20e157cd3b5c8f556097725",
    "Pegasus Boots":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ed/ALttP_Pegasus_Shoes_Sprite.png?version=405f42f97240c9dcd2b71ffc4bebc7f9",
    "Progressive Glove":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/53/ALttP_Titan's_Mitt_Sprite.png?version=6ac54c3016a23b94413784881fcd3c75",
    "Flippers":
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/88/ALttP_Zora's_Flippers_Sprite.png?version=b9d7521bb3a5a4d986879f70a70bc3da",
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
        r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Powder_Sprite.png?version=deaf51f8636823558bd6e6307435fb01",
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

multi_items = {get_id(name) for name in ("Progressive Sword", "Progressive Bow", "Bottle", "Progressive Glove")}
links = {get_id(key): get_id(value) for key, value in links.items()}
levels = {get_id(key): value for key, value in levels.items()}

tracking_names = ["Progressive Sword", "Progressive Bow", "Book of Mudora", "Hammer",
                  "Hookshot", "Magic Mirror", "Flute",
                  "Pegasus Boots", "Progressive Glove", "Flippers", "Moon Pearl", "Blue Boomerang",
                  "Red Boomerang", "Bug Catching Net", "Cape", "Shovel", "Lamp",
                  "Mushroom", "Magic Powder",
                  "Cane of Somaria", "Cane of Byrna", "Fire Rod", "Ice Rod", "Bombos", "Ether", "Quake",
                  "Bottle", "Triforce"]  # TODO make sure this list has what we need and sort it better

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

key_locations = {"Desert Palace", "Eastern Palace", "Hyrule Castle", "Agahnims Tower", "Tower of Hera", "Swamp Palace",
                 "Thieves Town", "Skull Woods", "Ice Palace", "Misery Mire", "Turtle Rock", "Palace of Darkness",
                 "Ganons Tower"}

big_key_locations = {"Desert Palace", "Eastern Palace", "Tower of Hera", "Swamp Palace", "Thieves Town", "Skull Woods",
                     "Ice Palace", "Misery Mire", "Turtle Rock", "Palace of Darkness", "Ganons Tower"}
location_to_area = {}
for area, locations in default_locations.items():
    for location in locations:
        location_to_area[location] = area

checks_in_area = {area: len(checks) for area, checks in default_locations.items()}
checks_in_area["Total"] = 216

ordered_areas = ('Light World', 'Dark World', 'Hyrule Castle', 'Agahnims Tower', 'Eastern Palace', 'Desert Palace',
                 'Tower of Hera', 'Palace of Darkness', 'Swamp Palace', 'Skull Woods', 'Thieves Town', 'Ice Palace',
                 'Misery Mire', 'Turtle Rock', 'Ganons Tower', "Total")

tracking_ids = []

for item in tracking_names:
    tracking_ids.append(get_id(item))

small_key_ids = {}
big_key_ids = {}

for item_name, data in Items.item_table.items():
    if "Key" in item_name:
        area = item_name.split("(")[1][:-1]
        if "Small" in item_name:
            small_key_ids[area] = data[3]
        else:
            big_key_ids[area] = data[3]

from MultiServer import get_item_name_from_id


def attribute_item(inventory, team, recipient, item):
    target_item = links.get(item, item)
    if item in levels:  # non-progressive
        inventory[team][recipient][target_item] = max(inventory[team][recipient][target_item], levels[item])
    else:
        inventory[team][recipient][target_item] += 1


@app.template_filter()
def render_timedelta(delta: datetime.timedelta):
    hours, minutes = divmod(delta.total_seconds() / 60, 60)
    hours = str(int(hours))
    minutes = str(int(minutes)).zfill(2)
    return f"{hours}:{minutes}"


_multidata_cache = {}


def get_static_room_data(room: Room):
    result = _multidata_cache.get(room.seed.id, None)
    if result:
        return result
    multidata = room.seed.multidata
    # in > 100 players this can take a bit of time and is the main reason for the cache
    locations = {tuple(k): tuple(v) for k, v in multidata['locations']}
    names = multidata["names"]

    use_door_tracker = False
    if "tags" in multidata:
        use_door_tracker = "DR" in multidata.tags
    result = locations, names, use_door_tracker
    _multidata_cache[room.seed.id] = result
    return result


@app.route('/tracker/<uuid:tracker>')
@cache.memoize(timeout=30)  # update every 30 seconds
def get_tracker(tracker: UUID):
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)
    locations, names, use_door_tracker = get_static_room_data(room)

    inventory = {teamnumber: {playernumber: collections.Counter() for playernumber in range(1, len(team) + 1)}
                 for teamnumber, team in enumerate(names)}

    checks_done = {teamnumber: {playernumber: {loc_name: 0 for loc_name in default_locations}
                                for playernumber in range(1, len(team) + 1)}
                   for teamnumber, team in enumerate(names)}
    precollected_items = room.seed.multidata.get("precollected_items", None)

    for (team, player), locations_checked in room.multisave.get("location_checks", {}):
        if precollected_items:
            precollected = precollected_items[player - 1]
            for item_id in precollected:
                attribute_item(inventory, team, player, item_id)
        for location in locations_checked:
            item, recipient = locations[location, player]
            attribute_item(inventory, team, recipient, item)
            checks_done[team][player][location_to_area[location]] += 1
            checks_done[team][player]["Total"] += 1

    for (team, player), game_state in room.multisave.get("client_game_state", []):
        if game_state:
            inventory[team][player][106] = 1  # Triforce

    activity_timers = {}
    now = datetime.datetime.utcnow()
    for (team, player), timestamp in room.multisave.get("client_activity_timers", []):
        activity_timers[team, player] = now - datetime.datetime.utcfromtimestamp(timestamp)

    player_names = {}
    for team, names in enumerate(names):
        for player, name in enumerate(names, 1):
            player_names[(team, player)] = name

    for (team, player), alias in room.multisave.get("name_aliases", []):
        player_names[(team, player)] = alias

    video = {}
    for (team, player), data in room.multisave.get("video", []):
        video[(team, player)] = data

    return render_template("tracker.html", inventory=inventory, get_item_name_from_id=get_item_name_from_id,
                           lookup_id_to_name=Items.lookup_id_to_name, player_names=player_names,
                           tracking_names=tracking_names, tracking_ids=tracking_ids, room=room, icons=icons,
                           multi_items=multi_items, checks_done=checks_done, ordered_areas=ordered_areas,
                           checks_in_area=checks_in_area, activity_timers=activity_timers,
                           key_locations=key_locations, small_key_ids=small_key_ids, big_key_ids=big_key_ids,
                           video=video, big_key_locations = key_locations if use_door_tracker else big_key_locations)
