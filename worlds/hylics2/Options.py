from dataclasses import dataclass
from Options import Choice, Removed, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions


class PartyShuffle(Toggle):
    """
    Shuffles party members into the item pool.
    
    Note that enabling this can significantly increase both the difficulty and length of a run.
    """
    display_name = "Shuffle Party Members"


class GestureShuffle(Choice):
    """
    Choose where gestures will appear in the item pool.
    """
    display_name = "Shuffle Gestures"
    option_anywhere = 0
    option_tvs_only = 1
    option_default_locations = 2
    default = 0


class MedallionShuffle(Toggle):
    """
    Shuffles red medallions into the item pool.
    """
    display_name = "Shuffle Red Medallions"


class StartLocation(Choice):
    """
    Select the starting location from 1 of 4 positions.
    """
    display_name = "Start Location"
    option_waynehouse = 0
    option_viewaxs_edifice = 1
    option_tv_island = 2
    option_shield_facility = 3
    default = 0

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == 1:
            return "Viewax's Edifice"
        if value == 2:
            return "TV Island"
        return super().get_option_name(value)


class ExtraLogic(DefaultOnToggle):
    """
    Include some extra items in logic (CHARGE UP, 1x PAPER CUP) to prevent the game from becoming too difficult.
    """
    display_name = "Extra Items in Logic"


class Hylics2DeathLink(DeathLink):
    """
    When you die, everyone dies. The reverse is also true.
    
    Note that this also includes death by using the PERISH gesture.
    
    Can be toggled via in-game console command "/deathlink".
    """


@dataclass
class Hylics2Options(PerGameCommonOptions):
    party_shuffle: PartyShuffle
    gesture_shuffle: GestureShuffle
    medallion_shuffle: MedallionShuffle
    start_location: StartLocation
    extra_items_in_logic: ExtraLogic
    death_link: Hylics2DeathLink

    # Removed options
    random_start: Removed
