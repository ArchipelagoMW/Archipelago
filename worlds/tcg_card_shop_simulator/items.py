from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from BaseClasses import Item, CollectionRule, Location, ItemClassification
from Options import OptionError
from rule_builder.rules import Rule, True_

from .data.regions.regions import get_level_region
from .data.items.events import Events
from .constants import ITEMS_WORKER_OFFSET, ITEMS_GHOST_OFFSET
from .data import ItemTypeEnum, ItemData
from .data.items import Blockers, DIYItems, Expansions, event_items, get_shop_items, \
    all_diy_items, all_expansion_items, minimal_diy_items, minimal_expansion_items, diy_items, \
    expansion_items, all_worker_items
from .data.items.ghost import GHOST_ITEM_BY_ID
from .data.items.workers import WORKERS_ITEM_BY_ID

if TYPE_CHECKING:
    from . import TCGSimulatorWorld
    from .world_base import TCGSimulatorBase


def create_item(world: "TCGSimulatorWorld", item: ItemData):
    for i in range(item.amount):
        world.itempool.append(world.create_item(item.type.value))


def create_single_item(world: "TCGSimulatorWorld", item_type: ItemTypeEnum):
    world.itempool.append(world.create_item(item_type.value))

def create_filler_item(world: "TCGSimulatorWorld", item_value: str):
    world.filler_items.append(
        world.create_item(item_value)
    )


def generate_ghost_card_items(world: "TCGSimulatorWorld", locs_available):
    if locs_available * 5 < world.options.ghost_goal_amount.value:
        raise OptionError("Not enough locations for ghost goal")

    result = []
    remaining = world.options.ghost_goal_amount.value
    remaining_slots = locs_available

    while remaining > 0 and remaining_slots > 0:
        max_size = min(5 if remaining_slots < 50 else 2, remaining)
        min_size = max(1, remaining - (remaining_slots - 1) * 5)
        size = world.random.randint(min_size, max_size)

        result.append(size)
        remaining -= size
        remaining_slots -= 1

    for size in result:
        create_single_item(world, GHOST_ITEM_BY_ID[ITEMS_GHOST_OFFSET + size])

    return dict(Counter(
        GHOST_ITEM_BY_ID[ITEMS_GHOST_OFFSET + size].value
        for size in result
    ))


def create_items(world: TCGSimulatorWorld):
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))

    starting_items: list[Item] = []
    ghost_card_amounts = []

    for item_type in world.starting_license_items:
        starting_items.append(world.create_item(item_type.value))

    starting_items.append(world.create_item(Events.STANDARD.value))

    if world.options.start_with_worker.value != 0:
        starting_items.append(world.create_item(WORKERS_ITEM_BY_ID[ITEMS_WORKER_OFFSET + world.options.start_with_worker.value].value))

    for item_data in get_shop_items(world.license_items):
        create_item(world, item_data)

    for item_type in Blockers:
        create_single_item(world, item_type)

    if not world.options.no_formats.value:
        for item_type in event_items:
            create_item(world, item_type)

    _remaining = total_location_count - len(world.itempool)
    _filler_space = 15

    if world.options.goal.value == world.options.goal.option_grade_ghost_cards:
        ghost_card_amounts = generate_ghost_card_items(world, _remaining)

    minimum_ghost_slots = (
        (world.options.ghost_goal_amount.value + 4) // 5
        if world.options.goal.value == world.options.goal.option_grade_ghost_cards
        else 0
    )

    if _remaining-(minimum_ghost_slots+15) < 100:
        for item_data in minimal_diy_items:
            create_item(world, item_data)

        for item_data in minimal_expansion_items:
            create_item(world, item_data)

        _remaining = total_location_count - len(world.itempool)


        excluded_items: set[str] = set()

        if world.options.start_with_worker.value != 0:
            starting_worker = WORKERS_ITEM_BY_ID[
                ITEMS_WORKER_OFFSET + world.options.start_with_worker.value
            ].value
            excluded_items.add(starting_worker)

        optional_items: list[ItemData] = [
            *diy_items,
            *expansion_items,
            *all_worker_items,
        ]

        available_slots = max(0, _remaining - _filler_space)

        possible_items: list[ItemTypeEnum] = [
            item_data.type
            for item_data in optional_items
            if item_data.type.value not in excluded_items
            for _ in range(item_data.amount)
        ]

        world.random.shuffle(possible_items)

        for item_type in possible_items[:available_slots]:
            create_single_item(world, item_type)

    else:
        for item_data in all_diy_items:
            create_item(world, item_data)

        for item_data in all_expansion_items:
            create_item(world, item_data)

        for item_data in all_worker_items:
            create_item(world, item_data)

    _remaining = total_location_count - len(world.itempool)

    trap_count = round(
        _remaining * world.options.trap_fill.value / 100) if world.options.trap_fill.value > 0 else 0

    junk_count = _remaining - trap_count

    if trap_count > 0 == sum(world.options.trap_weights.value.values()):
        junk_count += trap_count
        trap_count = 0

    if junk_count > 0:
        junk: list[str] = world.random.choices(
            list(world.options.filler_weights.value.keys()),
            weights=list(world.options.filler_weights.value.values()),
            k=junk_count
        )
        for junk_name in junk:
            create_filler_item(world, junk_name)

    if trap_count > 0:
        traps: list[str] = world.random.choices(
            list(world.options.trap_weights.value.keys()),
            weights=list(world.options.trap_weights.value.values()),
            k=trap_count
        )
        for trap_name in traps:
            create_filler_item(world, trap_name)

    if world.multiworld.players > 1 and world.options.card_sanity.value > 0:
        capacity = (
                len(world.sanity_fill_locations)
                + len(world.backup_sanity_fill_locations)
        )

        world.random.shuffle(world.filler_items)

        reserved_count = min(len(world.filler_items), capacity)

        reserved_fillers = world.filler_items[:reserved_count]
        normal_fillers = world.filler_items[reserved_count:]

        world.filler_items = reserved_fillers
    else:
        normal_fillers = world.filler_items
        world.filler_items = []

    world.multiworld.itempool.extend(world.itempool)
    world.multiworld.itempool.extend(normal_fillers)

    return starting_items, ghost_card_amounts



def create_event(world: "TCGSimulatorWorld", region_name: str, item_name: str, loc_name: str | None = None,
                 rule: CollectionRule | Rule[TCGSimulatorBase] = True_()) -> None:
    if loc_name is None:
        loc_name = "Event " + item_name
    region = world.get_region(region_name)
    event_loc = Location(world.player, loc_name, None, region)
    world.set_rule(event_loc, rule)
    event_loc.place_locked_item(
        Item(item_name, ItemClassification.progression, None, world.player))
    region.locations.append(event_loc)

def create_events(world: "TCGSimulatorWorld"):
    if world.options.goal.value == world.options.goal.option_reach_max_level:
        create_event(world, region_name=get_level_region(world.options.max_level.value).value,
                     item_name="Victory", loc_name="Reach Max Level")
