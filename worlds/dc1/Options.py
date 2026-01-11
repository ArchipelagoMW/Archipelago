from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, Range, Visibility


class Goal(Range):
    """Select Dungeon from 2-6 to be the goal."""
    display_name = "Boss Goal"
    default = 6
    range_start = 2
    range_end = 6

class AllBosses(Toggle):
    """Requires defeating every boss up to the goal boss in order to finish the game."""
    display_name = "All Bosses"
    default = 0

class OpenDungeon(Choice):
    """Open all dungeon floors as they become logically available."""
    display_name = "Open Dungeon"
    default = 1
    option_closed = 0
    option_open = 1

class BetterStartingWeapons(Toggle):
    """Give each character a Tier 1 weapon in addition to their unbreakable starter."""
    display_name = "Better Starting Weapons"
    default = 1

class MiracleSanity(Toggle):
    """Currently doesn't do anything but change item classification for certain items. Only added for now to begin logic coding for MCs.
    Don't use if you find this!!"""
    display_name = "Miracle Sanity"
    default = 0
    # TODO make visible with MC shuffle update
    visibility = Visibility.none

class AbsMultiplier(Choice):
    """Adjust the ABS gained from enemies."""
    display_name = "ABS Multiplier"
    option_half = 0
    option_normal = 1
    option_one_and_half = 2
    option_double = 3
    option_double_and_half = 4
    option_triple = 5
    default = 3

class AutoBuild(Choice):
    """Automatically places building pieces as received.
    Hundo places buildings for 100% town completion.
    Any percent places only buildings with chests clustered similar to how speed runs place them.
    Muska only auto builds only Muska Lacka for 100%, robot only the sun giant and muska/robot builds both."""
    display_name = "Auto Build Buildings"
    option_off = 0
    option_any_percent = 1
    option_hundo = 2
    option_muska_only = 3
    option_robot_only = 4
    option_muska_robot_only = 5
    default = 2

# TODO death link.
# class DeathLink(DeathLink):

@dataclass
class DarkCloudOptions(PerGameCommonOptions):
    boss_goal: Goal
    all_bosses: AllBosses
    open_dungeon: OpenDungeon
    starter_weapons: BetterStartingWeapons
    miracle_sanity: MiracleSanity
    abs_multiplier: AbsMultiplier
    auto_build: AutoBuild
