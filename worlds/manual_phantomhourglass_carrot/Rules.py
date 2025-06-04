from typing import TYPE_CHECKING, Optional
from worlds.generic.Rules import set_rule
from .Regions import regionMap
from .hooks import Rules
from BaseClasses import MultiWorld, CollectionState
from .Helpers import clamp, is_item_enabled, get_items_with_value, is_option_enabled
from worlds.AutoWorld import World

import re
import math
import inspect
import logging

if TYPE_CHECKING:
    from . import ManualWorld

def infix_to_postfix(expr, location):
    prec = {"&": 2, "|": 2, "!": 3}

    stack = []
    postfix = ""

    try:
        for c in expr:
            if c.isnumeric():
                postfix += c
            elif c in prec:
                while stack and stack[-1] != "(" and prec[c] <= prec[stack[-1]]:
                    postfix += stack.pop()
                stack.append(c)
            elif c == "(":
                stack.append(c)
            elif c == ")":
                while stack and stack[-1] != "(":
                    postfix += stack.pop()
                stack.pop()
        while stack:
            postfix += stack.pop()
    except Exception:
        raise KeyError("Invalid logic format for location/region {}.".format(location))
    return postfix


def evaluate_postfix(expr: str, location: str) -> bool:
    stack = []
    try:
        for c in expr:
            if c == "0":
                stack.append(False)
            elif c == "1":
                stack.append(True)
            elif c == "&":
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(op1 and op2)
            elif c == "|":
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(op1 or op2)
            elif c == "!":
                op = stack.pop()
                stack.append(not op)
    except Exception:
        raise KeyError("Invalid logic format for location/region {}.".format(location))

    if len(stack) != 1:
        raise KeyError("Invalid logic format for location/region {}.".format(location))
    return stack.pop()

def set_rules(world: "ManualWorld", multiworld: MultiWorld, player: int):
    # this is only called when the area (think, location or region) has a "requires" field that is a string
    def checkRequireStringForArea(state: CollectionState, area: dict):
        requires_list = area["requires"]

        # Get the "real" item counts of item in the pool/placed/starting_items
        items_counts = world.get_item_counts(player)

        if requires_list == "":
            return True

        for item in re.findall(r'\{(\w+)\((.*?)\)\}', requires_list):
            func_name = item[0]
            func_args = item[1].split(",")
            if func_args == ['']:
                func_args.pop()

            func = globals().get(func_name)

            if func is None:
                func = getattr(Rules, func_name, None)

            if not callable(func):
                raise ValueError(f"Invalid function `{func_name}` in {area}.")

            convert_req_function_args(func, func_args, area.get("name", f"An area with these parameters: {area}"))
            result = func(world, multiworld, state, player, *func_args)
            if isinstance(result, bool):
                requires_list = requires_list.replace("{" + func_name + "(" + item[1] + ")}", "1" if result else "0")
            else:
                requires_list = requires_list.replace("{" + func_name + "(" + item[1] + ")}", str(result))


        # parse user written statement into list of each item
        for item in re.findall(r'\|[^|]+\|', requires_list):
            require_type = 'item'

            if '|@' in item:
                require_type = 'category'

            item_base = item
            item = item.lstrip('|@$').rstrip('|')

            item_parts = item.split(":")  # type: list[str]
            item_name = item
            item_count = "1"


            if len(item_parts) > 1:
                item_name = item_parts[0].strip()
                item_count = item_parts[1].strip()

            total = 0

            if require_type == 'category':
                category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
                category_items_counts = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
                if item_count.lower() == 'all':
                    item_count = category_items_counts
                elif item_count.lower() == 'half':
                    item_count = int(category_items_counts / 2)
                elif item_count.endswith('%') and len(item_count) > 1:
                    percent = clamp(float(item_count[:-1]) / 100, 0, 1)
                    item_count = math.ceil(category_items_counts * percent)
                else:
                    try:
                        item_count = int(item_count)
                    except ValueError as e:
                        raise ValueError(f"Invalid item count `{item_name}` in {area}.") from e

                for category_item in category_items:
                    total += state.count(category_item["name"], player)

                    if total >= item_count:
                        requires_list = requires_list.replace(item_base, "1")
            elif require_type == 'item':
                item_current_count = items_counts.get(item_name, 0)
                if item_count.lower() == 'all':
                    item_count = item_current_count
                elif item_count.lower() == 'half':
                    item_count = int(item_current_count / 2)
                elif item_count.endswith('%') and len(item_count) > 1:
                    percent = clamp(float(item_count[:-1]) / 100, 0, 1)
                    item_count = math.ceil(item_current_count * percent)
                else:
                    item_count = int(item_count)

                total = state.count(item_name, player)

                if total >= item_count:
                    requires_list = requires_list.replace(item_base, "1")

            if total <= item_count:
                requires_list = requires_list.replace(item_base, "0")

        requires_list = re.sub(r'\s?\bAND\b\s?', '&', requires_list, 0, re.IGNORECASE)
        requires_list = re.sub(r'\s?\bOR\b\s?', '|', requires_list, 0, re.IGNORECASE)

        requires_string = infix_to_postfix("".join(requires_list), area)
        return (evaluate_postfix(requires_string, area))

    # this is only called when the area (think, location or region) has a "requires" field that is a dict
    def checkRequireDictForArea(state: CollectionState, area: dict):
        canAccess = True

        for item in area["requires"]:
            # if the require entry is an object with "or" or a list of items, treat it as a standalone require of its own
            if (isinstance(item, dict) and "or" in item and isinstance(item["or"], list)) or (isinstance(item, list)):
                canAccessOr = True
                or_items = item

                if isinstance(item, dict):
                    or_items = item["or"]

                for or_item in or_items:
                    or_item_parts = or_item.split(":")
                    or_item_name = or_item
                    or_item_count = 1

                    if len(or_item_parts) > 1:
                        or_item_name = or_item_parts[0]
                        or_item_count = int(or_item_parts[1])

                    if not state.has(or_item_name, player, or_item_count):
                        canAccessOr = False

                if canAccessOr:
                    canAccess = True
                    break
            else:
                item_parts = item.split(":")
                item_name = item
                item_count = 1

                if len(item_parts) > 1:
                    item_name = item_parts[0]
                    item_count = int(item_parts[1])

                if not state.has(item_name, player, item_count):
                    canAccess = False

        return canAccess

    # handle any type of checking needed, then ferry the check off to a dedicated method for that check
    def fullLocationOrRegionCheck(state: CollectionState, area: dict):
        # if it's not a usable object of some sort, default to true
        if not area:
            return True

        # don't require the "requires" key for locations and regions if they don't need to use it
        if "requires" not in area.keys():
            return True

        if isinstance(area["requires"], str):
            return checkRequireStringForArea(state, area)
        else:  # item access is in dict form
            return checkRequireDictForArea(state, area)

    used_location_names = []
    # Region access rules
    for region in regionMap.keys():
        used_location_names.extend([l.name for l in multiworld.get_region(region, player).locations])
        if region != "Menu":
            for exitRegion in multiworld.get_region(region, player).exits:
                def fullRegionCheck(state: CollectionState, region=regionMap[region]):
                    return fullLocationOrRegionCheck(state, region)

                set_rule(multiworld.get_entrance(exitRegion.name, player), fullRegionCheck)

    # Location access rules
    for location in world.location_table:
        if location["name"] not in used_location_names:
            continue

        locFromWorld = multiworld.get_location(location["name"], player)

        locationRegion = regionMap[location["region"]] if "region" in location else None

        if "requires" in location: # Location has requires, check them alongside the region requires
            def checkBothLocationAndRegion(state: CollectionState, location=location, region=locationRegion):
                locationCheck = fullLocationOrRegionCheck(state, location)
                regionCheck = True # default to true unless there's a region with requires

                if region:
                    regionCheck = fullLocationOrRegionCheck(state, region)

                return locationCheck and regionCheck

            set_rule(locFromWorld, checkBothLocationAndRegion)
        elif "region" in location: # Only region access required, check the location's region's requires
            def fullRegionCheck(state, region=locationRegion):
                return fullLocationOrRegionCheck(state, region)

            set_rule(locFromWorld, fullRegionCheck)
        else: # No location region and no location requires? It's accessible.
            def allRegionsAccessible(state):
                return True

            set_rule(locFromWorld, allRegionsAccessible)

    # Victory requirement
    multiworld.completion_condition[player] = lambda state: state.has("__Victory__", player)

    def convert_req_function_args(func, args: list[str], areaName: str, warn: bool = False):
        parameters = inspect.signature(func).parameters
        knownArguments = ["world", "multiworld", "state", "player"]
        index = 0
        for parameter, info in parameters.items():
            if parameter in knownArguments:
                continue

            argType = info.annotation
            optional = False
            try:
                if issubclass(argType, inspect._empty): #if not set then it wont get converted but still be checked for valid data at index
                    argType = str

            except TypeError: # Optional
                if argType.__module__ == 'typing' and argType._name == 'Optional':
                    optional = True
                    argType = argType.__args__[0]
                else:
                    #Implementing complex typing is not simple so ill skip it for now
                    index += 1
                    continue

            try:
                value = args[index].strip()

            except IndexError:
                if info is not inspect.Parameter.empty:
                    value = info.default

                else:
                    raise Exception(f"A call of the {func.__name__} function in '{areaName}'s requirement, asks for a value of type {argType}\nfor its argument '{info.name}' but its missing")

            if optional:
                if isinstance(value, type(None)):
                    index += 1
                    continue
                elif isinstance(value, str):
                    if value.lower() == 'none':
                        value = None
                        args[index] = value
                        index += 1
                        continue


            if not isinstance(value, argType):
                if issubclass(argType, bool):
                    #Special conversion to bool
                    if value.lower() in ['true', '1']:
                        value = True

                    elif value.lower() in ['false', '0']:
                        value = False

                    else:
                        value = bool(value)
                        if warn:
                        # warning here spam the console if called from rules.py, might be worth to make it a data validation instead
                            logging.warn(f"A call of the {func.__name__} function in '{areaName}'s requirement, asks for a value of type {argType}\nfor its argument '{info.name}' but an unknown string was passed and thus converted to {value}")

                else:
                    try:
                        value = argType(value)

                    except ValueError:
                        raise Exception(f"A call of the {func.__name__} function in '{areaName}'s requirement, asks for a value of type {argType}\nfor its argument '{info.name}' but its value '{value}' cannot be converted to {argType}")

                args[index] = value

            index += 1

def ItemValue(world: World, multiworld: MultiWorld, state: CollectionState, player: int, valueCount: str, skipCache: bool = False):
    """When passed a string with this format: 'valueName:int',
    this function will check if the player has collect at least 'int' valueName worth of items\n
    eg. {ItemValue(Coins:12)} will check if the player has collect at least 12 coins worth of items\n
    You can add a second string argument to disable creating/checking the cache like this:
    '{ItemValue(Coins:12,Disable)}' it can be any string you want
    """

    valueCount = valueCount.split(":")
    if not len(valueCount) == 2 or not valueCount[1].isnumeric():
        raise Exception(f"ItemValue needs a number after : so it looks something like 'ItemValue({valueCount[0]}:12)'")
    value_name = valueCount[0].lower().strip()
    requested_count = int(valueCount[1].strip())

    if not hasattr(world, 'item_values_cache'): #Cache made for optimization purposes
        world.item_values_cache = {}

    if not world.item_values_cache.get(player, {}):
        world.item_values_cache[player] = {}

    if not skipCache:
        if not world.item_values_cache[player].get(value_name, {}):
            world.item_values_cache[player][value_name] = {
                'state': {},
                'count': -1,
                }

    if (skipCache or world.item_values_cache[player][value_name].get('count', -1) == -1
            or world.item_values_cache[player][value_name].get('state') != dict(state.prog_items[player])):
        # Run First Time, if state changed since last check or if skipCache has a value
        existing_item_values = get_items_with_value(world, multiworld, value_name)
        total_Count = 0
        for name, value in existing_item_values.items():
            count = state.count(name, player)
            if count > 0:
                total_Count += count * value
        if skipCache:
            return total_Count >= requested_count
        world.item_values_cache[player][value_name]['count'] = total_Count
        world.item_values_cache[player][value_name]['state'] = dict(state.prog_items[player])
    return world.item_values_cache[player][value_name]['count'] >= requested_count

# Two useful functions to make require work if an item is disabled instead of making it inaccessible
def OptOne(world: World, multiworld: MultiWorld, state: CollectionState, player: int, item: str, items_counts: Optional[dict] = None):
    """Check if the passed item (with or without ||) is enabled, then this returns |item:count|
    where count is clamped to the maximum number of said item in the itempool.\n
    Eg. requires: "{OptOne(|DisabledItem|)} and |other items|" become "|DisabledItem:0| and |other items|" if the item is disabled.
    """
    if item == "":
        return "" #Skip this function if item is left blank
    if not items_counts:
        items_counts = world.get_item_counts()

    require_type = 'item'

    if '@' in item[:2]:
        require_type = 'category'

    item = item.lstrip('|@$').rstrip('|')

    item_parts = item.split(":")
    item_name = item
    item_count = '1'

    if len(item_parts) > 1:
        item_name = item_parts[0]
        item_count = item_parts[1]

    if require_type == 'category':
        if item_count.isnumeric():
            #Only loop if we can use the result to clamp
            category_items = [item for item in world.item_name_to_item.values() if "category" in item and item_name in item["category"]]
            category_items_counts = sum([items_counts.get(category_item["name"], 0) for category_item in category_items])
            item_count = clamp(int(item_count), 0, category_items_counts)
        return f"|@{item_name}:{item_count}|"
    elif require_type == 'item':
        if item_count.isnumeric():
            item_current_count = items_counts.get(item_name, 0)
            item_count = clamp(int(item_count), 0, item_current_count)
        return f"|{item_name}:{item_count}|"

# OptAll check the passed require string and loop every item to check if they're enabled,
def OptAll(world: World, multiworld: MultiWorld, state: CollectionState, player: int, requires: str):
    """Check the passed require string and loop every item to check if they're enabled,
    then returns the require string with items counts adjusted using OptOne\n
    eg. requires: "{OptAll(|DisabledItem| and |@CategoryWithModifedCount:10|)} and |other items|"
    become "|DisabledItem:0| and |@CategoryWithModifedCount:2| and |other items|" """
    requires_list = requires

    items_counts = world.get_item_counts()

    functions = {}
    if requires_list == "":
        return True
    for item in re.findall(r'\{(\w+)\(([^)]*)\)\}', requires_list):
        #so this function doesn't try to get item from other functions, in theory.
        func_name = item[0]
        functions[func_name] = item[1]
        requires_list = requires_list.replace("{" + func_name + "(" + item[1] + ")}", "{" + func_name + "(temp)}")
    # parse user written statement into list of each item
    for item in re.findall(r'\|[^|]+\|', requires):
        itemScanned = OptOne(world, multiworld, state, player, item, items_counts)
        requires_list = requires_list.replace(item, itemScanned)

    for function in functions:
        requires_list = requires_list.replace("{" + function + "(temp)}", "{" + func_name + "(" + functions[func_name] + ")}")
    return requires_list

# Rule to expose the can_reach_location core function
def canReachLocation(world: World, multiworld: MultiWorld, state: CollectionState, player: int, location: str):
    """Can the player reach the given location?"""
    if state.can_reach_location(location, player):
        return True
    return False

def YamlEnabled(world: "ManualWorld", multiworld: MultiWorld, state: CollectionState, player: int, param: str) -> bool:
    """Is a yaml option enabled?"""
    return is_option_enabled(multiworld, player, param)

def YamlDisabled(world: "ManualWorld", multiworld: MultiWorld, state: CollectionState, player: int, param: str) -> bool:
    """Is a yaml option disabled?"""
    return not is_option_enabled(multiworld, player, param)
