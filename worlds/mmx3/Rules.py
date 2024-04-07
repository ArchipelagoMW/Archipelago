from worlds.generic.Rules import add_rule, set_rule

from . import MMX3World
from .Names import LocationName, ItemName, RegionName, EventName

def set_rules(world: MMX3World):
    player = world.player
    multiworld = world.multiworld

    multiworld.completion_condition[player] = lambda state: state.has(ItemName.victory, player)

    # Hunter base entrance rules
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.blizzard_buffalo}", player),
             lambda state: state.has(ItemName.stage_blizzard_buffalo, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.toxic_seahorse}", player),
             lambda state: state.has(ItemName.stage_toxic_seahorse, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.tunnel_rhino}", player),
             lambda state: state.has(ItemName.stage_tunnel_rhino, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.volt_catfish}", player),
             lambda state: state.has(ItemName.stage_volt_catfish, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.crush_crawfish}", player),
             lambda state: state.has(ItemName.stage_crush_crawfish, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.neon_tiger}", player),
             lambda state: state.has(ItemName.stage_neon_tiger, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.gravity_beetle}", player),
             lambda state: state.has(ItemName.stage_gravity_beetle, player))
    set_rule(multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.blast_hornet}", player),
             lambda state: state.has(ItemName.stage_blast_hornet, player))

    # Doppler Lab entrance rules
    doppler_open = world.options.doppler_open
    entrance = multiworld.get_entrance(f"{RegionName.intro_stage} -> {RegionName.dr_doppler_lab}", player)

    if doppler_open == "multiworld":
        add_rule(entrance, lambda state: state.has(ItemName.stage_doppler_lab, player))
    elif doppler_open == "medals":
        add_rule(entrance, lambda state: state.has(ItemName.maverick_medal, player, world.options.doppler_medal_count.value))
    elif doppler_open == "weapons":
        add_rule(entrance, lambda state: state.has_group("Weapons", player, world.options.doppler_weapon_count.value))
    elif doppler_open == "armor_upgrades":
        add_rule(entrance, lambda state: state.has_group("Armor Upgrades", player, world.options.doppler_upgrade_count.value))
    elif doppler_open == "heart_tanks":
        add_rule(entrance, lambda state: state.has(ItemName.heart_tank, player, world.options.doppler_heart_tank_count.value))
    elif doppler_open == "sub_tanks":
        add_rule(entrance, lambda state: state.has(ItemName.sub_tank, player, world.options.doppler_sub_tank_count.value))

    if world.options.logic_vile_required.value:
        add_rule(entrance, lambda state: state.has(EventName.vile_defeated, player))

    # Doppler Lab level rules
    set_rule(multiworld.get_entrance(f"{RegionName.dr_doppler_lab_1} -> {RegionName.dr_doppler_lab_2}", player),
             lambda state: state.has(EventName.dr_doppler_lab_1_clear, player))
    set_rule(multiworld.get_entrance(f"{RegionName.dr_doppler_lab_2} -> {RegionName.dr_doppler_lab_3}", player),
             lambda state: state.has(EventName.dr_doppler_lab_2_clear, player))
    set_rule(multiworld.get_entrance(f"{RegionName.dr_doppler_lab_3_boss} -> {RegionName.dr_doppler_lab_4}", player),
             lambda state: state.has(EventName.dr_doppler_lab_3_clear, player))

    # Set Boss rematch rules
    set_rule(multiworld.get_entrance(f"{RegionName.dr_doppler_lab_3_rematches} -> {RegionName.dr_doppler_lab_3_boss}", player),
             lambda state: state.has(EventName.boss_rematch_clear, player, world.options.doppler_lab_3_boss_rematch_count.value))

    # Vile entrance rules
    vile_open = world.options.vile_open
    entrance_blizzard = multiworld.get_entrance(f"{RegionName.blizzard_buffalo_start} -> {RegionName.vile}", player)
    entrance_volt = multiworld.get_entrance(f"{RegionName.volt_catfish_start} -> {RegionName.vile}", player)
    entrance_crush = multiworld.get_entrance(f"{RegionName.crush_crawfish_start} -> {RegionName.vile}", player)
    if vile_open == "multiworld":
        set_rule(entrance_blizzard, lambda state: state.has(ItemName.stage_vile, player))
        set_rule(entrance_volt, lambda state: state.has(ItemName.stage_vile, player))
        set_rule(entrance_crush, lambda state: state.has(ItemName.stage_vile, player))
    elif vile_open == "medals":
        set_rule(entrance_blizzard, lambda state: state.has(ItemName.maverick_medal, player, world.options.vile_medal_count.value))
        set_rule(entrance_volt, lambda state: state.has(ItemName.maverick_medal, player, world.options.vile_medal_count.value))
        set_rule(entrance_crush, lambda state: state.has(ItemName.maverick_medal, player, world.options.vile_medal_count.value))
    elif vile_open == "weapons":
        set_rule(entrance_blizzard, lambda state: state.has_group("Weapons", player, world.options.vile_weapon_count.value))
        set_rule(entrance_volt, lambda state: state.has_group("Weapons", player, world.options.vile_weapon_count.value))
        set_rule(entrance_crush, lambda state: state.has_group("Weapons", player, world.options.vile_weapon_count.value))
    elif vile_open == "armor_upgrades":
        set_rule(entrance_blizzard, lambda state: state.has_group("Armor Upgrades", player, world.options.vile_upgrade_count.value))
        set_rule(entrance_volt, lambda state: state.has_group("Armor Upgrades", player, world.options.vile_upgrade_count.value))
        set_rule(entrance_crush, lambda state: state.has_group("Armor Upgrades", player, world.options.vile_upgrade_count.value))
    elif vile_open == "heart_tanks":
        set_rule(entrance_blizzard, lambda state: state.has(ItemName.heart_tank, player, world.options.vile_heart_tank_count.value))
        set_rule(entrance_volt, lambda state: state.has(ItemName.heart_tank, player, world.options.vile_heart_tank_count.value))
        set_rule(entrance_crush, lambda state: state.has(ItemName.heart_tank, player, world.options.vile_heart_tank_count.value))
    elif vile_open == "sub_tanks":
        set_rule(entrance_blizzard, lambda state: state.has(ItemName.sub_tank, player, world.options.vile_sub_tank_count.value))
        set_rule(entrance_volt, lambda state: state.has(ItemName.sub_tank, player, world.options.vile_sub_tank_count.value))
        set_rule(entrance_crush, lambda state: state.has(ItemName.sub_tank, player, world.options.vile_sub_tank_count.value))

    # Bit & Byte arena entrance rules
    set_rule(multiworld.get_entrance(f"{RegionName.blast_hornet_bit_byte} -> {RegionName.bit_byte}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.blizzard_buffalo_bit_byte} -> {RegionName.bit_byte}", player),
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.toxic_seahorse_bit_byte} -> {RegionName.bit_byte}", player),
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.tunnel_rhino_bit_byte} -> {RegionName.bit_byte}", player),
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.volt_catfish_bit_byte} -> {RegionName.bit_byte}", player),
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.crush_crawfish_bit_byte} -> {RegionName.bit_byte}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.neon_tiger_bit_byte} -> {RegionName.bit_byte}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    set_rule(multiworld.get_entrance(f"{RegionName.gravity_beetle_bit_byte} -> {RegionName.bit_byte}", player), 
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    
    # Set Bit rules
    set_rule(multiworld.get_location(LocationName.bit_defeat, player),
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    set_rule(multiworld.get_location(EventName.bit_defeated, player),
             lambda state: state.has(ItemName.maverick_medal, player, world.options.bit_medal_count.value))
    
    # Set Byte rules
    set_rule(multiworld.get_location(LocationName.byte_defeat, player),
             lambda state: state.has(ItemName.maverick_medal, player, world.options.byte_medal_count.value))
    set_rule(multiworld.get_location(EventName.byte_defeated, player),
             lambda state: state.has(ItemName.maverick_medal, player, world.options.byte_medal_count.value))

    # Set Blizzard Buffalo collectible rules
    set_rule(multiworld.get_location(LocationName.blizzard_buffalo_heart_tank, player),
             lambda state: (
                state.has(ItemName.tornado_fang, player) or
                state.has(ItemName.ride_chimera, player) or
                state.has(ItemName.ride_kangaroo, player)
             ))
    set_rule(multiworld.get_location(LocationName.blizzard_buffalo_sub_tank, player),
             lambda state: state.has(ItemName.third_armor_legs, player, 1))
    
    # Set Toxic Seahorse collectible rules
    set_rule(multiworld.get_location(LocationName.toxic_seahorse_kangaroo_ride, player),
             lambda state: (
                state.has(ItemName.third_armor_legs, player, 1) and
                (
                    state.has(ItemName.ride_frog, player) or 
                    (   
                        state.has(ItemName.frost_shield, player) and
                        state.has(ItemName.third_armor_arms, player, 1)
                    )
                )
             ))
    
    set_rule(multiworld.get_location(LocationName.toxic_seahorse_leg, player),
             lambda state: (
                state.has(ItemName.ride_frog, player) or 
                (   
                    state.has(ItemName.frost_shield, player) and
                    state.has(ItemName.third_armor_arms, player, 1)
                )
             ))
    
    # Set Tunnel Rhino collectible rules
    set_rule(multiworld.get_location(LocationName.tunnel_rhino_heart_tank, player),
             lambda state: (
                state.has(ItemName.third_armor_arms, player, 1) and
                state.has(ItemName.triad_thunder, player)
             ))
    set_rule(multiworld.get_location(LocationName.tunnel_rhino_helmet, player),
             lambda state: (
                state.has(ItemName.third_armor_arms, player, 1) and
                state.has(ItemName.triad_thunder, player)
             ))
    
    # Set Volt Catfish collectible rules
    set_rule(multiworld.get_location(LocationName.volt_catfish_sub_tank, player),
             lambda state: state.has_group("Ride Armors", player, 1))
    set_rule(multiworld.get_location(LocationName.volt_catfish_body, player),
             lambda state: (
                state.has(ItemName.third_armor_arms, player, 1) and
                state.has(ItemName.gravity_well, player)
             ))
    
    # Set Crush Crawfish collectible rules
    set_rule(multiworld.get_location(LocationName.crush_crawfish_heart_tank, player),
             lambda state: state.has_group("Ride Armors", player, 1))
    set_rule(multiworld.get_location(LocationName.crush_crawfish_body, player),
             lambda state: state.has_group("Ride Armors", player, 1))
    set_rule(multiworld.get_location(LocationName.crush_crawfish_hawk_ride, player),
             lambda state: (
                state.has(ItemName.third_armor_arms, player, 1) and
                state.has(ItemName.triad_thunder, player)
             ))
    
    # Set Neon Tiger collectible rules
    set_rule(multiworld.get_location(LocationName.neon_tiger_arms, player),
             lambda state: (
                state.has(ItemName.third_armor_legs, player, 1) and
                state.has(ItemName.tornado_fang, player)
             ))
    
    # Set Gravity Beetle collectible rules
    set_rule(multiworld.get_location(LocationName.gravity_beetle_heart_tank, player),
             lambda state: state.has(EventName.blast_hornet_defeated, player))
    set_rule(multiworld.get_location(LocationName.gravity_beetle_frog_ride, player),
             lambda state: state.has(ItemName.third_armor_legs, player, 1))
    set_rule(multiworld.get_location(LocationName.gravity_beetle_arms, player),
             lambda state: (
                state.has(ItemName.ride_chimera, player) or
                state.has(ItemName.ride_kangaroo, player) or
                state.has(ItemName.ride_hawk, player)
             ))
    
    # Set Blast Hornet collectible rules
    set_rule(multiworld.get_location(LocationName.blast_hornet_heart_tank, player),
             lambda state: state.has(ItemName.third_armor_legs, player, 1))
    set_rule(multiworld.get_location(LocationName.blast_hornet_chimera_ride, player),
             lambda state: state.has(ItemName.tornado_fang, player))
    set_rule(multiworld.get_location(LocationName.blast_hornet_helmet, player),
             lambda state: (
                state.has(ItemName.third_armor_legs, player, 2) or
                state.has(ItemName.ride_hawk, player)
             ))
    
    # Handle bosses weakness
    if world.options.logic_boss_weakness.value:
        add_boss_weakness_logic(world)

    # Z-Saber logic
    if world.options.logic_z_saber != "not_required":
        add_z_saber_logic(world)
        
    # Handle pickupsanity logic
    if world.options.pickupsanity.value:
        add_pickupsanity_logic(world)


def add_boss_weakness_logic(world):
    player = world.player
    multiworld = world.multiworld

    # Set Blizzard Buffalo rules
    set_rule(multiworld.get_location(LocationName.blizzard_buffalo_boss, player),
             lambda state: state.has(ItemName.parasitic_bomb, player))
    set_rule(multiworld.get_location(LocationName.blizzard_buffalo_clear, player),
             lambda state: state.has(ItemName.parasitic_bomb, player))

    # Set Toxic Seahorse rules
    set_rule(multiworld.get_location(LocationName.toxic_seahorse_boss, player),
             lambda state: state.has(ItemName.frost_shield, player))
    set_rule(multiworld.get_location(LocationName.toxic_seahorse_clear, player),
             lambda state: state.has(ItemName.frost_shield, player))
    
    # Set Tunnel Rhino rules
    set_rule(multiworld.get_location(LocationName.tunnel_rhino_boss, player),
             lambda state: state.has(ItemName.acid_burst, player))
    set_rule(multiworld.get_location(LocationName.tunnel_rhino_clear, player),
             lambda state: state.has(ItemName.acid_burst, player))
    
    # Set Volt Catfish rules
    set_rule(multiworld.get_location(LocationName.volt_catfish_boss, player),
             lambda state: state.has(ItemName.tornado_fang, player))
    set_rule(multiworld.get_location(LocationName.volt_catfish_clear, player),
             lambda state: state.has(ItemName.tornado_fang, player))
    
    # Set Crush Crawfish rules
    set_rule(multiworld.get_location(LocationName.crush_crawfish_boss, player),
             lambda state: state.has(ItemName.triad_thunder, player))
    set_rule(multiworld.get_location(LocationName.crush_crawfish_clear, player),
             lambda state: state.has(ItemName.triad_thunder, player))
    
    # Set Neon Tiger rules
    set_rule(multiworld.get_location(LocationName.neon_tiger_boss, player),
             lambda state: state.has(ItemName.spinning_blade, player))
    set_rule(multiworld.get_location(LocationName.neon_tiger_clear, player),
             lambda state: state.has(ItemName.spinning_blade, player))
    
    # Set Gravity Beetle rules
    set_rule(multiworld.get_location(LocationName.gravity_beetle_boss, player),
             lambda state: state.has(ItemName.ray_splasher, player))
    set_rule(multiworld.get_location(LocationName.gravity_beetle_clear, player),
             lambda state: state.has(ItemName.ray_splasher, player))
    
    # Set Blast Hornet rules
    set_rule(multiworld.get_location(LocationName.blast_hornet_boss, player), 
             lambda state: state.has(ItemName.gravity_well, player))
    set_rule(multiworld.get_location(LocationName.blast_hornet_clear, player), 
             lambda state: state.has(ItemName.gravity_well, player)) 
    
    # Set maverick rematch rules
    if world.options.doppler_lab_3_boss_rematch_count.value != 0:
        set_rule(multiworld.get_location(LocationName.doppler_lab_3_blizzard_buffalo, player),
                lambda state: state.has(ItemName.parasitic_bomb, player))
        set_rule(multiworld.get_location(EventName.blizzard_buffalo_rematch, player),
                lambda state: state.has(ItemName.parasitic_bomb, player))
        set_rule(multiworld.get_location(LocationName.doppler_lab_3_toxic_seahorse, player),
                lambda state: state.has(ItemName.frost_shield, player))
        set_rule(multiworld.get_location(EventName.toxic_seahorse_rematch, player),
                lambda state: state.has(ItemName.frost_shield, player))
        set_rule(multiworld.get_location(LocationName.doppler_lab_3_tunnel_rhino, player),
                lambda state: state.has(ItemName.acid_burst, player))
        set_rule(multiworld.get_location(EventName.tunnel_rhino_rematch, player),
                lambda state: state.has(ItemName.acid_burst, player))
        set_rule(multiworld.get_location(LocationName.doppler_lab_3_volt_catfish, player),
                lambda state: state.has(ItemName.tornado_fang, player))
        set_rule(multiworld.get_location(EventName.volt_catfish_rematch, player),
                lambda state: state.has(ItemName.tornado_fang, player))
        set_rule(multiworld.get_location(LocationName.doppler_lab_3_crush_crawfish, player),
                lambda state: state.has(ItemName.triad_thunder, player))
        set_rule(multiworld.get_location(EventName.crush_crawfish_rematch, player),
                lambda state: state.has(ItemName.triad_thunder, player))
        set_rule(multiworld.get_location(LocationName.doppler_lab_3_neon_tiger, player),
                lambda state: state.has(ItemName.spinning_blade, player))
        set_rule(multiworld.get_location(EventName.neon_tiger_rematch, player),
                lambda state: state.has(ItemName.spinning_blade, player))
        set_rule(multiworld.get_location(LocationName.doppler_lab_3_gravity_beetle, player), 
                lambda state: state.has(ItemName.ray_splasher, player))
        set_rule(multiworld.get_location(EventName.gravity_beetle_rematch, player),
                lambda state: state.has(ItemName.ray_splasher, player))
        set_rule(multiworld.get_location(LocationName.doppler_lab_3_blast_hornet, player), 
                lambda state: state.has(ItemName.gravity_well, player))
        set_rule(multiworld.get_location(EventName.blast_hornet_rematch, player),
                lambda state: state.has(ItemName.gravity_well, player))
    
    # Set Bit rules
    add_rule(multiworld.get_location(LocationName.bit_defeat, player), 
             lambda state: (
                state.has(ItemName.frost_shield, player) or
                state.has(ItemName.triad_thunder, player)
             ))
    
    # Set Byte rules
    add_rule(multiworld.get_location(LocationName.byte_defeat, player),
             lambda state: (
                state.has(ItemName.tornado_fang, player) or
                state.has(ItemName.ray_splasher, player)
             ))

    # Set Vile rules
    add_rule(multiworld.get_location(LocationName.vile_stage_boss, player), 
             lambda state: (
                state.has(ItemName.spinning_blade, player) or
                state.has(ItemName.ray_splasher, player)
             ))

    # Set Press Disposer rules
    add_rule(multiworld.get_location(EventName.dr_doppler_lab_1_clear, player),
                lambda state: (
                state.has(ItemName.tornado_fang, player) or
                state.has(ItemName.ray_splasher, player)
            ))
    add_rule(multiworld.get_location(LocationName.doppler_lab_1_boss, player),
                lambda state: (
                state.has(ItemName.tornado_fang, player) or
                state.has(ItemName.ray_splasher, player)
            ))
    # Set Godkarmachine O' Inary rules
    add_rule(multiworld.get_location(EventName.dr_doppler_lab_1_clear, player),
                lambda state: state.has(ItemName.ray_splasher, player))
    add_rule(multiworld.get_location(LocationName.doppler_lab_1_boss, player),
                lambda state: state.has(ItemName.ray_splasher, player))

    if world.options.doppler_lab_2_boss == "volt_kurageil":
        # Set Volt Kurageil rules
        add_rule(multiworld.get_location(EventName.dr_doppler_lab_2_clear, player),
                 lambda state: (
                    state.has(ItemName.frost_shield, player) or
                    state.has(ItemName.triad_thunder, player)
                 ))
        add_rule(multiworld.get_location(LocationName.doppler_lab_2_boss, player),
                 lambda state: (
                    state.has(ItemName.frost_shield, player) or
                    state.has(ItemName.triad_thunder, player)
                 ))
    elif world.options.doppler_lab_2_boss == "vile":
        # Set Vile rematch rules
        add_rule(multiworld.get_location(EventName.dr_doppler_lab_2_clear, player),
                 lambda state: (
                    (
                        state.has(ItemName.parasitic_bomb, player) or 
                        state.has(ItemName.tornado_fang, player)
                    ) and (
                        state.has(ItemName.spinning_blade, player) or
                        state.has(ItemName.ray_splasher, player)
                    )
                 ))
        add_rule(multiworld.get_location(LocationName.doppler_lab_2_boss, player),
                 lambda state: (
                    (
                        state.has(ItemName.parasitic_bomb, player) or 
                        state.has(ItemName.tornado_fang, player)
                    ) and (
                        state.has(ItemName.spinning_blade, player) or
                        state.has(ItemName.ray_splasher, player)
                    )
                 ))
        
    # Set Dr. Doppler rules
    add_rule(multiworld.get_location(LocationName.doppler_lab_3_boss, player),
             lambda state: state.has(ItemName.acid_burst, player))
    add_rule(multiworld.get_location(EventName.dr_doppler_lab_3_clear, player),
             lambda state: state.has(ItemName.acid_burst, player))
    # Set Sigma rules
    set_rule(multiworld.get_location(LocationName.doppler_lab_3_boss, player),
             lambda state: (
                state.has(ItemName.spinning_blade, player) or 
                state.has(ItemName.frost_shield, player)
             ))


def add_z_saber_logic(world):
    player = world.player
    multiworld = world.multiworld

    logic_z_saber = world.options.logic_z_saber
    if logic_z_saber == 0:
        add_rule(multiworld.get_entrance(f"{RegionName.dr_doppler_lab} -> {RegionName.dr_doppler_lab_1}", player),
                 lambda state: state.has(ItemName.z_saber, player))
    elif logic_z_saber == 1:
        add_rule(multiworld.get_entrance(f"{RegionName.dr_doppler_lab_1} -> {RegionName.dr_doppler_lab_2}", player), 
                 lambda state: state.has(ItemName.z_saber, player))
    elif logic_z_saber == 2:
        add_rule(multiworld.get_entrance(f"{RegionName.dr_doppler_lab_2} -> {RegionName.dr_doppler_lab_3}", player), 
                 lambda state: state.has(ItemName.z_saber, player))
    elif logic_z_saber == 3:
        add_rule(multiworld.get_location(LocationName.doppler_lab_3_boss, player), 
                 lambda state: state.has(ItemName.z_saber, player))
    elif logic_z_saber == 4:
        add_rule(multiworld.get_entrance(f"{RegionName.dr_doppler_lab_3_boss} -> {RegionName.dr_doppler_lab_4}", player), 
                 lambda state: state.has(ItemName.z_saber, player))


def add_pickupsanity_logic(world):
    player = world.player
    multiworld = world.multiworld

    # Volt Catfish
    set_rule(multiworld.get_location(LocationName.volt_catfish_energy_2, player),
             lambda state: state.has_group("Ride Armors", player, 1))
    set_rule(multiworld.get_location(LocationName.volt_catfish_energy_3, player),
             lambda state: state.has_group("Ride Armors", player, 1))
    set_rule(multiworld.get_location(LocationName.volt_catfish_hp_3, player),
             lambda state: state.has_group("Ride Armors", player, 1))
    set_rule(multiworld.get_location(LocationName.volt_catfish_hp_4, player),
             lambda state: state.has_group("Ride Armors", player, 1))
    set_rule(multiworld.get_location(LocationName.volt_catfish_hp_5, player),
             lambda state: state.has_group("Ride Armors", player, 1))
    
    # Crush Crawfish
    set_rule(multiworld.get_location(LocationName.crush_crawfish_1up_1, player),
             lambda state: state.has(ItemName.tornado_fang, player))
    set_rule(multiworld.get_location(LocationName.crush_crawfish_1up_2, player),
             lambda state: state.has(ItemName.tornado_fang, player))
    
