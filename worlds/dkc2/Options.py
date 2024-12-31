from dataclasses import dataclass

from .Items import item_groups
from .data.Trivia import trivia_data

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, PerGameCommonOptions, StartInventoryPool, DeathLink, Visibility

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
    - **Strict**: Ensures everything is reachable as the original devs intended. For beginners or people who want to go out of logic with some tricks.
    - **Loose**: Reaching locations may require some level of mastery about the game's mechanics.
    - **Expert**: Locations expects players to be extremely good at the game with minimal amount of abilities. Hard to go out of logic.
    """
    display_name = "Logic Difficulty"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    default = 0

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
    display_name = "Goal"
    option_flying_krock = 1
    option_lost_world = 2
    option_kompletionist = 3
    default = 1

class FlyingKrockTokens(Range):
    """
    How many Boss Tokens are required to access the Flying Krock.

    If this value is set to 0, then the access will be a multiworld item.
    """
    display_name = "Flying Krock Tokens"
    range_start = 0
    range_end = 5
    default = 5

class LostWorldRocks(Range):
    """
    How many rocks are required to be found to be able to duel K. Rool at Lost World's Kore
    """
    display_name = "Lost World Rocks"
    range_start = 1
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

class KONGChecks(DefaultOnToggle):
    """
    Whether collecting all KONG letters in each level will grant a check
    """
    display_name = "KONG Letters Checks"

class DKCoinChecks(DefaultOnToggle):
    """
    Whether collecting a DK Coin in each level will grant a check
    """
    display_name = "DK Coin Checks"

class SwankyChecks(DefaultOnToggle):
    """
    Whether completing a quiz will grant a check
    """
    display_name = "Swanky Quiz Checks"

class SwankyQuestionsPerQuiz(Range):
    """
    Whether completing a quiz will grant a check
    """
    display_name = "Swanky Questions Per Quiz"
    range_start = 1
    range_end = 10
    default = 3

class SwankyExcludeTopics(OptionSet):
    """
    Which topics will be excluded from Swanky's Bonus Bonanza pool of questions.

    Swanky enforces questions from the multiworld. This will help you to remove topics from games you don't know/care about in the session.
    Donkey Kong Country 2 can't be excluded (can be put here, but it'll be forced anyway)

    Do note that if you remove way too many topics and set a very high question per quiz count an error may arise from the lack of questions available
    """
    display_name = "Swanky Excluded Topics"
    default = {topic for topic in trivia_data.keys()}
    valid_keys = {topic for topic in trivia_data.keys()}

class SwankyForceTopics(OptionSet):
    """
    Which additional topics will be added to Swanky's Bonus Bonanza pool of questions.

    Swanky already enforces questions from games in the multiworld if they're on the database.

    This option has priority over the Excluded Topics option.
    """
    display_name = "Swanky Forced Topics"
    default = {topic for topic in trivia_data.keys()}
    valid_keys = {topic for topic in trivia_data.keys()}

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

class DamageTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which damages the player
    """
    display_name = "Damage Trap Weight"
    visibility = Visibility.spoiler | Visibility.complex_ui | Visibility.template
    default = 0

class InstaDeathTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which instantly kills the player
    """
    display_name = "Instant Death Trap Weight"
    visibility = Visibility.spoiler | Visibility.complex_ui | Visibility.template
    default = 0

dkc2_option_groups = [
    OptionGroup("Goal", [
        Goal,
        FlyingKrockTokens,
        LostWorldRocks,
    ]),
    OptionGroup("Locations", [
        Logic,
        KONGChecks,
        DKCoinChecks,
        SwankyChecks,
    ]),
    OptionGroup("Shuffle", [
        StartingKong,
        ShuffleLevels,
        AbilityShuffle,
        AnimalShuffle,
        BarrelShuffle,
    ]),
    OptionGroup("Trivia", [
        SwankyQuestionsPerQuiz,
        SwankyForceTopics,
        SwankyExcludeTopics,
    ]),
    OptionGroup("Traps", [
        TrapFillPercentage,
        FreezeTrapWeight,
        ReverseTrapWeight,
        DamageTrapWeight,
        InstaDeathTrapWeight,
    ]),
]

@dataclass
class DKC2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    starting_life_count: StartingLifeCount
    starting_kong: StartingKong
    goal: Goal
    krock_boss_tokens: FlyingKrockTokens
    lost_world_rocks: LostWorldRocks
    logic: Logic
    shuffle_levels: ShuffleLevels
    shuffle_abilities: AbilityShuffle
    shuffle_animals: AnimalShuffle
    shuffle_barrels: BarrelShuffle
    kong_checks: KONGChecks
    dk_coin_checks: DKCoinChecks
    swanky_checks: SwankyChecks
    swanky_questions_per_quiz: SwankyQuestionsPerQuiz
    swanky_forced_topics: SwankyForceTopics
    swanky_excluded_topics: SwankyExcludeTopics
    trap_fill_percentage: TrapFillPercentage
    freeze_trap_weight: FreezeTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    damage_trap_weight: DamageTrapWeight
    insta_death_trap_weight: InstaDeathTrapWeight
