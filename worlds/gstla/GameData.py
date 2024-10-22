import json
import os
from collections import defaultdict
from enum import Enum, IntFlag, auto, IntEnum
from typing import NamedTuple, List, Dict

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


class LocationDatum(NamedTuple):
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

    def is_gear(self):
        return self == 1 or self == 2 or self == 3 or self == 4 or self == 5 or \
                self == 8 or self == 9

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
    item_type: ItemType = ItemType.Psyenergy

class PsyDatum(NamedTuple):
    id: int
    name: str
    addr: int
    item_type: ItemType = ItemType.Psyenergy

class LocationName(NamedTuple):
    id: int
    flag: int
    py_name: str
    str_name: str

    @classmethod
    def from_loc_data(cls, loc: LocationDatum, suffix: str = ''):
        key = loc.map_name
        val = loc.vanilla_name + suffix
        py_name = key.replace(' ', '_').replace("'", '')
        str_name = val.replace(' ', '_').replace("'", '').replace('???', 'Empty')
        return LocationName(loc.id, loc.flag, py_name + '_' + str_name, py_name + ' - ' + str_name)

class ItemName(NamedTuple):
    id: int
    py_name: str
    str_name: str

    @classmethod
    def from_item_data(cls, item: ItemDatum, suffix = ''):
        key = item.name + suffix
        val = item.name + suffix
        ret = ItemName(item.id,
                        key.replace(' ', '_').replace("'", '').replace('???', 'Empty'),
                        val.replace('???', 'Empty'))
        return ret

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
    222: ItemName(222, 'Mythril_Bag_Mars', 'Mythril Bag (Mars)'),
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
        self.location_names: Dict[int, LocationName] = dict()
        self.item_names: Dict[int, ItemName] = dict()
        self.events: Dict[int, EventDatum] = dict()
        self._load_locations()
        self._load_items()
        self._load_djinn()
        self._load_summons()
        self._setup_events()
        self._setup_location_names()
        self._setup_item_names()
        self._setup_psy_energies()

    def _load_locations(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'item_locations.json'), 'r') as loc_file:
            location_data = json.load(loc_file)
        for flag, locs in location_data.items():
            # The extra locations are variations on the same map.  We mostly don't care for the client,
            # but the rom generator currently does care, since it will need to place the same item on all
            # variations of the map
            loc = locs[0]
            addr = [x['addr'] for x in locs]
            self.raw_location_data.append(
                LocationDatum(int(flag, 16), loc['mapId'], loc['locked'], loc['isSummon'], loc['isKeyItem'],
                              loc['isMajorItem'], loc['isHidden'], addr, loc['eventType'],
                              loc['locationId'], loc['id'], loc['vanillaContents'], loc['vanillaName'], loc['mapName'])
            )

    def _load_items(self):
        with open(os.path.join(SCRIPT_DIR, 'data', 'items.json'), 'r') as item_file:
            item_data = json.load(item_file)
        for item in item_data.values():
            self.raw_item_data.append(
                ItemDatum(item['id'],
                          item['name'],
                          item['addr'],
                          ItemType(item['itemType']),
                          ItemFlags(item['flags']),
                          item['useEffect'])
            )

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

    def _setup_location_names(self):
        names: defaultdict[str, int] = defaultdict(lambda: 0)
        for loc in self.raw_location_data:
            loc_name = LocationName.from_loc_data(loc)
            count = names[loc_name.py_name] + 1
            names[loc_name.py_name] = count
            if count > 1:
                loc_name = LocationName.from_loc_data(loc, ' ' + num_words[count])
            assert loc_name.id not in self.location_names, "Id: %s, Name: %s" % (hex(loc_name.flag), loc_name.str_name)
            self.location_names[loc_name.id] = loc_name

    def _setup_item_names(self):
        for item in self.raw_item_data:
            if item.id in SPECIAL_NAMES:
                item_name = SPECIAL_NAMES[item.id]
            else:
                item_name = ItemName.from_item_data(item)
            assert item_name.id not in self.item_names
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

    def _setup_events(self):
        # Just some offset to avoid colliding with anything else; needs to avoid any location or item ids in AP
        event_offset = 5000
        events = [
            EventDatum(event_offset + 1, 0x778, "Mars Lighthouse - Doom Dragon Fight", "Victory" ),
            EventDatum(event_offset + 2, 0x8AB, "Alhafra Briggs", "Briggs defeated" ),
            EventDatum(event_offset + 3, 0x97F, "Alhafra Prison Briggs", "Briggs escaped" ),
            EventDatum(event_offset + 4, 0x8FF, "Gabomba Statue", "Gabomba Statue Completed" ),
            EventDatum(event_offset + 5, 0x9EE, "Gaia Rock - Serpent Fight", "Serpent defeated" ),
            # TODO: the emo tracker doesn't track this, so not sure what this is supposed to be?
            # TODO: is the flag 0x8DD?
            EventDatum(event_offset + 6, 0x8DD, "Sea of Time - Poseidon fight", "Poseidon defeated"),
            EventDatum(event_offset + 7, 0x93F, "Lemurian Ship - Aqua Hydra fight", "Aqua Hydra defeated"),
            EventDatum(event_offset + 8, 0x94D, "Shaman Village - Moapa fight", "Moapa defeated" ),
            EventDatum(event_offset + 9, 0xA21, "Jupiter_Lighthouse Aeri - Agatio and Karst fight", "Jupiter Beacon Lit"),
            EventDatum(event_offset + 10, 0xA4B, "Mars Lighthouse - Flame Dragons fight", "Flame Dragons - defeated"),
            EventDatum(event_offset + 11, 0x8DE, "Lemurian Ship - Engine Room", "Ship")
        ]
        self.events = {e.event_id: e for e in events}
        for event in self.events.values():
            self.location_names[event.event_id] = LocationName(event.event_id, event.flag, event.location_name.replace(' ', '_').replace('-', '').replace('__', '_'), event.location_name)
        for event in self.events.values():
            self.item_names[event.event_id] = ItemName(event.event_id, event.item_name.replace('-', '').replace(' ', '_').replace('__', '_'), event.item_name)
