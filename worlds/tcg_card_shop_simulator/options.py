from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions,OptionGroup, DeathLink,Range, Toggle, DefaultOnToggle

class MaxLevel(Range):
    """
    What is the maximum level you would like to reach?
    This will be rounded up to the nearest multiple of 5

    The host can limit this setting to 50 for syncs
    """

    display_name = "Max Level"
    range_start = 10
    range_end = 100
    default = 20

class LicensesPerLevelGroup(Range):
    """
    Every 5 levels, across all 4 shop pages, how many licenses will be available?
    these are spread evenly as possible across all 4 shops
    """

    display_name = "Licenses Per Level Group"
    range_start = 6
    range_end = 14
    default = 6

class RequiredLicensesPercentage(Range):
    """
    Every 5 levels, you will stop leveling up until you have a certain number of licenses unlocked for items that you can sell.
    Every 5 levels what percentage of licenses do you need to find to progress?

    A high level goal will change this percentage at later levels for better generation
    """

    display_name = "Required licenses"
    range_start = 50
    range_end = 100
    default = 50


class Goal(Choice):
    """
    The victory condition for your run.
    Collection Builder is about getting your card collection to a collected percentage
    Sell Ghost Cards hides ghost cards in locations to be found
    """

    display_name = "Goal"
    option_reach_max_level = 0
    # option_collection_builder = 1
    option_sell_ghost_cards = 2
    default = 0

class GhostGoalAmount(Range):
    """
    If on Ghost cards Goal, How many do you need to sell?
    This causes ghost card items to be seeded in the multiworld
    """

    display_name = "Ghost Goal Amount"
    range_start = 1
    range_end = 80
    default = 40

# class CollectionGoalPercentage(Range):
#     """
#     If on CollectionGoal, What percentage of the collection should you collect?
#     the host can limit this setting to 50%
#     """
#
#     display_name = "Collection Goal Percentage"
#     range_start = 10
#     range_end = 100
#     default = 20

class StartWithWorker(Choice):
    """
    Choose a worker to start with.
    Reminder, you still have to pay their salary every day
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
    default = 0

class AutoRenovate(DefaultOnToggle):
    """
    This automatically renovates shop expansions for you when you receive expansions. never look at RENO BIGG again!
    """
    display_name = "Auto Renovate"

class BetterTrades(DefaultOnToggle):
    """
    Makes Customers always have New cards. If card sanity is on, the cards will always be Checks
    """
    display_name = "Better Trades"

class ExtraStartingItemChecks(Range):
    """
    This setting stops generation failures from very limited starts.
    The maximum checks per item are capped to 16 regardless of this setting
    """

    display_name = "Extra Starting Item Checks"
    range_start = 5
    range_end = 8
    default = 5

class SellCheckAmount(Range):
    """
    How many sell checks will each item have?

    The host can limit this to 8
    """
    display_name = "Sell Check Amount"
    range_start = 2
    range_end = 16
    default = 2

class ChecksPerPack(Range):
    """
    How many checks are in each of the 8 packs:
    Basic Tetramon, Rare Tetramon, Epic Tetramon, Legendary Tetramon, Basic Destiny, Rare Destiny, Epic Destiny, Legendary Destiny
    so 10 would be 10 checks per pack

    0 disables checks in card packs
    """
    display_name = "Checks Per Pack"
    range_start = 0
    range_end = 30
    default = 10

class CardCollectPercentage(Range):
    """
    How much of a pack do you need to collect to get all card checks

    this places the checks evenly in the range.
    example if there are 10 checks and percentage is 50, there will be a check every 5%

    The host can limit this percentage to 50%
    """
    display_name = "Card Collection Percentage"
    range_start = 10
    range_end = 100
    default = 33

class NumberOfSellCardChecks(Range):
    """
    This adds checks to selling Tetramon and Destiny cards.
    Both Sets will have this number of checks making the total checks double this amount
    """
    display_name = "Number of Sell Card Checks"
    range_start = 0
    range_end = 50
    default = 0

class SellCardsPerCheck(Range):
    """
    How many cards do you need to sell per check
    """
    display_name = "Cards sold per check"
    range_start = 1
    range_end = 10
    default = 1

class PlayTableChecks(Range):
    """
    How many checks are there for play tables
    """
    display_name = "Number of PlayTable Checks"
    range_start = 0
    range_end = 50
    default = 10

class GamesPerCheck(Range):
    """
    How many play table games are needed per game check.
    the higher the value the longer it takes to do a check
    """
    display_name = "Games Per Check"
    range_start = 1
    range_end = 10
    default = 1

class AllLevelsAreChecks(Toggle):
    """
    Adds all levels to the location pool, rather than the default of only every 5 levels
    """
    display_name = "All Levels Are Checks"

# class DecoShop(Toggle):
#     """
#     Turns the Deco Screen into a shop you can buy AP items in
#     """
#     display_name = "Decoration Shop"

class CardSanity(Choice):
    """
    Overrides Checks per pack and makes each card a unique check
    Enables new Cards from that rarity and below to be checks. For each level you add 360 locations. at legendary it is 1452 locations. At destiny Legendary you are adding 2904 checks
    """
    display_name = "Card Sanity"
    option_disabled = 0
    option_basic = 1
    option_rare = 2
    option_epic = 3
    option_legendary = 4
    option_destiny_basic = 5
    option_destiny_rare = 6
    option_destiny_epic = 7
    option_destiny_legendary = 8
    default = 0

class FoilInSanity(DefaultOnToggle):
    """
    Adds Foil cards to Card sanity
    Halves the amount of checks in card sanity
    """
    display_name = "Foil Cards in Sanity"

class BorderInSanity(Choice):
    """
    Adds the borders up to the selected border to Card Sanity.
    There are ~30 cards in each set of that border.
    """
    display_name = "Card Borders in Sanity"
    option_Base = 0
    option_FirstEdition = 1
    option_Silver = 2
    option_Gold = 3
    option_EX = 4
    option_FullArt = 5
    default = 0

# class CardSellingSanity(Toggle):
#     """
#     Changes Selling Card checks to be based on border and monstertype in addition to set
#     """
#     display_name = "Card Selling Sanity"

class MoneyBags(Range):
    """
    Determines the percentage of Filler contain money
    """
    display_name = "Money Filler"
    range_start = 0
    range_end = 100
    default = 50

class XpBoosts(Range):
    """
    Determines the percentage of Filler contain Shop Xp
    If your goal is Level goal, these are disabled
    """
    display_name = "XP Filler"
    range_start = 0
    range_end = 100
    default = 50

class RandomCard(Range):
    """
    Determines the percentage of Filler are random cards. Watch out for repeats!
    """
    display_name = "Random Card"
    range_start = 0
    range_end = 100
    default = 50

class RandomNewCard(Range):
    """
    Determines the percentage of Filler are random cards that will always be new
    if card sanity is checked, these cards will always be a check
    """
    display_name = "New Card"
    range_start = 0
    range_end = 100
    default = 50

class ProgressiveCustomerWealth(Range):
    """
    Determines the percentage of Filler
    increases how much money your customers have
    """
    display_name = "Progressive Customer Wealth"
    range_start = 0
    range_end = 100
    default = 25

class CardLuck(Range):
    """
    Determines the percentage of Filler
    increases your chances to find better cards in packs
    """
    display_name = "Card Luck"
    range_start = 0
    range_end = 100
    default = 25

class TrapFill(Range):
    """
    Determines the percentage of the junk fill which is filled with traps.
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 80
    default = 0

class StinkTrap(Range):
    """
    You know what this does. Stinky.
    Determines the percentage of Traps are Stink Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Stink Trap"
    range_start = 0
    range_end = 100
    default = 50

class PoltergeistTrap(Range):
    """
    Something is messing with the lights
    Determines the percentage of Traps are Poltergeist Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Poltergeist Trap"
    range_start = 0
    range_end = 100
    default = 50

class MarketChangeTrap(Range):
    """
    Causes prices to randomize
    Determines the percentage of Traps are Market Change Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Market Change Trap"
    range_start = 0
    range_end = 100
    default = 50
class CurrencyTrap(Range):
    """
    Causes Currency to Randomize
    Determines the percentage of Traps are Currency Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Currency Trap"
    range_start = 0
    range_end = 100
    default = 0

class DecreaseCardLuckTrap(Range):
    """
    Lowers your card luck
    Determines the percentage of Traps are Decrease Card Luck Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Reduce Card Luck Trap"
    range_start = 0
    range_end = 100
    default = 20

class CreditCardFailureTrap(Range):
    """
    Credit cards fail to work for a little while
    Determines the percentage of Traps are Credit Card Failure Traps.
    Traps must be enabled for this to have any effect.
    """
    display_name = "Credit Card Failure Trap"
    range_start = 0
    range_end = 100
    default = 50

@dataclass
class tcg_cardshop_simulator_option_groups(PerGameCommonOptions):
    OptionGroup("Goal Options", [
        MaxLevel,
        LicensesPerLevelGroup,
        RequiredLicensesPercentage,
        Goal,
        # CollectionGoalPercentage,
        GhostGoalAmount,
    ]),
    OptionGroup("General", [
        StartWithWorker,
        AutoRenovate,
        BetterTrades,
        ExtraStartingItemChecks,
        SellCheckAmount,
        ChecksPerPack,
        CardCollectPercentage,
        PlayTableChecks,
        GamesPerCheck,
        NumberOfSellCardChecks,
        SellCardsPerCheck,
        AllLevelsAreChecks,
        # DecoShop
    ]),
    OptionGroup("Sanity", [
        CardSanity,
        FoilInSanity,
        BorderInSanity
    ]),
    OptionGroup("Death Link", [
        DeathLink
    ])
    OptionGroup("Filler and Traps", [
        MoneyBags,
        XpBoosts,
        RandomCard,
        RandomNewCard,
        ProgressiveCustomerWealth,
        CardLuck,
        TrapFill,
        StinkTrap,
        PoltergeistTrap,
        CreditCardFailureTrap,
        MarketChangeTrap,
        CurrencyTrap,
        DecreaseCardLuckTrap
    ])
    
@dataclass
class TCGSimulatorOptions(PerGameCommonOptions):
    max_level: MaxLevel
    licenses_per_region: LicensesPerLevelGroup
    required_licenses: RequiredLicensesPercentage
    goal: Goal
    # collection_goal_percentage: CollectionGoalPercentage
    ghost_goal_amount: GhostGoalAmount
    start_with_worker: StartWithWorker
    auto_renovate: AutoRenovate
    better_trades: BetterTrades
    extra_starting_item_checks: ExtraStartingItemChecks
    sell_check_amount: SellCheckAmount
    checks_per_pack: ChecksPerPack
    card_collect_percent: CardCollectPercentage
    play_table_checks: PlayTableChecks
    games_per_check: GamesPerCheck
    sell_card_check_count: NumberOfSellCardChecks
    sell_cards_per_check: SellCardsPerCheck
    all_level_checks: AllLevelsAreChecks
    # deco_shop: DecoShop
    deathlink: DeathLink
    card_sanity: CardSanity
    foil_sanity: FoilInSanity
    border_sanity: BorderInSanity
    money_bags: MoneyBags
    xp_boosts: XpBoosts
    random_card: RandomCard
    random_new_card: RandomNewCard
    customer_wealth: ProgressiveCustomerWealth
    card_luck: CardLuck
    trap_fill: TrapFill
    stink_trap: StinkTrap
    poltergeist_trap: PoltergeistTrap
    credit_card_failure_trap: CreditCardFailureTrap
    market_change_trap: MarketChangeTrap
    currency_trap: CurrencyTrap
    decrease_card_luck_trap: DecreaseCardLuckTrap
