from BaseClasses import MultiWorld
from typing import Dict, List, Union
from Options import Option, Choice, DefaultOnToggle, Range, Toggle

class Badges(Choice):
    """Sets where badges can be found
    Vanilla: Gym leaders give their own badges
    Shuffle: Gym leaders give a random badge
    Badgesanity: Badges can be anywhere"""
    display_name = "Badges"
    option_vanilla = 0
    option_shuffle = 1
    option_badgesanity = 2

class HMs(Choice):
    """Sets where HMs can be found
    Vanilla: HMs are at their vanilla locations
    Shuffle: HMs are shuffled between locations you would normally find an HM
    Fully Random: HMs can be anywhere"""
    display_name = "Badges"
    option_vanilla = 0
    option_shuffle = 1
    option_fully_random = 2

class KeyItems(Toggle):
    """Adds many key items to the pool. These are categorized by whether locations
    or regions logically require them to get to (e.g. Devon Scope, Letter, Devon Goods)"""
    display_name = "Key Items"

class Rods(Toggle):
    """Adds fishing rods to the pool"""
    display_name = "Fishing Rods"

class Items(DefaultOnToggle):
    """Adds items on the ground with a Pokeball sprite to the pool"""
    display_name = "Overworld Items"

class HiddenItems(Toggle):
    """Adds hidden items to the pool"""
    display_name = "Hidden Items"

class NpcGifts(Toggle):
    """Adds most gifts received from NPCs to the pool"""
    display_name = "NPC Gifts"

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
  "Badges": Badges,
  "HMs": HMs,
  "KeyItems": KeyItems,
  "Items": Items,
  "HiddenItems": HiddenItems,
  "NpcGifts": NpcGifts,
  "ExpMultiplier": ExpMultiplier
}

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
