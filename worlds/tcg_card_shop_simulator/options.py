from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, OptionGroup, Range, Toggle, DefaultOnToggle, DeathLink, OptionCounter
from worlds.tcg_card_shop_simulator.data.items.filler import get_filler_default_dict
from worlds.tcg_card_shop_simulator.data.items.traps import get_traps_default_dict


class MaxLevel(Range):
    """
    Maximum shop level to reach.
    Rounded up to the nearest multiple of 5.

    Hosts may limit this to 60 with a Host.yaml setting.
    """

    display_name = "Max Level"
    range_start = 10
    range_end = 100
    default = 20

class TotalProductLicenses(Range):
    """
    How many product items are there for checks? This includes the 4 starting items

    Level caps are based on this value spread across your max level.
    """

    display_name = "Product Licenses"
    range_start = 12
    range_end = 106
    default = 20


class Goal(Choice):
    """
    Main victory condition.

    Max Level: Reach the max level
    Collection Builder: Unlock all packs and collect a target amount of cards.
    Grade Ghost Cards: Find and grade ghost cards hidden in the multiworld.
    """

    display_name = "Goal"
    option_reach_max_level = 0
    option_collection_builder = 1
    option_grade_ghost_cards = 2
    default = 0

class GhostGoalAmount(Range):
    """
    Number of Unique ghost cards required for victory.

    Ghost card items will be added to the multiworld.
    """

    display_name = "Ghost Goal Amount"
    range_start = 5
    range_end = 80
    default = 40

class CollectionGoalPercentage(Range):
    """
    Collection percentage required after unlocking all packs.

    Hosts may limit this to 60% with a Host.yaml setting.
    """

    display_name = "Collection Goal Percentage"
    range_start = 10
    range_end = 100
    default = 40

class StartWithWorker(Choice):
    """
    Start with a hired worker.

    You must still pay their daily salary.
    """
    display_name = "Starting Worker"
    option_none = 0
    option_zachery = 1
    option_terence = 2
    option_dennis = 3
    option_clark = 4
    option_angus = 5
    option_benji = 6
    option_lauren = 7
    option_axel = 8
    option_alexander = 9
    default = 0

class AutoRenovate(DefaultOnToggle):
    """
    Automatically renovate shop expansions when received. Never look at RENO BIGG again!
    """
    display_name = "Auto Renovate"

class SellCheckAmount(Range):
    """
    Number of sell checks per product.

    Selling an entire box counts as one check.
    """
    display_name = "Sell Check Amount"
    range_start = 2
    range_end = 100
    default = 2

class BulkBoxChecks(Toggle):
    """
    Selling bulk boxes from the workbench can grant checks.
    """
    display_name = "Enable Bulk Box Checks"

class CardSanity(Choice):
    """
    Individual cards become location checks. By default, these will be local filled with Filler

    Enabled:
    Different card variants count as separate checks based on Card Opening difficulty. 1452 checks

    Unique Foils:
    Foil cards also count as separate checks. 2904 checks
    """
    display_name = "Card Sanity"
    option_disabled = 0
    option_enabled = 1
    option_uniqueFoils = 2
    default = 0

class CardSanityCheckPercentage(Range):
    """
    What percentage of Card Sanity Checks should be allowed to hold items from other games?

    This can be limited by Host Yaml
    """
    display_name = "Sell Check Amount"
    range_start = 4
    range_end = 100
    default = 4

class CardOpeningCheckDifficulty(Choice):
    """
    Difficulty of achievement checks for opening cards.

    There are around 10 achievements for each difficulty. Harder options include easier achievements.

    Example achievements:
    Easy: First common foil
    Medium: Open 20 gold border foils from legendary packs
    Hard: Collect all 12 versions of a card
    Impossible: Collect 100 full arts from a pack
    """
    display_name = "Card Opening Check Difficulty"
    option_disabled = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_impossible = 4
    default = 2

class CardSellingCheckDifficulty(Choice):
    """
    Difficulty of achievement checks for selling cards.

    There are around 10 achievements for each difficulty. Harder options include easier achievements.

    Example goals:
    Easy: Sell 20 commons
    Medium: Sell 100 foils
    Hard: Sell 1000 cards
    Impossible: Sell 50 foil full arts
    """
    display_name = "Card Selling Check Difficulty"
    option_disabled = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_impossible = 4
    default = 1

class CardGradingCheckDifficulty(Choice):
    """
    Difficulty of achievement checks for grading cards.

    There are around 10 achievements for each difficulty. Harder options include easier achievements.

    Grading checks take much longer and are better for async games.

    Example goals:
    Easy: Grade 10 commons
    Medium: Grade 50 foils
    Hard: Grade 100 cards
    Impossible: Grade 20 foil full arts
    """
    display_name = "Card Grading Check Difficulty"
    option_disabled = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_impossible = 4
    default = 0


class NoFormats(Toggle):
    """
    All play table formats share one combined check pool.
    """
    display_name = "No Formats"

class PlayTableChecks(Range):
    """
    Number of checks available per play table format. Large values take a long time.
    """
    display_name = "Number of PlayTable Checks"
    range_start = 0
    range_end = 100
    default = 10

class FillerWeights(OptionCounter):
    """
    Change the weights of each trap

    Valid Options:
        - **Flip Controls Trap** - Invert your controls
        - **Floor Is Lava Trap** - Leave a trail of lava
        - **Giant Trap** - Mina gets larger
        - **2x Giant Trap** - Mina gets VERY large
        - **Giant Enemies Trap** - All enemies get larger
        - **2x Giant Enemies Trap** - All enemies get VERY large
        - **Invisible Trap** - Mina becomes invisible
        - **No HUD Trap** - Remove your HUD
        - **Rotate Camera Trap** - Slowly rotate your camera for a short time
        - **Rotate Camera Input Trap** - Moving now rotates your camera slowly
        - **Mirror Screen Trap** - Mirror your screen
        - **Upsidedown Screen Trap** - Mirror your screen vertically
    """
    display_name = "Filler Weights"
    default = get_filler_default_dict()
    min = 0
    valid_keys = get_filler_default_dict().keys()

class TrapFill(Range):
    """
    Percentage of junk items replaced with traps.
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 80
    default = 0

class TrapWeights(OptionCounter):
    """
    Change the weights of each trap

    Valid Options:
        - **Flip Controls Trap** - Invert your controls
        - **Floor Is Lava Trap** - Leave a trail of lava
        - **Giant Trap** - Mina gets larger
        - **2x Giant Trap** - Mina gets VERY large
        - **Giant Enemies Trap** - All enemies get larger
        - **2x Giant Enemies Trap** - All enemies get VERY large
        - **Invisible Trap** - Mina becomes invisible
        - **No HUD Trap** - Remove your HUD
        - **Rotate Camera Trap** - Slowly rotate your camera for a short time
        - **Rotate Camera Input Trap** - Moving now rotates your camera slowly
        - **Mirror Screen Trap** - Mirror your screen
        - **Upsidedown Screen Trap** - Mirror your screen vertically
    """
    display_name = "Trap Weights"
    default = get_traps_default_dict()
    min = 0
    valid_keys = get_traps_default_dict().keys()

tcg_cardshop_simulator_option_groups= [
    OptionGroup("Goal Options", [
        MaxLevel,
        LicensesPerLevelCap,
        Goal,
        CollectionGoalPercentage,
        GhostGoalAmount,
    ]),
    OptionGroup("General", [
        StartWithWorker,
        AutoRenovate,
        SellCheckAmount,
        BulkBoxChecks,
        PlayTableChecks,
        NoFormats,
        # DecoShop,
    ]),
    OptionGroup("Card Checks", [
        CardOpeningCheckDifficulty,
        CardSellingCheckDifficulty,
        CardGradingCheckDifficulty,
    ]),
    OptionGroup("Sanity", [
        CardSanity,
        CardSanityCheckPercentage,
    ]),
    OptionGroup("Death Link", [
        DeathLink
    ]),
    OptionGroup("Filler", [
        FillerWeights
    ]),
    OptionGroup("Traps", [
        TrapFill,
        TrapWeights
    ]),
]
    
@dataclass
class TCGSimulatorOptions(PerGameCommonOptions):
    max_level: MaxLevel
    licenses_per_cap: LicensesPerLevelCap
    goal: Goal
    collection_goal_percentage: CollectionGoalPercentage
    ghost_goal_amount: GhostGoalAmount
    start_with_worker: StartWithWorker
    auto_renovate: AutoRenovate
    sell_check_amount: SellCheckAmount
    bulk_box: BulkBoxChecks
    play_table_checks: PlayTableChecks
    no_formats: NoFormats
    checks_opening_difficulty: CardOpeningCheckDifficulty
    card_sanity: CardSanity
    card_sanity_percentage: CardSanityCheckPercentage
    checks_selling_difficulty: CardSellingCheckDifficulty
    checks_grading_difficulty: CardGradingCheckDifficulty
    deathlink: DeathLink

    trap_fill: TrapFill
    trap_weights: TrapWeights
    filler_weights: FillerWeights
