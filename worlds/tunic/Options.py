import typing

from Options import DefaultOnToggle, Toggle, StartInventoryPool, Choice, AssembleOptions, Range


class SwordProgression(DefaultOnToggle):
    """Adds four sword upgrades to the item pool that will progressively grant stronger melee weapons, including two new
    swords with increased range and attack power."""
    display_name = "Sword Progression"


class StartWithSword(Toggle):
    """Start with a sword in the player's inventory. Does not count towards Sword Progression."""
    display_name = "Start With Sword"


class KeysBehindBosses(Toggle):
    """Places the three hexagon keys behind their respective boss fight in your world."""
    display_name = "Keys Behind Bosses"


class AbilityShuffling(Toggle):
    """Locks the usage of Prayer, Holy Cross*, and Ice Rod until the relevant pages of the manual have been found.
        If playing with Hexagon Quest, abilities are instead randomly unlocked after obtaining 5, 10, and 15 Gold Hexagons.
        *Certain Holy Cross usages are still allowed, such as the free bomb codes, the seeking spell, and other player-facing codes.
    """
    display_name = "Ability Shuffling"


class FoolTraps(Choice):
    """Replaces low-to-medium value money rewards in the item pool with fool traps, which cause random negative
    effects to the player."""
    display_name = "Fool Traps"
    option_off = 0
    option_normal = 1
    option_double = 2
    option_onslaught = 3
    default = 1


class HexagonQuest(Toggle):
    """An alternate goal that shuffles Gold "Questagon" items into the item pool and allows the game to be completed after
    collecting the required number of them."""
    display_name = "Hexagon Quest"


class HexagonGoal(Range):
    """How many Gold Questagons are required to complete the game on Hexagon Quest."""
    display_name = "Gold Hexagons Required"
    range_start = 15
    range_end = 50
    default = 20


class ExtraHexagonPercentage(Range):
    """How many extra Gold Questagons are shuffled into the item pool, taken as a percentage of the goal amount."""
    display_name = "Percentage of Extra Gold Hexagons"
    range_start = 0
    range_end = 100
    default = 50


tunic_options: typing.Dict[str, AssembleOptions] = {
    "sword_progression": SwordProgression,
    "start_with_sword": StartWithSword,
    "keys_behind_bosses": KeysBehindBosses,
    "ability_shuffling": AbilityShuffling,
    "fool_traps": FoolTraps,
    "hexagon_quest": HexagonQuest,
    "hexagon_goal": HexagonGoal,
    "extra_hexagon_percentage": ExtraHexagonPercentage,
    "start_inventory_from_pool": StartInventoryPool,
}
