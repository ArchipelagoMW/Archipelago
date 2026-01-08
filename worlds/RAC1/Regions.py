import typing

from BaseClasses import CollectionState, Location, Region
from .data import Planets
from .data.Items import check_progressive_item, get_gold_bolts
from .data.Locations import LocationData, POOL_GOLD_BOLT, POOL_GOLDEN_WEAPON
from .data.Planets import PlanetData
from ..generic.Rules import forbid_item

if typing.TYPE_CHECKING:
    from . import RacWorld


class RacLocation(Location):
    game: str = "Ratchet & Clank"


def create_regions(world: 'RacWorld'):
    # create all regions and populate with locations
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    for planet_data in Planets.LOGIC_PLANETS:
        if planet_data.locations:
            def generate_planet_access_rule(planet: PlanetData) -> typing.Callable[[CollectionState], bool]:
                def planet_access_rule(state: CollectionState):
                    # Connect with special case access rules (not relevant for rac1?)
                    # if planet == Planets.TABORA:
                    #     return (
                    #         state.has(Items.coord_for_planet(planet.number).name, world.player)
                    #         and can_heli(state, world.player)
                    #         and can_swingshot(state, world.player)
                    #     )
                    # if planet == Planets.ARANOS_PRISON:
                    #     return (
                    #         state.has(Items.coord_for_planet(planet.number).name, world.player)
                    #         and state.has_all([
                    #             Items.GRAVITY_BOOTS.name, Items.LEVITATOR.name, Items.INFILTRATOR.name], world.player
                    #         )
                    #     )
                    # Connect with general case access rule
                    # else:
                    return state.has(planet.name, world.player)

                return planet_access_rule

            region = Region(planet_data.name, world.player, world.multiworld)
            world.multiworld.regions.append(region)
            menu.connect(region, None, generate_planet_access_rule(planet_data))

            for location_data in planet_data.locations:
                def generate_access_rule(loc: LocationData) -> typing.Callable[[CollectionState], bool]:
                    def access_rule(state: CollectionState):
                        if loc.access_rule:
                            return loc.access_rule(state, world.player)
                        return True

                    return access_rule

                region.add_locations({location_data.name: location_data.location_id}, RacLocation)
                if POOL_GOLD_BOLT in location_data.pools:
                    location_data.vanilla_item = get_gold_bolts(world.options)
                elif location_data.vanilla_item is not None:
                    location_data.vanilla_item = check_progressive_item(world.options, location_data.vanilla_item)

                location = world.multiworld.get_location(location_data.name, world.player)
                location.access_rule = generate_access_rule(location_data)
                if POOL_GOLDEN_WEAPON in location_data.pools:
                    forbid_item(location, get_gold_bolts(world.options), world.player)

    # from Utils import visualize_regions
    # visualize_regions(world.multiworld.get_region("Menu", world.player), "my_world.puml")
