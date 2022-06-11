import typing

from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from .Locations import first_mission_location_table, second_mission_location_table, third_mission_location_table, \
    fourth_mission_location_table, fifth_mission_location_table, \
    upgrade_location_table, boss_gate_set
from ..AutoWorld import LogicMixin
from ..generic.Rules import add_rule, set_rule
from .GateBosses import boss_has_requirement


def set_mission_progress_rules(world: MultiWorld, player: int):
    for (k1, v1), (k2, v2), (k3, v3), (k4, v4), (k5, v5) in \
            zip(sorted(first_mission_location_table.items()),
                sorted(second_mission_location_table.items()),
                sorted(third_mission_location_table.items()),
                sorted(fourth_mission_location_table.items()),
                sorted(fifth_mission_location_table.items())):

        if world.include_missions[player].value >= 2:
            set_rule(world.get_location(k2, player), lambda state, k1=k1: state.can_reach(k1, "Location", player))

        if world.include_missions[player].value >= 3:
            set_rule(world.get_location(k3, player), lambda state, k2=k2: state.can_reach(k2, "Location", player))

        if world.include_missions[player].value >= 4:
            set_rule(world.get_location(k4, player), lambda state, k3=k3: state.can_reach(k3, "Location", player))

        if world.include_missions[player].value >= 5:
            set_rule(world.get_location(k5, player), lambda state, k4=k4: state.can_reach(k4, "Location", player))


def set_mission_upgrade_rules(world: MultiWorld, player: int):
    # Mission 1 Upgrade Requirements
    add_rule(world.get_location(LocationName.metal_harbor_1, player),
             lambda state: state.has(ItemName.sonic_light_shoes, player))
    add_rule(world.get_location(LocationName.pumpkin_hill_1, player),
             lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule(world.get_location(LocationName.mission_street_1, player),
             lambda state: state.has(ItemName.tails_booster, player))
    add_rule(world.get_location(LocationName.aquatic_mine_1, player),
             lambda state: state.has(ItemName.knuckles_shovel_claws, player))
    add_rule(world.get_location(LocationName.hidden_base_1, player),
             lambda state: state.has(ItemName.tails_booster, player))
    add_rule(world.get_location(LocationName.pyramid_cave_1, player),
             lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
    add_rule(world.get_location(LocationName.death_chamber_1, player),
             lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                           state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule(world.get_location(LocationName.eternal_engine_1, player),
             lambda state: state.has(ItemName.tails_booster, player) and
                           state.has(ItemName.tails_bazooka, player))
    add_rule(world.get_location(LocationName.meteor_herd_1, player),
             lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                           state.has(ItemName.knuckles_hammer_gloves, player))
    add_rule(world.get_location(LocationName.crazy_gadget_1, player),
             lambda state: state.has(ItemName.sonic_light_shoes, player) and
                           state.has(ItemName.sonic_bounce_bracelet, player) and
                           state.has(ItemName.sonic_flame_ring, player))
    add_rule(world.get_location(LocationName.final_rush_1, player),
             lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

    add_rule(world.get_location(LocationName.egg_quarters_1, player),
             lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule(world.get_location(LocationName.lost_colony_1, player),
             lambda state: state.has(ItemName.eggman_jet_engine, player))
    add_rule(world.get_location(LocationName.weapons_bed_1, player),
             lambda state: state.has(ItemName.eggman_jet_engine, player) and
                           state.has(ItemName.eggman_large_cannon, player))
    add_rule(world.get_location(LocationName.security_hall_1, player),
             lambda state: state.has(ItemName.rouge_pick_nails, player))
    add_rule(world.get_location(LocationName.white_jungle_1, player),
             lambda state: state.has(ItemName.shadow_air_shoes, player))
    add_rule(world.get_location(LocationName.mad_space_1, player),
             lambda state: state.has(ItemName.rouge_pick_nails, player) and
                           state.has(ItemName.rouge_iron_boots, player))
    add_rule(world.get_location(LocationName.cosmic_wall_1, player),
             lambda state: state.has(ItemName.eggman_jet_engine, player))

    add_rule(world.get_location(LocationName.cannon_core_1, player),
             lambda state: state.has(ItemName.tails_booster, player) and
                           state.has(ItemName.eggman_jet_engine, player) and
                           state.has(ItemName.knuckles_hammer_gloves, player) and
                           state.has(ItemName.knuckles_air_necklace, player) and
                           state.has(ItemName.sonic_bounce_bracelet, player))

    # Mission 2 Upgrade Requirements
    if world.include_missions[player].value >= 2:
        add_rule(world.get_location(LocationName.metal_harbor_2, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.mission_street_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.hidden_base_2, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.death_chamber_2, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_2, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.crazy_gadget_2, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.lost_colony_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.weapons_bed_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.security_hall_2, player),
                 lambda state: state.has(ItemName.rouge_pick_nails, player))
        add_rule(world.get_location(LocationName.mad_space_2, player),
                 lambda state: state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.cosmic_wall_2, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_2, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player))

    # Mission 3 Upgrade Requirements
    if world.include_missions[player].value >= 3:
        add_rule(world.get_location(LocationName.city_escape_3, player),
                 lambda state: state.has(ItemName.sonic_mystic_melody, player))
        add_rule(world.get_location(LocationName.wild_canyon_3, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_mystic_melody, player))
        add_rule(world.get_location(LocationName.prison_lane_3, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_mystic_melody, player))
        add_rule(world.get_location(LocationName.metal_harbor_3, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_mystic_melody, player))
        add_rule(world.get_location(LocationName.green_forest_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_mystic_melody, player))
        add_rule(world.get_location(LocationName.pumpkin_hill_3, player),
                 lambda state: state.has(ItemName.knuckles_mystic_melody, player))
        add_rule(world.get_location(LocationName.mission_street_3, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_mystic_melody, player))
        add_rule(world.get_location(LocationName.aquatic_mine_3, player),
                 lambda state: state.has(ItemName.knuckles_mystic_melody, player))
        add_rule(world.get_location(LocationName.hidden_base_3, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_mystic_melody, player))
        add_rule(world.get_location(LocationName.pyramid_cave_3, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_mystic_melody, player))
        add_rule(world.get_location(LocationName.death_chamber_3, player),
                 lambda state: state.has(ItemName.knuckles_mystic_melody, player) and
                               state.has(ItemName.knuckles_air_necklace, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_3, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_mystic_melody, player))
        add_rule(world.get_location(LocationName.meteor_herd_3, player),
                 lambda state: state.has(ItemName.knuckles_mystic_melody, player))
        add_rule(world.get_location(LocationName.crazy_gadget_3, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_flame_ring, player) and
                               state.has(ItemName.sonic_mystic_melody, player))
        add_rule(world.get_location(LocationName.final_rush_3, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_mystic_melody, player))

        add_rule(world.get_location(LocationName.iron_gate_3, player),
                 lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.dry_lagoon_3, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                               state.has(ItemName.rouge_pick_nails, player) and
                               state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.sand_ocean_3, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.radical_highway_3, player),
                 lambda state: state.has(ItemName.shadow_mystic_melody, player))
        add_rule(world.get_location(LocationName.egg_quarters_3, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                               state.has(ItemName.rouge_pick_nails, player) and
                               state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.lost_colony_3, player),
                 lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                               state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.weapons_bed_3, player),
                 lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.security_hall_3, player),
                 lambda state: state.has(ItemName.rouge_treasure_scope, player))
        add_rule(world.get_location(LocationName.white_jungle_3, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player) and
                               state.has(ItemName.shadow_mystic_melody, player))
        add_rule(world.get_location(LocationName.sky_rail_3, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player) and
                               state.has(ItemName.shadow_mystic_melody, player))
        add_rule(world.get_location(LocationName.mad_space_3, player),
                 lambda state: state.has(ItemName.rouge_mystic_melody, player) and
                               state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.cosmic_wall_3, player),
                 lambda state: state.has(ItemName.eggman_mystic_melody, player) and
                               state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.final_chase_3, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player) and
                               state.has(ItemName.shadow_mystic_melody, player))

        add_rule(world.get_location(LocationName.cannon_core_3, player),
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
    if world.include_missions[player].value >= 4:
        add_rule(world.get_location(LocationName.metal_harbor_4, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.pumpkin_hill_4, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player))
        add_rule(world.get_location(LocationName.mission_street_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.aquatic_mine_4, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player))
        add_rule(world.get_location(LocationName.hidden_base_4, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_4, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.death_chamber_4, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.eternal_engine_4, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.meteor_herd_4, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player))
        add_rule(world.get_location(LocationName.crazy_gadget_4, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_flame_ring, player))
        add_rule(world.get_location(LocationName.final_rush_4, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.egg_quarters_4, player),
                 lambda state: state.has(ItemName.rouge_pick_nails, player))
        add_rule(world.get_location(LocationName.lost_colony_4, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))
        add_rule(world.get_location(LocationName.weapons_bed_4, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.security_hall_4, player),
                 lambda state: state.has(ItemName.rouge_pick_nails, player))
        add_rule(world.get_location(LocationName.white_jungle_4, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player))
        add_rule(world.get_location(LocationName.mad_space_4, player),
                 lambda state: state.has(ItemName.rouge_pick_nails, player) and
                               state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.cosmic_wall_4, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_4, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_air_necklace, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player))

    # Mission 5 Upgrade Requirements
    if world.include_missions[player].value >= 5:
        add_rule(world.get_location(LocationName.city_escape_5, player),
                 lambda state: state.has(ItemName.sonic_flame_ring, player) and
                               state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.wild_canyon_5, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_sunglasses, player))
        add_rule(world.get_location(LocationName.metal_harbor_5, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player))
        add_rule(world.get_location(LocationName.pumpkin_hill_5, player),
                 lambda state: state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_sunglasses, player))
        add_rule(world.get_location(LocationName.mission_street_5, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.aquatic_mine_5, player),
                 lambda state: state.has(ItemName.knuckles_mystic_melody, player) and
                               state.has(ItemName.knuckles_air_necklace, player) and
                               state.has(ItemName.knuckles_sunglasses, player))
        add_rule(world.get_location(LocationName.hidden_base_5, player),
                 lambda state: state.has(ItemName.tails_booster, player))
        add_rule(world.get_location(LocationName.pyramid_cave_5, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))
        add_rule(world.get_location(LocationName.death_chamber_5, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_shovel_claws, player) and
                               state.has(ItemName.knuckles_mystic_melody, player) and
                               state.has(ItemName.knuckles_air_necklace, player))
        add_rule(world.get_location(LocationName.eternal_engine_5, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.tails_bazooka, player))
        add_rule(world.get_location(LocationName.meteor_herd_5, player),
                 lambda state: state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_sunglasses, player))
        add_rule(world.get_location(LocationName.crazy_gadget_5, player),
                 lambda state: state.has(ItemName.sonic_light_shoes, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player) and
                               state.has(ItemName.sonic_flame_ring, player))
        add_rule(world.get_location(LocationName.final_rush_5, player),
                 lambda state: state.has(ItemName.sonic_bounce_bracelet, player))

        add_rule(world.get_location(LocationName.iron_gate_5, player),
                 lambda state: state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.dry_lagoon_5, player),
                 lambda state: state.has(ItemName.rouge_treasure_scope, player))
        add_rule(world.get_location(LocationName.egg_quarters_5, player),
                 lambda state: state.has(ItemName.rouge_treasure_scope, player))
        add_rule(world.get_location(LocationName.lost_colony_5, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.weapons_bed_5, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.eggman_large_cannon, player))
        add_rule(world.get_location(LocationName.security_hall_5, player),
                 lambda state: state.has(ItemName.rouge_pick_nails, player) and
                               state.has(ItemName.rouge_treasure_scope, player) and
                               state.has(ItemName.rouge_iron_boots, player))
        add_rule(world.get_location(LocationName.white_jungle_5, player),
                 lambda state: state.has(ItemName.shadow_air_shoes, player) and
                               state.has(ItemName.shadow_flame_ring, player))
        add_rule(world.get_location(LocationName.cosmic_wall_5, player),
                 lambda state: state.has(ItemName.eggman_jet_engine, player))

        add_rule(world.get_location(LocationName.cannon_core_5, player),
                 lambda state: state.has(ItemName.tails_booster, player) and
                               state.has(ItemName.eggman_jet_engine, player) and
                               state.has(ItemName.knuckles_mystic_melody, player) and
                               state.has(ItemName.knuckles_hammer_gloves, player) and
                               state.has(ItemName.knuckles_air_necklace, player) and
                               state.has(ItemName.sonic_bounce_bracelet, player))

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


def set_boss_gate_rules(world: MultiWorld, player: int, gate_bosses: typing.Dict[int, int]):
    for x in range(len(gate_bosses)):
        if boss_has_requirement(gate_bosses[x + 1]):
            add_rule(world.get_location(boss_gate_set[x], player),
                     lambda state: state.has(ItemName.knuckles_shovel_claws, player))


def set_rules(world: MultiWorld, player: int, gate_bosses: typing.Dict[int, int]):
    # Mission Progression Rules (Mission 1 begets Mission 2, etc.)
    set_mission_progress_rules(world, player)

    # Upgrade Requirements for each mission location
    set_mission_upgrade_rules(world, player)

    # Upgrade Requirements for each boss gate
    set_boss_gate_rules(world, player, gate_bosses)

    world.completion_condition[player] = lambda state: state.has(ItemName.maria, player)
