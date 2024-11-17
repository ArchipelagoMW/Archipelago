import pkgutil
from typing import Dict, List, Literal, Optional, Set, TypedDict, Union
from typing_extensions import NotRequired, TypeAlias

from BaseClasses import ItemClassification
from Utils import parse_yaml

GAME_NAME = "Autopelago"
BASE_ID = 300000


class AutopelagoItemDefinitionCls(TypedDict):
    name: str
    rat_count: NotRequired[int]
    flavor_text: NotRequired[str]


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
    reward_is_fixed: Optional[bool]
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
    items: AutopelagoItemDefinitions
    regions: AutopelagoRegionDefinitions


class AutopelagoRegionDefinition:
    key: str
    exits: List[str]
    locations: List[str]
    requires: AutopelagoAllRequirement

    def __init__(self, key: str, exits: List[str], locations: List[str], requires: AutopelagoGameRequirement):
        self.key = key
        self.exits = exits
        self.locations = locations
        self.requires = requires


_defs: AutopelagoDefinitions = parse_yaml(pkgutil.get_data(__name__, 'AutopelagoDefinitions.yml'))

def _gen_ids():
    next_id = BASE_ID
    while True:
        yield next_id
        next_id += 1


item_name_to_id: Dict[str, int] = {}
generic_nonprogression_item_table: Dict[AutopelagoNonProgressionItemType, List[str]] = {'useful_nonprogression': [],
                                                                                        'trap': [], 'filler': []}
item_name_to_classification: Dict[str, Optional[ItemClassification]] = {}
item_name_to_rat_count: Dict[str, int] = {}
game_specific_nonprogression_items: Dict[str, Dict[AutopelagoNonProgressionItemType, List[str]]] = {}
item_key_to_name: Dict[str, str] = {}
_item_id_gen = _gen_ids()

for k, v in ((k, v) for k, v in _defs['items'].items() if
             k not in {'rats', 'useful_nonprogression', 'trap', 'filler'}):
    _name = _name_of(v)
    item_name_to_id[_name] = next(_item_id_gen)
    item_name_to_classification[_name] = ItemClassification.progression
    rat_count = _rat_count_of(v)
    if rat_count and rat_count > 0:
        item_name_to_rat_count[_name] = rat_count
    item_key_to_name[k] = _name

for k, v in _defs['items']['rats'].items():
    _name = _name_of(v)
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
            continue

        if isinstance(i, list):
            generic_nonprogression_item_table[k].append(i[0])
            item_name_to_id[i[0]] = next(_item_id_gen)
            item_name_to_classification[i[0]] = item_classification
            continue

        if 'game_specific' not in i:
            _name = _name_of(i)
            generic_nonprogression_item_table[k].append(_name)
            item_name_to_id[_name] = next(_item_id_gen)
            item_name_to_classification[_name] = item_classification
            item_name_to_rat_count[_name] = _rat_count_of(i) or 0
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
                    continue

                if isinstance(it, list):
                    game_specific_nonprogression_items[g][k].append(it[0])
                    item_name_to_id[it[0]] = next(_item_id_gen)
                    item_name_to_classification[it[0]] = item_classification


_append_nonprogression('useful_nonprogression')
_append_nonprogression('trap')
_append_nonprogression('filler')

autopelago_regions: Dict[str, AutopelagoRegionDefinition] = {}
location_name_to_progression_item_name: Dict[str, str] = {}
location_name_to_nonprogression_item: Dict[str, Literal['useful_nonprogression', 'filler']] = {}
location_name_to_requirement: Dict[str, AutopelagoGameRequirement] = {}
location_name_to_id: Dict[str, int] = {}
location_names_with_fixed_rewards: Set[str] = set()
_location_id_gen = _gen_ids()

for k, r in _defs['regions']['landmarks'].items():
    if k == 'moon_comma_the':
        # "Moon, The" is only a "region" on the client.
        continue
    _name = r['name']
    location_name_to_id[_name] = next(_location_id_gen)
    location_name_to_progression_item_name[_name] = item_key_to_name[r['unrandomized_item']]
    location_name_to_requirement[_name] = r['requires']
    exits: List[str] = r['exits'] if 'exits' in r else []
    autopelago_regions[k] = AutopelagoRegionDefinition(k, exits, [_name], r['requires'])
    if 'reward_is_fixed' in r and r['reward_is_fixed']:
        location_names_with_fixed_rewards.add(_name)
for rk, r in _defs['regions']['fillers'].items():
    _locations: List[str] = []
    _cur = 1
    region_items = r['unrandomized_items']
    for k in region_items['key'] if 'key' in region_items else []:
        if isinstance(k, str):
            _name = r['name_template'].replace('{n}', f'{_cur}')
            location_name_to_id[_name] = next(_location_id_gen)
            location_name_to_progression_item_name[_name] = item_key_to_name[k]
            _locations.append(_name)
            _cur += 1
        else:
            for i in range(k['count']):
                _name = r['name_template'].replace('{n}', f'{_cur}')
                location_name_to_id[_name] = next(_location_id_gen)
                location_name_to_progression_item_name[_name] = item_key_to_name[k['item']]
                _locations.append(_name)
                _cur += 1
    for i in range(region_items['useful_nonprogression']) if 'useful_nonprogression' in region_items else []:
        _name = r['name_template'].replace('{n}', f'{_cur}')
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_nonprogression_item[_name] = 'useful_nonprogression'
        _locations.append(_name)
        _cur += 1
    for i in range(region_items['filler']) if 'filler' in region_items else []:
        _name = r['name_template'].replace('{n}', f'{_cur}')
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_nonprogression_item[_name] = 'filler'
        _locations.append(_name)
        _cur += 1
    autopelago_regions[rk] = AutopelagoRegionDefinition(rk, r['exits'], _locations, {'all': []})


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
