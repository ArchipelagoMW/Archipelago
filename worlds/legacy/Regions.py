from .Constants import TOTAL_LOCATIONS
import typing


def create_regions(world, player: int):
    from . import create_region
    from .Locations import base_location_table, location_table

    locations: typing.List[str] = []

    # Add required locations.
    locations += [location for location in location_table]

    # # Fill remaining spots with chests.
    # chest_counter = -1
    # fairy_counter = 0
    # for i in range(0, TOTAL_LOCATIONS - 67):
    #     zone_cycle = i % 4
    #     zone = ""
    #     if zone_cycle == 0:
    #         zone = "Castle"
    #         chest_counter += 1
    #     elif zone_cycle == 1:
    #         zone = "Garden"
    #     elif zone_cycle == 2:
    #         zone = "Tower"
    #     elif zone_cycle == 3:
    #         zone = "Dungeon"
    #     fairy = chest_counter % 3 == 0
    #     if fairy:
    #         fairy_counter += 1
    #         locations += [f"{zone} Fairy Chest {chest_counter // 3 + 1}"]
    #     else:
    #         locations += [
    #             f"{zone} Chest {chest_counter + 1 - fairy_counter // 4}"]
    #
    # locations += ["Victory"]

    # Set up the regions correctly.
    world.regions += [
        create_region(world, player, "Menu", None, ["Outside Castle Hamson"]),
        create_region(world, player, "Castle Hamson", locations),
    ]
    world.get_entrance("Outside Castle Hamson", player).connect(
        world.get_region("Castle Hamson", player))
