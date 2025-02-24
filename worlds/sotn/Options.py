from dataclasses import dataclass
from BaseClasses import MultiWorld
from Options import (OptionGroup, Toggle, Choice, Range, FreeText, ItemsAccessibility, StartInventoryPool,
                     PerGameCommonOptions)


class OpenedNO4NO3(Toggle):
    """
        If true, the back door of Underground Caverns will be open
    """
    display_name = "Opened NO4 Backdoor in NP3"


class EarlyOpenedNO4NO3(Toggle):
    """
        If true, the back door of Underground Caverns will be open from the start
    """
    display_name = "Opened NO4 Backdoor in NO3"


class OpenedDAIARE(Toggle):
    """
        If true, the back door of Colosseum will be open
    """
    display_name = "Opened ARE Backdoor"


class Extension(Choice):
    """full: Every location on the map are added to the pool
    relic_prog: Only relics, silver/gold rings, spike breaker and holy glasses locations are added
    guarded: relic_prog + some items behind bosses are locations
    equipment: guarded + most floor equipments are locations"""
    display_name = "Extension"
    option_full = 0
    option_relic_prog = 1
    option_guarded = 2
    option_equipment = 3
    default = 0


class InfiniteWing(Toggle):
    """
        Makes wing smash remains until hit a wall or run out of MP
    """
    display_name = "Infinite wing smash"


class RandomizeNonLocations(Toggle):
    """
        Will randomize items that aren't locations on the seed
    """
    display_name = "Randomize extra items"


class ExtraPool(Toggle):
    """
        Try to add powerful items to the pool: Duplicator, Crissaegrim, Ring of varda, Mablung sword, Masamune, Marsil, Yasutsuna
    """
    display_name = "Add extra items to the pool"


@dataclass
class SOTNOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    start_inventory: StartInventoryPool
    open_no4: OpenedNO4NO3
    early_open_no4: EarlyOpenedNO4NO3
    open_are: OpenedDAIARE
    extension: Extension
    infinite_wing: InfiniteWing
    randomize_items: RandomizeNonLocations
    extra_pool: ExtraPool


sotn_option_groups = [
    OptionGroup("gameplay tweaks", [
        EarlyOpenedNO4NO3, OpenedNO4NO3, OpenedDAIARE, Extension, RandomizeNonLocations
    ]),
    OptionGroup("QOL", [
        InfiniteWing, ExtraPool
    ])
]




