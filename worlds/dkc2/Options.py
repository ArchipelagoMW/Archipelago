from dataclasses import dataclass

from .Items import item_groups

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, PerGameCommonOptions, StartInventoryPool

class StartingLifeCount(Range):
    """
    How many lives to start the game with. 
    Note: This number becomes the new default life count, meaning that it will persist after a game over.
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 99
    default = 5

class StartingKong(Choice):
    """
    Which Kongs will be available at the start
    """
    display_name = "Starting Kong"
    option_diddy = 1
    option_dixie = 2
    option_both = 3
    default = 1

class Logic(Choice):
    """
    Logic difficulty. May become irrelevant if not a lot of items are added to the item pool.
    - **Strict**: Ensures everything is reachable as the original devs intended
    - **Loose**: Reaching locations may require some level of mastery about the game's mechanics
    - **Expert**: Locations expects players to be extremely good at the game with minimal amount of abilities
    """
    display_name = "Logic Difficulty"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    default = 1

class ShuffleLevels(Toggle):
    """
    Shuffles levels and bosses around
    """
    display_name = "Shuffle Levels"

class Goal(Choice):
    """
    Which goal will be used to mark the game as completed
    - **Flying Krock:** Duel with K. Rool at the Flying Krock
    - **Lost World:** Duel with K. Rool at Lost World
    - **Kompletionist:** Duel with K. Rool at both Flying Krock and Lost World
    """
    display_name = "Barrel Kannons Shuffle"
    option_flying_krock = 1
    option_lost_world = 2
    option_kompletionist = 3
    default = 1

class LostWorldRocks(Range):
    """
    How many rocks are required to be found to be able to duel K. Rool at Lost World's Kore
    """
    display_name = "Lost World Rocks"
    range_start = 0
    range_end = 10
    default = 5

class AbilityShuffle(OptionSet):
    """
    Which abilities will be added as items in the item pool
    If an ability is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Ability Shuffle"
    default = {ability for ability in item_groups["Abilities"]}
    valid_keys = {ability for ability in item_groups["Abilities"]}

class AnimalShuffle(OptionSet):
    """
    Which animal buddies will be added as items in the item pool
    If an animal buddy is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Animal Buddies Shuffle"
    default = {ability for ability in item_groups["Animals"]}
    valid_keys = {ability for ability in item_groups["Animals"]}

class BarrelShuffle(OptionSet):
    """
    Which kind of barrels will be added as items in the item pool
    If a barrel is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Barrel Kannons Shuffle"
    default = {ability for ability in item_groups["Barrels"]}
    valid_keys = {ability for ability in item_groups["Barrels"]}

class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0

class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2

class FreezeTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which freezes the controllable kong
    """
    display_name = "Freeze Trap Weight"


class ReverseTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which reverses the player's controls
    """
    display_name = "Reverse Trap Weight"


@dataclass
class DKC2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    starting_life_count: StartingLifeCount
    starting_kong: StartingKong
    goal: Goal
    lost_world_rocks: LostWorldRocks
    logic: Logic
    shuffle_levels: ShuffleLevels
    shuffle_abilities: AbilityShuffle
    shuffle_animals: AnimalShuffle
    shuffle_barrels: BarrelShuffle
    trap_fill_percentage: TrapFillPercentage
    freeze_trap_weight: FreezeTrapWeight
    reverse_trap_weight: ReverseTrapWeight
