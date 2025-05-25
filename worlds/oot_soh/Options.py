from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, StartInventoryPool


class DeathLink(Toggle):
    """You die, others die. Others die, you die!"""
    display_name = "Death Link"

class ShuffleCows(Toggle):
    """Shuffle cows"""
    display_name = "Shuffle Cows"

@dataclass
class SohOptions(PerGameCommonOptions):
    death_link: DeathLink
    shuffle_cows: ShuffleCows
