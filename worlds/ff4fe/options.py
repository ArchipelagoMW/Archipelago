# options.py
from dataclasses import dataclass

from Options import Toggle, Range, Choice, PerGameCommonOptions


class DarkMatterHunt(Toggle):
    """Find the Dark Matter to win."""
    display_name = "Dark Matter Hunt"

class NoFreeCharacters(Toggle):
    display_name = "No Free Characters"

class NoEarnedCharacters(Toggle):
    display_name = "No Earned Characters"

class HeroChallenge(Choice):
    display_name = "Hero Challenge"
    option_none = 0
    option_cecil = 1
    option_kain = 2
    option_rydia = 3
    option_tellah = 4
    option_edward = 5
    option_rosa = 6
    option_yang = 7
    option_palom = 8
    option_porom = 9
    option_cid = 10
    option_edge = 11
    option_fusoya = 12
    option_random_character = 13
    default = 0

class PassEnabled(Toggle):
    display_name = "Pass Enabled"

class UsefulPercentage(Range):
    display_name = "Useful Item Percentage"
    range_start = 0
    range_end = 100
    default = 30


@dataclass
class FF4FEOptions(PerGameCommonOptions):
    DarkMatterHunt: DarkMatterHunt
    NoFreeCharacters: NoFreeCharacters
    NoEarnedCharacters: NoEarnedCharacters
    HeroChallenge: HeroChallenge
    PassEnabled: PassEnabled
    UsefulPercentage: UsefulPercentage