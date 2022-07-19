from Options import Range, Toggle, DefaultOnToggle, Choice

class UseResourcePacks(DefaultOnToggle):
    """Uses Resource Packs to fill out the item pool from Raft. Resource Packs have basic earlygame items such as planks, plastic, or food."""
    display_name = "Use resource packs"

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
    """Adds duplicates of items to the item pool. These will be selected alongside
    Resource Packs (if configured). Note that there are not many progression items,
    and selecting Progression may produce many of the same duplicate item."""
    display_name = "Duplicate items"
    option_disabled = 0
    option_progression = 1
    option_non_progression = 2
    option_any = 3

class IslandFrequencyLocations(Choice):
    """Sets where frequencies for story islands are located."""
    display_name = "Frequency locations"
    option_vanilla = 0
    option_random_on_island = 1
    option_progressive = 2
    option_anywhere = 3
    default = 1

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
    """Makes unlocking items in the Crafting Table consume the researched items."""
    display_name = "Expensive research"

class ProgressiveItems(DefaultOnToggle):
    """Makes some items, like the Bow and Arrow, progressive rather than raw unlocks."""
    display_name = "Progressive items"

class BigIslandEarlyCrafting(Toggle):
    """Allows recipes that require items from big islands (eg leather) to lock earlygame items like the Receiver, Bolt, or Smelter."""
    display_name = "Early recipes behind big islands"

class PaddleboardMode(Toggle):
    """Sets later story islands to in logic without an Engine or Steering Wheel. May require lots of paddling. Not recommended."""
    display_name = "Paddleboard Mode"

raft_options = {
    "use_resource_packs": UseResourcePacks,
    "minimum_resource_pack_amount": MinimumResourcePackAmount,
    "maximum_resource_pack_amount": MaximumResourcePackAmount,
    "duplicate_items": DuplicateItems,
    "island_frequency_locations": IslandFrequencyLocations,
    "island_generation_distance": IslandGenerationDistance,
    "expensive_research": ExpensiveResearch,
    "progressive_items": ProgressiveItems,
    "big_island_early_crafting": BigIslandEarlyCrafting,
    "paddleboard_mode": PaddleboardMode
}
