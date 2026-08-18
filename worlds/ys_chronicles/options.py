"""
Ys I Chronicles - Randomizer Options

Options that players can customize for their randomized game.
"""

from dataclasses import dataclass
from Options import (
    Toggle,
    DefaultOnToggle,
    Choice,
    Range,
    PerGameCommonOptions,
)


class Goal(Choice):
    """
    What is required to complete the game.

    Dark Fact: Defeat Dark Fact (standard ending)
    All Books: Collect all 6 Books of Ys and defeat Dark Fact
    All Bosses: Defeat all bosses 
    """
    display_name = "Goal"
    option_dark_fact = 0
    option_all_books = 1
    option_all_bosses = 2
    default = 0


class ShuffleEquipment(DefaultOnToggle):
    """
    Include weapons, armor, and shields in the item pool.
    If disabled, equipment is found in vanilla locations.
    """
    display_name = "Shuffle Equipment"


class ShuffleRings(DefaultOnToggle):
    """
    Include rings in the item pool.
    """
    display_name = "Shuffle Rings"


class ShuffleKeys(DefaultOnToggle):
    """
    Include keys in the item pool.
    Keys are always progression items.
    """
    display_name = "Shuffle Keys"


class ShuffleQuestItems(DefaultOnToggle):
    """
    Include quest items (Books of Ys, Harmonica, etc.) in the pool.
    """
    display_name = "Shuffle Quest Items"


class ShuffleConsumables(Toggle):
    """
    Include consumable items (Heal Potions, Mirrors) in the pool.
    These become filler items from other players' worlds.
    """
    display_name = "Shuffle Consumables"


class ShuffleShops(DefaultOnToggle):
    """
    Shop purchases are location checks.
    First purchase of each shop item gives the randomized item.
    Subsequent purchases give the vanilla item.
    """
    display_name = "Shuffle Shops"


class BossChecks(DefaultOnToggle):
    """
    Boss kills are location checks that can contain randomized items.
    When enabled, Books of Ys are shuffled into the item pool.
    When disabled, bosses give their vanilla rewards.
    """
    display_name = "Boss Checks"


class BossRandomization(Choice):
    """
    How bosses are handled.

    Vanilla: Bosses appear in their normal locations
    Shuffled: Boss order is randomized (same progression requirements)
    """
    display_name = "Boss Randomization"
    option_vanilla = 0
    option_shuffled = 1
    default = 0


class StartingWeapon(Choice):
    """
    What weapon you start with.

    None: Start with no weapon (hard mode)
    Short Sword: Start with Short Sword (vanilla)
    Long Sword: Start with Long Sword (easier)
    """
    display_name = "Starting Weapon"
    option_none = 0
    option_short_sword = 1
    option_long_sword = 2
    default = 0


class ExperienceMultiplier(Range):
    """
    Multiplier for experience gained from enemies.
    100 = normal, 200 = double, 50 = half
    """
    display_name = "Experience Multiplier"
    range_start = 25
    range_end = 400
    default = 100


class GoldMultiplier(Range):
    """
    Multiplier for gold gained from enemies.
    100 = normal, 200 = double, 50 = half
    """
    display_name = "Gold Multiplier"
    range_start = 25
    range_end = 400
    default = 100


class DeathLink(Toggle):
    """
    When you die, everyone with DeathLink enabled also dies.
    When someone else dies, you die too.
    """
    display_name = "Death Link"


@dataclass
class YsChroniclesOptions(PerGameCommonOptions):
    """Options for Ys I Chronicles randomizer."""

    goal: Goal
    shuffle_equipment: ShuffleEquipment
    shuffle_rings: ShuffleRings
    shuffle_keys: ShuffleKeys
    shuffle_quest_items: ShuffleQuestItems
    shuffle_consumables: ShuffleConsumables
    shuffle_shops: ShuffleShops
    boss_checks: BossChecks
    boss_randomization: BossRandomization
    starting_weapon: StartingWeapon
    experience_multiplier: ExperienceMultiplier
    gold_multiplier: GoldMultiplier
    death_link: DeathLink
