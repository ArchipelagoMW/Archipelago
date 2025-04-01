from dataclasses import dataclass
from BaseClasses import MultiWorld
from Options import (OptionGroup, Toggle, Choice, Range, FreeText, ItemsAccessibility, StartInventoryPool,
                     PerGameCommonOptions)


class OpenedNO4NO3(Choice):
    """Determines the behavior for the back door from Entrance to Underground Cavern
    closed: The door will be closed as in vanilla
    open: The door will be open after reaching Alchemy Laboratory, ensuring the Death cutscene
    open_early: The door will be open from the start, allowing you to break the Death cutscene"""
    display_name = "Opened NO4 Backdoor"
    option_closed = 0
    option_open = 1
    option_open_early = 2
    default = 0


class OpenedDAIARE(Toggle):
    """
        If true, the back door from Chapel to Colosseum will be open
    """
    display_name = "Opened ARE Backdoor"


class Extension(Choice):
    """relic_prog: Only relics, silver/gold rings, spike breaker and holy glasses locations are checks
    guarded: All of the above, plus most items guarded by bosses
    equipment: All of the above, plus most floor equipment
    full: Every location on the map is added to the pool"""
    display_name = "Item pool"
    option_relic_prog = 0
    option_guarded = 1
    option_equipment = 2
    option_full = 3
    default = 3


class InfiniteWing(Toggle):
    """
        Makes wing smash continue until you hit a wall or run out of MP (cancellable by exiting bat form)
    """
    display_name = "Infinite wing smash"


class RandomizeNonLocations(Toggle):
    """
        Will randomize items not chosen from the item_pool setting
    """
    display_name = "Randomize extra items"


class ExtraPool(Toggle):
    """
        Try to add powerful items to the pool: Duplicator, Crissaegrim, Ring of varda, Mablung sword, Masamune, Marsil, Yasutsuna
    """
    display_name = "Powerful items"


class BossLocations(Toggle):
    """Boss drops would be part of the seed pool."""
    display_name = "Make boss drops part of the pool"


class Enemysanity(Toggle):
    """Hitting an enemy becomes a check. Extra locations will be added based on difficult
    easy: Duplicate relics and progression items adds 50 extra vessels and random equipments
    normal: Duplicate progression items adds 35 extra vessels and random equipments
    hard: 15 extra vessels and random equipments"""
    display_name = "Enemysanity"


class EnemyScroll(Toggle):
    """Enemysanity require Faerie Scroll"""
    display_name = "Enemysanity require Spirit Orb"


class Difficult(Choice):
    """easy: 50% less monster HP and attack, 50% more XP and drop chance increased
    normal: All vanilla stats
    hard: 25% more monster HP and attack, 25% less XP
    very_hard: 50% more monster HP and attack, 50% less XP"""
    display_name = "Difficult"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_very_hard = 3
    default = 1


class XpModifier(Range):
    """Modifier for monster XP, override difficult preset
    Any number above 100 increase the attribute and bellow decrease"""
    display_name = "XP modifier"
    range_start = 0
    range_end = 500
    default = 0


class AtkModifier(Range):
    """Modifier for monster attack, override difficult preset
    Any number above 100 increase the attribute and bellow decrease"""
    display_name = "Attack modifier"
    range_start = 0
    range_end = 500
    default = 0


class HPModifier(Range):
    """Modifier for monster HP, override difficult preset
    Any number above 100 increase the attribute and bellow decrease"""
    display_name = "HP modifier"
    range_start = 0
    range_end = 500
    default = 0


class DropModifier(Choice):
    """Modifier for monster drop, override difficult preset"""
    display_name = "Drop modifier"
    option_normal = 0
    option_increased = 1
    option_abundant = 2
    default = 0


class RandomStartGear(Toggle):
    """Randomize starting equipment"""
    display_name = "Randomize starting equipment"


class DeathLink(Toggle):
    """When you die, everyone who enabled death link dies. Of course, the reverse is true too."""
    display_name = "Death link"


@dataclass
class SOTNOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    start_inventory: StartInventoryPool
    open_no4: OpenedNO4NO3
    open_are: OpenedDAIARE
    item_pool: Extension
    infinite_wing_smash: InfiniteWing
    randomize_items: RandomizeNonLocations
    powerful_items: ExtraPool
    boss_locations: BossLocations
    enemysanity: Enemysanity
    enemy_scroll: EnemyScroll
    difficult: Difficult
    xp_mod: XpModifier
    atk_mod: AtkModifier
    hp_mod: HPModifier
    drop_mod: DropModifier
    rng_start_gear: RandomStartGear
    death_link: DeathLink


sotn_option_groups = [
    OptionGroup("gameplay tweaks", [
        OpenedNO4NO3, OpenedDAIARE, Extension, RandomizeNonLocations, Enemysanity, EnemyScroll, Difficult, XpModifier,
        AtkModifier, HPModifier, DropModifier, RandomStartGear, DeathLink
    ]),
    OptionGroup("QOL", [
        InfiniteWing, ExtraPool, BossLocations
    ])
]




