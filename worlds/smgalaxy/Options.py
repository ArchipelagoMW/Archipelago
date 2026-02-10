from dataclasses import dataclass

from Options import Choice, Range, PerGameCommonOptions, OptionSet, Toggle, OptionCounter


class GalaxyShuffle(OptionSet):
    """
    Determine what kinds of galaxies should be shuffled between each other

    Full: Any galaxy in any galaxy position
    Dome Majors: Add Major galaxies to shuffle pool
    Dome Minors: Add Minor galaxies to shuffle pool
    Observatory Specials: Add Direct from Observatory galaxies to shuffle pool, such as Trials or Hungry Luma galaxies
    Bosses: Add Boss galaxies to shuffle pool
    """
    display_name = "Galaxy Shuffle"
    internal_name = "galaxy_shuffle"
    valid_keys = {"Full", "Dome Majors", "Dome Minors", "Observatory Specials", "Bosses"}

class ShuffleDomes(Toggle):
    """
    Shuffle Dome entrances
    """
    display_name = "Dome Shuffle"
    internal_name = "dome_shuffle"

# this defines the enable_purple_coin_stars setting 
class EnablePurpleCoinStars(Choice):
    """
    Add Purple Coin star location. Only one of these is normally available outside of post game
    """
    display_name = "Enable Purple Coin Stars"
    internal_name = "enable_purple_coin_stars"
    option_main_game_only = 0
    option_all = 1
    option_none = 2

# this allows players to pick their own star count to finish the game. 
class StarstoFinish(Range):
    """This will set the number of stars required to reach the center of the universe."""
    display_name = "Stars to finish"
    internal_name = "stars_to_finish"
    range_start = 25
    range_end = 95
    default = 60

class Dome1Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 1, which is the Terrace in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 10

    These are based on each orbit in the dome, in case levels are shuffled. Inner Orbit is excluded, to ensure you have
    at least one world to start.
    """
    display_name = "Dome 1 Access"
    internal_name = "dome_one_counts"
    min = 0
    max = 10
    valid_keys = ["Second Orbit", "Third Orbit", "Fourth Orbit", "Outer Orbit"]
    default = {
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Final Orbit": 0
    }


class Dome2Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 2, which is the Fountain in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 20

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 2 Access"
    internal_name = "dome_two_counts"
    min = 0
    max = 20
    valid_keys = ["Inner Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Outer Orbit"]
    default = {
        "Inner Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Final Orbit": 0
    }

class Dome3Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 3, which is the Kitchen in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 20

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 3 Access"
    internal_name = "dome_three_counts"
    min = 0
    max = 20
    valid_keys = ["Inner Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Outer Orbit"]
    default = {
        "Inner Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Final Orbit": 0
    }

class Dome4Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 4, which is the Bedroom in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 20

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 4 Access"
    internal_name = "dome_four_counts"
    min = 0
    max = 20
    valid_keys = ["Inner Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Outer Orbit"]
    default = {
        "Inner Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Final Orbit": 0
    }

class Dome5Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 5, which is the Engine Room in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 20

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 5 Access"
    internal_name = "dome_five_counts"
    min = 0
    max = 20
    valid_keys = ["Inner Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Outer Orbit"]
    default = {
        "Inner Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Final Orbit": 0
    }

class Dome6Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 6, which is the Garden in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 20

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 6 Access"
    internal_name = "dome_six_counts"
    min = 0
    max = 20
    valid_keys = ["Inner Orbit", "Second Orbit", "Third Orbit", "Outer Orbit"]
    default = {
        "Inner Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Final Orbit": 0
    }

# this defines all the options.
@dataclass
class SMGOptions(PerGameCommonOptions):
    enable_purple_coin_stars: EnablePurpleCoinStars
    stars_to_finish: StarstoFinish
    # dome_one_counts: Dome1Offsets
    # dome_two_counts: Dome2Offsets
    # dome_three_counts: Dome3Offsets
    # dome_four_counts: Dome4Offsets
    # dome_five_counts: Dome5Offsets
    # dome_six_counts: Dome6Offsets
    #dome_shuffle: ShuffleDomes Enable when Ready
    #galaxy_shuffle: GalaxyShuffle Enable when Ready


