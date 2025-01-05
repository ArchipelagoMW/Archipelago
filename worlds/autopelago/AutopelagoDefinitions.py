import pkgutil
from collections import deque
from typing import Dict, List, Literal, Optional, Set, TypedDict, Union, Deque, Tuple
from typing_extensions import NotRequired, TypeAlias

from BaseClasses import ItemClassification
from Utils import parse_yaml

GAME_NAME = "Autopelago"
BASE_ID = 300000

class AutopelagoItemDefinitionCls(TypedDict):
    name: str
    rat_count: NotRequired[int]
    flavor_text: NotRequired[str]
    auras_granted: NotRequired[List[str]]


AutopelagoItemDefinition = Union[str, List[Union[str, List[str]]], AutopelagoItemDefinitionCls]
AutopelagoItemDefinitionsSimple = Dict[str, AutopelagoItemDefinition]
AutopelagoGameSpecificItemGroup = Dict[Literal['game_specific'], Dict[str, List[AutopelagoItemDefinition]]]
AutopelagoNonProgressionGroupItems = List[Union[AutopelagoItemDefinition, AutopelagoGameSpecificItemGroup]]
AutopelagoNonProgressionItemType = Literal['useful_nonprogression', 'trap', 'filler']


def _name_of(item: AutopelagoItemDefinition):
    return \
        item if isinstance(item, str) else \
        item[0] if isinstance(item, list) else \
        item['name']


def _rat_count_of(item: AutopelagoItemDefinition):
    return item['rat_count'] if isinstance(item, dict) and 'rat_count' in item else None


def _auras_of(item: AutopelagoItemDefinition) -> List[str]:
    return \
        [] if isinstance(item, str) else \
        item[1] if isinstance(item, list) else \
        item['auras_granted'] if 'auras_granted' in item else \
        []

def autopelago_item_classification_of(item: AutopelagoNonProgressionItemType):
    if item == 'useful_nonprogression':
        return ItemClassification.useful
    elif item == 'trap':
        return ItemClassification.trap
    elif item == 'filler':
        return ItemClassification.filler
    else:
        return None


class AutopelagoItemDefinitions(TypedDict):
    rats: AutopelagoItemDefinitionsSimple
    useful_nonprogression: AutopelagoNonProgressionGroupItems
    trap: AutopelagoNonProgressionGroupItems
    filler: AutopelagoNonProgressionGroupItems
    # any_other_str_key_not_listed: AutopelagoItemDefinition


AutopelagoGameRequirement: TypeAlias = Union[
    'AutopelagoAllRequirement', 'AutopelagoAnyRequirement', 'AutopelagoItemRequirement',
    'AutopelagoRatCountRequirement', 'AutopelagoAnyTwoRequirement']


class AutopelagoAllRequirement(TypedDict):
    all: List[AutopelagoGameRequirement]


class AutopelagoAnyRequirement(TypedDict):
    any: List[AutopelagoGameRequirement]


class AutopelagoAnyTwoRequirement(TypedDict):
    any_two: List[AutopelagoGameRequirement]


class AutopelagoItemRequirement(TypedDict):
    item: str


class AutopelagoRatCountRequirement(TypedDict):
    rat_count: int


class AutopelagoLandmarkRegionDefinition(TypedDict):
    name: str
    unrandomized_item: str
    requires: AutopelagoGameRequirement
    exits: Optional[List[str]]


class AutopelagoFillerItemDefinitionCls(TypedDict):
    item: str
    count: int


AutopelagoFillerItemDefinition = Union[str, AutopelagoFillerItemDefinitionCls]


class AutopelagoFillerRegionItemsDefinition(TypedDict):
    key: List[AutopelagoFillerItemDefinition]
    useful_nonprogression: int
    filler: int


class AutopelagoFillerRegionDefinition(TypedDict):
    name_template: str
    unrandomized_items: AutopelagoFillerRegionItemsDefinition
    ability_check_dc: int
    exits: List[str]


class AutopelagoRegionDefinitions(TypedDict):
    landmarks: Dict[str, AutopelagoLandmarkRegionDefinition]
    fillers: Dict[str, AutopelagoFillerRegionDefinition]


class AutopelagoDefinitions(TypedDict):
    version_stamp: str
    items: AutopelagoItemDefinitions
    regions: AutopelagoRegionDefinitions


class AutopelagoRegionDefinition:
    key: str
    exits: List[str]
    locations: List[str]
    requires: AutopelagoAllRequirement
    landmark: bool

    def __init__(self, key: str, exits: List[str], locations: List[str], requires: AutopelagoGameRequirement,
                 landmark: bool):
        self.key = key
        self.exits = exits
        self.locations = locations
        self.requires = requires
        self.landmark = landmark


_defs: AutopelagoDefinitions = parse_yaml(pkgutil.get_data(__name__, 'AutopelagoDefinitions.yml'))

version_stamp = _defs['version_stamp']

def _gen_ids():
    next_id = BASE_ID
    while True:
        yield next_id
        next_id += 1


item_name_to_auras: Dict[str, List[str]] = {}
generic_nonprogression_item_table: Dict[AutopelagoNonProgressionItemType, List[str]] = {'useful_nonprogression': [],
                                                                                        'trap': [], 'filler': []}
item_name_to_classification: Dict[str, Optional[ItemClassification]] = {}
item_name_to_rat_count: Dict[str, int] = {}
game_specific_nonprogression_items: Dict[str, Dict[AutopelagoNonProgressionItemType, List[str]]] = {}
item_key_to_name: Dict[str, str] = {}
_item_id_gen = _gen_ids()
item_name_to_id: Dict[str, int] = {}

for k, v in ((k, v) for k, v in _defs['items'].items() if
             k not in {'rats', 'useful_nonprogression', 'trap', 'filler'}):
    _name = _name_of(v)
    item_name_to_auras[_name] = _auras_of(v)
    item_name_to_id[_name] = next(_item_id_gen)
    item_name_to_classification[_name] = ItemClassification.progression
    rat_count = _rat_count_of(v)
    if rat_count and rat_count > 0:
        item_name_to_rat_count[_name] = rat_count
    item_key_to_name[k] = _name

for k, v in _defs['items']['rats'].items():
    _name = _name_of(v)
    item_name_to_auras[_name] = _auras_of(v)
    item_name_to_id[_name] = next(_item_id_gen)
    item_name_to_classification[_name] = ItemClassification.progression
    item_name_to_rat_count[_name] = _rat_count_of(v) or 1
    item_key_to_name[k] = _name


def _append_nonprogression(k: AutopelagoNonProgressionItemType):
    item_classification = autopelago_item_classification_of(k)
    for i in _defs['items'][k]:
        if isinstance(i, str):
            generic_nonprogression_item_table[k].append(i)
            item_name_to_id[i] = next(_item_id_gen)
            item_name_to_classification[i] = item_classification
            item_name_to_auras[i] = _auras_of(i)
            continue

        if isinstance(i, list):
            generic_nonprogression_item_table[k].append(i[0])
            item_name_to_id[i[0]] = next(_item_id_gen)
            item_name_to_classification[i[0]] = item_classification
            item_name_to_auras[i[0]] = _auras_of(i)
            continue

        if 'game_specific' not in i:
            _name = _name_of(i)
            generic_nonprogression_item_table[k].append(_name)
            item_name_to_id[_name] = next(_item_id_gen)
            item_name_to_classification[_name] = item_classification
            item_name_to_rat_count[_name] = _rat_count_of(i) or 0
            item_name_to_auras[_name] = _auras_of(i)
            continue

        for g, v in i['game_specific'].items():
            if g not in game_specific_nonprogression_items:
                game_specific_nonprogression_items[g] = {}
            game_specific_nonprogression_items[g][k] = []
            for it in v:
                if isinstance(it, str):
                    game_specific_nonprogression_items[g][k].append(it)
                    item_name_to_id[it] = next(_item_id_gen)
                    item_name_to_classification[it] = item_classification
                    item_name_to_auras[it] = _auras_of(i)
                    continue

                if isinstance(it, list):
                    game_specific_nonprogression_items[g][k].append(it[0])
                    item_name_to_id[it[0]] = next(_item_id_gen)
                    item_name_to_classification[it[0]] = item_classification
                    item_name_to_auras[it[0]] = _auras_of(it)


_append_nonprogression('useful_nonprogression')
_append_nonprogression('trap')
_append_nonprogression('filler')

autopelago_regions: Dict[str, AutopelagoRegionDefinition] = {}
location_name_to_progression_item_name: Dict[str, str] = {}
location_name_to_nonprogression_item: Dict[str, Literal['useful_nonprogression', 'filler']] = {}
location_name_to_requirement: Dict[str, AutopelagoGameRequirement] = {}
location_name_to_id: Dict[str, int] = {}
_location_id_gen = _gen_ids()

for k, curr_region in _defs['regions']['landmarks'].items():
    _name = curr_region['name']
    location_name_to_id[_name] = next(_location_id_gen)
    location_name_to_progression_item_name[_name] = item_key_to_name[curr_region['unrandomized_item']]
    location_name_to_requirement[_name] = curr_region['requires']
    exits: List[str] = curr_region['exits'] if 'exits' in curr_region else []
    autopelago_regions[k] = AutopelagoRegionDefinition(k, exits, [_name], curr_region['requires'], True)
for rk, curr_region in _defs['regions']['fillers'].items():
    _locations: List[str] = []
    _cur = 1
    region_items = curr_region['unrandomized_items']
    for k in region_items['key'] if 'key' in region_items else []:
        if isinstance(k, str):
            _name = curr_region['name_template'].replace('{n}', f'{_cur}')
            location_name_to_id[_name] = next(_location_id_gen)
            location_name_to_progression_item_name[_name] = item_key_to_name[k]
            _locations.append(_name)
            _cur += 1
        else:
            for i in range(k['count']):
                _name = curr_region['name_template'].replace('{n}', f'{_cur}')
                location_name_to_id[_name] = next(_location_id_gen)
                location_name_to_progression_item_name[_name] = item_key_to_name[k['item']]
                _locations.append(_name)
                _cur += 1
    for i in range(region_items['useful_nonprogression']) if 'useful_nonprogression' in region_items else []:
        _name = curr_region['name_template'].replace('{n}', f'{_cur}')
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_nonprogression_item[_name] = 'useful_nonprogression'
        _locations.append(_name)
        _cur += 1
    for i in range(region_items['filler']) if 'filler' in region_items else []:
        _name = curr_region['name_template'].replace('{n}', f'{_cur}')
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_nonprogression_item[_name] = 'filler'
        _locations.append(_name)
        _cur += 1
    autopelago_regions[rk] = AutopelagoRegionDefinition(rk, curr_region['exits'], _locations, {'all': []}, False)


def _get_required_rat_count(req: AutopelagoGameRequirement):
    if 'all' in req:
        return max(_get_required_rat_count(sub_req) for sub_req in req['all']) if req['all'] else 0
    elif 'any' in req:
        return min(_get_required_rat_count(sub_req) for sub_req in req['any'])
    elif 'rat_count' in req:
        return req['rat_count']
    else:
        return 0


max_required_rat_count = max(_get_required_rat_count(req) for req in
                             [location_name_to_requirement.values()] + [r.requires for r in
                                                                        autopelago_regions.values()])
total_available_rat_count = sum(
    item_name_to_rat_count[i] for i in location_name_to_progression_item_name.values() if
    i in item_name_to_rat_count)

item_name_groups: Dict[str, Set[str]] = {
    'Sewer Progression': set(),
    'Cool World Progression': set(),
    'Space Progression': set(),
    'Rats': {k for k, v in item_name_to_rat_count.items() if v},
    'Special Rats': {k for k, v in item_name_to_rat_count.items() if v and k != item_key_to_name['pack_rat']},

    'Progression Items': set(),
    'Buffs': set(),
    'Fillers': set(),
    'Traps': set(),
}

location_name_groups: Dict[str, Set[str]] = {
    'Landmarks': set(),
    'Fillers': set(),
    'Zone Bosses': set(),
    'Sewer Landmarks': set(),
    'Sewer Fillers': set(),
    'Cool World Landmarks': set(),
    'Cool World Fillers': set(),
    'Space Landmarks': set(),
    'Space Fillers': set(),
    'Optional Bosses': set(),
    'Optional Fillers': set(),
}

for item_name, classification in item_name_to_classification.items():
    if classification == ItemClassification.filler:
        item_name_groups['Fillers'].add(item_name)
    elif classification == ItemClassification.useful:
        item_name_groups['Buffs'].add(item_name)
    elif classification == ItemClassification.trap:
        item_name_groups['Traps'].add(item_name)
    elif classification == ItemClassification.progression:
        item_name_groups['Progression Items'].add(item_name)

    auras = item_name_to_auras[item_name]
    for aura in auras:
        nice_name = aura.replace('_', ' ').title()

        item_group_all = f'Gives {nice_name}'
        item_group_only = f'Gives Only {nice_name}'
        if item_group_all not in item_name_groups:
            item_name_groups[item_group_all] = set()
            item_name_groups[item_group_only] = set()

        item_name_groups[item_group_all].add(item_name)
        if len(set(auras)) == 1:
            item_name_groups[item_group_only].add(item_name)


def _visit_for_items(group_name: str, req: AutopelagoGameRequirement):
    if 'item' in req:
        req: AutopelagoItemRequirement
        item_name_groups[group_name].add(item_key_to_name[req['item']])
    elif 'all' in req:
        req: AutopelagoAllRequirement
        for sub_req in req['all']:
            _visit_for_items(group_name, sub_req)
    elif 'any' in req:
        req: AutopelagoAnyRequirement
        for sub_req in req['any']:
            _visit_for_items(group_name, sub_req)
    elif 'any_two' in req:
        req: AutopelagoAnyTwoRequirement
        for sub_req in req['any_two']:
            _visit_for_items(group_name, sub_req)


q: Deque[Tuple[str, Optional[AutopelagoRegionDefinition], AutopelagoRegionDefinition]] = deque()
q.append(('Sewer', None, autopelago_regions['Menu']))
while q:
    prev_region_from_q: AutopelagoRegionDefinition
    curr_region_from_q: AutopelagoRegionDefinition
    zone, prev_region_from_q, curr_region_from_q = q.popleft()
    _visit_for_items(f'{zone} Progression', curr_region_from_q.requires)
    region_type = 'Landmarks' if curr_region_from_q.landmark else 'Fillers'
    if curr_region_from_q.key == 'captured_goldfish':
        region_type = 'Zone Bosses'
        next_zone = 'Cool World'
    elif curr_region_from_q.key == 'secret_cache':
        region_type = 'Zone Bosses'
        next_zone = 'Space'
    elif curr_region_from_q.key == 'snakes_on_a_planet':
        # nothing else needed beyond here
        continue
    else:
        next_zone = zone

    next_regions = [autopelago_regions[e] for e in curr_region_from_q.exits]
    for loc in curr_region_from_q.locations:
        location_name_groups[region_type].add(loc)
        if region_type != 'Zone Bosses':
            location_name_groups[f'{zone} {region_type}'].add(loc)

        if not next_regions:
            location_name_groups['Optional Bosses'].add(loc)
            for prev_loc in prev_region_from_q.locations:
                location_name_groups['Optional Fillers'].add(prev_loc)

    if next_zone:
        for next_region in next_regions:
            q.append((next_zone, curr_region_from_q, next_region))
