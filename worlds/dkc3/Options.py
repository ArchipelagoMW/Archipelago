from dataclasses import dataclass

from Options import Choice, Range, Toggle, DefaultOnToggle, OptionGroup, PerGameCommonOptions


class Goal(Choice):
    """
    Determines the goal of the seed

    Knautilus: Scuttle the Knautilus in Krematoa and defeat Baron K. Roolenstein

    Banana Bird Hunt: Find a certain number of Banana Birds and rescue their mother
    """
    display_name = "Goal"
    option_knautilus = 0
    option_banana_bird_hunt = 1
    default = 0


class IncludeTradeSequence(Toggle):
    """
    Allows logic to place items at the various steps of the trade sequence
    """
    display_name = "Include Trade Sequence"


class DKCoinsForGyrocopter(Range):
    """
    How many DK Coins are needed to unlock the Gyrocopter

    Note: Achieving this number before unlocking the Turbo Ski will cause the game to grant you a
    one-time upgrade to the next non-unlocked boat, until you return to Funky. Logic does not assume
    that you will use this.
    """
    display_name = "DK Coins for Gyrocopter"
    range_start = 10
    range_end = 41
    default = 30


class KrematoaBonusCoinCost(Range):
    """
    How many Bonus Coins are needed to unlock each level in Krematoa
    """
    display_name = "Krematoa Bonus Coins Cost"
    range_start = 1
    range_end = 17
    default = 15


class PercentageOfExtraBonusCoins(Range):
    """
    What Percentage of unneeded Bonus Coins are included in the item pool
    """
    display_name = "Percentage of Extra Bonus Coins"
    range_start = 0
    range_end = 100
    default = 100


class NumberOfBananaBirds(Range):
    """
    How many Banana Birds are put into the item pool
    """
    display_name = "Number of Banana Birds"
    range_start = 5
    range_end = 15
    default = 15


class PercentageOfBananaBirds(Range):
    """
    What Percentage of Banana Birds in the item pool are required for Banana Bird Hunt
    """
    display_name = "Percentage of Banana Birds"
    range_start = 20
    range_end = 100
    default = 100


class KONGsanity(Toggle):
    """
    Whether collecting all four KONG letters in each level grants a check
    """
    display_name = "KONGsanity"


class LevelShuffle(Toggle):
    """
    Whether levels are shuffled
    """
    display_name = "Level Shuffle"


class Difficulty(Choice):
    """
    Which Difficulty Level to use

    NORML: The Normal Difficulty
    HARDR: Many DK Barrels are removed
    TUFST: Most DK Barrels and all Midway Barrels are removed
    """
    display_name = "Difficulty"
    option_norml = 0
    option_hardr = 1
    option_tufst = 2
    default = 0

    @classmethod
    def get_option_name(cls, value) -> str:
        if cls.auto_display_name:
            return cls.name_lookup[value].upper()
        else:
            return cls.name_lookup[value]


class Autosave(DefaultOnToggle):
    """
    Whether the game should autosave after each level
    """
    display_name = "Autosave"


class MERRY(Toggle):
    """
    Whether the Bonus Barrels will be Christmas-themed
    """
    display_name = "MERRY"


class MusicShuffle(Toggle):
    """
    Whether music is shuffled
    """
    display_name = "Music Shuffle"


class KongPaletteSwap(Choice):
    """
    Which Palette to use for the Kongs
    """
    display_name = "Kong Palette Swap"
    option_default = 0
    option_purple = 1
    option_spooky = 2
    option_dark = 3
    option_chocolate = 4
    option_shadow = 5
    option_red_gold = 6
    option_gbc = 7
    option_halloween = 8
    default = 0


class StartingLifeCount(Range):
    """
    How many extra lives to start the game with
    """
    display_name = "Starting Life Count"
    range_start = 1
    range_end = 99
    default = 5


dkc3_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        KrematoaBonusCoinCost,
        PercentageOfExtraBonusCoins,
        NumberOfBananaBirds,
        PercentageOfBananaBirds,
    ]),
    OptionGroup("Aesthetics", [
        Autosave,
        MERRY,
        MusicShuffle,
        KongPaletteSwap,
        StartingLifeCount,
    ]),
]


@dataclass
class DKC3Options(PerGameCommonOptions):
    #death_link: DeathLink                                 # Disabled
    #include_trade_sequence: IncludeTradeSequence          # Disabled

    goal: Goal
    krematoa_bonus_coin_cost: KrematoaBonusCoinCost
    percentage_of_extra_bonus_coins: PercentageOfExtraBonusCoins
    number_of_banana_birds: NumberOfBananaBirds
    percentage_of_banana_birds: PercentageOfBananaBirds

    dk_coins_for_gyrocopter: DKCoinsForGyrocopter
    kongsanity: KONGsanity
    level_shuffle: LevelShuffle
    difficulty: Difficulty

    autosave: Autosave
    merry: MERRY
    music_shuffle: MusicShuffle
    kong_palette_swap: KongPaletteSwap
    starting_life_count: StartingLifeCount
