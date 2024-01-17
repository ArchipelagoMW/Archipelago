import typing
from Options import Option, Toggle, Range, ItemDict, StartInventoryPool


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
    progression items will not break logic."""
    verify_item_name = True
    display_name = "Exclude Items"


metroidprime_options: typing.Dict[str, type(Option)] = {
    "start_inventory_from_pool": StartInventoryPool,
    "spring_ball": SpringBall,
    "required_artifacts": RequiredArtifacts,
    "exclude_items": ExcludeItems
}
