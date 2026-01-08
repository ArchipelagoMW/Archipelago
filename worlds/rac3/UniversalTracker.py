from typing import Any, TYPE_CHECKING

from .Rac3Addresses import ADDRESSES, LOCATIONS

if TYPE_CHECKING:
    from . import RaC3World


def setup_options_from_slot_data(world: "RaC3World") -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if world.game in world.multiworld.re_gen_passthrough:
            world.using_ut = True
            world.passthrough = world.multiworld.re_gen_passthrough[world.game]
            world.options.start_inventory_from_pool.value = world.passthrough["options"]["start_inventory_from_pool"]
            world.options.starting_weapons.value = world.passthrough["options"]["starting_weapons"]
            world.options.bolt_and_xp_multiplier.value = world.passthrough["options"]["bolt_and_xp_multiplier"]
            world.options.enable_progressive_weapons.value = world.passthrough["options"][
                "enable_progressive_weapons"]
            world.options.extra_armor_upgrade.value = world.passthrough["options"]["extra_armor_upgrade"]
            world.options.skill_points.value = world.passthrough["options"]["skill_points"]
            world.options.trophies.value = world.passthrough["options"]["trophies"]
            world.options.titanium_bolts.value = world.passthrough["options"]["titanium_bolts"]
            world.options.nanotech_milestones.value = world.passthrough["options"]["nanotech_milestones"]
        else:
            world.using_ut = False
    else:
        world.using_ut = False


def map_page_index(data: Any) -> int:
    planet_values = ADDRESSES["SCUS-97353"]["PlanetValues"]
    # exception(f'Looking up key: {data}')
    return planet_values.get(data, 0)


def poptracker_data() -> dict[str, int]:
    return {loc["Name"]: loc["Id"] for loc in LOCATIONS}


tracker_world = {
    "map_page_maps": "maps/maps.json",
    "map_page_locations": "locations/locations.json",
    "map_page_setting_key": r'rac3_current_planet_{player}_{team}',
    "map_page_index": map_page_index,
    "poptracker_name_mapping": poptracker_data()
}
