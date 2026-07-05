from dataclasses import dataclass
from Options import Toggle, Choice, PerGameCommonOptions

class UselessToggle(Toggle):
    """
    This toggle literally does nothing, but it serves as an excellent structural 
    example for future options.
    """
    display_name = "Useless Toggle"

@dataclass
class TemplateGameOptions(PerGameCommonOptions):
    useless_toggle: UselessToggle