from BaseClasses import MultiWorld
from typing import Dict, List, Union
from Options import Option, Choice, DefaultOnToggle, Range, Toggle

class RandomizeBadges(Choice):
    """Adds Badges to the pool
    Vanilla: Gym leaders give their own badge
    Shuffle: Gym leaders give a random badge
    Completely Random: Badges can be found anywhere"""
    display_name = "Randomize Badges"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2

class RandomizeHms(Choice):
    """Adds HMs to the pool
    Vanilla: HMs are at their vanilla locations
    Shuffle: HMs are shuffled among vanilla HM locations
    Completely Random: HMs can be found anywhere"""
    display_name = "Randomize HMs"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2

class RandomizeKeyItems(Toggle):
    """Adds most key items to the pool. These are usually required to unlock
    a location or region (e.g. Devon Scope, Letter, Basement Key)"""
    display_name = "Randomize Key Items"

class RandomizeBikes(Toggle):
    """Adds the mach bike and acro bike to the pool"""
    display_name = "Randomize Bikes"

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

class DarkCavesRequireFlash(DefaultOnToggle):
    """The lower floors of Granite Cave and Victory Road logically require use of HM05 Flash"""
    display_name = "Require Flash"

class RandomizeWildPokemon(Choice):
    """Randomizes wild pokemon encounters (grass, caves, water, fishing)
    Vanilla: Wild encounters are unchanged
    Match Base Stats: Wild pokemon are replaced with species with approximately the same bst
    Completely Random: There are no restrictions"""
    display_name = "Randomize Wild Pokemon"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_completely_random = 2

class RandomizeStarters(Choice):
    """Randomizes the starter pokemon in Professor Birch's bag
    Vanilla: Starters are unchanged
    Match Base Stats: Starters are replaced with species with approximately the same bst
    Completely Random: There are no restrictions"""
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_completely_random = 2

class MinCatchRate(Range):
    """Sets the minimum catch rate a pokemon can have. Any pokemon with a catch rate below this floor will have it raised to this value.
    Legendaries are often in the single digits
    Fully evolved pokemon are often double digits
    Pidgey is 255"""
    display_name = "Minimum Catch Rate"
    range_start = 3
    range_end = 255
    default = 3

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

class LevelUpMoves(Choice):
    """Randomizes the moves a pokemon learns when they reach a level where they would learn a move. Your starter is guaranteed to have a move with which it can gain experience.
    Vanilla: Learnset is unchanged
    Randomized: Moves are randomized
    Start with Four Moves: Moves are randomized and all Pokemon have 4 starting moves"""
    display_name = "Level Up Moves"
    default = 0
    option_vanilla = 0
    option_randomized = 1
    option_start_with_four_moves = 2

class TmCompatibility(Choice):
    """Modifies the compatability of TMs with species
    Vanilla: Compatibility is unchanged
    Fully Compatible: Every species can learn any TM
    Completely Random: Compatibility is 50/50 for every TM (does not remain consistent across evolution)"""
    display_name = "TM Compatibility"
    default = 0
    option_vanilla = 0
    option_fully_compatible = 1
    option_completely_random = 2

class HmCompatibility(Choice):
    """Modifies the compatability of HMs with species
    Vanilla: Compatibility is unchanged
    Fully Compatible: Every species can learn any HM
    Completely Random: Compatibility is 50/50 for every HM (does not remain consistent across evolution)"""
    display_name = "HM Compatibility"
    default = 0
    option_vanilla = 0
    option_fully_compatible = 1
    option_completely_random = 2

class EnableFerry(Toggle):
    """The ferry between Slateport, Lilycove, and the Battle Frontier can be used if you have the S.S. Ticket"""
    display_name = "Enable Ferry"

class TurboA(Toggle):
    """Holding A will advance most text automatically"""
    display_name = "Turbo A"

options: Dict[str, Option] = {
  "badges": RandomizeBadges,
  "hms": RandomizeHms,
  "key_items": RandomizeKeyItems,
  "bikes": RandomizeBikes,
  "rods": RandomizeRods,
  "overworld_items": RandomizeOverworldItems,
  "hidden_items": RandomizeHiddenItems,
  "npc_gifts": RandomizeNpcGifts,
  "require_itemfinder": HiddenItemsRequireItemfinder,
  "require_flash": DarkCavesRequireFlash,
  "wild_pokemon": RandomizeWildPokemon,
  "starters": RandomizeStarters,
  "min_catch_rate": MinCatchRate,
  "exp_modifier": ExpModifier,
  "blind_trainers": BlindTrainers,
  "level_up_moves": LevelUpMoves,
  "tm_compatibility": TmCompatibility,
  "hm_compatibility": HmCompatibility,
  "enable_ferry": EnableFerry,
  "turbo_a": TurboA
}

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
