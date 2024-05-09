from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, PerGameCommonOptions


class HiddenLocs(Toggle):
    """Places items on the secret invisible item locations."""
    display_name = "Hidden Item Checks"

class CaveLevel(Choice):
    """This will determine the color palette of the cave you venture though."""
    display_name = "Cave Palette"
    option_cave_1 = 0
    option_cave_2 = 1
    option_cave_3 = 2
    option_cave_4 = 3
    default = 0

@dataclass
class SpelunkerOptions(PerGameCommonOptions):
    hidden_items: HiddenLocs
    cave_color: CaveLevel
    death_link: DeathLink
