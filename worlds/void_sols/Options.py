from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Range, Toggle

class EnemyRandomization(DefaultOnToggle):
    """Toggle whether enemies are randomized or vanilla."""

    display_name = "Enemy Randomization"

class StartingWeapon(Choice):
    """Which weapon you start with or randomized"""

    display_name = "Starting Weapon"
    option_sword = 0
    option_dagger = 1
    option_great_hammer = 2
    option_pickaxe = 3
    option_halberd = 4
    option_katana = 5
    option_gauntlets = 6
    option_morningstar = 7
    option_dual_handaxes = 8
    option_scythe = 9
    option_frying_pan = 10
    option_randomized = 11
    default = option_randomized

class SparksChecks(Toggle):
    """ Toggle if Sparks of Light count as checks"""

    display_name = "Sparks of Light Checks"

class TorchChecks(Toggle):
    """ Toggle if Torch count as checks"""

    display_name = "Torch Checks"

class HiddenWallsChecks(Toggle):
    """ Toggle if Hidden Walls count as checks"""

    display_name = "Hidden Walls Checks"

@dataclass
class VoidSolsOptions(PerGameCommonOptions):
    enemy_randomization: EnemyRandomization
    starting_weapon: StartingWeapon
    sparks_checks: SparksChecks
    torch_checks: TorchChecks
    hidden_walls_checks: HiddenWallsChecks