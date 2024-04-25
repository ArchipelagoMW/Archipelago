from worlds.generic.Rules import add_rule, set_rule

from . import MMXWorld
from .Names import LocationName, ItemName, RegionName, EventName

def set_rules(world: MMXWorld):
    player = world.player
    multiworld = world.multiworld
    jammed_buster = world.options.jammed_buster.value

    multiworld.completion_condition[player] = lambda state: state.has(ItemName.victory, player)

    # Intro entrance rules
    set_rule(multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.armored_armadillo}", player),
             lambda state: state.has(ItemName.stage_armored_armadillo, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.boomer_kuwanger}", player),
             lambda state: state.has(ItemName.stage_boomer_kuwanger, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.chill_penguin}", player),
             lambda state: state.has(ItemName.stage_chill_penguin, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.flame_mammoth}", player),
             lambda state: state.has(ItemName.stage_flame_mammoth, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.launch_octopus}", player),
             lambda state: state.has(ItemName.stage_launch_octopus, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.spark_mandrill}", player),
             lambda state: state.has(ItemName.stage_spark_mandrill, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.sting_chameleon}", player),
             lambda state: state.has(ItemName.stage_sting_chameleon, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.storm_eagle}", player),
             lambda state: state.has(ItemName.stage_storm_eagle, player))
    
    # Fortress entrance rules
    fortress_open = world.options.sigma_open
    entrance = multiworld.get_entrance(f"{RegionName.intro} -> {RegionName.sigma_fortress}", player)

    if fortress_open == "multiworld":
        add_rule(entrance, lambda state: state.has(ItemName.stage_sigma_fortress, player))
    if fortress_open in ("medals", "all") and world.options.sigma_medal_count.value > 0:
        add_rule(entrance, lambda state: state.has(ItemName.maverick_medal, player, world.options.sigma_medal_count.value))
    if fortress_open in ("weapons", "all") and world.options.sigma_weapon_count.value > 0:
        add_rule(entrance, lambda state: state.has_group("Weapons", player, world.options.sigma_weapon_count.value))
    if fortress_open in ("armor_upgrades", "all") and world.options.sigma_upgrade_count.value > 0:
        add_rule(entrance, lambda state: state.has_group("Armor Upgrades", player, world.options.sigma_upgrade_count.value))
    if fortress_open in ("heart_tanks", "all") and world.options.sigma_heart_tank_count.value > 0:
        add_rule(entrance, lambda state: state.has(ItemName.heart_tank, player, world.options.sigma_heart_tank_count.value))
    if fortress_open in ("sub_tanks", "all") and world.options.sigma_sub_tank_count.value > 0:
        add_rule(entrance, lambda state: state.has(ItemName.sub_tank, player, world.options.sigma_sub_tank_count.value))

    if world.options.logic_leg_sigma.value:
        add_rule(entrance, lambda state: state.has(ItemName.legs, player))

    # Sigma Fortress level rules
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_1_boss} -> {RegionName.sigma_fortress_2}", player),
             lambda state: state.has(EventName.sigma_fortress_1_clear, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_2_boss} -> {RegionName.sigma_fortress_3}", player),
             lambda state: state.has(EventName.sigma_fortress_2_clear, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_3_boss} -> {RegionName.sigma_fortress_4}", player),
             lambda state: state.has(EventName.sigma_fortress_3_clear, player))
    
    # Sigma rules
    add_rule(multiworld.get_location(LocationName.sigma_fortress_4_sigma, player),
             lambda state: state.has(ItemName.arms, player, jammed_buster + 1))

    # Chill Penguin collectibles
    set_rule(multiworld.get_location(LocationName.chill_penguin_heart_tank, player),
             lambda state: state.has(ItemName.fire_wave, player))
    
    # Flame Mammoth collectibles
    set_rule(multiworld.get_location(LocationName.flame_mammoth_arms, player),
             lambda state: (
                 state.has(ItemName.legs, player) and
                 state.has(ItemName.helmet, player) 
             ))
    set_rule(multiworld.get_location(LocationName.flame_mammoth_heart_tank, player),
             lambda state: (
                 state.has(EventName.chill_penguin_clear, player) or
                 (
                    state.has(ItemName.chameleon_sting, player) and
                    state.has(ItemName.arms, player, jammed_buster + 1) 
                 )
             ))
    set_rule(multiworld.get_location(LocationName.flame_mammoth_sub_tank, player),
             lambda state: state.has(ItemName.legs, player))

    # Boomer Kuwanger collectibles
    set_rule(multiworld.get_location(LocationName.boomer_kuwanger_heart_tank, player),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    
    # Sting Chameleon collectibles
    set_rule(multiworld.get_location(LocationName.sting_chameleon_body, player),
             lambda state: state.has(ItemName.legs, player))
    set_rule(multiworld.get_location(LocationName.sting_chameleon_heart_tank, player),
             lambda state: (
                 state.has(ItemName.legs, player) and
                 state.has(EventName.launch_octopus_clear, player)
             ))
    
    # Spark Mandrill collectibles
    set_rule(multiworld.get_location(LocationName.spark_mandrill_sub_tank, player),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    set_rule(multiworld.get_location(LocationName.spark_mandrill_heart_tank, player),
             lambda state: state.has(ItemName.boomerang_cutter, player))

    # Storm Eagle collectibles
    set_rule(multiworld.get_location(LocationName.storm_eagle_heart_tank, player),
             lambda state: state.has(ItemName.legs, player))
    set_rule(multiworld.get_location(LocationName.storm_eagle_helmet, player),
             lambda state: state.has(ItemName.legs, player))

    # Handle pickupsanity
    if world.options.pickupsanity.value:
        add_pickupsanity_logic(world)

    # Handle bosses weakness
    if world.options.logic_boss_weakness.value:
        add_boss_weakness_logic(world)

    # Handle charged shotgun ice logic
    if world.options.logic_charged_shotgun_ice.value:
        add_charged_shotgun_ice_logic(world)


def add_pickupsanity_logic(world):
    player = world.player
    multiworld = world.multiworld
    jammed_buster = world.options.jammed_buster.value

    set_rule(multiworld.get_location(LocationName.chill_penguin_hp_1, player),
             lambda state: state.has(ItemName.fire_wave, player))
    
    set_rule(multiworld.get_location(LocationName.armored_armadillo_hp_1, player),
             lambda state: state.has(ItemName.helmet, player))
    set_rule(multiworld.get_location(LocationName.armored_armadillo_hp_2, player),
             lambda state: state.has(ItemName.helmet, player))

    set_rule(multiworld.get_location(LocationName.sigma_fortress_3_hp_1, player),
             lambda state: (
                 state.has(ItemName.legs, player) and
                 state.has(ItemName.boomerang_cutter, player)
             ))
    set_rule(multiworld.get_location(LocationName.sigma_fortress_3_hp_2, player),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    set_rule(multiworld.get_location(LocationName.sigma_fortress_3_energy_1, player),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    set_rule(multiworld.get_location(LocationName.sigma_fortress_3_hp_4, player),
             lambda state: (
                 state.has(ItemName.arms, player, jammed_buster + 1) and
                 state.has(ItemName.chameleon_sting, player)
             ))
    set_rule(multiworld.get_location(LocationName.sigma_fortress_3_energy_3, player),
             lambda state: (
                 state.has(ItemName.arms, player, jammed_buster + 1) and
                 state.has(ItemName.chameleon_sting, player)
             ))
    set_rule(multiworld.get_location(LocationName.sigma_fortress_3_1up, player),
             lambda state: (
                 state.has(ItemName.arms, player, jammed_buster + 1) and
                 (
                    state.has(ItemName.chameleon_sting, player) or
                    state.has(ItemName.shotgun_ice, player)
                 )
             ))


def add_boss_weakness_logic(world):
    player = world.player
    multiworld = world.multiworld

    # Armored Armadillo
    set_rule(multiworld.get_entrance(f"{RegionName.armored_armadillo_ride_3} -> {RegionName.armored_armadillo_boss}", player),
             lambda state: state.has(ItemName.electric_spark, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_3} -> {RegionName.sigma_fortress_3_rematch_1}", player),
            lambda state: state.has(ItemName.electric_spark, player))

    # Chill Penguin
    set_rule(multiworld.get_entrance(f"{RegionName.chill_penguin_ride} -> {RegionName.chill_penguin_boss}", player),
             lambda state: state.has(ItemName.fire_wave, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_2_start} -> {RegionName.sigma_fortress_2_rematch_1}", player),
            lambda state: state.has(ItemName.fire_wave, player))
    
    # Flame Mammoth
    set_rule(multiworld.get_entrance(f"{RegionName.flame_mammoth_lava_river_2} -> {RegionName.flame_mammoth_boss}", player),
             lambda state: state.has(ItemName.storm_tornado, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_3_rematch_4} -> {RegionName.sigma_fortress_3_rematch_5}", player),
             lambda state: state.has(ItemName.storm_tornado, player))

    # Boomer Kuwanger
    set_rule(multiworld.get_entrance(f"{RegionName.boomer_kuwanger_top} -> {RegionName.boomer_kuwanger_boss}", player),
             lambda state: state.has(ItemName.homing_torpedo, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_1_vertical} -> {RegionName.sigma_fortress_1_rematch_1}", player),
             lambda state: state.has(ItemName.homing_torpedo, player))
    
    # Sting Chameleon
    set_rule(multiworld.get_entrance(f"{RegionName.sting_chameleon_swamp} -> {RegionName.sting_chameleon_boss}", player),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_3_rematch_1} -> {RegionName.sigma_fortress_3_rematch_2}", player),
             lambda state: state.has(ItemName.boomerang_cutter, player))
    
    # Spark Mandrill
    set_rule(multiworld.get_entrance(f"{RegionName.spark_mandrill_deep} -> {RegionName.spark_mandrill_boss}", player),
             lambda state: state.has(ItemName.shotgun_ice, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_3_rematch_2} -> {RegionName.sigma_fortress_3_rematch_3}", player),
             lambda state: state.has(ItemName.shotgun_ice, player))

    # Storm Eagle
    set_rule(multiworld.get_entrance(f"{RegionName.storm_eagle_aircraft} -> {RegionName.storm_eagle_boss}", player),
             lambda state: state.has(ItemName.chameleon_sting, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_2_ride} -> {RegionName.sigma_fortress_2_rematch_2}", player),
             lambda state: state.has(ItemName.chameleon_sting, player))
    
    # Launch Octopus
    set_rule(multiworld.get_entrance(f"{RegionName.launch_octopus_sea} -> {RegionName.launch_octopus_boss}", player),
             lambda state: state.has(ItemName.rolling_shield, player))
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_3_rematch_3} -> {RegionName.sigma_fortress_3_rematch_4}", player),
             lambda state: state.has(ItemName.rolling_shield, player))

    # Bospider
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_1_rematch_1} -> {RegionName.sigma_fortress_1_boss}", player),
            lambda state: state.has(ItemName.shotgun_ice, player))
    
    # Rangda Bangda
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_2_rematch_2} -> {RegionName.sigma_fortress_2_boss}", player),
            lambda state: state.has(ItemName.chameleon_sting, player))
    
    # D-Rex
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_3_rematch_5} -> {RegionName.sigma_fortress_3_boss}", player),
            lambda state: state.has(ItemName.boomerang_cutter, player))
    
    # Velguarder
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_4} -> {RegionName.sigma_fortress_4_dog}", player),
            lambda state: state.has(ItemName.shotgun_ice, player))
    
    # Sigma & Wolf Sigma
    set_rule(multiworld.get_entrance(f"{RegionName.sigma_fortress_4_dog} -> {RegionName.sigma_fortress_4_sigma}", player),
            lambda state: (
                state.has(ItemName.electric_spark, player) and
                state.has(ItemName.rolling_shield, player)
            ))


def add_charged_shotgun_ice_logic(world):
    player = world.player
    multiworld = world.multiworld
    jammed_buster = world.options.jammed_buster.value

    # Flame Mammoth collectibles
    add_rule(multiworld.get_location(LocationName.flame_mammoth_sub_tank, player),
             lambda state: (
                state.has(ItemName.arms, player, jammed_buster + 1) and
                state.has(ItemName.boomerang_cutter, player) and
                state.has(ItemName.shotgun_ice, player) 
             ))
    # Boomer Kuwanger collectibles
    add_rule(multiworld.get_location(LocationName.boomer_kuwanger_heart_tank, player),
             lambda state: (
                state.has(ItemName.shotgun_ice, player) and
                state.has(ItemName.arms, player, jammed_buster + 1) 
             ))
    # Sting Chameleon collectibles
    add_rule(multiworld.get_location(LocationName.sting_chameleon_body, player),
             lambda state: (
                state.has(ItemName.shotgun_ice, player) and
                state.has(ItemName.arms, player, jammed_buster + 1) 
             ))
