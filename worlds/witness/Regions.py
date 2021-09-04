def create_regions(world, player: int):
    from . import create_region
    from .Locations import location_table

    world.regions += [
        create_region(world, player, 'Menu', None, ["The Splashscreen?"]),
        create_region(world, player, 'Witness Island', [location for location in location_table])
    ]

    world.get_entrance("The Splashscreen?", player).connect(world.get_region('Witness Island', player))