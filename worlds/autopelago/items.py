import importlib.resources
import pathlib
import sys

from BaseClasses import ItemClassification
from Utils import parse_yaml

from .definitions_types import (
    Aura,
    AutopelagoItemDefinition,
    AutopelagoNonProgressionItemType,
)
from .util import defs, gen_ids

names_with_lactose = set()
lactose_intolerant_names = set()
nonprogression_item_types: list[AutopelagoNonProgressionItemType] = \
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


item_name_to_auras: dict[str, list[Aura]] = {}
progression_item_names: set[str] = set()
item_name_to_rat_count: dict[str, int] = {}
items_by_game: dict[str, list[str]] = {}
item_key_to_name: dict[str, str] = {}
_item_id_gen = gen_ids()
item_name_to_id: dict[str, int] = {}

# since some buffs / traps can be disabled for a particular multiworld, it would be not-quite-right to put each item
# into a fixed "buff" / "trap" / "filler" category like earlier versions once did. instead, assign a score to each aura
# based on what it does, and determine that category based on the combination of the item's auras *that are enabled*.
for k, v in defs["items"].items():
    for _name in _names_of(v):
        item_name_to_auras[_name] = _auras_of(v)
        item_name_to_id[_name] = next(_item_id_gen)
        progression_item_names.add(_name)
        rat_count = _rat_count_of(v)
        if rat_count and rat_count > 0:
            item_name_to_rat_count[_name] = rat_count
        item_key_to_name[k] = _name


def _append_items(item_definitions: list[AutopelagoItemDefinition]):
    res: list[str] = []
    for item_definition in item_definitions:
        for _name in _names_of(item_definition):
            res.append(_name)
            item_name_to_auras[_name] = _auras_of(item_definition)
            item_name_to_id[_name] = next(_item_id_gen)
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
        items_by_game[game_name] = _append_items(parse_yaml(f.open("r")))

item_name_groups: dict[str, set[str]] = {
    "Sewer Progression": set(),
    "Cool World Progression": set(),
    "Space Progression": set(),
    "Rats": {k for k, v in item_name_to_rat_count.items() if v},
    "Special Rats": {k for k, v in item_name_to_rat_count.items() if v and k != item_key_to_name["pack_rat"]},
    "Progression Items": set(),
}

for item_name in item_name_to_id:
    if item_name in progression_item_names:
        item_name_groups["Progression Items"].add(item_name)

    auras = item_name_to_auras[item_name]
    for aura in auras:
        nice_name = aura.replace("_", " ").title()

        item_group_all = f"Gives {nice_name}"
        item_group_only = f"Gives Only {nice_name}"
        item_name_groups.setdefault(item_group_all, set()).add(item_name)
        if len(set(auras)) == 1:
            item_name_groups.setdefault(item_group_only, set()).add(item_name)

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
ENABLED_AURA_SCORE_MULTIPLIER = 1_000_000
ENABLED_AURA_SCORE_THRESHOLD = 100_000

def score_item_by_auras(item: str, enabled_auras: set[Aura]) -> int:
    score = 0
    for aura in item_name_to_auras[item]:
        # disabled auras contribute a tiny bit to the score. they won't influence the score enough
        # to overpower the effects of even the weakest enabled aura, but by keeping their relative
        # pushes/pulls on the overall score intact, we ensure that, e.g., when asking for a "filler"
        # item, we'll usually tend to pick items that would be fillers with all buffs/traps enabled
        # before items that are normally buffs/traps but just happen to have everything disabled.
        # I'm sure there will be exceptions, but it's not SUPER important to do a FANTASTIC job at
        # this, so I'm not spending more time on it right now.
        tmp = _aura_classification_points[aura]
        if aura in enabled_auras:
            tmp *= ENABLED_AURA_SCORE_MULTIPLIER
        score += tmp
    if item in item_name_to_rat_count:
        # if it adds any rats, then it's automatically at least considered "useful". ideally, it
        # ought to be "progression", but there was some reason why I didn't make it like that in the
        # first versions, so keep it that way for now (airbreather 2026-01-03).
        score += 99 * ENABLED_AURA_SCORE_MULTIPLIER
    return score


def classify_item_by_score(score: int) -> ItemClassification:
    return \
        ItemClassification.useful if score > ENABLED_AURA_SCORE_THRESHOLD else \
        ItemClassification.trap if score < -ENABLED_AURA_SCORE_THRESHOLD else \
        ItemClassification.filler
