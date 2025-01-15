import typing
from dataclasses import dataclass
from Options import DeathLink, PerGameCommonOptions


@dataclass
class ChecksFinderOptions(PerGameCommonOptions):
    death_link: DeathLink