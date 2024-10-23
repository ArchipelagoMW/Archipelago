import typing
import dataclasses

from Options import Range, Choice, PerGameCommonOptions, Toggle
from dataclasses import dataclass

#class DuelistRematches(Choice):
#    """
#    No matter what choice is made here, Yami Yugi will be unlocked after defeating every duelist
#    at least once.
#
#    "No Rematches" means the only checks that will appear are unlocks for specific duelists.
#    Each duelist you unlock can be beaten only once to yield a check.
#
#    "One Rematch" means that checks will appear for specific duelists and a random selection
#    of (91 - NumStartingDuelists) dice from the potential 124 in the dice pool (all unique, no duplicates).
#    Each duelist you unlock can be beaten twice to yield two different checks.
#
#    "Two Rematches" means that checks will appear for specific dueslists and a random selection
#    of 2*(91 - NumStartingDuelists) dice from the potential 124 in the dice pool (meaning there can be duplicates).
#    Each duelist you unlock can be beaten thrice to yield three different checks.
#
#    The more rematches / checks you add, the more game time you can expect to have.
#    """
#    display_name = "Duelist Rematches"
#    option_no_rematches = 0
#    option_one_rematch = 1
#    option_two_rematches = 2
#    default = 1
#
#class StartingDuelists(Range):
#    """
#    The number of Duelists to start with unlocked.
#    There are 92 duelists in total, Yami Yugi is reserved for the game's goal and there must be
#    at least as many duelists to unlock as you start with, so the max you can start with is 45.
#    """
#    display_name = "Starting Duelists"
#    range_start = 1
#    range_end = 45
#    default = 1

@dataclass
class YGODDMOptions(PerGameCommonOptions):
    #duelist_rematches: DuelistRematches
    #starting_duelists: StartingDuelists

    def serialize(self) -> typing.Dict[str, int]:
        return {field.name: getattr(self, field.name).value for field in dataclasses.fields(self)}