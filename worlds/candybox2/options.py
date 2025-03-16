from dataclasses import dataclass

from Options import PerGameCommonOptions


@dataclass
class CandyBox2Options(PerGameCommonOptions):
    progression_balancing = True