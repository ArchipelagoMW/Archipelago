from Options import Toggle, DefaultOnToggle, DeathLink, Choice, PerGameCommonOptions, StartInventoryPool
from dataclasses import dataclass


class Goal(Choice):
    """
    Decide what needs to happen to be counted as a win

    **all peaks**: Finish all peaks in selected books to win/complete your run
    **all artefacts**: Collect all artefacts on selected peaks
    **all artefacts all peaks**: complete both of the above
    **all**: all items including bird seeds and ropes
    """
    display_name = "Goal"
    option_all_peaks = 0
    option_all_artefacts = 1
    option_all_artefacts_all_peaks = 2
    option_all = 3
    default = 0


class StartingBook(Choice):
    """Choose what book to start with. If the book is not enabled, the easiest enabled book will be chosen"""
    display_name = "Starting Book"
    option_fundamentals = 0
    option_intermediate = 1
    option_advanced = 2
    option_expert = 3
    default = 0


class StartWithBarometer(DefaultOnToggle):
    """Choose to start with the barometer, to locate items quicker"""
    display_name = "Start With Barometer"


class RopeUnlockMode(Choice):
    """
    Choose when the rope unlock item is given

    instant: Unlock ropes as soon as you receive them
    early: Try to unlock the item early on in the game
    normal: Do not put rope unlock earlier and randomise it like any other item
    """
    display_name = "Rope Unlock Mode"
    option_instant = 0
    option_early = 1
    option_normal = 2
    default = 1


class EnableFundamental(DefaultOnToggle):
    """Enables Fundamentals book, items and collectibles"""
    display_name = "Fundamental Peaks"


class EnableIntermediate(DefaultOnToggle):
    """Enables Intermediate book, items and collectibles"""
    display_name = "Intermediate Peaks"


class EnableAdvanced(DefaultOnToggle):
    """Enables Advanced book, items and collectibles"""
    display_name = "Advanced Peaks"


class EnableExpert(DefaultOnToggle):
    """Enables Expert book, items and collectibles"""
    display_name = "Expert Peaks"


class DisableSolemnTempest(DefaultOnToggle):
    """Removes Solemn Tempest from the locations pool, has no effect if \"Enable Expert Peaks\" is disabled"""
    display_name = "Disable Solemn Tempest"


@dataclass
class PeaksOfYoreOptions(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    starting_book: StartingBook
    start_with_barometer: StartWithBarometer
    rope_unlock_mode: RopeUnlockMode
    enable_fundamental: EnableFundamental
    enable_intermediate: EnableIntermediate
    enable_advanced: EnableAdvanced
    enable_expert: EnableExpert
    disable_solemn_tempest: DisableSolemnTempest
    start_inventory_from_pool: StartInventoryPool
