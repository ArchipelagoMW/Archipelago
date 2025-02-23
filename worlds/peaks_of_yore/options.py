from Options import Toggle, DefaultOnToggle, DeathLink, Choice, PerGameCommonOptions, StartInventoryPool, OptionGroup
from dataclasses import dataclass


class Goal(Choice):
    """
    Decide what needs to happen to be counted as a win

    - **All Peaks**: Finish all peaks in selected books to win/complete your run
    - **All Artefacts**: Collect all artefacts on selected peaks
    - **All Artefacts All Peaks**: complete both of the above
    - **All**: all items including bird seeds and ropes
    """
    display_name = "Goal"
    option_all_peaks = 0
    option_all_artefacts = 1
    option_all_artefacts_all_peaks = 2
    option_all = 3
    default = 0


class StartingBook(Choice):
    """
    Choose what book to start with. If the book is not enabled, the easiest enabled book will be chosen.

    - **Random Book** will choose a random book from the enabled options."""
    display_name = "Starting Book"
    option_fundamentals = 0
    option_intermediate = 1
    option_advanced = 2
    option_expert = 3
    option_random_book = 4
    default = 0


class StartWithBarometer(DefaultOnToggle):
    """Choose to start with the barometer, to locate items quicker"""
    display_name = "Start with Barometer"


class StartWithOilLamp(Toggle):
    """
    Choose whether the Aldr Grotto oil lamp is given at the start.
    Also works with the Idol of Sundown.
    """
    display_name = "Start with Oil Lamp"


class RopeUnlockMode(Choice):
    """
    Choose when the rope unlock item is given

    - **Instant**: Unlock ropes as soon as you receive them
    - **Early**: Try to unlock the item early on in the game
    - **Normal**: Do not put rope unlock earlier and randomise it like any other item
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
    """Removes Solemn Tempest from the locations pool, has no effect if **Enable Expert Peaks** is disabled"""
    display_name = "Disable Solemn Tempest"


poy_option_groups = [
    OptionGroup("Starting Items", [
        StartingBook,
        StartWithBarometer,
        StartWithOilLamp,
        RopeUnlockMode
    ]),
    OptionGroup("Peaks", [
        EnableFundamental,
        EnableIntermediate,
        EnableAdvanced,
        EnableExpert,
        DisableSolemnTempest
    ]),
]


@dataclass
class PeaksOfYoreOptions(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    starting_book: StartingBook
    start_with_barometer: StartWithBarometer
    start_with_oil_lamp: StartWithOilLamp
    rope_unlock_mode: RopeUnlockMode
    enable_fundamental: EnableFundamental
    enable_intermediate: EnableIntermediate
    enable_advanced: EnableAdvanced
    enable_expert: EnableExpert
    disable_solemn_tempest: DisableSolemnTempest
    start_inventory_from_pool: StartInventoryPool
