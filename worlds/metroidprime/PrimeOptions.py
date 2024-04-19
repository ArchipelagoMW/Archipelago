
from Options import DeathLink, Toggle, Range, ItemDict, StartInventoryPool, Choice, PerGameCommonOptions
from dataclasses import dataclass


class SpringBall(Toggle):
    """Adds Spring Ball to the item pool. This item will allow you to jump in Morph Ball mode,
    significantly reducing the necessity of bomb jumps. Does not change the logic at this current time."""
    display_name = "Add Spring Ball"


class RequiredArtifacts(Range):
    """Determines the amount of Artifacts needed to begin the endgame sequence."""
    display_name = "Required Artifacts"
    range_start = 1
    range_end = 12
    default = 12


class ExcludeItems(ItemDict):
    """Replaces the following items with filler. INPUT AT YOUR OWN RISK. I cannot promise that removing
    progression items will not break logic. (for now please leave the default starting items in)"""
    verify_item_name = True
    display_name = "Exclude Items"


class FinalBosses(Choice):
    """Determines the final bosses required to beat the seed. Choose from Meta Ridley, Metroid Prime,
    both, or neither."""
    display_name = "Final Boss Select"
    option_both = 0
    option_ridley = 1
    option_prime = 2
    option_none = 3
    default = 0


@dataclass
class MetroidPrimeOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    spring_ball: SpringBall
    required_artifacts: RequiredArtifacts
    exclude_items: ExcludeItems
    final_bosses: FinalBosses
    death_link: DeathLink

