def create_regions(world, player: int):
    from . import create_region
    from .Locations import lookup_name_to_id as location_lookup_name_to_id

    world.regions += [
        create_region(world, player, 'Startup', None, ['Games Menu']),
        create_region(world, player, 'Solitaire', [location for location in location_lookup_name_to_id])
    ]
