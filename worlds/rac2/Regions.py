import typing

from BaseClasses import CollectionState, Region, Location
from .Logic import can_heli, can_swingshot
from .data import Planets
from .data import Items
from .data.Planets import PlanetData
from .data.Locations import LocationData

if typing.TYPE_CHECKING:
    from . import Rac2World


class Rac2Location(Location):
    game: str = "Ratchet & Clank 2"


def create_regions(world: 'Rac2World'):
    # create all regions and populate with locations
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    for planet_data in Planets.LOGIC_PLANETS:
        if planet_data.locations:
            def generate_planet_access_rule(planet: PlanetData) -> typing.Callable[[CollectionState], bool]:
                def planet_access_rule(state: CollectionState):
                    # Connect with special case access rules
                    if planet == Planets.TABORA:
                        return (
                            state.has(Items.coord_for_planet(planet.number).name, world.player)
                            and can_heli(state, world.player)
                            and can_swingshot(state, world.player)
                        )
                    if planet == Planets.ARANOS_PRISON:
                        return (
                            state.has(Items.coord_for_planet(planet.number).name, world.player)
                            and state.has_all([
                                Items.GRAVITY_BOOTS.name, Items.LEVITATOR.name, Items.INFILTRATOR.name], world.player
                            )
                        )
                    # Connect with general case access rule
                    else:
                        return state.has(Items.coord_for_planet(planet.number).name, world.player)
                return planet_access_rule

            region = Region(planet_data.name, world.player, world.multiworld)
            world.multiworld.regions.append(region)
            menu.connect(region, None, generate_planet_access_rule(planet_data))

            options_dict = world.get_options_as_dict()
            for location_data in planet_data.locations:
                # Don't create the location if there is an "enable_if" clause and it returned False
                if location_data.enable_if is not None and not location_data.enable_if(options_dict):
                    continue

                def generate_access_rule(loc: LocationData) -> typing.Callable[[CollectionState], bool]:
                    def access_rule(state: CollectionState):
                        if loc.access_rule:
                            return loc.access_rule(state, world.player)
                        return True
                    return access_rule

                region.add_locations({location_data.name: location_data.location_id}, Rac2Location)
                location = world.multiworld.get_location(location_data.name, world.player)
                location.access_rule = generate_access_rule(location_data)

    # from Utils import visualize_regions
    # visualize_regions(world.multiworld.get_region("Menu", world.player), "my_world.puml")
