from dataclasses import dataclass

from Options import DeathLink, PerGameCommonOptions

@dataclass
class YTGVOptions(PerGameCommonOptions):
    death_link: DeathLink
    