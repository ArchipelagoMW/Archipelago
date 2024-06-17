from dataclasses import dataclass
from typing import List

from Options import Choice, Range, Toggle, PerGameCommonOptions


class StartingLevitation(Toggle):
    """Start with Levitation Level 1"""
    display_name = "Start with Levitation"
    default = False


class StartingMentalMagnet(Toggle):
    """Start with Mental Magnet, pulling health, ammo, and arrowhead drops towards you."""
    display_name = "Start with Mental Magnet"
    default = True


class StartingCobwebDuster(Toggle):
    """Start with the Cobweb Duster."""
    display_name = "Start with Cobweb Duster"
    default = False


class RandomStartingMinds(Range):
    """Start with a random number of mind/area unlocking items."""
    display_name = "Random Starting Minds"
    range_start = 0
    range_end = 10
    default = 3


class LootboxVaults(Toggle):
    """Turns all Memory Vaults into Lootboxes! Vaults will contain 10-50 Arrowheads, with a 50% chance to recieve a rank up.
    If you get really lucky, you can even win jackpots of up to 250 Arrowheads or Five Ranks Up!
    If False, Vaults will always give One Rank Up and 15 Arrowheads."""
    display_name = "Lootbox Vaults"
    default = True


class EasyMillaRace(Toggle):
    """Make the race in Milla's Mind easier by removing Bobby from the race, and increasing player speed to 1.5x"""
    display_name = "Easy Milla Race"
    default = False


class EasyFlightMode(Toggle):
    """Replicate the Levitation Flight Glitch by simply holding down float in the air. No more button mashing.
    WARNING: Makes getting locations out of logic VERY easy."""
    display_name = "Easy Flight Mode"
    default = False


class EnemyDamageMultiplier(Range):
    """Adjust how much damage Raz takes from enemies for an additional challenge.
    If set to 0, Raz will take no damage from enemies, but will still flinch."""
    display_name = "Enemy Damage Multiplier"
    range_start = 0
    range_end = 5
    default = 1


class InstantDeathMode(Toggle):
    """Take any amount of damage, die instantly. Has priority over Enemy Damage Multiplier."""
    display_name = "Instant Death Mode"
    default = False


class Goal(Choice):
    """Win Condition
    Asylum Brain Tank: Climb the Asylum and defeat the Coach Oleander Brain Tank.

    Brain Hunt: Find the required amount of Camper Brains and re-brain them in Ford's Sanctuary.

    Asylum Brain Tank and Brain Hunt: Find the required amount of Camper Brains, AND defeat the Coach Oleander Brain Tank."""
    display_name = "Goal"
    option_braintank = 0
    option_brainhunt = 1
    option_braintank_and_brainhunt = 2
    default = 0


class BrainsRequired(Range):
    """Number of Brains required to collect to Win, or open final door to Meat Circus Final Bosses.

    If Goal is not Brain Hunt, or Asylum Brain Tank and Brain Hunt, this does nothing."""
    display_name = "Brains Required"
    range_start = 1
    range_end = 19
    default = 10


class RequireMeatCircus(Toggle):
    """Require finishing Meat Circus Final Bosses in addition to your goal."""
    display_name = "Require Meat Circus"
    default = True


class DeepArrowheadShuffle(Toggle):
    """Add Deep Arrowhead checks and shuffle the Dowsing Rod and extra Arrowhead Bundles into the item pool.

    Deep Arrowhead locations must be dug up from the ground using the Dowsing Rod and will set a shorter 10-minute
    (unpaused in-game time) respawn time after being dug up for the first time. Digging up a Deep Arrowhead again, after
    waiting for it to respawn, will award arrowheads like normal and set the normal 30-minute respawn time.

    The Deep Arrowheads found under the Lake are not affected by this option."""
    display_name = "Deep Arrowhead Shuffle"
    default = False


class MentalCobwebShuffle(Toggle):
    """Add Mental Cobweb checks and shuffle an extra PSI Card into the item pool for each Mental Cobweb.

    Mental Cobweb locations must be collected using the Cobweb Duster. Collecting a Mental Cobweb will not add it to
    Raz's inventory, so the loom in Ford's Sanctuary will have no use."""
    display_name = "Mental Cobweb Shuffle"
    default = False


@dataclass
class PsychonautsOptions(PerGameCommonOptions):
    StartingLevitation: StartingLevitation
    StartingMentalMagnet: StartingMentalMagnet
    StartingCobwebDuster: StartingCobwebDuster
    RandomStartingMinds: RandomStartingMinds
    LootboxVaults: LootboxVaults
    EasyMillaRace: EasyMillaRace
    EasyFlightMode: EasyFlightMode
    EnemyDamageMultiplier: EnemyDamageMultiplier
    InstantDeathMode: InstantDeathMode
    Goal: Goal
    BrainsRequired: BrainsRequired
    RequireMeatCircus: RequireMeatCircus
    DeepArrowheadShuffle: DeepArrowheadShuffle
    MentalCobwebShuffle: MentalCobwebShuffle


SLOT_DATA_OPTIONS: List[str] = [
    "StartingLevitation",
    "StartingMentalMagnet",
    "LootboxVaults",
    "EasyMillaRace",
    "EasyFlightMode",
    "EnemyDamageMultiplier",
    "InstantDeathMode",
    "Goal",
    "BrainsRequired",
    "RequireMeatCircus",
    "DeepArrowheadShuffle",
    "MentalCobwebShuffle",
]
