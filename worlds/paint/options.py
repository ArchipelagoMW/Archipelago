from dataclasses import dataclass

from Options import Range, PerGameCommonOptions, StartInventoryPool, Toggle, Choice, Visibility


class LogicPercent(Range):
    """Sets the maximum percent similarity required for a check to be in logic.
    Higher values are more difficult and items/locations will not be generated beyond this number."""
    display_name = "Logic Percent"
    range_start = 50
    range_end = 95
    default = 80


class GoalPercent(Range):
    """Sets the percent similarity required to achieve your goal.
    If this number is higher than the value for logic percent,
    reaching goal will be in logic upon obtaining all progression items."""
    display_name = "Goal Percent"
    range_start = 50
    range_end = 95
    default = 80


class HalfPercentChecks(Range):
    """Sets the lowest percent at which locations will be created for each 0.5% of similarity.
    Below this number, there will be a check every 1%.
    Above this number, there will be a check every 0.5%."""
    display_name = "Half Percent Checks"
    range_start = 0
    range_end = 95
    default = 50


class QuarterPercentChecks(Range):
    """Sets the lowest percent at which locations will be created for each 0.25% of similarity.
    This number will override Half Percent Checks if it is lower."""
    display_name = "Quarter Percent Checks"
    range_start = 0
    range_end = 95
    default = 70


class CanvasSizeIncrement(Choice):
    """Sets the number of pixels the canvas will expand for each width/height item received.
    Ensure an adequate number of locations are generated if setting this below 50."""
    display_name = "Canvas Size Increment"
    # option_10 = 10
    # option_20 = 20
    option_25 = 25
    option_50 = 50
    option_100 = 100
    default = 100
    visibility = Visibility.none


class CanvasWidthIncrement(Choice):
    """Sets the number of pixels the canvas will expand for each width item received.
    Ensure an adequate number of locations are generated if setting this below 50."""
    display_name = "Canvas Width Increment"
    # option_10 = 10
    # option_20 = 20
    option_25 = 25
    option_50 = 50
    option_100 = 100
    default = 100


class CanvasHeightIncrement(Choice):
    """Sets the number of pixels the canvas will expand for each height item received.
    Ensure an adequate number of locations are generated if setting this below 50."""
    display_name = "Canvas Height Increment"
    # option_10 = 10
    # option_20 = 20
    option_25 = 25
    option_50 = 50
    option_100 = 100
    default = 100


class AspectRatio(Choice):
    """Sets the aspect ratio of your final image. Useful when using a custom goal image, also affects game length.
    Possible options are fullscreen (800x600), widescreen (800x450), square (800x800), fullscreen vertical (600x800),
    and widescreen vertical (450x800)."""
    display_name = "Aspect Ratio"
    option_fullscreen = 0
    option_widescreen = 1
    option_square = 2
    option_fullscreen_vertical = 3
    option_widescreen_vertical = 4
    default = 0


class GoalImage(Range):
    """Sets the numbered image you will be required to match.
    See https://github.com/MarioManTAW/jspaint/tree/master/images/archipelago
    for a list of possible images or choose random.
    This can also be overwritten client-side by using File->Open."""
    display_name = "Goal Image"
    range_start = 1
    range_end = 1
    default = 1
    visibility = Visibility.none


class StartingTool(Choice):
    """Sets which tool (other than Magnifier) you will be able to use from the start."""
    option_brush = 0
    option_pencil = 1
    option_eraser = 2
    option_airbrush = 3
    option_line = 4
    option_rectangle = 5
    option_ellipse = 6
    option_rounded_rectangle = 7
    default = 0


class TrapCount(Range):
    """Sets the percentage of filler items to be replaced by random traps."""
    display_name = "Trap Fill Percent"
    range_start = 0
    range_end = 100
    default = 0


class DeathLink(Toggle):
    """If on, using the Undo or Clear Image functions will send a death to all other players with death link on.
    Receiving a death will clear the image and reset the history.
    This option also prevents Undo and Clear Image traps from being generated in the item pool."""
    display_name = "Death Link"


@dataclass
class PaintOptions(PerGameCommonOptions):
    logic_percent: LogicPercent
    goal_percent: GoalPercent
    half_percent_checks: HalfPercentChecks
    quarter_percent_checks: QuarterPercentChecks
    canvas_size_increment: CanvasSizeIncrement
    canvas_width_increment: CanvasWidthIncrement
    canvas_height_increment: CanvasHeightIncrement
    aspect_ratio: AspectRatio
    goal_image: GoalImage
    starting_tool: StartingTool
    trap_count: TrapCount
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
