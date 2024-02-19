from dataclasses import dataclass

from Options import Choice, Toggle, DeathLink, DefaultOnToggle, TextChoice, Range, PerGameCommonOptions


class StartingRobotMaster(Choice):
    """
    The initial stage unlocked at the start.
    """
    display_name = "Starting Robot Master"
    option_heat_man = 0
    option_air_man = 1
    option_wood_man = 2
    option_bubble_man = 3
    option_quick_man = 4
    option_flash_man = 5
    option_metal_man = 6
    option_crash_man = 7
    default = "random"


class YokuJumps(Toggle):
    """
    When enabled, the player is expected to be able to perform the yoku block sequence in Heat Man's
    stage without any of the Items.
    """


class EnableLasers(Toggle):
    """
    When enabled, the player is expected to complete (and acquire items within) the laser sections of Quick Man's
    stage without the Time Stopper.
    """


class Consumables(DefaultOnToggle):
    """
    When enabled, e-tanks/1-ups/health/weapon energy will be added to the pool of items and included as checks.
    """


class Quickswap(DefaultOnToggle):
    """
    When enabled, the player can quickswap through all received weapons by pressing Select.
    """


class PaletteShuffle(TextChoice):
    """
    Change the color of Mega Man and the Robot Masters.
    None: The palettes are unchanged.
    Shuffled: Palette colors are shuffled amongst the robot masters.
    Randomized: Random (usually good) palettes are generated for each robot master.
    Singularity: one palette is generated and used for all robot masters.
    Supports custom palettes using HTML named colors in the
    following format: Mega Buster-Lavender|Violet;randomized
    The first value is the character whose palette you'd like to define, then separated by - is a set of 2 colors for
    that character. separate every color with a pipe, and separate every character as well as the remaining shuffle with
    a semicolon.
    """
    display_name = "Palette Shuffle"
    option_none = 0
    option_shuffled = 1
    option_randomized = 2
    option_singularity = 3

    """
    Valid Targets:
    Mega Buster
    Atomic Fire
    Air Shooter
    Leaf Shield
    Bubble Lead
    Quick Boomerang
    Metal Blade
    Crash Bomber
    Time Stopper
    Heat Man
    Air Man
    Wood Man
    Bubble Man
    Metal Man
    Quick Man
    Flash Man
    Crash Man
    """


class StrictWeaknesses(Toggle):
    """Only your starting Robot Master will take damage from the Mega Buster, the rest must be defeated with weapons.
    Weapons that only do 1 damage to bosses no longer deal damage (aside from Alien)."""
    display_name = "Strict Weaknesses"


class RandomWeaknesses(Toggle):
    """Randomize boss weaknesses."""
    display_name = "Random Weaknesses"


class Wily5Requirement(Range):
    """Change the amount of Robot Masters that are required to be defeated for
    the teleporter to the Wily Machine to appear."""
    default = 8
    range_start = 1
    range_end = 8

@dataclass
class MM2Options(PerGameCommonOptions):
    death_link: DeathLink
    starting_robot_master: StartingRobotMaster
    consumables: Consumables
    yoku_jumps: YokuJumps
    enable_lasers: EnableLasers
    quickswap: Quickswap
    palette_shuffle: PaletteShuffle
    strict_weakness: StrictWeaknesses
    random_weakness: RandomWeaknesses
    wily_5_requirement: Wily5Requirement
