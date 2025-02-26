from dataclasses import dataclass

from Options import Toggle, PerGameCommonOptions


class DisableBlockEvents(Toggle):
    """Disable Blocking Events. Making Game more open."""
    display_name = "Disable Blocking Events"

@dataclass
class PokeparkOptions(PerGameCommonOptions):
    disable_block_events: DisableBlockEvents