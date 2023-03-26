import typing

from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from .Locations import boss_gate_set
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule, set_rule, CollectionRule
from .GateBosses import boss_has_requirement
from .Missions import stage_name_prefixes, mission_orders


def add_rule_safe(multiworld: MultiWorld, spot_name: str, player: int, rule: CollectionRule):
    try:
        location = multiworld.get_location(spot_name, player)
    except KeyError:
        # Do nothing for mission locations that do not exist
        pass
    else:
        add_rule(location, rule)


def set_mission_progress_rules(world: MultiWorld, player: int, mission_map: typing.Dict[int, int], mission_count_map: typing.Dict[int, int]):
    for i in range(31):
        mission_count = mission_count_map[i]
        mission_order: typing.List[int] = mission_orders[mission_map[i]]
        stage_prefix: str = stage_name_prefixes[i]

        for j in range(mission_count):
            if j == 0:
                continue

            mission_number = mission_order[j]
            prev_mission_number = mission_order[j - 1]
            location_name: str = stage_prefix + str(mission_number)
            prev_location_name: str = stage_prefix + str(prev_mission_number)
            set_rule(world.get_location(location_name, player),
                     lambda state, prev_location_name=prev_location_name: state.can_reach(prev_location_name, "Location", player))


def set_mission_upgrade_rules_standard(world: MultiWorld, player: int):
    # Mission 1 Upgrade Requirements
    add_rule_safe(world, LocationName.metal_harbor_1, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player))
    add_rule_safe(world, LocationName.pumpkin_hill_1, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.mission_street_1, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.aquatic_mine_1, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.hidden_base_1, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.pyramid_cave_1, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
    add_rule_safe(world, LocationName.death_chamber_1, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.eternal_engine_1, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))
    add_rule_safe(world, LocationName.meteor_herd_1, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.crazy_gadget_1, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_flame_ring, player))
    add_rule_safe(world, LocationName.final_rush_1, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule_safe(world, LocationName.egg_quarters_1, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule_safe(world, LocationName.lost_colony_1, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.weapons_bed_1, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.security_hall_1, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule_safe(world, LocationName.white_jungle_1, player,
                  lambda state: state.has(ItemName.shadow_air_shoes, player))
    add_rule_safe(world, LocationName.mad_space_1, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player) and
                                state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.cosmic_wall_1, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_1, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player) and
                                state.has(ItemName.knuckles_air_necklace, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player))

    # Mission 2 Upgrade Requirements
    add_rule_safe(world, LocationName.metal_harbor_2, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player))
    add_rule_safe(world, LocationName.mission_street_2, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.hidden_base_2, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.death_chamber_2, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.eternal_engine_2, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))
    add_rule_safe(world, LocationName.crazy_gadget_2, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule_safe(world, LocationName.lost_colony_2, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.weapons_bed_2, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.security_hall_2, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule_safe(world, LocationName.mad_space_2, player,
                  lambda state: state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.cosmic_wall_2, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_2, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.eggman_jet_engine, player))

    # Mission 3 Upgrade Requirements
    add_rule_safe(world, LocationName.city_escape_3, player,
                  lambda state: state.has(ItemName.sonic_mystic_melody, player))
    add_rule_safe(world, LocationName.wild_canyon_3, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player) and
                                state.has(ItemName.knuckles_mystic_melody, player))
    add_rule_safe(world, LocationName.prison_lane_3, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_mystic_melody, player))
    add_rule_safe(world, LocationName.metal_harbor_3, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_mystic_melody, player))
    add_rule_safe(world, LocationName.green_forest_3, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_mystic_melody, player))
    add_rule_safe(world, LocationName.pumpkin_hill_3, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player))
    add_rule_safe(world, LocationName.mission_street_3, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_mystic_melody, player))
    add_rule_safe(world, LocationName.aquatic_mine_3, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player))
    add_rule_safe(world, LocationName.hidden_base_3, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_mystic_melody, player))
    add_rule_safe(world, LocationName.pyramid_cave_3, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_mystic_melody, player))
    add_rule_safe(world, LocationName.death_chamber_3, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player) and
                                state.has(ItemName.knuckles_air_necklace, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.eternal_engine_3, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_mystic_melody, player))
    add_rule_safe(world, LocationName.meteor_herd_3, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player))
    add_rule_safe(world, LocationName.crazy_gadget_3, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_flame_ring, player) and
                                state.has(ItemName.sonic_mystic_melody, player))
    add_rule_safe(world, LocationName.final_rush_3, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_mystic_melody, player))

    add_rule_safe(world, LocationName.iron_gate_3, player,
                  lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                                state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.dry_lagoon_3, player,
                  lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                                state.has(ItemName.rouge_pick_nails, player) and
                                state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.sand_ocean_3, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.radical_highway_3, player,
                  lambda state: state.has(ItemName.shadow_mystic_melody, player))
    add_rule_safe(world, LocationName.egg_quarters_3, player,
                  lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                                state.has(ItemName.rouge_pick_nails, player) and
                                state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.lost_colony_3, player,
                  lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                                state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.weapons_bed_3, player,
                  lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                                state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.security_hall_3, player,
                  lambda state: state.has(ItemName.rouge_treasure_scope, player))
    add_rule_safe(world, LocationName.white_jungle_3, player,
                  lambda state: state.has(ItemName.shadow_air_shoes, player) and
                                state.has(ItemName.shadow_mystic_melody, player))
    add_rule_safe(world, LocationName.sky_rail_3, player,
                  lambda state: state.has(ItemName.shadow_air_shoes, player) and
                                state.has(ItemName.shadow_mystic_melody, player))
    add_rule_safe(world, LocationName.mad_space_3, player,
                  lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                                state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.cosmic_wall_3, player,
                  lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                                state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.final_chase_3, player,
                  lambda state: state.has(ItemName.shadow_air_shoes, player) and
                                state.has(ItemName.shadow_mystic_melody, player))

    add_rule_safe(world, LocationName.cannon_core_3, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.eggman_mystic_melody, player) and
                                state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player) and
                                state.has(ItemName.rouge_mystic_melody, player) and
                                state.has(ItemName.knuckles_mystic_melody, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player) and
                                state.has(ItemName.knuckles_air_necklace, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_light_shoes, player))

    # Mission 4 Upgrade Requirements
    add_rule_safe(world, LocationName.metal_harbor_4, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player))
    add_rule_safe(world, LocationName.pumpkin_hill_4, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.mission_street_4, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.aquatic_mine_4, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.hidden_base_4, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.pyramid_cave_4, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
    add_rule_safe(world, LocationName.death_chamber_4, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.eternal_engine_4, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))
    add_rule_safe(world, LocationName.meteor_herd_4, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.crazy_gadget_4, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_flame_ring, player))
    add_rule_safe(world, LocationName.final_rush_4, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule_safe(world, LocationName.egg_quarters_4, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule_safe(world, LocationName.lost_colony_4, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.weapons_bed_4, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.security_hall_4, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule_safe(world, LocationName.white_jungle_4, player,
                  lambda state: state.has(ItemName.shadow_air_shoes, player))
    add_rule_safe(world, LocationName.mad_space_4, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player) and
                                state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.cosmic_wall_4, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_4, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player) and
                                state.has(ItemName.knuckles_air_necklace, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player))

    # Mission 5 Upgrade Requirements
    add_rule_safe(world, LocationName.city_escape_5, player,
                  lambda state: state.has(ItemName.sonic_flame_ring, player) and
                                state.has(ItemName.sonic_light_shoes, player))
    add_rule_safe(world, LocationName.wild_canyon_5, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_sunglasses, player))
    add_rule_safe(world, LocationName.metal_harbor_5, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player))
    add_rule_safe(world, LocationName.green_forest_5, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
    add_rule_safe(world, LocationName.pumpkin_hill_5, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_sunglasses, player))
    add_rule_safe(world, LocationName.mission_street_5, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))
    add_rule_safe(world, LocationName.aquatic_mine_5, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player) and
                                state.has(ItemName.knuckles_air_necklace, player) and
                                state.has(ItemName.knuckles_sunglasses, player))
    add_rule_safe(world, LocationName.hidden_base_5, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.pyramid_cave_5, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
    add_rule_safe(world, LocationName.death_chamber_5, player,
                  lambda state: state.has(ItemName.knuckles_hammer_gloves, player) and
                                state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_mystic_melody, player) and
                                state.has(ItemName.knuckles_air_necklace, player))
    add_rule_safe(world, LocationName.eternal_engine_5, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))
    add_rule_safe(world, LocationName.meteor_herd_5, player,
                  lambda state: state.has(ItemName.knuckles_sunglasses, player))
    add_rule_safe(world, LocationName.crazy_gadget_5, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_flame_ring, player))
    add_rule_safe(world, LocationName.final_rush_5, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule_safe(world, LocationName.iron_gate_5, player,
                  lambda state: state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.dry_lagoon_5, player,
                  lambda state: state.has(ItemName.rouge_treasure_scope, player))
    add_rule_safe(world, LocationName.sand_ocean_5, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.egg_quarters_5, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player) and
                                state.has(ItemName.rouge_treasure_scope, player))
    add_rule_safe(world, LocationName.lost_colony_5, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.weapons_bed_5, player,
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.security_hall_5, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player) and
                                state.has(ItemName.rouge_treasure_scope, player) and
                                state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.white_jungle_5, player,
                  lambda state: state.has(ItemName.shadow_air_shoes, player) and
                                state.has(ItemName.shadow_flame_ring, player))
    add_rule_safe(world, LocationName.mad_space_5, player,
                  lambda state: state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.cosmic_wall_5, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_5, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.knuckles_mystic_melody, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player) and
                                state.has(ItemName.knuckles_air_necklace, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player))

    # Upgrade Spot Upgrade Requirements
    add_rule(world.get_location(LocationName.city_escape_upgrade, player),
             lambda state: state.has(ItemName.sonic_bounce_bracelet, player) and
                           state.has(ItemName.sonic_flame_ring, player))
    add_rule(world.get_location(LocationName.wild_canyon_upgrade, player),
             lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule(world.get_location(LocationName.prison_lane_upgrade, player),
             lambda state: state.has(ItemName.tails_bazooka, player))
    add_rule(world.get_location(LocationName.hidden_base_upgrade, player),
             lambda state: state.has(ItemName.tails_booster, player) and
                           state.has(ItemName.tails_bazooka, player))
    add_rule(world.get_location(LocationName.eternal_engine_upgrade, player),
             lambda state: state.has(ItemName.tails_booster, player))
    add_rule(world.get_location(LocationName.meteor_herd_upgrade, player),
             lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule(world.get_location(LocationName.crazy_gadget_upgrade, player),
             lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
    add_rule(world.get_location(LocationName.final_rush_upgrade, player),
             lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule(world.get_location(LocationName.iron_gate_upgrade, player),
             lambda state: state.has(ItemName.eggman_large_cannon, player))
    add_rule(world.get_location(LocationName.dry_lagoon_upgrade, player),
             lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule(world.get_location(LocationName.sand_ocean_upgrade, player),
             lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule(world.get_location(LocationName.radical_highway_upgrade, player),
             lambda state: state.has(ItemName.shadow_air_shoes, player))
    add_rule(world.get_location(LocationName.security_hall_upgrade, player),
             lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                           state.has(ItemName.rouge_iron_boots, player))
    add_rule(world.get_location(LocationName.cosmic_wall_upgrade, player),
             lambda state: state.has(ItemName.eggman_jet_engine, player))

    # Chao Key Upgrade Requirements
    if world.keysanity[player]:
        add_rule(world.get_location(LocationName.prison_lane_chao_1, player),
                 lambda state: state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.mission_street_chao_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_chao_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_chao_1, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_chao_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_chao_1, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.cosmic_wall_chao_1, player),
                 lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_chao_1, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))

        add_rule(world.get_location(LocationName.prison_lane_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.metal_harbor_chao_2, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.mission_street_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_chao_2, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.death_chamber_chao_2, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_chao_2, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.weapons_bed_chao_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.white_jungle_chao_2, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.mad_space_chao_2, player),
                 lambda state: state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.cosmic_wall_chao_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.metal_harbor_chao_3, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.mission_street_chao_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_chao_3, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_mystic_melody, player))
        add_rule(world.get_location(LocationName.death_chamber_chao_3, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_chao_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_chao_3, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_flame_ring, player))
        add_rule(world.get_location(LocationName.final_rush_chao_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.egg_quarters_chao_3, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player))
        add_rule(world.get_location(LocationName.lost_colony_chao_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.weapons_bed_chao_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.security_hall_chao_3, player),
                 lambda state: state.has(ItemName.rouge_pick_nails, player))
        add_rule(world.get_location(LocationName.white_jungle_chao_3, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.mad_space_chao_3, player),
                 lambda state: state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.cosmic_wall_chao_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_chao_3, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_air_necklace, player) and
                               state.has(ItemName.sonic_flame_ring, player))

    # Pipe Upgrade Requirements
    if world.whistlesanity[player].value == 1 or world.whistlesanity[player].value == 3:
        add_rule(world.get_location(LocationName.mission_street_pipe_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_pipe_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.sand_ocean_pipe_1, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_1, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.mission_street_pipe_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_pipe_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_pipe_2, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_pipe_2, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.sand_ocean_pipe_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.lost_colony_pipe_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_pipe_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.prison_lane_pipe_3, player),
                 lambda state: state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.mission_street_pipe_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_pipe_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_pipe_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.death_chamber_pipe_3, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_pipe_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_mystic_melody, player))

        add_rule(world.get_location(LocationName.weapons_bed_pipe_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.white_jungle_pipe_3, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.mad_space_pipe_3, player),
                 lambda state: state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_pipe_3, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.hidden_base_pipe_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_pipe_4, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_4, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_pipe_4, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_flame_ring, player))

        add_rule(world.get_location(LocationName.weapons_bed_pipe_4, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.white_jungle_pipe_4, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.mad_space_pipe_4, player),
                 lambda state: state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_4, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_pipe_4, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.hidden_base_pipe_5, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_5, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))

        add_rule(world.get_location(LocationName.weapons_bed_pipe_5, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_5, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_pipe_5, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_air_necklace, player))

    # Hidden Whistle Upgrade Requirements
    if world.whistlesanity[player].value == 2 or world.whistlesanity[player].value == 3:
        add_rule(world.get_location(LocationName.mission_street_hidden_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.mission_street_hidden_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_hidden_1, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.death_chamber_hidden_2, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.crazy_gadget_hidden_1, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.white_jungle_hidden_3, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.cannon_core_hidden_1, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player))

    # Omochao Upgrade Requirements
    if world.omosanity[player]:
        add_rule(world.get_location(LocationName.eternal_engine_omo_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.hidden_base_omo_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_omo_2, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_2, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.radical_highway_omo_2, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.weapons_bed_omo_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.mission_street_omo_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_omo_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_omo_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.final_rush_omo_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.weapons_bed_omo_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))

        add_rule(world.get_location(LocationName.metal_harbor_omo_4, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.mission_street_omo_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_omo_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_omo_4, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_4, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.mad_space_omo_4, player),
                 lambda state: state.has(ItemName.rouge_iron_boots, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.metal_harbor_omo_5, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.mission_street_omo_5, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_5, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_5, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_5, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.white_jungle_omo_5, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.mad_space_omo_5, player),
                 lambda state: state.has(ItemName.rouge_iron_boots, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_5, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.mission_street_omo_6, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_6, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_6, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_6, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.lost_colony_omo_6, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_6, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.mission_street_omo_7, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_7, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_7, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_7, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.lost_colony_omo_7, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_7, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_air_necklace, player))

        add_rule(world.get_location(LocationName.mission_street_omo_8, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_8, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_8, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_8, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.lost_colony_omo_8, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.security_hall_omo_8, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                               state.has(ItemName.rouge_iron_boots, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_8, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_air_necklace, player))

        add_rule(world.get_location(LocationName.death_chamber_omo_9, player),
                 lambda state: state.has(ItemName.knuckles_mystic_melody, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_9, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_9, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_9, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_air_necklace, player))

        add_rule(world.get_location(LocationName.eternal_engine_omo_10, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_10, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.eternal_engine_omo_11, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_11, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.eternal_engine_omo_12, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_12, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_flame_ring, player))

        add_rule(world.get_location(LocationName.crazy_gadget_omo_13, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_flame_ring, player))

    # Gold Beetle Upgrade Requirements
    if world.beetlesanity[player]:
        add_rule(world.get_location(LocationName.mission_street_beetle, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_beetle, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_beetle, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.death_chamber_beetle, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_beetle, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_beetle, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_flame_ring, player))

        add_rule(world.get_location(LocationName.dry_lagoon_beetle, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                               state.has(ItemName.rouge_pick_nails, player) and
                               state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.lost_colony_beetle, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.white_jungle_beetle, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.mad_space_beetle, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                               state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.cosmic_wall_beetle, player),
                 lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_beetle, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_air_necklace, player))

def set_mission_upgrade_rules_hard(world: MultiWorld, player: int):
    # Mission 1 Upgrade Requirements
    add_rule_safe(world, LocationName.pumpkin_hill_1, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.mission_street_1, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.hidden_base_1, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.death_chamber_1, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.eternal_engine_1, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))
    add_rule_safe(world, LocationName.crazy_gadget_1, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_flame_ring, player))
    add_rule_safe(world, LocationName.final_rush_1, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule_safe(world, LocationName.egg_quarters_1, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule_safe(world, LocationName.lost_colony_1, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.weapons_bed_1, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.cosmic_wall_1, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_1, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))

    # Mission 2 Upgrade Requirements
    add_rule_safe(world, LocationName.mission_street_2, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.hidden_base_2, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.death_chamber_2, player,
                  lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.eternal_engine_2, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))

    add_rule_safe(world, LocationName.lost_colony_2, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.weapons_bed_2, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.cosmic_wall_2, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_2, player,
                  lambda state: state.has(ItemName.tails_booster, player))

    # Mission 3 Upgrade Requirements
    add_rule_safe(world, LocationName.wild_canyon_3, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.prison_lane_3, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.mission_street_3, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.aquatic_mine_3, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player))
    add_rule_safe(world, LocationName.hidden_base_3, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_mystic_melody, player))
    add_rule_safe(world, LocationName.death_chamber_3, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.eternal_engine_3, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.meteor_herd_3, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player))
    add_rule_safe(world, LocationName.crazy_gadget_3, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_flame_ring, player))
    add_rule_safe(world, LocationName.final_rush_3, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule_safe(world, LocationName.iron_gate_3, player,
                  lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                                state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.dry_lagoon_3, player,
                  lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                                state.has(ItemName.rouge_pick_nails, player) and
                                state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.sand_ocean_3, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.egg_quarters_3, player,
                  lambda state: state.has(ItemName.rouge_mystic_melody, player))
    add_rule_safe(world, LocationName.lost_colony_3, player,
                  lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                                state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.weapons_bed_3, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.mad_space_3, player,
                  lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                                state.has(ItemName.rouge_iron_boots, player))
    add_rule_safe(world, LocationName.cosmic_wall_3, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_3, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))

    # Mission 4 Upgrade Requirements
    add_rule_safe(world, LocationName.pumpkin_hill_4, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.mission_street_4, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.hidden_base_4, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.death_chamber_4, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule_safe(world, LocationName.eternal_engine_4, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))
    add_rule_safe(world, LocationName.crazy_gadget_4, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_flame_ring, player))
    add_rule_safe(world, LocationName.final_rush_4, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule_safe(world, LocationName.egg_quarters_4, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule_safe(world, LocationName.lost_colony_4, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.weapons_bed_4, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.cosmic_wall_4, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_4, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))

    # Mission 5 Upgrade Requirements
    add_rule_safe(world, LocationName.city_escape_5, player,
                  lambda state: state.has(ItemName.sonic_flame_ring, player))
    add_rule_safe(world, LocationName.wild_canyon_5, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.pumpkin_hill_5, player,
                  lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule_safe(world, LocationName.mission_street_5, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.aquatic_mine_5, player,
                  lambda state: state.has(ItemName.knuckles_mystic_melody, player))
    add_rule_safe(world, LocationName.hidden_base_5, player,
                  lambda state: state.has(ItemName.tails_booster, player))
    add_rule_safe(world, LocationName.death_chamber_5, player,
                  lambda state: state.has(ItemName.knuckles_hammer_gloves, player) and
                                state.has(ItemName.knuckles_shovel_claws, player) and
                                state.has(ItemName.knuckles_mystic_melody, player))
    add_rule_safe(world, LocationName.eternal_engine_5, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.tails_bazooka, player))
    add_rule_safe(world, LocationName.crazy_gadget_5, player,
                  lambda state: state.has(ItemName.sonic_light_shoes, player) and
                                state.has(ItemName.sonic_bounce_bracelet, player) and
                                state.has(ItemName.sonic_flame_ring, player))
    add_rule_safe(world, LocationName.final_rush_5, player,
                  lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule_safe(world, LocationName.iron_gate_5, player,
                  lambda state: state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.dry_lagoon_5, player,
                  lambda state: state.has(ItemName.rouge_treasure_scope, player))
    add_rule_safe(world, LocationName.sand_ocean_5, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.egg_quarters_5, player,
                  lambda state: state.has(ItemName.rouge_pick_nails, player) and
                                state.has(ItemName.rouge_treasure_scope, player))
    add_rule_safe(world, LocationName.lost_colony_5, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player) and
                                state.has(ItemName.eggman_large_cannon, player))
    add_rule_safe(world, LocationName.weapons_bed_5, player,
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule_safe(world, LocationName.security_hall_5, player,
                  lambda state: state.has(ItemName.rouge_treasure_scope, player))
    add_rule_safe(world, LocationName.cosmic_wall_5, player,
                  lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule_safe(world, LocationName.cannon_core_5, player,
                  lambda state: state.has(ItemName.tails_booster, player) and
                                state.has(ItemName.knuckles_mystic_melody, player) and
                                state.has(ItemName.knuckles_hammer_gloves, player))

    # Upgrade Spot Upgrade Requirements
    add_rule(world.get_location(LocationName.city_escape_upgrade, player),
             lambda state: state.has(ItemName.sonic_bounce_bracelet, player) and
                           state.has(ItemName.sonic_flame_ring, player))
    add_rule(world.get_location(LocationName.wild_canyon_upgrade, player),
             lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule(world.get_location(LocationName.prison_lane_upgrade, player),
             lambda state: state.has(ItemName.tails_bazooka, player))
    add_rule(world.get_location(LocationName.hidden_base_upgrade, player),
             lambda state: state.has(ItemName.tails_booster, player) and
                           (state.has(ItemName.tails_bazooka, player) or state.has(ItemName.tails_mystic_melody, player)))
    add_rule(world.get_location(LocationName.eternal_engine_upgrade, player),
             lambda state: state.has(ItemName.tails_booster, player))
    add_rule(world.get_location(LocationName.meteor_herd_upgrade, player),
             lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule(world.get_location(LocationName.final_rush_upgrade, player),
             lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule(world.get_location(LocationName.iron_gate_upgrade, player),
             lambda state: state.has(ItemName.eggman_jet_engine, player) or
                           state.has(ItemName.eggman_large_cannon, player))
    add_rule(world.get_location(LocationName.dry_lagoon_upgrade, player),
             lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule(world.get_location(LocationName.sand_ocean_upgrade, player),
             lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule(world.get_location(LocationName.security_hall_upgrade, player),
             lambda state: state.has(ItemName.rouge_iron_boots, player))
    add_rule(world.get_location(LocationName.cosmic_wall_upgrade, player),
             lambda state: state.has(ItemName.eggman_jet_engine, player))

    # Chao Key Upgrade Requirements
    if world.keysanity[player]:
        add_rule(world.get_location(LocationName.prison_lane_chao_1, player),
                 lambda state: state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.mission_street_chao_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_chao_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_chao_1, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_chao_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.cosmic_wall_chao_1, player),
                 lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_chao_1, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))

        add_rule(world.get_location(LocationName.prison_lane_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.mission_street_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_chao_2, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_chao_2, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.weapons_bed_chao_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.cosmic_wall_chao_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_chao_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.mission_street_chao_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_chao_3, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_chao_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.crazy_gadget_chao_3, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_flame_ring, player))
        add_rule(world.get_location(LocationName.final_rush_chao_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.egg_quarters_chao_3, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player))
        add_rule(world.get_location(LocationName.lost_colony_chao_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.weapons_bed_chao_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.security_hall_chao_3, player),
                 lambda state: state.has(ItemName.rouge_pick_nails, player))
        add_rule(world.get_location(LocationName.cosmic_wall_chao_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_chao_3, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.sonic_flame_ring, player))

    # Pipe Upgrade Requirements
    if world.whistlesanity[player].value == 1 or world.whistlesanity[player].value == 3:
        add_rule(world.get_location(LocationName.hidden_base_pipe_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.cosmic_wall_pipe_1, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.hidden_base_pipe_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_pipe_2, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.lost_colony_pipe_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_pipe_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.prison_lane_pipe_3, player),
                 lambda state: state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.mission_street_pipe_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_pipe_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_pipe_3, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.weapons_bed_pipe_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_pipe_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.hidden_base_pipe_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_4, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_pipe_4, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_flame_ring, player))

        add_rule(world.get_location(LocationName.weapons_bed_pipe_4, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_4, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_pipe_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.hidden_base_pipe_5, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.eternal_engine_pipe_5, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))

        add_rule(world.get_location(LocationName.weapons_bed_pipe_5, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.cosmic_wall_pipe_5, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_pipe_5, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))

    # Hidden Whistle Upgrade Requirements
    if world.whistlesanity[player].value == 2 or world.whistlesanity[player].value == 3:
        add_rule(world.get_location(LocationName.mission_street_hidden_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.mission_street_hidden_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_hidden_1, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.death_chamber_hidden_2, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.cannon_core_hidden_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))

    # Omochao Upgrade Requirements
    if world.omosanity[player]:
        add_rule(world.get_location(LocationName.eternal_engine_omo_1, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.hidden_base_omo_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_2, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.weapons_bed_omo_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) or
                               state.has(ItemName.eggman_large_cannon, player))

        add_rule(world.get_location(LocationName.hidden_base_omo_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_3, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.final_rush_omo_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.weapons_bed_omo_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.hidden_base_omo_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_4, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.mission_street_omo_5, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_5, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_5, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_5, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.mission_street_omo_6, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_6, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_6, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.lost_colony_omo_6, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_6, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.mission_street_omo_7, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_7, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_7, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.lost_colony_omo_7, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_7, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))

        add_rule(world.get_location(LocationName.mission_street_omo_8, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_omo_8, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_8, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.lost_colony_omo_8, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.security_hall_omo_8, player),
                 lambda state: state.has(ItemName.rouge_iron_boots, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_8, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))

        add_rule(world.get_location(LocationName.death_chamber_omo_9, player),
                 lambda state: state.has(ItemName.knuckles_mystic_melody, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_omo_9, player),
                 lambda state: state.has(ItemName.tails_booster, player))

        add_rule(world.get_location(LocationName.cannon_core_omo_9, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))

        add_rule(world.get_location(LocationName.eternal_engine_omo_10, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))

        add_rule(world.get_location(LocationName.eternal_engine_omo_11, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))

        add_rule(world.get_location(LocationName.eternal_engine_omo_12, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_omo_12, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_flame_ring, player))

        add_rule(world.get_location(LocationName.crazy_gadget_omo_13, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_flame_ring, player))

    # Gold Beetle Upgrade Requirements
    if world.beetlesanity[player]:
        add_rule(world.get_location(LocationName.hidden_base_beetle, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_beetle, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_beetle, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_beetle, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_flame_ring, player))

        add_rule(world.get_location(LocationName.dry_lagoon_beetle, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                               state.has(ItemName.rouge_pick_nails, player) and
                               state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.lost_colony_beetle, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.cosmic_wall_beetle, player),
                 lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                               state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_beetle, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))


def set_boss_gate_rules(world: MultiWorld, player: int, gate_bosses: typing.Dict[int, int]):
    for x in range(len(gate_bosses)):
        if boss_has_requirement(gate_bosses[x + 1]):
            add_rule(world.get_location(boss_gate_set[x], player),
                     lambda state: state.has(ItemName.knuckles_shovel_claws, player))


def set_rules(world: MultiWorld, player: int, gate_bosses: typing.Dict[int, int], mission_map: typing.Dict[int, int], mission_count_map: typing.Dict[int, int]):
    # Mission Progression Rules (Mission 1 begets Mission 2, etc.)
    set_mission_progress_rules(world, player, mission_map, mission_count_map)

    if world.goal[player].value != 3:
        # Upgrade Requirements for each mission location
        if world.logic_difficulty[player].value == 0:
            set_mission_upgrade_rules_standard(world, player)
        elif world.logic_difficulty[player].value == 1:
            set_mission_upgrade_rules_hard(world, player)

    # Upgrade Requirements for each boss gate
    set_boss_gate_rules(world, player, gate_bosses)

    world.completion_condition[player] = lambda state: state.has(ItemName.maria, player)
