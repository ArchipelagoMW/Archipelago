from dataclasses import dataclass
from Options import Toggle, PerGameCommonOptions, Choice


class FillWithDetermination(Toggle):
    """Either fills the rat with determination, or does nothing. Perhaps both."""
    display_name = "Fill With Determination"


class VictoryLocation(Choice):
    """Optionally moves the final victory location earlier to reduce the number of locations in the multiworld."""
    display_name = "Victory Location"
    option_snakes_on_a_planet = 0
    option_secret_cache = 1
    option_captured_goldfish = 2
    default = 0


@dataclass
class ArchipelagoGameOptions(PerGameCommonOptions):
    fill_with_determination: FillWithDetermination
    victory_location: VictoryLocation
