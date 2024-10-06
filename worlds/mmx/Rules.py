from worlds.generic.Rules import add_rule, set_rule
from BaseClasses import CollectionState

from .Names import LocationName, ItemName, RegionName, EventName
  
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MMXWorld

bosses = {
    "Sting Chameleon": [
        f"{RegionName.sting_chameleon_swamp} -> {RegionName.sting_chameleon_boss}",
        f"{RegionName.sigma_fortress_3_after_rematch_1} -> {RegionName.sigma_fortress_3_rematch_2}"
    ],
    "Storm Eagle": [
        f"{RegionName.storm_eagle_aircraft} -> {RegionName.storm_eagle_boss}",
        f"{RegionName.sigma_fortress_2_ride} -> {RegionName.sigma_fortress_2_rematch_2}"
    ],
    "Flame Mammoth": [
        f"{RegionName.flame_mammoth_lava_river_2} -> {RegionName.flame_mammoth_boss}",
        f"{RegionName.sigma_fortress_3_after_rematch_4} -> {RegionName.sigma_fortress_3_rematch_5}"
    ],
    "Chill Penguin": [
        f"{RegionName.chill_penguin_ride} -> {RegionName.chill_penguin_boss}",
        f"{RegionName.sigma_fortress_2_start} -> {RegionName.sigma_fortress_2_rematch_1}"
    ],
    "Spark Mandrill": [
        f"{RegionName.spark_mandrill_deep} -> {RegionName.spark_mandrill_boss}",
        f"{RegionName.sigma_fortress_3_after_rematch_2} -> {RegionName.sigma_fortress_3_rematch_3}"
    ],
    "Armored Armadillo": [
        f"{RegionName.armored_armadillo_ride_3} -> {RegionName.armored_armadillo_boss}",
        f"{RegionName.sigma_fortress_3} -> {RegionName.sigma_fortress_3_rematch_1}"
    ],
    "Launch Octopus": [
        f"{RegionName.launch_octopus_sea} -> {RegionName.launch_octopus_boss}",
        f"{RegionName.sigma_fortress_3_after_rematch_3} -> {RegionName.sigma_fortress_3_rematch_4}"
    ],
    "Boomer Kuwanger": [
        f"{RegionName.boomer_kuwanger_top} -> {RegionName.boomer_kuwanger_boss}",
        f"{RegionName.sigma_fortress_1_vertical} -> {RegionName.sigma_fortress_1_rematch_1}"
    ],
    "Thunder Slimer": [
        f"{RegionName.spark_mandrill_entrance} -> {RegionName.spark_mandrill_mid_boss}"
    ],
    "Vile": [
        f"{RegionName.sigma_fortress_1_outside} -> {RegionName.sigma_fortress_1_vile}"
    ],
    "Bospider": [
        f"{RegionName.sigma_fortress_1_before_boss} -> {RegionName.sigma_fortress_1_boss}"
    ],
    "Rangda Bangda": [
        f"{RegionName.sigma_fortress_2_before_boss} -> {RegionName.sigma_fortress_2_boss}"
    ],
    "D-Rex": [
        f"{RegionName.sigma_fortress_3_after_rematch_5} -> {RegionName.sigma_fortress_3_boss}"
    ],
    "Velguarder": [
        f"{RegionName.sigma_fortress_4} -> {RegionName.sigma_fortress_4_dog}"
    ],
    "Sigma": [
        f"{RegionName.sigma_fortress_4_dog} -> {RegionName.sigma_fortress_4_sigma}"
    ],
    "Wolf Sigma": [
        f"{RegionName.sigma_fortress_4_dog} -> {RegionName.sigma_fortress_4_sigma}"
    ],
}


def build_rules(world: "MMXWorld") -> None:
    player = world.player
    multiworld = world.multiworld
    jammed_buster = world.options.jammed_buster.value

    multiworld.completion_condition[player] = lambda state: state.has(ItemName.victory, player)

    # Intro entrance rules
    set_rule(world.get_entrance(f"{RegionName.intro} -> {RegionName.armored_armadillo}"),
             lambda state: state.has(ItemName.stage_armored_armadillo, player))
    set_rule(world.get_entrance(f"{RegionName.intro} -> {RegionName.boomer_kuwanger}"),
             lambda state: state.has(ItemName.stage_boomer_kuwanger, player))
    set_rule(world.get_entrance(f"{RegionName.intro} -> {RegionName.chill_penguin}"),
             lambda state: state.has(ItemName.stage_chill_penguin, player))
    set_rule(world.get_entrance(f"{RegionName.intro} -> {RegionName.flame_mammoth}"),
             lambda state: state.has(ItemName.stage_flame_mammoth, player))
    set_rule(world.get_entrance(f"{RegionName.intro} -> {RegionName.launch_octopus}"),
             lambda state: state.has(ItemName.stage_launch_octopus, player))
    set_rule(world.get_entrance(f"{RegionName.intro} -> {RegionName.spark_mandrill}"),
             lambda state: state.has(ItemName.stage_spark_mandrill, player))
    set_rule(world.get_entrance(f"{RegionName.intro} -> {RegionName.sting_chameleon}"),
             lambda state: state.has(ItemName.stage_sting_chameleon, player))
    set_rule(world.get_entrance(f"{RegionName.intro} -> {RegionName.storm_eagle}"),
             lambda state: state.has(ItemName.stage_storm_eagle, player))
    
    # Fortress entrance rules
    fortress_open = world.options.sigma_open.value
    entrance = world.get_entrance(f"{RegionName.intro} -> {RegionName.sigma_fortress}")

    if len(fortress_open) == 0:
        add_rule(entrance, lambda state: state.has(ItemName.stage_sigma_fortress, player))
    else:
        if "Medals" in fortress_open and world.options.sigma_medal_count > 0:
            add_rule(entrance, lambda state: state.has(ItemName.maverick_medal, player, world.options.sigma_medal_count.value))
        if "Weapons" in fortress_open and world.options.sigma_weapon_count > 0:
            add_rule(entrance, lambda state: state.has_group_unique("Weapons", player, world.options.sigma_weapon_count.value))
        if "Armor Upgrades" in fortress_open and world.options.sigma_upgrade_count > 0:
            add_rule(entrance, lambda state: state.has_group_unique("Armor Upgrades", player, world.options.sigma_upgrade_count.value))
        if "Heart Tanks" in fortress_open and world.options.sigma_heart_tank_count > 0:
            add_rule(entrance, lambda state: state.has(ItemName.heart_tank, player, world.options.sigma_heart_tank_count.value))
        if "Sub Tanks" in fortress_open and world.options.sigma_sub_tank_count > 0:
            add_rule(entrance, lambda state: state.has(ItemName.sub_tank, player, world.options.sigma_sub_tank_count.value))

    if world.options.logic_leg_sigma:
        add_rule(entrance, lambda state: state.has(ItemName.legs, player))

    # Sigma Fortress level rules
    if world.options.sigma_all_levels:
        set_rule(world.get_entrance(f"{RegionName.sigma_fortress} -> {RegionName.sigma_fortress_4}"),
                 lambda state: (
                     state.has(EventName.sigma_fortress_1_clear, player) and 
                     state.has(EventName.sigma_fortress_2_clear, player) and 
                     state.has(EventName.sigma_fortress_3_clear, player)
                    ))
    else:
        set_rule(world.get_entrance(f"{RegionName.sigma_fortress_1_boss} -> {RegionName.sigma_fortress_2}"),
                lambda state: state.has(EventName.sigma_fortress_1_clear, player))
        set_rule(world.get_entrance(f"{RegionName.sigma_fortress_2_boss} -> {RegionName.sigma_fortress_3}"),
                lambda state: state.has(EventName.sigma_fortress_2_clear, player))
        set_rule(world.get_entrance(f"{RegionName.sigma_fortress_3_boss} -> {RegionName.sigma_fortress_4}"),
                lambda state: state.has(EventName.sigma_fortress_3_clear, player))
    
    # Sigma rules
    add_rule(world.get_location(LocationName.sigma_fortress_4_sigma),
             lambda state: state.has(ItemName.arms, player, jammed_buster + 1))

    # Chill Penguin collectibles
    set_rule(world.get_location(LocationName.chill_penguin_heart_tank),
             lambda state: state.has(ItemName.fire_wave, player))
    
    # Flame Mammoth collectibles
    set_rule(world.get_location(LocationName.flame_mammoth_arms),
             lambda state: (
                 state.has(ItemName.legs, player) and
                 state.has(ItemName.helmet, player) 
             ))
    set_rule(world.get_location(LocationName.flame_mammoth_heart_tank),
             lambda state: (
                 state.has(EventName.chill_penguin_clear, player) or
                 (
                    state.has(ItemName.chameleon_sting, player) and
                    state.has(ItemName.arms, player, jammed_buster + 1) 
                 )
             ))
    set_rule(world.get_location(LocationName.flame_mammoth_sub_tank),
             lambda state: state.has(ItemName.legs, player))

    # Boomer Kuwanger collectibles
    set_rule(world.get_location(LocationName.boomer_kuwanger_heart_tank),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    
    # Sting Chameleon collectibles
    set_rule(world.get_location(LocationName.sting_chameleon_body),
             lambda state: state.has(ItemName.legs, player))
    set_rule(world.get_location(LocationName.sting_chameleon_heart_tank),
             lambda state: (
                 state.has(ItemName.legs, player) and
                 state.has(EventName.launch_octopus_clear, player)
             ))
    
    # Spark Mandrill collectibles
    set_rule(world.get_location(LocationName.spark_mandrill_sub_tank),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    set_rule(world.get_location(LocationName.spark_mandrill_heart_tank),
             lambda state: (
                 state.has(ItemName.boomerang_cutter, player) or 
                 state.has(ItemName.legs, player)
             ))

    # Storm Eagle collectibles
    set_rule(world.get_location(LocationName.storm_eagle_heart_tank),
             lambda state: state.has(ItemName.legs, player))
    set_rule(world.get_location(LocationName.storm_eagle_helmet),
             lambda state: state.has(ItemName.legs, player))

    # Handle pickupsanity
    if world.options.pickupsanity:
        add_pickupsanity_logic(world)

    # Handle bosses weakness
    if world.options.logic_boss_weakness or world.options.boss_weakness_strictness >= 2:
        add_boss_weakness_logic(world)

    # Handle charged shotgun ice logic
    if world.options.logic_charged_shotgun_ice:
        add_charged_shotgun_ice_logic(world)

    # Handle helmet logic
    if world.options.logic_helmet_checkpoints:
        add_helmet_logic(world)


def add_pickupsanity_logic(world: "MMXWorld") -> None:
    player = world.player
    jammed_buster = world.options.jammed_buster.value

    set_rule(world.get_location(LocationName.chill_penguin_hp_1),
             lambda state: state.has(ItemName.fire_wave, player))
    
    set_rule(world.get_location(LocationName.armored_armadillo_hp_1),
             lambda state: state.has(ItemName.helmet, player))
    set_rule(world.get_location(LocationName.armored_armadillo_hp_2),
             lambda state: state.has(ItemName.helmet, player))

    set_rule(world.get_location(LocationName.sigma_fortress_3_hp_1),
             lambda state: (
                 state.has(ItemName.legs, player) and
                 state.has(ItemName.boomerang_cutter, player)
             ))
    set_rule(world.get_location(LocationName.sigma_fortress_3_hp_2),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    set_rule(world.get_location(LocationName.sigma_fortress_3_energy_1),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    set_rule(world.get_location(LocationName.sigma_fortress_3_hp_4),
             lambda state: (
                 state.has(ItemName.arms, player, jammed_buster + 1) and
                 state.has(ItemName.chameleon_sting, player)
             ))
    set_rule(world.get_location(LocationName.sigma_fortress_3_energy_3),
             lambda state: (
                 state.has(ItemName.arms, player, jammed_buster + 1) and
                 state.has(ItemName.chameleon_sting, player)
             ))
    set_rule(world.get_location(LocationName.sigma_fortress_3_1up),
             lambda state: (
                 state.has(ItemName.arms, player, jammed_buster + 1) and
                 (
                    state.has(ItemName.chameleon_sting, player) or
                    state.has(ItemName.shotgun_ice, player)
                 )
             ))


def check_weaknesses(state: CollectionState, player: int, rulesets: list) -> bool:
    states = list()
    for i in range(len(rulesets)):
        valid = state.has_all_counts(rulesets[i], player)
        states.append(valid)
    return any(states)


def add_boss_weakness_logic(world: "MMXWorld") -> None:
    player = world.player
    jammed_buster = world.options.jammed_buster.value

    for boss, regions in bosses.items():
        weaknesses = world.boss_weaknesses[boss]
        rulesets = list()
        for weakness in weaknesses:
            if weakness[0] is None:
                rulesets = None
                break
            weakness = weakness[0]
            ruleset = dict()
            if "Check Charge" in weakness[0]:
                ruleset[ItemName.arms] = jammed_buster + int(weakness[0][-1:]) - 1
            elif "Check Dash" in weakness[0]:
                ruleset[ItemName.legs] = 1
            else:
                ruleset[weakness[0]] = 1
            if len(weakness) != 1:
                ruleset[weakness[1]] = 1
            rulesets.append(ruleset)

        if rulesets is not None:
            for region in regions:
                add_rule(world.get_entrance(region),
                         lambda state, rulesets=rulesets: check_weaknesses(state, player, rulesets))


def add_charged_shotgun_ice_logic(world: "MMXWorld") -> None:
    player = world.player
    jammed_buster = world.options.jammed_buster.value

    # Flame Mammoth collectibles
    add_rule(world.get_location(LocationName.flame_mammoth_sub_tank),
             lambda state: (
                state.has(ItemName.arms, player, jammed_buster + 1) and
                state.has(ItemName.boomerang_cutter, player) and
                state.has(ItemName.shotgun_ice, player) 
             ))
    # Boomer Kuwanger collectibles
    add_rule(world.get_location(LocationName.boomer_kuwanger_heart_tank),
             lambda state: (
                state.has(ItemName.shotgun_ice, player) and
                state.has(ItemName.arms, player, jammed_buster + 1) 
             ))
    # Sting Chameleon collectibles
    add_rule(world.get_location(LocationName.sting_chameleon_body),
             lambda state: (
                state.has(ItemName.shotgun_ice, player) and
                state.has(ItemName.arms, player, jammed_buster + 1) 
             ))


def add_helmet_logic(world: "MMXWorld") -> None:
    player = world.player

    set_rule(world.get_entrance(f"{RegionName.spark_mandrill} -> {RegionName.spark_mandrill_deep}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_1} -> {RegionName.sigma_fortress_1_vertical}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_1} -> {RegionName.sigma_fortress_1_before_boss}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_2} -> {RegionName.sigma_fortress_2_ride}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_2} -> {RegionName.sigma_fortress_2_before_boss}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_3} -> {RegionName.sigma_fortress_3_after_rematch_1}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_3} -> {RegionName.sigma_fortress_3_after_rematch_2}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_3} -> {RegionName.sigma_fortress_3_after_rematch_3}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_3} -> {RegionName.sigma_fortress_3_after_rematch_4}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
    set_rule(world.get_entrance(f"{RegionName.sigma_fortress_3} -> {RegionName.sigma_fortress_3_after_rematch_5}"), 
             lambda state: state.has(ItemName.helmet, player, 1))
