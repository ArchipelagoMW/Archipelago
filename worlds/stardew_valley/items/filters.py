from collections.abc import Iterable

from .item_data import ItemData, Group
from ..options import StardewValleyOptions, ExcludeGingerIsland


def filter_excluded(items: Iterable[ItemData], options: StardewValleyOptions) -> list[ItemData]:
    return [
        item
        for item in items
        if Group.DEPRECATED not in item.groups
           and (options.exclude_ginger_island == ExcludeGingerIsland.option_false or Group.GINGER_ISLAND not in item.groups)
           and (item.mod_name is None or item.mod_name in options.mods.value)
    ]


def filter_limited_amount_resource_packs(packs: Iterable[ItemData]) -> list[ItemData]:
    return [
        resource_pack
        for resource_pack in packs
        if not resource_pack.has_limited_amount()
    ]


def filter_already_included_maximum_one(items: Iterable[ItemData], already_added_items: set[str]) -> list[ItemData]:
    return [
        item
        for item in items
        if item.name not in already_added_items or Group.MAXIMUM_ONE not in item.groups
    ]
