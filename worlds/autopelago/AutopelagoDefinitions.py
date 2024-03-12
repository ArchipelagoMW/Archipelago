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


AutopelagoItemDefinition = str | AutopelagoItemDefinitionCls
AutopelagoItemDefinitionsSimple = dict[str, AutopelagoItemDefinition]
AutopelagoGameSpecificItemGroup = dict[Literal['game_specific'], dict[str, list[str]]]
AutopelagoNonProgressionGroupItems = list[str | AutopelagoGameSpecificItemGroup]
AutopelagoNonProgressionItemType = Literal['useful_nonprogression', 'trap', 'filler', 'uncategorized']

def _name_of(item: AutopelagoItemDefinition):
    return item if isinstance(item, str) else item['name']

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
    goal: AutopelagoItemDefinition
    rats: AutopelagoItemDefinitionsSimple
    useful_nonprogression: AutopelagoNonProgressionGroupItems
    trap: AutopelagoNonProgressionGroupItems
    filler: AutopelagoNonProgressionGroupItems
    uncategorized: AutopelagoNonProgressionGroupItems
    # any_other_str_key_not_listed: AutopelagoItemDefinition


AutopelagoGameRequirement: TypeAlias = 'AutopelagoAllRequirement | AutopelagoAnyRequirement | AutopelagoItemRequirement | AutopelagoAbilityCheckRequirement | AutopelagoRatCountRequirement'


class AutopelagoAllRequirement(TypedDict):
    all: list[AutopelagoGameRequirement]


class AutopelagoAnyRequirement(TypedDict):
    any: list[AutopelagoGameRequirement]


class AutopelagoItemRequirement(TypedDict):
    item: str


class AutopelagoAbilityCheckRequirement(TypedDict):
    ability_check_with_dc: int


class AutopelagoRatCountRequirement(TypedDict):
    rat_count: int


class AutopelagoLandmarkRegionDefinition(TypedDict):
    name: str
    unrandomized_item: str
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
    each_requires: list[AutopelagoGameRequirement]
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

    def __init__(self, key: str, exits: list[str], locations: list[str], requires: list[AutopelagoGameRequirement] = []):
        self.key = key
        self.exits = exits
        self.locations = locations
        self.requires = { 'all': requires }


with open(PurePath(__file__).with_name('AutopelagoDefinitions.yml'), 'r') as f:
    _defs: AutopelagoDefinitions = parse_yaml(f.read())

def _gen_ids():
    next_id = BASE_ID
    while True:
        yield next_id
        next_id += 1

item_name_to_id: dict[str, int] = { }
generic_nonprogression_item_table: dict[AutopelagoNonProgressionItemType, list[str]] = { 'useful_nonprogression': [], 'trap': [], 'filler': [], 'uncategorized': [] }
item_name_to_defined_classification: dict[str, Optional[ItemClassification]] = { }
item_name_to_rat_count: dict[str, int] = { }
game_specific_nonprogression_items: dict[str, dict[AutopelagoNonProgressionItemType, list[str]]] = { }
item_key_to_name: dict[str, str] = { }
_id_gen = _gen_ids()
for k, v in ((k, v) for k, v in _defs['items'].items() if k not in { 'rats', 'useful_nonprogression', 'trap', 'filler', 'uncategorized' }):
    _name = _name_of(v)
    item_name_to_id[_name] = next(_id_gen)
    item_name_to_defined_classification[_name] = ItemClassification.progression
    item_name_to_rat_count[_name] = _rat_count_of(v)
    item_key_to_name[k] = _name

for k, v in _defs['items']['rats'].items():
    _name = _name_of(v)
    item_name_to_id[_name] = next(_id_gen)
    item_name_to_defined_classification[_name] = ItemClassification.progression
    item_name_to_rat_count[_name] = _rat_count_of(v) or 1
    item_key_to_name[k] = _name

def _append_nonprogression(k: AutopelagoNonProgressionItemType):
    item_classification = autopelago_item_classification_of(k)
    for i in _defs['items'][k]:
        if isinstance(i, str):
            generic_nonprogression_item_table[k].append(i)
            item_name_to_id[i] = next(_id_gen)
            item_name_to_defined_classification[i] = item_classification
            item_name_to_rat_count[_name] = 0
            continue

        for g, v in i['game_specific'].items():
            if g not in game_specific_nonprogression_items:
                game_specific_nonprogression_items[g] = { }
            game_specific_nonprogression_items[g][k] = []
            for it in v:
                game_specific_nonprogression_items[g][k].append(it)
                item_name_to_id[it] = next(_id_gen)
                item_name_to_defined_classification[it] = item_classification
                item_name_to_rat_count[_name] = 0

_append_nonprogression('useful_nonprogression')
_append_nonprogression('trap')
_append_nonprogression('filler')
_append_nonprogression('uncategorized')

regions: dict[str, AutopelagoRegionDefinition] = { 'goal': AutopelagoRegionDefinition('goal', [], []) }
location_name_to_id: dict[str, int] = { }
location_name_to_requirement: dict[str, AutopelagoGameRequirement] = { }
location_name_to_unrandomized_progression_item_name: dict[str, Optional[str]] = { }
location_name_to_unrandomized_nonprogression_item: dict[str, Optional[Literal['useful_nonprogression', 'filler']]] = { }
_id_gen = _gen_ids()
for k, r in _defs['regions']['landmarks'].items():
    location_name_to_unrandomized_progression_item_name[r['name']] = item_key_to_name[r['unrandomized_item']]
    location_name_to_unrandomized_nonprogression_item[r['name']] = None
    location_name_to_requirement[r['name']] = { 'all': r['requires'] }
    location_name_to_id[r['name']] = next(_id_gen)
    regions[k] = AutopelagoRegionDefinition(k, r['exits'], [r['name']], r['requires'])
for rk, r in _defs['regions']['fillers'].items():
    if rk == 'menu':
        rk = 'Menu'
    _locations: list[str] = []
    _cur = 1
    for k in r['unrandomized_items']['key']:
        if isinstance(k, str):
            _name = r['name_template'].replace('{n}', f'{_cur}')
            location_name_to_unrandomized_progression_item_name[_name] = item_key_to_name[k]
            location_name_to_unrandomized_nonprogression_item[_name] = None
            location_name_to_requirement[_name] = { 'all': r['each_requires'] }
            location_name_to_id[_name] = next(_id_gen)
            _locations.append(_name)
            _cur += 1
        else:
            for i in range(k['count']):
                _name = r['name_template'].replace('{n}', f'{_cur}')
                location_name_to_unrandomized_progression_item_name[_name] = item_key_to_name[k['item']]
                location_name_to_unrandomized_nonprogression_item[_name] = None
                location_name_to_requirement[_name] = { 'all': r['each_requires'] }
                location_name_to_id[_name] = next(_id_gen)
                _locations.append(_name)
                _cur += 1
    for i in range(r['unrandomized_items']['useful_nonprogression']):
        _name = r['name_template'].replace('{n}', f'{_cur}')
        location_name_to_unrandomized_progression_item_name[_name] = None
        location_name_to_unrandomized_nonprogression_item[_name] = 'useful_nonprogression'
        location_name_to_requirement[_name] = { 'all': r['each_requires'] }
        location_name_to_id[_name] = next(_id_gen)
        _locations.append(_name)
        _cur += 1
    for i in range(r['unrandomized_items']['filler']):
        _name = r['name_template'].replace('{n}', f'{_cur}')
        location_name_to_unrandomized_progression_item_name[_name] = None
        location_name_to_unrandomized_nonprogression_item[_name] = 'filler'
        location_name_to_requirement[_name] = { 'all': r['each_requires'] }
        location_name_to_id[_name] = next(_id_gen)
        _locations.append(_name)
        _cur += 1
    regions[rk] = AutopelagoRegionDefinition(rk, r['exits'], _locations)

del _append_nonprogression
del _cur
del _defs
del _id_gen
del _locations
del _name
del _name_of
del _rat_count_of
