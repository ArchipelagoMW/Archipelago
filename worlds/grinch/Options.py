from dataclasses import dataclass

from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionList, \
    PerGameCommonOptions, OptionSet

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

class ProgressiveVacuum(Toggle):#DefaultOnToggle
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
    Allows entire environments to be an excluded location to ensure you are not logically required to enter the environment along
    with any and all checks that are in that environment too. WARNING: Excluding too many environments may cause generation to fail.
    [NOT IMPLEMENTED]

    Valid keys: "Whoville", "Who Forest", "Who Dump", "Who Lake", "Post Office", "Clock Tower", "City Hall",
                  "Ski Resort", "Civic Center", "Minefield", "Power Plant", "Generator Building", "Scout's Hut",
                  "North Shore", "Mayor's Villa", "Sleigh Ride"

    """
    display_name = "Exclude Environments"
    valid_keys = {"Whoville", "Who Forest", "Who Dump", "Who Lake", "Post Office", "Clock Tower", "City Hall",
                  "Ski Resort", "Civic Center", "Minefield", "Power Plant", "Generator Building", "Scout's Hut",
                  "North Shore", "Mayor's Villa", "Sleigh Ride"}

class ProgressiveGadget(Toggle):#DefaultOnToggle
    """
    Determines whether you get access to a gadget as individual blueprint count. [NOT IMPLEMENTED]
    """
    display_name = "Progressive Gadgets"

class Supadow(Toggle):
    """Enables completing minigames through the Supadows in Mount Crumpit as checks. NOT IMPLEMENTED]"""
    display_name = "Supadow Minigames"

class Gifts(Range):
    """
    Considers how many gifts must be squashed per check.
    Enabling this will also enable squashing all gifts in a region mission along side this. [NOT IMPLEMENTED]"""
    display_name = "Gifts Squashed per Check"
    range_start = 0
    range_end = 300
    default = 0

class GadgetRando(OptionSet):
    """
    Randomizes Grinch's gadgets along with randomizing Binoculars into the pool. [NOT IMPLEMENTED]

    Valid keys: "Binoculars", "Rotten Egg Launcher", "Rocket Spring", "Slime Shooter", "Octopus Climbing Device",
                "Marine Mobile", "Grinch Copter"
    """
    display_name = "Gadgets Randomized"
    valid_keys = {"Binoculars", "Rotten Egg Launcher", "Rocket Spring", "Slime Shooter", "Octopus Climbing Device",
                "Marine Mobile", "Grinch Copter"}

class Moverando(OptionSet):
    """Randomizes Grinch's moveset along with randomizing max into the pool. [NOT IMPLEMENTED]

    Valid keys: "Pancake", "Push & Pull", "Max", "Bad Breath", "Tip Toe"
    """
    display_name = "Moves Randomized"
    valid_keys = {"Pancake", "Push & Pull", "Max", "Bad Breath", "Tip Toe"}

class UnlimitedEggs(Toggle):
    """Determine whether or not you run out of rotten eggs when you utilize your gadgets."""
    display_name = "Unlimited Rotten Eggs"

class RingLinkOption(Toggle):
    """Whenever this is toggled, your ammo is linked with other ringlink-compatible games that also have this enabled."""
    display_name = "Ring Link"

class TrapLinkOption(Toggle):
    """If a trap is sent from Grinch, traps that are compatible with other games are triggered as well. [NOT IMPLEMENTED]"""
    display_name = "Trap Link"

@dataclass
class GrinchOptions(PerGameCommonOptions):#DeathLinkMixin
    starting_area: StartingArea
    progressive_vacuum: ProgressiveVacuum
    missionsanity: Missionsanity
    exclude_environments: ExcludeEnvironments
    progressive_gadget: ProgressiveGadget
    supadow_minigames: Supadow
    giftsanity: Gifts
    move_rando: Moverando
    unlimited_eggs: UnlimitedEggs
    ring_link: RingLinkOption
    trap_link: TrapLinkOption
