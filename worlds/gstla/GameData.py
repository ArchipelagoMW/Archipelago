import json
import os
from collections import defaultdict
from enum import Enum, IntFlag, auto, IntEnum
from typing import NamedTuple, List, Dict, Set

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))

num_words = {
    1: 'One',
    2: 'Two',
    3: 'Three',
    4: 'Four',
    5: 'Five',
    6: 'Six',
    7: 'Seven',
    8: 'Eight',
    9: 'Nine',
    10: 'Ten'
}

mimic_names = [
    "Milquetoast Mimic",
    "Clumsy Mimic",
    "Mimic",
    "Journeyman Mimic",
    "Advanced Mimic",
    "Sacred Mimic",
    "Royal Mimic",
    "Imperial Mimic",
    "Divine Mimic"
]


class LocationDatum(NamedTuple):
    rando_flag: int
    flag: int
    mapId: int
    locked: bool
    is_summon: bool
    is_key_item: bool
    is_major_item: bool
    is_hidden: bool
    addr: List[int]
    event_type: int
    location_id: int
    id: int
    vanilla_contents: int
    vanilla_name: str
    map_name: str
    restrictions: int

class EnemyDatum(NamedTuple):
    name: str
    id: int
    ap_id: int
    flag: int

class EventDatum(NamedTuple):
    event_id: int
    flag: int
    location_name: str
    item_name: str

class ItemType(int, Enum):
    Consumable = 0 # is this the right name?
    Weapon = 1
    Armor = 2
    Shield = 3
    Helm = 4
    Boots = 5
    PsyenergyItem = 6
    Trident = 7
    Ring = 8
    Shirt = 9
    Class = 10
    KeyItem = 11
    Psyenergy = 12
    Djinn = 13
    Event = 14
    Character = 15
    Mimic = 16
    Summon = 17

class ItemFlags(IntFlag):
    NONE = 0
    Cursed = auto()# 1 "Curses on pickup"
    Sticky = auto()# 2 "Unremovable"
    Rare = auto()# 4 "If dropped, can be bought back from shops"
    Important = auto()# 8 "Cannot be dropped"
    Stackable = auto()# 16 "Carry up to 30"
    NoTransfer = auto()# 32 "Cannot be transfered from GS1 to GS2"
    UnusedOne = auto()
    UnusedTwo = auto()

class ItemDatum(NamedTuple):
    # TODO: add more?
    id: int
    name: str
    addr: int
    item_type: ItemType
    flags: ItemFlags
    use_effect: int = 0
    # TODO: event type is a property of locations, not of items
    # event_type: int
    is_mimic: bool = False

class ElementType(IntEnum):
    Earth = 0
    Water = 1
    Fire = 2
    Air = 3

class DjinnDatum(NamedTuple):
    ap_id: int
    id: int
    element: ElementType
    name: str
    addr: int
    stats_addr: int
    stats: List[int]
    vanilla_flag: int
    item_type: ItemType = ItemType.Djinn

class SummonDatum(NamedTuple):
    # ap_id: int
    id: int
    name: str
    addr: int
    item_type: ItemType = ItemType.Summon

class PsyDatum(NamedTuple):
    id: int
    name: str
    addr: int
    item_type: ItemType = ItemType.Psyenergy

class CharacterDatum(NamedTuple):
    id: int
    name: str
    flag: int
    addr: int
    item_type: ItemType = ItemType.Character

class LocationName(NamedTuple):
    id: int
    flag: int
    py_name: str
    str_name: str

    @classmethod
    def from_loc_data(cls, loc: LocationDatum, value: str = None, suffix: str = ''):
        key = loc.map_name
        val = loc.vanilla_name + suffix
        py_name = key.replace(' ', '_').replace("'", '')
        str_name = val.replace(' ', '_').replace("'", '').replace('???', 'Empty')
        if value is None:
            return LocationName(loc.id, loc.flag, py_name + '_' + str_name, py_name + ' - ' + str_name)
        else:
            return LocationName(loc.id, loc.flag, py_name + '_' + str_name, value)

class ItemName(NamedTuple):
    id: int
    py_name: str
    str_name: str

    @classmethod
    def from_item_data(cls, item: ItemDatum, suffix = ''):
        ret = ItemName(item.id,
                        ItemName.setup_py_name(item.name, suffix),
                        ItemName.setup_str_name(item.name,suffix))
        return ret

    @classmethod
    def from_enemy_data(cls, enemy: EnemyDatum, event: bool = True):
        ret = ItemName(enemy.ap_id,
                       ItemName.setup_py_name(enemy.name, '_'+str(enemy.id) + (" Event" if event else "")),
                       ItemName.setup_str_name(enemy.name, ' '+str(enemy.id) + (" Event" if event else "")))
        return ret

    @staticmethod
    def setup_py_name(name: str, suffix=''):
        return (name + suffix).replace(' ', '_').replace("'", '').replace('???', 'Empty')

    @staticmethod
    def setup_str_name(name: str, suffix = ''):
        return (name + suffix).replace('???', 'Empty')


SPECIAL_NAMES = {
    419: ItemName(419, 'Rusty_Sword_CorsairsEdge',"Rusty Sword - Corsair's Edge"),
    417: ItemName(417, 'Rusty_Sword_RobbersBlade',"Rusty Sword - Robber's Blade"),
    420: ItemName(420, 'Rusty_Sword_PiratesSabre',"Rusty Sword - Pirate's Sabre"),
    418: ItemName(418, 'Rusty_Sword_SoulBrand',"Rusty Sword - Soul Brand"),
    421: ItemName(421, 'Rusty_Axe_CaptainsAxe',"Rusty Axe - Captain's Axe"),
    422: ItemName(422, 'Rusty_Axe_VikingAxe',"Rusty Axe - Viking Axe"),
    424: ItemName(424, 'Rusty_Mace_HagboneMace',"Rusty Mace - Hagbone Mace"),
    423: ItemName(423, 'Rusty_Mace_DemonMace',"Rusty Mace - Demon Mace"),
    425: ItemName(425, 'Rusty_Staff_Dracomace',"Rusty Staff - Dracomace"),
    426: ItemName(426, 'Rusty_Staff_GlowerStaff',"Rusty Staff - Glower Staff"),
    427: ItemName(427, 'Rusty_Staff_GoblinsRod',"Rusty Staff - Goblin's Rod"),
    123: ItemName(123, 'Dragon_Shield_GS', "Dragon Shield GS"),
    132: ItemName(132, 'Spirit_Gloves_GS', 'Spirit Gloves GS'),
    222: ItemName(222, 'Mars_Star', 'Mars Star'),
    223: ItemName(223, 'Mythril_Bag_Jupiter', 'Mythril Bag (Jupiter)'),
    224: ItemName(224, 'Mythril_Bag_Empty', 'Mythril Bag (Empty)'),
    245: ItemName(245, 'Mythril_Bag_Mars_Jupiter', 'Mythril Bag (Mars & Jupiter)'),
}

class GameData:
    def __init__(self):
        self.raw_location_data: List[LocationDatum] = []
        self.raw_item_data: List[ItemDatum] = []
        self.raw_djinn_data: List[DjinnDatum] = []
        self.raw_summon_data: List[SummonDatum] = []
        self.raw_psy_data: List[PsyDatum] = []
        self.raw_character_data: List[CharacterDatum] = []
        self.raw_enemy_data: List[EnemyDatum] = []
        self.location_names: Dict[int, LocationName] = dict()
        self.item_names: Dict[int, ItemName] = dict()
        self.events: Dict[int, EventDatum] = dict()
        self.vanilla_item_ids: Set[int] = set()
        self.vanilla_shop_contents: Set[int] = set()
        self.forgeable_ids: Set[int] = set()
        self.lucky_medal_ids: Set[int] = {
            # 23, # Assassin Blade
            # 37, # Burning Axe
            # 48, # Grevious Mace
            # 81, # Spirit Armor
            # 97, # Kimono
            # 108, # Cocktail Dress
            # 124, # Earth Shield
            # 133, # Battle Gloves
            # 142, # Guardian Armlet
            # 152, # Adept's Helm
            # 160, # Ninja Hood
            # 171, # Glittering Tiara
            183, # Potion
            186, # Psy Crystal
            189, # Water of Life
            280, # Hestia Blade
            302, # Mighty Axe
            320, # Fireman's Pole
            327, # Leda's Bracelet
            335, # Erebus Armor
            341, # Wild Coat
            342, # Floral Dress
            359, # Aegis Shield
            364, # Crafted Gloves
            380, # Minerva Helm
            387, # Crown of Glory
            395, # Brilliant Circlet
        }
        self.lucky_wheels_ids: Set[int] = {
            181, # Nut
            182, # Vial
            183, # Potion
            188, # Elixer
            186, # Psy Crystal
            189, # Water of Life
            258, # Fur Boots
            257, # Quick Boots
            256, # Hyper Boots
            252, # Running Shirt
            251, # Silk Shirt
            250, # Mythril Shirt
            264, #Sleep Ring
            263, # War Ring
            262, # Adept Ring
        }
        self._load_locations()
        self._load_items()
        self._load_shop_data()
        self._load_djinn()
        self._load_summons()
        self._load_forgeables()
        self._setup_events()
        self._setup_location_names()
        self._setup_item_names()
        self._setup_psy_energies()
        self._setup_characters()

    def _load_locations(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'item_locations.json'), 'r') as loc_file:
            location_data = json.load(loc_file)
        # A few locations use different flags than stated in the item_locations.json file
        # E.g. character starting inventories
        flag_overwrites = {
            16384202: 0x4, # Shaman's Rod -> Felix
            16384204: 0x6, # Mind Read -> Sheba
            16384206: 0x6, # Whirlwind -> Sheba
            16384208: 0x4, # Growth -> Felix
            16384210: 0x3, # Carry Stone -> Mia
            16384212: 0x2, # Lifting Gem -> Ivan
            16384214: 0x1, # Orb of Force -> Garet
            16384216: 0x0, # Catch Beads -> Isaac
            16384218: 0x7, # Douse Drop -> Piers
            16384220: 0x7,  # Frost Jewel -> Piers

        }
        restriction_map = {'no-empty': 1, 'no-mimic': 2, 'no-summon': 4, 'no-money': 8}
        restriction_dict: defaultdict[int, int] = defaultdict(lambda: 0)
        for loc_logic_file in os.listdir(os.path.join(SCRIPT_DIR, 'data', 'location_logic')):
            assert loc_logic_file.endswith('.json')
            with open(os.path.join(SCRIPT_DIR, 'data', 'location_logic', loc_logic_file), 'r') as data_file:
                data = json.load(data_file)

            treasure_data = data['Treasure']
            for datum in treasure_data:
                if 'Restriction' not in datum:
                    continue
                restrictions = datum['Restriction']
                addr = int(datum['Addr'], 16)
                assert addr not in restriction_dict
                for restriction in restrictions:
                    restriction_dict[addr] += restriction_map[restriction]

        for flag, locs in location_data.items():
            # The extra locations are variations on the same map.  We mostly don't care for the client,
            # but the rom generator currently does care, since it will need to place the same item on all
            # variations of the map
            loc = locs[0]
            addr = [x['addr'] for x in locs]
            rando_flag = int(flag, 16)
            mapped_flag = flag_overwrites.get(addr[0], rando_flag)
            restriction_data = restriction_dict[loc['id']]
            if 0x80 != loc['eventType'] and 0x84 != loc['eventType']:
                restriction_data |= restriction_map['no-empty'] + restriction_map['no-mimic']
            if addr[0] > 0xFA0000:
                restriction_data |= restriction_map['no-money']
            if loc['id'] < 0x10 or (loc['id'] | 0xF00) == 0x100:
                restriction_data |= restriction_map['no-empty'] + restriction_map['no-mimic'] + restriction_map['no-money']
            datum = LocationDatum(rando_flag, mapped_flag, loc['mapId'], loc['locked'], loc['isSummon'], loc['isKeyItem'],
                              loc['isMajorItem'], loc['isHidden'], addr, loc['eventType'],
                              loc['locationId'], loc['id'], loc['vanillaContents'], loc['vanillaName'],
                              loc['mapName'], restriction_data)
            self.raw_location_data.append(datum)
            if datum.vanilla_name == 'Mimic':
                self.raw_item_data.append(
                    # Agreed upon rando id of 0xA00 + mimic id
                    ItemDatum(0xA01 + datum.vanilla_contents, mimic_names[datum.vanilla_contents], datum.addr[0], ItemType.Mimic, ItemFlags.NONE, 0, True)
                )
            else:
                self.vanilla_item_ids.add(datum.vanilla_contents)

    def _load_shop_data(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'shops.json'), 'r') as shop_file:
            shop_data = json.load(shop_file)

        for shop in shop_data:
            for id in shop['items']:
                if id != 0:
                    self.vanilla_shop_contents.add(id)
            for artifact in shop['artifacts']:
                if artifact != 0:
                    self.vanilla_shop_contents.add(artifact)

    def _load_forgeables(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'forgeables.json'), 'r') as forge_file:
            forge_data = json.load(forge_file)

        for forge in forge_data.values():
            for result in forge['results']:
                if result != 0:
                    self.forgeable_ids.add(result)

    def _load_items(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'items.json'), 'r') as item_file:
            item_data = json.load(item_file)
        for item in item_data.values():
            item_type = ItemType(item['itemType'])
            self.raw_item_data.append(
                ItemDatum(item['id'] if item_type != ItemType.PsyenergyItem else item['useEffect'] + 0xE00,
                          item['name'],
                          item['addr'],
                          item_type,
                          ItemFlags(item['flags']),
                          item['useEffect'])
            )
        coins = dict()
        for loc in self.raw_location_data:
            if loc.vanilla_contents > 0x8000:
                # TODO: get the name in a better way?
                coins[loc.vanilla_contents] = ItemDatum(loc.vanilla_contents, f"Coins {loc.vanilla_contents-0x8000}", loc.addr[0], ItemType.Consumable, ItemFlags(0))
        for coin in coins.values():
            self.raw_item_data.append(coin)


    def _load_djinn(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'djinn.json'), 'r') as djinn_file:
            djinn_data = json.load(djinn_file)
        for djinn in djinn_data:
            # Largest vanilla item id is 460
            self.raw_djinn_data.append(
                DjinnDatum(
                    djinn['addr'],
                    djinn['vanillaId'],
                    ElementType(djinn['vanillaElement']),
                    djinn['vanillaName'],
                    djinn['addr'],
                    # From emo tracker pack
                    djinn['statAddr'],
                    djinn['stats'],
                    # 0x30 is the start of the djinn flags; the game has flag slots for 20 djinn
                    # per element, even though there's only 18 per element, so some flags are just unused
                    0x30 + (djinn['vanillaElement'] * 20) + djinn['vanillaId'],
                )
            )
        for djinn in self.raw_djinn_data:
            self.item_names[djinn.ap_id] = (ItemName(djinn.ap_id, djinn.name, djinn.name))

    def _load_summons(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'summons.json'), 'r') as summon_file:
            summon_data = json.load(summon_file)
            for summon in summon_data:
                self.raw_summon_data.append(
                    SummonDatum(summon['id'] + 0xF00, summon['name'], summon['addr'])
                )

    def _load_enemies(self):
        # Function is unused, but leaving here in case we actually want to use it for some reason
        enemy_offset = 6000
        with open(os.path.join(SCRIPT_DIR, 'data', 'enemies.json'), 'r') as enemy_file:
            enemy_data = json.load(enemy_file)
            for name, list in enemy_data.items():
                if name == "???":
                    continue
                for enemy in list:
                    self.raw_enemy_data.append(
                        # Enemy kill flags start at 0x600; the flag is off by 7 sorta; -1 for the json
                        # starting at 1 instead of 0, and + 8 for player characters
                        EnemyDatum(enemy['name'], enemy['id'] - 1, enemy['id']+enemy_offset, enemy['id'] - 1 + 8 + 0x600)
                    )

        for enemy in self.raw_enemy_data:
            name = ItemName.from_enemy_data(enemy)
            self.item_names[enemy.ap_id] = name
            self.location_names[enemy.ap_id] = LocationName(enemy.ap_id, enemy.flag, name.py_name, name.str_name)

    def _recurse_tracker_data(self,
                              tracker_name_data: Dict[int, str],
                              tracker_names: Dict[str, int],
                              node: Dict[str, any]) -> None:
        if 'sections' not in node:
            if 'children' in node:
                for child in node['children']:
                    self._recurse_tracker_data(tracker_name_data, tracker_names, child)
            return
        sections = node['sections']
        area_name = node['name']
        for i in range(len(sections)):
            section = sections[i]
            flags = node['children'][i]['name']
            for flag_str in flags.split(","):
                flag = int(flag_str, 16)
                if flag in tracker_name_data:
                    continue
                tracker_name = f"{area_name} - {section['name']}"
                # count = names[tracker_name] + 1
                tracker_names[tracker_name] += 1
                count = tracker_names[tracker_name]
                suffix = ''
                if count > 1:
                    suffix = ' ' + num_words[count]
                tracker_name_data[flag] = tracker_name + suffix

    def _setup_location_names(self):
        names: defaultdict[str, int] = defaultdict(lambda: 0)
        tracker_name_data: Dict[int, str] = dict()
        tracker_names: defaultdict[str, int] = defaultdict(lambda: 0)
        with open(os.path.join(SCRIPT_DIR, 'data', 'locations.json')) as infile:
            tracker_data = json.load(infile)[0]
        self._recurse_tracker_data(tracker_name_data, tracker_names, tracker_data)
        for loc in self.raw_location_data:
            tracker_name = tracker_name_data.get(loc.rando_flag, None)
            # tracker_name = None
            if tracker_name is not None:
                loc_name = LocationName.from_loc_data(loc, tracker_name)
            else:
                loc_name = LocationName.from_loc_data(loc)
            count = names[loc_name.py_name] + 1
            names[loc_name.py_name] = count
            if count > 1:
                if tracker_name is not None:
                    loc_name = LocationName.from_loc_data(loc, tracker_name, ' ' + num_words[count])
                else:
                    loc_name = LocationName.from_loc_data(loc, None, ' ' + num_words[count])
                # loc_name = LocationName.from_loc_data(loc, None, ' ' + num_words[count])
            assert loc_name.id not in self.location_names, "Id: %s, Name: %s" % (hex(loc_name.id), loc_name.str_name)
            self.location_names[loc_name.id] = loc_name

    def _setup_item_names(self):
        for item in self.raw_item_data:
            item_id = item.id
            if item_id in SPECIAL_NAMES:
                item_name = SPECIAL_NAMES[item_id]
            else:
                item_name = ItemName.from_item_data(item)
            assert item_name.id not in self.item_names, (item_name.id, item_name.str_name)
            self.item_names[item_name.id] = item_name

    def _setup_psy_energies(self):
        self.raw_psy_data += [
            PsyDatum(3596, 'Growth', 3596),
            PsyDatum(3662, 'Whirlwind', 3662),
            PsyDatum(3722, 'Parch', 3722),
            PsyDatum(3723, 'Sand', 3723),
            PsyDatum(3725, 'Mind Read', 3725),
            PsyDatum(3728, 'Reveal', 3728),
            PsyDatum(3738, 'Blaze', 3738),
        ]
        for d in self.raw_psy_data:
            self.item_names[d.id] = ItemName(d.id, d.name.replace(' ', '_'), d.name)

    def _setup_characters(self):
        self.raw_character_data += [
            CharacterDatum(3328, "Isaac", 3328, 16384384),
            CharacterDatum(3329, "Garet", 3329, 16384386),
            CharacterDatum(3330, "Ivan", 3330, 16384388),
            CharacterDatum(3331, "Mia", 3331, 16384390),
            # Felix is 3332, but we don't do nutin with him
            CharacterDatum(3333, "Jenna", 3333, 16384392),
            CharacterDatum(3334, "Sheba", 3334, 16384394),
            CharacterDatum(3335, "Piers", 3335, 16384396),
        ]
        for c in self.raw_character_data:
            self.item_names[c.id] = ItemName(c.id, c.name, c.name)

    def _setup_events(self):
        # Just some offset to avoid colliding with anything else; needs to avoid any location or item ids in AP
        event_offset = 5000
        events = [
            EventDatum(event_offset + 1, 0x778, "Mars Lighthouse - Doom Dragon", "Doom Dragon Defeated" ),
            EventDatum(event_offset + 2, 0x8AB, "Alhafra Briggs", "Briggs defeated" ),
            EventDatum(event_offset + 3, 0x97F, "Alhafra Prison Briggs", "Briggs escaped" ),
            EventDatum(event_offset + 4, 0x8FF, "Gabomba Statue Ritual", "Gabomba Statue Completed" ),
            EventDatum(event_offset + 5, 0x9EE, "Gaia Rock - Serpent", "Serpent defeated" ),
            EventDatum(event_offset + 6, 0x665, "Sea of Time - Poseidon", "Poseidon defeated"),
            EventDatum(event_offset + 7, 0x93F, "Lemurian Ship - Aqua Hydra", "Aqua Hydra defeated"),
            EventDatum(event_offset + 8, 0x94D, "Shaman Village - Moapa", "Moapa defeated" ),
            EventDatum(event_offset + 9, 0xA21, "Jupiter_Lighthouse Aeri - Agatio and Karst", "Jupiter Beacon Lit"),
            EventDatum(event_offset + 10, 0xA4B, "Mars Lighthouse - Flame Dragons", "Flame Dragons - defeated"),
            EventDatum(event_offset + 11, 0x8DE, "Lemurian Ship - Engine Room", "Ship"),
            EventDatum(event_offset + 12, 0x8DF, "Contigo - Wings of Anemos", "Wings of Anemos"),
            EventDatum(event_offset + 13, 0x64a, "Kandorean Temple - Chestbeaters", "Chestbeaters defeated"),
            EventDatum(event_offset + 14, 0x64d, "Yampi Desert - King Scorpion", "King Scorpion defeated"),
            EventDatum(event_offset + 15, 0x662, "Champa - Avimander", "Avimander defeated"),
            EventDatum(event_offset + 16, 0x6a4, "Treasure Isle - Star Magician", "Star Magician defeated"),
            EventDatum(event_offset + 17, 0x6dd, "Islet Cave - Sentinel", "Sentinel defeated"),
            EventDatum(event_offset + 18, 0x6d1, "Yampi Desert Cave - Valukar", "Valukar defeated"),
            EventDatum(event_offset + 19, 0x6da, "Anemos Inner Sanctum - Dullahan", "Dullahan defeated"),
            # Flag here is really the Jupiter Lighthouse flag.  Base rando with PC shuffle seems to do something weird
            # with the reunion flag
            EventDatum(event_offset + 20, 0xA21, "Contigo - Reunion", "Reunion"),
            EventDatum(event_offset + 21, 0x1, "Victory Event", "Victory"),
            EventDatum(event_offset + 22, 0xA5F, "Loho - Ship Cannon", "Ship Cannon"),
            EventDatum(event_offset + 23, 0xA30, "Mars Lighthouse - Heated", "Mars Lighthouse Heated"),
            # EventDatum(event_offset + 15,, "Jupiter Lighthouse - Karst", "Karst defeated"),
            # EventDatum(event_offset + 15,, "Jupiter Lighthouse - Agatio", "Agatio defeated"),
        ]
        self.events = {e.event_id: e for e in events}
        for event in self.events.values():
            self.location_names[event.event_id] = LocationName(event.event_id, event.flag, event.location_name.replace(' ', '_').replace('-', '').replace('__', '_'), event.location_name)
        for event in self.events.values():
            self.item_names[event.event_id] = ItemName(event.event_id, event.item_name.replace('-', '').replace(' ', '_').replace('__', '_'), event.item_name)
