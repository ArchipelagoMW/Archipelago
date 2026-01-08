import typing

from BaseClasses import CollectionState, MultiWorld, Region, Entrance, ItemClassification
from .Locations import MMX3Location
from .Items import MMX3Item
from .Names import LocationName, ItemName, RegionName, EventName
from worlds.AutoWorld import World


def create_regions(multiworld: MultiWorld, player: int, world: World, active_locations):
    menu = create_region(multiworld, player, active_locations, 'Menu')

    intro_stage = create_region(multiworld, player, active_locations, RegionName.intro_stage)

    blizzard_buffalo = create_region(multiworld, player, active_locations, RegionName.blizzard_buffalo)
    blizzard_buffalo_start = create_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_start)
    blizzard_buffalo_bit_byte = create_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_bit_byte)
    blizzard_buffalo_after_bit_byte = create_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_after_bit_byte)
    blizzard_buffalo_boss = create_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_boss)

    toxic_seahorse = create_region(multiworld, player, active_locations, RegionName.toxic_seahorse)
    toxic_seahorse_start = create_region(multiworld, player, active_locations, RegionName.toxic_seahorse_start)
    toxic_seahorse_bit_byte = create_region(multiworld, player, active_locations, RegionName.toxic_seahorse_bit_byte)
    toxic_seahorse_underwater = create_region(multiworld, player, active_locations, RegionName.toxic_seahorse_underwater)
    toxic_seahorse_hootareca = create_region(multiworld, player, active_locations, RegionName.toxic_seahorse_hootareca)
    toxic_seahorse_dam = create_region(multiworld, player, active_locations, RegionName.toxic_seahorse_dam)
    toxic_seahorse_before_boss = create_region(multiworld, player, active_locations, RegionName.toxic_seahorse_before_boss)
    toxic_seahorse_boss = create_region(multiworld, player, active_locations, RegionName.toxic_seahorse_boss)

    tunnel_rhino = create_region(multiworld, player, active_locations, RegionName.tunnel_rhino)
    tunnel_rhino_start = create_region(multiworld, player, active_locations, RegionName.tunnel_rhino_start)
    tunnel_rhino_bit_byte = create_region(multiworld, player, active_locations, RegionName.tunnel_rhino_bit_byte)
    tunnel_rhino_wall_jump = create_region(multiworld, player, active_locations, RegionName.tunnel_rhino_wall_jump)
    tunnel_rhino_hell_crusher = create_region(multiworld, player, active_locations, RegionName.tunnel_rhino_hell_crusher)
    tunnel_rhino_climbing = create_region(multiworld, player, active_locations, RegionName.tunnel_rhino_climbing)
    tunnel_rhino_boss = create_region(multiworld, player, active_locations, RegionName.tunnel_rhino_boss)

    volt_catfish = create_region(multiworld, player, active_locations, RegionName.volt_catfish)
    volt_catfish_start = create_region(multiworld, player, active_locations, RegionName.volt_catfish_start)
    volt_catfish_bit_byte = create_region(multiworld, player, active_locations, RegionName.volt_catfish_bit_byte)
    volt_catfish_inside = create_region(multiworld, player, active_locations, RegionName.volt_catfish_inside)
    volt_catfish_boss = create_region(multiworld, player, active_locations, RegionName.volt_catfish_boss)

    crush_crawfish = create_region(multiworld, player, active_locations, RegionName.crush_crawfish)
    crush_crawfish_start = create_region(multiworld, player, active_locations, RegionName.crush_crawfish_start)
    crush_crawfish_bit_byte = create_region(multiworld, player, active_locations, RegionName.crush_crawfish_bit_byte)
    crush_crawfish_inside = create_region(multiworld, player, active_locations, RegionName.crush_crawfish_inside)
    crush_crawfish_boss = create_region(multiworld, player, active_locations, RegionName.crush_crawfish_boss)

    neon_tiger = create_region(multiworld, player, active_locations, RegionName.neon_tiger)
    neon_tiger_start = create_region(multiworld, player, active_locations, RegionName.neon_tiger_start)
    neon_tiger_worm = create_region(multiworld, player, active_locations, RegionName.neon_tiger_worm)
    neon_tiger_bit_byte = create_region(multiworld, player, active_locations, RegionName.neon_tiger_bit_byte)
    neon_tiger_hill = create_region(multiworld, player, active_locations, RegionName.neon_tiger_hill)
    neon_tiger_boss = create_region(multiworld, player, active_locations, RegionName.neon_tiger_boss)

    gravity_beetle = create_region(multiworld, player, active_locations, RegionName.gravity_beetle)
    gravity_beetle_start = create_region(multiworld, player, active_locations, RegionName.gravity_beetle_start)
    gravity_beetle_bit_byte = create_region(multiworld, player, active_locations, RegionName.gravity_beetle_bit_byte)
    gravity_beetle_outside = create_region(multiworld, player, active_locations, RegionName.gravity_beetle_outside)
    gravity_beetle_inside = create_region(multiworld, player, active_locations, RegionName.gravity_beetle_inside)
    gravity_beetle_boss = create_region(multiworld, player, active_locations, RegionName.gravity_beetle_boss)

    blast_hornet = create_region(multiworld, player, active_locations, RegionName.blast_hornet)
    blast_hornet_start = create_region(multiworld, player, active_locations, RegionName.blast_hornet_start)
    blast_hornet_conveyors = create_region(multiworld, player, active_locations, RegionName.blast_hornet_conveyors)
    blast_hornet_shurikein = create_region(multiworld, player, active_locations, RegionName.blast_hornet_shurikein)
    blast_hornet_outside = create_region(multiworld, player, active_locations, RegionName.blast_hornet_outside)
    blast_hornet_bit_byte = create_region(multiworld, player, active_locations, RegionName.blast_hornet_bit_byte)
    blast_hornet_boss = create_region(multiworld, player, active_locations, RegionName.blast_hornet_boss)

    vile = create_region(multiworld, player, active_locations, RegionName.vile)
    vile_before = create_region(multiworld, player, active_locations, RegionName.vile_before)
    vile_boss = create_region(multiworld, player, active_locations, RegionName.vile_boss)
    vile_after = create_region(multiworld, player, active_locations, RegionName.vile_after)

    dr_doppler_lab = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab)
    dr_doppler_lab_1 = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_1)
    dr_doppler_lab_2 = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_2)
    dr_doppler_lab_3 = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3)
    dr_doppler_lab_3_rematches = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches)
    dr_doppler_lab_3_after_rematches = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_after_rematches)
    dr_doppler_lab_3_boss = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_boss)
    dr_doppler_lab_4 = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_4)
    dr_doppler_lab_4_boss = create_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_4_boss)

    bit_byte = create_region(multiworld, player, active_locations, RegionName.bit_byte)

    multiworld.regions += [
        menu,
        intro_stage,
        blizzard_buffalo,
        blizzard_buffalo_start,
        blizzard_buffalo_bit_byte,
        blizzard_buffalo_after_bit_byte,
        blizzard_buffalo_boss,
        toxic_seahorse,
        toxic_seahorse_start,
        toxic_seahorse_bit_byte,
        toxic_seahorse_underwater,
        toxic_seahorse_hootareca,
        toxic_seahorse_dam,
        toxic_seahorse_before_boss,
        toxic_seahorse_boss,
        tunnel_rhino,
        tunnel_rhino_start,
        tunnel_rhino_bit_byte,
        tunnel_rhino_wall_jump,
        tunnel_rhino_hell_crusher,
        tunnel_rhino_climbing,
        tunnel_rhino_boss,
        volt_catfish,
        volt_catfish_start,
        volt_catfish_bit_byte,
        volt_catfish_inside,
        volt_catfish_boss,
        crush_crawfish,
        crush_crawfish_start,
        crush_crawfish_bit_byte,
        crush_crawfish_inside,
        crush_crawfish_boss,
        neon_tiger,
        neon_tiger_start,
        neon_tiger_worm,
        neon_tiger_bit_byte,
        neon_tiger_hill,
        neon_tiger_boss,
        gravity_beetle,
        gravity_beetle_start,
        gravity_beetle_bit_byte,
        gravity_beetle_outside,
        gravity_beetle_inside,
        gravity_beetle_boss,
        blast_hornet,
        blast_hornet_start,
        blast_hornet_conveyors,
        blast_hornet_shurikein,
        blast_hornet_outside,
        blast_hornet_bit_byte,
        blast_hornet_boss,
        vile,
        vile_before,
        vile_boss,
        vile_after,
        dr_doppler_lab,
        dr_doppler_lab_1,
        dr_doppler_lab_2,
        dr_doppler_lab_3,
        dr_doppler_lab_3_rematches,
        dr_doppler_lab_3_after_rematches,
        dr_doppler_lab_3_boss,
        dr_doppler_lab_4,
        dr_doppler_lab_4_boss,
        bit_byte,
    ]

    # Hunter Base
    add_location_to_region(multiworld, player, active_locations, RegionName.intro_stage, LocationName.intro_stage_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.intro_stage, LocationName.intro_stage_mini_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.intro_stage, LocationName.intro_stage_clear)

    # Blizzard Buffalo
    add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_start, LocationName.blizzard_buffalo_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_after_bit_byte, LocationName.blizzard_buffalo_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_after_bit_byte, LocationName.blizzard_buffalo_legs)
    add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_boss, LocationName.blizzard_buffalo_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_boss, LocationName.blizzard_buffalo_clear)

    # Toxic Seahorse
    add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_start, LocationName.toxic_seahorse_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_underwater, LocationName.toxic_seahorse_leg)
    add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_underwater, LocationName.toxic_seahorse_kangaroo_ride)
    add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_hootareca, LocationName.toxic_seahorse_mini_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_boss, LocationName.toxic_seahorse_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_boss, LocationName.toxic_seahorse_clear)

    # Tunnel Rhino
    add_location_to_region(multiworld, player, active_locations, RegionName.tunnel_rhino_start, LocationName.tunnel_rhino_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.tunnel_rhino_start, LocationName.tunnel_rhino_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.tunnel_rhino_wall_jump, LocationName.tunnel_rhino_helmet)
    add_location_to_region(multiworld, player, active_locations, RegionName.tunnel_rhino_hell_crusher, LocationName.tunnel_rhino_mini_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.tunnel_rhino_boss, LocationName.tunnel_rhino_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.tunnel_rhino_boss, LocationName.tunnel_rhino_clear)

    # Volt Catfish
    add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_start, LocationName.volt_catfish_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_start, LocationName.volt_catfish_body)
    add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_inside, LocationName.volt_catfish_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_boss, LocationName.volt_catfish_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_boss, LocationName.volt_catfish_clear)

    # Crush Crawfish
    add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_start, LocationName.crush_crawfish_hawk_ride)
    add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_start, LocationName.crush_crawfish_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_start, LocationName.crush_crawfish_body)
    add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_boss, LocationName.crush_crawfish_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_boss, LocationName.crush_crawfish_clear)

    # Neon Tiger
    add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_start, LocationName.neon_tiger_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_start, LocationName.neon_tiger_arms)
    add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_worm, LocationName.neon_tiger_mini_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_hill, LocationName.neon_tiger_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_boss, LocationName.neon_tiger_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_boss, LocationName.neon_tiger_clear)

    # Gravity Beetle
    add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_start, LocationName.gravity_beetle_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_start, LocationName.gravity_beetle_frog_ride)
    add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_inside, LocationName.gravity_beetle_arms)
    add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_boss, LocationName.gravity_beetle_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_boss, LocationName.gravity_beetle_clear)

    # Blast Hornet
    add_location_to_region(multiworld, player, active_locations, RegionName.blast_hornet_start, LocationName.blast_hornet_helmet)
    add_location_to_region(multiworld, player, active_locations, RegionName.blast_hornet_shurikein, LocationName.blast_hornet_mini_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.blast_hornet_outside, LocationName.blast_hornet_chimera_ride)
    add_location_to_region(multiworld, player, active_locations, RegionName.blast_hornet_outside, LocationName.blast_hornet_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.blast_hornet_boss, LocationName.blast_hornet_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.blast_hornet_boss, LocationName.blast_hornet_clear)
    add_event_to_region(multiworld, player, RegionName.blast_hornet_boss, EventName.blast_hornet_defeated)

    # Dr. Doppler Lab 1
    add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_1, LocationName.doppler_lab_1_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_1, LocationName.doppler_lab_1_mini_boss)
    add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_1, EventName.dr_doppler_lab_1_clear)

    # Dr. Doppler Lab 2
    add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_2, LocationName.doppler_lab_2_boss)
    #add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_2, LocationName.doppler_lab_2_mini_boss)
    add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_2, EventName.dr_doppler_lab_2_clear)

    # Dr. Doppler Lab 3
    if world.options.doppler_lab_3_boss_rematch_count.value > 0:
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches, LocationName.doppler_lab_3_blizzard_buffalo)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches, LocationName.doppler_lab_3_toxic_seahorse)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches, LocationName.doppler_lab_3_tunnel_rhino)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches, LocationName.doppler_lab_3_volt_catfish)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches, LocationName.doppler_lab_3_crush_crawfish)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches, LocationName.doppler_lab_3_neon_tiger)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches, LocationName.doppler_lab_3_gravity_beetle)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_rematches, LocationName.doppler_lab_3_blast_hornet)
        add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_rematches, EventName.blizzard_buffalo_rematch, EventName.boss_rematch_clear)
        add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_rematches, EventName.toxic_seahorse_rematch, EventName.boss_rematch_clear)
        add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_rematches, EventName.tunnel_rhino_rematch, EventName.boss_rematch_clear)
        add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_rematches, EventName.volt_catfish_rematch, EventName.boss_rematch_clear)
        add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_rematches, EventName.crush_crawfish_rematch, EventName.boss_rematch_clear)
        add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_rematches, EventName.neon_tiger_rematch, EventName.boss_rematch_clear)
        add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_rematches, EventName.gravity_beetle_rematch, EventName.boss_rematch_clear)
        add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_rematches, EventName.blast_hornet_rematch, EventName.boss_rematch_clear)
        
    add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_boss, LocationName.doppler_lab_3_boss)
    add_event_to_region(multiworld, player, RegionName.dr_doppler_lab_3_boss, EventName.dr_doppler_lab_3_clear)

    # Dr. Doppler Lab 4
    add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_4_boss, LocationName.victory)

    # Vile
    add_location_to_region(multiworld, player, active_locations, RegionName.vile_boss, LocationName.vile_stage_boss)
    add_event_to_region(multiworld, player, RegionName.vile_boss, EventName.vile_defeated)
    
    # Bit & Byte
    add_location_to_region(multiworld, player, active_locations, RegionName.bit_byte, LocationName.bit_defeat)
    add_location_to_region(multiworld, player, active_locations, RegionName.bit_byte, LocationName.byte_defeat)
    add_event_to_region(multiworld, player, RegionName.bit_byte, EventName.bit_defeated)
    add_event_to_region(multiworld, player, RegionName.bit_byte, EventName.byte_defeated)

    if world.options.pickupsanity:
        # Hunter Base
        add_location_to_region(multiworld, player, active_locations, RegionName.intro_stage, LocationName.intro_stage_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.intro_stage, LocationName.intro_stage_hp_2)

        # Blizzard Buffalo
        add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_start, LocationName.blizzard_buffalo_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_start, LocationName.blizzard_buffalo_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_after_bit_byte, LocationName.blizzard_buffalo_hp_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_after_bit_byte, LocationName.blizzard_buffalo_hp_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.blizzard_buffalo_after_bit_byte, LocationName.blizzard_buffalo_hp_5)

        # Toxic Seahorse
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_start, LocationName.toxic_seahorse_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_start, LocationName.toxic_seahorse_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_seahorse_dam, LocationName.toxic_seahorse_hp_3)

        # Tunnel Rhino
        add_location_to_region(multiworld, player, active_locations, RegionName.tunnel_rhino_start, LocationName.tunnel_rhino_energy_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.tunnel_rhino_wall_jump, LocationName.tunnel_rhino_hp_1)

        # Volt Catfish
        add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_start, LocationName.volt_catfish_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_start, LocationName.volt_catfish_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_inside, LocationName.volt_catfish_hp_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_inside, LocationName.volt_catfish_hp_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_inside, LocationName.volt_catfish_energy_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_inside, LocationName.volt_catfish_energy_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_inside, LocationName.volt_catfish_hp_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.volt_catfish_inside, LocationName.volt_catfish_energy_3)

        # Crush Crawfish
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_start, LocationName.crush_crawfish_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_start, LocationName.crush_crawfish_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_inside, LocationName.crush_crawfish_hp_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_inside, LocationName.crush_crawfish_hp_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_inside, LocationName.crush_crawfish_energy_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_inside, LocationName.crush_crawfish_hp_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_inside, LocationName.crush_crawfish_hp_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_inside, LocationName.crush_crawfish_1up_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.crush_crawfish_inside, LocationName.crush_crawfish_1up_2)

        # Neon Tiger
        add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_start, LocationName.neon_tiger_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_start, LocationName.neon_tiger_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.neon_tiger_start, LocationName.neon_tiger_hp_3)

        # Gravity Beetle
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_start, LocationName.gravity_beetle_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_outside, LocationName.gravity_beetle_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_outside, LocationName.gravity_beetle_hp_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_outside, LocationName.gravity_beetle_energy_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_outside, LocationName.gravity_beetle_hp_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_outside, LocationName.gravity_beetle_1up)
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_outside, LocationName.gravity_beetle_energy_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_outside, LocationName.gravity_beetle_hp_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.gravity_beetle_inside, LocationName.gravity_beetle_hp_6)

        # Blast Hornet
        add_location_to_region(multiworld, player, active_locations, RegionName.blast_hornet_conveyors, LocationName.blast_hornet_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.blast_hornet_outside, LocationName.blast_hornet_hp_2)

        # Dr. Doppler Lab 1
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_1, LocationName.doppler_lab_1_energy)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_1, LocationName.doppler_lab_1_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_1, LocationName.doppler_lab_1_hp_2)
        
        # Dr. Doppler Lab 3
        add_location_to_region(multiworld, player, active_locations, RegionName.dr_doppler_lab_3_after_rematches, LocationName.doppler_lab_3_hp)

        # Vile
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_before, LocationName.vile_stage_hp_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_before, LocationName.vile_stage_hp_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_before, LocationName.vile_stage_hp_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_before, LocationName.vile_stage_hp_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_before, LocationName.vile_stage_energy)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_after, LocationName.vile_stage_1up)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_after, LocationName.vile_stage_hp_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_after, LocationName.vile_stage_hp_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_after, LocationName.vile_stage_hp_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_after, LocationName.vile_stage_hp_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.vile_after, LocationName.vile_stage_hp_9)
        

def connect_regions(world: World):
    connect(world, "Menu", RegionName.intro_stage)

    # Connect Hunter Base
    connect(world, RegionName.intro_stage, RegionName.blizzard_buffalo)
    connect(world, RegionName.intro_stage, RegionName.toxic_seahorse)
    connect(world, RegionName.intro_stage, RegionName.tunnel_rhino)
    connect(world, RegionName.intro_stage, RegionName.volt_catfish)
    connect(world, RegionName.intro_stage, RegionName.crush_crawfish)
    connect(world, RegionName.intro_stage, RegionName.neon_tiger)
    connect(world, RegionName.intro_stage, RegionName.gravity_beetle)
    connect(world, RegionName.intro_stage, RegionName.blast_hornet)

    # Connect Blizzard Buffalo
    connect(world, RegionName.blizzard_buffalo, RegionName.blizzard_buffalo_start)
    connect(world, RegionName.blizzard_buffalo_start, RegionName.blizzard_buffalo_bit_byte)
    connect(world, RegionName.blizzard_buffalo_bit_byte, RegionName.bit_byte)
    connect(world, RegionName.blizzard_buffalo_bit_byte, RegionName.blizzard_buffalo_after_bit_byte)
    connect(world, RegionName.blizzard_buffalo_after_bit_byte, RegionName.blizzard_buffalo_boss)

    # Connect Toxic Seahorse
    connect(world, RegionName.toxic_seahorse, RegionName.toxic_seahorse_start)
    connect(world, RegionName.toxic_seahorse_start, RegionName.toxic_seahorse_bit_byte)
    connect(world, RegionName.toxic_seahorse_bit_byte, RegionName.bit_byte)
    connect(world, RegionName.toxic_seahorse_bit_byte, RegionName.toxic_seahorse_underwater)
    connect(world, RegionName.toxic_seahorse_underwater, RegionName.toxic_seahorse_hootareca)
    connect(world, RegionName.toxic_seahorse_hootareca, RegionName.toxic_seahorse_dam)
    connect(world, RegionName.toxic_seahorse_dam, RegionName.toxic_seahorse_before_boss)
    connect(world, RegionName.toxic_seahorse_before_boss, RegionName.toxic_seahorse_boss)

    # Connect Tunnel Rhino
    connect(world, RegionName.tunnel_rhino, RegionName.tunnel_rhino_start)
    connect(world, RegionName.tunnel_rhino_start, RegionName.tunnel_rhino_bit_byte)
    connect(world, RegionName.tunnel_rhino_bit_byte, RegionName.bit_byte)
    connect(world, RegionName.tunnel_rhino_bit_byte, RegionName.tunnel_rhino_wall_jump)
    connect(world, RegionName.tunnel_rhino_wall_jump, RegionName.tunnel_rhino_hell_crusher)
    connect(world, RegionName.tunnel_rhino_hell_crusher, RegionName.tunnel_rhino_climbing)
    connect(world, RegionName.tunnel_rhino_climbing, RegionName.tunnel_rhino_boss)

    # Connect Volt Catfish
    connect(world, RegionName.volt_catfish, RegionName.volt_catfish_start)
    connect(world, RegionName.volt_catfish_start, RegionName.volt_catfish_bit_byte)
    connect(world, RegionName.volt_catfish_bit_byte, RegionName.bit_byte)
    connect(world, RegionName.volt_catfish_bit_byte, RegionName.volt_catfish_inside)
    connect(world, RegionName.volt_catfish_inside, RegionName.volt_catfish_boss)

    # Connect Crush Crawfish
    connect(world, RegionName.crush_crawfish, RegionName.crush_crawfish_start)
    connect(world, RegionName.crush_crawfish_start, RegionName.crush_crawfish_bit_byte)
    connect(world, RegionName.crush_crawfish_bit_byte, RegionName.bit_byte)
    connect(world, RegionName.crush_crawfish_bit_byte, RegionName.crush_crawfish_inside)
    connect(world, RegionName.crush_crawfish_inside, RegionName.crush_crawfish_boss)

    # Connect Neon Tiger
    connect(world, RegionName.neon_tiger, RegionName.neon_tiger_start)
    connect(world, RegionName.neon_tiger_start, RegionName.neon_tiger_worm)
    connect(world, RegionName.neon_tiger_worm, RegionName.neon_tiger_bit_byte)
    connect(world, RegionName.neon_tiger_bit_byte, RegionName.bit_byte)
    connect(world, RegionName.neon_tiger_bit_byte, RegionName.neon_tiger_hill)
    connect(world, RegionName.neon_tiger_hill, RegionName.neon_tiger_boss)

    # Connect Gravity Beetle
    connect(world, RegionName.gravity_beetle, RegionName.gravity_beetle_start)
    connect(world, RegionName.gravity_beetle_start, RegionName.gravity_beetle_bit_byte)
    connect(world, RegionName.gravity_beetle_bit_byte, RegionName.bit_byte)
    connect(world, RegionName.gravity_beetle_bit_byte, RegionName.gravity_beetle_outside)
    connect(world, RegionName.gravity_beetle_outside, RegionName.gravity_beetle_inside)
    connect(world, RegionName.gravity_beetle_inside, RegionName.gravity_beetle_boss)

    # Connect Blast Hornet
    connect(world, RegionName.blast_hornet, RegionName.blast_hornet_start)
    connect(world, RegionName.blast_hornet_start, RegionName.blast_hornet_conveyors)
    connect(world, RegionName.blast_hornet_conveyors, RegionName.blast_hornet_shurikein)
    connect(world, RegionName.blast_hornet_shurikein, RegionName.blast_hornet_outside)
    connect(world, RegionName.blast_hornet_outside, RegionName.blast_hornet_bit_byte)
    connect(world, RegionName.blast_hornet_bit_byte, RegionName.bit_byte)
    connect(world, RegionName.blast_hornet_bit_byte, RegionName.blast_hornet_boss)
    
    # Connect Vile
    connect(world, RegionName.blizzard_buffalo_start, RegionName.vile)
    connect(world, RegionName.volt_catfish_start, RegionName.vile)
    connect(world, RegionName.crush_crawfish_start, RegionName.vile)
    connect(world, RegionName.vile, RegionName.vile_before)
    connect(world, RegionName.vile_before, RegionName.vile_boss)
    connect(world, RegionName.vile_boss, RegionName.vile_after)


    # Connect Dr. Doppler Lab
    connect(world, RegionName.intro_stage, RegionName.dr_doppler_lab)

    # Connect Dr. Doppler Lab levels
    if world.options.doppler_all_labs.value:
        connect(world, RegionName.dr_doppler_lab, RegionName.dr_doppler_lab_1)
        connect(world, RegionName.dr_doppler_lab, RegionName.dr_doppler_lab_2)
        connect(world, RegionName.dr_doppler_lab, RegionName.dr_doppler_lab_3)
        connect(world, RegionName.dr_doppler_lab, RegionName.dr_doppler_lab_4)
    else:
        connect(world, RegionName.dr_doppler_lab, RegionName.dr_doppler_lab_1)
        connect(world, RegionName.dr_doppler_lab_1, RegionName.dr_doppler_lab_2)
        connect(world, RegionName.dr_doppler_lab_2, RegionName.dr_doppler_lab_3)
        connect(world, RegionName.dr_doppler_lab_3_boss, RegionName.dr_doppler_lab_4)
    
    connect(world, RegionName.dr_doppler_lab_3, RegionName.dr_doppler_lab_3_rematches)
    connect(world, RegionName.dr_doppler_lab_3_rematches, RegionName.dr_doppler_lab_3_after_rematches)
    connect(world, RegionName.dr_doppler_lab_3_after_rematches, RegionName.dr_doppler_lab_3_boss)
    
    connect(world, RegionName.dr_doppler_lab_4, RegionName.dr_doppler_lab_4_boss)

    # Connect checkpoints
    # Connect Toxic Seahorse
    connect(world, RegionName.toxic_seahorse, RegionName.toxic_seahorse_underwater)
    connect(world, RegionName.toxic_seahorse, RegionName.toxic_seahorse_before_boss)

    # Connect Tunnel Rhino
    connect(world, RegionName.tunnel_rhino, RegionName.tunnel_rhino_wall_jump)
    connect(world, RegionName.tunnel_rhino, RegionName.tunnel_rhino_climbing)

    # Connect Neon Tiger
    connect(world, RegionName.neon_tiger, RegionName.neon_tiger_bit_byte)
    connect(world, RegionName.neon_tiger, RegionName.neon_tiger_hill)

    # Connect Blast Hornet
    connect(world, RegionName.blast_hornet, RegionName.blast_hornet_outside)
    
    # Connect Dr. Doppler Lab levels
    connect(world, RegionName.dr_doppler_lab_3, RegionName.dr_doppler_lab_3_after_rematches)

    
def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = MMX3Location(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret


def add_event_to_region(multiworld: MultiWorld, player: int, region_name: str, event_name: str, event_item=None):
    region = multiworld.get_region(region_name, player)
    event = MMX3Location(player, event_name, None, region)
    if event_item:
        event.place_locked_item(MMX3Item(event_item, ItemClassification.progression, None, player))
    else:
        event.place_locked_item(MMX3Item(event_name, ItemClassification.progression, None, player))
    region.locations.append(event)


def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str):
    region = multiworld.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = MMX3Location(player, location_name, loc_id, region)
        region.locations.append(location)


def connect(world: World, source: str, target: str):
    source_region: Region = world.multiworld.get_region(source, world.player)
    target_region: Region = world.multiworld.get_region(target, world.player)
    source_region.connect(target_region)
