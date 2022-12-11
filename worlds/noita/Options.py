from typing import Dict
from Options import Option, DeathLink, DefaultOnToggle, Range, Choice


class TotalLocations(Range):
    """Number of location checks which are added to the playthrough."""
    display_name = "Total Locations"
    range_start = 10
    range_end = 500
    default = 100


class BadEffects(DefaultOnToggle):
    """Negative effects on the Noita world are added to the item pool."""
    display_name = "Bad Times"


class VictoryCondition(Choice):
    """Greed is to get to the bottom, grab the sampo, beat the boss, and enter the portal
    Pure is to get the 11 orbs in the main world, grab the sampo, and bring it to the mountain altar
    Peaceful is to get all 33 orbs in main + parallel, grab the sampo, and bring it to the mountain altar
    Yendor is peaceful but with 34 orbs. Might not keep this one."""
    display_name = "Victory Condition"
    option_victory_greed = 0
    option_victory_pure = 1
    option_victory_peaceful = 2
    option_victory_yendor = 3
    default = 0


class OrbsAsChecks(Choice):
    """fill this in later"""
    display_name = "Orbs as Location Checks"
    option_no_orbs = 0
    option_main_world = 1
    option_parallel_no_lava = 2
    default = 0


class BossesAsChecks(DefaultOnToggle):
    """fill this in later"""
    display_name = "Bosses as Location Checks"


noita_options: Dict[str, type(Option)] = {
    "total_locations": TotalLocations,
    "bad_effects": BadEffects,
    "death_link": DeathLink,
    "victory_condition": VictoryCondition,
    "orbs_as_checks": OrbsAsChecks,
    "bosses_as_checks": BossesAsChecks,
}
