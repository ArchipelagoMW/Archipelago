from typing import Dict
from Options import Option, DeathLink, DefaultOnToggle, Range, Choice, Toggle


class PathOption(Choice):
    """Choose where you would like checks to be placed. This affects which bosses, orbs, and chest checks are enabled.
    Main Path includes the main 7 biomes you typically go through to get to the final boss.
    Side Path includes areas off the main path, but not ones you need to go way out of your way for. 10 biomes total.
    Main World includes the full world (excluding parallel worlds). 15 biomes total."""
    display_name = "Path Option"
    option_main_path = 1
    option_side_path = 2
    option_main_world = 3
    default = 1


class HiddenChests(Range):
    """Number of hidden chest checks added to the applicable biomes."""
    display_name = "Hidden Chest Locations"
    range_start = 0
    range_end = 20
    default = 5


class PedestalChecks(Range):
    """Number of checks that will spawn on pedestals in the applicable biomes."""
    display_name = "Pedestal Checks"  # feel free to rename/redescribe this, edit ranges, etc.
    range_start = 0
    range_end = 20
    default = 5


class Traps(DefaultOnToggle):
    """Whether negative effects on the Noita world are added to the item pool."""
    display_name = "Traps"


class OrbsAsChecks(Choice):  # todo: rework this to work with the paths option
    """Decides whether finding the orbs that naturally spawn in the world count as checks.
    The orbs included is based off of your Path Option choice.
    The Main Path option includes only the floating island and abyss orb room orbs.
    The Side Path option includes the Main Path, magical temple, lukki lair, and lava lake orbs.
    The Main World option includes all 11 orbs."""
    display_name = "Orbs as Location Checks"
    option_no_orbs = 0
    option_main_path = 1
    option_side_path = 2
    option_main_world = 3
    default = 0


class BossesAsChecks(Choice):
    """Makes bosses count as location checks. The boss only needs to die, you do not need the kill credit.
    The Main Path option includes Gate Guardian, Suomuhauki, and Kolmisilma.
    The Side Path option includes the Main Path bosses, Sauvojen Tuntija, and Ylialkemisti.
    The Main World option includes all 12 bosses."""
    display_name = "Bosses as Location Checks"
    option_no_bosses = 0
    option_main_path = 1
    option_side_path = 2
    option_all_bosses = 3
    default = 0


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


noita_options: Dict[str, type(Option)] = {
    "path_option": PathOption,
    "hidden_chests": HiddenChests,
    "pedestal_checks": PedestalChecks,
    "bad_effects": Traps,
    "death_link": DeathLink,
    "orbs_as_checks": OrbsAsChecks,
    "bosses_as_checks": BossesAsChecks,
    "victory_condition": VictoryCondition,
}
