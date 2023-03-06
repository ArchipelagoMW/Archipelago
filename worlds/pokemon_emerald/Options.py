from BaseClasses import MultiWorld
from typing import Dict, List, Union
from Options import Option, Choice, DefaultOnToggle, Range, Toggle

class RandomizeBadges(DefaultOnToggle):
    """Adds Badges to the pool"""
    display_name = "Randomize Badges"

class RandomizeHms(DefaultOnToggle):
    """Adds HMs to the pool"""
    display_name = "Randomize HMs"

class RandomizeKeyItems(Toggle):
    """Adds most key items to the pool. These are usually required to unlock
    a location or region (e.g. Devon Scope, Letter, Basement Key)"""
    display_name = "Randomize Key Items"

class RandomizeRods(Toggle):
    """Adds fishing rods to the pool"""
    display_name = "Randomize Fishing Rods"

class RandomizeOverworldItems(DefaultOnToggle):
    """Adds items on the ground with a Pokeball sprite to the pool"""
    display_name = "Randomize Overworld Items"

class RandomizeHiddenItems(Toggle):
    """Adds hidden items to the pool"""
    display_name = "Randomize Hidden Items"

class RandomizeNpcGifts(Toggle):
    """Adds most gifts received from NPCs to the pool (not including key items or HMs)"""
    display_name = "Randomize NPC Gifts"

class HiddenItemsRequireItemfinder(DefaultOnToggle):
    """The Itemfinder is logically required to pick up hidden items"""
    display_name = "Require Itemfinder"

class RandomizeWildPokemon(Choice):
    """Randomizes the starter pokemon in Professor Birch's bag
    Vanilla: Starters are unchanged
    Completely Random: There are no restrictions"""
    default = 0
    option_vanilla = 0
    option_completely_random = 1

class RandomizeStarters(Choice):
    """Randomizes the starter pokemon in Professor Birch's bag
    Vanilla: Starters are unchanged
    Completely Random: There are no restrictions"""
    default = 0
    option_vanilla = 0
    option_completely_random = 1

class ExpModifier(Range):
    """Multiplies gained experience by a percentage
    100 is default
    50 is half
    200 is double
    etc..."""
    display_name = "Exp Modifier"
    range_start = 50
    range_end = 10000
    default = 100

class BlindTrainers(Toggle):
    """Causes trainers to not start a battle with you unless you talk to them"""
    display_name = "Blind Trainers"

class EnableFerry(Toggle):
    """The ferry between Slateport, Lilycove, and the Battle Frontier can be used if you have the S.S. Ticket"""
    display_name = "Enable Ferry"

options: Dict[str, Option] = {
  "badges": RandomizeBadges,
  "hms": RandomizeHms,
  "key_items": RandomizeKeyItems,
  "rods": RandomizeRods,
  "overworld_items": RandomizeOverworldItems,
  "hidden_items": RandomizeHiddenItems,
  "npc_gifts": RandomizeNpcGifts,
  "require_itemfinder": HiddenItemsRequireItemfinder,
  "wild_pokemon": RandomizeWildPokemon,
  "starters": RandomizeStarters,
  "exp_modifier": ExpModifier,
  "blind_trainers": BlindTrainers,
  "enable_ferry": EnableFerry
}

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
