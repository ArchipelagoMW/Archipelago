from BaseClasses import MultiWorld, Region, ItemClassification
from . import CCCharlesItem
from .Options import CCCharlesOptions
from .Locations import CCCharlesLocation, loc_start_camp, loc_tony_tiddle_mission, loc_tutorial_candice_mission, \
    loc_swamp, loc_lizbeth_murkwater_mission, loc_daryl_mission, loc_south_house, loc_helen_mission, \
    loc_sgt_flint_mission, loc_south_mine_outside, loc_south_mine_inside, loc_theodore_mission, loc_canyon_theodore, \
    loc_watchtower, loc_boulder_field, loc_house_sasha_mission, loc_house_santiago, loc_port_santiago_mission, \
    loc_trench_house, loc_doll_woods, loc_lost_stairs, loc_east_house, loc_explosive_training, \
    loc_john_smith_mission, loc_greg_mission, loc_claire_mission, loc_north_mine_outside, loc_north_mine_inside, \
    loc_wood_bridge, loc_paul_mission, loc_gertrude_mission, loc_west_beach, loc_church, loc_refuge_gale_mission, \
    loc_caravan, loc_trailer_house, loc_ronny_mission, loc_north_beach, loc_mine_shaft, loc_mob_camp, \
    loc_mine_elevator_exit, loc_mountain_ruin_outside, loc_mountain_ruin_inside, loc_prism_temple, \
    loc_field_pickle_lady_mission, loc_shrine_near_temple, loc_morse_bunker


class CCCharlesRegion(Region):
    regions = []

def create_regions(world: MultiWorld, options: CCCharlesOptions, player: int):
    menu_region = Region("Menu", player, world, "Eugene's Boat")
    world.regions.append(menu_region)

    start_camp_region = Region("Start Camp", player, world)
    start_camp_region.add_locations(loc_start_camp, CCCharlesLocation)
    world.regions.append(start_camp_region)

    tony_tiddle_barn_region = Region("Tony Tiddle Barn", player, world)
    tony_tiddle_barn_region.add_locations(loc_tony_tiddle_mission, CCCharlesLocation)
    world.regions.append(tony_tiddle_barn_region)

    candice_house_region = Region("Candice House", player, world)
    candice_house_region.add_locations(loc_tutorial_candice_mission, CCCharlesLocation)
    world.regions.append(candice_house_region)

    swamp_region = Region("Swamp", player, world)
    swamp_region.add_locations(loc_swamp, CCCharlesLocation)
    world.regions.append(swamp_region)

    shack_region = Region("Shack", player, world)
    shack_region.add_locations(loc_lizbeth_murkwater_mission, CCCharlesLocation)
    world.regions.append(shack_region)

    junkyard_region = Region("Junkyard", player, world)
    junkyard_region.add_locations(loc_daryl_mission, CCCharlesLocation)
    world.regions.append(junkyard_region)

    dianne_house_region = Region("Dianne House", player, world)
    dianne_house_region.add_locations(loc_south_house, CCCharlesLocation)
    world.regions.append(dianne_house_region)

    helen_house_region = Region("Helen House", player, world)
    helen_house_region.add_locations(loc_helen_mission, CCCharlesLocation)
    world.regions.append(helen_house_region)

    military_base_region = Region("Military Base", player, world)
    military_base_region.add_locations(loc_sgt_flint_mission, CCCharlesLocation)
    world.regions.append(military_base_region)

    outside_south_mine_region = Region("Outside South Mine", player, world)
    outside_south_mine_region.add_locations(loc_south_mine_outside, CCCharlesLocation)
    world.regions.append(outside_south_mine_region)

    inside_south_mine_region = Region("Inside South Mine", player, world)
    inside_south_mine_region.add_locations(loc_south_mine_inside, CCCharlesLocation)
    world.regions.append(inside_south_mine_region)

    theodore_station_region = Region("Theodore Station", player, world)
    theodore_station_region.add_locations(loc_theodore_mission, CCCharlesLocation)
    world.regions.append(theodore_station_region)

    theodore_canyon_region = Region("Theodore Canyon", player, world)
    theodore_canyon_region.add_locations(loc_canyon_theodore, CCCharlesLocation)
    world.regions.append(theodore_canyon_region)

    watchtower_region = Region("Watchtower", player, world)
    watchtower_region.add_locations(loc_watchtower, CCCharlesLocation)
    world.regions.append(watchtower_region)

    ghost_boulder_field_region = Region("Ghost Boulder Field", player, world)
    ghost_boulder_field_region.add_locations(loc_boulder_field, CCCharlesLocation)
    world.regions.append(ghost_boulder_field_region)

    sasha_house_region = Region("Sasha House", player, world)
    sasha_house_region.add_locations(loc_house_sasha_mission, CCCharlesLocation)
    world.regions.append(sasha_house_region)

    santiago_house_region = Region("Santiago House", player, world)
    santiago_house_region.add_locations(loc_house_santiago, CCCharlesLocation)
    world.regions.append(santiago_house_region)

    santiago_port_region = Region("Santiago Port", player, world)
    santiago_port_region.add_locations(loc_port_santiago_mission, CCCharlesLocation)
    world.regions.append(santiago_port_region)

    trench_house_region = Region("Trench House", player, world)
    trench_house_region.add_locations(loc_trench_house, CCCharlesLocation)
    world.regions.append(trench_house_region)

    doll_woods_region = Region("Doll Woods", player, world)
    doll_woods_region.add_locations(loc_doll_woods, CCCharlesLocation)
    world.regions.append(doll_woods_region)

    forest_lost_stairs_region = Region("Forest Lost Stairs", player, world)
    forest_lost_stairs_region.add_locations(loc_lost_stairs, CCCharlesLocation)
    world.regions.append(forest_lost_stairs_region)

    far_east_house_region = Region("Far East House", player, world)
    far_east_house_region.add_locations(loc_east_house, CCCharlesLocation)
    world.regions.append(far_east_house_region)

    explosive_training_region = Region("Explosive Training", player, world)
    explosive_training_region.add_locations(loc_explosive_training, CCCharlesLocation)
    world.regions.append(explosive_training_region)

    john_smith_workshop_region = Region("John Smith Workshop", player, world)
    john_smith_workshop_region.add_locations(loc_john_smith_mission, CCCharlesLocation)
    world.regions.append(john_smith_workshop_region)

    greg_tower_region = Region("Greg Tower", player, world)
    greg_tower_region.add_locations(loc_greg_mission, CCCharlesLocation)
    world.regions.append(greg_tower_region)

    lighthouse_region = Region("Lighthouse", player, world)
    lighthouse_region.add_locations(loc_claire_mission, CCCharlesLocation)
    world.regions.append(lighthouse_region)

    outside_north_mine_region = Region("Outside North Mine", player, world)
    outside_north_mine_region.add_locations(loc_north_mine_outside, CCCharlesLocation)
    world.regions.append(outside_north_mine_region)

    inside_north_mine_region = Region("Inside North Mine", player, world)
    inside_north_mine_region.add_locations(loc_north_mine_inside, CCCharlesLocation)
    world.regions.append(inside_north_mine_region)

    wood_bridge_region = Region("Wood Bridge", player, world)
    wood_bridge_region.add_locations(loc_wood_bridge, CCCharlesLocation)
    world.regions.append(wood_bridge_region)

    paul_museum_region = Region("Paul Museum", player, world)
    paul_museum_region.add_locations(loc_paul_mission, CCCharlesLocation)
    world.regions.append(paul_museum_region)

    gertrude_base_region = Region("Gertrude Base", player, world)
    gertrude_base_region.add_locations(loc_gertrude_mission, CCCharlesLocation)
    world.regions.append(gertrude_base_region)

    beach_region = Region("Beach", player, world)
    beach_region.add_locations(loc_west_beach, CCCharlesLocation)
    world.regions.append(beach_region)

    church_region = Region("Church", player, world)
    church_region.add_locations(loc_church, CCCharlesLocation)
    world.regions.append(church_region)

    gale_house_region = Region("Gale House", player, world)
    gale_house_region.add_locations(loc_refuge_gale_mission, CCCharlesLocation)
    world.regions.append(gale_house_region)

    caravan_region = Region("Caravan", player, world)
    caravan_region.add_locations(loc_caravan, CCCharlesLocation)
    world.regions.append(caravan_region)

    abandoned_house_region = Region("Abandoned House", player, world)
    abandoned_house_region.add_locations(loc_trailer_house, CCCharlesLocation)
    world.regions.append(abandoned_house_region)

    ronny_towers_region = Region("Ronny Towers", player, world)
    ronny_towers_region.add_locations(loc_ronny_mission, CCCharlesLocation)
    world.regions.append(ronny_towers_region)

    north_frank_fisher_region = Region("North Frank Fisher", player, world)
    north_frank_fisher_region.add_locations(loc_north_beach, CCCharlesLocation)
    world.regions.append(north_frank_fisher_region)

    hidden_hole_region = Region("Hidden Hole", player, world)
    hidden_hole_region.add_locations(loc_mine_shaft, CCCharlesLocation)
    world.regions.append(hidden_hole_region)

    mob_camp_region = Region("Mob Camp", player, world)
    mob_camp_region.add_locations(loc_mob_camp, CCCharlesLocation)
    world.regions.append(mob_camp_region)

    mine_elevator_exit_region = Region("Mine Elevator Exit", player, world)
    mine_elevator_exit_region.add_locations(loc_mine_elevator_exit, CCCharlesLocation)
    world.regions.append(mine_elevator_exit_region)

    outside_mountain_ruin_region = Region("Outside Mountain Ruin", player, world)
    outside_mountain_ruin_region.add_locations(loc_mountain_ruin_outside, CCCharlesLocation)
    world.regions.append(outside_mountain_ruin_region)

    inside_mountain_ruin_region = Region("Inside Mountain Ruin", player, world)
    inside_mountain_ruin_region.add_locations(loc_mountain_ruin_inside, CCCharlesLocation)
    world.regions.append(inside_mountain_ruin_region)

    prism_temple_region = Region("Prism Temple", player, world)
    prism_temple_region.add_locations(loc_prism_temple, CCCharlesLocation)
    world.regions.append(prism_temple_region)

    pickle_lady_house_region = Region("Pickle Lady House", player, world)
    pickle_lady_house_region.add_locations(loc_field_pickle_lady_mission, CCCharlesLocation)
    world.regions.append(pickle_lady_house_region)

    shrine_near_temple_region = Region("Temple Shrine", player, world)
    shrine_near_temple_region.add_locations(loc_shrine_near_temple, CCCharlesLocation)
    world.regions.append(shrine_near_temple_region)

    morse_refuge_region = Region("Morse Refuge", player, world)
    morse_refuge_region.add_locations(loc_morse_bunker, CCCharlesLocation)
    world.regions.append(morse_refuge_region)

    # Include Victory event
    loc_final_boss = CCCharlesLocation(player, "Final Boss", None, menu_region)
    loc_final_boss.place_locked_item(CCCharlesItem("Victory", ItemClassification.progression, None, player))

    menu_region.locations.append(loc_final_boss)

    menu_region.connect(start_camp_region)
    menu_region.connect(tony_tiddle_barn_region)
    menu_region.connect(candice_house_region)
    menu_region.connect(swamp_region)
    menu_region.connect(shack_region)
    menu_region.connect(junkyard_region)
    menu_region.connect(dianne_house_region)
    menu_region.connect(helen_house_region)
    menu_region.connect(military_base_region)
    menu_region.connect(outside_south_mine_region)
    menu_region.connect(inside_south_mine_region)
    menu_region.connect(theodore_station_region)
    menu_region.connect(theodore_canyon_region)
    menu_region.connect(watchtower_region)
    menu_region.connect(ghost_boulder_field_region)
    menu_region.connect(sasha_house_region)
    menu_region.connect(santiago_house_region)
    menu_region.connect(santiago_port_region)
    menu_region.connect(trench_house_region)
    menu_region.connect(doll_woods_region)
    menu_region.connect(forest_lost_stairs_region)
    menu_region.connect(far_east_house_region)
    menu_region.connect(explosive_training_region)
    menu_region.connect(john_smith_workshop_region)
    menu_region.connect(greg_tower_region)
    menu_region.connect(lighthouse_region)
    menu_region.connect(outside_north_mine_region)
    menu_region.connect(inside_north_mine_region)
    menu_region.connect(wood_bridge_region)
    menu_region.connect(paul_museum_region)
    menu_region.connect(gertrude_base_region)
    menu_region.connect(beach_region)
    menu_region.connect(church_region)
    menu_region.connect(gale_house_region)
    menu_region.connect(caravan_region)
    menu_region.connect(abandoned_house_region)
    menu_region.connect(ronny_towers_region)
    menu_region.connect(north_frank_fisher_region)
    menu_region.connect(hidden_hole_region)
    menu_region.connect(mob_camp_region)
    menu_region.connect(mine_elevator_exit_region)
    menu_region.connect(outside_mountain_ruin_region)
    menu_region.connect(inside_mountain_ruin_region)
    menu_region.connect(prism_temple_region)
    menu_region.connect(pickle_lady_house_region)
    menu_region.connect(shrine_near_temple_region)
    menu_region.connect(morse_refuge_region)
