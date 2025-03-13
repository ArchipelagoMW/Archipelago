from dataclasses import dataclass
import random

from Options import Choice, Range, DefaultOnToggle, Toggle, TextChoice, DeathLink, OptionGroup, PerGameCommonOptions, OptionError
from worlds.AutoWorld import World


class DeathLinkAmnesty(Range):
    """
    How many deaths it takes to send a DeathLink
    """
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 10


class GoalArea(Choice):
    """
    What Area must be cleared to gain access to the Epilogue and complete the game
    """
    display_name = "Goal Area"
    option_Summit_A = 0
    option_Core_A = 3
    option_Empty_Space = 6
    option_Farewell = 7
    option_Farewell_Golden = 8
    default = 0

class LockGoalArea(DefaultOnToggle):
    """
    Determines whether your Goal Area will be locked until you receive your required Strawberries, or only the Epilogue
    """
    display_name = "Lock Goal Area"

class GoalAreaCheckpointsanity(Toggle):
    """
    Determines whether the Checkpoints in your Goal Area will be shuffled into the item pool or not
    """
    display_name = "Goal Area Checkpointsanity"

class TotalStrawberries(Range):
    """
    Maximum number of how many Strawberries can exist
    """
    display_name = "Total Strawberries"
    range_start = 0
    range_end = 200
    default = 20

class StrawberriesRequiredPercentage(Range):
    """
    Percentage of existing Strawberries you must receive to access your Goal Area (if Lock Goal Area is active) and the Epilogue
    """
    display_name = "Strawberries Required Percentage"
    range_start = 0
    range_end = 100
    default = 80


class Checkpointsanity(Toggle):
    """
    Determines whether Checkpoints will be shuffled into the item pool
    """
    display_name = "Checkpointsanity"

class Binosanity(Toggle):
    """
    Determines whether using Binoculars sends location checks
    """
    display_name = "Binosanity"

class Keysanity(Toggle):
    """
    Determines whether individual Keys are shuffled into the item pool
    """
    display_name = "Keysanity"

class Roomsanity(Toggle):
    """
    Determines whether entering individual rooms sends location checks
    """
    display_name = "Roomsanity"

class IncludeGoldens(Toggle):
    """
    Determines whether collecting Golden Strawberries sends location checks
    """
    display_name = "Roomsanity"


class IncludeCore(Toggle):
    """
    Determines whether Chapter 8 - Core Levels will be included
    """
    display_name = "Include Core"

class IncludeFarewell(Toggle):
    """
    Determines whether Chapter 9 - Farewell Level will be included
    """
    display_name = "Include Farewell"

class IncludeBSides(Toggle):
    """
    Determines whether the B-Side Levels will be included
    """
    display_name = "Include B-Sides"

class IncludeCSides(Toggle):
    """
    Determines whether the C-Side Levels will be included
    """
    display_name = "Include C-Sides"


class MadelineHairLength(Choice):
    """
    How long Madeline's hair is
    """
    display_name = "Madeline Hair Length"
    option_very_short = 1
    option_short = 2
    option_default = 4
    option_long = 7
    option_very_long = 10
    option_absurd = 20
    default = 4


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



celeste_option_groups = [
    OptionGroup("Goal Options", [
        GoalArea,
        LockGoalArea,
        GoalAreaCheckpointsanity,
        TotalStrawberries,
        StrawberriesRequiredPercentage,
    ]),
    OptionGroup("Location Options", [
        Checkpointsanity,
        Binosanity,
        Keysanity,
        Roomsanity,
        IncludeCore,
        IncludeFarewell,
        IncludeBSides,
        IncludeCSides,
    ]),
    OptionGroup("Aesthetic Options", [
        MadelineHairLength,
        MadelineOneDashHairColor,
        MadelineTwoDashHairColor,
        MadelineNoDashHairColor,
        MadelineFeatherHairColor,
    ]),
]


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


@dataclass
class CelesteOptions(PerGameCommonOptions):
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty

    goal_area: GoalArea
    lock_goal_area: LockGoalArea
    goal_area_checkpointsanity: GoalAreaCheckpointsanity
    total_strawberries: TotalStrawberries
    strawberries_required_percentage: StrawberriesRequiredPercentage

    checkpointsanity: Checkpointsanity
    binosanity: Binosanity
    keysanity: Keysanity
    roomsanity: Roomsanity
    include_goldens: IncludeGoldens
    include_core: IncludeCore
    include_farewell: IncludeFarewell
    include_b_sides: IncludeBSides
    include_c_sides: IncludeCSides

    madeline_hair_length: MadelineHairLength
    madeline_one_dash_hair_color: MadelineOneDashHairColor
    madeline_two_dash_hair_color: MadelineTwoDashHairColor
    madeline_no_dash_hair_color: MadelineNoDashHairColor
    madeline_feather_hair_color: MadelineFeatherHairColor
