from BaseClasses import MultiWorld, Region, ItemClassification
from .Items import CCCharlesItem
from .Options import CCCharlesOptions
from .Locations import (
    CCCharlesLocation, loc_start_camp, loc_tony_tiddle_mission, loc_barn, loc_candice_mission, \
    loc_tutorial_house, loc_swamp_edges, loc_swamp_mission, loc_junkyard_area, loc_south_house, \
    loc_junkyard_shed, loc_military_base, loc_south_mine_outside, loc_south_mine_inside, \
    loc_middle_station, loc_canyon, loc_watchtower, loc_boulder_field, loc_haunted_house, \
    loc_santiago_house, loc_port, loc_trench_house, loc_doll_woods, loc_lost_stairs, loc_east_house, \
    loc_rockets_testing_ground, loc_rockets_testing_bunker, loc_workshop, loc_east_tower, \
    loc_lighthouse, loc_north_mine_outside, loc_north_mine_inside, loc_wood_bridge, loc_museum, \
    loc_barbed_shelter, loc_west_beach, loc_church, loc_west_cottage, loc_caravan, loc_trailer_cabin, \
    loc_towers, loc_north_beach, loc_mine_shaft, loc_mob_camp, loc_mob_camp_locked_room, \
    loc_mine_elevator_exit, loc_mountain_ruin_outside, loc_mountain_ruin_inside, loc_prism_temple, \
    loc_pickle_val, loc_shrine_near_temple, loc_morse_bunker
)


def create_regions(world: MultiWorld, options: CCCharlesOptions, player: int) -> None:
    menu_region = Region("Menu", player, world, "Aranearum")
    world.regions.append(menu_region)

    start_camp_region = Region("Start Camp", player, world)
    start_camp_region.add_locations(loc_start_camp, CCCharlesLocation)
    world.regions.append(start_camp_region)

    tony_tiddle_mission_region = Region("Tony Tiddle Mission", player, world)
    tony_tiddle_mission_region.add_locations(loc_tony_tiddle_mission, CCCharlesLocation)
    world.regions.append(tony_tiddle_mission_region)

    barn_region = Region("Barn", player, world)
    barn_region.add_locations(loc_barn, CCCharlesLocation)
    world.regions.append(barn_region)

    candice_mission_region = Region("Candice Mission", player, world)
    candice_mission_region.add_locations(loc_candice_mission, CCCharlesLocation)
    world.regions.append(candice_mission_region)

    tutorial_house_region = Region("Tutorial House", player, world)
    tutorial_house_region.add_locations(loc_tutorial_house, CCCharlesLocation)
    world.regions.append(tutorial_house_region)

    swamp_edges_region = Region("Swamp Edges", player, world)
    swamp_edges_region.add_locations(loc_swamp_edges, CCCharlesLocation)
    world.regions.append(swamp_edges_region)

    swamp_mission_region = Region("Swamp Mission", player, world)
    swamp_mission_region.add_locations(loc_swamp_mission, CCCharlesLocation)
    world.regions.append(swamp_mission_region)

    junkyard_area_region = Region("Junkyard Area", player, world)
    junkyard_area_region.add_locations(loc_junkyard_area, CCCharlesLocation)
    world.regions.append(junkyard_area_region)

    south_house_region = Region("South House", player, world)
    south_house_region.add_locations(loc_south_house, CCCharlesLocation)
    world.regions.append(south_house_region)

    junkyard_shed_region = Region("Junkyard Shed", player, world)
    junkyard_shed_region.add_locations(loc_junkyard_shed, CCCharlesLocation)
    world.regions.append(junkyard_shed_region)

    military_base_region = Region("Military Base", player, world)
    military_base_region.add_locations(loc_military_base, CCCharlesLocation)
    world.regions.append(military_base_region)

    south_mine_outside_region = Region("South Mine Outside", player, world)
    south_mine_outside_region.add_locations(loc_south_mine_outside, CCCharlesLocation)
    world.regions.append(south_mine_outside_region)

    south_mine_inside_region = Region("South Mine Inside", player, world)
    south_mine_inside_region.add_locations(loc_south_mine_inside, CCCharlesLocation)
    world.regions.append(south_mine_inside_region)

    middle_station_region = Region("Middle Station", player, world)
    middle_station_region.add_locations(loc_middle_station, CCCharlesLocation)
    world.regions.append(middle_station_region)

    canyon_region = Region("Canyon", player, world)
    canyon_region.add_locations(loc_canyon, CCCharlesLocation)
    world.regions.append(canyon_region)

    watchtower_region = Region("Watchtower", player, world)
    watchtower_region.add_locations(loc_watchtower, CCCharlesLocation)
    world.regions.append(watchtower_region)

    boulder_field_region = Region("Boulder Field", player, world)
    boulder_field_region.add_locations(loc_boulder_field, CCCharlesLocation)
    world.regions.append(boulder_field_region)

    haunted_house_region = Region("Haunted House", player, world)
    haunted_house_region.add_locations(loc_haunted_house, CCCharlesLocation)
    world.regions.append(haunted_house_region)

    santiago_house_region = Region("Santiago House", player, world)
    santiago_house_region.add_locations(loc_santiago_house, CCCharlesLocation)
    world.regions.append(santiago_house_region)

    port_region = Region("Port", player, world)
    port_region.add_locations(loc_port, CCCharlesLocation)
    world.regions.append(port_region)

    trench_house_region = Region("Trench House", player, world)
    trench_house_region.add_locations(loc_trench_house, CCCharlesLocation)
    world.regions.append(trench_house_region)

    doll_woods_region = Region("Doll Woods", player, world)
    doll_woods_region.add_locations(loc_doll_woods, CCCharlesLocation)
    world.regions.append(doll_woods_region)

    lost_stairs_region = Region("Lost Stairs", player, world)
    lost_stairs_region.add_locations(loc_lost_stairs, CCCharlesLocation)
    world.regions.append(lost_stairs_region)

    east_house_region = Region("East House", player, world)
    east_house_region.add_locations(loc_east_house, CCCharlesLocation)
    world.regions.append(east_house_region)

    rockets_testing_ground_region = Region("Rockets Testing Ground", player, world)
    rockets_testing_ground_region.add_locations(loc_rockets_testing_ground, CCCharlesLocation)
    world.regions.append(rockets_testing_ground_region)

    rockets_testing_bunker_region = Region("Rockets Testing Bunker", player, world)
    rockets_testing_bunker_region.add_locations(loc_rockets_testing_bunker, CCCharlesLocation)
    world.regions.append(rockets_testing_bunker_region)

    workshop_region = Region("Workshop", player, world)
    workshop_region.add_locations(loc_workshop, CCCharlesLocation)
    world.regions.append(workshop_region)

    east_tower_region = Region("East Tower", player, world)
    east_tower_region.add_locations(loc_east_tower, CCCharlesLocation)
    world.regions.append(east_tower_region)

    lighthouse_region = Region("Lighthouse", player, world)
    lighthouse_region.add_locations(loc_lighthouse, CCCharlesLocation)
    world.regions.append(lighthouse_region)

    north_mine_outside_region = Region("North Mine Outside", player, world)
    north_mine_outside_region.add_locations(loc_north_mine_outside, CCCharlesLocation)
    world.regions.append(north_mine_outside_region)

    north_mine_inside_region = Region("North Mine Inside", player, world)
    north_mine_inside_region.add_locations(loc_north_mine_inside, CCCharlesLocation)
    world.regions.append(north_mine_inside_region)

    wood_bridge_region = Region("Wood Bridge", player, world)
    wood_bridge_region.add_locations(loc_wood_bridge, CCCharlesLocation)
    world.regions.append(wood_bridge_region)

    museum_region = Region("Museum", player, world)
    museum_region.add_locations(loc_museum, CCCharlesLocation)
    world.regions.append(museum_region)

    barbed_shelter_region = Region("Barbed Shelter", player, world)
    barbed_shelter_region.add_locations(loc_barbed_shelter, CCCharlesLocation)
    world.regions.append(barbed_shelter_region)

    west_beach_region = Region("West Beach", player, world)
    west_beach_region.add_locations(loc_west_beach, CCCharlesLocation)
    world.regions.append(west_beach_region)

    church_region = Region("Church", player, world)
    church_region.add_locations(loc_church, CCCharlesLocation)
    world.regions.append(church_region)

    west_cottage_region = Region("West Cottage", player, world)
    west_cottage_region.add_locations(loc_west_cottage, CCCharlesLocation)
    world.regions.append(west_cottage_region)

    caravan_region = Region("Caravan", player, world)
    caravan_region.add_locations(loc_caravan, CCCharlesLocation)
    world.regions.append(caravan_region)

    trailer_cabin_region = Region("Trailer Cabin", player, world)
    trailer_cabin_region.add_locations(loc_trailer_cabin, CCCharlesLocation)
    world.regions.append(trailer_cabin_region)

    towers_region = Region("Towers", player, world)
    towers_region.add_locations(loc_towers, CCCharlesLocation)
    world.regions.append(towers_region)

    north_beach_region = Region("North beach", player, world)
    north_beach_region.add_locations(loc_north_beach, CCCharlesLocation)
    world.regions.append(north_beach_region)

    mine_shaft_region = Region("Mine Shaft", player, world)
    mine_shaft_region.add_locations(loc_mine_shaft, CCCharlesLocation)
    world.regions.append(mine_shaft_region)

    mob_camp_region = Region("Mob Camp", player, world)
    mob_camp_region.add_locations(loc_mob_camp, CCCharlesLocation)
    world.regions.append(mob_camp_region)

    mob_camp_locked_room_region = Region("Mob Camp Locked Room", player, world)
    mob_camp_locked_room_region.add_locations(loc_mob_camp_locked_room, CCCharlesLocation)
    world.regions.append(mob_camp_locked_room_region)

    mine_elevator_exit_region = Region("Mine Elevator Exit", player, world)
    mine_elevator_exit_region.add_locations(loc_mine_elevator_exit, CCCharlesLocation)
    world.regions.append(mine_elevator_exit_region)

    mountain_ruin_outside_region = Region("Mountain Ruin Outside", player, world)
    mountain_ruin_outside_region.add_locations(loc_mountain_ruin_outside, CCCharlesLocation)
    world.regions.append(mountain_ruin_outside_region)

    mountain_ruin_inside_region = Region("Mountain Ruin Inside", player, world)
    mountain_ruin_inside_region.add_locations(loc_mountain_ruin_inside, CCCharlesLocation)
    world.regions.append(mountain_ruin_inside_region)

    prism_temple_region = Region("Prism Temple", player, world)
    prism_temple_region.add_locations(loc_prism_temple, CCCharlesLocation)
    world.regions.append(prism_temple_region)

    pickle_val_region = Region("Pickle Val", player, world)
    pickle_val_region.add_locations(loc_pickle_val, CCCharlesLocation)
    world.regions.append(pickle_val_region)

    shrine_near_temple_region = Region("Shrine Near Temple", player, world)
    shrine_near_temple_region.add_locations(loc_shrine_near_temple, CCCharlesLocation)
    world.regions.append(shrine_near_temple_region)

    morse_bunker_region = Region("Morse Bunker", player, world)
    morse_bunker_region.add_locations(loc_morse_bunker, CCCharlesLocation)
    world.regions.append(morse_bunker_region)

    # Place "Victory" event at "Final Boss" location
    loc_final_boss = CCCharlesLocation(player, "Final Boss", None, prism_temple_region)
    loc_final_boss.place_locked_item(CCCharlesItem("Victory", ItemClassification.progression, None, player))
    prism_temple_region.locations.append(loc_final_boss)

    # Connect the Regions by named Entrances that must have access Rules
    menu_region.connect(start_camp_region)
    menu_region.connect(tony_tiddle_mission_region)
    menu_region.connect(barn_region, "Barn Door")
    menu_region.connect(candice_mission_region)
    menu_region.connect(tutorial_house_region, "Tutorial House Door")
    menu_region.connect(swamp_edges_region)
    menu_region.connect(swamp_mission_region)
    menu_region.connect(junkyard_area_region)
    menu_region.connect(south_house_region)
    menu_region.connect(junkyard_shed_region)
    menu_region.connect(military_base_region)
    menu_region.connect(south_mine_outside_region)
    south_mine_outside_region.connect(south_mine_inside_region, "South Mine Gate")
    menu_region.connect(middle_station_region)
    menu_region.connect(canyon_region)
    menu_region.connect(watchtower_region)
    menu_region.connect(boulder_field_region)
    menu_region.connect(haunted_house_region)
    menu_region.connect(santiago_house_region)
    menu_region.connect(port_region)
    menu_region.connect(trench_house_region)
    menu_region.connect(doll_woods_region)
    menu_region.connect(lost_stairs_region)
    menu_region.connect(east_house_region)
    menu_region.connect(rockets_testing_ground_region)
    rockets_testing_ground_region.connect(rockets_testing_bunker_region, "Stuck Bunker Door")
    menu_region.connect(workshop_region)
    menu_region.connect(east_tower_region)
    menu_region.connect(lighthouse_region)
    menu_region.connect(north_mine_outside_region)
    north_mine_outside_region.connect(north_mine_inside_region, "North Mine Gate")
    menu_region.connect(wood_bridge_region)
    menu_region.connect(museum_region)
    menu_region.connect(barbed_shelter_region)
    menu_region.connect(west_beach_region)
    menu_region.connect(church_region)
    menu_region.connect(west_cottage_region)
    menu_region.connect(caravan_region)
    menu_region.connect(trailer_cabin_region)
    menu_region.connect(towers_region)
    menu_region.connect(north_beach_region)
    menu_region.connect(mine_shaft_region)
    menu_region.connect(mob_camp_region)
    mob_camp_region.connect(mob_camp_locked_room_region, "Mob Camp Locked Door")
    menu_region.connect(mine_elevator_exit_region)
    menu_region.connect(mountain_ruin_outside_region)
    mountain_ruin_outside_region.connect(mountain_ruin_inside_region, "Mountain Ruin Gate")
    menu_region.connect(prism_temple_region)
    menu_region.connect(pickle_val_region)
    menu_region.connect(shrine_near_temple_region)
    menu_region.connect(morse_bunker_region)
