from typing import Dict
from Options import Option, DeathLink, DefaultOnToggle, Range, Choice


class PathOption(Choice):
    """Choose where you would like Hidden Chest and Pedestal checks to be placed.
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
    display_name = "Hidden Chests per Biome"
    range_start = 0
    range_end = 20
    default = 3


class PedestalChecks(Range):
    """Number of checks that will spawn on pedestals in the applicable biomes."""
    display_name = "Pedestal Checks per Biome"
    range_start = 0
    range_end = 20
    default = 6


class Traps(DefaultOnToggle):
    """Whether negative effects on the Noita world are added to the item pool."""
    display_name = "Traps"


class OrbsAsChecks(Choice):
    """Decides whether finding the orbs that naturally spawn in the world count as checks.
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
    The Main Path option includes Gate Guardian, Suomuhauki, and Kolmisilmä.
    The Side Path option includes the Main Path bosses, Sauvojen Tuntija, and Ylialkemisti.
    The All Bosses option includes all 12 bosses."""
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
    Orbs will be added to the randomizer pool according to what victory condition you chose.
    The base game orbs will not count towards these victory conditions."""
    display_name = "Victory Condition"
    option_greed_ending = 0
    option_pure_ending = 1
    option_peaceful_ending = 2
    default = 0


noita_options: Dict[str, type(Option)] = {
    "death_link": DeathLink,
    "bad_effects": Traps,
    "victory_condition": VictoryCondition,
    "path_option": PathOption,
    "hidden_chests": HiddenChests,
    "pedestal_checks": PedestalChecks,
    "orbs_as_checks": OrbsAsChecks,
    "bosses_as_checks": BossesAsChecks,
}
