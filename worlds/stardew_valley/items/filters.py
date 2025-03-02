from typing import Iterable

from .item_data import ItemData, Group
from ..content import StardewContent


def remove_excluded(items: Iterable[ItemData], content: StardewContent) -> list[ItemData]:
    return [
        item
        for item in items
        if Group.DEPRECATED not in item.groups
           and content.are_all_enabled(item.content_packs)
    ]


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
        if item.name not in already_added_items
           or (item.has_any_group(Group.RESOURCE_PACK, Group.TRAP) and Group.MAXIMUM_ONE not in item.groups)
    ]
