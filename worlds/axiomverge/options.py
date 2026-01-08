from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Toggle


class Goal(Choice):
    """Victory condition."""
    display_name = "Goal"
    option_athetos = 0
    # option_boss_rush = 1
    # option_gun_hunt = 2
    default = 0


class StartLocation(Choice):
    """
    Changes the initial save room you will spawn in, and the reset to start point.
    WARNING: Later save rooms may have difficulty generating with progressive items.
    """
    display_name = "Randomize start location"
    option_eribu = 0
    option_elsenova = 1
    option_purple_absu = 2
    option_lower_kur = 3
    default = 0

# Item Options
class ProgressiveAddressDisruptor(Choice):
    """
    Combine Address Disruptors into a single progressive upgrade. Can optionally keep bomb seperate.
    """
    option_false = 0
    option_exclude_bomb = 1
    option_true = 2
    display_name = "Progressive Address Disruptor"


class ProgressiveCoat(DefaultOnToggle):
    """Combine Coat upgrades into a single progressive upgrade. Lab -> Trench -> Red."""
    display_name = "Progressive Coat Upgrades"


class ProgressiveDrone(DefaultOnToggle):
    """
    Combine Drone upgrades into a single progressive upgrade. Drone -> Launcher.
    Drone Teleport remains separate.
    """
    display_name = "Progressive Drone Upgrades"


class ShuffleSecretWorldWeapons(DefaultOnToggle):
    """Randomize Secret world weapons into the item pool. Currently not implemented."""


# Logic Options
class AllowDisplacementWarps(Toggle):
    """Allows for displacement warps to be considered in logic."""


class AllowFlight(Toggle):
    """Allows for flying to be considered in logic."""


class AllowRoofGrappleClips(Toggle):
    """Allows for upwards coat dashes with grapple to be considered in logic."""


class AllowWallGrappleClips(Choice):
    """
    Allows for grapple clips through 1 width walls to be considered in logic.

    Swing: Include all 5 height walls (Extend grapple and swing to clip through wall)
    All: Include walls of any height
    """

    option_off = 0
    option_swing = 1
    option_all = 2


class AllowFloorGrappleClips(Toggle):
    """Allows for grapple clips through floors to be considered in logic."""


class AllowRocketJumps(Choice):
    """Allows for rocket jumps to be considered in logic."""

    option_off = 0
    option_brown = 1
    option_red = 2
    option_both = 3


class AllowObscureSkips(Toggle):
    """
    Allow for unintended/difficult to find progression paths.

    For example, using coats to pass bomb checks, or grappling along an uneven roof.
    """


class RequireNodes(DefaultOnToggle):
    """
    Disable any node requirements on transitions/items.

    WARNING: This may require you to do later game checks with little health/damage. Disable at own risk!
    """


@dataclass
class AxiomVergeOptions(PerGameCommonOptions):
    allow_displacement_warps: AllowDisplacementWarps
    allow_flight: AllowFlight
    allow_floor_grapple_clips: AllowFloorGrappleClips
    allow_roof_grapple_clips: AllowRoofGrappleClips
    allow_rocket_jumps: AllowRocketJumps
    allow_wall_grapple_clips: AllowWallGrappleClips
    allow_obscure_skips: AllowObscureSkips
    goal: Goal
    progressive_address_disruptor: ProgressiveAddressDisruptor
    progressive_coat: ProgressiveCoat
    progressive_drone: ProgressiveDrone
    secret_world_weapons: ShuffleSecretWorldWeapons
    require_nodes: RequireNodes
    start_location: StartLocation
