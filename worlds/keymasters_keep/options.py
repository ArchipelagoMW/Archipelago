import typing

from dataclasses import dataclass

from Options import (
    Choice,
    DefaultOnToggle,
    OptionGroup,
    OptionList,
    OptionSet,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
)

from .game import AutoGameRegister
from .games import GameArchipelagoOptions


class Goal(Choice):
    """
    Determines the victory condition.

    Keymasters Challenge: Retrieve X artifacts of resolve to unlock the Keymaster's challenge chamber and beat the ultimate challenge
    Magic Key Heist: Acquire X magic keys and escape the Keymaster's Keep
    """

    display_name: str = "Goal"

    option_keymasters_challenge: int = 0
    option_magic_key_heist: int = 1

    default = 0


class ArtifactsOfResolveTotal(Range):
    """
    Determines how many Artifacts of Resolve are in the item pool.

    Only relevant if the selected goal is Keymaster's Challenge.
    """

    display_name: str = "Artifacts of Resolve Total"

    range_start: int = 3
    range_end: int = 25

    default = 5


class ArtifactsOfResolveRequired(Range):
    """
    Determines how many Artifacts of Resolve are required to unlock the Keymaster's challenge room.

    Only relevant if the selected goal is Keymaster's Challenge.
    """

    display_name: str = "Artifacts of Resolve Required"

    range_start: int = 1
    range_end: int = 25

    default = 3


class MagicKeysRequired(Range):
    """
    Determines how many Magic Keys are required before escaping the Keymaster's Keep.

    Only relevant if the selected goal is Magic Key Heist.
    """

    display_name: str = "Magic Keys Required"

    range_start: int = 10
    range_end: int = 50

    default = 18


class KeepAreas(Range):
    """
    Determines how many areas are in the Keymaster's Keep.

    Each area will contain a new set of trials and most will be locked by one or more keys.
    """

    display_name: str = "Keep Areas"

    range_start: int = 10
    range_end: int = 100

    default = 20


class MagicKeysTotal(Range):
    """
    Determines how many Magic Keys are in the item pool.

    The keys in that pool will be used to generate the lock combinations for areas in the Keymaster's Keep. They will
    also act as the amount of available keys to the player in the Magic Key Heist goal.
    """

    display_name: str = "Magic Keys Total"

    range_start: int = 10
    range_end: int = 50

    default = 30


class UnlockedAreas(Range):
    """
    Determines how many areas are unlocked at the start of the game.

    The remaining areas will be locked by one or more keys.
    """

    display_name: str = "Unlocked Areas"

    range_start: int = 1
    range_end: int = 5

    default = 1


class LockMagicKeysMinimum(Range):
    """
    Determines the minimum amount of Magic Keys that could be required to unlock an area.

    The amount of keys required to unlock an area will be a random number between this value and the maximum. Note that
    this option will be ignored for the first few areas to ensure the game is completable.
    """

    display_name: str = "Lock Keys Minimum"

    range_start: int = 1
    range_end: int = 5

    default = 1


class LockMagicKeysMaximum(Range):
    """
    Determines the maximum amount of Magic Keys that could be required to unlock an area.

    The amount of keys required to unlock an area will be a random number between the minimum and this value. Note that
    this option will be ignored for the first few areas to ensure the game is completable.
    """

    display_name: str = "Lock Keys Maximum"

    range_start: int = 1
    range_end: int = 5

    default = 3


class AreaTrialsMinimum(Range):
    """
    Determines the minimum amount of trials that could be in an area.

    The amount of trials in an area will be a random number between this value and the maximum, but might get adjusted
    upwards to hold the item pool size.
    """

    display_name: str = "Area Trials Minimum"

    range_start: int = 1
    range_end: int = 25

    default = 3


class AreaTrialsMaximum(Range):
    """
    Determines the maximum amount of trials that could be in an area.

    The amount of trials in an area will be a random number between the minimum and this value, but might get adjusted
    upwards to hold the item pool size.
    """

    display_name: str = "Area Trials Maximum"

    range_start: int = 1
    range_end: int = 25

    default = 7


class Shops(Toggle):
    """
    If true, keep areas will have a chance to be replaced by a shop that will sell a handful of items.

    The presence of shops will add Unique Relics to the item pool, which will need to be found to purchase items.

    Yes, the option is named "shops_". Thank you, ALTTP!
    """

    display_name: str = "Shops"


class ShopsPercentageChance(Range):
    """
    Determines the percentage chance of a shop overriding a keep area when shops are enabled.

    A maximum of 10 shops can exist in the keep at once.
    """

    display_name: str = "Shops Percentage Chance"

    range_start: int = 5
    range_end: int = 50

    default = 20


class ShopItemsMinimum(Range):
    """
    Determines the minimum amount of items that could be sold in a shop.

    The amount of items sold in a shop will be a random number between this value and the maximum.
    """

    display_name: str = "Shop Items Minimum"

    range_start: int = 1
    range_end: int = 5

    default = 2


class ShopItemsMaximum(Range):
    """
    Determines the maximum amount of items that could be sold in a shop.

    The amount of items sold in a shop will be a random number between the minimum and this value.
    """

    display_name: str = "Shop Items Maximum"

    range_start: int = 1
    range_end: int = 5

    default = 5


class ShopItemsProgressionPercentageChance(Range):
    """
    Determines the percentage chance of each item in a shop being a guaranteed progression item.

    Since items are purchased with unique relics, it is recommended to set this value on the higher side. Each unique
    relic will only be able to unlock a single item in the keep, so ideally, they are worth the trouble.
    """

    display_name: str = "Shop Items Progression Percentage Chance"

    range_start: int = 0
    range_end: int = 100

    default = 100


class ShopHints(Toggle):
    """
    If true, upon discovering a shop, hints will be generated for the items sold in that shop.
    """

    display_name: str = "Shop Hints"


class GameMedleyMode(Toggle):
    """
    If true, a percentage of keep areas will feature Game Medley as their game, with each trial sourced randomly from
    a separate, dedicated pool of games.

    Activating Game Medley Mode will disable optional game conditions for keep areas assigned to Game Medley.
    """

    display_name: str = "Game Medley Mode"


class GameMedleyPercentageChance(Range):
    """
    Determines the percentage chance of a game medley being selected when Game Medley Mode is enabled.
    """

    display_name: str = "Game Medley Percentage Chance"

    range_start: int = 1
    range_end: int = 100

    default = 100


class GameMedleyGameSelection(OptionList):
    """
    Defines the game pool that will be used to generate Game Medley trials.

    Only game names originally listed in 'game_selection' are accepted.

    You are allowed to place games that already appear in other selection options here.

    You are allowed to add the same game multiple times here. This will act as a weighted pool.

    If this is left empty, all games from other selection options will be used as a default.
    """

    display_name: str = "Game Medley Game Selection"
    valid_keys = sorted(AutoGameRegister.games.keys())

    default = list()


class GameSelection(OptionList):
    """
    Defines the game pool to select from.

    All supported games are listed. Remove the ones you don't own or want to play.

    You are allowed to add the same game multiple times here. This will act as a weighted pool.
    """

    display_name: str = "Game Selection"
    valid_keys = sorted(AutoGameRegister.games.keys())

    default = sorted(AutoGameRegister.games.keys())


class IncludeAdultOnlyOrUnratedGames(Toggle):
    """
    Determines if adult only or unrated games should be considered for the game pool.

    Can be a useful filter to adhere to the rules of certain communities.
    """

    display_name: str = "Include Adult Only or Unrated Games"


class IncludeModernConsoleGames(DefaultOnToggle):
    """
    Determines if modern console games should be considered for the game pool.

    Can be a useful filter to adhere to the rules of certain communities.
    """

    display_name: str = "Include Modern Console Games"


class IncludeDifficultObjectives(Toggle):
    """
    Determines if difficult objectives should be considered.

    Enabling this option might yield objectives that some players will struggle or not be able to complete.

    If enabled, you can still exclude specific games with the 'excluded_games_difficult_objectives' option.
    """

    display_name: str = "Include Difficult Objectives"


class ExcludedGamesDifficultObjectives(OptionSet):
    """
    When 'include_difficult_objectives' is enabled, this option allows you to still exclude specific games.

    Only game names originally listed in 'game_selection' are accepted.

    If a game specified here only offers difficult objectives, this option will have no effect for it.
    """

    display_name: str = "Excluded Games Difficult Objectives"
    valid_keys = sorted(AutoGameRegister.games.keys())

    default = list()


class IncludeTimeConsumingObjectives(DefaultOnToggle):
    """
    Determines if time-consuming objectives should be considered.

    Enabling this option might yield objectives that take much longer to complete (i.e. more than 1 hour).

    If enabled, you can still exclude specific games with the 'excluded_games_time_consuming_objectives' option.
    """

    display_name: str = "Include Time-Consuming Objectives"


class ExcludedGamesTimeConsumingObjectives(OptionSet):
    """
    When 'include_time_consuming_objectives' is enabled, this option allows you to still exclude specific games.

    Only game names originally listed in 'game_selection' are accepted.

    If a game specified here only offers time-consuming objectives, this option will have no effect for it.
    """

    display_name: str = "Excluded Games Time-Consuming Objectives"
    valid_keys = sorted(AutoGameRegister.games.keys())

    default = list()


class HintsRevealObjectives(Toggle):
    """
    Determines if Archipelago hints will provide information about a location's objective.

    Enabling this option will potentially spoil the game for an area and the objective that needs to be completed.
    """

    display_name: str = "Hints Reveal Objectives"


@dataclass
class KeymastersKeepOptions(PerGameCommonOptions, GameArchipelagoOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    artifacts_of_resolve_total: ArtifactsOfResolveTotal
    artifacts_of_resolve_required: ArtifactsOfResolveRequired
    magic_keys_required: MagicKeysRequired
    keep_areas: KeepAreas
    magic_keys_total: MagicKeysTotal
    unlocked_areas: UnlockedAreas
    lock_magic_keys_minimum: LockMagicKeysMinimum
    lock_magic_keys_maximum: LockMagicKeysMaximum
    area_trials_minimum: AreaTrialsMinimum
    area_trials_maximum: AreaTrialsMaximum
    shops_: Shops
    shops_percentage_chance: ShopsPercentageChance
    shop_items_minimum: ShopItemsMinimum
    shop_items_maximum: ShopItemsMaximum
    shop_items_progression_percentage_chance: ShopItemsProgressionPercentageChance
    shop_hints: ShopHints
    game_medley_mode: GameMedleyMode
    game_medley_percentage_chance: GameMedleyPercentageChance
    game_medley_game_selection: GameMedleyGameSelection
    game_selection: GameSelection
    include_adult_only_or_unrated_games: IncludeAdultOnlyOrUnratedGames
    include_modern_console_games: IncludeModernConsoleGames
    include_difficult_objectives: IncludeDifficultObjectives
    excluded_games_difficult_objectives: ExcludedGamesDifficultObjectives
    include_time_consuming_objectives: IncludeTimeConsumingObjectives
    excluded_games_time_consuming_objectives: ExcludedGamesTimeConsumingObjectives
    hints_reveal_objectives: HintsRevealObjectives


# Option presets here...


option_groups: typing.List[OptionGroup] = [
    OptionGroup(
        "Goal Options",
        [
            Goal,
            ArtifactsOfResolveTotal,
            ArtifactsOfResolveRequired,
            MagicKeysRequired,
        ],
    ),
    OptionGroup(
        "Keep Generation Options",
        [
            KeepAreas,
            MagicKeysTotal,
            UnlockedAreas,
            LockMagicKeysMinimum,
            LockMagicKeysMaximum,
            AreaTrialsMinimum,
            AreaTrialsMaximum,
            Shops,
            ShopsPercentageChance,
            ShopItemsMinimum,
            ShopItemsMaximum,
            ShopItemsProgressionPercentageChance,
            ShopHints,
        ],
    ),
    OptionGroup(
        "Game / Objective Selection Options",
        [
            IncludeAdultOnlyOrUnratedGames,
            IncludeModernConsoleGames,
            IncludeDifficultObjectives,
            ExcludedGamesDifficultObjectives,
            IncludeTimeConsumingObjectives,
            ExcludedGamesTimeConsumingObjectives,
            HintsRevealObjectives,
            GameMedleyMode,
            GameMedleyPercentageChance,
            GameMedleyGameSelection,
            GameSelection,
        ],
    ),
    OptionGroup(
        "Individual Game Options",
        typing.get_type_hints(GameArchipelagoOptions).values(),
    )
]
