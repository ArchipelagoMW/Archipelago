from BaseClasses import Region

from .Locations import PokemonHGSSLocation


def create_region(world, name: str, locations=None) -> Region:
    region = Region(name, world.player, world.multiworld)

    if locations:
        for location_name, location_id in locations.items():
            location = PokemonHGSSLocation(
                world.player,
                location_name,
                location_id,
                region,
            )
            region.locations.append(location)

    return region