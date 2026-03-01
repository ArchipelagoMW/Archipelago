from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Choice, Range


class Dexsanity(Toggle):
    """If enabled, each Pokemon has its own location check ('Guess {Pokemon}') and requires
    a '{Pokemon} Unlock' item to be received before it can be guessed. Disabling this removes
    all per-Pokemon locations and Unlock items, leaving only milestone-based progression.
    Disabling dramatically reduces generation time and item pool size."""
    display_name = "Dexsanity"
    default = 1


class EnableTypeLocks(Toggle):
    """If true, guessing a Pokémon requires both its specific unlock item and its elemental Type Key."""
    display_name = "Enable Type Locks"
    default = 1


class PokemonGenerations(Choice):
    """Select how many generations of Pokémon to include in the randomizer.
    Gen 1 (Kanto) = 151
    Gen 2 (Johto) = 251 
    Gen 3 (Hoenn) = 386
    Gen 4 (Sinnoh) = 493
    Gen 5 (Unova) = 649
    Gen 6 (Kalos) = 721
    Gen 7 (Alola) = 809
    Gen 8 (Galar) = 898
    Gen 9 (Paldea) = 1025"""
    display_name = "Pokemon Generations"
    option_gen1 = 0
    option_gen2 = 1
    option_gen3 = 2
    option_gen4 = 3
    option_gen5 = 4
    option_gen6 = 5
    option_gen7 = 6
    option_gen8 = 7
    option_gen9 = 8
    default = 0


class StartingPokemon(Choice):
    """(Deprecated) This option is currently ignored as all three starters are provided by default."""
    display_name = "Starting Pokémon (Legacy)"
    option_bulbasaur = 0
    option_charmander = 1
    option_squirtle = 2
    default = 0


class GoalType(Choice):
    """How the goal is defined.
    Percentage: guess a percentage of the selected generation (see 'Goal Percentage').
    Count: guess a fixed number of Pokémon (see 'Goal Count')."""
    display_name = "Goal Type"
    option_percentage = 0
    option_count = 1
    default = 0


class GoalPercentage(Range):
    """Percentage of the selected generation that must be guessed to complete the game.
    Only used when 'Goal Type' is set to 'percentage'.
    For example, 100 means guess every Pokémon in the selected generation."""
    display_name = "Goal Percentage"
    range_start = 1
    range_end = 100
    default = 100


class GoalCount(Range):
    """Fixed number of Pokémon that must be guessed to complete the game.
    Only used when 'Goal Type' is set to 'count'.
    Automatically capped to the total Pokémon available in the selected generation."""
    display_name = "Goal Count"
    range_start = 1
    range_end = 1025
    default = 151


class TrapChance(Range):
    """Percentage chance (0-100) that a filler item slot will be replaced by a trap item.
    0 means no traps; 100 means all filler items will be traps."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 25


@dataclass
class PokepelagoOptions(PerGameCommonOptions):
    dexsanity: Dexsanity
    pokemon_generations: PokemonGenerations
    type_locks: EnableTypeLocks
    starting_pokemon: StartingPokemon
    goal_type: GoalType
    goal_percentage: GoalPercentage
    goal_count: GoalCount
    trap_chance: TrapChance