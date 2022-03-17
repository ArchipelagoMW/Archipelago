import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import SA2BItem
from .Locations import SA2BLocation
from .Names import LocationName, ItemName


def create_regions(world, player: int, active_locations):

    menu_region = create_region(world, player, active_locations, 'Menu', None, None)
    
    city_escape_region_locations = [
        LocationName.city_escape_1,
        LocationName.city_escape_2,
        LocationName.city_escape_3,
        LocationName.city_escape_4,
        LocationName.city_escape_5,
        LocationName.city_escape_upgrade,
    ]
    city_escape_region = create_region(world, player, active_locations, LocationName.city_escape_region, city_escape_region_locations, None)
    
    metal_harbor_region_locations = [
        LocationName.metal_harbor_1,
        LocationName.metal_harbor_2,
        LocationName.metal_harbor_3,
        LocationName.metal_harbor_4,
        LocationName.metal_harbor_5,
        LocationName.metal_harbor_upgrade,
    ]
    metal_harbor_region = create_region(world, player, active_locations, LocationName.metal_harbor_region, metal_harbor_region_locations, None)
    
    green_jungle_region_locations = [
        LocationName.green_jungle_1,
        LocationName.green_jungle_2,
        LocationName.green_jungle_3,
        LocationName.green_jungle_4,
        LocationName.green_jungle_5,
        LocationName.green_jungle_upgrade,
    ]
    green_jungle_region = create_region(world, player, active_locations, LocationName.green_jungle_region, green_jungle_region_locations, None)
    
    pyramid_cave_region_locations = [
        LocationName.pyramid_cave_1,
        LocationName.pyramid_cave_2,
        LocationName.pyramid_cave_3,
        LocationName.pyramid_cave_4,
        LocationName.pyramid_cave_5,
        LocationName.pyramid_cave_upgrade,
    ]
    pyramid_cave_region = create_region(world, player, active_locations, LocationName.pyramid_cave_region, pyramid_cave_region_locations, None)

    crazy_gadget_region_locations = [
        LocationName.crazy_gadget_1,
        LocationName.crazy_gadget_2,
        LocationName.crazy_gadget_3,
        LocationName.crazy_gadget_4,
        LocationName.crazy_gadget_5,
        LocationName.crazy_gadget_upgrade,
    ]
    crazy_gadget_region = create_region(world, player, active_locations, LocationName.crazy_gadget_region, crazy_gadget_region_locations, None)

    final_rush_region_locations = [
        LocationName.final_rush_1,
        LocationName.final_rush_2,
        LocationName.final_rush_3,
        LocationName.final_rush_4,
        LocationName.final_rush_5,
        LocationName.final_rush_upgrade,
    ]
    final_rush_region = create_region(world, player, active_locations, LocationName.final_rush_region, final_rush_region_locations, None)

    prison_lane_region_locations = [
        LocationName.prison_lane_1,
        LocationName.prison_lane_2,
        LocationName.prison_lane_3,
        LocationName.prison_lane_4,
        LocationName.prison_lane_5,
        LocationName.prison_lane_upgrade,
    ]
    prison_lane_region = create_region(world, player, active_locations, LocationName.prison_lane_region, prison_lane_region_locations, None)

    mission_street_region_locations = [
        LocationName.mission_street_1,
        LocationName.mission_street_2,
        LocationName.mission_street_3,
        LocationName.mission_street_4,
        LocationName.mission_street_5,
        LocationName.mission_street_upgrade,
    ]
    mission_street_region = create_region(world, player, active_locations, LocationName.mission_street_region, mission_street_region_locations, None)

    route_101_region_locations = [
        LocationName.route_101_1,
        LocationName.route_101_2,
        LocationName.route_101_3,
        LocationName.route_101_4,
        LocationName.route_101_5,
    ]
    route_101_region = create_region(world, player, active_locations, LocationName.route_101_region, route_101_region_locations, None)

    hidden_base_region_locations = [
        LocationName.hidden_base_1,
        LocationName.hidden_base_2,
        LocationName.hidden_base_3,
        LocationName.hidden_base_4,
        LocationName.hidden_base_5,
        LocationName.hidden_base_upgrade,
    ]
    hidden_base_region = create_region(world, player, active_locations, LocationName.hidden_base_region, hidden_base_region_locations, None)

    eternal_engine_region_locations = [
        LocationName.eternal_engine_1,
        LocationName.eternal_engine_2,
        LocationName.eternal_engine_3,
        LocationName.eternal_engine_4,
        LocationName.eternal_engine_5,
        LocationName.eternal_engine_upgrade,
    ]
    eternal_engine_region = create_region(world, player, active_locations, LocationName.eternal_engine_region, eternal_engine_region_locations, None)

    wild_canyon_region_locations = [
        LocationName.wild_canyon_1,
        LocationName.wild_canyon_2,
        LocationName.wild_canyon_3,
        LocationName.wild_canyon_4,
        LocationName.wild_canyon_5,
        LocationName.wild_canyon_upgrade,
    ]
    wild_canyon_region = create_region(world, player, active_locations, LocationName.wild_canyon_region, wild_canyon_region_locations, None)

    pumpkin_hill_region_locations = [
        LocationName.pumpkin_hill_1,
        LocationName.pumpkin_hill_2,
        LocationName.pumpkin_hill_3,
        LocationName.pumpkin_hill_4,
        LocationName.pumpkin_hill_5,
        LocationName.pumpkin_hill_upgrade,
    ]
    pumpkin_hill_region = create_region(world, player, active_locations, LocationName.pumpkin_hill_region, pumpkin_hill_region_locations, None)

    aquatic_mine_region_locations = [
        LocationName.aquatic_mine_1,
        LocationName.aquatic_mine_2,
        LocationName.aquatic_mine_3,
        LocationName.aquatic_mine_4,
        LocationName.aquatic_mine_5,
        LocationName.aquatic_mine_upgrade,
    ]
    aquatic_mine_region = create_region(world, player, active_locations, LocationName.aquatic_mine_region, aquatic_mine_region_locations, None)

    death_chamber_region_locations = [
        LocationName.death_chamber_1,
        LocationName.death_chamber_2,
        LocationName.death_chamber_3,
        LocationName.death_chamber_4,
        LocationName.death_chamber_5,
        LocationName.death_chamber_upgrade,
    ]
    death_chamber_region = create_region(world, player, active_locations, LocationName.death_chamber_region, death_chamber_region_locations, None)

    meteor_herd_region_locations = [
        LocationName.meteor_herd_1,
        LocationName.meteor_herd_2,
        LocationName.meteor_herd_3,
        LocationName.meteor_herd_4,
        LocationName.meteor_herd_5,
        LocationName.meteor_herd_upgrade,
    ]
    meteor_herd_region = create_region(world, player, active_locations, LocationName.meteor_herd_region, meteor_herd_region_locations, None)

    radical_highway_region_locations = [
        LocationName.radical_highway_1,
        LocationName.radical_highway_2,
        LocationName.radical_highway_3,
        LocationName.radical_highway_4,
        LocationName.radical_highway_5,
        LocationName.radical_highway_upgrade,
    ]
    radical_highway_region = create_region(world, player, active_locations, LocationName.radical_highway_region, radical_highway_region_locations, None)

    white_jungle_region_locations = [
        LocationName.white_jungle_1,
        LocationName.white_jungle_2,
        LocationName.white_jungle_3,
        LocationName.white_jungle_4,
        LocationName.white_jungle_5,
        LocationName.white_jungle_upgrade,
    ]
    white_jungle_region = create_region(world, player, active_locations, LocationName.white_jungle_region, white_jungle_region_locations, None)

    sky_rail_region_locations = [
        LocationName.sky_rail_1,
        LocationName.sky_rail_2,
        LocationName.sky_rail_3,
        LocationName.sky_rail_4,
        LocationName.sky_rail_5,
        LocationName.sky_rail_upgrade,
    ]
    sky_rail_region = create_region(world, player, active_locations, LocationName.sky_rail_region, sky_rail_region_locations, None)

    final_chase_region_locations = [
        LocationName.final_chase_1,
        LocationName.final_chase_2,
        LocationName.final_chase_3,
        LocationName.final_chase_4,
        LocationName.final_chase_5,
        LocationName.final_chase_upgrade,
    ]
    final_chase_region = create_region(world, player, active_locations, LocationName.final_chase_region, final_chase_region_locations, None)

    iron_gate_region_locations = [
        LocationName.iron_gate_1,
        LocationName.iron_gate_2,
        LocationName.iron_gate_3,
        LocationName.iron_gate_4,
        LocationName.iron_gate_5,
        LocationName.iron_gate_upgrade,
    ]
    iron_gate_region = create_region(world, player, active_locations, LocationName.iron_gate_region, iron_gate_region_locations, None)

    sand_ocean_region_locations = [
        LocationName.sand_ocean_1,
        LocationName.sand_ocean_2,
        LocationName.sand_ocean_3,
        LocationName.sand_ocean_4,
        LocationName.sand_ocean_5,
        LocationName.sand_ocean_upgrade,
    ]
    sand_ocean_region = create_region(world, player, active_locations, LocationName.sand_ocean_region, sand_ocean_region_locations, None)

    lost_colony_region_locations = [
        LocationName.lost_colony_1,
        LocationName.lost_colony_2,
        LocationName.lost_colony_3,
        LocationName.lost_colony_4,
        LocationName.lost_colony_5,
        LocationName.lost_colony_upgrade,
    ]
    lost_colony_region = create_region(world, player, active_locations, LocationName.lost_colony_region, lost_colony_region_locations, None)

    weapons_bed_region_locations = [
        LocationName.weapons_bed_1,
        LocationName.weapons_bed_2,
        LocationName.weapons_bed_3,
        LocationName.weapons_bed_4,
        LocationName.weapons_bed_5,
        LocationName.weapons_bed_upgrade,
    ]
    weapons_bed_region = create_region(world, player, active_locations, LocationName.weapons_bed_region, weapons_bed_region_locations, None)

    cosmic_wall_region_locations = [
        LocationName.cosmic_wall_1,
        LocationName.cosmic_wall_2,
        LocationName.cosmic_wall_3,
        LocationName.cosmic_wall_4,
        LocationName.cosmic_wall_5,
        LocationName.cosmic_wall_upgrade,
    ]
    cosmic_wall_region = create_region(world, player, active_locations, LocationName.cosmic_wall_region, cosmic_wall_region_locations, None)

    dry_lagoon_region_locations = [
        LocationName.dry_lagoon_1,
        LocationName.dry_lagoon_2,
        LocationName.dry_lagoon_3,
        LocationName.dry_lagoon_4,
        LocationName.dry_lagoon_5,
        LocationName.dry_lagoon_upgrade,
    ]
    dry_lagoon_region = create_region(world, player, active_locations, LocationName.dry_lagoon_region, dry_lagoon_region_locations, None)

    egg_quarters_region_locations = [
        LocationName.egg_quarters_1,
        LocationName.egg_quarters_2,
        LocationName.egg_quarters_3,
        LocationName.egg_quarters_4,
        LocationName.egg_quarters_5,
        LocationName.egg_quarters_upgrade,
    ]
    egg_quarters_region = create_region(world, player, active_locations, LocationName.egg_quarters_region, egg_quarters_region_locations, None)

    security_hall_region_locations = [
        LocationName.security_hall_1,
        LocationName.security_hall_2,
        LocationName.security_hall_3,
        LocationName.security_hall_4,
        LocationName.security_hall_5,
        LocationName.security_hall_upgrade,
    ]
    security_hall_region = create_region(world, player, active_locations, LocationName.security_hall_region, security_hall_region_locations, None)

    route_280_region_locations = [
        LocationName.route_280_1,
        LocationName.route_280_2,
        LocationName.route_280_3,
        LocationName.route_280_4,
        LocationName.route_280_5,
    ]
    route_280_region = create_region(world, player, active_locations, LocationName.route_280_region, route_280_region_locations, None)

    mad_space_region_locations = [
        LocationName.mad_space_1,
        LocationName.mad_space_2,
        LocationName.mad_space_3,
        LocationName.mad_space_4,
        LocationName.mad_space_5,
        LocationName.mad_space_upgrade,
    ]
    mad_space_region = create_region(world, player, active_locations, LocationName.mad_space_region, mad_space_region_locations, None)

    cannon_core_region_locations = [
        LocationName.cannon_core_1,
        LocationName.cannon_core_2,
        LocationName.cannon_core_3,
        LocationName.cannon_core_4,
        LocationName.cannon_core_5,
    ]
    cannon_core_region = create_region(world, player, active_locations, LocationName.cannon_core_region, cannon_core_region_locations, None)

    chao_garden_region_locations = [
        LocationName.chao_beginner_race,
        LocationName.chao_jewel_race,
        LocationName.chao_challenge_race,
        LocationName.chao_hero_race,
        LocationName.chao_dark_race,
        LocationName.chao_beginner_karate,
        LocationName.chao_standard_karate,
        LocationName.chao_expert_karate,
        LocationName.chao_super_karate,
    ]
    chao_garden_region = create_region(world, player, active_locations, LocationName.chao_garden_region, chao_garden_region_locations, None)
    
    # Set up the regions correctly.
    world.regions = [
        menu_region,
        city_escape_region,
        metal_harbor_region,
        green_jungle_region,
        pyramid_cave_region,
        crazy_gadget_region,
        final_rush_region,
        prison_lane_region,
        mission_street_region,
        route_101_region,
        hidden_base_region,
        eternal_engine_region,
        wild_canyon_region,
        pumpkin_hill_region,
        aquatic_mine_region,
        death_chamber_region,
        meteor_herd_region,
        radical_highway_region,
        white_jungle_region,
        sky_rail_region,
        final_chase_region,
        iron_gate_region,
        sand_ocean_region,
        lost_colony_region,
        weapons_bed_region,
        cosmic_wall_region,
        dry_lagoon_region,
        egg_quarters_region,
        security_hall_region,
        route_280_region,
        mad_space_region,
        cannon_core_region,
        chao_garden_region,
    ]

    
    names: typing.Dict[str, int] = {}

    connect(world, player, names, 'Menu', LocationName.city_escape_region)
    connect(world, player, names, 'Menu', LocationName.metal_harbor_region)
    connect(world, player, names, 'Menu', LocationName.green_jungle_region)
    connect(world, player, names, 'Menu', LocationName.pyramid_cave_region)
    connect(world, player, names, 'Menu', LocationName.crazy_gadget_region)
    connect(world, player, names, 'Menu', LocationName.final_rush_region)
    connect(world, player, names, 'Menu', LocationName.prison_lane_region)
    connect(world, player, names, 'Menu', LocationName.mission_street_region)
    connect(world, player, names, 'Menu', LocationName.route_101_region)
    connect(world, player, names, 'Menu', LocationName.hidden_base_region)
    connect(world, player, names, 'Menu', LocationName.eternal_engine_region)
    connect(world, player, names, 'Menu', LocationName.wild_canyon_region)
    connect(world, player, names, 'Menu', LocationName.pumpkin_hill_region)
    connect(world, player, names, 'Menu', LocationName.aquatic_mine_region)
    connect(world, player, names, 'Menu', LocationName.death_chamber_region)
    connect(world, player, names, 'Menu', LocationName.meteor_herd_region)
    connect(world, player, names, 'Menu', LocationName.radical_highway_region)
    connect(world, player, names, 'Menu', LocationName.white_jungle_region)
    connect(world, player, names, 'Menu', LocationName.sky_rail_region)
    connect(world, player, names, 'Menu', LocationName.final_chase_region)
    connect(world, player, names, 'Menu', LocationName.iron_gate_region)
    connect(world, player, names, 'Menu', LocationName.sand_ocean_region)
    connect(world, player, names, 'Menu', LocationName.lost_colony_region)
    connect(world, player, names, 'Menu', LocationName.weapons_bed_region)
    connect(world, player, names, 'Menu', LocationName.cosmic_wall_region)
    connect(world, player, names, 'Menu', LocationName.dry_lagoon_region)
    connect(world, player, names, 'Menu', LocationName.egg_quarters_region)
    connect(world, player, names, 'Menu', LocationName.security_hall_region)
    connect(world, player, names, 'Menu', LocationName.route_280_region)
    connect(world, player, names, 'Menu', LocationName.mad_space_region)
    connect(world, player, names, 'Menu', LocationName.cannon_core_region)
    connect(world, player, names, 'Menu', LocationName.chao_garden_region)


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None, exits=None):
    # Shamelessly stolen from the ROR2 definition, lol
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id:
                location = SA2BLocation(player, location, loc_id, ret)
                ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


def connect(world: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str, rule: typing.Optional[typing.Callable] = None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, sourceRegion)

    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)