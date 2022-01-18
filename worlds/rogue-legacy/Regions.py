import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import LegacyItem
from .Locations import LegacyLocation, diary_location_table, location_table, base_location_table
from .Names import LocationName, ItemName


def create_regions(world, player: int):

    locations: typing.List[str] = []

    # Add required locations.
    locations += [location for location in base_location_table]
    locations += [location for location in diary_location_table]

    # Add chests per settings.
    fairies = int(world.fairy_chests_per_zone[player])
    for i in range(0, fairies):
        locations += [f"{LocationName.castle} - Fairy Chest {i + 1}"]
        locations += [f"{LocationName.garden} - Fairy Chest {i + 1}"]
        locations += [f"{LocationName.tower} - Fairy Chest {i + 1}"]
        locations += [f"{LocationName.dungeon} - Fairy Chest {i + 1}"]

    chests = int(world.chests_per_zone[player])
    for i in range(0, chests):
        locations += [f"{LocationName.castle} - Chest {i + 1}"]
        locations += [f"{LocationName.garden} - Chest {i + 1}"]
        locations += [f"{LocationName.tower} - Chest {i + 1}"]
        locations += [f"{LocationName.dungeon} - Chest {i + 1}"]

    # Set up the regions correctly.
    world.regions += [
        create_region(world, player, "Menu", None, [LocationName.outside]),
        create_region(world, player, LocationName.castle, locations),
    ]

    # Connect entrances and set up events.
    world.get_entrance(LocationName.outside, player).connect(world.get_region(LocationName.castle, player))
    world.get_location(LocationName.castle, player).place_locked_item(LegacyItem(ItemName.boss_khindr, True, None, player))
    world.get_location(LocationName.garden, player).place_locked_item(LegacyItem(ItemName.boss_alexander, True, None, player))
    world.get_location(LocationName.tower, player).place_locked_item(LegacyItem(ItemName.boss_leon, True, None, player))
    world.get_location(LocationName.dungeon, player).place_locked_item(LegacyItem(ItemName.boss_herodotus, True, None, player))
    world.get_location(LocationName.fountain, player).place_locked_item(LegacyItem(ItemName.boss_fountain, True, None, player))


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    # Shamelessly stolen from the ROR2 definition, lol
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = LegacyLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
