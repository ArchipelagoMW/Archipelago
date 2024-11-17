from dataclasses import dataclass
from Options import Toggle, PerGameCommonOptions


class FillWithDetermination(Toggle):
    """Either fills the rat with determination, or does nothing. Perhaps both."""
    display_name = "Fill With Determination"


# Per feedback: having SOME options (even if they do nothing) helps to generate a template.
@dataclass
class ArchipelagoGameOptions(PerGameCommonOptions):
    fill_with_determination: FillWithDetermination
