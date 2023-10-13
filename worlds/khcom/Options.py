from dataclasses import dataclass
from Options import Toggle, Range, Choice, PerGameCommonOptions

@dataclass
class khcom_options(PerGameCommonOptions):
    include_battle_cards: Toggle