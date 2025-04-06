from dataclasses import dataclass
import random

from Options import Choice, TextChoice, Range, Toggle, DeathLink, OptionGroup, PerGameCommonOptions, OptionError
from worlds.AutoWorld import World


class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink
    """
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 10

class TotalStrawberries(Range):
    """
    How many Strawberries exist
    """
    display_name = "Total Strawberries"
    range_start = 0
    range_end = 55
    default = 20

class StrawberriesRequiredPercentage(Range):
    """
    Percentage of existing Strawberries you must receive to finish
    """
    display_name = "Strawberries Required Percentage"
    range_start = 0
    range_end = 100
    default = 80


class LogicDifficulty(Choice):
    """
    Whether the logic expects you to play the intended way, or to be able to use advanced tricks and skips
    """
    display_name = "Logic Difficulty"
    option_standard = 0
    option_hard = 1
    default = 0

class MoveShuffle(Toggle):
    """
    Whether the following base movement abilities are shuffled into the item pool:
    - Ground Dash
    - Air Dash
    - Skid Jump
    - Climb

    NOTE: Having Move Shuffle and Standard Logic Difficulty will guarantee that one of the four Move items will be immediately accessible

    WARNING: Combining Move Shuffle and Hard Logic Difficulty can require very difficult tricks
    """
    display_name = "Move Shuffle"


class Friendsanity(Toggle):
    """
    Whether chatting with your friends grants location checks
    """
    display_name = "Friendsanity"

class Signsanity(Toggle):
    """
    Whether reading signs grants location checks
    """
    display_name = "Signsanity"

class Carsanity(Toggle):
    """
    Whether riding on cars grants location checks
    """
    display_name = "Carsanity"

class Checkpointsanity(Toggle):
    """
    Whether activating Checkpoints grants location checks

    Activating this will also shuffle items into the pool which allow usage and warping to each Checkpoint
    """
    display_name = "Checkpointsanity"


class ColorChoice(TextChoice):
    option_strawberry = 0xDB2C00
    option_empty = 0x6EC0FF
    option_double = 0xFA91FF
    option_golden = 0xF2D450
    option_baddy = 0x9B3FB5
    option_fire_red = 0xFF0000
    option_maroon = 0x800000
    option_salmon = 0xFF3A65
    option_orange = 0xD86E0A
    option_lime_green = 0x8DF920
    option_bright_green = 0x0DAF05
    option_forest_green = 0x132818
    option_royal_blue = 0x0036BF
    option_brown = 0xB78726
    option_black = 0x000000
    option_white = 0xFFFFFF
    option_grey = 0x808080
    option_any_color = -1

    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            choice_list = list(cls.name_lookup)
            choice_list.remove(cls.option_any_color)
            return cls(random.choice(choice_list))
        return super().from_text(text)


class MadelineOneDashHairColor(ColorChoice):
    """
    What color Madeline's hair is when she has one dash

    The `any_color` option will choose a fully random color

    A custom color entry may be supplied as a 6-character RGB hex color code
    e.g. F542C8
    """
    display_name = "Madeline One Dash Hair Color"
    default = ColorChoice.option_strawberry

class MadelineTwoDashHairColor(ColorChoice):
    """
    What color Madeline's hair is when she has two dashes

    The `any_color` option will choose a fully random color

    A custom color entry may be supplied as a 6-character RGB hex color code
    e.g. F542C8
    """
    display_name = "Madeline Two Dash Hair Color"
    default = ColorChoice.option_double

class MadelineNoDashHairColor(ColorChoice):
    """
    What color Madeline's hair is when she has no dashes

    The `any_color` option will choose a fully random color

    A custom color entry may be supplied as a 6-character RGB hex color code
    e.g. F542C8
    """
    display_name = "Madeline No Dash Hair Color"
    default = ColorChoice.option_empty

class MadelineFeatherHairColor(ColorChoice):
    """
    What color Madeline's hair is when she has a feather

    The `any_color` option will choose a fully random color

    A custom color entry may be supplied as a 6-character RGB hex color code
    e.g. F542C8
    """
    display_name = "Madeline Feather Hair Color"
    default = ColorChoice.option_golden


class BadelineChaserSource(Choice):
    """
    What type of action causes more Badeline Chasers to start spawning

    Locations: The number of locations you've checked contributes to Badeline Chasers

    Strawberries: The number of Strawberry items you've received contributes to Badeline Chasers
    """
    display_name = "Badeline Chaser Source"
    option_locations = 0
    option_strawberries = 1
    default = 0

class BadelineChaserFrequency(Range):
    """
    How many of the `Badeline Chaser Source` actions must occur to make each Badeline Chaser start spawning

    NOTE: Choosing `0` disables Badeline Chasers entirely

    WARNING: Turning on Badeline Chasers alongside Move Shuffle could result in extremely difficult situations
    """
    display_name = "Badeline Chaser Frequency"
    range_start = 0
    range_end = 10
    default = 0

class BadelineChaserSpeed(Range):
    """
    How many seconds behind you each Badeline Chaser will be
    """
    display_name = "Badeline Chaser Speed"
    range_start = 2
    range_end = 10
    default = 3


celeste_64_option_groups = [
    OptionGroup("Goal Options", [
        TotalStrawberries,
        StrawberriesRequiredPercentage,
    ]),
    OptionGroup("Sanity Options", [
        Friendsanity,
        Signsanity,
        Carsanity,
        Checkpointsanity,
    ]),
    OptionGroup("Aesthetic Options", [
        MadelineOneDashHairColor,
        MadelineTwoDashHairColor,
        MadelineNoDashHairColor,
        MadelineFeatherHairColor,
    ]),
    OptionGroup("Badeline Chasers", [
        BadelineChaserSource,
        BadelineChaserFrequency,
        BadelineChaserSpeed,
    ]),
]


@dataclass
class Celeste64Options(PerGameCommonOptions):
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty

    total_strawberries: TotalStrawberries
    strawberries_required_percentage: StrawberriesRequiredPercentage

    logic_difficulty: LogicDifficulty
    move_shuffle: MoveShuffle

    friendsanity: Friendsanity
    signsanity: Signsanity
    carsanity: Carsanity
    checkpointsanity: Checkpointsanity

    madeline_one_dash_hair_color: MadelineOneDashHairColor
    madeline_two_dash_hair_color: MadelineTwoDashHairColor
    madeline_no_dash_hair_color: MadelineNoDashHairColor
    madeline_feather_hair_color: MadelineFeatherHairColor

    badeline_chaser_source: BadelineChaserSource
    badeline_chaser_frequency: BadelineChaserFrequency
    badeline_chaser_speed: BadelineChaserSpeed


def resolve_options(world: World):
    # One Dash Hair
    if isinstance(world.options.madeline_one_dash_hair_color.value, str):
        try:
            world.madeline_one_dash_hair_color = int(world.options.madeline_one_dash_hair_color.value.strip("#")[:6], 16)
        except ValueError:
            raise OptionError(f"Invalid input for option `madeline_one_dash_hair_color`:"
                              f"{world.options.madeline_one_dash_hair_color.value} for "
                              f"{world.player_name}")
    elif world.options.madeline_one_dash_hair_color.value == ColorChoice.option_any_color:
        world.madeline_one_dash_hair_color = world.random.randint(0, 0xFFFFFF)
    else:
        world.madeline_one_dash_hair_color = world.options.madeline_one_dash_hair_color.value

    # Two Dash Hair
    if isinstance(world.options.madeline_two_dash_hair_color.value, str):
        try:
            world.madeline_two_dash_hair_color = int(world.options.madeline_two_dash_hair_color.value.strip("#")[:6], 16)
        except ValueError:
            raise OptionError(f"Invalid input for option `madeline_two_dash_hair_color`:"
                              f"{world.options.madeline_two_dash_hair_color.value} for "
                              f"{world.player_name}")
    elif world.options.madeline_two_dash_hair_color.value == ColorChoice.option_any_color:
        world.madeline_two_dash_hair_color = world.random.randint(0, 0xFFFFFF)
    else:
        world.madeline_two_dash_hair_color = world.options.madeline_two_dash_hair_color.value

    # No Dash Hair
    if isinstance(world.options.madeline_no_dash_hair_color.value, str):
        try:
            world.madeline_no_dash_hair_color = int(world.options.madeline_no_dash_hair_color.value.strip("#")[:6], 16)
        except ValueError:
            raise OptionError(f"Invalid input for option `madeline_no_dash_hair_color`:"
                              f"{world.options.madeline_no_dash_hair_color.value} for "
                              f"{world.player_name}")
    elif world.options.madeline_no_dash_hair_color.value == ColorChoice.option_any_color:
        world.madeline_no_dash_hair_color = world.random.randint(0, 0xFFFFFF)
    else:
        world.madeline_no_dash_hair_color = world.options.madeline_no_dash_hair_color.value

    # Feather Hair
    if isinstance(world.options.madeline_feather_hair_color.value, str):
        try:
            world.madeline_feather_hair_color = int(world.options.madeline_feather_hair_color.value.strip("#")[:6], 16)
        except ValueError:
            raise OptionError(f"Invalid input for option `madeline_feather_hair_color`:"
                              f"{world.options.madeline_feather_hair_color.value} for "
                              f"{world.player_name}")
    elif world.options.madeline_feather_hair_color.value == ColorChoice.option_any_color:
        world.madeline_feather_hair_color = world.random.randint(0, 0xFFFFFF)
    else:
        world.madeline_feather_hair_color = world.options.madeline_feather_hair_color.value

