"""
Contains the Custom Mission Order option. Also validates the option value, so generation can assume the data matches the specification.
"""

from __future__ import annotations
import random

from Options import OptionDict, Visibility
from schema import Schema, Optional, And, Or
import typing
from typing import Any, Union, Dict, Set, List
import copy

from ..mission_tables import lookup_name_to_mission
from ..mission_groups import mission_groups
from ..item.item_tables import item_table
from ..item.item_groups import item_name_groups
from . import layout_types
from .layout_types import LayoutType, Column, Grid, Hopscotch, Gauntlet, Blitz, Canvas
from .mission_pools import Difficulty
from .presets_static import (
    static_preset, preset_mini_wol_with_prophecy, preset_mini_wol, preset_mini_hots, preset_mini_prophecy,
    preset_mini_lotv_prologue, preset_mini_lotv, preset_mini_lotv_epilogue, preset_mini_nco,
    preset_wol_with_prophecy, preset_wol, preset_prophecy, preset_hots, preset_lotv_prologue,
    preset_lotv_epilogue, preset_lotv, preset_nco
)
from .presets_scripted import make_golden_path

GENERIC_KEY_NAME = "Key".casefold()
GENERIC_PROGRESSIVE_KEY_NAME = "Progressive Key".casefold()

STR_OPTION_VALUES: Dict[str, Dict[str, Any]] = {
    "type": {
        "column": Column.__name__, "grid": Grid.__name__, "hopscotch": Hopscotch.__name__, "gauntlet": Gauntlet.__name__, "blitz": Blitz.__name__,
        "canvas": Canvas.__name__,
    },
    "difficulty": {
        "relative": Difficulty.RELATIVE.value, "starter": Difficulty.STARTER.value, "easy": Difficulty.EASY.value,
        "medium": Difficulty.MEDIUM.value, "hard": Difficulty.HARD.value, "very hard": Difficulty.VERY_HARD.value
    },
    "preset": {
        "none": lambda _: {},
        "wol + prophecy": static_preset(preset_wol_with_prophecy),
        "wol": static_preset(preset_wol),
        "prophecy": static_preset(preset_prophecy),
        "hots": static_preset(preset_hots),
        "prologue": static_preset(preset_lotv_prologue),
        "lotv prologue": static_preset(preset_lotv_prologue),
        "lotv": static_preset(preset_lotv),
        "epilogue": static_preset(preset_lotv_epilogue),
        "lotv epilogue": static_preset(preset_lotv_epilogue),
        "nco": static_preset(preset_nco),
        "mini wol + prophecy": static_preset(preset_mini_wol_with_prophecy),
        "mini wol": static_preset(preset_mini_wol),
        "mini prophecy": static_preset(preset_mini_prophecy),
        "mini hots": static_preset(preset_mini_hots),
        "mini prologue": static_preset(preset_mini_lotv_prologue),
        "mini lotv prologue": static_preset(preset_mini_lotv_prologue),
        "mini lotv": static_preset(preset_mini_lotv),
        "mini epilogue": static_preset(preset_mini_lotv_epilogue),
        "mini lotv epilogue": static_preset(preset_mini_lotv_epilogue),
        "mini nco": static_preset(preset_mini_nco),
        "golden path": make_golden_path
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
IntZeroToTen = And(int, lambda val: 0 <= val <= 10)

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
ItemEntryRule = {
    "items": {str: int}
}
EntryRule = Or(SubRuleEntryRule, MissionCountEntryRule, BeatMissionsEntryRule, ItemEntryRule)
SchemaDifficulty = Or(*[value.value for value in Difficulty])

class CustomMissionOrder(OptionDict):
    """
    Used to generate a custom mission order. Please see documentation to understand usage.
    Will do nothing unless `mission_order` is set to `custom`.
    """
    display_name = "Custom Mission Order"
    visibility = Visibility.template
    value: Dict[str, Dict[str, Any]]
    default = {
        "Default Campaign": {
            "display_name": "null",
            "unique_name": False,
            "entry_rules": [],
            "unique_progression_track": 0,
            "goal": True,
            "min_difficulty": "relative",
            "max_difficulty": "relative",
            GLOBAL_ENTRY: {
                "display_name": "null",
                "unique_name": False,
                "entry_rules": [],
                "unique_progression_track": 0,
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
            "unique_name": bool,
            "entry_rules": [EntryRule],
            "unique_progression_track": int,
            "goal": bool,
            "min_difficulty": SchemaDifficulty,
            "max_difficulty": SchemaDifficulty,
            "single_layout_campaign": bool,
            # Layouts
            str: {
                "display_name": [str],
                "unique_name": bool,
                # Type options
                "type": lambda val: issubclass(getattr(layout_types, val), LayoutType),
                "size": IntOne,
                # Link options
                "exit": bool,
                "goal": bool,
                "entry_rules": [EntryRule],
                "unique_progression_track": int,
                # Mission pool options
                "mission_pool": {int},
                "min_difficulty": SchemaDifficulty,
                "max_difficulty": SchemaDifficulty,
                # Allow arbitrary options for layout types
                Optional(str): Or(int, str, bool, [Or(int, str, bool)]),
                # Mission slots
                "missions": [{
                    "index": [Or(int, str)],
                    Optional("entrance"): bool,
                    Optional("exit"): bool,
                    Optional("goal"): bool,
                    Optional("empty"): bool,
                    Optional("next"): [Or(int, str)],
                    Optional("entry_rules"): [EntryRule],
                    Optional("mission_pool"): {int},
                    Optional("difficulty"): SchemaDifficulty,
                    Optional("victory_cache"): IntZeroToTen,
                }],
            },
        }
    })
    
    def __init__(self, yaml_value: Dict[str, Dict[str, Any]]) -> None:
        # This function constructs self.value by parts,
        # so the parent constructor isn't called
        self.value: Dict[str, Dict[str, Any]] = {}
        yaml_value = copy.deepcopy(yaml_value) # Ensure that all the mutations are local to the world

        for campaign in yaml_value:
            self.value[campaign] = {}

            # Check if this campaign has a layout type, making it a campaign-level layout
            single_layout_campaign = "type" in yaml_value[campaign]
            if single_layout_campaign:
                # Single-layout campaigns are not allowed to declare more layouts
                single_layout = {key: val for (key, val) in yaml_value[campaign].items() if type(val) != dict}
                yaml_value[campaign] = {campaign: single_layout}
                # Campaign should inherit certain values from the layout
                if "goal" not in single_layout or not single_layout["goal"]:
                    yaml_value[campaign]["goal"] = False
                if "unique_progression_track" in single_layout:
                    yaml_value[campaign]["unique_progression_track"] = single_layout["unique_progression_track"]
                # Hide campaign name for single-layout campaigns
                yaml_value[campaign]["display_name"] = ""
            yaml_value[campaign]["single_layout_campaign"] = single_layout_campaign

            # Check if this campaign has a global layout
            global_dict = {}
            for name in yaml_value[campaign]:
                if name.lower() == GLOBAL_ENTRY:
                    global_dict = yaml_value[campaign].pop(name)
                    break

            # Strip layouts and unknown options from the campaign
            # The latter are assumed to be preset options
            preset_key: str = yaml_value[campaign].pop("preset", "none")
            layout_keys = [key for (key, val) in yaml_value[campaign].items() if type(val) == dict]
            layouts = {key: yaml_value[campaign].pop(key) for key in layout_keys}
            preset_option_keys = [key for key in yaml_value[campaign] if key not in self.default["Default Campaign"]]
            preset_option_keys.remove("single_layout_campaign")
            preset_options = {key: yaml_value[campaign].pop(key) for key in preset_option_keys}

            # Resolve preset
            preset: Dict[str, Any] = _resolve_string_option_single("preset", preset_key)(preset_options)
            # Preset global is resolved internally to avoid conflict with user global
            preset_global_dict = {}
            for name in preset:
                if name.lower() == GLOBAL_ENTRY:
                    preset_global_dict = preset.pop(name)
                    break
            preset_layout_keys = [key for (key, val) in preset.items() if type(val) == dict]
            preset_layouts = {key: preset.pop(key) for key in preset_layout_keys}
            ordered_layouts = {key: copy.deepcopy(preset_global_dict) for key in preset_layout_keys}
            for key in preset_layout_keys:
                ordered_layouts[key].update(preset_layouts[key])
            # Final layouts are preset layouts (updated by same-name user layouts) followed by custom user layouts
            for key in layouts:
                if key in ordered_layouts:
                    # Mission slots for presets should go before user mission slots
                    if "missions" in layouts[key] and "missions" in ordered_layouts[key]:
                        layouts[key]["missions"] = ordered_layouts[key]["missions"] + layouts[key]["missions"]
                    ordered_layouts[key].update(layouts[key])
                else:
                    ordered_layouts[key] = layouts[key]

            # Campaign values = default options (except for default layouts) + preset options (except for layouts) +  campaign options
            self.value[campaign] = {key: value for (key, value) in self.default["Default Campaign"].items() if type(value) != dict}
            self.value[campaign].update(preset)
            self.value[campaign].update(yaml_value[campaign])
            _resolve_special_options(self.value[campaign])

            for layout in ordered_layouts:
                # Layout values = default options + campaign's global options + layout options
                self.value[campaign][layout] = copy.deepcopy(self.default["Default Campaign"][GLOBAL_ENTRY])
                self.value[campaign][layout].update(global_dict)
                self.value[campaign][layout].update(ordered_layouts[layout])
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

    # Special case for canvas layouts determining their own size
    if "type" in data and data["type"] == Canvas.__name__:
        canvas: List[str] = data["canvas"]
        longest_line = max(len(line) for line in canvas)
        data["size"] = len(canvas) * longest_line
        data["width"] = longest_line


def _resolve_special_option(option: str, option_value: Any) -> Any:
    # Option values can be string representations of values
    if option in STR_OPTION_VALUES:
        return _resolve_string_option(option, option_value)
    
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
        
    if option in ["index", "next"]:
        # All index values could be ranges
        if type(option_value) == list:
            # Flatten any nested lists
            indices = [idx for val in [idx if type(idx) == list else [idx] for idx in option_value] for idx in val]
            indices = [_resolve_potential_range(index) for index in indices]
            indices = [idx if type(idx) == int else str(idx) for idx in indices]
            return indices
        else:
            idx = _resolve_potential_range(option_value)
            return [idx if type(idx) == int else str(idx)]

    # Option values can be ranges
    return _resolve_potential_range(option_value)


def _resolve_string_option_single(option: str, option_value: str) -> Any:
    formatted_value = option_value.lower().replace("_", " ")
    if formatted_value not in STR_OPTION_VALUES[option]:
        raise ValueError(
            f"Option \"{option}\" received unknown value \"{option_value}\".\n"
            f"Allowed values are: {list(STR_OPTION_VALUES[option].keys())}"
        )
    return STR_OPTION_VALUES[option][formatted_value]


def _resolve_string_option(option: str, option_value: Union[List[str], str]) -> Any:
    if type(option_value) == list:
        return [_resolve_string_option_single(option, val) for val in option_value]
    else:
        return _resolve_string_option_single(option, option_value)


def _resolve_entry_rule(option_value: Dict[str, Any]) -> Dict[str, Any]:
    resolved: Dict[str, Any] = {}
    mutually_exclusive: List[str] = []
    if "amount" in option_value:
        resolved["amount"] = _resolve_potential_range(option_value["amount"])
    if "scope" in option_value:
        mutually_exclusive.append("scope")
        # A scope may be a list or a single address
        if type(option_value["scope"]) == list:
            resolved["scope"] = [str(subscope) for subscope in option_value["scope"]]
        else:
            resolved["scope"] = [str(option_value["scope"])]
    if "rules" in option_value:
        mutually_exclusive.append("rules")
        resolved["rules"] = [_resolve_entry_rule(subrule) for subrule in option_value["rules"]]
        # Make sure sub-rule rules have a specified amount
        if "amount" not in option_value:
            resolved["amount"] = -1
    if "items" in option_value:
        mutually_exclusive.append("items")
        option_items: Dict[str, Any] = option_value["items"]
        resolved_items = {item: int(_resolve_potential_range(str(amount))) for (item, amount) in option_items.items()}
        resolved_items = _resolve_item_names(resolved_items)
        resolved["items"] = {}
        for item in resolved_items:
            if item not in item_table:
                if item.casefold() == GENERIC_KEY_NAME or item.casefold().startswith(GENERIC_PROGRESSIVE_KEY_NAME):
                    resolved["items"][item] = max(0, resolved_items[item])
                    continue
                raise ValueError(f"Item rule contains \"{item}\", which is not a valid item name.")
            amount = max(0, resolved_items[item])
            quantity = item_table[item].quantity
            if amount == 0:
                final_amount = quantity
            elif quantity == 0:
                final_amount = amount
            else:
                final_amount = amount
            resolved["items"][item] = final_amount
    if len(mutually_exclusive) > 1:
        raise ValueError(
            "Entry rule contains too many identifiers.\n"
            f"Rule: {option_value}\n"
            f"Remove all but one of these entries: {mutually_exclusive}"
        )
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


def _resolve_mission_pool(option_value: Union[str, List[str]]) -> Set[int]:
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
            elif line.startswith("^"):
                if len(pool) == 0:
                    raise ValueError(f"Mission Pool term {line} tried to remove missions from an empty pool.")
                term = line[1:].strip()
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


# Version of options.Sc2ItemDict.verify without World
def _resolve_item_names(value: Dict[str, int]) -> Dict[str, int]:
    new_value: dict[str, int] = {}
    case_insensitive_group_mapping = {
        group_name.casefold(): group_value for group_name, group_value in item_name_groups.items()
    }
    case_insensitive_group_mapping.update({item.casefold(): {item} for item in item_table})
    for group_name in value:
        item_names = case_insensitive_group_mapping.get(group_name.casefold(), {group_name})
        for item_name in item_names:
            new_value[item_name] = new_value.get(item_name, 0) + value[group_name]
    return new_value
    