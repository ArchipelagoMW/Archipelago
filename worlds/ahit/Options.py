import typing
from worlds.AutoWorld import World
from Options import Option, Range, Toggle, DeathLink, Choice, OptionDict


def adjust_options(world: World):
    world.multiworld.HighestChapterCost[world.player].value = max(
        world.multiworld.HighestChapterCost[world.player].value,
        world.multiworld.LowestChapterCost[world.player].value)

    world.multiworld.LowestChapterCost[world.player].value = min(
        world.multiworld.LowestChapterCost[world.player].value,
        world.multiworld.HighestChapterCost[world.player].value)

    world.multiworld.FinalChapterMinCost[world.player].value = min(
        world.multiworld.FinalChapterMinCost[world.player].value,
        world.multiworld.FinalChapterMaxCost[world.player].value)

    world.multiworld.FinalChapterMaxCost[world.player].value = max(
        world.multiworld.FinalChapterMaxCost[world.player].value,
        world.multiworld.FinalChapterMinCost[world.player].value)

    world.multiworld.BadgeSellerMinItems[world.player].value = min(
        world.multiworld.BadgeSellerMinItems[world.player].value,
        world.multiworld.BadgeSellerMaxItems[world.player].value)

    world.multiworld.BadgeSellerMaxItems[world.player].value = max(
        world.multiworld.BadgeSellerMinItems[world.player].value,
        world.multiworld.BadgeSellerMaxItems[world.player].value)

    total_tps: int = get_total_time_pieces(world)
    if world.multiworld.HighestChapterCost[world.player].value > total_tps-5:
        world.multiworld.HighestChapterCost[world.player].value = min(45, total_tps-5)

    if world.multiworld.LowestChapterCost[world.player].value > total_tps-5:
        world.multiworld.LowestChapterCost[world.player].value = min(45, total_tps-5)

    if world.multiworld.FinalChapterMaxCost[world.player].value > total_tps:
        world.multiworld.FinalChapterMaxCost[world.player].value = min(50, total_tps)

    if world.multiworld.FinalChapterMinCost[world.player].value > total_tps:
        world.multiworld.FinalChapterMinCost[world.player].value = min(50, total_tps-5)

    # Don't allow Rush Hour goal if DLC2 content is disabled
    if world.multiworld.EndGoal[world.player].value == 2 and world.multiworld.EnableDLC2[world.player].value == 0:
        world.multiworld.EndGoal[world.player].value = 1

    # Don't allow Seal the Deal goal if Death Wish content is disabled
    if world.multiworld.EndGoal[world.player].value == 3 and not world.is_dw():
        world.multiworld.EndGoal[world.player].value = 1

    if world.multiworld.DWEnableBonus[world.player].value > 0:
        world.multiworld.DWAutoCompleteBonuses[world.player].value = 0

    if world.is_dw_only():
        world.multiworld.EndGoal[world.player].value = 3
        world.multiworld.ActRandomizer[world.player].value = 0
        world.multiworld.ShuffleAlpineZiplines[world.player].value = 0
        world.multiworld.ShuffleSubconPaintings[world.player].value = 0
        world.multiworld.ShuffleStorybookPages[world.player].value = 0
        world.multiworld.ShuffleActContracts[world.player].value = 0
        world.multiworld.EnableDLC1[world.player].value = 0
        world.multiworld.LogicDifficulty[world.player].value = 0
        world.multiworld.KnowledgeChecks[world.player].value = 0
        world.multiworld.DWTimePieceRequirement[world.player].value = 0
        world.multiworld.progression_balancing[world.player].value = 0


def get_total_time_pieces(world: World) -> int:
    count: int = 40
    if world.is_dlc1():
        count += 6

    if world.is_dlc2():
        count += 10

    return min(40+world.multiworld.MaxExtraTimePieces[world.player].value, count)


class EndGoal(Choice):
    """The end goal required to beat the game.
    Finale: Reach Time's End and beat Mustache Girl. The Finale will be in its vanilla location.

    Rush Hour: Reach and complete Rush Hour. The level will be in its vanilla location and Chapter 7
    will be the final chapter. You also must find Nyakuza Metro itself and complete all of its levels.
    Requires DLC2 content to be enabled.

    Seal the Deal: Reach and complete the Seal the Deal death wish main objective.
    Requires Death Wish content to be enabled."""
    display_name = "End Goal"
    option_finale = 1
    option_rush_hour = 2
    option_seal_the_deal = 3
    default = 1


class ActRandomizer(Choice):
    """If enabled, shuffle the game's Acts between each other.
    Light will cause Time Rifts to only be shuffled amongst each other,
    and Blue Time Rifts and Purple Time Rifts to be shuffled separately."""
    display_name = "Shuffle Acts"
    option_false = 0
    option_light = 1
    option_insanity = 2
    default = 1


class ActPlando(OptionDict):
    """Plando acts onto other acts. For example, \"Train Rush\": \"Alpine Free Roam\""""
    display_name = "Act Plando"


class FinaleShuffle(Toggle):
    """If enabled, chapter finales will only be shuffled amongst each other in act shuffle."""
    display_name = "Finale Shuffle"
    default = 0


class LogicDifficulty(Choice):
    """Choose the difficulty setting for logic."""
    display_name = "Logic Difficulty"
    option_normal = 0
    option_hard = 1
    option_expert = 2
    default = 0


class KnowledgeChecks(Toggle):
    """Put tricks into logic that are not necessarily difficult,
     but require knowledge that is not obvious or commonly known. Can include glitches such as No Bonk Surfing.
     This option will be forced on if logic difficulty is at least hard."""
    display_name = "Knowledge Checks"
    default = 0


class RandomizeHatOrder(Choice):
    """Randomize the order that hats are stitched in.
    Time Stop Last will force Time Stop to be the last hat in the sequence."""
    display_name = "Randomize Hat Order"
    option_false = 0
    option_true = 1
    option_time_stop_last = 2
    default = 1


class YarnBalancePercent(Range):
    """How much (in percentage) of the yarn in the pool that will be progression balanced."""
    display_name = "Yarn Balance Percentage"
    default = 20
    range_start = 0
    range_end = 100


class TimePieceBalancePercent(Range):
    """How much (in percentage) of time pieces in the pool that will be progression balanced."""
    display_name = "Time Piece Balance Percentage"
    default = 35
    range_start = 0
    range_end = 100


class StartWithCompassBadge(Toggle):
    """If enabled, start with the Compass Badge. In Archipelago, the Compass Badge will track all items in the world
    (instead of just Relics). Recommended if you're not familiar with where item locations are."""
    display_name = "Start with Compass Badge"
    default = 1


class CompassBadgeMode(Choice):
    """closest - Compass Badge points to the closest item regardless of classification
    important_only - Compass Badge points to progression/useful items only
    important_first - Compass Badge points to progression/useful items first, then it will point to junk items"""
    display_name = "Compass Badge Mode"
    option_closest = 1
    option_important_only = 2
    option_important_first = 3
    default = 1


class UmbrellaLogic(Toggle):
    """Makes Hat Kid's default punch attack do absolutely nothing, making the Umbrella much more relevant and useful"""
    display_name = "Umbrella Logic"
    default = 0


class ShuffleStorybookPages(Toggle):
    """If enabled, each storybook page in the purple Time Rifts is an item check.
    The Compass Badge can track these down for you."""
    display_name = "Shuffle Storybook Pages"
    default = 1


class ShuffleActContracts(Toggle):
    """If enabled, shuffle Snatcher's act contracts into the pool as items"""
    display_name = "Shuffle Contracts"
    default = 1


class ShuffleAlpineZiplines(Toggle):
    """If enabled, Alpine's zipline paths leading to the peaks will be locked behind items."""
    display_name = "Shuffle Alpine Ziplines"
    default = 0


class ShuffleSubconPaintings(Toggle):
    """If enabled, shuffle items into the pool that unlock Subcon Forest fire spirit paintings.
    These items are progressive, with the order of Village-Swamp-Courtyard."""
    display_name = "Shuffle Subcon Paintings"
    default = 0


class StartingChapter(Choice):
    """Determines which chapter you will be guaranteed to be able to enter at the beginning of the game."""
    display_name = "Starting Chapter"
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    default = 1


class ChapterCostIncrement(Range):
    """Lower values mean chapter costs increase slower. Higher values make the cost differences more steep."""
    display_name = "Chapter Cost Increment"
    range_start = 1
    range_end = 8
    default = 4


class ChapterCostMinDifference(Range):
    """The minimum difference between chapter costs."""
    display_name = "Minimum Chapter Cost Difference"
    range_start = 1
    range_end = 8
    default = 4


class LowestChapterCost(Range):
    """Value determining the lowest possible cost for a chapter.
    Chapter costs will, progressively, be calculated based on this value (except for the final chapter)."""
    display_name = "Lowest Possible Chapter Cost"
    range_start = 0
    range_end = 10
    default = 5


class HighestChapterCost(Range):
    """Value determining the highest possible cost for a chapter.
    Chapter costs will, progressively, be calculated based on this value (except for the final chapter)."""
    display_name = "Highest Possible Chapter Cost"
    range_start = 15
    range_end = 45
    default = 25


class FinalChapterMinCost(Range):
    """Minimum Time Pieces required to enter the final chapter. This is part of your goal."""
    display_name = "Final Chapter Minimum Time Piece Cost"
    range_start = 0
    range_end = 50
    default = 30


class FinalChapterMaxCost(Range):
    """Maximum Time Pieces required to enter the final chapter. This is part of your goal."""
    display_name = "Final Chapter Maximum Time Piece Cost"
    range_start = 0
    range_end = 50
    default = 35


class MaxExtraTimePieces(Range):
    """Maximum amount of extra Time Pieces from the DLCs.
    Arctic Cruise will add up to 6. Nyakuza Metro will add up to 10. The absolute maximum is 56."""
    display_name = "Max Extra Time Pieces"
    range_start = 0
    range_end = 16
    default = 16


class YarnCostMin(Range):
    """The minimum possible yarn needed to stitch a hat."""
    display_name = "Minimum Yarn Cost"
    range_start = 1
    range_end = 12
    default = 4


class YarnCostMax(Range):
    """The maximum possible yarn needed to stitch a hat."""
    display_name = "Maximum Yarn Cost"
    range_start = 1
    range_end = 12
    default = 8


class YarnAvailable(Range):
    """How much yarn is available to collect in the item pool."""
    display_name = "Yarn Available"
    range_start = 30
    range_end = 75
    default = 45


class MinExtraYarn(Range):
    """The minimum amount of extra yarn in the item pool.
    There must be at least this much more yarn over the total amount of yarn needed to craft all hats.
    For example, if this option's value is 10, and the total yarn needed to craft all hats is 40,
    there must be at least 50 yarn in the pool."""
    display_name = "Max Extra Yarn"
    range_start = 0
    range_end = 15
    default = 10


class MinPonCost(Range):
    """The minimum amount of Pons that any shop item can cost."""
    display_name = "Minimum Shop Pon Cost"
    range_start = 10
    range_end = 800
    default = 75


class MaxPonCost(Range):
    """The maximum amount of Pons that any shop item can cost."""
    display_name = "Maximum Shop Pon Cost"
    range_start = 10
    range_end = 800
    default = 300


class BadgeSellerMinItems(Range):
    """The smallest amount of items that the Badge Seller can have for sale."""
    display_name = "Badge Seller Minimum Items"
    range_start = 0
    range_end = 10
    default = 4


class BadgeSellerMaxItems(Range):
    """The largest amount of items that the Badge Seller can have for sale."""
    display_name = "Badge Seller Maximum Items"
    range_start = 0
    range_end = 10
    default = 8


class CTRWithSprint(Toggle):
    """If enabled, clearing Cheating the Race with just Sprint Hat can be in logic."""
    display_name = "Cheating the Race with Sprint Hat"
    default = 0


class EnableDLC1(Toggle):
    """Shuffle content from The Arctic Cruise (Chapter 6) into the game. This also includes the Tour time rift.
    DO NOT ENABLE THIS OPTION IF YOU DO NOT HAVE SEAL THE DEAL DLC INSTALLED!!!"""
    display_name = "Shuffle Chapter 6"
    default = 0


class Tasksanity(Toggle):
    """If enabled, Ship Shape tasks will become checks. Requires DLC1 content to be enabled."""
    display_name = "Tasksanity"
    default = 0


class TasksanityTaskStep(Range):
    """How many tasks the player must complete in Tasksanity to send a check."""
    display_name = "Tasksanity Task Step"
    range_start = 1
    range_end = 3
    default = 1


class TasksanityCheckCount(Range):
    """How many Tasksanity checks there will be in total."""
    display_name = "Tasksanity Check Count"
    range_start = 5
    range_end = 30
    default = 18


class ExcludeTour(Toggle):
    """Removes the Tour time rift from the game. This option is recommended if you don't want to deal with
    important levels being shuffled onto the Tour time rift, or important items being shuffled onto Tour pages
    when your goal is Time's End."""
    display_name = "Exclude Tour Time Rift"
    default = 0


class ShipShapeCustomTaskGoal(Range):
    """Change the amount of tasks required to complete Ship Shape. This will not affect Cruisin' for a Bruisin'."""
    display_name = "Ship Shape Custom Task Goal"
    range_start = 5
    range_end = 30
    default = 18


class EnableDLC2(Toggle):
    """Shuffle content from Nyakuza Metro (Chapter 7) into the game.
    DO NOT ENABLE THIS OPTION IF YOU DO NOT HAVE NYAKUZA METRO DLC INSTALLED!!!"""
    display_name = "Shuffle Chapter 7"
    default = 0


class MetroMinPonCost(Range):
    """The cheapest an item can be in any Nyakuza Metro shop. Includes ticket booths."""
    display_name = "Metro Shops Minimum Pon Cost"
    range_start = 10
    range_end = 800
    default = 50


class MetroMaxPonCost(Range):
    """The most expensive an item can be in any Nyakuza Metro shop. Includes ticket booths."""
    display_name = "Metro Shops Maximum Pon Cost"
    range_start = 10
    range_end = 800
    default = 200


class NyakuzaThugMinShopItems(Range):
    """The smallest amount of items that the thugs in Nyakuza Metro can have for sale."""
    display_name = "Nyakuza Thug Minimum Shop Items"
    range_start = 0
    range_end = 5
    default = 2


class NyakuzaThugMaxShopItems(Range):
    """The largest amount of items that the thugs in Nyakuza Metro can have for sale."""
    display_name = "Nyakuza Thug Maximum Shop Items"
    range_start = 0
    range_end = 5
    default = 4


class BaseballBat(Toggle):
    """Replace the Umbrella with the baseball bat from Nyakuza Metro.
    DLC2 content does not have to be shuffled for this option but Nyakuza Metro still needs to be installed."""
    display_name = "Baseball Bat"
    default = 0


class EnableDeathWish(Toggle):
    """Shuffle Death Wish contracts into the game. Each contract by default will have 1 check granted upon completion.
    DO NOT ENABLE THIS OPTION IF YOU DO NOT HAVE SEAL THE DEAL DLC INSTALLED!!!"""
    display_name = "Enable Death Wish"
    default = 0


class DeathWishOnly(Toggle):
    """An alternative gameplay mode that allows you to exclusively play Death Wish in a seed.
    This has the following effects:
    - Death Wish is instantly unlocked from the start
    - All hats and other progression items are instantly given to you
    - Useful items such as Fast Hatter Badge will still be in the item pool instead of in your inventory at the start
    - All chapters and their levels are unlocked, act shuffle is forced off
    - Any checks other than Death Wish contracts are completely removed
    - All Pons in the item pool are replaced with Health Pons or random cosmetics
    - The EndGoal option is forced to complete Seal the Deal"""
    display_name = "Death Wish Only"
    default = 0


class DWShuffle(Toggle):
    """An alternative mode for Death Wish where each contract is unlocked one by one, in a random order.
    Stamp requirements to unlock contracts is removed. Any excluded contracts will not be shuffled into the sequence.
    If Seal the Deal is the end goal, it will always be the last Death Wish in the sequence.
    Disabling candles is highly recommended."""
    display_name = "Death Wish Shuffle"
    default = 0


class DWShuffleCountMin(Range):
    """The minimum number of Death Wishes that can be in the Death Wish shuffle sequence.
    The final result is clamped at the number of non-excluded Death Wishes."""
    display_name = "Death Wish Shuffle Minimum Count"
    range_start = 5
    range_end = 38
    default = 18


class DWShuffleCountMax(Range):
    """The maximum number of Death Wishes that can be in the Death Wish shuffle sequence.
    The final result is clamped at the number of non-excluded Death Wishes."""
    display_name = "Death Wish Shuffle Maximum Count"
    range_start = 5
    range_end = 38
    default = 25


class DWEnableBonus(Toggle):
    """In Death Wish, allow the full completion of contracts to reward items.
    WARNING!! Only for the brave! This option can create VERY DIFFICULT SEEDS!
    ONLY turn this on if you know what you are doing to yourself and everyone else in the multiworld!
    Using Peace and Tranquility to auto-complete the bonuses will NOT count!"""
    display_name = "Shuffle Death Wish Full Completions"
    default = 0


class DWAutoCompleteBonuses(Toggle):
    """If enabled, auto complete all bonus stamps after completing the main objective in a Death Wish.
    This option will have no effect if bonus checks (DWEnableBonus) are turned on."""
    display_name = "Auto Complete Bonus Stamps"
    default = 1


class DWExcludeAnnoyingContracts(Toggle):
    """Exclude Death Wish contracts from the pool that are particularly tedious or take a long time to reach/clear.
    Excluded Death Wishes are automatically completed as soon as they are unlocked.
    This option currently excludes the following contracts:
    - Vault Codes in the Wind
    - Boss Rush
    - Camera Tourist
    - The Mustache Gauntlet
    - Rift Collapse: Deep Sea
    - Cruisin' for a Bruisin'
    - Seal the Deal (non-excluded if goal, but the checks are still excluded)"""
    display_name = "Exclude Annoying Death Wish Contracts"
    default = 1


class DWExcludeAnnoyingBonuses(Toggle):
    """If Death Wish full completions are shuffled in, exclude tedious Death Wish full completions from the pool.
    Excluded bonus Death Wishes automatically reward their bonus stamps upon completion of the main objective.
    This option currently excludes the following bonuses:
    - So You're Back From Outer Space
    - Encore! Encore!
    - Snatcher's Hit List
    - 10 Seconds until Self-Destruct
    - Killing Two Birds
    - Snatcher Coins in Battle of the Birds
    - Zero Jumps
    - Bird Sanctuary
    - Wound-Up Windmill
    - Snatcher Coins in Alpine Skyline
    - Seal the Deal"""
    display_name = "Exclude Annoying Death Wish Full Completions"
    default = 1


class DWExcludeCandles(Toggle):
    """If enabled, exclude all candle Death Wishes."""
    display_name = "Exclude Candle Death Wishes"
    default = 1


class DWTimePieceRequirement(Range):
    """How many Time Pieces that will be required to unlock Death Wish."""
    display_name = "Death Wish Time Piece Requirement"
    range_start = 0
    range_end = 35
    default = 15


class TrapChance(Range):
    """The chance for any junk item in the pool to be replaced by a trap."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0


class BabyTrapWeight(Range):
    """The weight of Baby Traps in the trap pool.
    Baby Traps place a multitude of the Conductor's grandkids into Hat Kid's hands, causing her to lose her balance."""
    display_name = "Baby Trap Weight"
    range_start = 0
    range_end = 100
    default = 40


class LaserTrapWeight(Range):
    """The weight of Laser Traps in the trap pool.
    Laser Traps will spawn multiple giant lasers (from Snatcher's boss fight) at Hat Kid's location."""
    display_name = "Laser Trap Weight"
    range_start = 0
    range_end = 100
    default = 40


class ParadeTrapWeight(Range):
    """The weight of Parade Traps in the trap pool.
    Parade Traps will summon multiple Express Band owls with knives that chase Hat Kid by mimicking her movement."""
    display_name = "Parade Trap Weight"
    range_start = 0
    range_end = 100
    default = 20


ahit_options: typing.Dict[str, type(Option)] = {

    "EndGoal":                  EndGoal,
    "ActRandomizer":            ActRandomizer,
    "ActPlando":                ActPlando,
    "ShuffleAlpineZiplines":    ShuffleAlpineZiplines,
    "FinaleShuffle":            FinaleShuffle,
    "LogicDifficulty":          LogicDifficulty,
    "KnowledgeChecks":          KnowledgeChecks,
    "YarnBalancePercent":       YarnBalancePercent,
    "TimePieceBalancePercent":  TimePieceBalancePercent,
    "RandomizeHatOrder":        RandomizeHatOrder,
    "UmbrellaLogic":            UmbrellaLogic,
    "StartWithCompassBadge":    StartWithCompassBadge,
    "CompassBadgeMode":         CompassBadgeMode,
    "ShuffleStorybookPages":    ShuffleStorybookPages,
    "ShuffleActContracts":      ShuffleActContracts,
    "ShuffleSubconPaintings":   ShuffleSubconPaintings,
    "StartingChapter":          StartingChapter,
    "CTRWithSprint":            CTRWithSprint,

    "EnableDLC1":               EnableDLC1,
    "Tasksanity":               Tasksanity,
    "TasksanityTaskStep":       TasksanityTaskStep,
    "TasksanityCheckCount":     TasksanityCheckCount,
    "ExcludeTour":              ExcludeTour,
    "ShipShapeCustomTaskGoal":  ShipShapeCustomTaskGoal,

    "EnableDeathWish":              EnableDeathWish,
    "DWShuffle":                    DWShuffle,
    "DWShuffleCountMin":            DWShuffleCountMin,
    "DWShuffleCountMax":            DWShuffleCountMax,
    "DeathWishOnly":                DeathWishOnly,
    "DWEnableBonus":                DWEnableBonus,
    "DWAutoCompleteBonuses":        DWAutoCompleteBonuses,
    "DWExcludeAnnoyingContracts":   DWExcludeAnnoyingContracts,
    "DWExcludeAnnoyingBonuses":     DWExcludeAnnoyingBonuses,
    "DWExcludeCandles":             DWExcludeCandles,
    "DWTimePieceRequirement":       DWTimePieceRequirement,

    "EnableDLC2":               EnableDLC2,
    "BaseballBat":              BaseballBat,
    "MetroMinPonCost":          MetroMinPonCost,
    "MetroMaxPonCost":          MetroMaxPonCost,
    "NyakuzaThugMinShopItems":  NyakuzaThugMinShopItems,
    "NyakuzaThugMaxShopItems":  NyakuzaThugMaxShopItems,

    "LowestChapterCost":        LowestChapterCost,
    "HighestChapterCost":       HighestChapterCost,
    "ChapterCostIncrement":     ChapterCostIncrement,
    "ChapterCostMinDifference": ChapterCostMinDifference,
    "MaxExtraTimePieces":       MaxExtraTimePieces,

    "FinalChapterMinCost":          FinalChapterMinCost,
    "FinalChapterMaxCost":          FinalChapterMaxCost,

    "YarnCostMin":              YarnCostMin,
    "YarnCostMax":              YarnCostMax,
    "YarnAvailable":            YarnAvailable,
    "MinExtraYarn":             MinExtraYarn,

    "MinPonCost":               MinPonCost,
    "MaxPonCost":               MaxPonCost,
    "BadgeSellerMinItems":      BadgeSellerMinItems,
    "BadgeSellerMaxItems":      BadgeSellerMaxItems,

    "TrapChance":               TrapChance,
    "BabyTrapWeight":           BabyTrapWeight,
    "LaserTrapWeight":          LaserTrapWeight,
    "ParadeTrapWeight":         ParadeTrapWeight,

    "death_link":               DeathLink,
}

slot_data_options: typing.Dict[str, type(Option)] = {

    "EndGoal":                      EndGoal,
    "ActRandomizer":                ActRandomizer,
    "ShuffleAlpineZiplines":        ShuffleAlpineZiplines,
    "LogicDifficulty":              LogicDifficulty,
    "KnowledgeChecks":              KnowledgeChecks,
    "RandomizeHatOrder":            RandomizeHatOrder,
    "UmbrellaLogic":                UmbrellaLogic,
    "CompassBadgeMode":             CompassBadgeMode,
    "ShuffleStorybookPages":        ShuffleStorybookPages,
    "ShuffleActContracts":          ShuffleActContracts,
    "ShuffleSubconPaintings":       ShuffleSubconPaintings,

    "EnableDLC1":               EnableDLC1,
    "Tasksanity":               Tasksanity,
    "TasksanityTaskStep":       TasksanityTaskStep,
    "TasksanityCheckCount":     TasksanityCheckCount,
    "ShipShapeCustomTaskGoal":  ShipShapeCustomTaskGoal,
    "ExcludeTour":              ExcludeTour,

    "EnableDeathWish":          EnableDeathWish,
    "DWShuffle":                DWShuffle,
    "DeathWishOnly":            DeathWishOnly,
    "DWEnableBonus":            DWEnableBonus,
    "DWAutoCompleteBonuses":    DWAutoCompleteBonuses,
    "DWTimePieceRequirement":   DWTimePieceRequirement,

    "EnableDLC2":       EnableDLC2,
    "MetroMinPonCost":  MetroMinPonCost,
    "MetroMaxPonCost":  MetroMaxPonCost,
    "BaseballBat":      BaseballBat,

    "MinPonCost":       MinPonCost,
    "MaxPonCost":       MaxPonCost,

    "death_link":       DeathLink,
}
