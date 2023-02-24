from typing import Dict
from Options import Option, DeathLink, DefaultOnToggle, Range, Choice, Toggle


class TotalLocations(Range):
    """Number of location checks which are added to the playthrough."""
    display_name = "Total Locations"
    range_start = 75
    range_end = 500
    default = 100


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


class OrbsAsChecks(Choice):
    """Decides whether finding the orbs that naturally spawn in the world count as checks.
    The Main Path option includes only the floating island, lava lake, abyss orb room, magical temple, and lukki lair
    orbs. If you are doing the Greed Ending, this option or the No Orbs option are recommended.
    The Main World option makes only orbs found in the main world give checks. Recommended if doing the Pure Ending.
    The Main and Parallel Worlds option makes orbs found in the east and west worlds count too. Recommended if doing the Peaceful Ending.
    Note that the parallel lava lake orbs still do not spawn in the regular game, so there will be 31 orbs total."""
    display_name = "Orbs as Location Checks"
    option_no_orbs = 0
    option_main_path = 1
    option_main_world = 2
    option_main_and_parallel_worlds = 3
    default = 0


class BossesAsChecks(Choice):
    """Makes bosses count as location checks. The boss only needs to die, you do not need the kill credit.
    The Main Path option includes only the Kolmisilma, Sauvojen Tuntija, Ylialkemisti, Suomuhauki, and Gate Guardian."""
    display_name = "Bosses as Location Checks"
    option_no_bosses = 0
    option_main_path = 1
    option_all_bosses = 2
    default = 0


noita_options: Dict[str, type(Option)] = {
    "total_locations": TotalLocations,
    "bad_effects": Traps,
    "death_link": DeathLink,
    "victory_condition": VictoryCondition,
    "orbs_as_checks": OrbsAsChecks,
    "bosses_as_checks": BossesAsChecks,
}
