import ast
import csv
import os
import pkgutil
import json

from BaseClasses import MultiWorld, Item
from enum import IntEnum
from typing import Optional, List, TYPE_CHECKING, Union, get_args, get_origin, Any
from types import GenericAlias
from worlds.AutoWorld import World
from .hooks.Helpers import before_is_category_enabled, before_is_item_enabled, before_is_location_enabled

if TYPE_CHECKING:
    from .Items import ManualItem
    from .Locations import ManualLocation

# blatantly copied from the minecraft ap world because why not
def load_data_file(*args) -> dict:
    fname = "/".join(["data", *args])

    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata

def load_data_csv(*args) -> list[dict]:
    fname = "/".join(["data", *args])

    try:
        lines = pkgutil.get_data(__name__, fname).decode().splitlines()
    except:
        lines = []
    filedata = list(csv.DictReader(lines))

    return filedata

def is_option_enabled(multiworld: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(multiworld, player, name) > 0

def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(multiworld.worlds[player].options, name, None)
    if option is None:
        return 0

    return option.value

def clamp(value, min, max):
    """Returns value clamped to the inclusive range of min and max"""
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

def is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> bool:
    from .Data import category_table
    """Check if a category has been disabled by a yaml option."""
    hook_result = before_is_category_enabled(multiworld, player, category_name)
    if hook_result is not None:
        return hook_result

    category_data = category_table.get(category_name, {})
    return resolve_yaml_option(multiworld, player, category_data)

def resolve_yaml_option(multiworld: MultiWorld, player: int, data: dict) -> bool:
    if "yaml_option" in data:
        for option_name in data["yaml_option"]:
            required = True
            if option_name.startswith("!"):
                option_name = option_name[1:]
                required = False

            option_name = format_to_valid_identifier(option_name)
            if is_option_enabled(multiworld, player, option_name) != required:
                return False
    return True

def is_item_name_enabled(multiworld: MultiWorld, player: int, item_name: str) -> bool:
    """Check if an item named 'item_name' has been disabled by a yaml option."""
    item = multiworld.worlds[player].item_name_to_item.get(item_name, {})
    if not item:
        return False

    return is_item_enabled(multiworld, player, item)

def is_item_enabled(multiworld: MultiWorld, player: int, item: "ManualItem") -> bool:
    """Check if an item has been disabled by a yaml option."""
    hook_result = before_is_item_enabled(multiworld, player, item)
    if hook_result is not None:
        return hook_result

    return _is_manualobject_enabled(multiworld, player, item)

def is_location_name_enabled(multiworld: MultiWorld, player: int, location_name: str) -> bool:
    """Check if a location named 'location_name' has been disabled by a yaml option."""
    location = multiworld.worlds[player].location_name_to_location.get(location_name, {})
    if not location:
        return False

    return is_location_enabled(multiworld, player, location)

def is_location_enabled(multiworld: MultiWorld, player: int, location: "ManualLocation") -> bool:
    """Check if a location has been disabled by a yaml option."""
    hook_result = before_is_location_enabled(multiworld, player, location)
    if hook_result is not None:
        return hook_result

    return _is_manualobject_enabled(multiworld, player, location)

def _is_manualobject_enabled(multiworld: MultiWorld, player: int, object: Any) -> bool:
    """Internal method: Check if a Manual Object has any category disabled by a yaml option.
    \nPlease use the proper is_'item/location'_enabled or is_'item/location'_name_enabled methods instead.
    """
    enabled = True
    for category in object.get("category", []):
        if not is_category_enabled(multiworld, player, category):
            enabled = False
            break

    return enabled

def get_items_for_player(multiworld: MultiWorld, player: int, includePrecollected: bool = False) -> List[Item]:
    """Return list of items of a player including placed items"""
    items = [i for i in multiworld.get_items() if i.player == player]
    if includePrecollected:
        items.extend(multiworld.precollected_items.get(player, []))
    return items

def reset_specific_item_value_cache_for_player(world: World, value: str, player: Optional[int] = None) -> dict[str, int]:
    if player is None:
        player = world.player
    return world.item_values[player].pop(value, {})

def reset_item_value_cache_for_player(world: World, player: Optional[int] = None):
    if player is None:
        player = world.player
    world.item_values[player] = {}

def get_items_with_value(world: World, multiworld: MultiWorld, value: str, player: Optional[int] = None, skipCache: bool = False) -> dict[str, int]:
    """Return a dict of every items with a specific value type present in their respective 'value' dict\n
    Output in the format 'Item Name': 'value count'\n
    Keep a cache of the result, it can be skipped with 'skipCache == True'\n
    To force a Reset of the player's cache of a value use either reset_specific_item_value_cache_for_player or reset_item_value_cache_for_player
    """
    if player is None:
        player = world.player

    player_items = get_items_for_player(multiworld, player, True)
    # Just a small check to prevent caching {} if items don't exist yet
    if not player_items:
        return {value: -1}

    value = value.lower().strip()

    if not skipCache:
        if not hasattr(world, 'item_values'): #Cache of just the item values
            world.item_values = {}

        if not world.item_values.get(player):
            world.item_values[player] = {}

    if value not in world.item_values.get(player, {}).keys() or skipCache:
        item_with_values = {i.name: world.item_name_to_item[i.name]['value'].get(value, 0)
                            for i in player_items if i.code is not None
                            and i.name in world.item_name_groups.get(f'has_{value}_value', [])}
        if skipCache:
            return item_with_values
        world.item_values[player][value] = item_with_values
    return world.item_values[player].get(value)


def filter_used_regions(player_regions: dict|list) -> set:
    """Return a set of regions that are actually used in Generation. It includes region that have no locations but are required by other regions\n
    The dict version of the player_regions must be in the format: dict(region name str: region)
    """
    used_regions = set()

    if isinstance(player_regions, list):
        player_regions = {r.name: r for r in player_regions}

    #Grab all the player's regions and take note of those with locations
    for region in player_regions.values():
        if region.locations:
            used_regions.add(region)

    #Check every known region with location for parent regions
    checked_parent = []
    for region in set(used_regions):
        def checkParent(parent_region):
            if parent_region.name in checked_parent: #dont check a region twice
                return
            checked_parent.append(parent_region.name)
            used_regions.add(parent_region)
            for entrance in parent_region.entrances:
                if player_regions.get(entrance.parent_region.name):
                    checkParent(entrance.parent_region)
            return
        checkParent(region)
    return used_regions

def convert_to_long_string(input: str | list[str]) -> str:
    """Verify that the input is a str. If it's a list[str] then it combine them into a str in a way that works with yaml template/website options descriptions"""
    if not isinstance(input, str):
        return str.join("\n    ", input)
    return input

def format_to_valid_identifier(input: str) -> str:
    """Make sure the input is a valid python identifier"""
    input = input.strip()
    if input[:1].isdigit():
        input = "_" + input
    return input.replace(" ", "_")

class ProgItemsCat(IntEnum):
    VALUE = 1
    CATEGORY = 2

def format_state_prog_items_key(category: str|ProgItemsCat ,key: str) -> str:
    """Convert the inputted key to the format used in state.has(key) to check/set the count of an item_value.
    Using either one of the predefined categories or a custom string.

    Example: Coin -> MANUAL_VALUE_coin
    """
    if isinstance(category, str):
        cat_key = format_to_valid_identifier(category.upper())
    else:
        cat_key = category.name

    return f"MANUAL_{cat_key}_{format_to_valid_identifier(key.lower())}"

def convert_string_to_type(input: str, target_type: type) -> Any:
    """Take a string and attempt to convert it to {target_type}
    \ntarget_type can be a single type(ex. str), an union (int|str), an Optional type (Optional[str]) or a combo of any of those (Optional[int|str])
    \nSpecial logic:
    - When target_type is Optional or contains None: it will check if input.lower() is "none"
    - When target_type contains bool: it will check if input.lower() is "true", "1", "false" or "0"
    - If bool is the last type in target_type it also run the input directly through bool(input) if previous fails
    \nif you want this to possibly fail without Exceptions include str in target_type, your input should get returned if all the other conversions fails
    """
    def checktype(target_type, found_types: list):
        if issubclass(type(target_type), type): #is it a single type (str, list, etc)
            if target_type not in found_types:
                found_types.append(target_type)

        elif issubclass(type(target_type), GenericAlias): #is it something like list[str] and dict{str:int}
            if target_type not in found_types and get_origin(target_type) not in found_types: #dont add 'dict[str]' if we already search for 'dict'
                found_types.append(target_type)

        elif issubclass(type(target_type), type(str|int)) \
            or issubclass(type(target_type), type(Union[str|int])): #Support both version of Union, and Optional and other alike
            for arg in get_args(target_type):
                checktype(arg, found_types)

        else:
            raise Exception(f"'{value}' cannot be converted to {target_type} since its not a supported type \nAsk about it in #Manual-support and it might be added.")

    found_types = []
    checktype(target_type, found_types)

    if str in found_types: #do it last
        found_types.remove(str)
        found_types.append(str)

    value = input.strip()
    i = 0
    errors = []
    for value_type in found_types:
        i += 1
        if issubclass(value_type, type(None)):
            if value.lower() == 'none':
                return None
            errors.append(str(value_type) + ": value was not 'none'")

        elif issubclass(value_type, bool):
            if value.lower() in ['true', '1', 'on']:
                return True

            elif value.lower() in ['false', '0', 'off']:
                return False

            else:
                if i == len(found_types):
                    return value_type(value) #if its the last type might as well try and convert to bool
                errors.append(str(value_type) + ": value was not in either ['true', '1', 'on'] or ['false', '0', 'off']")

        elif issubclass(value_type, list) or issubclass(value_type, dict) \
            or issubclass(value_type, set) or issubclass(type(value_type), GenericAlias):
            try:
                try:
                    converted_value = ast.literal_eval(value)
                except ValueError as e:
                    # The ValueError from ast when the string cannot be evaluated as a literal is usually something like
                    # "malformed node or string on line 1: <ast.Name object at 0x000001AEBBCC7590>", which is not
                    # helpful, so re-raise with a better exception message.
                    raise ValueError(f"'{value}' could not be evaluated as a literal") from e

                compareto = get_origin(value_type) if issubclass(type(value_type), GenericAlias) else value_type
                if issubclass(compareto, type(converted_value)):
                    return converted_value
                else:
                    errors.append(str(value_type) + f": value '{value}' was not a valid {str(compareto)}")
            except Exception as e:
                errors.append(str(value_type) + ": " + str(e))
                continue
        else:
            try:
                return value_type(value)

            except Exception as e:
                errors.append(str(value_type) + ": " + str(e))
                continue

    newline = "\n"
    raise Exception(f"'{value}' could not be converted to {target_type}, here's the conversion failure message(s):\n\n{newline.join([' - ' + str(validation_error) for validation_error in errors])}\n\n")
