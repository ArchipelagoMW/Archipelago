from dataclasses import dataclass
from typing import List

from Options import Choice, Range, Toggle, DefaultOnToggle, PerGameCommonOptions, StartInventoryPool, OptionGroup

class StartingLevitation(Toggle):
    """Start with Progressive Levitation level 1."""
    display_name = "Start with Levitation"


class StartingCobwebDuster(Toggle):
    """Start with the Cobweb Duster."""
    display_name = "Start with Cobweb Duster"


class StartingMentalMagnet(DefaultOnToggle):
    """Start with Mental Magnet, pulling health, ammo, and arrowhead drops towards you."""
    display_name = "Start with Mental Magnet"


class StartingColorizer(DefaultOnToggle):
    """Start with the Colorizer, allowing you to change the color of your Psiball using the Bacon."""
    display_name = "Start with Colorizer"


class RandomStartingMinds(Range):
    """Start with a random number of mind/area unlocking items."""
    display_name = "Random Starting Minds"
    range_start = 0
    range_end = 10
    default = 3


class VaultHints(DefaultOnToggle):
    """When receiving a Memory Vault, hint a random location in your AP world that hasn't been collected yet."""
    display_name = "Vault Hints"


class VaultCount(Range):
    """How many Memory Vaults are added to the item pool."""
    display_name = "Vaults in Item Pool"
    range_start = 0
    range_end = 101
    default = 19


class EasyMillaRace(Toggle):
    """Makes collecting figments and winning the race in Milla's Mind easier by removing everyone else from the race."""
    display_name = "Easy Milla Race"


class EasyFlightMode(Toggle):
    """Replicate the Levitation Flight Glitch by simply holding down float in the air. No more button mashing.
    WARNING: Makes getting locations out of logic VERY easy."""
    display_name = "Easy Flight Mode" 


class BetterDowsingRod(Toggle): 
    """Makes the Dowsing Rod gauge fill faster to collect Deep Arrowheads easier."""
    display_name = "Better Dowsing Rod"


class OtherItemsModel(Choice): 
    """Choose what your Archipelago items for other games look like inside Psychonauts
    Archipelago: The standard Archipelago symbol.

    Bunny: The original PsychoRando model for Archipelago items, Bunnies!
    
    Present: Open some holiday gift boxes!"""
    display_name = "Archipelago Item Model"
    option_archipelago = 0
    option_bunny = 1
    option_present = 2
    default = 0


class PsiBallColor(Choice):
    """Choose the starting color of your PsiBall."""
    display_name = "PsiBall Color"
    option_red = 0
    option_white = 1
    option_pink = 2
    option_yellow = 3
    option_purple = 4
    option_blue = 5
    option_lightpurple = 6
    option_cyan = 7
    option_green = 8
    option_orange = 9
    option_lightgreen = 10
    option_lightpeach = 11
    option_lightpink = 12
    option_lighterpink = 13
    default = 0


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


class Goal(Choice):
    """Win Condition
    Asylum Brain Tank: Climb the Asylum and defeat the Coach Oleander Brain Tank.

    Brain Hunt: Find the required amount of Camper Brains and re-brain them in Ford's Sanctuary.

    Asylum Brain Tank and Brain Hunt: Find the required amount of Camper Brains, AND defeat the Coach Oleander Brain Tank."""
    display_name = "Goal"
    option_asylum_brain_tank = 0
    option_brain_hunt = 1
    option_asylum_brain_tank_and_brain_hunt = 2
    default = 0


class BrainsRequired(Range):
    """Number of Brains required to collect to Win, or open final door to Meat Circus Final Bosses.

    If Goal is not Brain Hunt, or Asylum Brain Tank and Brain Hunt, this does nothing."""
    display_name = "Brains Required"
    range_start = 1
    range_end = 19
    default = 10


class RequireMeatCircus(DefaultOnToggle):
    """Require finishing Meat Circus Final Bosses in addition to your goal."""
    display_name = "Require Meat Circus"


class RankSanity(Toggle):
    """Add Rank Rewards to EVERY Rank Up, instead of the traditional Five Ranks Up."""
    display_name = "Rank Sanity"


class FigmentPercentageChecks(Choice):
    """Controls the maximum percentage of figments needed from each mind that will send checks.

    One check is sent for every 20 percent of figments found in each mind, up to the maximum set here.

    If set to 0, no figment collecting is required."""
    display_name = "Figment Percentage Maximum"
    option_0_percent = 0
    option_20_percent = 1
    option_40_percent = 2
    option_60_percent = 3
    option_80_percent = 4
    option_100_percent = 5
    default = 0


class DeepArrowheadShuffle(Toggle):
    """Add Deep Arrowhead checks and shuffle the Dowsing Rod and extra Arrowhead Bundles into the item pool.

    Deep Arrowhead locations must be dug up from the ground using the Dowsing Rod and will set a shorter 10-minute
    (unpaused in-game time) respawn time after being dug up for the first time. Digging up a Deep Arrowhead again, after
    waiting for it to respawn, will award arrowheads like normal and set the normal 30-minute respawn time.

    The Deep Arrowheads found under the Lake are not affected by this option."""
    display_name = "Deep Arrowhead Shuffle"


class MentalCobwebShuffle(Toggle):
    """Add Mental Cobweb checks and shuffle an extra PSI Card into the item pool for each Mental Cobweb.

    Mental Cobweb locations must be collected using the Cobweb Duster. Collecting a Mental Cobweb will not add it to
    Raz's inventory, so the loom in Ford's Sanctuary will have no use."""
    display_name = "Mental Cobweb Shuffle"


class HintUnclaimedBaggage(DefaultOnToggle):
    """When interacting with Baggage that you don't have a matching tag for yet, automatically creates a hint for 
    the location in the client."""
    display_name = "Hint Unclaimed Baggage"


class ProgressiveBaggage(Toggle):
    """Turns Emotional Baggage into Progressive Locations
    
    Each time you redeem a Baggage Tag with it's matching Baggage, you'll earn the next check for that type."""
    display_name = "Progressive Baggage"


class MaximumProgressiveBaggage(Range):
    """Maximum amount of each type of Baggage that will give checks.
    
    Only works if Progressive Baggage is Enabled and value is greater than 0."""
    display_name = "Maximum Progressive Baggage"
    range_start = 0
    range_end = 10
    default = 5


@dataclass
class PsychonautsOptions(PerGameCommonOptions):
    StartingLevitation: StartingLevitation
    StartingCobwebDuster: StartingCobwebDuster
    StartingMentalMagnet: StartingMentalMagnet
    StartingColorizer: StartingColorizer
    PsiBallColor: PsiBallColor
    RandomStartingMinds: RandomStartingMinds
    VaultHints: VaultHints
    VaultCount: VaultCount
    EasyMillaRace: EasyMillaRace
    EasyFlightMode: EasyFlightMode
    BetterDowsingRod: BetterDowsingRod
    OtherItemsModel: OtherItemsModel
    EnemyDamageMultiplier: EnemyDamageMultiplier
    InstantDeathMode: InstantDeathMode
    Goal: Goal
    BrainsRequired: BrainsRequired
    RequireMeatCircus: RequireMeatCircus
    RankSanity: RankSanity
    FigmentPercentageChecks: FigmentPercentageChecks
    DeepArrowheadShuffle: DeepArrowheadShuffle
    MentalCobwebShuffle: MentalCobwebShuffle
    HintUnclaimedBaggage: HintUnclaimedBaggage
    ProgressiveBaggage: ProgressiveBaggage
    MaximumProgressiveBaggage: MaximumProgressiveBaggage
    start_inventory: StartInventoryPool


SLOT_DATA_OPTIONS: List[str] = [
    "StartingLevitation",
    "StartingCobwebDuster",
    "StartingMentalMagnet",
    "StartingColorizer",
    "PsiBallColor",
    "RandomStartingMinds",
    "VaultHints",
    "VaultCount",
    "EasyMillaRace",
    "EasyFlightMode",
    "BetterDowsingRod",
    "OtherItemsModel",
    "EnemyDamageMultiplier",
    "InstantDeathMode",
    "Goal",
    "BrainsRequired",
    "RequireMeatCircus",
    "RankSanity",
    "FigmentPercentageChecks",
    "DeepArrowheadShuffle",
    "MentalCobwebShuffle",
    "HintUnclaimedBaggage",
    "ProgressiveBaggage",
    "MaximumProgressiveBaggage",
]


OPTION_GROUPS: list [OptionGroup] = [
    OptionGroup("Starting Options", [
        StartingLevitation,
        StartingCobwebDuster,
        StartingMentalMagnet,
        RandomStartingMinds,
    ]),
    OptionGroup("Cosmetic Options", [
        OtherItemsModel,
        PsiBallColor,
        StartingColorizer,
    ]),
    OptionGroup("Goal Options", [
        Goal,
        BrainsRequired,
        RequireMeatCircus,
    ]),
    OptionGroup("Extra Location Options", [
        RankSanity,
        FigmentPercentageChecks,
        DeepArrowheadShuffle,
        MentalCobwebShuffle,       
    ]),
    OptionGroup("Baggage Options", [
        HintUnclaimedBaggage,
        ProgressiveBaggage,
        MaximumProgressiveBaggage, 
    ]),
    OptionGroup("Vault Options", [
        VaultHints,
        VaultCount,
    ]),
    OptionGroup("Difficulty Options", [
        EasyFlightMode,
        EasyMillaRace,
        BetterDowsingRod,
        EnemyDamageMultiplier,
        InstantDeathMode,        
    ]),
]
