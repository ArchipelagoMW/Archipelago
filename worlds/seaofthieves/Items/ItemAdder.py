from ..Configurations import SotOptionsDerived
from BaseClasses import MultiWorld, Region, Entrance, ItemClassification
from ..Items.Items import Items, SOTItem
from ..Items.ItemCollection import ItemCollection
import math


def create_items(world: MultiWorld, location_count: int, options: SotOptionsDerived, itemCollection: ItemCollection,
                 player: int):
    update_items_from_options(options, itemCollection)

    # we know the pre fill locations cannot be used
    location_count = location_count - itemCollection.pre_fill_count

    location_count -= __add_main_items(world, itemCollection, player)
    location_count -= __add_fill_and_traps(world, itemCollection, player, location_count, options)

    if (location_count != 0):
        raise Exception(
            "In item creation, items added to the pool resulted in {} locations remaining.".format(location_count))


def update_items_from_options(options: SotOptionsDerived, itemCollection: ItemCollection):
    itemCollection.informCollectionOfPrefillAction(Items.seal_gh.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.seal_ma.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.seal_af.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.seal_rb.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.seal_oos.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.pirate_legend.name, 1)
    itemCollection.informCollectionOfPrefillAction(Items.sail.name, 1)


def __add_main_items(world: MultiWorld, itemCollection: ItemCollection, player: int) -> int:
    count = 0
    for detail in itemCollection.progression:
        count_to_add_to_world = detail.countToSpawnByDefault - itemCollection.getPreFillCountForName(detail.name)
        if count_to_add_to_world < 0:
            count_to_add_to_world = 0
        for i in range(count_to_add_to_world):
            world.itempool.append(SOTItem(detail.name, detail.classification, detail.id, player))
            count += 1
    return count


def __add_fill_and_traps(world: MultiWorld, itemCollection: ItemCollection, player: int, count: int,
                         options: SotOptionsDerived):
    # trap count
    trap_count = int(math.floor(float(count) * (float(options.trapsPercentage) / 100.0)))
    fill_count = count - trap_count
    cnt_added = 0

    # Add filler items
    for i in range(fill_count):
        detail = world.random.choice(itemCollection.filler)
        world.itempool.append(SOTItem(detail.name, detail.classification, detail.id, player))
        cnt_added += 1

    # Add trap items
    for i in range(trap_count):
        detail = world.random.choice(itemCollection.trap)
        world.itempool.append(SOTItem(detail.name, detail.classification, detail.id, player))
        cnt_added += 1

    return cnt_added
