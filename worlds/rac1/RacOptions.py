from dataclasses import dataclass

from Options import (Choice, PerGameCommonOptions, StartInventoryPool, Toggle)


class StartingWeapons(Choice):
    """Randomize what two weapons you start the game with.
    Vanilla: Start with the Lancer and Gravity Bomb.
    Balanced: Start with two random weapons that are relatively balanced.
    Non-Broken: Start with two random weapons besides RYNO II and Zodiac.
    Unrestricted: Start with any two non-upgraded weapons.
    """
    display_name = "Starting Weapons"
    option_vanilla = 0
    option_balanced = 1
    option_non_broken = 2
    option_unrestricted = 3
    default = 0


class EnableBoltMultiplier(Toggle):
    """Enables the bolt multiplier feature without being in New Game+."""
    display_name = "Enable Bolt Multiplier"


class ExtendWeaponProgression(Toggle):
    """If enabled, make all weapon tiers obtainable through weapon experience. This means LV2 (orange) weapons can
    upgrade into LV3 (yellow) weapons, which can then upgrade into LV4 (blue) weapons.
    This effectively makes all weapons that are usually restricted to NG+ available with enough grinding."""
    display_name = "Extended Weapon Progression"


@dataclass
class RacOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    # death_link: DeathLink
    # starting_weapons: StartingWeapons
    # enable_bolt_multiplier: EnableBoltMultiplier
    # extend_weapon_progression: ExtendWeaponProgression
