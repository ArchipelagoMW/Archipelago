from __future__ import annotations
import random

from Options import OptionDict
from schema import Schema, Optional, And, Or
import typing
from typing import Any, Union, Dict, Set, List
import copy

from ..mission_tables import lookup_name_to_mission
from ..mission_groups import mission_groups
from .structs import Difficulty, LayoutType
from .types import Column, Grid, Hopscotch, Gauntlet, Blitz

STR_OPTION_VALUES = {
    "type": {
        "column": Column, "grid": Grid, "hopscotch": Hopscotch, "gauntlet": Gauntlet, "blitz": Blitz,
    },
    "difficulty": {
        "relative": Difficulty.RELATIVE, "starter": Difficulty.STARTER, "easy": Difficulty.EASY,
        "medium": Difficulty.MEDIUM, "hard": Difficulty.HARD, "very hard": Difficulty.VERY_HARD
    },
}
STR_OPTION_VALUES["min_difficulty"] = STR_OPTION_VALUES["difficulty"]
STR_OPTION_VALUES["max_difficulty"] = STR_OPTION_VALUES["difficulty"]
GLOBAL_ENTRY = "global"

StrOption = lambda cat: And(str, lambda val: val.lower() in STR_OPTION_VALUES[cat])
IntNegOne = And(int, lambda val: val >= -1)
IntZero = And(int, lambda val: val >= 0)
IntOne = And(int, lambda val: val >= 1)
IntPercent = And(int, lambda val: 0 <= val <= 100)

SubRuleEntryRule = {
    "rules": [{str: object}], # recursive schema checking is too hard
    "amount": IntNegOne,
}
MissionCountEntryRule = {
    "scope": [str],
    "amount": IntNegOne,
}
BeatMissionsEntryRule = {
    "scope": [str],
}
EntryRule = Or(SubRuleEntryRule, MissionCountEntryRule, BeatMissionsEntryRule)

class CustomMissionOrder(OptionDict):
    """
    Used to generate a custom mission order. Please look at documentation to understand usage.
    """
    display_name = "Custom Mission Order"
    value: Dict[str, Dict[str, Any]]
    default = {
        "Default Campaign": {
            "display_name": "null",
            "entry_rules": [],
            "goal": True,
            "min_difficulty": "relative",
            "max_difficulty": "relative",
            "single_layout_campaign": False,
            GLOBAL_ENTRY: {
                "display_name": "null",
                "entry_rules": [],
                "goal": False,
                "exit": False,
                "mission_pool": ["all missions"],
                "min_difficulty": "relative",
                "max_difficulty": "relative",
                "missions": [],
            },
            "Default Layout": {
                "type": "grid",
                "size": 9,
            },
        },
    }
    schema = Schema({
        # Campaigns
        str: {
            "display_name": [str],
            "entry_rules": [EntryRule],
            "goal": bool,
            "min_difficulty": Difficulty,
            "max_difficulty": Difficulty,
            "single_layout_campaign": bool,
            # Layouts
            str: {
                # Type options
                "type": lambda val: issubclass(val, LayoutType),
                "size": IntOne,
                # Link options
                "exit": bool,
                "goal": bool,
                "display_name": [str],
                "entry_rules": [EntryRule],
                # Mission pool options
                "mission_pool": {int},
                "min_difficulty": Difficulty,
                "max_difficulty": Difficulty,
                # Allow arbitrary options for layout types
                Optional(str): Or(int, str, bool, [Or(int, str, bool)]),
                # Mission slots
                "missions": [{
                    "index": [Or(int, str)],
                    Optional("entrance"): bool,
                    Optional("exit"): bool,
                    Optional("goal"): bool,
                    Optional("empty"): bool,
                    Optional("next"): [int],
                    Optional("entry_rules"): [EntryRule],
                    Optional("mission_pool"): {int},
                    Optional("difficulty"): Difficulty,
                }],
            },
        }
    })
    
    def __init__(self, value: Dict[str, Dict[str, Any]]):
        # Make sure all the globals are filled
        self.value: Dict[str, Dict[str, Any]] = {}
        if value == self.default: # If this option is default, it shouldn't mess with its own values
            value = copy.deepcopy(self.default)

        for campaign in value:
            self.value[campaign] = {}

            # Check if this campaign has a layout type, making it a campaign-level layout
            single_layout_campaign = "type" in value[campaign]
            if single_layout_campaign:
                # Single-layout campaigns are not allowed to declare more layouts
                single_layout = {key: val for (key, val) in value[campaign].items() if type(val) != dict}
                value[campaign] = {campaign: single_layout}
                # Campaign should inherit layout goal status
                if not "goal" in single_layout or not single_layout["goal"]:
                    value[campaign]["goal"] = False
                # Hide campaign name for single-layout campaigns
                value[campaign]["display_name"] = ""
            value[campaign]["single_layout_campaign"] = single_layout_campaign

            # Check if this campaign has a global layout
            global_dict = {}
            for name in value[campaign]:
                if name.lower() == GLOBAL_ENTRY:
                    global_dict = value[campaign].pop(name, {})
                    break

            # Campaign values = default options (except for default layouts) + campaign options
            self.value[campaign] = {key: value for (key, value) in self.default["Default Campaign"].items() if type(value) != dict}
            self.value[campaign].update(value[campaign])
            _resolve_special_options(self.value[campaign])

            for layout in value[campaign]:
                if type(value[campaign][layout]) != dict:
                    continue
                # Layout values = default options + campaign's global options + layout options
                self.value[campaign][layout] = copy.deepcopy(self.default["Default Campaign"][GLOBAL_ENTRY])
                self.value[campaign][layout].update(global_dict)
                self.value[campaign][layout].update(value[campaign][layout])
                _resolve_special_options(self.value[campaign][layout])

                for mission_slot_index in range(len(self.value[campaign][layout]["missions"])):
                    # Defaults for mission slots are handled by the mission slot struct
                    _resolve_special_options(self.value[campaign][layout]["missions"][mission_slot_index])

    # Overloaded to remove pre-init schema validation
    # Schema is still validated after __init__
    @classmethod
    def from_any(cls, data: Dict[str, Any]) -> CustomMissionOrder:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")

def _resolve_special_options(data: Dict[str, Any]):
    # Handle range values & string-to-value conversions
    for option in data:
        option_value = data[option]
        new_value = _resolve_special_option(option, option_value)
        data[option] = new_value

def _resolve_special_option(option: str, option_value: Any) -> Any:
    # Option values can be string representations of values
    if option in STR_OPTION_VALUES:
        if type(option_value) == list:
            return [STR_OPTION_VALUES[option][val.lower()] for val in option_value]
        else:
            return STR_OPTION_VALUES[option][option_value.lower()]
    
    if option == "mission_pool":
        return _resolve_mission_pool(option_value)
    
    if option == "entry_rules":
        rules = [_resolve_entry_rule(subrule) for subrule in option_value]
        return rules
    
    if option == "display_name":
        # Make sure all the values are strings
        if type(option_value) == list:
            names = [str(value) for value in option_value]
            return names
        elif option_value == "null":
            # "null" means no custom display name
            return []
        else:
            return [str(option_value)]
        
    if option == "index":
        # All index values could be ranges
        if type(option_value) == list:
            indices = [_resolve_potential_range(index) for index in option_value]
            indices = [idx if type(idx) == int else str(idx) for idx in indices]
            return indices
        else:
            idx = _resolve_potential_range(option_value)
            return [idx if type(idx) == int else str(idx)]

    # Option values can be ranges
    return _resolve_potential_range(option_value)

def _resolve_entry_rule(option_value: Dict[str, Any]) -> Dict[str, Any]:
    resolved: Dict[str, Any] = {}
    if "amount" in option_value:
        resolved["amount"] = _resolve_potential_range(option_value["amount"])
    if "scope" in option_value:
        # A scope may be a list or a single address
        # Since addresses can be a single index, they may be ranges
        if type(option_value["scope"]) == list:
            resolved["scope"] = [_resolve_potential_range(str(subscope)) for subscope in option_value["scope"]]
        else:
            resolved["scope"] = [_resolve_potential_range(str(option_value["scope"]))]
    if "rules" in option_value:
        resolved["rules"] = [_resolve_entry_rule(subrule) for subrule in option_value["rules"]]
        # Make sure sub-rule rules have a specified amount
        if not "amount" in option_value:
            resolved["amount"] = -1
    return resolved

def _resolve_potential_range(option_value: Union[Any, str]) -> Union[Any, int]:
    # An option value may be a range
    if type(option_value) == str and option_value.startswith("random-range-"):
        resolved = _custom_range(option_value)
        return resolved
    else:
        # As this is a catch-all function,
        # assume non-range option values are handled elsewhere
        # or intended to fall through
        return option_value

def _resolve_mission_pool(option_value: Union[str, List[str]]) -> Set[str]:
    if type(option_value) == str:
        pool = _get_target_missions(option_value)
    else:
        pool: Set[int] = set()
        for line in option_value:
            if line.startswith("~"):
                if len(pool) == 0:
                    raise ValueError(f"Mission Pool term {line} tried to remove missions from an empty pool.")
                term = line[1:].strip()
                missions = _get_target_missions(term)
                pool.difference_update(missions)
            elif line.startswith("and "): # TODO figure out a real symbol
                if len(pool) == 0:
                    raise ValueError(f"Mission Pool term {line} tried to remove missions from an empty pool.")
                term = line[4:].strip()
                missions = _get_target_missions(term)
                pool.intersection_update(missions)
            else:
                if line.startswith("+"):
                    term = line[1:].strip()
                else:
                    term = line.strip()
                missions = _get_target_missions(term)
                pool.update(missions)
    if len(pool) == 0:
        raise ValueError(f"Mission pool evaluated to zero missions: {option_value}")
    return pool

def _get_target_missions(term: str) -> Set[int]:
    if term in lookup_name_to_mission:
        return {lookup_name_to_mission[term].id}
    else:
        groups = [mission_groups[group] for group in mission_groups if group.casefold() == term.casefold()]
        if len(groups) > 0:
            return {lookup_name_to_mission[mission].id for mission in groups[0]}
        else:
            raise ValueError(f"Mission pool term \"{term}\" did not resolve to any specific mission or mission group.")

# Class-agnostic version of AP Options.Range.custom_range
def _custom_range(text: str) -> int:
        textsplit = text.split("-")
        try:
            random_range = [int(textsplit[len(textsplit) - 2]), int(textsplit[len(textsplit) - 1])]
        except ValueError:
            raise ValueError(f"Invalid random range {text} for option {CustomMissionOrder.__name__}")
        random_range.sort()
        if text.startswith("random-range-low"):
            return _triangular(random_range[0], random_range[1], random_range[0])
        elif text.startswith("random-range-middle"):
            return _triangular(random_range[0], random_range[1])
        elif text.startswith("random-range-high"):
            return _triangular(random_range[0], random_range[1], random_range[1])
        else:
            return random.randint(random_range[0], random_range[1])

def _triangular(lower: int, end: int, tri: typing.Optional[int] = None) -> int:
    return int(round(random.triangular(lower, end, tri), 0))