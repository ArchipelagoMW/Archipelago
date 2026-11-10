from typing import TYPE_CHECKING, List
from BaseClasses import Item, Location, Region
from .Locations import exclusion_table
from .Locations import advancement_table as location_table
from .er_data import undertale_er_regions, portal_mapping, Portal
from .er_rules import set_er_region_rules
import platformdirs
import os
from typing import Dict
from rule_builder.rules import CanReachLocation, CanReachRegion

if TYPE_CHECKING:
    from . import UndertaleWorld


class UndertaleERItem(Item):
    game: str = "Undertale"


class UndertaleERLocation(Location):
    game: str = "Undertale"


def create_er_regions_vanilla(world: "UndertaleWorld"):
    temp_portal_mapping = portal_mapping.copy()

    regions: Dict[str, Region] = {}

    for region_name, region_data in undertale_er_regions.items():
            regions[region_name] = Region(region_name, world.player, world.multiworld)

    for location_name, location_id in location_table.items():
        if regions.__contains__(location_table[location_name].er_region) and (
                location_name not in exclusion_table["NoKills"] or (world.options.kill_sanity != 0 and (
                world.options.route_required == "genocide" or world.options.route_required == "all_routes"))) and (
                location_name not in exclusion_table["NoStats"] or (world.options.rando_stats and (
                world.options.route_required == "genocide" or world.options.route_required == "all_routes"))) and (
                location_name not in exclusion_table["ChestLocations"] or
                world.options.bonus_locations) and (
                "Hub Shop " not in location_name) and (
                location_name not in exclusion_table["NoLove"] or (world.options.rando_love and (
                world.options.route_required == "genocide" or world.options.route_required == "all_routes"))) and (
                location_name not in exclusion_table["NoSpare"]) and \
                location_name not in exclusion_table[world.options.route_required.current_key]:
            if "Approach Door " not in location_name or (location_name.removeprefix("Approach Door ") in world.all_door_locks):
                region = regions[location_table[location_name].er_region]
                location = UndertaleERLocation(world.player, location_name, location_id.id, region)
                region.locations.append(location)

    for region_name, region_data in undertale_er_regions.items():
        if world.options.spare_sanity != 0 and world.options.route_required != "genocide":
            if region_name == "Ruins Grind Rooms":
                regions[region_name].locations += [
                    UndertaleERLocation(world.player, "Ruins Spare " + str(i + 1), 78013 + i, regions[region_name])
                    for i in range(world.options.spare_sanity_max.value)]
            elif region_name == "Snowdin Grind Rooms":
                regions[region_name].locations += [
                    UndertaleERLocation(world.player, "Snowdin Spare " + str(i + 1), 78113 + i,
                                        regions[region_name]) for i in
                    range(world.options.spare_sanity_max.value)]
            elif region_name == "Waterfall Grind Rooms":
                regions[region_name].locations += [
                    UndertaleERLocation(world.player, "Waterfall Spare " + str(i + 1), 78213 + i,
                                        regions[region_name]) for i in
                    range(world.options.spare_sanity_max.value)]
            elif region_name == "Hotland Grind Rooms":
                regions[region_name].locations += [
                    UndertaleERLocation(world.player, "Hotland Spare " + str(i + 1), 78313 + i,
                                        regions[region_name]) for i in
                    range(world.options.spare_sanity_max.value)]

    for region in regions.values():
        world.multiworld.regions.append(region)

    set_er_region_rules(world)
    created_info_dumps: List[str] = []
    to_path = os.path.join(platformdirs.user_config_dir(appname="UNDERTALEAP", ensure_exists=True, appauthor=False), "room_door_names_list.txt")
    with open(to_path, "w") as f:
                f.close()
    while len(temp_portal_mapping) > 0:
        world.get_region(temp_portal_mapping[0].region).add_exits({temp_portal_mapping[0].destination: temp_portal_mapping[0].destination_string()})
        if ((temp_portal_mapping[0].scene() + ":" + temp_portal_mapping[0].destination_scene()) not in created_info_dumps) and temp_portal_mapping[0].scene() != "room_area1" and temp_portal_mapping[0].destination_scene() != "room_area1":
            with open(to_path, "a") as f:
                f.write(temp_portal_mapping[0].scene() + ":" + temp_portal_mapping[0].destination_scene() + "\n")
                created_info_dumps.append(temp_portal_mapping[0].scene() + ":" + temp_portal_mapping[0].destination_scene())
                created_info_dumps.append(temp_portal_mapping[0].destination_scene() + ":" + temp_portal_mapping[0].scene())
                f.close()
        temp_portal_mapping.remove(temp_portal_mapping[0])

    undertale_er_add_extra_region_info(world, regions)


def undertale_er_add_extra_region_info(world: "UndertaleWorld", regions: Dict[str, Region]):

    world.multiworld.register_indirect_condition(regions["room_fire_shootguy_2"],
                                                 world.multiworld.get_entrance("Fire Door 1 Block", world.player))
    world.multiworld.register_indirect_condition(regions["room_fire_shootguy_1"],
                                                 world.multiworld.get_entrance("Fire Door 1 Block", world.player))

    world.multiworld.register_indirect_condition(regions["room_fire_shootguy_3"],
                                                 world.multiworld.get_entrance("Fire Door 2 Block", world.player))
    world.multiworld.register_indirect_condition(regions["room_fire_shootguy_4"],
                                                 world.multiworld.get_entrance("Fire Door 2 Block", world.player))

    if world.options.route_required.current_key == "neutral":
        world.set_completion_rule(CanReachRegion("room_castle_throneroom"))
    elif world.options.route_required.current_key == "pacifist" or \
            world.options.route_required.current_key == "all_routes":
        world.set_completion_rule(CanReachRegion("room_castle_throneroom") & CanReachLocation("Popato Chisps Machine"))
    elif world.options.route_required.current_key == "genocide":
        world.set_completion_rule(CanReachRegion("room_castle_throneroom"))
