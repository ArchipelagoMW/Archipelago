import collections
import typing
from typing import Counter, Optional, Dict, Any, Tuple, Set, List, TYPE_CHECKING

from flask import render_template
from werkzeug.exceptions import abort
import datetime
from uuid import UUID

from worlds.alttp import Items
from WebHostLib import app, cache, Room
from Utils import restricted_loads
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name
from worlds.AutoWorld import AutoWorldRegister
from MultiServer import get_item_name_from_id, Context
from NetUtils import SlotType


class PlayerTracker:
    """This class will create a basic 'prettier' tracker for each world using their themes automatically. This
            can be overridden to customize how it will appear. Can provide icons and custom regions. The html used is also
            a jinja template that can be overridden if you want your tracker to look different in certain aspects. To render
            icons and regions add dictionaries to the relevant attributes of the tracker_info. To customize the layout of
            your icons you can create a new html in your world and extend playerTracker.html and overwrite the icons_render
            block then change the tracker_info template attribute to your template."""

    template: str = 'playerTracker.html'
    icons: Dict[str, str] = {}
    progressive_items: List[str] = []
    progressive_names: Dict[str, List[str]] = {}
    regions: Dict[str, List[str]] = {}
    checks_done: Dict[str, Set[str]] = {}
    room: Any
    team: int
    player: int
    name: str
    all_locations: Set[str]
    checked_locations: Set[str]
    all_prog_items: Counter[str]
    items_received: Counter[str]
    received_prog_items: Counter[str]
    slot_data: Dict[any, any]
    theme: str

    region_keys: Dict[str, str] = {}

    def __init__(self, room: Any, team: int, player: int, name: str, all_locations: Set[str],
                 checked_locations: set, all_progression_items: Counter[str], items_received: Counter[str],
                 slot_data: Dict[any, any]):
        self.room = room
        self.team = team
        self.player = player
        self.name = name
        self.all_locations = all_locations
        self.checked_locations = checked_locations
        self.all_prog_items = all_progression_items
        self.items_received = items_received
        self.slot_data = slot_data


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

    result = locations, names, use_door_tracker, player_checks_in_area, player_location_to_area, \
             multidata["precollected_items"], multidata["games"], multidata["slot_data"], groups
    _multidata_cache[room.seed.id] = result
    return result


@app.route('/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
@cache.memoize(timeout=60)  # multisave is currently created at most every minute
def get_player_tracker(tracker: UUID, tracked_team: int, tracked_player: int, want_generic: bool = False):
    # Team and player must be positive and greater than zero
    if tracked_team < 0 or tracked_player < 1:
        abort(404)

    room: Optional[Room] = Room.get(tracker=tracker)
    if not room:
        abort(404)

    player_tracker, multisave, inventory, seed_checks_in_area, lttp_checks_done, \
    slot_data, games, player_name, display_icons = fill_tracker_data(room, tracked_team, tracked_player)

    game_name = games[tracked_player]
    # TODO move all games in game_specific_trackers to new system
    if game_name in game_specific_trackers and not want_generic:
        specific_tracker = game_specific_trackers.get(game_name, None)
        return specific_tracker(multisave, room, player_tracker.all_locations, inventory, tracked_team, tracked_player, player_name,
                                seed_checks_in_area, lttp_checks_done, slot_data[tracked_player])
    elif game_name in AutoWorldRegister.world_types and not want_generic:
        return render_template(
            "trackers/" + player_tracker.template,
            all_progression_items=player_tracker.all_prog_items,
            player=player_tracker.player,
            team=player_tracker.team,
            room=player_tracker.room,
            player_name=player_tracker.name,
            checked_locations=sorted(player_tracker.checked_locations),
            locations=sorted(player_tracker.all_locations),
            theme=player_tracker.theme,
            icons=display_icons,
            regions=player_tracker.regions,
            checks_done=player_tracker.checks_done,
            region_keys=player_tracker.region_keys
        )
    else:
        return __renderGenericTracker(multisave, room, player_tracker.all_locations, inventory, tracked_team, tracked_player, player_name, seed_checks_in_area, lttp_checks_done)


@app.route('/generic_tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
@cache.memoize(timeout=60)
def get_generic_tracker(tracker: UUID, tracked_team: int, tracked_player: int):
    return get_player_tracker(tracker, tracked_team, tracked_player, True)


def get_tracker_icons_and_regions(player_tracker: PlayerTracker) -> Dict[str, str]:
    """this function allows multiple icons to be used for the same item but it does require the world to submit both
    a progressive_items list and the icons dict together"""
    display_icons: Dict[str, str] = {}
    if player_tracker.progressive_names and player_tracker.icons:
        for item in player_tracker.progressive_items:
            if item in player_tracker.progressive_names:
                level = min(player_tracker.items_received[item], len(player_tracker.progressive_names[item]) - 1)
                display_name = player_tracker.progressive_names[item][level]
                if display_name in player_tracker.icons:
                    display_icons[item] = player_tracker.icons[display_name]
                else:
                    display_icons[item] = player_tracker.icons[item]
            else:
                display_icons[item] = player_tracker.icons[item]
    else:
        if player_tracker.progressive_items and player_tracker.icons:
            for item in player_tracker.progressive_items:
                display_icons[item] = player_tracker.icons[item]

    if player_tracker.regions:
        for region in player_tracker.regions:
            for location in region:
                if location in player_tracker.checked_locations:
                    player_tracker.checks_done.setdefault(region, set()).add(location)

    return display_icons


def fill_tracker_data(room: Room, team: int, player: int) -> Tuple:
    """Collect seed information and pare it down to a single player"""
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, \
        precollected_items, games, slot_data, groups = get_static_room_data(room)
    player_name = names[team][player - 1]
    location_to_area = player_location_to_area[player]
    inventory = collections.Counter()
    lttp_checks_done = {loc_name: 0 for loc_name in default_locations}

    # Add starting items to inventory
    starting_items = precollected_items[player]
    if starting_items:
        for item_id in starting_items:
            attribute_item_solo(inventory, item_id)

    if room.multisave:
        multisave: Dict[str, Any] = restricted_loads(room.multisave)
    else:
        multisave: Dict[str, Any] = {}

    slots_aimed_at_player = {player}
    for group_id, group_members in groups.items():
        if player in group_members:
            slots_aimed_at_player.add(group_id)

    checked_locations = set()
    # Add items to player inventory
    for (ms_team, ms_player), locations_checked in multisave.get("location_checks", {}).items():
        # Skip teams and players not matching the request
        player_locations = locations[ms_player]
        if ms_team == team:
            # If the player does not have the item, do nothing
            for location in locations_checked:
                if location in player_locations:
                    item, recipient, flags = player_locations[location]
                    if recipient in slots_aimed_at_player:  # a check done for the tracked player
                        attribute_item_solo(inventory, item)
                    if ms_player == player:  # a check done by the tracked player
                        lttp_checks_done[location_to_area[location]] += 1
                        lttp_checks_done["Total"] += 1
                        checked_locations.add(lookup_any_location_id_to_name[location])

    prog_items = collections.Counter
    all_location_names = set()

    all_location_names = {lookup_any_location_id_to_name[id] for id in locations[player]}
    prog_items = collections.Counter()
    for player in locations:
        for location in locations[player]:
            item, recipient, flags = locations[player][location]
            if recipient == player:
                if flags & 1:
                    item_name = lookup_any_item_id_to_name[item]
                    prog_items[item_name] += 1

    items_received = collections.Counter()
    for id in inventory:
        items_received[lookup_any_item_id_to_name[id]] = inventory[id]

    player_tracker = PlayerTracker(
        room,
        team,
        player,
        player_name,
        all_location_names,
        checked_locations,
        prog_items,
        items_received,
        slot_data[player]
    )

    # grab webworld and apply its theme to the tracker
    webworld = AutoWorldRegister.world_types[games[player]].web
    player_tracker.theme = webworld.theme
    # allow the world to add information to the tracker class
    webworld.modify_tracker(player_tracker)
    display_icons = get_tracker_icons_and_regions(player_tracker)

    return player_tracker, multisave, inventory, seed_checks_in_area, lttp_checks_done, slot_data, games, player_name, display_icons


def __renderTimespinnerTracker(multisave: Dict[str, Any], room: Room, locations: set,
                               inventory: Counter, team: int, player: int, playerName: str,
                               seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict[str, Any]) -> str:

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

    return render_template("trackers/" + "timespinnerTracker.html",
                            inventory=inventory, icons=icons, acquired_items=acquired_items,
                            player=player, team=team, room=room, player_name=playerName,
                            checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                            options=options, **display_data)

def __renderSuperMetroidTracker(multisave: Dict[str, Any], room: Room, locations: set,
                                inventory: Counter, team: int, player: int, playerName: str,
                                seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int], slot_data: Dict) -> str:

    icons = {
        "Energy Tank":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/ETank.png",
        "Missile":          "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Missile.png",
        "Super Missile":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Super.png",
        "Power Bomb":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/PowerBomb.png",
        "Bomb":             "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Bomb.png",
        "Charge Beam":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Charge.png",
        "Ice Beam":         "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Ice.png",
        "Hi-Jump Boots":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/HiJump.png",
        "Speed Booster":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/SpeedBooster.png",
        "Wave Beam":        "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Wave.png",
        "Spazer":           "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Spazer.png",
        "Spring Ball":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/SpringBall.png",
        "Varia Suit":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Varia.png",
        "Plasma Beam":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Plasma.png",
        "Grappling Beam":   "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Grapple.png",
        "Morph Ball":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Morph.png",
        "Reserve Tank":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Reserve.png",
        "Gravity Suit":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/Gravity.png",
        "X-Ray Scope":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/XRayScope.png",
        "Space Jump":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/SpaceJump.png",
        "Screw Attack":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/ScrewAttack.png",
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
        count = inventory[item_id]
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

    return render_template("trackers/" + "supermetroidTracker.html",
                            inventory=inventory, icons=icons,
                            acquired_items={lookup_any_item_id_to_name[id] for id in inventory if
                                            id in lookup_any_item_id_to_name},
                            player=player, team=team, room=room, player_name=playerName,
                            checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
                            **display_data)


def __renderGenericTracker(multisave: Dict[str, Any], room: Room, locations: set,
                           inventory: Counter, team: int, player: int, playerName: str,
                           seed_checks_in_area: Dict[int, Dict[str, int]], checks_done: Dict[str, int]) -> str:

    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    player_received_items = {}
    if multisave.get('version', 0) > 0:
        # add numbering to all items but starter_inventory
        ordered_items = multisave.get('received_items', {}).get((team, player, True), [])
    else:
        ordered_items = multisave.get('received_items', {}).get((team, player), [])

    for order_index, networkItem in enumerate(ordered_items, start=1):
        player_received_items[networkItem.item] = order_index

    return render_template("trackers/" + "genericTracker.html",
                            inventory=inventory,
                            player=player, team=team, room=room, player_name=playerName,
                            checked_locations=checked_locations,
                            not_checked_locations=locations - checked_locations,
                            received_items=player_received_items)


@app.route('/tracker/<suuid:tracker>')
@cache.memoize(timeout=60)  # multisave is currently created at most every minute
def getTracker(tracker: UUID):
    room: Room = Room.get(tracker=tracker)
    if not room:
        abort(404)
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, \
        precollected_items, games, slot_data, groups = get_static_room_data(room)

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

    player_big_key_locations = {playernumber: set() for playernumber in range(1, len(names[0]) + 1) if playernumber not in groups}
    player_small_key_locations = {playernumber: set() for playernumber in range(1, len(names[0]) + 1) if playernumber not in groups}
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

    return render_template("trackers/" + "multiworldTracker.html", inventory=inventory, get_item_name_from_id=get_item_name_from_id,
                           lookup_id_to_name=Items.lookup_id_to_name, player_names=player_names,
                           tracking_names=tracking_names, tracking_ids=tracking_ids, room=room, icons=alttp_icons,
                           multi_items=multi_items, checks_done=checks_done, ordered_areas=ordered_areas,
                           checks_in_area=seed_checks_in_area, activity_timers=activity_timers,
                           key_locations=group_key_locations, small_key_ids=small_key_ids, big_key_ids=big_key_ids,
                           video=video, big_key_locations=group_big_key_locations,
                           hints=hints, long_player_names=long_player_names)


game_specific_trackers: typing.Dict[str, typing.Callable] = {
    "Timespinner": __renderTimespinnerTracker,
    "Super Metroid": __renderSuperMetroidTracker
}