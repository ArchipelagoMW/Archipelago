import collections
import datetime
import typing
from typing import Counter, Optional, Dict, Any, Tuple
from uuid import UUID

from flask import render_template
from werkzeug.exceptions import abort

from MultiServer import Context, get_saving_second
from NetUtils import SlotType
from Utils import restricted_loads
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name
from worlds.alttp import Items
from . import app, cache
from .models import Room

alttp_icons = {
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
    "Progressive Sword": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/cc/ALttP_Master_Sword_Sprite.png?version=55869db2a20e157cd3b5c8f556097725",
    "Pegasus Boots": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ed/ALttP_Pegasus_Shoes_Sprite.png?version=405f42f97240c9dcd2b71ffc4bebc7f9",
    "Progressive Glove": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/c/c1/STitanMitt.png?width=1920",
    "Flippers": r"https://oyster.ignimgs.com/mediawiki/apis.ign.com/the-legend-of-zelda-a-link-to-the-past/4/4c/ZoraFlippers.png?width=1920",
    "Moon Pearl": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/6/63/ALttP_Moon_Pearl_Sprite.png?version=d601542d5abcc3e006ee163254bea77e",
    "Progressive Bow": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Bow_%26_Arrows_Sprite.png?version=cfb7648b3714cccc80e2b17b2adf00ed",
    "Blue Boomerang": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/c3/ALttP_Boomerang_Sprite.png?version=96127d163759395eb510b81a556d500e",
    "Red Boomerang": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/b9/ALttP_Magical_Boomerang_Sprite.png?version=47cddce7a07bc3e4c2c10727b491f400",
    "Hookshot": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/2/24/Hookshot.png?version=c90bc8e07a52e8090377bd6ef854c18b",
    "Mushroom": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/35/ALttP_Mushroom_Sprite.png?version=1f1acb30d71bd96b60a3491e54bbfe59",
    "Magic Powder": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Powder_Sprite.png?version=c24e38effbd4f80496d35830ce8ff4ec",
    "Fire Rod": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d6/FireRod.png?version=6eabc9f24d25697e2c4cd43ddc8207c0",
    "Ice Rod": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d7/ALttP_Ice_Rod_Sprite.png?version=1f944148223d91cfc6a615c92286c3bc",
    "Bombos": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/8c/ALttP_Bombos_Medallion_Sprite.png?version=f4d6aba47fb69375e090178f0fc33b26",
    "Ether": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/3c/Ether.png?version=34027651a5565fcc5a83189178ab17b5",
    "Quake": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/56/ALttP_Quake_Medallion_Sprite.png?version=efd64d451b1831bd59f7b7d6b61b5879",
    "Lamp": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/6/63/ALttP_Lantern_Sprite.png?version=e76eaa1ec509c9a5efb2916698d5a4ce",
    "Hammer": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d1/ALttP_Hammer_Sprite.png?version=e0adec227193818dcaedf587eba34500",
    "Shovel": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/c/c4/ALttP_Shovel_Sprite.png?version=e73d1ce0115c2c70eaca15b014bd6f05",
    "Flute": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/db/Flute.png?version=ec4982b31c56da2c0c010905c5c60390",
    "Bug Catching Net": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/5/54/Bug-CatchingNet.png?version=4d40e0ee015b687ff75b333b968d8be6",
    "Book of Mudora": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/2/22/ALttP_Book_of_Mudora_Sprite.png?version=11e4632bba54f6b9bf921df06ac93744",
    "Bottle": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ef/ALttP_Magic_Bottle_Sprite.png?version=fd98ab04db775270cbe79fce0235777b",
    "Cane of Somaria": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e1/ALttP_Cane_of_Somaria_Sprite.png?version=8cc1900dfd887890badffc903bb87943",
    "Cane of Byrna": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/bc/ALttP_Cane_of_Byrna_Sprite.png?version=758b607c8cbe2cf1900d42a0b3d0fb54",
    "Cape": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/1/1c/ALttP_Magic_Cape_Sprite.png?version=6b77f0d609aab0c751307fc124736832",
    "Magic Mirror": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e5/ALttP_Magic_Mirror_Sprite.png?version=e035dbc9cbe2a3bd44aa6d047762b0cc",
    "Triforce": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/4/4e/TriforceALttPTitle.png?version=dc398e1293177581c16303e4f9d12a48",
    "Small Key": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/f/f1/ALttP_Small_Key_Sprite.png?version=4f35d92842f0de39d969181eea03774e",
    "Big Key": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/33/ALttP_Big_Key_Sprite.png?version=136dfa418ba76c8b4e270f466fc12f4d",
    "Chest": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/7/73/ALttP_Treasure_Chest_Sprite.png?version=5f530ecd98dcb22251e146e8049c0dda",
    "Light World": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/e7/ALttP_Soldier_Green_Sprite.png?version=d650d417934cd707a47e496489c268a6",
    "Dark World": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/9/94/ALttP_Moblin_Sprite.png?version=ebf50e33f4657c377d1606bcc0886ddc",
    "Hyrule Castle": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/d/d3/ALttP_Ball_and_Chain_Trooper_Sprite.png?version=1768a87c06d29cc8e7ddd80b9fa516be",
    "Agahnims Tower": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/1/1e/ALttP_Agahnim_Sprite.png?version=365956e61b0c2191eae4eddbe591dab5",
    "Desert Palace": r"https://www.zeldadungeon.net/wiki/images/2/25/Lanmola-ALTTP-Sprite.png",
    "Eastern Palace": r"https://www.zeldadungeon.net/wiki/images/d/dc/RedArmosKnight.png",
    "Tower of Hera": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/3c/ALttP_Moldorm_Sprite.png?version=c588257bdc2543468e008a6b30f262a7",
    "Palace of Darkness": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/e/ed/ALttP_Helmasaur_King_Sprite.png?version=ab8a4a1cfd91d4fc43466c56cba30022",
    "Swamp Palace": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/7/73/ALttP_Arrghus_Sprite.png?version=b098be3122e53f751b74f4a5ef9184b5",
    "Skull Woods": r"https://alttp-wiki.net/images/6/6a/Mothula.png",
    "Thieves Town": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/86/ALttP_Blind_the_Thief_Sprite.png?version=3833021bfcd112be54e7390679047222",
    "Ice Palace": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/3/33/ALttP_Kholdstare_Sprite.png?version=e5a1b0e8b2298e550d85f90bf97045c0",
    "Misery Mire": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/8/85/ALttP_Vitreous_Sprite.png?version=92b2e9cb0aa63f831760f08041d8d8d8",
    "Turtle Rock": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/9/91/ALttP_Trinexx_Sprite.png?version=0cc867d513952aa03edd155597a0c0be",
    "Ganons Tower": r"https://gamepedia.cursecdn.com/zelda_gamepedia_en/b/b9/ALttP_Ganon_Sprite.png?version=956f51f054954dfff53c1a9d4f929c74"
}


def get_alttp_id(item_name):
    return Items.item_table[item_name][2]


app.jinja_env.filters["location_name"] = lambda location: lookup_any_location_id_to_name.get(location, location)
app.jinja_env.filters['item_name'] = lambda id: lookup_any_item_id_to_name.get(id, id)

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

# cleanup global namespace
del item_name
del data
del item


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
    multidata = Context.decompress(room.seed.multidata)
    # in > 100 players this can take a bit of time and is the main reason for the cache
    locations: Dict[int, Dict[int, Tuple[int, int, int]]] = multidata['locations']
    names: Dict[int, Dict[int, str]] = multidata["names"]
    groups = {}
    if "slot_info" in multidata:
        groups = {slot: slot_info.group_members for slot, slot_info in multidata["slot_info"].items()
                  if slot_info.type == SlotType.group}
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
                             for playernumber in range(1, len(names[0]) + 1)
                             if playernumber not in groups}
    player_location_to_area = {playernumber: get_location_table(multidata["checks_in_area"][playernumber])
                               for playernumber in range(1, len(names[0]) + 1)
                               if playernumber not in groups}
    saving_second = get_saving_second(multidata["seed_name"])
    result = locations, names, use_door_tracker, player_checks_in_area, player_location_to_area, \
             multidata["precollected_items"], multidata["games"], multidata["slot_data"], groups, saving_second
    _multidata_cache[room.seed.id] = result
    return result


@app.route('/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
def get_player_tracker(tracker: UUID, tracked_team: int, tracked_player: int, want_generic: bool = False):
    key = f"{tracker}_{tracked_team}_{tracked_player}_{want_generic}"
    tracker_page = cache.get(key)
    if tracker_page:
        return tracker_page
    timeout, tracker_page = _get_player_tracker(tracker, tracked_team, tracked_player, want_generic)
    cache.set(key, tracker_page, timeout)
    return tracker_page


def _get_player_tracker(tracker: UUID, tracked_team: int, tracked_player: int, want_generic: bool):
    # Team and player must be positive and greater than zero
    if tracked_team < 0 or tracked_player < 1:
        abort(404)

    room: Optional[Room] = Room.get(tracker=tracker)
    if not room:
        abort(404)

    # Collect seed information and pare it down to a single player
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, \
        precollected_items, games, slot_data, groups, saving_second = get_static_room_data(room)
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
        multisave: Dict[str, Any] = restricted_loads(room.multisave)
    else:
        multisave: Dict[str, Any] = {}

    slots_aimed_at_player = {tracked_player}
    for group_id, group_members in groups.items():
        if tracked_player in group_members:
            slots_aimed_at_player.add(group_id)

    # Add items to player inventory
    for (ms_team, ms_player), locations_checked in multisave.get("location_checks", {}).items():
        # Skip teams and players not matching the request
        player_locations = locations[ms_player]
        if ms_team == tracked_team:
            # If the player does not have the item, do nothing
            for location in locations_checked:
                if location in player_locations:
                    item, recipient, flags = player_locations[location]
                    if recipient in slots_aimed_at_player:  # a check done for the tracked player
                        attribute_item_solo(inventory, item)
                    if ms_player == tracked_player:  # a check done by the tracked player
                        checks_done[location_to_area[location]] += 1
                        checks_done["Total"] += 1
    specific_tracker = game_specific_trackers.get(games[tracked_player], None)
    if specific_tracker and not want_generic:
        tracker =  specific_tracker(multisave, room, locations, inventory, tracked_team, tracked_player, player_name,
                                seed_checks_in_area, checks_done, slot_data[tracked_player], saving_second)
    else:
        tracker =  __renderGenericTracker(multisave, room, locations, inventory, tracked_team, tracked_player, player_name,
                                      seed_checks_in_area, checks_done, saving_second)

    return (saving_second - datetime.datetime.now().second) % 60 or 60, tracker


@app.route('/generic_tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
def get_generic_tracker(tracker: UUID, tracked_team: int, tracked_player: int):
    return get_player_tracker(tracker, tracked_team, tracked_player, True)


def __renderAlttpTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                         inventory: Counter, team: int, player: int, player_name: str,
                         seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict,
                         saving_second: int) -> str:

    # Note the presence of the triforce item
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
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
        level = min(inventory[item_id], len(progressive_names[item_name]) - 1)
        display_name = progressive_names[item_name][level]
        acquired = True
        if not display_name:
            acquired = False
            display_name = progressive_names[item_name][level + 1]
        base_name = item_name.split(maxsplit=1)[1].lower()
        display_data[base_name + "_acquired"] = acquired
        display_data[base_name + "_url"] = alttp_icons[display_name]

    # The single player tracker doesn't care about overworld, underworld, and total checks. Maybe it should?
    sp_areas = ordered_areas[2:15]

    player_big_key_locations = set()
    player_small_key_locations = set()
    for loc_data in locations.values():
        for values in loc_data.values():
            item_id, item_player, flags = values
            if item_player == player:
                if item_id in ids_big_key:
                    player_big_key_locations.add(ids_big_key[item_id])
                elif item_id in ids_small_key:
                    player_small_key_locations.add(ids_small_key[item_id])

    return render_template("lttpTracker.html", inventory=inventory,
                            player_name=player_name, room=room, icons=alttp_icons, checks_done=checks_done,
                            checks_in_area=seed_checks_in_area[player],
                            acquired_items={lookup_any_item_id_to_name[id] for id in inventory},
                            small_key_ids=small_key_ids, big_key_ids=big_key_ids, sp_areas=sp_areas,
                            key_locations=player_small_key_locations,
                            big_key_locations=player_big_key_locations,
                            **display_data)


def __renderMinecraftTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                             inventory: Counter, team: int, player: int, playerName: str,
                             seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict,
                             saving_second: int) -> str:

    icons = {
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
        "Brewing Stand": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b3/Brewing_Stand_%28empty%29_JE10.png",
        "Ender Pearl": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f6/Ender_Pearl_JE3_BE2.png",
        "Bucket": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Bucket_JE2_BE2.png",
        "Bow": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/ab/Bow_%28Pull_2%29_JE1_BE1.png",
        "Shield": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c6/Shield_JE2_BE1.png",
        "Red Bed": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/6a/Red_Bed_%28N%29.png",
        "Netherite Scrap": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/33/Netherite_Scrap_JE2_BE1.png",
        "Flint and Steel": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/94/Flint_and_Steel_JE4_BE2.png",
        "Enchanting Table": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Enchanting_Table.gif",
        "Fishing Rod": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7f/Fishing_Rod_JE2_BE2.png",
        "Campfire": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/91/Campfire_JE2_BE2.gif",
        "Water Bottle": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/75/Water_Bottle_JE2_BE2.png",
        "Spyglass": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c1/Spyglass_JE2_BE1.png",
        "Dragon Egg Shard": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/38/Dragon_Egg_JE4.png",
        "Lead": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/1/1f/Lead_JE2_BE2.png", 
        "Saddle": "https://i.imgur.com/2QtDyR0.png",
        "Channeling Book": "https://i.imgur.com/J3WsYZw.png",
        "Silk Touch Book": "https://i.imgur.com/iqERxHQ.png",
        "Piercing IV Book": "https://i.imgur.com/OzJptGz.png",
    }

    minecraft_location_ids = {
        "Story": [42073, 42023, 42027, 42039, 42002, 42009, 42010, 42070, 
                  42041, 42049, 42004, 42031, 42025, 42029, 42051, 42077],
        "Nether": [42017, 42044, 42069, 42058, 42034, 42060, 42066, 42076, 42064, 42071, 42021,
                   42062, 42008, 42061, 42033, 42011, 42006, 42019, 42000, 42040, 42001, 42015, 42104, 42014],
        "The End": [42052, 42005, 42012, 42032, 42030, 42042, 42018, 42038, 42046],
        "Adventure": [42047, 42050, 42096, 42097, 42098, 42059, 42055, 42072, 42003, 42109, 42035, 42016, 42020,
                      42048, 42054, 42068, 42043, 42106, 42074, 42075, 42024, 42026, 42037, 42045, 42056, 42105, 42099, 42103, 42110, 42100],
        "Husbandry": [42065, 42067, 42078, 42022, 42113, 42107, 42007, 42079, 42013, 42028, 42036, 42108, 42111, 42112,
                      42057, 42063, 42053, 42102, 42101, 42092, 42093, 42094, 42095],
        "Archipelago": [42080, 42081, 42082, 42083, 42084, 42085, 42086, 42087, 42088, 42089, 42090, 42091],
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
        level = min(inventory[item_id], len(progressive_names[item_name]) - 1)
        display_name = progressive_names[item_name][level]
        base_name = item_name.split(maxsplit=1)[1].lower().replace(' ', '_')
        display_data[base_name + "_url"] = icons[display_name]

    # Multi-items
    multi_items = {
        "3 Ender Pearls": 45029,
        "8 Netherite Scrap": 45015,
        "Dragon Egg Shard": 45043
    }
    for item_name, item_id in multi_items.items():
        base_name = item_name.split()[-1].lower()
        count = inventory[item_id]
        if count >= 0:
            display_data[base_name + "_count"] = count

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    # Turn location IDs into advancement tab counts
    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    lookup_name = lambda id: lookup_any_location_id_to_name[id]
    location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                        for tab_name, tab_locations in minecraft_location_ids.items()}
    checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                    for tab_name, tab_locations in minecraft_location_ids.items()}
    checks_done['Total'] = len(checked_locations)
    checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in minecraft_location_ids.items()}
    checks_in_area['Total'] = sum(checks_in_area.values())

    return render_template("minecraftTracker.html",
                            inventory=inventory, icons=icons,
                            acquired_items={lookup_any_item_id_to_name[id] for id in inventory if
                                            id in lookup_any_item_id_to_name},
                            player=player, team=team, room=room, player_name=playerName, saving_second = saving_second,
                            checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                            **display_data)


def __renderOoTTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                       inventory: Counter, team: int, player: int, playerName: str,
                       seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict,
                       saving_second: int) -> str:

    icons = {
        "Fairy Ocarina":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/97/OoT_Fairy_Ocarina_Icon.png",
        "Ocarina of Time":          "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Ocarina_of_Time_Icon.png",
        "Slingshot":                "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/32/OoT_Fairy_Slingshot_Icon.png",
        "Boomerang":                "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d5/OoT_Boomerang_Icon.png",
        "Bottle":                   "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/fc/OoT_Bottle_Icon.png",
        "Rutos Letter":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/OoT_Letter_Icon.png",
        "Bombs":                    "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/11/OoT_Bomb_Icon.png",
        "Bombchus":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/36/OoT_Bombchu_Icon.png",
        "Lens of Truth":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/05/OoT_Lens_of_Truth_Icon.png",
        "Bow":                      "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/9a/OoT_Fairy_Bow_Icon.png",
        "Hookshot":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/OoT_Hookshot_Icon.png",
        "Longshot":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a4/OoT_Longshot_Icon.png",
        "Megaton Hammer":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/93/OoT_Megaton_Hammer_Icon.png",
        "Fire Arrows":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/1e/OoT_Fire_Arrow_Icon.png",
        "Ice Arrows":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3c/OoT_Ice_Arrow_Icon.png",
        "Light Arrows":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/76/OoT_Light_Arrow_Icon.png",
        "Dins Fire":                r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/da/OoT_Din%27s_Fire_Icon.png",
        "Farores Wind":             r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/7a/OoT_Farore%27s_Wind_Icon.png",
        "Nayrus Love":              r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/be/OoT_Nayru%27s_Love_Icon.png",
        "Kokiri Sword":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/53/OoT_Kokiri_Sword_Icon.png",
        "Biggoron Sword":           r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/OoT_Giant%27s_Knife_Icon.png",
        "Mirror Shield":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b0/OoT_Mirror_Shield_Icon_2.png",
        "Goron Bracelet":           r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b7/OoT_Goron%27s_Bracelet_Icon.png",
        "Silver Gauntlets":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b9/OoT_Silver_Gauntlets_Icon.png",
        "Golden Gauntlets":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/6a/OoT_Golden_Gauntlets_Icon.png",
        "Goron Tunic":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/1c/OoT_Goron_Tunic_Icon.png",
        "Zora Tunic":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2c/OoT_Zora_Tunic_Icon.png",
        "Silver Scale":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Silver_Scale_Icon.png",
        "Gold Scale":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/95/OoT_Golden_Scale_Icon.png",
        "Iron Boots":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/34/OoT_Iron_Boots_Icon.png",
        "Hover Boots":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/22/OoT_Hover_Boots_Icon.png",
        "Adults Wallet":            r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f9/OoT_Adult%27s_Wallet_Icon.png",
        "Giants Wallet":            r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/8/87/OoT_Giant%27s_Wallet_Icon.png",
        "Small Magic":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/9f/OoT3D_Magic_Jar_Icon.png",
        "Large Magic":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3e/OoT3D_Large_Magic_Jar_Icon.png",
        "Gerudo Membership Card":   "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Gerudo_Token_Icon.png",
        "Gold Skulltula Token":     "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/47/OoT_Token_Icon.png",
        "Triforce Piece":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/0b/SS_Triforce_Piece_Icon.png",
        "Triforce":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/68/ALttP_Triforce_Title_Sprite.png",
        "Zeldas Lullaby":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Eponas Song":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Sarias Song":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Suns Song":                "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Song of Time":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Song of Storms":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
        "Minuet of Forest":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e4/Green_Note.png",
        "Bolero of Fire":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/Red_Note.png",
        "Serenade of Water":        "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/0f/Blue_Note.png",
        "Requiem of Spirit":        "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a4/Orange_Note.png",
        "Nocturne of Shadow":       "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/97/Purple_Note.png",
        "Prelude of Light":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/90/Yellow_Note.png",
        "Small Key":                "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e5/OoT_Small_Key_Icon.png",
        "Boss Key":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/40/OoT_Boss_Key_Icon.png",
    }

    display_data = {}

    # Determine display for progressive items
    progressive_items = {
        "Progressive Hookshot": 66128,
        "Progressive Strength Upgrade": 66129,
        "Progressive Wallet": 66133,
        "Progressive Scale": 66134,
        "Magic Meter": 66138,
        "Ocarina": 66139,
    }

    progressive_names = {
        "Progressive Hookshot": ["Hookshot", "Hookshot", "Longshot"],
        "Progressive Strength Upgrade": ["Goron Bracelet", "Goron Bracelet", "Silver Gauntlets", "Golden Gauntlets"],
        "Progressive Wallet": ["Adults Wallet", "Adults Wallet", "Giants Wallet", "Giants Wallet"],
        "Progressive Scale": ["Silver Scale", "Silver Scale", "Gold Scale"],
        "Magic Meter": ["Small Magic", "Small Magic", "Large Magic"],
        "Ocarina": ["Fairy Ocarina", "Fairy Ocarina", "Ocarina of Time"]
    }

    for item_name, item_id in progressive_items.items():
        level = min(inventory[item_id], len(progressive_names[item_name])-1)
        display_name = progressive_names[item_name][level]
        if item_name.startswith("Progressive"):
            base_name = item_name.split(maxsplit=1)[1].lower().replace(' ', '_')
        else:
            base_name = item_name.lower().replace(' ', '_')
        display_data[base_name+"_url"] = icons[display_name]

        if base_name == "hookshot":
            display_data['hookshot_length'] = {0: '', 1: 'H', 2: 'L'}.get(level)
        if base_name == "wallet": 
            display_data['wallet_size'] = {0: '99', 1: '200', 2: '500', 3: '999'}.get(level)

    # Determine display for bottles. Show letter if it's obtained, determine bottle count
    bottle_ids = [66015, 66020, 66021, 66140, 66141, 66142, 66143, 66144, 66145, 66146, 66147, 66148]
    display_data['bottle_count'] = min(sum(map(lambda item_id: inventory[item_id], bottle_ids)), 4)
    display_data['bottle_url'] = icons['Rutos Letter'] if inventory[66021] > 0 else icons['Bottle']

    # Determine bombchu display
    display_data['has_bombchus'] = any(map(lambda item_id: inventory[item_id] > 0, [66003, 66106, 66107, 66137]))

    # Multi-items
    multi_items = {
        "Gold Skulltula Token": 66091,
        "Triforce Piece": 66202,
    }
    for item_name, item_id in multi_items.items():
        base_name = item_name.split()[-1].lower()
        count = inventory[item_id]
        display_data[base_name+"_count"] = inventory[item_id]

    # Gather dungeon locations
    area_id_ranges = {
        "Overworld":                ((67000, 67263), (67269, 67280), (67747, 68024), (68054, 68062)),
        "Deku Tree":                ((67281, 67303), (68063, 68077)),
        "Dodongo's Cavern":         ((67304, 67334), (68078, 68160)),
        "Jabu Jabu's Belly":        ((67335, 67359), (68161, 68188)),
        "Bottom of the Well":       ((67360, 67384), (68189, 68230)),
        "Forest Temple":            ((67385, 67420), (68231, 68281)),
        "Fire Temple":              ((67421, 67457), (68282, 68350)),
        "Water Temple":             ((67458, 67484), (68351, 68483)),
        "Shadow Temple":            ((67485, 67532), (68484, 68565)),
        "Spirit Temple":            ((67533, 67582), (68566, 68625)),
        "Ice Cavern":               ((67583, 67596), (68626, 68649)),
        "Gerudo Training Ground":   ((67597, 67635), (68650, 68656)),
        "Thieves' Hideout":         ((67264, 67268), (68025, 68053)),
        "Ganon's Castle":           ((67636, 67673), (68657, 68705)),
    }

    def lookup_and_trim(id, area):
        full_name = lookup_any_location_id_to_name[id]
        if 'Ganons Tower' in full_name:
            return full_name
        if area not in ["Overworld", "Thieves' Hideout"]:
            # trim dungeon name. leaves an extra space that doesn't display, or trims fully for DC/Jabu/GC
            return full_name[len(area):]
        return full_name

    checked_locations = multisave.get("location_checks", {}).get((team, player), set()).intersection(set(locations[player]))
    location_info = {}
    checks_done = {}
    checks_in_area = {}
    for area, ranges in area_id_ranges.items():
        location_info[area] = {}
        checks_done[area] = 0
        checks_in_area[area] = 0
        for r in ranges:
            min_id, max_id = r
            for id in range(min_id, max_id+1):
                if id in locations[player]:
                    checked = id in checked_locations
                    location_info[area][lookup_and_trim(id, area)] = checked
                    checks_in_area[area] += 1
                    checks_done[area] += checked

    checks_done['Total'] = sum(checks_done.values())
    checks_in_area['Total'] = sum(checks_in_area.values())

    # Give skulltulas on non-tracked locations
    non_tracked_locations = multisave.get("location_checks", {}).get((team, player), set()).difference(set(locations[player]))
    for id in non_tracked_locations:
        if "GS" in lookup_and_trim(id, ''):
            display_data["token_count"] += 1

    oot_y = '✔'
    oot_x = '✕'

    # Gather small and boss key info
    small_key_counts = {
        "Forest Temple":            oot_y if inventory[66203] else inventory[66175],
        "Fire Temple":              oot_y if inventory[66204] else inventory[66176],
        "Water Temple":             oot_y if inventory[66205] else inventory[66177],
        "Spirit Temple":            oot_y if inventory[66206] else inventory[66178],
        "Shadow Temple":            oot_y if inventory[66207] else inventory[66179],
        "Bottom of the Well":       oot_y if inventory[66208] else inventory[66180],
        "Gerudo Training Ground":   oot_y if inventory[66209] else inventory[66181],
        "Thieves' Hideout":         oot_y if inventory[66210] else inventory[66182],
        "Ganon's Castle":           oot_y if inventory[66211] else inventory[66183],
    }
    boss_key_counts = {
        "Forest Temple":            oot_y if inventory[66149] else oot_x,
        "Fire Temple":              oot_y if inventory[66150] else oot_x,
        "Water Temple":             oot_y if inventory[66151] else oot_x,
        "Spirit Temple":            oot_y if inventory[66152] else oot_x,
        "Shadow Temple":            oot_y if inventory[66153] else oot_x,
        "Ganon's Castle":           oot_y if inventory[66154] else oot_x,
    }

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    return render_template("ootTracker.html",
                           inventory=inventory, player=player, team=team, room=room, player_name=playerName,
                           icons=icons, acquired_items={lookup_any_item_id_to_name[id] for id in inventory},
                           checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                           small_key_counts=small_key_counts, boss_key_counts=boss_key_counts,
                           **display_data)


def __renderTimespinnerTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                               inventory: Counter, team: int, player: int, playerName: str,
                               seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int],
                               slot_data: Dict[str, Any], saving_second: int) -> str:

    icons = {
        "Timespinner Wheel":    "https://timespinnerwiki.com/mediawiki/images/7/76/Timespinner_Wheel.png",
        "Timespinner Spindle":  "https://timespinnerwiki.com/mediawiki/images/1/1a/Timespinner_Spindle.png",
        "Timespinner Gear 1":   "https://timespinnerwiki.com/mediawiki/images/3/3c/Timespinner_Gear_1.png",
        "Timespinner Gear 2":   "https://timespinnerwiki.com/mediawiki/images/e/e9/Timespinner_Gear_2.png",
        "Timespinner Gear 3":   "https://timespinnerwiki.com/mediawiki/images/2/22/Timespinner_Gear_3.png",
        "Talaria Attachment":   "https://timespinnerwiki.com/mediawiki/images/6/61/Talaria_Attachment.png",
        "Succubus Hairpin":     "https://timespinnerwiki.com/mediawiki/images/4/49/Succubus_Hairpin.png",
        "Lightwall":            "https://timespinnerwiki.com/mediawiki/images/0/03/Lightwall.png",
        "Celestial Sash":       "https://timespinnerwiki.com/mediawiki/images/f/f1/Celestial_Sash.png",
        "Twin Pyramid Key":     "https://timespinnerwiki.com/mediawiki/images/4/49/Twin_Pyramid_Key.png",
        "Security Keycard D":   "https://timespinnerwiki.com/mediawiki/images/1/1b/Security_Keycard_D.png",
        "Security Keycard C":   "https://timespinnerwiki.com/mediawiki/images/e/e5/Security_Keycard_C.png",
        "Security Keycard B":   "https://timespinnerwiki.com/mediawiki/images/f/f6/Security_Keycard_B.png",
        "Security Keycard A":   "https://timespinnerwiki.com/mediawiki/images/b/b9/Security_Keycard_A.png",
        "Library Keycard V":    "https://timespinnerwiki.com/mediawiki/images/5/50/Library_Keycard_V.png",
        "Tablet":               "https://timespinnerwiki.com/mediawiki/images/a/a0/Tablet.png",
        "Elevator Keycard":     "https://timespinnerwiki.com/mediawiki/images/5/55/Elevator_Keycard.png",
        "Oculus Ring":          "https://timespinnerwiki.com/mediawiki/images/8/8d/Oculus_Ring.png",
        "Water Mask":           "https://timespinnerwiki.com/mediawiki/images/0/04/Water_Mask.png",
        "Gas Mask":             "https://timespinnerwiki.com/mediawiki/images/2/2e/Gas_Mask.png",
        "Djinn Inferno":        "https://timespinnerwiki.com/mediawiki/images/f/f6/Djinn_Inferno.png",
        "Pyro Ring":            "https://timespinnerwiki.com/mediawiki/images/2/2c/Pyro_Ring.png",
        "Infernal Flames":      "https://timespinnerwiki.com/mediawiki/images/1/1f/Infernal_Flames.png",
        "Fire Orb":             "https://timespinnerwiki.com/mediawiki/images/3/3e/Fire_Orb.png",
        "Royal Ring":           "https://timespinnerwiki.com/mediawiki/images/f/f3/Royal_Ring.png",
        "Plasma Geyser":        "https://timespinnerwiki.com/mediawiki/images/1/12/Plasma_Geyser.png",
        "Plasma Orb":           "https://timespinnerwiki.com/mediawiki/images/4/44/Plasma_Orb.png",
        "Kobo":                 "https://timespinnerwiki.com/mediawiki/images/c/c6/Familiar_Kobo.png",
        "Merchant Crow":        "https://timespinnerwiki.com/mediawiki/images/4/4e/Familiar_Crow.png",
    }

    timespinner_location_ids = {
        "Present": [ 
            1337000, 1337001, 1337002, 1337003, 1337004, 1337005, 1337006, 1337007, 1337008, 1337009,
            1337010, 1337011, 1337012, 1337013, 1337014, 1337015, 1337016, 1337017, 1337018, 1337019,
            1337020, 1337021, 1337022, 1337023, 1337024, 1337025, 1337026, 1337027, 1337028, 1337029,
            1337030, 1337031, 1337032, 1337033, 1337034, 1337035, 1337036, 1337037, 1337038, 1337039,
            1337040, 1337041, 1337042, 1337043, 1337044, 1337045, 1337046, 1337047, 1337048, 1337049,
            1337050, 1337051, 1337052, 1337053, 1337054, 1337055, 1337056, 1337057, 1337058, 1337059,
            1337060, 1337061, 1337062, 1337063, 1337064, 1337065, 1337066, 1337067, 1337068, 1337069,
            1337070, 1337071, 1337072, 1337073, 1337074, 1337075, 1337076, 1337077, 1337078, 1337079,
            1337080, 1337081, 1337082, 1337083, 1337084, 1337085],
        "Past": [
                                                                  1337086, 1337087, 1337088, 1337089,
            1337090, 1337091, 1337092, 1337093, 1337094, 1337095, 1337096, 1337097, 1337098, 1337099,
            1337100, 1337101, 1337102, 1337103, 1337104, 1337105, 1337106, 1337107, 1337108, 1337109,
            1337110, 1337111, 1337112, 1337113, 1337114, 1337115, 1337116, 1337117, 1337118, 1337119,
            1337120, 1337121, 1337122, 1337123, 1337124, 1337125, 1337126, 1337127, 1337128, 1337129,
            1337130, 1337131, 1337132, 1337133, 1337134, 1337135, 1337136, 1337137, 1337138, 1337139,
            1337140, 1337141, 1337142, 1337143, 1337144, 1337145, 1337146, 1337147, 1337148, 1337149,
            1337150, 1337151, 1337152, 1337153, 1337154, 1337155,
                     1337171, 1337172, 1337173, 1337174, 1337175],
        "Ancient Pyramid": [
                                                                  1337236, 
                                                                  1337246, 1337247, 1337248, 1337249]
    }

    if(slot_data["DownloadableItems"]):
        timespinner_location_ids["Present"] += [
                                                                  1337156, 1337157,          1337159,
            1337160, 1337161, 1337162, 1337163, 1337164, 1337165, 1337166, 1337167, 1337168, 1337169, 
            1337170]
    if(slot_data["Cantoran"]):
        timespinner_location_ids["Past"].append(1337176)
    if(slot_data["LoreChecks"]):
        timespinner_location_ids["Present"] += [
                                                                           1337177, 1337178, 1337179, 
            1337180, 1337181, 1337182, 1337183, 1337184, 1337185, 1337186, 1337187]
        timespinner_location_ids["Past"] += [
                                                                                    1337188, 1337189,
            1337190, 1337191, 1337192, 1337193, 1337194, 1337195, 1337196, 1337197, 1337198]
    if(slot_data["GyreArchives"]):
        timespinner_location_ids["Ancient Pyramid"] += [
                                                                           1337237, 1337238, 1337239,
            1337240, 1337241, 1337242, 1337243, 1337244, 1337245]

    display_data = {}

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    # Turn location IDs into advancement tab counts
    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    lookup_name = lambda id: lookup_any_location_id_to_name[id]
    location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                        for tab_name, tab_locations in timespinner_location_ids.items()}
    checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                    for tab_name, tab_locations in timespinner_location_ids.items()}
    checks_done['Total'] = len(checked_locations)
    checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in timespinner_location_ids.items()}
    checks_in_area['Total'] = sum(checks_in_area.values())
    acquired_items = {lookup_any_item_id_to_name[id] for id in inventory if id in lookup_any_item_id_to_name}
    options = {k for k, v in slot_data.items() if v}

    return render_template("timespinnerTracker.html",
                            inventory=inventory, icons=icons, acquired_items=acquired_items,
                            player=player, team=team, room=room, player_name=playerName,
                            checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                            options=options, **display_data)

def __renderSuperMetroidTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                                inventory: Counter, team: int, player: int, playerName: str,
                                seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict,
                                saving_second: int) -> str:

    icons = {
        "Energy Tank":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/ETank.png",
        "Missile":          "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Missile.png",
        "Super Missile":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Super.png",
        "Power Bomb":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/PowerBomb.png",
        "Bomb":             "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Bomb.png",
        "Charge Beam":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Charge.png",
        "Ice Beam":         "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Ice.png",
        "Hi-Jump Boots":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/HiJump.png",
        "Speed Booster":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/SpeedBooster.png",
        "Wave Beam":        "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Wave.png",
        "Spazer":           "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Spazer.png",
        "Spring Ball":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/SpringBall.png",
        "Varia Suit":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Varia.png",
        "Plasma Beam":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Plasma.png",
        "Grappling Beam":   "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Grapple.png",
        "Morph Ball":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Morph.png",
        "Reserve Tank":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Reserve.png",
        "Gravity Suit":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Gravity.png",
        "X-Ray Scope":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/XRayScope.png",
        "Space Jump":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/SpaceJump.png",
        "Screw Attack":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/ScrewAttack.png",
        "Nothing":          "",
        "No Energy":        "",
        "Kraid":            "",
        "Phantoon":         "",
        "Draygon":          "",
        "Ridley":           "",
        "Mother Brain":     "",
    }

    multi_items = {
        "Energy Tank": 83000,
        "Missile": 83001,
        "Super Missile": 83002,
        "Power Bomb": 83003,
        "Reserve Tank": 83020,
    }

    supermetroid_location_ids = {
        'Crateria/Blue Brinstar': [82005, 82007, 82008, 82026, 82029,
                     82000, 82004, 82006, 82009, 82010,
                     82011, 82012, 82027, 82028, 82034,
                     82036, 82037],
        'Green/Pink Brinstar': [82017, 82023, 82030, 82033, 82035,
                              82013, 82014, 82015, 82016, 82018,
                              82019, 82021, 82022, 82024, 82025,
                              82031],
        'Red Brinstar': [82038, 82042, 82039, 82040, 82041],
        'Kraid': [82043, 82048, 82044],
        'Norfair': [82050, 82053, 82061, 82066, 82068,
                    82049, 82051, 82054, 82055, 82056,
                    82062, 82063, 82064, 82065, 82067],
        'Lower Norfair': [82078, 82079, 82080, 82070, 82071,
                         82073, 82074, 82075, 82076, 82077],
        'Crocomire': [82052, 82060, 82057, 82058, 82059],
        'Wrecked Ship': [82129, 82132, 82134, 82135, 82001,
                        82002, 82003, 82128, 82130, 82131,
                        82133],
        'West Maridia': [82138, 82136, 82137, 82139, 82140,
                        82141, 82142],
        'East Maridia': [82143, 82145, 82150, 82152, 82154,
                        82144, 82146, 82147, 82148, 82149,
                        82151],
    }

    display_data = {}


    for item_name, item_id in multi_items.items():
        base_name = item_name.split()[0].lower()
        display_data[base_name+"_count"] = inventory[item_id]

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    # Turn location IDs into advancement tab counts
    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    lookup_name = lambda id: lookup_any_location_id_to_name[id]
    location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                     for tab_name, tab_locations in supermetroid_location_ids.items()}
    checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                   for tab_name, tab_locations in supermetroid_location_ids.items()}
    checks_done['Total'] = len(checked_locations)
    checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in supermetroid_location_ids.items()}
    checks_in_area['Total'] = sum(checks_in_area.values())

    return render_template("supermetroidTracker.html",
                            inventory=inventory, icons=icons,
                            acquired_items={lookup_any_item_id_to_name[id] for id in inventory if
                                            id in lookup_any_item_id_to_name},
                            player=player, team=team, room=room, player_name=playerName,
                            checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                            **display_data)

def __renderSC2WoLTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                          inventory: Counter, team: int, player: int, playerName: str,
                          seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int],
                          slot_data: Dict, saving_second: int) -> str:

    SC2WOL_LOC_ID_OFFSET = 1000
    SC2WOL_ITEM_ID_OFFSET = 1000

    icons = {
        "Starting Minerals": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/icons/icon-mineral-protoss.png",
        "Starting Vespene": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/icons/icon-gas-terran.png",
        "Starting Supply": "https://static.wikia.nocookie.net/starcraft/images/d/d3/TerranSupply_SC2_Icon1.gif",

        "Infantry Weapons Level 1": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryweaponslevel1.png",
        "Infantry Weapons Level 2": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryweaponslevel2.png",
        "Infantry Weapons Level 3": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryweaponslevel3.png",
        "Infantry Armor Level 1": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryarmorlevel1.png",
        "Infantry Armor Level 2": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryarmorlevel2.png",
        "Infantry Armor Level 3": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryarmorlevel3.png",
        "Vehicle Weapons Level 1": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleweaponslevel1.png",
        "Vehicle Weapons Level 2": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleweaponslevel2.png",
        "Vehicle Weapons Level 3": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleweaponslevel3.png",
        "Vehicle Armor Level 1": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleplatinglevel1.png",
        "Vehicle Armor Level 2": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleplatinglevel2.png",
        "Vehicle Armor Level 3": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleplatinglevel3.png",
        "Ship Weapons Level 1": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipweaponslevel1.png",
        "Ship Weapons Level 2": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipweaponslevel2.png",
        "Ship Weapons Level 3": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipweaponslevel3.png",
        "Ship Armor Level 1": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipplatinglevel1.png",
        "Ship Armor Level 2": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipplatinglevel2.png",
        "Ship Armor Level 3": "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipplatinglevel3.png",

        "Bunker": "https://static.wikia.nocookie.net/starcraft/images/c/c5/Bunker_SC2_Icon1.jpg",
        "Missile Turret": "https://static.wikia.nocookie.net/starcraft/images/5/5f/MissileTurret_SC2_Icon1.jpg",
        "Sensor Tower": "https://static.wikia.nocookie.net/starcraft/images/d/d2/SensorTower_SC2_Icon1.jpg",

        "Projectile Accelerator (Bunker)": "https://0rganics.org/archipelago/sc2wol/ProjectileAccelerator.png",
        "Neosteel Bunker (Bunker)": "https://0rganics.org/archipelago/sc2wol/NeosteelBunker.png",
        "Titanium Housing (Missile Turret)": "https://0rganics.org/archipelago/sc2wol/TitaniumHousing.png",
        "Hellstorm Batteries (Missile Turret)": "https://0rganics.org/archipelago/sc2wol/HellstormBatteries.png",
        "Advanced Construction (SCV)": "https://0rganics.org/archipelago/sc2wol/AdvancedConstruction.png",
        "Dual-Fusion Welders (SCV)": "https://0rganics.org/archipelago/sc2wol/Dual-FusionWelders.png",
        "Fire-Suppression System (Building)": "https://0rganics.org/archipelago/sc2wol/Fire-SuppressionSystem.png",
        "Orbital Command (Building)": "https://0rganics.org/archipelago/sc2wol/OrbitalCommandCampaign.png",

        "Marine": "https://static.wikia.nocookie.net/starcraft/images/4/47/Marine_SC2_Icon1.jpg",
        "Medic": "https://static.wikia.nocookie.net/starcraft/images/7/74/Medic_SC2_Rend1.jpg",
        "Firebat": "https://static.wikia.nocookie.net/starcraft/images/3/3c/Firebat_SC2_Rend1.jpg",
        "Marauder": "https://static.wikia.nocookie.net/starcraft/images/b/ba/Marauder_SC2_Icon1.jpg",
        "Reaper": "https://static.wikia.nocookie.net/starcraft/images/7/7d/Reaper_SC2_Icon1.jpg",

        "Stimpack (Marine)": "https://0rganics.org/archipelago/sc2wol/StimpacksCampaign.png",
        "Combat Shield (Marine)": "https://0rganics.org/archipelago/sc2wol/CombatShieldCampaign.png",
        "Advanced Medic Facilities (Medic)": "https://0rganics.org/archipelago/sc2wol/AdvancedMedicFacilities.png",
        "Stabilizer Medpacks (Medic)": "https://0rganics.org/archipelago/sc2wol/StabilizerMedpacks.png",
        "Incinerator Gauntlets (Firebat)": "https://0rganics.org/archipelago/sc2wol/IncineratorGauntlets.png",
        "Juggernaut Plating (Firebat)": "https://0rganics.org/archipelago/sc2wol/JuggernautPlating.png",
        "Concussive Shells (Marauder)": "https://0rganics.org/archipelago/sc2wol/ConcussiveShellsCampaign.png",
        "Kinetic Foam (Marauder)": "https://0rganics.org/archipelago/sc2wol/KineticFoam.png",
        "U-238 Rounds (Reaper)": "https://0rganics.org/archipelago/sc2wol/U-238Rounds.png",
        "G-4 Clusterbomb (Reaper)": "https://0rganics.org/archipelago/sc2wol/G-4Clusterbomb.png",

        "Hellion": "https://static.wikia.nocookie.net/starcraft/images/5/56/Hellion_SC2_Icon1.jpg",
        "Vulture": "https://static.wikia.nocookie.net/starcraft/images/d/da/Vulture_WoL.jpg",
        "Goliath": "https://static.wikia.nocookie.net/starcraft/images/e/eb/Goliath_WoL.jpg",
        "Diamondback": "https://static.wikia.nocookie.net/starcraft/images/a/a6/Diamondback_WoL.jpg",
        "Siege Tank": "https://static.wikia.nocookie.net/starcraft/images/5/57/SiegeTank_SC2_Icon1.jpg",

        "Twin-Linked Flamethrower (Hellion)": "https://0rganics.org/archipelago/sc2wol/Twin-LinkedFlamethrower.png",
        "Thermite Filaments (Hellion)": "https://0rganics.org/archipelago/sc2wol/ThermiteFilaments.png",
        "Cerberus Mine (Vulture)": "https://0rganics.org/archipelago/sc2wol/CerberusMine.png",
        "Replenishable Magazine (Vulture)": "https://0rganics.org/archipelago/sc2wol/ReplenishableMagazine.png",
        "Multi-Lock Weapons System (Goliath)": "https://0rganics.org/archipelago/sc2wol/Multi-LockWeaponsSystem.png",
        "Ares-Class Targeting System (Goliath)": "https://0rganics.org/archipelago/sc2wol/Ares-ClassTargetingSystem.png",
        "Tri-Lithium Power Cell (Diamondback)": "https://0rganics.org/archipelago/sc2wol/Tri-LithiumPowerCell.png",
        "Shaped Hull (Diamondback)": "https://0rganics.org/archipelago/sc2wol/ShapedHull.png",
        "Maelstrom Rounds (Siege Tank)": "https://0rganics.org/archipelago/sc2wol/MaelstromRounds.png",
        "Shaped Blast (Siege Tank)": "https://0rganics.org/archipelago/sc2wol/ShapedBlast.png",

        "Medivac": "https://static.wikia.nocookie.net/starcraft/images/d/db/Medivac_SC2_Icon1.jpg",
        "Wraith": "https://static.wikia.nocookie.net/starcraft/images/7/75/Wraith_WoL.jpg",
        "Viking": "https://static.wikia.nocookie.net/starcraft/images/2/2a/Viking_SC2_Icon1.jpg",
        "Banshee": "https://static.wikia.nocookie.net/starcraft/images/3/32/Banshee_SC2_Icon1.jpg",
        "Battlecruiser": "https://static.wikia.nocookie.net/starcraft/images/f/f5/Battlecruiser_SC2_Icon1.jpg",

        "Rapid Deployment Tube (Medivac)": "https://0rganics.org/archipelago/sc2wol/RapidDeploymentTube.png",
        "Advanced Healing AI (Medivac)": "https://0rganics.org/archipelago/sc2wol/AdvancedHealingAI.png",
        "Tomahawk Power Cells (Wraith)": "https://0rganics.org/archipelago/sc2wol/TomahawkPowerCells.png",
        "Displacement Field (Wraith)": "https://0rganics.org/archipelago/sc2wol/DisplacementField.png",
        "Ripwave Missiles (Viking)": "https://0rganics.org/archipelago/sc2wol/RipwaveMissiles.png",
        "Phobos-Class Weapons System (Viking)": "https://0rganics.org/archipelago/sc2wol/Phobos-ClassWeaponsSystem.png",
        "Cross-Spectrum Dampeners (Banshee)": "https://0rganics.org/archipelago/sc2wol/Cross-SpectrumDampeners.png",
        "Shockwave Missile Battery (Banshee)": "https://0rganics.org/archipelago/sc2wol/ShockwaveMissileBattery.png",
        "Missile Pods (Battlecruiser)": "https://0rganics.org/archipelago/sc2wol/MissilePods.png",
        "Defensive Matrix (Battlecruiser)": "https://0rganics.org/archipelago/sc2wol/DefensiveMatrix.png",

        "Ghost": "https://static.wikia.nocookie.net/starcraft/images/6/6e/Ghost_SC2_Icon1.jpg",
        "Spectre": "https://static.wikia.nocookie.net/starcraft/images/0/0d/Spectre_WoL.jpg",
        "Thor": "https://static.wikia.nocookie.net/starcraft/images/e/ef/Thor_SC2_Icon1.jpg",

        "Ocular Implants (Ghost)": "https://0rganics.org/archipelago/sc2wol/OcularImplants.png",
        "Crius Suit (Ghost)": "https://0rganics.org/archipelago/sc2wol/CriusSuit.png",
        "Psionic Lash (Spectre)": "https://0rganics.org/archipelago/sc2wol/PsionicLash.png",
        "Nyx-Class Cloaking Module (Spectre)": "https://0rganics.org/archipelago/sc2wol/Nyx-ClassCloakingModule.png",
        "330mm Barrage Cannon (Thor)": "https://0rganics.org/archipelago/sc2wol/330mmBarrageCannon.png",
        "Immortality Protocol (Thor)": "https://0rganics.org/archipelago/sc2wol/ImmortalityProtocol.png",

        "War Pigs": "https://static.wikia.nocookie.net/starcraft/images/e/ed/WarPigs_SC2_Icon1.jpg",
        "Devil Dogs": "https://static.wikia.nocookie.net/starcraft/images/3/33/DevilDogs_SC2_Icon1.jpg",
        "Hammer Securities": "https://static.wikia.nocookie.net/starcraft/images/3/3b/HammerSecurity_SC2_Icon1.jpg",
        "Spartan Company": "https://static.wikia.nocookie.net/starcraft/images/b/be/SpartanCompany_SC2_Icon1.jpg",
        "Siege Breakers": "https://static.wikia.nocookie.net/starcraft/images/3/31/SiegeBreakers_SC2_Icon1.jpg",
        "Hel's Angel": "https://static.wikia.nocookie.net/starcraft/images/6/63/HelsAngels_SC2_Icon1.jpg",
        "Dusk Wings": "https://static.wikia.nocookie.net/starcraft/images/5/52/DuskWings_SC2_Icon1.jpg",
        "Jackson's Revenge": "https://static.wikia.nocookie.net/starcraft/images/9/95/JacksonsRevenge_SC2_Icon1.jpg",

        "Ultra-Capacitors": "https://static.wikia.nocookie.net/starcraft/images/2/23/SC2_Lab_Ultra_Capacitors_Icon.png",
        "Vanadium Plating": "https://static.wikia.nocookie.net/starcraft/images/6/67/SC2_Lab_VanPlating_Icon.png",
        "Orbital Depots": "https://static.wikia.nocookie.net/starcraft/images/0/01/SC2_Lab_Orbital_Depot_Icon.png",
        "Micro-Filtering": "https://static.wikia.nocookie.net/starcraft/images/2/20/SC2_Lab_MicroFilter_Icon.png",
        "Automated Refinery": "https://static.wikia.nocookie.net/starcraft/images/7/71/SC2_Lab_Auto_Refinery_Icon.png",
        "Command Center Reactor": "https://static.wikia.nocookie.net/starcraft/images/e/ef/SC2_Lab_CC_Reactor_Icon.png",
        "Raven": "https://static.wikia.nocookie.net/starcraft/images/1/19/SC2_Lab_Raven_Icon.png",
        "Science Vessel": "https://static.wikia.nocookie.net/starcraft/images/c/c3/SC2_Lab_SciVes_Icon.png",
        "Tech Reactor": "https://static.wikia.nocookie.net/starcraft/images/c/c5/SC2_Lab_Tech_Reactor_Icon.png",
        "Orbital Strike": "https://static.wikia.nocookie.net/starcraft/images/d/df/SC2_Lab_Orb_Strike_Icon.png",

        "Shrike Turret": "https://static.wikia.nocookie.net/starcraft/images/4/44/SC2_Lab_Shrike_Turret_Icon.png",
        "Fortified Bunker": "https://static.wikia.nocookie.net/starcraft/images/4/4f/SC2_Lab_FortBunker_Icon.png",
        "Planetary Fortress": "https://static.wikia.nocookie.net/starcraft/images/0/0b/SC2_Lab_PlanetFortress_Icon.png",
        "Perdition Turret": "https://static.wikia.nocookie.net/starcraft/images/a/af/SC2_Lab_PerdTurret_Icon.png",
        "Predator": "https://static.wikia.nocookie.net/starcraft/images/8/83/SC2_Lab_Predator_Icon.png",
        "Hercules": "https://static.wikia.nocookie.net/starcraft/images/4/40/SC2_Lab_Hercules_Icon.png",
        "Cellular Reactor": "https://static.wikia.nocookie.net/starcraft/images/d/d8/SC2_Lab_CellReactor_Icon.png",
        "Regenerative Bio-Steel": "https://static.wikia.nocookie.net/starcraft/images/d/d3/SC2_Lab_BioSteel_Icon.png",
        "Hive Mind Emulator": "https://static.wikia.nocookie.net/starcraft/images/b/bc/SC2_Lab_Hive_Emulator_Icon.png",
        "Psi Disrupter": "https://static.wikia.nocookie.net/starcraft/images/c/cf/SC2_Lab_Psi_Disruptor_Icon.png",

        "Zealot": "https://static.wikia.nocookie.net/starcraft/images/6/6e/Icon_Protoss_Zealot.jpg",
        "Stalker": "https://static.wikia.nocookie.net/starcraft/images/0/0d/Icon_Protoss_Stalker.jpg",
        "High Templar": "https://static.wikia.nocookie.net/starcraft/images/a/a0/Icon_Protoss_High_Templar.jpg",
        "Dark Templar": "https://static.wikia.nocookie.net/starcraft/images/9/90/Icon_Protoss_Dark_Templar.jpg",
        "Immortal": "https://static.wikia.nocookie.net/starcraft/images/c/c1/Icon_Protoss_Immortal.jpg",
        "Colossus": "https://static.wikia.nocookie.net/starcraft/images/4/40/Icon_Protoss_Colossus.jpg",
        "Phoenix": "https://static.wikia.nocookie.net/starcraft/images/b/b1/Icon_Protoss_Phoenix.jpg",
        "Void Ray": "https://static.wikia.nocookie.net/starcraft/images/1/1d/VoidRay_SC2_Rend1.jpg",
        "Carrier": "https://static.wikia.nocookie.net/starcraft/images/2/2c/Icon_Protoss_Carrier.jpg",

        "Nothing": "",
    }

    sc2wol_location_ids = {
        "Liberation Day": [SC2WOL_LOC_ID_OFFSET + 100, SC2WOL_LOC_ID_OFFSET + 101, SC2WOL_LOC_ID_OFFSET + 102, SC2WOL_LOC_ID_OFFSET + 103, SC2WOL_LOC_ID_OFFSET + 104, SC2WOL_LOC_ID_OFFSET + 105, SC2WOL_LOC_ID_OFFSET + 106],
        "The Outlaws": [SC2WOL_LOC_ID_OFFSET + 200, SC2WOL_LOC_ID_OFFSET + 201],
        "Zero Hour": [SC2WOL_LOC_ID_OFFSET + 300, SC2WOL_LOC_ID_OFFSET + 301, SC2WOL_LOC_ID_OFFSET + 302, SC2WOL_LOC_ID_OFFSET + 303],
        "Evacuation": [SC2WOL_LOC_ID_OFFSET + 400, SC2WOL_LOC_ID_OFFSET + 401, SC2WOL_LOC_ID_OFFSET + 402, SC2WOL_LOC_ID_OFFSET + 403],
        "Outbreak": [SC2WOL_LOC_ID_OFFSET + 500, SC2WOL_LOC_ID_OFFSET + 501, SC2WOL_LOC_ID_OFFSET + 502],
        "Safe Haven": [SC2WOL_LOC_ID_OFFSET + 600, SC2WOL_LOC_ID_OFFSET + 601, SC2WOL_LOC_ID_OFFSET + 602, SC2WOL_LOC_ID_OFFSET + 603],
        "Haven's Fall": [SC2WOL_LOC_ID_OFFSET + 700, SC2WOL_LOC_ID_OFFSET + 701, SC2WOL_LOC_ID_OFFSET + 702, SC2WOL_LOC_ID_OFFSET + 703],
        "Smash and Grab": [SC2WOL_LOC_ID_OFFSET + 800, SC2WOL_LOC_ID_OFFSET + 801, SC2WOL_LOC_ID_OFFSET + 802, SC2WOL_LOC_ID_OFFSET + 803, SC2WOL_LOC_ID_OFFSET + 804],
        "The Dig": [SC2WOL_LOC_ID_OFFSET + 900, SC2WOL_LOC_ID_OFFSET + 901, SC2WOL_LOC_ID_OFFSET + 902, SC2WOL_LOC_ID_OFFSET + 903],
        "The Moebius Factor": [SC2WOL_LOC_ID_OFFSET + 1000, SC2WOL_LOC_ID_OFFSET + 1003, SC2WOL_LOC_ID_OFFSET + 1004, SC2WOL_LOC_ID_OFFSET + 1005, SC2WOL_LOC_ID_OFFSET + 1006, SC2WOL_LOC_ID_OFFSET + 1007, SC2WOL_LOC_ID_OFFSET + 1008],
        "Supernova": [SC2WOL_LOC_ID_OFFSET + 1100, SC2WOL_LOC_ID_OFFSET + 1101, SC2WOL_LOC_ID_OFFSET + 1102, SC2WOL_LOC_ID_OFFSET + 1103, SC2WOL_LOC_ID_OFFSET + 1104],
        "Maw of the Void": [SC2WOL_LOC_ID_OFFSET + 1200, SC2WOL_LOC_ID_OFFSET + 1201, SC2WOL_LOC_ID_OFFSET + 1202, SC2WOL_LOC_ID_OFFSET + 1203, SC2WOL_LOC_ID_OFFSET + 1204, SC2WOL_LOC_ID_OFFSET + 1205],
        "Devil's Playground": [SC2WOL_LOC_ID_OFFSET + 1300, SC2WOL_LOC_ID_OFFSET + 1301, SC2WOL_LOC_ID_OFFSET + 1302],
        "Welcome to the Jungle": [SC2WOL_LOC_ID_OFFSET + 1400, SC2WOL_LOC_ID_OFFSET + 1401, SC2WOL_LOC_ID_OFFSET + 1402, SC2WOL_LOC_ID_OFFSET + 1403],
        "Breakout": [SC2WOL_LOC_ID_OFFSET + 1500, SC2WOL_LOC_ID_OFFSET + 1501, SC2WOL_LOC_ID_OFFSET + 1502],
        "Ghost of a Chance": [SC2WOL_LOC_ID_OFFSET + 1600, SC2WOL_LOC_ID_OFFSET + 1601, SC2WOL_LOC_ID_OFFSET + 1602, SC2WOL_LOC_ID_OFFSET + 1603, SC2WOL_LOC_ID_OFFSET + 1604, SC2WOL_LOC_ID_OFFSET + 1605],
        "The Great Train Robbery": [SC2WOL_LOC_ID_OFFSET + 1700, SC2WOL_LOC_ID_OFFSET + 1701, SC2WOL_LOC_ID_OFFSET + 1702, SC2WOL_LOC_ID_OFFSET + 1703],
        "Cutthroat": [SC2WOL_LOC_ID_OFFSET + 1800, SC2WOL_LOC_ID_OFFSET + 1801, SC2WOL_LOC_ID_OFFSET + 1802, SC2WOL_LOC_ID_OFFSET + 1803, SC2WOL_LOC_ID_OFFSET + 1804],
        "Engine of Destruction": [SC2WOL_LOC_ID_OFFSET + 1900, SC2WOL_LOC_ID_OFFSET + 1901, SC2WOL_LOC_ID_OFFSET + 1902, SC2WOL_LOC_ID_OFFSET + 1903, SC2WOL_LOC_ID_OFFSET + 1904, SC2WOL_LOC_ID_OFFSET + 1905],
        "Media Blitz": [SC2WOL_LOC_ID_OFFSET + 2000, SC2WOL_LOC_ID_OFFSET + 2001, SC2WOL_LOC_ID_OFFSET + 2002, SC2WOL_LOC_ID_OFFSET + 2003, SC2WOL_LOC_ID_OFFSET + 2004],
        "Piercing the Shroud": [SC2WOL_LOC_ID_OFFSET + 2100, SC2WOL_LOC_ID_OFFSET + 2101, SC2WOL_LOC_ID_OFFSET + 2102, SC2WOL_LOC_ID_OFFSET + 2103, SC2WOL_LOC_ID_OFFSET + 2104, SC2WOL_LOC_ID_OFFSET + 2105],
        "Whispers of Doom": [SC2WOL_LOC_ID_OFFSET + 2200, SC2WOL_LOC_ID_OFFSET + 2201, SC2WOL_LOC_ID_OFFSET + 2202, SC2WOL_LOC_ID_OFFSET + 2203],
        "A Sinister Turn": [SC2WOL_LOC_ID_OFFSET + 2300, SC2WOL_LOC_ID_OFFSET + 2301, SC2WOL_LOC_ID_OFFSET + 2302, SC2WOL_LOC_ID_OFFSET + 2303],
        "Echoes of the Future": [SC2WOL_LOC_ID_OFFSET + 2400, SC2WOL_LOC_ID_OFFSET + 2401, SC2WOL_LOC_ID_OFFSET + 2402],
        "In Utter Darkness": [SC2WOL_LOC_ID_OFFSET + 2500, SC2WOL_LOC_ID_OFFSET + 2501, SC2WOL_LOC_ID_OFFSET + 2502],
        "Gates of Hell": [SC2WOL_LOC_ID_OFFSET + 2600, SC2WOL_LOC_ID_OFFSET + 2601],
        "Belly of the Beast": [SC2WOL_LOC_ID_OFFSET + 2700, SC2WOL_LOC_ID_OFFSET + 2701, SC2WOL_LOC_ID_OFFSET + 2702, SC2WOL_LOC_ID_OFFSET + 2703],
        "Shatter the Sky": [SC2WOL_LOC_ID_OFFSET + 2800, SC2WOL_LOC_ID_OFFSET + 2801, SC2WOL_LOC_ID_OFFSET + 2802, SC2WOL_LOC_ID_OFFSET + 2803, SC2WOL_LOC_ID_OFFSET + 2804, SC2WOL_LOC_ID_OFFSET + 2805],
    }

    display_data = {}

    # Determine display for progressive items
    progressive_items = {
        "Progressive Infantry Weapon": 100 + SC2WOL_ITEM_ID_OFFSET,
        "Progressive Infantry Armor": 102 + SC2WOL_ITEM_ID_OFFSET,
        "Progressive Vehicle Weapon": 103 + SC2WOL_ITEM_ID_OFFSET,
        "Progressive Vehicle Armor": 104 + SC2WOL_ITEM_ID_OFFSET,
        "Progressive Ship Weapon": 105 + SC2WOL_ITEM_ID_OFFSET,
        "Progressive Ship Armor": 106 + SC2WOL_ITEM_ID_OFFSET
    }
    progressive_names = {
        "Progressive Infantry Weapon": ["Infantry Weapons Level 1", "Infantry Weapons Level 1", "Infantry Weapons Level 2", "Infantry Weapons Level 3"],
        "Progressive Infantry Armor": ["Infantry Armor Level 1", "Infantry Armor Level 1", "Infantry Armor Level 2", "Infantry Armor Level 3"],
        "Progressive Vehicle Weapon": ["Vehicle Weapons Level 1", "Vehicle Weapons Level 1", "Vehicle Weapons Level 2", "Vehicle Weapons Level 3"],
        "Progressive Vehicle Armor": ["Vehicle Armor Level 1", "Vehicle Armor Level 1", "Vehicle Armor Level 2", "Vehicle Armor Level 3"],
        "Progressive Ship Weapon": ["Ship Weapons Level 1", "Ship Weapons Level 1", "Ship Weapons Level 2", "Ship Weapons Level 3"],
        "Progressive Ship Armor": ["Ship Armor Level 1", "Ship Armor Level 1", "Ship Armor Level 2", "Ship Armor Level 3"]
    }
    for item_name, item_id in progressive_items.items():
        level = min(inventory[item_id], len(progressive_names[item_name]) - 1)
        display_name = progressive_names[item_name][level]
        base_name = item_name.split(maxsplit=1)[1].lower().replace(' ', '_')
        display_data[base_name + "_level"] = level
        display_data[base_name + "_url"] = icons[display_name]

    # Multi-items
    multi_items = {
        "+15 Starting Minerals": 800 + SC2WOL_ITEM_ID_OFFSET,
        "+15 Starting Vespene": 801 + SC2WOL_ITEM_ID_OFFSET,
        "+2 Starting Supply": 802 + SC2WOL_ITEM_ID_OFFSET
    }
    for item_name, item_id in multi_items.items():
        base_name = item_name.split()[-1].lower()
        count = inventory[item_id]
        if base_name == "supply":
            count = count * 2
            display_data[base_name + "_count"] = count
        else:
            count = count * 15
            display_data[base_name + "_count"] = count

    # Victory condition
    game_state = multisave.get("client_game_state", {}).get((team, player), 0)
    display_data['game_finished'] = game_state == 30

    # Turn location IDs into mission objective counts
    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    lookup_name = lambda id: lookup_any_location_id_to_name[id]
    location_info = {mission_name: {lookup_name(id): (id in checked_locations) for id in mission_locations if id in set(locations[player])} for mission_name, mission_locations in sc2wol_location_ids.items()}
    checks_done = {mission_name: len([id for id in mission_locations if id in checked_locations and id in set(locations[player])]) for mission_name, mission_locations in sc2wol_location_ids.items()}
    checks_done['Total'] = len(checked_locations)
    checks_in_area = {mission_name: len([id for id in mission_locations if id in set(locations[player])]) for mission_name, mission_locations in sc2wol_location_ids.items()}
    checks_in_area['Total'] = sum(checks_in_area.values())

    return render_template("sc2wolTracker.html",
                            inventory=inventory, icons=icons,
                            acquired_items={lookup_any_item_id_to_name[id] for id in inventory if
                                            id in lookup_any_item_id_to_name},
                            player=player, team=team, room=room, player_name=playerName,
                            checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                            **display_data)


def __renderGenericTracker(multisave: Dict[str, Any], room: Room, locations: Dict[int, Dict[int, Tuple[int, int, int]]],
                           inventory: Counter, team: int, player: int, playerName: str,
                           seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int],
                           saving_second: int) -> str:

    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    player_received_items = {}
    if multisave.get('version', 0) > 0:
        ordered_items = multisave.get('received_items', {}).get((team, player, True), [])
    else:
        ordered_items = multisave.get('received_items', {}).get((team, player), [])

    # add numbering to all items but starter_inventory
    for order_index, networkItem in enumerate(ordered_items, start=1):
        player_received_items[networkItem.item] = order_index

    return render_template("genericTracker.html",
                           inventory=inventory,
                           player=player, team=team, room=room, player_name=playerName,
                           checked_locations=checked_locations,
                           not_checked_locations=set(locations[player]) - checked_locations,
                           received_items=player_received_items,
                           saving_second=saving_second)


@app.route('/tracker/<suuid:tracker>')
@cache.memoize(timeout=1)  # multisave is currently created at most every minute
def getTracker(tracker: UUID):
    room: Room = Room.get(tracker=tracker)
    if not room:
        abort(404)
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, \
        precollected_items, games, slot_data, groups, saving_second = get_static_room_data(room)

    inventory = {teamnumber: {playernumber: collections.Counter() for playernumber in range(1, len(team) + 1) if playernumber not in groups}
                 for teamnumber, team in enumerate(names)}

    checks_done = {teamnumber: {playernumber: {loc_name: 0 for loc_name in default_locations}
                                for playernumber in range(1, len(team) + 1) if playernumber not in groups}
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
        if player in groups:
            continue
        player_locations = locations[player]
        if precollected_items:
            precollected = precollected_items[player]
            for item_id in precollected:
                attribute_item(inventory, team, player, item_id)
        for location in locations_checked:
            if location not in player_locations or location not in player_location_to_area[player]:
                continue

            item, recipient, flags = player_locations[location]

            if recipient in names:
                attribute_item(inventory, team, recipient, item)
            checks_done[team][player][player_location_to_area[player][location]] += 1
            checks_done[team][player]["Total"] += 1

    for (team, player), game_state in multisave.get("client_game_state", {}).items():
        if player in groups:
            continue
        if game_state == 30:
            inventory[team][player][106] = 1  # Triforce

    player_big_key_locations = {playernumber: set() for playernumber in range(1, len(names[0]) + 1)}
    player_small_key_locations = {playernumber: set() for playernumber in range(1, len(names[0]) + 1)}
    for loc_data in locations.values():
        for values in loc_data.values():
            item_id, item_player, flags = values

            if item_id in ids_big_key:
                player_big_key_locations[item_player].add(ids_big_key[item_id])
            elif item_id in ids_small_key:
                player_small_key_locations[item_player].add(ids_small_key[item_id])
    group_big_key_locations = set()
    group_key_locations = set()
    for player in [player for player in range(1, len(names[0]) + 1) if player not in groups]:
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

    return render_template("tracker.html", inventory=inventory, get_item_name_from_id=lookup_any_item_id_to_name,
                           lookup_id_to_name=Items.lookup_id_to_name, player_names=player_names,
                           tracking_names=tracking_names, tracking_ids=tracking_ids, room=room, icons=alttp_icons,
                           multi_items=multi_items, checks_done=checks_done, ordered_areas=ordered_areas,
                           checks_in_area=seed_checks_in_area, activity_timers=activity_timers,
                           key_locations=group_key_locations, small_key_ids=small_key_ids, big_key_ids=big_key_ids,
                           video=video, big_key_locations=group_big_key_locations,
                           hints=hints, long_player_names=long_player_names)


game_specific_trackers: typing.Dict[str, typing.Callable] = {
    "Minecraft": __renderMinecraftTracker,
    "Ocarina of Time": __renderOoTTracker,
    "Timespinner": __renderTimespinnerTracker,
    "A Link to the Past": __renderAlttpTracker,
    "Super Metroid": __renderSuperMetroidTracker,
    "Starcraft 2 Wings of Liberty": __renderSC2WoLTracker
}
