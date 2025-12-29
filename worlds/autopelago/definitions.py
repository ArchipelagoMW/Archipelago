import importlib.resources
import pathlib
import pkgutil
import sys
from collections import deque
from typing import Literal, NotRequired, TypeAlias, TypedDict, Union

from BaseClasses import ItemClassification
from Utils import parse_yaml

GAME_NAME = "Autopelago"
names_with_lactose = set()
lactose_intolerant_names = set()
Aura = Literal[
  "well_fed",
  "lucky",
  "energized",
  "stylish",
  "smart",
  "confident",
  "upset_tummy",
  "unlucky",
  "sluggish",
  "distracted",
  "startled",
  "conspiratorial",
]


class AutopelagoItemDefinitionCls(TypedDict):
    name: str | list[str]
    rat_count: NotRequired[int]
    flavor_text: NotRequired[str]
    auras_granted: NotRequired[list[str]]


# AutopelagoItemDefinition can be in any of these formats:
# 1: [name, [aura1, aura2]]
# 2: [[name_with_lactose, lactose_intolerant_name], [aura1, aura2]]
# 3:
# - name: Yet Another Rat
#   rat_count: 1
#   flavor_text: Some flavor text that shows up nowhere for now.
#   auras_granted: [aura1, aura2]
AutopelagoItemDefinition = tuple[str | list[str], list[str]] | AutopelagoItemDefinitionCls
AutopelagoNonProgressionItemType = Literal["useful_nonprogression", "trap", "filler"]
autopelago_nonprogression_item_types: list[AutopelagoNonProgressionItemType] = \
    ["useful_nonprogression", "trap", "filler"]


def _to_lactose_name(name_or_list: str | list[str]) -> str:
    if isinstance(name_or_list, str):
        return name_or_list
    return name_or_list[0]


def _lactose_name_of(item: AutopelagoItemDefinition):
    return \
        _to_lactose_name(item[0]) if isinstance(item, list) else \
        _to_lactose_name(item["name"])


def _to_lactose_intolerant_name(name_or_list: str | list[str]) -> str:
    if isinstance(name_or_list, str):
        return name_or_list
    return name_or_list[1]


def _lactose_intolerant_name_of(item: AutopelagoItemDefinition):
    return \
        _to_lactose_intolerant_name(item[0]) if isinstance(item, list) else \
        _to_lactose_intolerant_name(item["name"])


def _names_of(item: AutopelagoItemDefinition):
    lactose_name = _lactose_name_of(item)
    lactose_intolerant_name = _lactose_intolerant_name_of(item)
    if lactose_name == lactose_intolerant_name:
        return [lactose_name]
    names_with_lactose.add(lactose_name)
    lactose_intolerant_names.add(lactose_intolerant_name)
    return [lactose_name, lactose_intolerant_name]


def _rat_count_of(item: AutopelagoItemDefinition):
    return item["rat_count"] if isinstance(item, dict) and "rat_count" in item else None


def _auras_of(item: AutopelagoItemDefinition) -> list[Aura]:
    return \
        item[1] if isinstance(item, list) else \
        item["auras_granted"] if "auras_granted" in item else \
        []


def autopelago_item_classification_of(item: AutopelagoNonProgressionItemType):
    match item:
        case "useful_nonprogression":
            return ItemClassification.useful
        case "trap":
            return ItemClassification.trap
        case "filler":
            return ItemClassification.filler
        case _:
            return None


AutopelagoGameRequirement: TypeAlias = Union[
    "AutopelagoAllRequirement", "AutopelagoAnyRequirement", "AutopelagoItemRequirement",
    "AutopelagoRatCountRequirement", "AutopelagoAnyTwoRequirement"]


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
    requires: AutopelagoGameRequirement
    exits: list[str] | None


class AutopelagoItemKeyReferenceCls(TypedDict):
    item: str
    count: int


AutopelagoItemKeyReference = str | AutopelagoItemKeyReferenceCls


# "filler region" means that it's a region to fill out the locations, not that it's a region intended to contain filler
# items. naming things is hard >.<
class AutopelagoFillerRegionItemsDefinition(TypedDict):
    # "key" as in "item key", as in "the key of the item in the 'items' section of this file", not as in "key item",
    # even though all are, in fact, progression items.
    key: list[AutopelagoItemKeyReference]
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
    items: dict[str, AutopelagoItemDefinitionCls]
    regions: AutopelagoRegionDefinitions


class AutopelagoRegionDefinition:
    key: str
    exits: list[str]
    locations: list[str]
    requires: AutopelagoAllRequirement
    landmark: bool

    def __init__(self, key: str, exits: list[str], locations: list[str], requires: AutopelagoGameRequirement,
                 landmark: bool):
        self.key = key
        self.exits = exits
        self.locations = locations
        self.requires = requires
        self.landmark = landmark


_defs: AutopelagoDefinitions = parse_yaml(pkgutil.get_data(__name__, "AutopelagoDefinitions.yml"))


def _gen_ids():
    next_id = 1
    while True:
        yield next_id
        next_id += 1


item_name_to_auras: dict[str, list[str]] = {}
item_name_to_classification: dict[str, ItemClassification | None] = {}
item_name_to_rat_count: dict[str, int] = {}
items_by_type_by_game: dict[str, dict[AutopelagoNonProgressionItemType, list[str]]] = {}
item_key_to_name: dict[str, str] = {}
_item_id_gen = _gen_ids()
item_name_to_id: dict[str, int] = {}

# since some buffs / traps can be disabled for a particular multiworld, it would be not-quite-right to put each item
# into a fixed "buff" / "trap" / "filler" category like earlier versions once did. instead, assign a score to each aura
# based on what it does, and determine that category based on the combination of the item's auras *that are enabled*.
#
#
#
# TODO (before publishing PR... if I forgor, then please get me!): we still classify items the "not-quite-right" way
# that's described above, because it's a much bigger change to fix that than what I have planned in-scope right now.
_aura_classification_points: dict[Aura, int] = {
  "well_fed": 5,
  "lucky": 3,
  "energized": 5,
  "stylish": 1,
  "smart": 1,
  "confident": 3,
  "upset_tummy": -5,
  "unlucky": -1,
  "sluggish": -5,
  "distracted": -3,
  "startled": -6,
  "conspiratorial": -1,
}

for k, v in _defs["items"].items():
    for _name in _names_of(v):
        item_name_to_auras[_name] = _auras_of(v)
        item_name_to_id[_name] = next(_item_id_gen)
        item_name_to_classification[_name] = ItemClassification.progression
        rat_count = _rat_count_of(v)
        if rat_count and rat_count > 0:
            item_name_to_rat_count[_name] = rat_count
        item_key_to_name[k] = _name


def _append_items(item_definitions: list[AutopelagoItemDefinition]):
    res: dict[AutopelagoNonProgressionItemType, list[str]] = {}
    for item_definition in item_definitions:
        for _name in _names_of(item_definition):
            item_name_to_auras[_name] = _auras_of(item_definition)
            item_name_to_id[_name] = next(_item_id_gen)
            pts = sum(_aura_classification_points[i] for i in _auras_of(item_definition))
            item_type: AutopelagoNonProgressionItemType = \
                "useful_nonprogression" if pts > 0 else \
                "trap" if pts < 0 else \
                "filler"
            res.setdefault(item_type, []).append(_name)
            item_name_to_classification[_name] = autopelago_item_classification_of(item_type)
            rat_count = _rat_count_of(item_definition)
            if rat_count and rat_count > 0:
                item_name_to_rat_count[_name] = rat_count
    return res


# importlib.resources.files changed in Python 3.12 to work a bit more sensibly for our situation. it's not really worth
# finding a way to build a string that will work here in Python 3.11 (which is essentially one foot out the door at the
# time of writing). just do what makes 3.11 work, but build it "correctly" for the future (airbreather 2025-12-09).
anchor = \
    __name__ if sys.version_info >= (3, 12) else \
    "worlds.autopelago"
for package_file_or_dir in importlib.resources.files(anchor).iterdir():
    if package_file_or_dir.name != "items_by_game":
        continue
    for f in package_file_or_dir.iterdir():
        game_name = pathlib.Path(f.name).with_suffix("").stem
        items_by_type_by_game[game_name] = _append_items(parse_yaml(f.open("r")))

autopelago_regions: dict[str, AutopelagoRegionDefinition] = {}
location_name_to_progression_item_name: dict[str, str] = {}
location_name_to_nonprogression_item: dict[str, Literal["useful_nonprogression", "filler"]] = {}
location_name_to_requirement: dict[str, AutopelagoGameRequirement] = {}
location_name_to_id: dict[str, int] = {}
_location_id_gen = _gen_ids()

# build regions for landmarks
for k, curr_region in _defs["regions"]["landmarks"].items():
    _name = curr_region["name"]
    location_name_to_id[_name] = next(_location_id_gen)
    location_name_to_progression_item_name[_name] = item_key_to_name[curr_region["unrandomized_item"]]
    location_name_to_requirement[_name] = curr_region["requires"]
    exits: list[str] = curr_region["exits"] if "exits" in curr_region else []
    autopelago_regions[k] = AutopelagoRegionDefinition(k, exits, [_name], curr_region["requires"], True)

# build regions for fillers. these don't have any special requirements beyond region connections.
_no_requirement: AutopelagoAllRequirement = {"all": []}
for rk, curr_region in _defs["regions"]["fillers"].items():
    _locations: list[str] = []
    _cur = 1
    region_items = curr_region["unrandomized_items"]
    for k in region_items["key"] if "key" in region_items else []:
        if isinstance(k, str):
            # key:
            #   - pizza_rat
            _name = curr_region["name_template"].replace("{n}", f"{_cur}")
            location_name_to_id[_name] = next(_location_id_gen)
            location_name_to_progression_item_name[_name] = item_key_to_name[k]
            _locations.append(_name)
            _cur += 1
        else:
            # key:
            #   - item: pack_rat
            #     count: 5
            for _ in range(k["count"]):
                _name = curr_region["name_template"].replace("{n}", f"{_cur}")
                location_name_to_id[_name] = next(_location_id_gen)
                location_name_to_progression_item_name[_name] = item_key_to_name[k["item"]]
                _locations.append(_name)
                _cur += 1
    for _ in range(region_items["useful_nonprogression"]) if "useful_nonprogression" in region_items else []:
        _name = curr_region["name_template"].replace("{n}", f"{_cur}")
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_nonprogression_item[_name] = "useful_nonprogression"
        _locations.append(_name)
        _cur += 1
    for _ in range(region_items["filler"]) if "filler" in region_items else []:
        _name = curr_region["name_template"].replace("{n}", f"{_cur}")
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_nonprogression_item[_name] = "filler"
        _locations.append(_name)
        _cur += 1
    autopelago_regions[rk] = AutopelagoRegionDefinition(rk, curr_region["exits"], _locations, _no_requirement, False)


def _get_required_rat_count(req: AutopelagoGameRequirement):
    if "all" in req:
        return max(_get_required_rat_count(sub_req) for sub_req in req["all"]) if req["all"] else 0
    if "any" in req:
        return min(_get_required_rat_count(sub_req) for sub_req in req["any"])
    if "rat_count" in req:
        return req["rat_count"]
    return 0


max_required_rat_count = max(
    _get_required_rat_count(req) for req in
        [location_name_to_requirement.values()] +
        [r.requires for r in autopelago_regions.values()]
)
total_available_rat_count = sum(
    item_name_to_rat_count[i] for i in
    location_name_to_progression_item_name.values()
        if i in item_name_to_rat_count
)

item_name_groups: dict[str, set[str]] = {
    "Sewer Progression": set(),
    "Cool World Progression": set(),
    "Space Progression": set(),
    "Rats": {k for k, v in item_name_to_rat_count.items() if v},
    "Special Rats": {k for k, v in item_name_to_rat_count.items() if v and k != item_key_to_name["pack_rat"]},

    "Progression Items": set(),
    # TODO: probably remove "Buffs", "Fillers", and "Traps" from item_name_groups because they're going to be dynamic.
    "Buffs": set(),
    "Fillers": set(),
    "Traps": set(),
}

location_name_groups: dict[str, set[str]] = {
    "Landmarks": set(),
    "Fillers": set(),
    "Zone Bosses": set(),
    "Sewer Landmarks": set(),
    "Sewer Fillers": set(),
    "Cool World Landmarks": set(),
    "Cool World Fillers": set(),
    "Space Landmarks": set(),
    "Space Fillers": set(),
    "Optional Bosses": set(),
    "Optional Fillers": set(),
}

for item_name, classification in item_name_to_classification.items():
    if classification == ItemClassification.filler:
        item_name_groups["Fillers"].add(item_name)
    elif classification == ItemClassification.useful:
        item_name_groups["Buffs"].add(item_name)
    elif classification == ItemClassification.trap:
        item_name_groups["Traps"].add(item_name)
    elif classification == ItemClassification.progression:
        item_name_groups["Progression Items"].add(item_name)

    auras = item_name_to_auras[item_name]
    for aura in auras:
        nice_name = aura.replace("_", " ").title()

        item_group_all = f"Gives {nice_name}"
        item_group_only = f"Gives Only {nice_name}"
        if item_group_all not in item_name_groups:
            item_name_groups[item_group_all] = set()
            item_name_groups[item_group_only] = set()

        item_name_groups[item_group_all].add(item_name)
        if len(set(auras)) == 1:
            item_name_groups[item_group_only].add(item_name)


def _visit_for_items(group_name: str, req: AutopelagoGameRequirement):
    if "item" in req:
        req: AutopelagoItemRequirement
        item_name_groups[group_name].add(item_key_to_name[req["item"]])
    elif "all" in req:
        req: AutopelagoAllRequirement
        for sub_req in req["all"]:
            _visit_for_items(group_name, sub_req)
    elif "any" in req:
        req: AutopelagoAnyRequirement
        for sub_req in req["any"]:
            _visit_for_items(group_name, sub_req)
    elif "any_two" in req:
        req: AutopelagoAnyTwoRequirement
        for sub_req in req["any_two"]:
            _visit_for_items(group_name, sub_req)


q: deque[tuple[str, AutopelagoRegionDefinition | None, AutopelagoRegionDefinition]] = deque()
q.append(("Sewer", None, autopelago_regions["before_basketball"]))
while q:
    prev_region_from_q: AutopelagoRegionDefinition
    curr_region_from_q: AutopelagoRegionDefinition
    zone, prev_region_from_q, curr_region_from_q = q.popleft()
    _visit_for_items(f"{zone} Progression", curr_region_from_q.requires)
    region_type = "Landmarks" if curr_region_from_q.landmark else "Fillers"
    if curr_region_from_q.key == "captured_goldfish":
        region_type = "Zone Bosses"
        next_zone = "Cool World"
    elif curr_region_from_q.key == "secret_cache":
        region_type = "Zone Bosses"
        next_zone = "Space"
    elif curr_region_from_q.key == "snakes_on_a_planet":
        # nothing else needed beyond here
        continue
    else:
        next_zone = zone

    next_regions = [autopelago_regions[e] for e in curr_region_from_q.exits]
    for loc in curr_region_from_q.locations:
        location_name_groups[region_type].add(loc)
        if region_type != "Zone Bosses":
            location_name_groups[f"{zone} {region_type}"].add(loc)

        if not next_regions:
            location_name_groups["Optional Bosses"].add(loc)
            for prev_loc in prev_region_from_q.locations:
                location_name_groups["Optional Fillers"].add(prev_loc)

    if next_zone:
        for next_region in next_regions:
            q.append((next_zone, curr_region_from_q, next_region))
