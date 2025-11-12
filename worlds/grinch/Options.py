from dataclasses import dataclass

from Options import (
    FreeText,
    NumericOption,
    Toggle,
    DefaultOnToggle,
    Choice,
    TextChoice,
    Range,
    NamedRange,
    OptionList,
    PerGameCommonOptions,
    OptionSet,
    OptionCounter,
)


class StartingArea(Choice):
    """
    Here, you can select which area you'll start the game with. [NOT IMPLEMENTED]
    Whichever one you pick is the region you'll have access to at the start of the Multiworld.
    """

    option_whoville = 0
    option_who_forest = 1
    option_who_dump = 2
    option_who_lake = 3
    default = 0
    display_name = "Starting Area"


class ProgressiveVacuum(Toggle):  # DefaultOnToggle
    """
    Determines whether you get access to main areas progressively [NOT IMPLEMENTED]

    Enabled: Whoville > Who Forest > Who Dump > Who Lake
    """

    display_name = "Progressive Vacuum Tubes"


class Missionsanity(Choice):
    """
    How mission checks are randomized in the pool [NOT IMPLEMENTED]

    None: Does not add mission checks
    Completion: Only completing the mission gives you a check
    Individual: Individual tasks for one mission, such as individual snowmen squashed, are checks.
    Both: Both individual tasks and mission completion are randomized.
    """

    display_name = "Mission Locations"
    option_none = 0
    option_completion = 1
    option_individual = 2
    option_both = 3
    default = 1


class ExcludeEnvironments(OptionSet):
    """
    Allows entire environments to be entirely removed to ensure you are not logically required to enter the environment
    along with any and all checks that are in that environment too. [NOT IMPLEMENTED]

    WARNING: Removing too many environments may cause generation to fail.

    Valid keys: "Whoville", "Who Forest", "Who Dump", "Who Lake", "Post Office", "Clock Tower", "City Hall",
                  "Ski Resort", "Civic Center", "Minefield", "Power Plant", "Generator Building", "Scout's Hut",
                  "North Shore", "Mayor's Villa", "Sleigh Ride"
    """

    display_name = "Exclude Environments"
    valid_keys = {
        "Whoville",
        "Who Forest",
        "Who Dump",
        "Who Lake",
        "Post Office",
        "Clock Tower",
        "City Hall",
        "Ski Resort",
        "Civic Center",
        "Minefield",
        "Power Plant",
        "Generator Building",
        "Scout's Hut",
        "North Shore",
        "Mayor's Villa",
        "Sleigh Ride",
    }


class ProgressiveGadget(Toggle):  # DefaultOnToggle
    """
    Determines whether you get access to a gadget as individual blueprint count. [NOT IMPLEMENTED]
    """

    display_name = "Progressive Gadgets"


class Supadow(Toggle):
    """
    Enables completing minigames through the Supadows in Mount Crumpit as checks. [NOT IMPLEMENTED]
    """

    display_name = "Supadow Minigames"


class Gifts(Range):
    """
    Considers how many gifts must be squashed per check.
    Enabling this will also enable squashing all gifts in a region mission alongside this. [NOT IMPLEMENTED]
    """

    display_name = "Gifts Squashed per Check"
    range_start = 0
    range_end = 300
    default = 0

class Gadgetrando(DefaultOnToggle):
    """
    Determines whether the Grinch's gadgets will be randomized or not.
    """

    display_name = "Randomize Gadgets"

class Gadgetrandolist(OptionSet):
    """
    If "Randomize Gadgets" is enabled, gadgets that you add to the dictionary will be randomized. [NOT IMPLEMENTED]
    """

    display_name = "Gadgets Randomized"
    default = [
        "Binoculars",
        "Rotten Egg Launcher",
        "Rocket Spring",
        "Slime Shooter",
        "Octopus Climbing Device",
        "Marine Mobile",
        "Grinch Copter",
    ]

class Moverando(Toggle):
    """
    Determines whether the Grinch's moves will be randomized or not.
    """

    display_name = "Randomize Moves"

class Moverandolist(OptionSet):
    """
    If "Randomize Moves" is enabled, the Grinch's moves that you add to the dictionary will be randomized. [NOT IMPLEMENTED]
    """

    display_name = "Moves Randomized"
    default = [
        "Pancake",
        "Bad Breath",
        "Seize",
        "Max",
        "Sneak",
    ]


class UnlimitedEggs(Toggle):
    """
    Determine whether or not you run out of rotten eggs when you utilize your gadgets.
    """

    display_name = "Unlimited Rotten Eggs"


class RingLinkOption(Toggle):
    """
    Whenever this is toggled, your ammo is linked with other ringlink-compatible games that also have this enabled.
    """

    display_name = "Ring Link"


class TrapLinkOption(Toggle):
    """
    If a trap is sent from Grinch, traps that are compatible with other games are triggered as well. [NOT IMPLEMENTED]
    """

    display_name = "Trap Link"

class FillerWeight(OptionCounter):
    """
    Determines which filler is added to the pool. [NOT IMPLEMENTED]
    """

    display_name = "Filler Weights"
    default = {
        "5 Rotten Eggs": 50,
        "10 Rotten Eggs": 25,
        "20 Rotten Eggs": 25,
    }

class TrapPercentage(Range):
    """
    Determines how much filler is replaced with traps. [NOT IMPLEMENTED]
    """

    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 10

class TrapWeight(OptionCounter):
    """
    Determines which traps are replaced with filler in the pool. [NOT IMPLEMENTED]
    """

    display_name = "Trap Weights"
    default = {
        "Dump it to Crumpit": 33,
        "Who sent me back?": 33,
        "Depletion Trap": 34,
    }

@dataclass
class GrinchOptions(PerGameCommonOptions):  # DeathLinkMixin
    starting_area: StartingArea
    progressive_vacuum: ProgressiveVacuum
    missionsanity: Missionsanity
    exclude_environments: ExcludeEnvironments
    progressive_gadget: ProgressiveGadget
    supadow_minigames: Supadow
    giftsanity: Gifts
    gadget_rando: Gadgetrando
    gadgets_to_randomize: Gadgetrandolist
    move_rando: Moverando
    moves_to_randomize: Moverandolist
    unlimited_eggs: UnlimitedEggs
    ring_link: RingLinkOption
    trap_link: TrapLinkOption
    filler_weight: FillerWeight
    trap_percentage: TrapPercentage
    trap_weight: TrapWeight
