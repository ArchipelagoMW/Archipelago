"""This module contains the YAML option for Holostar Skip"""
from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class HolostarSkip(Choice):
    """
    How much of the linear sections of Holostar studios should get skipped?
    Start as Clank: Nothing is skipped, the planet behaves like normal.
    Start at Trailer: Skip the Clank section and begin as Ratchet by the trailer
    """
    display_name = RAC3OPTION.HOLOSTAR_SKIP
    option_start_as_clank = 0
    option_start_at_trailer = 1
    # Todo: add Start at Ship option, logic, and interface functionality
    # Start at Ship: Skip the section as Ratchet without Clank, use the warp pad to return to the trailer section.
    # option_start_at_ship = 2
    default = 0
