
from typing import TYPE_CHECKING

from BaseClasses import Item
from .data import ItemTypeEnum
from .data.items import booster_pack_items, figurine_items

if TYPE_CHECKING:
    from . import TCGSimulatorWorld, BoosterPackItems, AccessoriesItems, FigurineItems, TableTopItems


def create_items(world: TCGSimulatorWorld):

    starting_items: list[Item] = []



    starting_items.append(world.create_item(StartingCar.HUNTER_CAVALRY.value))

    starting_events = set(world.random.sample(list(Events), 5))


    for event in starting_events:
        starting_items.append(world.create_item(event.value))

    remaining_events = set(Events) - starting_events

    if world.options.breakable_locks.value:
        for item_type in Blockers:
            create_single_item(world, item_type)
    for item_type in Cars:
        create_single_item(world, item_type)
    for item_type in BurningCars:
        create_single_item(world, item_type)
    for item_type in remaining_events:
        create_single_item(world, item_type)


    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))

    _remaining = total_location_count - len(world.itempool)

    create_item(world, ItemData(Filler.BOOST, _remaining))

    world.multiworld.itempool += world.itempool

    return starting_items