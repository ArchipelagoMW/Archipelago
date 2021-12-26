def create_regions(world, player: int):
    from . import create_region
    from .Locations import location_table

    world.regions += [
        create_region(world, player, "Menu", None, ["Outside Castle Hamson"]),
        create_region(world, player, "Castle Hamson",
                      [location for location in location_table]),
    ]

    world.get_entrance("Outside Castle Hamson", player).connect(
        world.get_region("Castle Hamson", player))
