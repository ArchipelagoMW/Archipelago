from __future__ import annotations
from math import floor, ceil
from BaseClasses import Item, ItemClassification
from .common import *
import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import BKSimWorld


class BKSim_Item(Item):
    game = game_name


class ItemInfo(typing.NamedTuple):
    name: str
    flag: ItemClassification


item_table = [
    ItemInfo(ITEM.SHOES, ItemClassification.progression),
    ItemInfo(ITEM.BOOTS, ItemClassification.progression),
    ItemInfo(ITEM.NEWLOC, ItemClassification.progression),
    ItemInfo(ITEM.TOY, ItemClassification.filler),
]
item_name_to_id = {str(name): num for num, (name, _) in enumerate(item_table, 1)}


def get_item_counts(world: BKSimWorld) -> list[int]:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    newloc_count: int = 0
    shoe_count: int = 0
    boot_count: int = 0

    for item in multiworld.precollected_items[player]:
        if item.name == ITEM.NEWLOC:
            newloc_count += 1
        elif item.name == ITEM.SHOES:
            shoe_count += 1
        elif item.name == ITEM.BOOTS:
            boot_count += 1

    extra_filler_rate: float = max(0, min(100, options.extra_filler_rate.value)) / 100.0
    per_weather_locs: int = int(options.locs_per_weather.value)
    total_locs: int = per_weather_locs * 3
    newloc_items: int = max(0, min(2, per_weather_locs) - newloc_count)
    snow_items: int = per_weather_locs
    shoe_items: int = per_weather_locs
    toy_items: int = per_weather_locs - newloc_items
    if extra_filler_rate > 0.0:  # replace shoes/boots with filler at the specified rate, but don't break logic
        shoe_items = max(0, (int(floor(per_weather_locs - 1) / 2)) + 1 - shoe_count,
                         ceil(shoe_items * (1.0 - extra_filler_rate)))
        snow_items = max(0, (int(floor(per_weather_locs - 1) / 2)) + 1 - boot_count,
                         ceil(snow_items * (1.0 - extra_filler_rate)))
        toy_items += (per_weather_locs - shoe_items) + (per_weather_locs - snow_items)

    # ensure proper item count
    toy_items += total_locs - (newloc_items + snow_items + shoe_items + toy_items)

    return [shoe_items, snow_items, newloc_items, toy_items]


def create_items(world: BKSimWorld) -> None:
    multiworld = world.multiworld
    player = world.player

    counts: list[int] = get_item_counts(world)
    itempool = []
    for q in range(len(item_table)):
        data: ItemInfo = item_table[q]
        count: int = counts[q]
        itempool += [BKSim_Item(data.name, data.flag, q + 1, player) for _ in range(count)]
    multiworld.itempool += itempool


def create_item(name: str, player: int) -> BKSim_Item:
    itemid = item_name_to_id[name]
    _, flag = item_table[itemid - 1]
    return BKSim_Item(name, flag, itemid, player)


def create_event_item(event: str, player: int) -> BKSim_Item:
    return BKSim_Item(event, ItemClassification.progression, None, player)
