from __future__ import annotations
import typing, random

from Options import OptionDict
from schema import Schema, Optional, And, Or
import copy

from ..mission_tables import lookup_name_to_mission, SC2Mission, MissionFlag, SC2Campaign
from ..mission_groups import mission_groups
from .structs import Difficulty, LayoutType
from .types import Column, Grid

STR_OPTION_VALUES = {
    "type": { "column": Column, "grid": Grid },
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

class CustomMissionOrder(OptionDict):
    """
    Used to generate a custom mission order. Please look at documentation to understand usage.
    """
    display_name = "Mission Order"
    value: typing.Dict[str, typing.Any]
    default = {
        "Default Campaign": {
            "order": 0,
            "unlock_count": -1,
            "unlock_specific": [],
            "required": True,
            "min_difficulty": "relative",
            "max_difficulty": "relative",
            GLOBAL_ENTRY: {
                "order": 0,
                "limit": 0,
                "required": False,
                "unlock_count": -1,
                "unlock_specific": [],
                "mission_pool": ["all missions"],
                "min_difficulty": "relative",
                "max_difficulty": "relative",
            },
            "Default Layout": {
                "type": "grid",
                "size": 9,
                "limit": 3,
            },
        },
    }
    schema = Schema({
        # Campaigns
        str: {
            "order": int,
            "unlock_count": IntNegOne,
            "unlock_specific": [str],
            "required": bool,
            "min_difficulty": Difficulty,
            "max_difficulty": Difficulty,
            # Layouts
            str: {
                # Type options
                "type": lambda val: issubclass(val, LayoutType),
                "order": int,
                "size": IntOne,
                "limit": IntZero,
                # Link options
                "required": bool,
                "unlock_count": IntNegOne,
                "unlock_specific": [str],
                # Mission pool options
                "mission_pool": {int},
                "min_difficulty": Difficulty,
                "max_difficulty": Difficulty,
                # Mission slots
                Optional(int): {
                    Optional("mission"): str,
                    Optional("required"): bool,
                    Optional("entrance"): bool,
                    Optional("exit"): bool,
                    Optional("empty"): bool,
                    Optional("next"): [int],
                    Optional("unlock_count"): IntZero,
                    Optional("unlock_specific"): [str],
                    Optional("mission_pool"): {int},
                    Optional("difficulty"): Difficulty,
                },
            },
        }
    })
    
    def __init__(self, value: typing.Dict[str, typing.Dict[str, typing.Any]]):
        # Make sure all the globals are filled
        self.value = dict()
        if value == self.default: # If this option is default, it shouldn't mess with its own values
            value = copy.deepcopy(self.default)
        for campaign in value:
            self.value[campaign] = dict()
            # Check if this campaign has a global layout
            global_dict = dict()
            for name in value[campaign]:
                if name.lower() == GLOBAL_ENTRY:
                    global_dict = value[campaign].pop(name, dict())
                    break
            self.value[campaign] = {key: value for (key, value) in self.default["Default Campaign"].items() if type(value) != dict}
            self.value[campaign].update(value[campaign])
            _resolve_special_options(self.value[campaign])
            for layout in value[campaign]:
                if type(value[campaign][layout]) != dict:
                    continue
                # Layout values = default options + global options + layout options
                self.value[campaign][layout] = copy.deepcopy(self.default["Default Campaign"][GLOBAL_ENTRY])
                self.value[campaign][layout].update(global_dict)
                self.value[campaign][layout].update(value[campaign][layout])
                _resolve_special_options(self.value[campaign][layout])
                for mission_slot in value[campaign][layout]:
                    if type(mission_slot) == int:
                        # Defaults for mission slots are handled by the mission slot struct
                        _resolve_special_options(self.value[campaign][layout][mission_slot])
        # print(self.value)

    # Overloaded to remove pre-init schema validation
    # Schema is still validated after __init__
    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]) -> CustomMissionOrder:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")

def _resolve_special_options(data: typing.Dict):
    # Handle range values & string-to-value conversions
    range_missions = []
    for option in data:
        # Mission slot indices can be ranges
        if type(option) == str and option.startswith("random-range-"):
            range_missions.append(option)
        option_value = data[option]
        # Option values can be ranges
        if type(option_value) == str and option_value.startswith("random-range-"):
            resolved = _custom_range(option_value)
            data[option] = resolved
        # Option values can be strings representations of values
        if option in STR_OPTION_VALUES:
            if type(option_value) == list:
                data[option] = [STR_OPTION_VALUES[option][val.lower()] for val in option_value]
            else:
                data[option] = STR_OPTION_VALUES[option][option_value.lower()]
        # 'unlock_specific' can contain indices, which need to be converted to strings
        if option == "unlock_specific":
            data[option] = [str(val) for val in option_value]
        # 'mission_pool' contains a list of instructions for making a set of mission indices
        if option == "mission_pool":
            if type(option_value) == str: # TODO consider if this is better or worse than a dedicated 'mission' option
                pool = {lookup_name_to_mission[option_value].id}
            else:
                pool: typing.Set[int] = set()
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
            if len(pool) == 0 and not len(data.get("mission", "")) > 0:
                raise ValueError(f"Mission pool evaluated to zero missions: {option_value}")
            data[option] = pool
    for range in range_missions:
        resolved = _custom_range(range)
        data.setdefault(resolved, dict()).update(data.pop(range))

def _get_target_missions(term: str) -> typing.Set[int]:
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