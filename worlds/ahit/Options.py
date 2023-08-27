import typing
from worlds.AutoWorld import World
from Options import Option, Range, Toggle, DeathLink, Choice
from .Items import get_total_time_pieces


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

    if world.multiworld.FinalChapterMaxCost[world.player].value > total_tps:
        world.multiworld.FinalChapterMaxCost[world.player].value = min(50, total_tps)

    # Don't allow Rush Hour goal if DLC2 content is disabled
    if world.multiworld.EndGoal[world.player].value == 2 and world.multiworld.EnableDLC2[world.player].value == 0:
        world.multiworld.EndGoal[world.player].value = 1


# General
class EndGoal(Choice):
    """The end goal required to beat the game.
    Finale: Reach Time's End and beat Mustache Girl. The Finale will be in its vanilla location.

    Rush Hour: Reach and complete Rush Hour. The level will be in its vanilla location and Chapter 7
    will be the final chapter. You also must find Nyakuza Metro itself and complete all of its levels.
    Requires DLC2 content to be enabled."""
    display_name = "End Goal"
    option_finale = 1
    option_rush_hour = 2
    default = 1


class ActRandomizer(Choice):
    """If enabled, shuffle the game's Acts between each other.
    Light will cause Time Rifts to only be shuffled amongst each other,
    and Blue Time Rifts and Purple Time Rifts are shuffled separately."""
    display_name = "Shuffle Acts"
    option_false = 0
    option_light = 1
    option_insanity = 2
    default = 1


class ShuffleAlpineZiplines(Toggle):
    """If enabled, Alpine's zipline paths leading to the peaks will be locked behind items."""
    display_name = "Shuffle Alpine Ziplines"
    default = 0


class VanillaAlpine(Choice):
    """If enabled, force Alpine (and optionally its finale) onto their vanilla locations in act shuffle."""
    display_name = "Vanilla Alpine Skyline"
    option_false = 0
    option_true = 1
    option_finale = 2
    default = 0


class LogicDifficulty(Choice):
    """Choose the difficulty setting for logic. Note that Hard or above will force SDJ logic on."""
    display_name = "Logic Difficulty"
    option_normal = 0
    option_hard = 1
    option_expert = 2
    default = 0


class RandomizeHatOrder(Toggle):
    """Randomize the order that hats are stitched in."""
    display_name = "Randomize Hat Order"
    default = 1


class UmbrellaLogic(Toggle):
    """Makes Hat Kid's default punch attack do absolutely nothing, making the Umbrella much more relevant and useful"""
    display_name = "Umbrella Logic"
    default = 0


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


class ShuffleStorybookPages(Toggle):
    """If enabled, each storybook page in the purple Time Rifts is an item check.
    The Compass Badge can track these down for you."""
    display_name = "Shuffle Storybook Pages"
    default = 1


class ShuffleActContracts(Toggle):
    """If enabled, shuffle Snatcher's act contracts into the pool as items"""
    display_name = "Shuffle Contracts"
    default = 1


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


class SDJLogic(Toggle):
    """Allow the SDJ (Sprint Double Jump) technique to be considered in logic."""
    display_name = "SDJ Logic"
    default = 0


class CTRWithSprint(Toggle):
    """If enabled, clearing Cheating the Race with just Sprint Hat can be in logic."""
    display_name = "Cheating the Race with Sprint Hat"
    default = 0


# DLC
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
    display_name = "Metro Shops Minimum Pon Cost"
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


class VanillaMetro(Choice):
    """Force Nyakuza Metro (and optionally its finale) onto their vanilla locations in act shuffle."""
    display_name = "Vanilla Metro"
    option_false = 0
    option_true = 1
    option_finale = 2


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
    default = 5


class LowestChapterCost(Range):
    """Value determining the lowest possible cost for a chapter.
    Chapter costs will, progressively, be calculated based on this value (except for Chapter 5)."""
    display_name = "Lowest Possible Chapter Cost"
    range_start = 0
    range_end = 10
    default = 5


class HighestChapterCost(Range):
    """Value determining the highest possible cost for a chapter.
    Chapter costs will, progressively, be calculated based on this value (except for Chapter 5)."""
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


# Death Wish
class EnableDeathWish(Toggle):
    """NOT IMPLEMENTED Shuffle Death Wish contracts into the game.
    Each contract by default will have a single check granted upon completion.
    DO NOT ENABLE THIS OPTION IF YOU DO NOT HAVE SEAL THE DEAL DLC INSTALLED!!!"""
    display_name = "Enable Death Wish"
    default = 0


class DWEnableBonus(Toggle):
    """NOT IMPLEMENTED In Death Wish, allow the full completion of contracts to reward items."""
    display_name = "Shuffle Death Wish Full Completions"
    default = 0


class DWExcludeAnnoyingContracts(Toggle):
    """NOT IMPLEMENTED Exclude Death Wish contracts from the pool that are particularly tedious or take a long time to reach/clear."""
    display_name = "Exclude Annoying Death Wish Contracts"
    default = 1


class DWExcludeAnnoyingBonuses(Toggle):
    """NOT IMPLEMENTED If Death Wish full completions are shuffled in, exclude particularly tedious Death Wish full completions
    from the pool"""
    display_name = "Exclude Annoying Death Wish Full Completions"
    default = 1


# Yarn
class YarnCostMin(Range):
    """The minimum possible yarn needed to stitch each hat."""
    display_name = "Minimum Yarn Cost"
    range_start = 1
    range_end = 12
    default = 4


class YarnCostMax(Range):
    """The maximum possible yarn needed to stitch each hat."""
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
    default = 400


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


# Traps
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
    "ShuffleAlpineZiplines":    ShuffleAlpineZiplines,
    "VanillaAlpine":            VanillaAlpine,
    "LogicDifficulty":          LogicDifficulty,
    "RandomizeHatOrder":        RandomizeHatOrder,
    "UmbrellaLogic":            UmbrellaLogic,
    "StartWithCompassBadge":    StartWithCompassBadge,
    "CompassBadgeMode":         CompassBadgeMode,
    "ShuffleStorybookPages":    ShuffleStorybookPages,
    "ShuffleActContracts":      ShuffleActContracts,
    "ShuffleSubconPaintings":   ShuffleSubconPaintings,
    "StartingChapter":          StartingChapter,
    "SDJLogic":                 SDJLogic,
    "CTRWithSprint":            CTRWithSprint,

    "EnableDLC1":               EnableDLC1,
    "Tasksanity":               Tasksanity,
    "TasksanityTaskStep":       TasksanityTaskStep,
    "TasksanityCheckCount":     TasksanityCheckCount,

    "EnableDeathWish":          EnableDeathWish,
    "EnableDLC2":               EnableDLC2,
    "BaseballBat":              BaseballBat,
    "VanillaMetro":             VanillaMetro,
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

    "EndGoal": EndGoal,
    "ActRandomizer": ActRandomizer,
    "ShuffleAlpineZiplines": ShuffleAlpineZiplines,
    "LogicDifficulty": LogicDifficulty,
    "RandomizeHatOrder": RandomizeHatOrder,
    "UmbrellaLogic": UmbrellaLogic,
    "CompassBadgeMode": CompassBadgeMode,
    "ShuffleStorybookPages": ShuffleStorybookPages,
    "ShuffleActContracts": ShuffleActContracts,
    "ShuffleSubconPaintings":   ShuffleSubconPaintings,
    "SDJLogic": SDJLogic,

    "EnableDLC1": EnableDLC1,
    "Tasksanity": Tasksanity,
    "TasksanityTaskStep": TasksanityTaskStep,
    "TasksanityCheckCount": TasksanityCheckCount,

    "EnableDeathWish": EnableDeathWish,

    "EnableDLC2": EnableDLC2,
    "MetroMinPonCost": MetroMinPonCost,
    "MetroMaxPonCost": MetroMaxPonCost,
    "BaseballBat": BaseballBat,

    "MinPonCost": MinPonCost,
    "MaxPonCost": MaxPonCost,

    "death_link": DeathLink,
}
