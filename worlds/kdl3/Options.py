from Options import Option, DeathLink, Choice, DefaultOnToggle, OptionDict, Range
import typing


class Goal(Choice):
    """
    Zero: collect the Heart Stars, purify the five bosses, and defeat Zero in the Hyper Zone.
    Boss Butch: purify the five bosses, and then complete the boss rematches in the Boss Butch mode.
    """
    display_name = "Goal"
    option_zero = 0
    option_boss_butch = 1
    default = 0


class TotalHeartStars(Range):
    """
    Total number of heart stars to include in the pool of items.
    """
    display_name = "Total Heart Stars"
    range_start = 1
    range_end = 50  # 30 default locations + 30 stage clears + 5 bosses - 14 progression items = 51, so round down
    default = 30


class HeartStarsRequired(Range):
    """
    Percentage of heart stars required to purify the five bosses and reach Zero.
    Each boss will require a differing amount of heart stars to purify.
    """
    display_name = "Max Heart Stars"
    range_start = 1
    range_end = 100
    default = 50


class LevelShuffle(Choice):
    """
    None: No level shuffling.
    Same World: shuffles levels around their world.
    Shuffled: shuffles levels across all worlds.
    """
    display_name = "Level Shuffle"
    option_none = 0
    option_same_world = 1
    option_shuffled = 2
    default = 0


class GameLanguage(Choice):
    """
    The language that the game should display. This does not have to match the given rom.
    """
    option_japanese = 0
    option_english = 1
    default = 1


class FillerPercentage(Range):
    """
    Percentage of non-required Heart Stars to be converted to filler items (1-Ups, Maxim Tomatoes, Invincibility Candy).
    """
    range_start = 0
    range_end = 100
    default = 50


class KirbyFlavorPreset(Choice):
    """
    The color of Kirby, from a list of presets.
    """
    display_name = "Kirby Flavor"
    #option_default = 0
    #option_bubblegum = 1
    #option_cherry = 2
    option_blueberry = 3
    #option_lemon = 4
    #option_lime = 5
    #option_grape = 6
    #option_chocolate = 7
    #option_marshmallow = 8
    #option_licorice = 9
    #option_watermelon = 10
    #option_orange = 11
    #option_kiwi = 12
    #option_lavender = 13
    default = 0

# class KirbyFlavor(OptionDict):
    """
    A custom color for Kirby.
    """


class GooeyFlavorPreset(Choice):
    """
    The color of Gooey, from a list of presets.
    """
    display_name = "Gooey Flavor"
    option_default = 0
    #option_bubblegum = 1
    #option_cherry = 2
    option_blueberry = 3
    #option_lemon = 4
    #option_lime = 5
    #option_grape = 6
    #option_chocolate = 7
    #option_marshmallow = 8
    #option_licorice = 9
    #option_watermelon = 10
    #option_orange = 11
    #option_kiwi = 12
    #option_lavender = 13
    default = 0


kdl3_options: typing.Dict[str, type(Option)] = {
    "death_link": DeathLink,
    "game_language": GameLanguage,
    "goal": Goal,
    "total_heart_stars": TotalHeartStars,
    "heart_stars_required": HeartStarsRequired,
    "filler_percentage": FillerPercentage,
    "kirby_flavor_preset": KirbyFlavorPreset,
    # "kirby_flavor": KirbyFlavor,
    "gooey_flavor_preset": GooeyFlavorPreset,
}
