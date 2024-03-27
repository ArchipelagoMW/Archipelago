import typing

from BaseClasses import CollectionState, MultiWorld, Region, Entrance, ItemClassification
from .Locations import MMX3Location
from .Items import MMX3Item
from .Names import LocationName, ItemName
from worlds.AutoWorld import World


def create_regions(multiworld: MultiWorld, player: int, world: World, active_locations):
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
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_clear)
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_sub_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.blizzard_buffalo_region, LocationName.blizzard_buffalo_legs)

    # Toxic Seahorse
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_clear)
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_mini_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_kangaroo_ride)
    add_location_to_region(multiworld, player, active_locations, LocationName.toxic_seahorse_region, LocationName.toxic_seahorse_leg)

    # Tunnel Rhino
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_clear)
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_mini_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_sub_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.tunnel_rhino_region, LocationName.tunnel_rhino_helmet)

    # Volt Catfish
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_clear)
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_sub_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_body)

    # Crush Crawfish
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_clear)
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_hawk_ride)
    add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_body)

    # Neon Tiger
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_clear)
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_mini_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_sub_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.neon_tiger_region, LocationName.neon_tiger_arms)

    # Gravity Beetle
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_clear)
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_frog_ride)
    add_location_to_region(multiworld, player, active_locations, LocationName.gravity_beetle_region, LocationName.gravity_beetle_arms)

    # Blast Hornet
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_clear)
    add_event_to_region(multiworld, player, LocationName.blast_hornet_region, LocationName.event_blast_hornet_defeated, ItemName.event_blast_hornet_defeated)
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_mini_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_heart_tank)
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_chimera_ride)
    add_location_to_region(multiworld, player, active_locations, LocationName.blast_hornet_region, LocationName.blast_hornet_helmet)

    # Dr. Doppler Lab 1
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, LocationName.doppler_lab_1_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_1_region, LocationName.doppler_lab_1_mini_boss)

    # Dr. Doppler Lab 2
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_2_region, LocationName.doppler_lab_2_boss)
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_2_region, LocationName.doppler_lab_2_mini_boss)

    # Dr. Doppler Lab 3
    add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_boss)
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
    add_location_to_region(multiworld, player, active_locations, LocationName.bit_byte_region, LocationName.bit_defeat)
    add_location_to_region(multiworld, player, active_locations, LocationName.bit_byte_region, LocationName.byte_defeat)

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
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_energy_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_energy_3)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_2)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_3)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_4)
        add_location_to_region(multiworld, player, active_locations, LocationName.volt_catfish_region, LocationName.volt_catfish_hp_5)

        # Crush Crawfish
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_1up_1)
        add_location_to_region(multiworld, player, active_locations, LocationName.crush_crawfish_region, LocationName.crush_crawfish_1up_2)
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
        
        # Dr. Doppler Lab 3
        add_location_to_region(multiworld, player, active_locations, LocationName.dr_doppler_lab_3_region, LocationName.doppler_lab_3_hp)

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
        

def connect_regions(world: World):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    connect(world, "Menu", LocationName.intro_stage_region)

    # Connect Hunter Base
    connect(world, LocationName.intro_stage_region, LocationName.blizzard_buffalo_region)
    connect(world, LocationName.intro_stage_region, LocationName.toxic_seahorse_region)
    connect(world, LocationName.intro_stage_region, LocationName.tunnel_rhino_region)
    connect(world, LocationName.intro_stage_region, LocationName.volt_catfish_region)
    connect(world, LocationName.intro_stage_region, LocationName.crush_crawfish_region)
    connect(world, LocationName.intro_stage_region, LocationName.neon_tiger_region)
    connect(world, LocationName.intro_stage_region, LocationName.gravity_beetle_region)
    connect(world, LocationName.intro_stage_region, LocationName.blast_hornet_region)
    
    # Connect Vile
    connect(world, LocationName.blizzard_buffalo_region, LocationName.vile_region)
    connect(world, LocationName.toxic_seahorse_region, LocationName.vile_region)
    connect(world, LocationName.crush_crawfish_region, LocationName.vile_region)

    # Connect Bit & Byte
    connect(world, LocationName.blast_hornet_region, LocationName.bit_byte_region)
    connect(world, LocationName.blizzard_buffalo_region, LocationName.bit_byte_region)
    connect(world, LocationName.toxic_seahorse_region, LocationName.bit_byte_region)
    connect(world, LocationName.tunnel_rhino_region, LocationName.bit_byte_region)
    connect(world, LocationName.volt_catfish_region, LocationName.bit_byte_region)
    connect(world, LocationName.crush_crawfish_region, LocationName.bit_byte_region)
    connect(world, LocationName.neon_tiger_region, LocationName.bit_byte_region)
    connect(world, LocationName.gravity_beetle_region, LocationName.bit_byte_region)
    
    # Connect Dr. Doppler Lab
    connect(world, LocationName.intro_stage_region, LocationName.dr_doppler_lab_region)

    # Connect Dr. Doppler Lab levels
    connect(world, LocationName.dr_doppler_lab_region, LocationName.dr_doppler_lab_1_region)
    connect(world, LocationName.dr_doppler_lab_1_region, LocationName.dr_doppler_lab_2_region)
    connect(world, LocationName.dr_doppler_lab_2_region, LocationName.dr_doppler_lab_3_region)
    connect(world, LocationName.dr_doppler_lab_3_region, LocationName.dr_doppler_lab_4_region)
    
    
def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = MMX3Location(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret


def add_event_to_region(multiworld: MultiWorld, player: int, region_name: str, event_name: str, event_item: str):
    region = multiworld.get_region(region_name, player)
    event = MMX3Location(player, event_name, None, region)
    event.place_locked_item(MMX3Item(event_item, ItemClassification.progression, None, player))
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
