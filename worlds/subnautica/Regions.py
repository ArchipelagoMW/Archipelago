def create_regions(world, player: int):
    from . import create_region
    from .Locations import lookup_name_to_id as location_lookup_name_to_id, events

    world.regions += [
        create_region(world, player, 'Menu', None, ['Lifepod 5']),
        create_region(world, player, 'Planet 4546B', events + list(location_lookup_name_to_id))
    ]
