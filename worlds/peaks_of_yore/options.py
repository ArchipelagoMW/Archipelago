from Options import Toggle, DefaultOnToggle, DeathLink, Choice, PerGameCommonOptions, StartInventoryPool, OptionGroup
from dataclasses import dataclass


class Goal(Choice):
    """
    Decide what needs to happen to be counted as a win

    - **All Peaks**: Finish all peaks in selected books to win/complete your run
    - **All Artefacts**: Collect all artefacts on selected peaks
    - **All Artefacts All Peaks**: complete both of the above
    - **Time Attack**: Complete All time, rope and hold challenges
    - **All**: all items including bird seeds and ropes
    """
    display_name = "Goal"
    option_all_peaks = 0
    option_all_artefacts = 1
    option_all_artefacts_all_peaks = 2
    option_time_attack = 3
    option_all = 4
    default = 0

class StartingBook(Choice):
    """
    Choose what book to start with. If the book is not enabled, the easiest enabled book will be chosen.

    If the selected book is disabled, a random enabled book will be chosen.
    """
    display_name = "Starting Book"
    option_fundamentals = 0
    option_intermediate = 1
    option_advanced = 2
    option_expert = 3
    default = 0

    def get_selected_book(self) -> str:
        if self.value == 0:
            return "Fundamentals Book"
        elif self.value == 1:
            return "Intermediate Book"
        elif self.value == 2:
            return "Advanced Book"
        return "Expert Book"

class StartWithBarometer(DefaultOnToggle):
    """Choose to start with the barometer, to locate items quicker"""
    display_name = "Start with Barometer"

class StartWithOilLamp(Toggle):
    """
    Choose whether the Aldr Grotto oil lamp is given at the start.
    Also works with the Idol of Sundown.
    """
    display_name = "Start with Oil Lamp"

class StartingHands(Choice):
    """
    Choose what hands you want to have enabled on start.
    WARNING: Setting this to any setting other than *both* can make the game **very** difficult!
    """
    display_name = "Starting Hands"
    option_both = 0
    option_left = 1
    option_right = 2

class EarlyHands(DefaultOnToggle):
    """
    Choose whether the missing hand will be placed earlier in the run.
    """
    display_name = "Early Hands"

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

class IncludeFreeSolo(DefaultOnToggle):
    """Add Free Solo Peaks to the pool"""
    display_name = "Include Free Solo Peaks"

class IncludeTimeAttack(DefaultOnToggle):
    """Adds beating peak time, hold and rope counts as checks"""
    display_name = "Include Time Attack Challenges"


poy_option_groups = [
    OptionGroup("Starting Items", [
        StartingBook,
        StartWithBarometer,
        StartWithOilLamp,
        RopeUnlockMode,
        StartingHands,
        EarlyHands
    ]),
    OptionGroup("Peaks", [
        EnableFundamental,
        EnableIntermediate,
        EnableAdvanced,
        EnableExpert,
        DisableSolemnTempest,
        IncludeFreeSolo,
        IncludeTimeAttack
    ]),
]

poy_option_presets: dict[str, dict[str, any]] = {
    "Challenging": {
        "death_link": True,
        "starting_book": "intermediate",
        "enable_expert": False,
        "start_with_hands": "left",
        "start_with_barometer": False,
        "rope_unlock_mode": "normal",
        "early_hands": True
    },
    "Hard": {
        "goal": "all",
        "death_link": True,
        "starting_book": "random",
        "enable_fundamental": True,
        "enable_intermediate": True,
        "enable_advanced": True,
        "enable_expert": True,
        "disable_solemn_tempest": False,
        "start_with_hands": "left",
        "start_with_barometer": False,
        "rope_unlock_mode": "normal",
        "early_hands": False
    }
}

@dataclass
class PeaksOfYoreOptions(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    starting_book: StartingBook
    start_with_barometer: StartWithBarometer
    start_with_oil_lamp: StartWithOilLamp
    start_with_hands: StartingHands
    early_hands: EarlyHands
    rope_unlock_mode: RopeUnlockMode
    enable_fundamental: EnableFundamental
    enable_intermediate: EnableIntermediate
    enable_advanced: EnableAdvanced
    enable_expert: EnableExpert
    disable_solemn_tempest: DisableSolemnTempest
    include_free_solo: IncludeFreeSolo
    include_time_attack: IncludeTimeAttack
    start_inventory_from_pool: StartInventoryPool

