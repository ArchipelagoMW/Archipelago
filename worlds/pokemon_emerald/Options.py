from BaseClasses import MultiWorld
from typing import Dict, List, Union
from Options import Option, Choice, DefaultOnToggle, Range, Toggle

class Badges(DefaultOnToggle):
    """Adds Badges to the pool"""
    display_name = "Randomize Badges"

class HMs(DefaultOnToggle):
    """Adds HMs to the pool"""
    display_name = "Randomize HMs"

class KeyItems(Toggle):
    """Adds most key items to the pool. These are usually required to unlock
    a location or region (e.g. Devon Scope, Letter, Basement Key)"""
    display_name = "Randomize Key Items"

class Rods(Toggle):
    """Adds fishing rods to the pool"""
    display_name = "Randomize Fishing Rods"

class OverworldItems(DefaultOnToggle):
    """Adds items on the ground with a Pokeball sprite to the pool"""
    display_name = "Randomize Overworld Items"

class HiddenItems(Toggle):
    """Adds hidden items to the pool"""
    display_name = "Randomize Hidden Items"

class NpcGifts(Toggle):
    """Adds most gifts received from NPCs to the pool (not including key items or HMs)"""
    display_name = "Randomize NPC Gifts"

class HiddenItemsRequireItemfinder(DefaultOnToggle):
    """The Itemfinder is logically required to pick up hidden items"""
    display_name = "Require Itemfinder"

class ExpMultiplier(Range):
    """Modifies gained experience by a percentage
    100 is default
    50 is half
    200 is double
    etc..."""
    display_name = "Exp Multiplier"
    range_start = 50
    range_end = 10000
    default = 100

options: Dict[str, Option] = {
  "badges": Badges,
  "hms": HMs,
  "key_items": KeyItems,
  "rods": Rods,
  "overworld_items": OverworldItems,
  "hidden_items": HiddenItems,
  "npc_gifts": NpcGifts,
  "require_itemfinder": HiddenItemsRequireItemfinder,
  "exp_multiplier": ExpMultiplier
}

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
