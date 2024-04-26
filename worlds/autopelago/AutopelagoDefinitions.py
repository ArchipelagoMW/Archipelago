from pathlib import PurePath
from typing import Literal, NotRequired, Optional, TypeAlias, TypedDict

from BaseClasses import ItemClassification
from Utils import parse_yaml

GAME_NAME = "Autopelago"
BASE_ID = 300000


class AutopelagoItemDefinitionCls(TypedDict):
    name: str
    rat_count: NotRequired[int]
    flavor_text: NotRequired[str]


AutopelagoItemDefinition = str | list[str, list[str]] | AutopelagoItemDefinitionCls
AutopelagoItemDefinitionsSimple = dict[str, AutopelagoItemDefinition]
AutopelagoGameSpecificItemGroup = dict[Literal['game_specific'], dict[str, list[AutopelagoItemDefinition]]]
AutopelagoNonProgressionGroupItems = list[AutopelagoItemDefinition | AutopelagoGameSpecificItemGroup]
AutopelagoNonProgressionItemType = Literal['useful_nonprogression', 'trap', 'filler', 'uncategorized']


def _name_of(item: AutopelagoItemDefinition):
    return \
        item if isinstance(item, str) else \
        item[0] if isinstance(item, list) else \
        item['name']


def _rat_count_of(item: AutopelagoItemDefinition):
    return item['rat_count'] if isinstance(item, dict) and 'rat_count' in item else None


def autopelago_item_classification_of(item: AutopelagoNonProgressionItemType):
    match item:
        case 'useful_nonprogression':
            return ItemClassification.useful
        case 'trap':
            return ItemClassification.trap
        case 'filler':
            return ItemClassification.filler
        case _:
            return None


class AutopelagoItemDefinitions(TypedDict):
    rats: AutopelagoItemDefinitionsSimple
    useful_nonprogression: AutopelagoNonProgressionGroupItems
    trap: AutopelagoNonProgressionGroupItems
    filler: AutopelagoNonProgressionGroupItems
    uncategorized: AutopelagoNonProgressionGroupItems
    # any_other_str_key_not_listed: AutopelagoItemDefinition


AutopelagoGameRequirement: TypeAlias = ('AutopelagoAllRequirement | AutopelagoAnyRequirement | '
                                        'AutopelagoItemRequirement | AutopelagoRatCountRequirement | '
                                        'AutopelagoAnyTwoRequirement')


class AutopelagoAllRequirement(TypedDict):
    all: list[AutopelagoGameRequirement]


class AutopelagoAnyRequirement(TypedDict):
    any: list[AutopelagoGameRequirement]


class AutopelagoAnyTwoRequirement(TypedDict):
    any_two: list[AutopelagoGameRequirement]


class AutopelagoItemRequirement(TypedDict):
    item: str


class AutopelagoRatCountRequirement(TypedDict):
    rat_count: int


class AutopelagoLandmarkRegionDefinition(TypedDict):
    name: str
    unrandomized_item: str
    reward_is_fixed: Optional[bool]
    requires: list[AutopelagoGameRequirement]
    exits: list[str]


class AutopelagoFillerItemDefinitionCls(TypedDict):
    item: str
    count: int


AutopelagoFillerItemDefinition = str | AutopelagoFillerItemDefinitionCls


class AutopelagoFillerRegionItemsDefinition(TypedDict):
    key: list[AutopelagoFillerItemDefinition]
    useful_nonprogression: int
    filler: int


class AutopelagoFillerRegionDefinition(TypedDict):
    name_template: str
    unrandomized_items: AutopelagoFillerRegionItemsDefinition
    ability_check_dc: int
    exits: list[str]


class AutopelagoRegionDefinitions(TypedDict):
    landmarks: dict[str, AutopelagoLandmarkRegionDefinition]
    fillers: dict[str, AutopelagoFillerRegionDefinition]


class AutopelagoDefinitions(TypedDict):
    items: AutopelagoItemDefinitions
    regions: AutopelagoRegionDefinitions


class AutopelagoRegionDefinition:
    key: str
    exits: list[str]
    locations: list[str]
    requires: AutopelagoAllRequirement

    def __init__(self, key: str, exits: list[str], locations: list[str], requires: list[AutopelagoGameRequirement]):
        self.key = key
        self.exits = exits
        self.locations = locations
        self.requires = {'all': requires}


with open(PurePath(__file__).with_name('AutopelagoDefinitions.yml'), 'r') as f:
    _defs: AutopelagoDefinitions = parse_yaml(f.read())


def _gen_ids():
    next_id = BASE_ID
    while True:
        yield next_id
        next_id += 1


item_name_to_id: dict[str, int] = {}
generic_nonprogression_item_table: dict[AutopelagoNonProgressionItemType, list[str]] = {'useful_nonprogression': [],
                                                                                        'trap': [], 'filler': [],
                                                                                        'uncategorized': []}
item_name_to_defined_classification: dict[str, Optional[ItemClassification]] = {}
item_name_to_rat_count: dict[str, int] = {}
game_specific_nonprogression_items: dict[str, dict[AutopelagoNonProgressionItemType, list[str]]] = {}
item_key_to_name: dict[str, str] = {}
_item_id_gen = _gen_ids()

for k, v in ((k, v) for k, v in _defs['items'].items() if
             k not in {'rats', 'useful_nonprogression', 'trap', 'filler', 'uncategorized'}):
    _name = _name_of(v)
    item_name_to_id[_name] = next(_item_id_gen)
    item_name_to_defined_classification[_name] = ItemClassification.progression
    rat_count = _rat_count_of(v)
    if rat_count and rat_count > 0:
        item_name_to_rat_count[_name] = rat_count
    item_key_to_name[k] = _name

for k, v in _defs['items']['rats'].items():
    _name = _name_of(v)
    item_name_to_id[_name] = next(_item_id_gen)
    item_name_to_defined_classification[_name] = ItemClassification.progression
    item_name_to_rat_count[_name] = _rat_count_of(v) or 1
    item_key_to_name[k] = _name


def _append_nonprogression(k: AutopelagoNonProgressionItemType):
    item_classification = autopelago_item_classification_of(k)
    for i in _defs['items'][k]:
        if isinstance(i, str):
            generic_nonprogression_item_table[k].append(i)
            item_name_to_id[i] = next(_item_id_gen)
            item_name_to_defined_classification[i] = item_classification
            continue

        if isinstance(i, list):
            generic_nonprogression_item_table[k].append(i[0])
            item_name_to_id[i[0]] = next(_item_id_gen)
            item_name_to_defined_classification[i[0]] = item_classification
            continue

        if 'game_specific' not in i:
            _name = _name_of(i)
            generic_nonprogression_item_table[k].append(_name)
            item_name_to_id[_name] = next(_item_id_gen)
            item_name_to_defined_classification[_name] = item_classification
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
                    item_name_to_defined_classification[it] = item_classification
                    continue

                if isinstance(it, list):
                    game_specific_nonprogression_items[g][k].append(it[0])
                    item_name_to_id[it[0]] = next(_item_id_gen)
                    item_name_to_defined_classification[it[0]] = item_classification


_append_nonprogression('useful_nonprogression')
_append_nonprogression('trap')
_append_nonprogression('filler')
_append_nonprogression('uncategorized')

autopelago_regions: dict[str, AutopelagoRegionDefinition] = {
    'Victory': AutopelagoRegionDefinition('Victory', [], ['Victory'], [])}
location_name_to_unrandomized_progression_item_name: dict[str, str] = {}
location_name_to_unrandomized_nonprogression_item: dict[str, Literal['useful_nonprogression', 'filler']] = {}
location_name_to_requirement: dict[str, AutopelagoGameRequirement] = {}
location_name_to_id: dict[str, int] = {}
location_names_with_fixed_rewards: set[str] = set()
_location_id_gen = _gen_ids()

for k, r in _defs['regions']['landmarks'].items():
    _name = r['name']
    location_name_to_id[_name] = next(_location_id_gen)
    location_name_to_unrandomized_progression_item_name[_name] = item_key_to_name[r['unrandomized_item']]
    location_name_to_requirement[_name] = {'all': r['requires']}
    autopelago_regions[k] = AutopelagoRegionDefinition(k, r['exits'], [_name], r['requires'])
    if 'reward_is_fixed' in r and r['reward_is_fixed']:
        location_names_with_fixed_rewards.add(_name)
for rk, r in _defs['regions']['fillers'].items():
    _locations: list[str] = []
    _cur = 1
    for k in r['unrandomized_items']['key'] if 'key' in r['unrandomized_items'] else []:
        if isinstance(k, str):
            _name = r['name_template'].replace('{n}', f'{_cur}')
            location_name_to_id[_name] = next(_location_id_gen)
            location_name_to_unrandomized_progression_item_name[_name] = item_key_to_name[k]
            _locations.append(_name)
            _cur += 1
        else:
            for i in range(k['count']):
                _name = r['name_template'].replace('{n}', f'{_cur}')
                location_name_to_id[_name] = next(_location_id_gen)
                location_name_to_unrandomized_progression_item_name[_name] = item_key_to_name[k['item']]
                _locations.append(_name)
                _cur += 1
    for i in range(r['unrandomized_items']['useful_nonprogression']) if 'useful_nonprogression' in r['unrandomized_items'] else []:
        _name = r['name_template'].replace('{n}', f'{_cur}')
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_unrandomized_nonprogression_item[_name] = 'useful_nonprogression'
        _locations.append(_name)
        _cur += 1
    for i in range(r['unrandomized_items']['filler']) if 'filler' in r['unrandomized_items'] else []:
        _name = r['name_template'].replace('{n}', f'{_cur}')
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_unrandomized_nonprogression_item[_name] = 'filler'
        _locations.append(_name)
        _cur += 1
    autopelago_regions[rk] = AutopelagoRegionDefinition(rk, r['exits'], _locations, [])


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
    item_name_to_rat_count[i] for i in location_name_to_unrandomized_progression_item_name.values() if
    i in item_name_to_rat_count)
assert total_available_rat_count >= max_required_rat_count, f'Game is probably not winnable: {max_required_rat_count} rat(s) might be required with only {total_available_rat_count} available'

del _append_nonprogression
del _cur
del _defs
del _get_required_rat_count
del _item_id_gen
del _location_id_gen
del _locations
del _name
del _name_of
del _rat_count_of
