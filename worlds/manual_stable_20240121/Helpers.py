from BaseClasses import MultiWorld
from .Data import category_table
from .hooks.Helpers import before_is_category_enabled

from typing import Union

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(world, name, None)
    if option is None:
        return 0

    return option[player].value

def is_category_enabled(world: MultiWorld, player: int, category_name: str) -> bool:
    """Check if a category has been disabled by a yaml option."""
    hook_result = before_is_category_enabled(world, player, category_name)
    if hook_result is not None:
        return hook_result

    category_data = category_table.get(category_name, {})
    if "yaml_option" in category_data:
        for option_name in category_data["yaml_option"]:
            if not is_option_enabled(world, player, option_name):
                return False
    return True
