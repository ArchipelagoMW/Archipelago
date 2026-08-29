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


def create_regions(multiworld: MultiWorld, options: CCCharlesOptions, player: int) -> None:
    menu_region = Region("Menu", player, multiworld, "Aranearum")
    multiworld.regions.append(menu_region)

    start_camp_region = Region("Start Camp", player, multiworld)
    start_camp_region.add_locations(loc_start_camp, CCCharlesLocation)
    multiworld.regions.append(start_camp_region)

    tony_tiddle_mission_region = Region("Tony Tiddle Mission", player, multiworld)
    tony_tiddle_mission_region.add_locations(loc_tony_tiddle_mission, CCCharlesLocation)
    multiworld.regions.append(tony_tiddle_mission_region)

    barn_region = Region("Barn", player, multiworld)
    barn_region.add_locations(loc_barn, CCCharlesLocation)
    multiworld.regions.append(barn_region)

    candice_mission_region = Region("Candice Mission", player, multiworld)
    candice_mission_region.add_locations(loc_candice_mission, CCCharlesLocation)
    multiworld.regions.append(candice_mission_region)

    tutorial_house_region = Region("Tutorial House", player, multiworld)
    tutorial_house_region.add_locations(loc_tutorial_house, CCCharlesLocation)
    multiworld.regions.append(tutorial_house_region)

    swamp_edges_region = Region("Swamp Edges", player, multiworld)
    swamp_edges_region.add_locations(loc_swamp_edges, CCCharlesLocation)
    multiworld.regions.append(swamp_edges_region)

    swamp_mission_region = Region("Swamp Mission", player, multiworld)
    swamp_mission_region.add_locations(loc_swamp_mission, CCCharlesLocation)
    multiworld.regions.append(swamp_mission_region)

    junkyard_area_region = Region("Junkyard Area", player, multiworld)
    junkyard_area_region.add_locations(loc_junkyard_area, CCCharlesLocation)
    multiworld.regions.append(junkyard_area_region)

    south_house_region = Region("South House", player, multiworld)
    south_house_region.add_locations(loc_south_house, CCCharlesLocation)
    multiworld.regions.append(south_house_region)

    junkyard_shed_region = Region("Junkyard Shed", player, multiworld)
    junkyard_shed_region.add_locations(loc_junkyard_shed, CCCharlesLocation)
    multiworld.regions.append(junkyard_shed_region)

    military_base_region = Region("Military Base", player, multiworld)
    military_base_region.add_locations(loc_military_base, CCCharlesLocation)
    multiworld.regions.append(military_base_region)

    south_mine_outside_region = Region("South Mine Outside", player, multiworld)
    south_mine_outside_region.add_locations(loc_south_mine_outside, CCCharlesLocation)
    multiworld.regions.append(south_mine_outside_region)

    south_mine_inside_region = Region("South Mine Inside", player, multiworld)
    south_mine_inside_region.add_locations(loc_south_mine_inside, CCCharlesLocation)
    multiworld.regions.append(south_mine_inside_region)

    middle_station_region = Region("Middle Station", player, multiworld)
    middle_station_region.add_locations(loc_middle_station, CCCharlesLocation)
    multiworld.regions.append(middle_station_region)

    canyon_region = Region("Canyon", player, multiworld)
    canyon_region.add_locations(loc_canyon, CCCharlesLocation)
    multiworld.regions.append(canyon_region)

    watchtower_region = Region("Watchtower", player, multiworld)
    watchtower_region.add_locations(loc_watchtower, CCCharlesLocation)
    multiworld.regions.append(watchtower_region)

    boulder_field_region = Region("Boulder Field", player, multiworld)
    boulder_field_region.add_locations(loc_boulder_field, CCCharlesLocation)
    multiworld.regions.append(boulder_field_region)

    haunted_house_region = Region("Haunted House", player, multiworld)
    haunted_house_region.add_locations(loc_haunted_house, CCCharlesLocation)
    multiworld.regions.append(haunted_house_region)

    santiago_house_region = Region("Santiago House", player, multiworld)
    santiago_house_region.add_locations(loc_santiago_house, CCCharlesLocation)
    multiworld.regions.append(santiago_house_region)

    port_region = Region("Port", player, multiworld)
    port_region.add_locations(loc_port, CCCharlesLocation)
    multiworld.regions.append(port_region)

    trench_house_region = Region("Trench House", player, multiworld)
    trench_house_region.add_locations(loc_trench_house, CCCharlesLocation)
    multiworld.regions.append(trench_house_region)

    doll_woods_region = Region("Doll Woods", player, multiworld)
    doll_woods_region.add_locations(loc_doll_woods, CCCharlesLocation)
    multiworld.regions.append(doll_woods_region)

    lost_stairs_region = Region("Lost Stairs", player, multiworld)
    lost_stairs_region.add_locations(loc_lost_stairs, CCCharlesLocation)
    multiworld.regions.append(lost_stairs_region)

    east_house_region = Region("East House", player, multiworld)
    east_house_region.add_locations(loc_east_house, CCCharlesLocation)
    multiworld.regions.append(east_house_region)

    rockets_testing_ground_region = Region("Rockets Testing Ground", player, multiworld)
    rockets_testing_ground_region.add_locations(loc_rockets_testing_ground, CCCharlesLocation)
    multiworld.regions.append(rockets_testing_ground_region)

    rockets_testing_bunker_region = Region("Rockets Testing Bunker", player, multiworld)
    rockets_testing_bunker_region.add_locations(loc_rockets_testing_bunker, CCCharlesLocation)
    multiworld.regions.append(rockets_testing_bunker_region)

    workshop_region = Region("Workshop", player, multiworld)
    workshop_region.add_locations(loc_workshop, CCCharlesLocation)
    multiworld.regions.append(workshop_region)

    east_tower_region = Region("East Tower", player, multiworld)
    east_tower_region.add_locations(loc_east_tower, CCCharlesLocation)
    multiworld.regions.append(east_tower_region)

    lighthouse_region = Region("Lighthouse", player, multiworld)
    lighthouse_region.add_locations(loc_lighthouse, CCCharlesLocation)
    multiworld.regions.append(lighthouse_region)

    north_mine_outside_region = Region("North Mine Outside", player, multiworld)
    north_mine_outside_region.add_locations(loc_north_mine_outside, CCCharlesLocation)
    multiworld.regions.append(north_mine_outside_region)

    north_mine_inside_region = Region("North Mine Inside", player, multiworld)
    north_mine_inside_region.add_locations(loc_north_mine_inside, CCCharlesLocation)
    multiworld.regions.append(north_mine_inside_region)

    wood_bridge_region = Region("Wood Bridge", player, multiworld)
    wood_bridge_region.add_locations(loc_wood_bridge, CCCharlesLocation)
    multiworld.regions.append(wood_bridge_region)

    museum_region = Region("Museum", player, multiworld)
    museum_region.add_locations(loc_museum, CCCharlesLocation)
    multiworld.regions.append(museum_region)

    barbed_shelter_region = Region("Barbed Shelter", player, multiworld)
    barbed_shelter_region.add_locations(loc_barbed_shelter, CCCharlesLocation)
    multiworld.regions.append(barbed_shelter_region)

    west_beach_region = Region("West Beach", player, multiworld)
    west_beach_region.add_locations(loc_west_beach, CCCharlesLocation)
    multiworld.regions.append(west_beach_region)

    church_region = Region("Church", player, multiworld)
    church_region.add_locations(loc_church, CCCharlesLocation)
    multiworld.regions.append(church_region)

    west_cottage_region = Region("West Cottage", player, multiworld)
    west_cottage_region.add_locations(loc_west_cottage, CCCharlesLocation)
    multiworld.regions.append(west_cottage_region)

    caravan_region = Region("Caravan", player, multiworld)
    caravan_region.add_locations(loc_caravan, CCCharlesLocation)
    multiworld.regions.append(caravan_region)

    trailer_cabin_region = Region("Trailer Cabin", player, multiworld)
    trailer_cabin_region.add_locations(loc_trailer_cabin, CCCharlesLocation)
    multiworld.regions.append(trailer_cabin_region)

    towers_region = Region("Towers", player, multiworld)
    towers_region.add_locations(loc_towers, CCCharlesLocation)
    multiworld.regions.append(towers_region)

    north_beach_region = Region("North beach", player, multiworld)
    north_beach_region.add_locations(loc_north_beach, CCCharlesLocation)
    multiworld.regions.append(north_beach_region)

    mine_shaft_region = Region("Mine Shaft", player, multiworld)
    mine_shaft_region.add_locations(loc_mine_shaft, CCCharlesLocation)
    multiworld.regions.append(mine_shaft_region)

    mob_camp_region = Region("Mob Camp", player, multiworld)
    mob_camp_region.add_locations(loc_mob_camp, CCCharlesLocation)
    multiworld.regions.append(mob_camp_region)

    mob_camp_locked_room_region = Region("Mob Camp Locked Room", player, multiworld)
    mob_camp_locked_room_region.add_locations(loc_mob_camp_locked_room, CCCharlesLocation)
    multiworld.regions.append(mob_camp_locked_room_region)

    mine_elevator_exit_region = Region("Mine Elevator Exit", player, multiworld)
    mine_elevator_exit_region.add_locations(loc_mine_elevator_exit, CCCharlesLocation)
    multiworld.regions.append(mine_elevator_exit_region)

    mountain_ruin_outside_region = Region("Mountain Ruin Outside", player, multiworld)
    mountain_ruin_outside_region.add_locations(loc_mountain_ruin_outside, CCCharlesLocation)
    multiworld.regions.append(mountain_ruin_outside_region)

    mountain_ruin_inside_region = Region("Mountain Ruin Inside", player, multiworld)
    mountain_ruin_inside_region.add_locations(loc_mountain_ruin_inside, CCCharlesLocation)
    multiworld.regions.append(mountain_ruin_inside_region)

    prism_temple_region = Region("Prism Temple", player, multiworld)
    prism_temple_region.add_locations(loc_prism_temple, CCCharlesLocation)
    multiworld.regions.append(prism_temple_region)

    pickle_val_region = Region("Pickle Val", player, multiworld)
    pickle_val_region.add_locations(loc_pickle_val, CCCharlesLocation)
    multiworld.regions.append(pickle_val_region)

    shrine_near_temple_region = Region("Shrine Near Temple", player, multiworld)
    shrine_near_temple_region.add_locations(loc_shrine_near_temple, CCCharlesLocation)
    multiworld.regions.append(shrine_near_temple_region)

    morse_bunker_region = Region("Morse Bunker", player, multiworld)
    morse_bunker_region.add_locations(loc_morse_bunker, CCCharlesLocation)
    multiworld.regions.append(morse_bunker_region)

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
