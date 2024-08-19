from dataclasses import dataclass
from Options import Range, Toggle, DefaultOnToggle, Choice, DeathLink, PerGameCommonOptions

class MinimumResourcePackAmount(Range):
    """The minimum amount of resources available in a resource pack"""
    display_name = "Minimum resource pack amount"
    range_start = 1
    range_end = 15
    default = 1

class MaximumResourcePackAmount(Range):
    """The maximum amount of resources available in a resource pack"""
    display_name = "Maximum resource pack amount"
    range_start = 1
    range_end = 15
    default = 5

class DuplicateItems(Choice):
    """Adds duplicates of items to the item pool (if configured in Filler items). These will be selected alongside
    Resource Packs (if configured). Note that there are not many progression items, and selecting Progression may
    produce many of the same duplicate item."""
    display_name = "Duplicate items"
    option_progression = 0
    option_non_progression = 1
    option_any = 2
    default = 2

class FillerItemTypes(Choice):
    """Determines whether to use Resource Packs, Duplicate Items (as configured), or both."""
    display_name = "Filler items"
    option_resource_packs = 0
    option_duplicates = 1
    option_both = 2

class IslandFrequencyLocations(Choice):
    """Sets where frequencies for story islands are located.
    Vanilla will keep frequencies in their vanilla, non-randomized locations.
    Random On Island will randomize each frequency within its vanilla island, but will preserve island order.
    Random Island Order will change the order you visit islands, but will preserve the vanilla location of each frequency unlock.
    Random On Island Random Order will randomize the location containing the frequency on each island and randomize the order.
    Progressive will randomize the frequencies to anywhere, but will always unlock the frequencies in vanilla order as the frequency items are received.
    Anywhere will randomize the frequencies to anywhere, and frequencies will be received in any order."""
    display_name = "Frequency locations"
    option_vanilla = 0
    option_random_on_island = 1
    option_random_island_order = 2
    option_random_on_island_random_order = 3
    option_progressive = 4
    option_anywhere = 5
    default = 2
    def is_filling_frequencies_in_world(self):
        return self.value <= self.option_random_on_island_random_order

class IslandGenerationDistance(Choice):
    """Sets how far away islands spawn from you when you input their coordinates into the Receiver."""
    display_name = "Island distance"
    option_quarter = 2
    option_half = 4
    option_vanilla = 8
    option_double = 16
    option_quadrouple = 32
    default = 8

class ExpensiveResearch(Toggle):
    """If No is selected, researching items and unlocking items in the Crafting Table works the same as vanilla Raft.
    If Yes is selected, each unlock in the Crafting Table will require its own set of researched items in order to unlock it."""
    display_name = "Expensive research"

class ProgressiveItems(DefaultOnToggle):
    """Makes some items, like the Bow and Arrow, progressive rather than raw unlocks."""
    display_name = "Progressive items"

class BigIslandEarlyCrafting(Toggle):
    """Allows recipes that require items from big islands (eg leather) to lock earlygame items like the Receiver, Bolt,
    or Smelter. Big islands are available from the start of the game, however it can take a long time to find them."""
    display_name = "Early recipes behind big islands"

class PaddleboardMode(Toggle):
    """Sets later story islands to be in logic without an Engine or Steering Wheel. May require lots of paddling."""
    display_name = "Paddleboard Mode"

@dataclass
class RaftOptions(PerGameCommonOptions):
    minimum_resource_pack_amount: MinimumResourcePackAmount
    maximum_resource_pack_amount: MaximumResourcePackAmount
    duplicate_items: DuplicateItems
    filler_item_types: FillerItemTypes
    island_frequency_locations: IslandFrequencyLocations
    island_generation_distance: IslandGenerationDistance
    expensive_research: ExpensiveResearch
    progressive_items: ProgressiveItems
    big_island_early_crafting: BigIslandEarlyCrafting
    paddleboard_mode: PaddleboardMode
    death_link: DeathLink
