# Key item randomization logic for open mode.

import random

from ...randomizer.data import items as items_data
from ...randomizer.data import chests, keys
from ...randomizer.data.locations import Area
from . import flags


class Inventory(list):
    """List subclass for item inventory during key item shuffle logic."""

    def has_item(self, item):
        """

        Args:
            item: Item class to check for.

        Returns:
            bool: True if inventory contains this item, False otherwise.

        """
        return any([i for i in self if i == item])


def item_location_filter(world, location):
    """Filter function for key item locations based on whether Seed/Fertilizer are included.

    Args:
        world (randomizer.logic.main.GameWorld):
        location (randomizer.data.locations.ItemLocation):

    Returns:
        bool:
    """
    # Don't include Seed/Fertilizer spots unless enabled.
    if (isinstance(location, (keys.Seed, keys.Fertilizer)) and
            not world.settings.is_flag_enabled(flags.IncludeSeedFertilizer)):
        return False

    # Don't include Bright Card spot unless enabled.
    if (isinstance(location, keys.KnifeGuy) and
            not world.settings.is_flag_enabled(flags.IncludeBrightCard)):
        return False

    # Check if including chests.
    if (isinstance(location, (chests.Chest, chests.Reward)) and
            not world.settings.is_flag_enabled(flags.ChestIncludeKeyItems)):
        return False

    # Check flags for extra locations: 3D maze, super jump rewards, Culex.
    if isinstance(location, chests.SunkenShip3DMaze) and not world.settings.is_flag_enabled(flags.ChestKIInclude3DMaze):
        return False

    if isinstance(location, chests.CulexReward) and not world.settings.is_flag_enabled(flags.ChestKIIncludeCulex):
        return False

    if isinstance(location, chests.SuperJumps30) and not world.settings.is_flag_enabled(flags.ChestKIInclude30):
        return False

    if isinstance(location, chests.SuperJumps100) and not world.settings.is_flag_enabled(flags.ChestKIInclude100):
        return False

    # Don't put key items in missable locations.
    if location.missable:
        return False

    # Exclude anything in the factory by default.
    if location.area == Area.Factory:
        return False

    # Exclude Bowser's Keep if not open.
    if location.area == Area.BowsersKeep and not world.settings.is_flag_enabled(flags.BowsersKeepOpen):
        return False

    # Everything else is fine.
    return True


def _place_items(world, items, locations, ap_data, base_inventory=None):
    """Place the given list of items within the given locations, and optionally a given starting inventory.

    Args:
        world (randomizer.logic.main.GameWorld):
        items (Inventory):
        locations (list[randomizer.data.locations.ItemLocation]):
        base_inventory (Inventory):

    """
    if base_inventory is None:
        base_inventory = Inventory()

    remaining_fill_items = Inventory(items)

    if len(remaining_fill_items) > len([l for l in locations if not l.has_item]):
        raise ValueError("Trying to fill more items than available locations")

    for location in locations:
        location.item = ap_data[location.name]

    # For each required item, place it assuming we can get all other items.
    #for item in items:
        # Get items we can get assuming we have everything but the one we're placing.
    #    remaining_fill_items.remove(item)
    #    assumed_items = _collect_items(world, remaining_fill_items + base_inventory)

    #    fillable_locations = [l for l in locations if not l.has_item and l.can_access(assumed_items)
    #                          and l.item_allowed(item)]
        #fillable_locations = [l for l in locations if not l.has_item and l.can_access(assumed_items)
        #                      and l.item_allowed(item)]

    #    if not fillable_locations:
    #        raise ValueError("No available locations for {}, {}".format(item, remaining_fill_items))

        # Place item in the first fillable location.
    #    fillable_locations[0].item = item



def _collect_items(world, collected=None):
    """Collect the available items in the world.

    Args:
        world (randomizer.logic.main.GameWorld): Game world
        collected (Inventory): Already collected items to start.

    Returns:
        Inventory: Collected items.

    """
    my_items = Inventory()
    if collected is not None:
        my_items.extend(collected)

    available_locations = [l for l in world.key_locations + world.chest_locations if l.has_item]

    # Search all locations and collect items until we can't get any more.
    while True:
        search_locations = [l for l in available_locations if l.can_access(my_items)]
        available_locations = [l for l in available_locations if l not in search_locations]
        found_items = Inventory([l.item for l in search_locations])
        my_items.extend(found_items)
        if len(found_items) == 0:
            break

    return my_items


def randomize_all(world, ap_data):
    """

    Args:
        world (randomizer.logic.main.GameWorld): Game world to randomize.

    """
    # Open mode-specific shuffles.
    if world.open_mode:
        # Shuffle key item locations.
        if (world.settings.is_flag_enabled(flags.KeyItemShuffle) and
                not world.settings.is_flag_enabled(flags.ChestIncludeKeyItems)):
            locations_to_fill = [l for l in world.key_locations if item_location_filter(world, l)]
            required_items = Inventory([l.item for l in locations_to_fill if
                                        l.item.shuffle_type == items_data.ItemShuffleType.Required])
            extra_items = Inventory([l.item for l in locations_to_fill if
                                     l.item.shuffle_type == items_data.ItemShuffleType.Extra])

            # Fill in locations.
            fill_locations(world, locations_to_fill, required_items, extra_items, ap_data=ap_data)
            pass


def fill_locations(world, locations_to_fill, required_items, extra_items=None, ap_data=None):
    """Fill the given locations with the given required and extra items.

    Args:
        world (randomizer.logic.main.GameWorld): Game world to randomize.
        locations_to_fill (list[randomizer.data.locations.ItemLocation]): Locations to fill.
        required_items (Inventory): Required items to place.
        extra_items (Inventory): Extra items to place.
        ap_data (dict[str, str]): Archipelago placement data.

    """
    if extra_items is None:
        extra_items = Inventory()
    if ap_data is None:
        ap_data = dict()

    required_items = []
    extra_items = []

    # Sanity check to make sure we're filling the right number of spots.
    if len(locations_to_fill) < len(required_items) + len(extra_items):
        raise ValueError("Not enough locations for number of items.")

    # Clear existing items to start.
    for location in locations_to_fill:
        location.item = None

    # Shuffle locations, required items and extra items.
    random.shuffle(locations_to_fill)
    random.shuffle(required_items)
    random.shuffle(extra_items)

    # Reverse remaining empty locations, then fill extra items.
    locations_to_fill = [l for l in locations_to_fill if not l.has_item]
    locations_to_fill.reverse()
    _place_items(world, extra_items, locations_to_fill, ap_data)

    # Sanity check to make sure we can collect all the items.
    collected_items = set(_collect_items(world))
    leftover = set(required_items + extra_items) - collected_items
    if leftover:
        raise ValueError("Items leftover from collection: {!r}, leftover {!r}".format(
            locations_to_fill, leftover))
