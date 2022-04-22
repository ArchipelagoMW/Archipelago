from .ExtractedData import region_names, exits, connectors


def create_regions(world, player: int):
    from . import create_region, HKLocation, HKItem
    world.regions.append(create_region(world, player, 'Menu', None, ['Hollow Nest S&Q']))
    for region in region_names:
        world.regions.append(create_region(world, player, region, [],
                                           exits.get(region, [])))
    for entrance_name, exit_name in connectors.items():
        if exit_name:
            target_region = world.get_entrance(exit_name, player).parent_region
            world.get_entrance(entrance_name, player).connect(target_region)
            if not entrance_name.endswith("_R"):
                # a traversable entrance puts the name of the target door "into logic".
                loc = HKLocation(player, exit_name, None, target_region)
                loc.place_locked_item(HKItem(exit_name,
                                             not exit_name.startswith("White_Palace_"),
                                             None, "Event", player))
                target_region.locations.append(loc)
        else:
            ent = world.get_entrance(entrance_name, player)
            ent.parent_region.exits.remove(ent)


