from typing import Iterable

from .options import StardewValleyOptions


def apply_most_restrictive_options(group_option: StardewValleyOptions, world_options: Iterable[StardewValleyOptions]) -> None:
    """Merge the options of the worlds member of the group that can impact fillers generation into the option class of the group.
    """

    # If at least one world disabled ginger island, disabling it for the whole group
    group_option.exclude_ginger_island.value = max(o.exclude_ginger_island.value for o in world_options)

    # If at least one world disabled traps, disabling them for the whole group
    group_option.trap_items.value = min(o.trap_items.value for o in world_options)
