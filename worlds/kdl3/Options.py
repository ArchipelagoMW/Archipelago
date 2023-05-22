from Options import Option, DeathLink, Choice, Toggle, OptionDict, Range, PlandoBosses, DefaultOnToggle
import typing
from .Names import LocationName


class Goal(Choice):
    """
    Zero: collect the Heart Stars, and defeat Zero in the Hyper Zone.
    Boss Butch: collect the Heart Stars, and then complete the boss rematches in the Boss Butch mode.
    MG5: collect the Heart Stars, and then complete a perfect run through the minigame gauntlet within the MG5
    Jumping: collect the Heart Stars, and then reach a designated score within the Jumping sub-game
    """
    display_name = "Goal"
    option_zero = 0
    option_boss_butch = 1
    option_mg5 = 2
    option_jumping = 3
    default = 0


class GoalSpeed(Choice):
    """
    Normal: the goal is unlocked after purifying the five bosses
    Fast: the goal is unlocked after acquiring the target number of Heart Stars
    """
    display_name = "Goal Speed"
    option_normal = 0
    option_fast = 1


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
    display_name = "Required Heart Stars"
    range_start = 1
    range_end = 100
    default = 50


class LevelShuffle(Choice):
    """
    None: No stage shuffling.
    Same World: shuffles stages around their world.
    Pattern: shuffles stages according to the stage pattern (stage 3 will always be a minigame stage, etc.)
    Shuffled: shuffles stages across all worlds.
    """
    display_name = "Stage Shuffle"
    option_none = 0
    option_same_world = 1
    option_pattern = 2
    option_shuffled = 3
    default = 0


class BossShuffle(PlandoBosses):
    """
    None: Bosses will remain in their vanilla locations
    Shuffled: Bosses will be shuffled amongst each other
    Singularity: All (non-Zero) bosses will be replaced with a single boss
    Supports plando placement.
    """
    bosses = LocationName.boss_names.keys()

    locations = LocationName.level_names.keys()

    duplicate_bosses = True
    @classmethod
    def can_place_boss(cls, boss: str, location: str) -> bool:
        # Kirby has no logic about requiring bosses in specific locations (since we load in their stage)
        return True

    display_name = "Boss Shuffle"
    option_none = 0
    option_shuffled = 1
    option_full = 2
    option_singularity = 3


class StrictBosses(DefaultOnToggle):
    """
    If enabled, one will not be able to move onto the next world until the previous world's boss has been purified.
    """
    display_name = "Strict Bosses"


class BossRequirementRandom(Toggle):
    """
    If enabled, boss purification will unlock in any order, requiring a random amount of Heart Stars.
    """
    display_name = "Randomize Purification Order"


class JumpingTarget(Range):
    """
    The required score needed to complete the Jumping minigame.
    """
    display_name = "Jumping Target Score"
    range_start = 1
    range_end = 25
    default = 10


class GameLanguage(Choice):
    """
    The language that the game should display. This does not have to match the given rom.
    """
    display_name = "Game Language"
    option_japanese = 0
    option_english = 1
    default = 1


class FillerPercentage(Range):
    """
    Percentage of non-required Heart Stars to be converted to filler items (1-Ups, Maxim Tomatoes, Invincibility Candy).
    """
    display_name = "Filler Percentage"
    range_start = 0
    range_end = 100
    default = 50


class ConsumableChecks(Toggle):
    """
    When enabled, adds all 1-Ups and Maxim Tomatoes as possible locations.
    """
    display_name = "Consumable-sanity"


class KirbyFlavorPreset(Choice):
    """
    The color of Kirby, from a list of presets.
    """
    display_name = "Kirby Flavor"
    option_default = 0
    #option_bubblegum = 1
    #option_cherry = 2
    option_blueberry = 3
    #option_lemon = 4
    #option_lime = 5
    #option_grape = 6
    #option_chocolate = 7
    option_marshmallow = 8
    #option_licorice = 9
    #option_watermelon = 10
    #option_orange = 11
    #option_kiwi = 12
    #option_lavender = 13
    option_custom = 14
    default = 0


class KirbyFlavor(OptionDict):
    """
    A custom color for Kirby.
    """
    default = {}


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
    option_custom = 14
    default = 0


class GooeyFlavor(OptionDict):
    """
    A custom color for Gooey.
    """
    default = {}


kdl3_options: typing.Dict[str, type(Option)] = {
    "death_link": DeathLink,
    "game_language": GameLanguage,
    "goal": Goal,
    "goal_speed": GoalSpeed,
    "total_heart_stars": TotalHeartStars,
    "heart_stars_required": HeartStarsRequired,
    "filler_percentage": FillerPercentage,
    "jumping_target": JumpingTarget,
    "stage_shuffle": LevelShuffle,
    "boss_shuffle": BossShuffle,
    "strict_bosses": StrictBosses,
    "boss_requirement_random": BossRequirementRandom,
    "consumables": ConsumableChecks,
    "kirby_flavor_preset": KirbyFlavorPreset,
    "kirby_flavor": KirbyFlavor,
    "gooey_flavor_preset": GooeyFlavorPreset,
    "gooey_flavor": GooeyFlavor,
}
