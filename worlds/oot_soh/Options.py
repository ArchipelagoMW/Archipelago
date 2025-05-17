from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, StartInventoryPool


class DeathLink(Toggle):
    """You die, others die. Others die, you die!"""
    display_name = "Death Link"


@dataclass
class SohOptions(PerGameCommonOptions):
    death_link: DeathLink
