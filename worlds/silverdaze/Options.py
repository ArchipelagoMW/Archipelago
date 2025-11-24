from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

class starting_party_member(Choice):
    """
    This selects which party member you are given at the very beginning of the game.
    """
    display_name = "Starting Party Member"
    option_random = 10
    option_pinn = 0
    option_geo = 1
    option_kani = 2
    default = option_random
#
#  class IncludeShops(Toggle):
#     """
#    This toggles whether shops can have important items.
#     """
#     display_name = "Include Shops"
#     default = 1
#
# class Deathlink(Toggle):
#     """
#    This toggles deathlink.
#     """
#     display_name = "Deathlink"
#     default = 1
#


class minibosses(Toggle):
    """
    This toggles whether or not minibosses drop important items.
    NOTE: You may still need to defeat minibosses if they are blocking your path to progression
    """
    display_name = "Miniboss Drops"
    default = 1

class wardens(Toggle):
    """
    This toggles whether or not Wardens drop important items.
    NOTE: This only includes normal Wardens, Chaos Wardens are a different option
    """
    display_name = "Warden Drops"
    default = 1

#class chaos_wardens(Toggle):
#    """
#    This toggles whether or not Chaos Wardens drop important items.
#    NOTE: This only includes Chaos Wardens, normal Wardens are a different option
#    """
#    display_name = "Chaos Warden Drops"
#    default = 1

#class omni(Toggle):
#   """
#   This toggles whether or not Omni drops important items.
#   """
#    display_name = "Omni Drops"
#    default = 0

@dataclass
class SilverDazeOptions(PerGameCommonOptions):
         starting_party_member: starting_party_member