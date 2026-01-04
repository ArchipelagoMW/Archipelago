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

class TrapLink(Toggle):
    """
    Whether your received traps are linked to other players

    You will also receive any linked traps from other players with Trap Link enabled,
    if you have a weight above "none" set for that trap
    """
    display_name = "Trap Link"


class GoalArea(Choice):
    """
    What Area must be cleared to gain access to the Epilogue and complete the game
    """
    display_name = "Goal Area"
    option_the_summit_a = 0
    option_the_summit_b = 1
    option_the_summit_c = 2
    option_core_a = 3
    option_core_b = 4
    option_core_c = 5
    option_empty_space = 6
    option_farewell = 7
    option_farewell_golden = 8
    default = 0

class LockGoalArea(DefaultOnToggle):
    """
    Determines whether your Goal Area will be locked until you receive your required Strawberries, or only the Epilogue
    """
    display_name = "Lock Goal Area"

class GoalAreaCheckpointsanity(Toggle):
    """
    Determines whether the Checkpoints in your Goal Area will be shuffled into the item pool (if Checkpointsanity is active)
    """
    display_name = "Goal Area Checkpointsanity"

class TotalStrawberries(Range):
    """
    Maximum number of how many Strawberries can exist
    """
    display_name = "Total Strawberries"
    range_start = 0
    range_end = 202
    default = 50

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

class Gemsanity(Toggle):
    """
    Determines whether Summit Gems are shuffled into the item pool
    """
    display_name = "Gemsanity"

class Carsanity(Toggle):
    """
    Determines whether riding on cars grants location checks
    """
    display_name = "Carsanity"

class Roomsanity(Toggle):
    """
    Determines whether entering individual rooms sends location checks
    """
    display_name = "Roomsanity"

class IncludeGoldens(Toggle):
    """
    Determines whether collecting Golden Strawberries sends location checks
    """
    display_name = "Include Goldens"


class IncludeCore(Toggle):
    """
    Determines whether Chapter 8 - Core Levels will be included
    """
    display_name = "Include Core"

class IncludeFarewell(Choice):
    """
    Determines how much of Chapter 9 - Farewell Level will be included
    """
    display_name = "Include Farewell"
    option_none = 0
    option_empty_space = 1
    option_farewell = 2
    default = 0

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


class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required Strawberries in the item pool with junk items
    """
    display_name = "Junk Fill Percentage"
    range_start = 0
    range_end = 100
    default = 50

class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0

class TrapExpirationAction(Choice):
    """
    The type of action which causes traps to wear off
    """
    display_name = "Trap Expiration Action"
    option_return_to_menu = 0
    option_deaths = 1
    option_new_screens = 2
    default = 1

class TrapExpirationAmount(Range):
    """
    The amount of the selected Trap Expiration Action that must occur for the trap to wear off
    """
    display_name = "Trap Expiration Amount"
    range_start = 1
    range_end = 10
    default = 5

class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2

class BaldTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which makes Maddy bald
    """
    display_name = "Bald Trap Weight"

class LiteratureTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the player to read literature
    """
    display_name = "Literature Trap Weight"

class StunTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which briefly stuns Maddy
    """
    display_name = "Stun Trap Weight"

class InvisibleTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which turns Maddy invisible
    """
    display_name = "Invisible Trap Weight"

class FastTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which increases the game speed
    """
    display_name = "Fast Trap Weight"

class SlowTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which decreases the game speed
    """
    display_name = "Slow Trap Weight"

class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the level to become slippery
    """
    display_name = "Ice Trap Weight"

class ReverseTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the controls to be reversed
    """
    display_name = "Reverse Trap Weight"

class ScreenFlipTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the screen to be flipped
    """
    display_name = "Screen Flip Trap Weight"

class LaughterTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes Maddy to laugh uncontrollably
    """
    display_name = "Laughter Trap Weight"

class HiccupTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes Maddy to hiccup uncontrollably
    """
    display_name = "Hiccup Trap Weight"

class ZoomTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the camera to focus on Maddy
    """
    display_name = "Zoom Trap Weight"


class MusicShuffle(Choice):
    """
    Music shuffle type

    None: No Music is shuffled

    Consistent: Each music track is consistently shuffled throughout the game

    Singularity: The entire game uses one song for levels
    """
    display_name = "Music Shuffle"
    option_none = 0
    option_consistent = 1
    option_singularity = 2
    default = 0

class RequireCassettes(Toggle):
    """
    Determines whether you must receive a level's Cassette Item to hear that level's music
    """
    display_name = "Require Cassettes"


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
    option_strawberry = 0xAC3232
    option_empty = 0x44B7FF
    option_double = 0xFF6DEF
    option_golden = 0xFFD65C
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
        Gemsanity,
        Carsanity,
        Roomsanity,
        IncludeGoldens,
        IncludeCore,
        IncludeFarewell,
        IncludeBSides,
        IncludeCSides,
    ]),
    OptionGroup("Junk and Traps", [
        JunkFillPercentage,
        TrapFillPercentage,
        TrapExpirationAction,
        TrapExpirationAmount,
        BaldTrapWeight,
        LiteratureTrapWeight,
        StunTrapWeight,
        InvisibleTrapWeight,
        FastTrapWeight,
        SlowTrapWeight,
        IceTrapWeight,
        ReverseTrapWeight,
        ScreenFlipTrapWeight,
        LaughterTrapWeight,
        HiccupTrapWeight,
        ZoomTrapWeight,
    ]),
    OptionGroup("Aesthetic Options", [
        MusicShuffle,
        RequireCassettes,
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
    trap_link: TrapLink

    goal_area: GoalArea
    lock_goal_area: LockGoalArea
    goal_area_checkpointsanity: GoalAreaCheckpointsanity
    total_strawberries: TotalStrawberries
    strawberries_required_percentage: StrawberriesRequiredPercentage

    junk_fill_percentage: JunkFillPercentage
    trap_fill_percentage: TrapFillPercentage
    trap_expiration_action: TrapExpirationAction
    trap_expiration_amount: TrapExpirationAmount
    bald_trap_weight: BaldTrapWeight
    literature_trap_weight: LiteratureTrapWeight
    stun_trap_weight: StunTrapWeight
    invisible_trap_weight: InvisibleTrapWeight
    fast_trap_weight: FastTrapWeight
    slow_trap_weight: SlowTrapWeight
    ice_trap_weight: IceTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    screen_flip_trap_weight: ScreenFlipTrapWeight
    laughter_trap_weight: LaughterTrapWeight
    hiccup_trap_weight: HiccupTrapWeight
    zoom_trap_weight: ZoomTrapWeight

    checkpointsanity: Checkpointsanity
    binosanity: Binosanity
    keysanity: Keysanity
    gemsanity: Gemsanity
    carsanity: Carsanity
    roomsanity: Roomsanity
    include_goldens: IncludeGoldens
    include_core: IncludeCore
    include_farewell: IncludeFarewell
    include_b_sides: IncludeBSides
    include_c_sides: IncludeCSides

    music_shuffle: MusicShuffle
    require_cassettes: RequireCassettes

    madeline_hair_length: MadelineHairLength
    madeline_one_dash_hair_color: MadelineOneDashHairColor
    madeline_two_dash_hair_color: MadelineTwoDashHairColor
    madeline_no_dash_hair_color: MadelineNoDashHairColor
    madeline_feather_hair_color: MadelineFeatherHairColor
