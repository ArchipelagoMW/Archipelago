from Options import Choice, Toggle, DeathLink, DefaultOnToggle


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


mm2_options = {
    "death_link": DeathLink,
    "starting_robot_master": StartingRobotMaster,
    "consumables": Consumables,
    "yoku_jumps": YokuJumps,
    "enable_lasers": EnableLasers,
    "quickswap": Quickswap,
}
