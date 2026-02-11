from BaseClasses import MultiWorld, Item
from typing import Optional, List
from worlds.AutoWorld import World
from .Data import category_table
from .Items import ManualItem
from .Locations import ManualLocation
from .hooks.Helpers import before_is_category_enabled, before_is_item_enabled, before_is_location_enabled

from typing import Union

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
    """Check if a category has been disabled by a yaml option."""
    hook_result = before_is_category_enabled(multiworld, player, category_name)
    if hook_result is not None:
        return hook_result

    category_data = category_table.get(category_name, {})
    if "yaml_option" in category_data:
        for option_name in category_data["yaml_option"]:
            required = True
            if option_name.startswith("!"):
                option_name = option_name[1:]
                required = False

            if is_option_enabled(multiworld, player, option_name) != required:
                return False
    return True

def is_item_name_enabled(multiworld: MultiWorld, player: int, item_name: str) -> bool:
    """Check if an item named 'item_name' has been disabled by a yaml option."""
    item = multiworld.worlds[player].item_name_to_item.get(item_name, {})
    if not item:
        return False

    return is_item_enabled(multiworld, player, item)

def is_item_enabled(multiworld: MultiWorld, player: int, item: ManualItem) -> bool:
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

def is_location_enabled(multiworld: MultiWorld, player: int, location: ManualLocation) -> bool:
    """Check if a location has been disabled by a yaml option."""
    hook_result = before_is_location_enabled(multiworld, player, location)
    if hook_result is not None:
        return hook_result

    return _is_manualobject_enabled(multiworld, player, location)

def _is_manualobject_enabled(multiworld: MultiWorld, player: int, object: any) -> bool:
    """Internal method: Check if a Manual Object has any category disabled by a yaml option.
    \nPlease use the proper is_'item/location'_enabled or is_'item/location'_name_enabled methods instead.
    """
    enabled = True
    for category in object.get("category", []):
        if not is_category_enabled(multiworld, player, category):
            enabled = False
            break

    return enabled

def get_items_for_player(multiworld: MultiWorld, player: int) -> List[Item]:
    """Return list of items of a player including placed items"""
    return [i for i in multiworld.get_items() if i.player == player]

def get_items_with_value(world: World, multiworld: MultiWorld, value: str, player: Optional[int] = None, force: bool = False) -> dict[str, int]:
    """Return a dict of every items with a specific value type present in their respective 'value' dict\n
    Output in the format 'Item Name': 'value count'\n
    Keep a cache of the result and wont redo unless 'force == True'
    """
    if player is None:
        player = world.player

    player_items = get_items_for_player(multiworld, player)
    # Just a small check to prevent caching {} if items don't exist yet
    if not player_items:
        return {value: -1}

    value = value.lower().strip()

    if not hasattr(world, 'item_values'): #Cache of just the item values
        world.item_values = {}

    if not world.item_values.get(player):
        world.item_values[player] = {}

    if value not in world.item_values.get(player, {}).keys() or force:
        item_with_values = {i.name: world.item_name_to_item[i.name]['value'].get(value, 0)
                            for i in player_items if i.code is not None
                            and i.name in world.item_name_groups.get(f'has_{value}_value', [])}
        world.item_values[player][value] = item_with_values
    return world.item_values[player].get(value)
