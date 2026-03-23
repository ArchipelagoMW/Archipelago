from Options import Toggle, DefaultOnToggle, DeathLink, Choice, PerGameCommonOptions, StartInventoryPool, OptionGroup, \
    TextChoice, T, OptionError
from dataclasses import dataclass

class PeakChoice(Choice):
    option_greenhorns_top = 0
    option_paltry_peak = 1
    option_old_mill = 2
    option_gray_gully = 3
    option_lighthouse = 4
    option_old_man_of_sjor = 5
    option_giants_shelf = 6
    option_evergreens_end = 7
    option_the_twins = 8
    option_old_groves_skelf = 9
    option_lands_end = 10
    option_hangmans_leap = 11
    option_old_langr = 12
    option_aldr_grotto = 13
    option_three_brothers = 14
    option_walters_crag = 15
    option_great_crevice = 16
    option_old_hagger = 17
    option_ugsome_storr = 18
    option_wuthering_crest = 19
    option_porters_boulder = 20
    option_jotunns_thumb = 21
    option_old_skerry = 22
    option_hamarr_stone = 23
    option_giants_nose = 24
    option_walters_boulder = 25
    option_sundered_sons = 26
    option_old_wealds_boulder = 27
    option_leaning_spire = 28
    option_cromlech = 29
    option_walkers_pillar = 30
    option_eldenhorn = 31
    option_great_gaol = 32
    option_st_haelga = 33
    option_ymirs_shadow = 34
    option_great_bulwark = 35
    option_solemn_tempest = 36
    default = 0

    def get_location_id(self) -> int:
        return self.value + 1

    def get_peak_book_option(self) -> int:
        if self.value <= 19:
            return StartingBook.option_fundamentals
        elif self.value <= 29:
            return StartingBook.option_intermediate
        elif self.value <= 34:
            return StartingBook.option_advanced
        else:
            return StartingBook.option_expert

    # incomplete, but simple
    @classmethod
    def get_option_name(cls, value: T) -> str:
        return super().get_option_name(value).replace("s ", "'s ")

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
    option_peak = 5
    default = 0

class PeakGoal(PeakChoice):
    """
    Decides what peak triggers the win, only affects the game when goal is set to "Peak"
    """
    display_name = "Peak Goal"
    default = 36

class GameMode(Choice):
    """
    CHose what mode to play
    - **Book Unlock**: unlock entire books at once, and play the peaks in whatever order you like
    - **Peak Unlock**: unlock individual peaks instead of entire books, more restrictive, more of a challenge
    """
    display_name = "Game Mode"
    option_book_unlock = 0
    option_peak_unlock = 1
    default = 0

class DeathLinkTraps(DefaultOnToggle):
    """
    Instead of killing the player, Death Link triggers traps.
    Only affects the game when Death Link is enabled.
    """
    display_name = "Death Link Traps"

class FillerTraps(DefaultOnToggle):
    """
    Adds traps to the item pool if enabled.
    """
    display_name = "Traps in pool"

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

    def get_start_peak_id(self) -> int:
        if self.value == self.option_fundamentals:
            return PeakChoice.option_greenhorns_top
        elif self.value == self.option_intermediate:
            return PeakChoice.option_porters_boulder
        elif self.value == self.option_advanced:
            return PeakChoice.option_walkers_pillar
        else:
            return PeakChoice.option_great_bulwark


    def needs_ice_axes(self) -> bool:
        return self.value in [3] # more will be added :p

class StartingPeak(PeakChoice):
    """
    Choose what peak to start with.

    Only affects the game when **game mode** is set to **peak unlock**.

    If this peak's book is disabled, the first peak of the **starting book** option will be chosen.
    """
    display_name = "Starting Peak"

class StartWithBarometer(DefaultOnToggle):
    """Choose to start with the barometer, to locate items quicker"""
    display_name = "Start with Barometer"

class StartWithChalk(Toggle):
    """Choose to start with the Chalk Bag, also unlocking bird seeds."""
    display_name = "Start with Chalk"

class StartWithCoffee(Toggle):
    """Choose to start with the Coffee Flask"""
    display_name = "Start with Coffee"

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

class RequirementsDifficulty(Choice):
    """
    Choose how lenient the generation is with required items.

    - **Normal**: Easiest, generation will not require you to do insane things
    - **Difficult**: Generation will be slightly less strict than Normal, might require you to climb some harder peaks with less items
    - **Free Solo**: Generation will only require the bare minimum of items (eg. Just Ice axes on Tempest)

    Note: required by generation does not mean that it is enforced upon the player.
    For example: no crampons requirement on Tempest does not mean that crampons WILL be placed after tempest, just that
    they MIGHT. (You are not guaranteed to get crampons before having to do Tempest)
    """
    display_name = "Requirements Difficulty"
    option_easy = 0
    option_normal = 1
    option_difficult = 2
    option_free_solo = 3
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
        StartingPeak,
        StartWithBarometer,
        StartWithChalk,
        StartWithCoffee,
        StartWithOilLamp,
        RopeUnlockMode,
        StartingHands,
        EarlyHands,
        RequirementsDifficulty
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
    goal: Goal
    peak_goal: PeakGoal
    game_mode: GameMode
    death_link: DeathLink
    death_link_traps: DeathLinkTraps
    item_traps: FillerTraps
    starting_book: StartingBook
    starting_peak: StartingPeak
    start_with_barometer: StartWithBarometer
    start_with_chalk: StartWithChalk
    start_with_coffee: StartWithCoffee
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
    requirements_difficulty: RequirementsDifficulty
