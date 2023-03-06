from typing import Dict
from Options import Option, DeathLink, DefaultOnToggle, Range, Choice, Toggle


class TotalLocations(Range):
    """Number of location checks which are added to the playthrough."""
    display_name = "Total Locations"
    range_start = 75
    range_end = 500
    default = 100


class HiddenChests(Range):
    """Number of hidden chest checks added to the applicable biomes."""
    display_name = "Hidden Chest Locations"
    range_start = 0
    range_end = 20
    default = 5


class Traps(DefaultOnToggle):
    """Whether negative effects on the Noita world are added to the item pool."""
    display_name = "Traps"


class VictoryCondition(Choice):
    """Greed is to get to the bottom, beat the boss, and win the game.
    Pure is to get the 11 orbs in the main world, grab the sampo, and bring it to the mountain altar.
    Peaceful is to get all 33 orbs in main + parallel, grab the sampo, and bring it to the mountain altar.
    Please note that the orbs will be placed in the archipelago item pool -- the regular orbs will not count for this."""
    display_name = "Victory Condition"
    option_greed_ending = 0
    option_pure_ending = 1
    option_peaceful_ending = 2
    default = 0


class PathOption(Choice):
    """Choose where you would like checks to be placed. This affects which bosses, orbs, and chest checks are enabled.
    Main Path includes the main 7 biomes you typically go through to get to the final boss and .
    Side Path includes areas off the main path, but not ones you need to go way out of your way for.
    Main World includes the full world (excluding parallel worlds)."""
    display_name = "Path Option"
    option_main_path = 1
    option_side_path = 2
    option_main_world = 3
    default = 1


class OrbsAsChecks(Toggle):  # todo: rework this to work with the paths option
    """Decides whether finding the orbs that naturally spawn in the world count as checks.
    The orbs included is based off of your Path Option choice.
    The Main Path option includes only the floating island and abyss orb room orbs.
    The Side Path option includes the Main Path, magical temple, lukki lair, and lava lake orbs.
    The Main World option includes all 11 orbs."""
    display_name = "Orbs as Location Checks"


class BossesAsChecks(Toggle):  # todo: rework this to work with the paths option
    """Makes bosses count as location checks. The boss only needs to die, you do not need the kill credit.
    The Main Path option includes Gate Guardian, Suomuhauki, and Kolmisilma.
    The Side Path option includes the Main Path bosses, Sauvojen Tuntija, and Ylialkemisti.
    The Main World option includes all 12 bosses."""
    display_name = "Bosses as Location Checks"


noita_options: Dict[str, type(Option)] = {
    "total_locations": TotalLocations,
    "bad_effects": Traps,
    "death_link": DeathLink,
    "victory_condition": VictoryCondition,
    "path_option": PathOption,
    "orbs_as_checks": OrbsAsChecks,
    "bosses_as_checks": BossesAsChecks,
}
