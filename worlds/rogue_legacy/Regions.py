import typing

from BaseClasses import MultiWorld, Region, RegionType, Entrance, ItemClassification
from .Items import LegacyItem
from .Locations import LegacyLocation, diary_location_table, location_table, base_location_table
from .Names import LocationName, ItemName

prog = ItemClassification.progression


def create_regions(world, player: int):

    locations: typing.List[str] = []

    # Add required locations.
    locations += [location for location in base_location_table]
    locations += [location for location in diary_location_table]

    # Add chests per settings.
    if world.universal_fairy_chests[player]:
        fairies = int(world.fairy_chests_per_zone[player]) * 4
        for i in range(0, fairies):
            locations += [f"Fairy Chest {i + 1}"]
    else:
        fairies = int(world.fairy_chests_per_zone[player])
        for i in range(0, fairies):
            locations += [f"{LocationName.castle} - Fairy Chest {i + 1}"]
            locations += [f"{LocationName.garden} - Fairy Chest {i + 1}"]
            locations += [f"{LocationName.tower} - Fairy Chest {i + 1}"]
            locations += [f"{LocationName.dungeon} - Fairy Chest {i + 1}"]

    if world.universal_chests[player]:
        chests = int(world.chests_per_zone[player]) * 4
        for i in range(0, chests):
            locations += [f"Chest {i + 1}"]
    else:
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
    world.get_location(LocationName.castle, player).place_locked_item(LegacyItem(ItemName.boss_castle, prog, None, player))
    world.get_location(LocationName.garden, player).place_locked_item(LegacyItem(ItemName.boss_forest, prog, None, player))
    world.get_location(LocationName.tower, player).place_locked_item(LegacyItem(ItemName.boss_tower, prog, None, player))
    world.get_location(LocationName.dungeon, player).place_locked_item(LegacyItem(ItemName.boss_dungeon, prog, None, player))
    world.get_location(LocationName.fountain, player).place_locked_item(LegacyItem(ItemName.boss_fountain, prog, None, player))


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    # Shamelessly stolen from the ROR2 definition, lol
    ret = Region(name, RegionType.Generic, name, player)
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
