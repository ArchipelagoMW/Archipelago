"""
Option definitions for Pokemon Emerald
"""
from typing import Dict, List, Union
from BaseClasses import MultiWorld
from Options import Option, Choice, DefaultOnToggle, Range, Toggle, OptionList

from .data import data


class RandomizeBadges(Choice):
    """
    Adds Badges to the pool
    Vanilla: Gym leaders give their own badge
    Shuffle: Gym leaders give a random badge
    Completely Random: Badges can be found anywhere
    """
    display_name = "Randomize Badges"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeHms(Choice):
    """
    Adds HMs to the pool
    Vanilla: HMs are at their vanilla locations
    Shuffle: HMs are shuffled among vanilla HM locations
    Completely Random: HMs can be found anywhere
    """
    display_name = "Randomize HMs"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeKeyItems(Toggle):
    """
    Adds most key items to the pool. These are usually required to unlock
    a location or region (e.g. Devon Scope, Letter, Basement Key)
    """
    display_name = "Randomize Key Items"


class RandomizeBikes(Toggle):
    """
    Adds the mach bike and acro bike to the pool
    """
    display_name = "Randomize Bikes"


class RandomizeRods(Toggle):
    """
    Adds fishing rods to the pool
    """
    display_name = "Randomize Fishing Rods"


class RandomizeOverworldItems(DefaultOnToggle):
    """
    Adds items on the ground with a Pokeball sprite to the pool
    """
    display_name = "Randomize Overworld Items"


class RandomizeHiddenItems(Toggle):
    """
    Adds hidden items to the pool
    """
    display_name = "Randomize Hidden Items"


class RandomizeNpcGifts(Toggle):
    """
    Adds most gifts received from NPCs to the pool (not including key items or HMs)
    """
    display_name = "Randomize NPC Gifts"


class ItemPoolType(Choice):
    """
    Determines which non-progression items get put into the item pool
    Shuffled: Randomized items are removed from their default locations and added to the pool
    Diverse: Randomized items are replaced by any non-unique item
    Diverse Exclude Berries: Diverse, but no berries are added, even if a berry would have been shuffled
    """
    display_name = "Item Pool Type"
    default = 0
    option_shuffled = 0
    option_diverse = 1
    option_diverse_exclude_berries = 2


class HiddenItemsRequireItemfinder(DefaultOnToggle):
    """
    The Itemfinder is logically required to pick up hidden items
    """
    display_name = "Require Itemfinder"


class DarkCavesRequireFlash(DefaultOnToggle):
    """
    The lower floors of Granite Cave and Victory Road logically require use of HM05 Flash
    """
    display_name = "Require Flash"


class RandomizeWildPokemon(Choice):
    """
    Randomizes wild pokemon encounters (grass, caves, water, fishing)
    Vanilla: Wild encounters are unchanged
    Match Base Stats: Wild pokemon are replaced with species with approximately the same bst
    Match Type: Wild pokemon are replaced with species that share a type with the original
    Match Base Stats and Type: Apply both Match Base Stats and Match Type
    Completely Random: There are no restrictions
    """
    display_name = "Randomize Wild Pokemon"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class RandomizeStarters(Choice):
    """
    Randomizes the starter pokemon in Professor Birch's bag
    Vanilla: Starters are unchanged
    Match Base Stats: Starters are replaced with species with approximately the same bst
    Match Type: Starters are replaced with species that share a type with the original
    Match Base Stats and Type: Apply both Match Base Stats and Match Type
    Completely Random: There are no restrictions
    """
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class RandomizeTrainerParties(Choice):
    """
    Randomizes the parties of all trainers
    Vanilla: Parties are unchanged
    Match Base Stats: Trainer pokemon are replaced with species with approximately the same bst
    Match Type: Trainer pokemon are replaced with species that share a type with the original
    Match Base Stats and Type: Apply both Match Base Stats and Match Type
    Completely Random: There are no restrictions
    """
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class RandomizeAbilities(Toggle):
    """
    Randomizes the abilities of every pokemon (each species will have the same number of abilities)
    """
    display_name = "Randomize Abilities"


class AbilityBlacklist(OptionList):
    """
    A list of abilities which no pokemon should have if abilities are randomized. For example, you could exclude Wonder Guard and Pressure like this:
    ["Wonder Guard", Pressure]
    """
    display_name = "Ability Blacklist"
    valid_keys = frozenset([ability.label for ability in data.abilities])


class MinCatchRate(Range):
    """
    Sets the minimum catch rate a pokemon can have. Any pokemon with a catch rate below this floor will have it raised to this value.
    Legendaries are often in the single digits
    Fully evolved pokemon are often double digits
    Pidgey is 255
    """
    display_name = "Minimum Catch Rate"
    range_start = 3
    range_end = 255
    default = 3


class ExpModifier(Range):
    """
    Multiplies gained experience by a percentage
    100 is default
    50 is half
    200 is double
    etc...
    """
    display_name = "Exp Modifier"
    range_start = 50
    range_end = 10000
    default = 100


class BlindTrainers(Toggle):
    """
    Causes trainers to not start a battle with you unless you talk to them
    """
    display_name = "Blind Trainers"


class LevelUpMoves(Choice):
    """
    Randomizes the moves a pokemon learns when they reach a level where they would learn a move. Your starter is guaranteed to have a move with which it can gain experience.
    Vanilla: Learnset is unchanged
    Randomized: Moves are randomized
    Start with Four Moves: Moves are randomized and all Pokemon have 4 starting moves
    """
    display_name = "Level Up Moves"
    default = 0
    option_vanilla = 0
    option_randomized = 1
    option_start_with_four_moves = 2


class TmCompatibility(Choice):
    """
    Modifies the compatability of TMs with species
    Vanilla: Compatibility is unchanged
    Fully Compatible: Every species can learn any TM
    Completely Random: Compatibility is 50/50 for every TM (does not remain consistent across evolution)
    """
    display_name = "TM Compatibility"
    default = 0
    option_vanilla = 0
    option_fully_compatible = 1
    option_completely_random = 2


class HmCompatibility(Choice):
    """
    Modifies the compatability of HMs with species
    Vanilla: Compatibility is unchanged
    Fully Compatible: Every species can learn any HM
    Completely Random: Compatibility is 50/50 for every HM (does not remain consistent across evolution)
    """
    display_name = "HM Compatibility"
    default = 1
    option_vanilla = 0
    option_fully_compatible = 1
    option_completely_random = 2


class EnableFerry(Toggle):
    """
    The ferry between Slateport, Lilycove, and the Battle Frontier can be used if you have the S.S. Ticket
    """
    display_name = "Enable Ferry"


class TurboA(Toggle):
    """
    Holding A will advance most text automatically
    """
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
  "item_pool_type": ItemPoolType,
  "require_itemfinder": HiddenItemsRequireItemfinder,
  "require_flash": DarkCavesRequireFlash,
  "wild_pokemon": RandomizeWildPokemon,
  "starters": RandomizeStarters,
  "trainer_parties": RandomizeTrainerParties,
  "abilities": RandomizeAbilities,
  "ability_blacklist": AbilityBlacklist,
  "min_catch_rate": MinCatchRate,
  "exp_modifier": ExpModifier,
  "blind_trainers": BlindTrainers,
  "level_up_moves": LevelUpMoves,
  "tm_compatibility": TmCompatibility,
  "hm_compatibility": HmCompatibility,
  "enable_ferry": EnableFerry,
  "turbo_a": TurboA
}


def get_option_value(multiworld: MultiWorld, player: int, option_name: str) -> Union[int, Dict, List]:
    """
    Returns the option value for a player in a multiworld
    """
    option = getattr(multiworld, option_name, None)
    if option is None:
        return options[option_name].default

    return option[player].value
