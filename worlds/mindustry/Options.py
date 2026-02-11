from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool, Range


class TutorialSkip(Toggle):
    """Remove the need to complete the tutorial and unlock tutorial related tech. Grant a free launch for every selected planet."""
    display_name = "Tutorial skip"

class CampaignChoice(Choice):
    """Select Serpulo, Erekir or both for the randomized campaign."""
    display_name = "Campaign choice"
    option_serpulo_only = 0
    option_erekir_only = 1
    option_all_planets = 2
    default = 0

class Goal(Choice):
    """The goal for the multiworld"""
    display_name = "Goal"
    option_resources = 0
    option_conquest = 1
    default = 0


class DisableInvasions(Toggle):
    """Disable invasions and prevent losing progress."""
    display_name = "Disable invasions"

class FasterProduction(Toggle):
    """Enable faster production and harvesting of resources."""
    display_name = "Faster production"

class FasterConveyor(Toggle):
    """Enable faster conveyor."""
    display_name = "Faster conveyor"

class DeathLink(Toggle):
    """Enable death link."""
    display_name = "Death link"

class DeathLinkMode(Choice):
    "Select the death link mode."
    display_name = "Death link mode"
    option_death_link_unit = 0
    option_death_link_core = 1
    option_death_link_core_russian_roulette = 2
    default = 0

class CoreRussianRouletteChambers(Range):
    "The number of chambers for the Core Russian roulette option. If you select X amount of chambers, you will have 1 in a X chance of having your cores destroyed"
    display_name = "Core Russian Roulette Chambers"
    range_start = 2
    range_end = 100
    default = 6

class MilitaryLevelTracking(DefaultOnToggle):
    """Ensure the player has enough military power to clear sectors. If turned off, the logic will consider that the player can clear every sector once they have the minimal requirement to land on that sector."""
    display_name = "Military level tracking"

class RandomizeCoreUnitsWeapon(Toggle):
    """Will randomize core units weapon. Erekir core unit will be made vulnerable and be given an ability instead."""
    display_name = "Randomize core units weapon"

class LogisticDistribution(Choice):
    """Change how logistics research are distributed."""
    display_name = "Logistic distribution"
    option_randomized_logistics = 0
    option_early_logistics = 1
    option_local_early_logistics = 2
    option_starter_logistics = 3
    default = 1

class ProgressiveDrills(Toggle):
    """Makes Drills progressive."""
    display_name = "Progressive Drills"

class ProgressiveGenerators(Toggle):
    """Makes Generators progressive."""
    display_name = "Progressive Generators"

class MakeEarlyRoadblocksLocal(Toggle):
    """Make items that could block the player early on local."""
    display_name = "Make early roadblocks local"

class AmountOfResourcesRequired(Range):
    """The amount of resources required to complete the 'Every resources collection' goal."""
    display_name = "Amount of resources required"
    range_start = 100
    range_end = 100000
    default = 2000

@dataclass
class MindustryOptions(PerGameCommonOptions):
    """
    Options for Mindustry randomizer.
    """
    start_inventory_from_pool: StartInventoryPool
    tutorial_skip: TutorialSkip
    campaign_choice: CampaignChoice
    goal: Goal
    disable_invasions: DisableInvasions
    faster_production: FasterProduction
    faster_conveyor: FasterConveyor
    death_link: DeathLink
    death_link_mode: DeathLinkMode
    military_level_tracking: MilitaryLevelTracking
    randomize_core_units_weapon: RandomizeCoreUnitsWeapon
    logistic_distribution: LogisticDistribution
    progressive_drills : ProgressiveDrills
    progressive_generators : ProgressiveGenerators
    make_early_roadblocks_local: MakeEarlyRoadblocksLocal
    amount_of_resources_required: AmountOfResourcesRequired
    core_russian_roulette_chambers: CoreRussianRouletteChambers
