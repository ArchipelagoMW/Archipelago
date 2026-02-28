from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

@dataclass
class SonicGensOptions(PerGameCommonOptions):
    pass

option_groups = []
option_presets = []