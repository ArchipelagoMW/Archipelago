def create_regions(world, player: int):
    from . import create_region
    from .Locations import location_table

    world.regions += [
        create_region(world, player, 'Menu', None, ['Neow\'s Room']),
        create_region(world, player, 'The Spire', [location for location in location_table])
    ]

    # link up our region with the entrance we just made
    world.get_entrance('Neow\'s Room', player).connect(world.get_region('The Spire', player))
