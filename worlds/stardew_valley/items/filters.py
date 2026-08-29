from typing import Iterable

from .item_data import ItemData, Group, FILLER_GROUPS
from ..content import StardewContent
from ..options import StardewValleyOptions, Hatsanity


def remove_excluded(items: Iterable[ItemData], content: StardewContent, options: StardewValleyOptions) -> list[ItemData]:
    filtered_items = [
        item for item in items
        if Group.DEPRECATED not in item.groups and content.are_all_enabled(item.content_packs)
    ]
    if options.hatsanity == Hatsanity.preset_none:
        return filtered_items
    return [item for item in filtered_items if Group.FILLER_HAT not in item.groups]


def remove_limited_amount_resource_packs(packs: Iterable[ItemData]) -> list[ItemData]:
    return [
        resource_pack
        for resource_pack in packs
        if not resource_pack.has_limited_amount()
    ]


def remove_already_included(items: Iterable[ItemData], already_added_items: set[str]) -> list[ItemData]:
    return [
        item
        for item in items
        if item.name not in already_added_items or (item.has_any_group(*FILLER_GROUPS, Group.TRAP) and Group.MAXIMUM_ONE not in item.groups)
    ]
