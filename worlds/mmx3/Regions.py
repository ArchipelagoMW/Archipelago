import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import MMX3Location
from .Names import LocationName, ItemName
from worlds.generic.Rules import add_rule, set_rule
from worlds.AutoWorld import World


def create_regions(multiworld: MultiWorld, player: int, world: World, active_locations):

    logic_z_saber = world.options.logic_z_saber.value

    menu_region = create_region(multiworld, player, active_locations, 'Menu', None)

    intro_stage_region = create_region(multiworld, player, active_locations, LocationName.intro_stage_region, None)
    blizzard_buffalo_region = create_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, None)
    toxic_seahorse_region = create_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, None)
    tunnel_rhino_region = create_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, None)
    volt_catfish_region = create_region(multiworld, player, active_locations, LocationName.volt_catfish_region, None)
    crush_crawfish_region = create_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, None)
    neon_tiger_region = create_region(multiworld, player, active_locations, LocationName.neon_tiger_region, None)
    gravity_beetle_region = create_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, None)
    blast_hornet_region = create_region(multiworld, player, active_locations, LocationName.blast_hornet_region, None)
    vile_region = create_region(multiworld, player, active_locations, LocationName.vile_region, None)
    bit_byte_region = create_region(multiworld, player, active_locations, LocationName.bit_byte_region, None)
    dr_doppler_lab_region = create_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_region, None)
    dr_doppler_lab_1_region = create_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, None)
    dr_doppler_lab_2_region = create_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_2_region, None)
    dr_doppler_lab_3_region = create_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, None)
    dr_doppler_lab_4_region = create_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_4_region, None)

    multiworld.regions += [
        menu_region,
        intro_stage_region,
        blizzard_buffalo_region,
        toxic_seahorse_region, 
        tunnel_rhino_region,
        volt_catfish_region,
        crush_crawfish_region,
        neon_tiger_region, 
        gravity_beetle_region,
        blast_hornet_region, 
        vile_region, 
        bit_byte_region, 
        dr_doppler_lab_region,
        dr_doppler_lab_1_region,
        dr_doppler_lab_2_region,
        dr_doppler_lab_3_region,
        dr_doppler_lab_4_region
    ]


    # Hunter Base
    add_location_to_region(multiworld, player, active_locations, LocationName.intro_stage_region, LocationName.intro_stage_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.intro_stage_region, LocationName.intro_stage_mini_boss)


    # Blizzard Buffalo
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_boss,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.parasitic_bomb, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_clear,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.parasitic_bomb, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_heart_tank,
        lambda state: (
                state.has(ItemName.tornado_fang, player) or
                state.has(ItemName.ride_chimera, player)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_sub_tank,
        lambda state: (
                state.has(ItemName.third_armor_legs, player, 1)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_legs)


    # Toxic Seahorse
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_boss,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.frost_shield, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_clear,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.frost_shield, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_mini_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_kangaroo_ride,
        lambda state: (
                (
                    state.has(ItemName.ride_frog, player)
                ) or (   
                    state.has(ItemName.frost_shield, player) and
                    state.has(ItemName.third_armor_arms, player, 1)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_leg,
        lambda state: (
                (
                    state.has(ItemName.ride_frog, player)
                ) or (   
                    state.has(ItemName.frost_shield, player) and
                    state.has(ItemName.third_armor_arms, player, 1)
                )
            ))


    # Tunnel Rhino
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_boss,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.acid_burst, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_clear,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.acid_burst, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_mini_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_heart_tank,
        lambda state: (
                state.has(ItemName.third_armor_arms, player, 1) and
                state.has(ItemName.triad_thunder, player)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_sub_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_helmet,
        lambda state: (
                state.has(ItemName.third_armor_arms, player, 1) and
                state.has(ItemName.triad_thunder, player)
            ))


    # Volt Catfish
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_boss,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.tornado_fang, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_clear,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.tornado_fang, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_sub_tank,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_body,
        lambda state: (
                state.has(ItemName.third_armor_arms, player, 1) and
                state.has(ItemName.gravity_well, player)
            ))


    # Crush Crawfish
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_boss,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.triad_thunder, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_clear,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.triad_thunder, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_heart_tank,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_hawk_ride,
        lambda state: (
                state.has(ItemName.third_armor_arms, player, 1) and
                state.has(ItemName.triad_thunder, player)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_body,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))


    # Neon Tiger
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_boss,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.spinning_blade, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_clear,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.spinning_blade, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_mini_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_sub_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_arms,
        lambda state: (
                state.has(ItemName.tornado_fang, player)
            ))


    # Gravity Beetle
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_boss,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.ray_splasher, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_clear,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.ray_splasher, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_heart_tank,
        lambda state: (
                state.has(ItemName.blast_hornet_core, player)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_frog_ride,
        lambda state: (
                state.has(ItemName.third_armor_legs, player, 1)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_arms,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))


    # Blast Hornet
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_boss,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.gravity_well, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_clear,
        lambda state: (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    state.has(ItemName.gravity_well, player)
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_mini_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_heart_tank,
        lambda state: (
                state.has(ItemName.third_armor_legs, player, 1)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_chimera_ride,
        lambda state: (
                state.has(ItemName.tornado_fang, player)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_helmet,
        lambda state: (
                state.has(ItemName.third_armor_legs, player, 2) or
                state.has(ItemName.ride_chimera, player) or
                state.has(ItemName.ride_hawk, player) or
                state.has(ItemName.ride_kangaroo, player)
            ))


    # Dr. Doppler Lab 1
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, LocationName.doppler_lab_1_clear,
        lambda state:  (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    (
                        state.has(ItemName.tornado_fang, player) or
                        state.has(ItemName.ray_splasher, player) or
                        state.has(ItemName.parasitic_bomb, player)
                    )
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, LocationName.doppler_lab_1_boss,
        lambda state:  (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    (
                        state.has(ItemName.tornado_fang, player) or
                        state.has(ItemName.ray_splasher, player) or
                        state.has(ItemName.parasitic_bomb, player)
                    )
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, LocationName.doppler_lab_1_mini_boss)


    # Dr. Doppler Lab 2
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_2_region, LocationName.doppler_lab_2_clear,
        lambda state:  (
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    (
                        state.has(ItemName.triad_thunder, player) or
                        state.has(ItemName.frost_shield, player) or
                        state.has(ItemName.tornado_fang, player) or
                        state.has(ItemName.parasitic_bomb, player)
                    )
                )
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_2_region, LocationName.doppler_lab_2_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_2_region, LocationName.doppler_lab_2_mini_boss)


    # Dr. Doppler Lab 3
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_boss,
            lambda state: (
                    check_z_saber(state, player, logic_z_saber, 3)
                ))
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_clear,
            lambda state: (
                    check_z_saber(state, player, logic_z_saber, 3)
                ))
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_blizzard_buffalo)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_toxic_seahorse)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_tunnel_rhino)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_volt_catfish)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_crush_crawfish)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_neon_tiger)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_gravity_beetle)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_blast_hornet)


    # Dr. Doppler Lab 4
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_4_region, LocationName.victory)


    # Vile
    add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_boss)
    

    # Bit & Byte
    add_location_to_region(multiworld, player, active_locations, LocationName.bit_byte_region, LocationName.bit_defeat,
        lambda state: (
                state.has(ItemName.frost_shield, player) or
                state.has(ItemName.triad_thunder, player)
            ))
    add_location_to_region(multiworld, player, active_locations, LocationName.bit_byte_region, LocationName.byte_defeat,
        lambda state: (
                state.has(ItemName.maverick_medal, player, 6) and
                (
                    state.has(ItemName.tornado_fang, player) or
                    state.has(ItemName.ray_splasher, player)
                )
            ))


    if world.options.pickupsanity:
    # Hunter Base
        add_location_to_region(multiworld, player, active_locations, LocationName.intro_stage_region, LocationName.intro_stage_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.intro_stage_region, LocationName.intro_stage_hp_2)

        # Blizzard Buffalo
        add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_hp_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_hp_3)
        add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_hp_4)
        add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_hp_5)

        # Toxic Seahorse
        add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_hp_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_hp_3)

        # Tunnel Rhino
        add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_energy_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_hp_1)

        # Volt Catfish
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_energy_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_energy_2,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_energy_3,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_3,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_4,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_5,
        lambda state: (
                state.has(ItemName.ride_chimera, player)
            ))

        # Crush Crawfish
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_1up_1,
        lambda state: (
                state.has(ItemName.tornado_fang, player)
            ))
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_1up_2,
        lambda state: (
                state.has(ItemName.tornado_fang, player)
            ))
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_energy_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_hp_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_hp_3)
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_hp_4)
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_hp_5)
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_hp_6)

        # Neon Tiger
        add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_hp_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_hp_3)

        # Gravity Beetle
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_1up)
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_energy_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_energy_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_hp_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_hp_3)
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_hp_4)
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_hp_5)
        add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_hp_6)

        # Blast Hornet
        add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_hp_2)

        # Dr. Doppler Lab 1
        add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, LocationName.doppler_lab_1_energy)
        add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, LocationName.doppler_lab_1_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, LocationName.doppler_lab_1_hp_2)
        
        # Dr. Doppler Lab 2

        # Dr. Doppler Lab 3
        add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_hp)

        # Dr. Doppler Lab 4

        # Vile
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_energy)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_1up)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_3)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_4)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_5)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_6)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_7)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_8)
        add_location_to_region(multiworld, player, active_locations, LocationName.vile_region, LocationName.vile_stage_hp_9)
        

def connect_regions(multiworld: MultiWorld, player: int, world: World):
    names: typing.Dict[str, int] = {}

    logic_z_saber = world.options.logic_z_saber.value

    connect(multiworld, player, names, "Menu", LocationName.intro_stage_region)

    # Connect Hunter Base
    connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.blizzard_buffalo_region,
            lambda state: (state.has(ItemName.stage_blizzard_buffalo, player)))
    connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.toxic_seahorse_region,
            lambda state: (state.has(ItemName.stage_toxic_seahorse, player)))
    connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.tunnel_rhino_region,
            lambda state: (state.has(ItemName.stage_tunnel_rhino, player)))
    connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.volt_catfish_region,
            lambda state: (state.has(ItemName.stage_volt_catfish, player)))
    connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.crush_crawfish_region,
            lambda state: (state.has(ItemName.stage_crush_crawfish, player)))
    connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.neon_tiger_region,
            lambda state: (state.has(ItemName.stage_neon_tiger, player)))
    connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.gravity_beetle_region,
            lambda state: (state.has(ItemName.stage_gravity_beetle, player)))
    connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.blast_hornet_region,
            lambda state: (state.has(ItemName.stage_blast_hornet, player)))
    
    # Connect Vile
    connect(multiworld, player, names, LocationName.blizzard_buffalo_region, LocationName.vile_region,
            lambda state: (
                state.has(ItemName.stage_blizzard_buffalo, player) and
                state.has(ItemName.maverick_medal, player, 2)
            ))
    connect(multiworld, player, names, LocationName.toxic_seahorse_region, LocationName.vile_region,
            lambda state: (
                state.has(ItemName.stage_toxic_seahorse, player) and
                state.has(ItemName.maverick_medal, player, 2)
            ))
    connect(multiworld, player, names, LocationName.crush_crawfish_region, LocationName.vile_region,
            lambda state: (
                state.has(ItemName.stage_crush_crawfish, player) and
                state.has(ItemName.maverick_medal, player, 2)
            ))
    
    # Connect Bit & Byte
    connect(multiworld, player, names, LocationName.blizzard_buffalo_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    connect(multiworld, player, names, LocationName.toxic_seahorse_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    connect(multiworld, player, names, LocationName.tunnel_rhino_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    connect(multiworld, player, names, LocationName.volt_catfish_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    connect(multiworld, player, names, LocationName.crush_crawfish_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    connect(multiworld, player, names, LocationName.neon_tiger_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    connect(multiworld, player, names, LocationName.gravity_beetle_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    connect(multiworld, player, names, LocationName.blast_hornet_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    
    # Connect Dr. Doppler Lab
    if world.options.doppler_open == "multiworld":
        connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.dr_doppler_lab_region,
                lambda state: (
                    state.has(ItemName.stage_doppler_lab, player)
                ))
    elif world.options.doppler_open == "medals":
        connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.dr_doppler_lab_region,
                lambda state: (
                    state.has(ItemName.maverick_medal, player, world.options.doppler_medal_count.value)
                ))
    elif world.options.doppler_open == "weapons":
        connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.dr_doppler_lab_region,
                lambda state: (
                    check_z_saber(state, player, logic_z_saber, 0) and
                    state.has_group("BossWeapons", player, world.options.doppler_weapon_count.value)
                ))
    elif world.options.doppler_open == "armor_upgrades":
        connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.dr_doppler_lab_region,
                lambda state: (
                    state.has_group("ArmorUpgrades", player, world.options.doppler_upgrade_count.value)
                ))
    elif world.options.doppler_open == "heart_tanks":
        connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.dr_doppler_lab_region,
                lambda state: (
                    state.has(ItemName.heart_tank, player, world.options.doppler_heart_tank_count.value)
                ))
    elif world.options.doppler_open == "sub_tanks":
        connect(multiworld, player, names, LocationName.intro_stage_region, LocationName.dr_doppler_lab_region,
                lambda state: (
                    state.has(ItemName.sub_tank, player, world.options.doppler_sub_tank_count.value)
                ))

    # Connect Dr. Doppler Lab levels
    connect(multiworld, player, names, LocationName.dr_doppler_lab_region, LocationName.dr_doppler_lab_1_region,
            lambda state: (
                check_z_saber(state, player, logic_z_saber, 0) and
                not world.options.logic_boss_weakness.value
                or (
                    world.options.logic_boss_weakness.value and
                    (
                        state.has(ItemName.tornado_fang, player) or
                        state.has(ItemName.ray_splasher, player) or
                        state.has(ItemName.parasitic_bomb, player)
                    )
                )
            ))
    connect(multiworld, player, names, LocationName.dr_doppler_lab_1_region, LocationName.dr_doppler_lab_2_region,
            lambda state: (
                    check_z_saber(state, player, logic_z_saber, 1) and
                    not world.options.logic_boss_weakness.value
                    or (
                        world.options.logic_boss_weakness.value and
                        (
                            state.has(ItemName.triad_thunder, player) or
                            state.has(ItemName.frost_shield, player) or
                            state.has(ItemName.tornado_fang, player) or
                            state.has(ItemName.parasitic_bomb, player)
                        )
                    )
                ))
    connect(multiworld, player, names, LocationName.dr_doppler_lab_2_region, LocationName.dr_doppler_lab_3_region,
            lambda state: (
                    check_z_saber(state, player, logic_z_saber, 2)
                ))
    connect(multiworld, player, names, LocationName.dr_doppler_lab_3_region, LocationName.dr_doppler_lab_4_region,
            lambda state: (
                    check_z_saber(state, player, logic_z_saber, 4)
                ))
    
    connect(multiworld, player, names, LocationName.blast_hornet_region, LocationName.bit_byte_region,
            lambda state: (state.has(ItemName.maverick_medal, player, 2)))
    

def check_z_saber(state: "CollectionState", player: int, logic_z_saber: int, option_level: int) -> bool:
    if logic_z_saber >= option_level:
        return state.has(ItemName.z_saber, player)
    else:
        return True
    
def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = MMX3Location(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret


def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str,
                           rule: typing.Optional[typing.Callable] = None):
    region = multiworld.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = MMX3Location(player, location_name, loc_id, region)
        region.locations.append(location)
        if rule:
            add_rule(location, rule)


def connect(multiworld: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = multiworld.get_region(source, player)
    target_region = multiworld.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
