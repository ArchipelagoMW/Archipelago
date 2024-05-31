import typing

from BaseClasses import CollectionState, MultiWorld, Region, Entrance, ItemClassification
from .Locations import MMX2Location
from .Items import MMX2Item
from .Names import LocationName, ItemName, RegionName, EventName
from worlds.AutoWorld import World


def create_regions(multiworld: MultiWorld, player: int, world: World, active_locations):
    menu = create_region(multiworld, player, active_locations, 'Menu')

    intro_stage = create_region(multiworld, player, active_locations, RegionName.intro_stage)

    wheel_gator = create_region(multiworld, player, active_locations, RegionName.wheel_gator)
    wheel_gator_start = create_region(multiworld, player, active_locations, RegionName.wheel_gator_start)
    wheel_gator_mid = create_region(multiworld, player, active_locations, RegionName.wheel_gator_mid)
    wheel_gator_end = create_region(multiworld, player, active_locations, RegionName.wheel_gator_end)
    wheel_gator_boss = create_region(multiworld, player, active_locations, RegionName.wheel_gator_boss)

    bubble_crab = create_region(multiworld, player, active_locations, RegionName.bubble_crab)
    bubble_crab_start = create_region(multiworld, player, active_locations, RegionName.bubble_crab_start)
    bubble_crab_open = create_region(multiworld, player, active_locations, RegionName.bubble_crab_open)
    bubble_crab_inside = create_region(multiworld, player, active_locations, RegionName.bubble_crab_inside)
    bubble_crab_boss = create_region(multiworld, player, active_locations, RegionName.bubble_crab_boss)

    flame_stag = create_region(multiworld, player, active_locations, RegionName.flame_stag)
    flame_stag_start = create_region(multiworld, player, active_locations, RegionName.flame_stag_start)
    flame_stag_volcano = create_region(multiworld, player, active_locations, RegionName.flame_stag_volcano)
    flame_stag_gas = create_region(multiworld, player, active_locations, RegionName.flame_stag_gas)
    flame_stag_boss = create_region(multiworld, player, active_locations, RegionName.flame_stag_boss)

    morph_moth = create_region(multiworld, player, active_locations, RegionName.morph_moth)
    morph_moth_start = create_region(multiworld, player, active_locations, RegionName.morph_moth_start)
    morph_moth_parasite_1 = create_region(multiworld, player, active_locations, RegionName.morph_moth_parasite_1)
    morph_moth_parasite_2 = create_region(multiworld, player, active_locations, RegionName.morph_moth_parasite_2)
    morph_moth_boss = create_region(multiworld, player, active_locations, RegionName.morph_moth_boss)

    magna_centipede = create_region(multiworld, player, active_locations, RegionName.magna_centipede)
    magna_centipede_start = create_region(multiworld, player, active_locations, RegionName.magna_centipede_start)
    magna_centipede_blade = create_region(multiworld, player, active_locations, RegionName.magna_centipede_blade)
    magna_centipede_security = create_region(multiworld, player, active_locations, RegionName.magna_centipede_security)
    magna_centipede_boss = create_region(multiworld, player, active_locations, RegionName.magna_centipede_boss)

    crystal_snail = create_region(multiworld, player, active_locations, RegionName.crystal_snail)
    crystal_snail_start = create_region(multiworld, player, active_locations, RegionName.crystal_snail_start)
    crystal_snail_after_arena = create_region(multiworld, player, active_locations, RegionName.crystal_snail_after_arena)
    crystal_snail_quartz = create_region(multiworld, player, active_locations, RegionName.crystal_snail_quartz)
    crystal_snail_downhill = create_region(multiworld, player, active_locations, RegionName.crystal_snail_downhill)
    crystal_snail_uphill = create_region(multiworld, player, active_locations, RegionName.crystal_snail_uphill)
    crystal_snail_boss = create_region(multiworld, player, active_locations, RegionName.crystal_snail_boss)

    overdrive_ostrich = create_region(multiworld, player, active_locations, RegionName.overdrive_ostrich)
    overdrive_ostrich_start = create_region(multiworld, player, active_locations, RegionName.overdrive_ostrich_start)
    overdrive_ostrich_arena = create_region(multiworld, player, active_locations, RegionName.overdrive_ostrich_arena)
    overdrive_ostrich_inside = create_region(multiworld, player, active_locations, RegionName.overdrive_ostrich_inside)
    overdrive_ostrich_boss = create_region(multiworld, player, active_locations, RegionName.overdrive_ostrich_boss)

    wire_sponge = create_region(multiworld, player, active_locations, RegionName.wire_sponge)
    wire_sponge_start = create_region(multiworld, player, active_locations, RegionName.wire_sponge_start)
    wire_sponge_elevator = create_region(multiworld, player, active_locations, RegionName.wire_sponge_elevator)
    wire_sponge_outside = create_region(multiworld, player, active_locations, RegionName.wire_sponge_outside)
    wire_sponge_boss = create_region(multiworld, player, active_locations, RegionName.wire_sponge_boss)

    x_hunter_arena = create_region(multiworld, player, active_locations, RegionName.x_hunter_arena)

    x_hunter_stage = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage)
    
    x_hunter_stage_1 = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_1)
    x_hunter_stage_1_start = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_1_start)
    x_hunter_stage_1_boss = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_1_boss)

    x_hunter_stage_2 = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_2)
    x_hunter_stage_2_start = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_2_start)
    x_hunter_stage_2_boss = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_2_boss)

    x_hunter_stage_3 = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_3)
    x_hunter_stage_3_start = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_3_start)
    x_hunter_stage_3_boss = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_3_boss)

    x_hunter_stage_4 = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4)
    x_hunter_stage_4_lobby = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby)
    x_hunter_stage_4_voice = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_voice)

    x_hunter_stage_5 = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_5)
    x_hunter_stage_5_zero = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_5_zero)
    x_hunter_stage_5_sigma = create_region(multiworld, player, active_locations, RegionName.x_hunter_stage_5_sigma)

    multiworld.regions += [
        menu,
        intro_stage,
        wheel_gator,
        wheel_gator_start,
        wheel_gator_mid,
        wheel_gator_end,
        wheel_gator_boss,
        bubble_crab,
        bubble_crab_start,
        bubble_crab_open,
        bubble_crab_inside,
        bubble_crab_boss,
        flame_stag,
        flame_stag_start,
        flame_stag_volcano,
        flame_stag_gas,
        flame_stag_boss,
        morph_moth,
        morph_moth_start,
        morph_moth_parasite_1,
        morph_moth_parasite_2,
        morph_moth_boss,
        magna_centipede,
        magna_centipede_start,
        magna_centipede_blade,
        magna_centipede_security,
        magna_centipede_boss,
        crystal_snail,
        crystal_snail_start,
        crystal_snail_after_arena,
        crystal_snail_quartz,
        crystal_snail_downhill,
        crystal_snail_uphill,
        crystal_snail_boss,
        overdrive_ostrich,
        overdrive_ostrich_start,
        overdrive_ostrich_arena,
        overdrive_ostrich_inside,
        overdrive_ostrich_boss,
        wire_sponge,
        wire_sponge_start,
        wire_sponge_elevator,
        wire_sponge_outside,
        wire_sponge_boss,
        x_hunter_arena,
        x_hunter_stage,
        x_hunter_stage_1,
        x_hunter_stage_1_start,
        x_hunter_stage_1_boss,
        x_hunter_stage_2,
        x_hunter_stage_2_start,
        x_hunter_stage_2_boss,
        x_hunter_stage_3,
        x_hunter_stage_3_start,
        x_hunter_stage_3_boss,
        x_hunter_stage_4,
        x_hunter_stage_4_lobby,
        x_hunter_stage_4_voice,
        x_hunter_stage_5,
        x_hunter_stage_5_zero,
        x_hunter_stage_5_sigma,
    ]

    # Intro Stage
    add_location_to_region(multiworld, player, active_locations, RegionName.intro_stage, LocationName.intro_stage_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.intro_stage, LocationName.intro_stage_clear)

    # Wheel Gator
    add_location_to_region(multiworld, player, active_locations, RegionName.wheel_gator, LocationName.wheel_gator_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.wheel_gator, LocationName.wheel_gator_arms)
    add_location_to_region(multiworld, player, active_locations, RegionName.wheel_gator, LocationName.wheel_gator_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.wheel_gator, LocationName.wheel_gator_clear)

    # Bubble Crab
    add_location_to_region(multiworld, player, active_locations, RegionName.bubble_crab, LocationName.bubble_crab_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.bubble_crab, LocationName.bubble_crab_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.bubble_crab, LocationName.bubble_crab_mini_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.bubble_crab, LocationName.bubble_crab_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.bubble_crab, LocationName.bubble_crab_clear)

    # Flame Stag
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_stag, LocationName.flame_stag_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_stag, LocationName.flame_stag_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_stag, LocationName.flame_stag_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.flame_stag, LocationName.flame_stag_clear)

    # Morph Moth
    add_location_to_region(multiworld, player, active_locations, RegionName.morph_moth, LocationName.morph_moth_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.morph_moth, LocationName.morph_moth_body)
    add_location_to_region(multiworld, player, active_locations, RegionName.morph_moth, LocationName.morph_moth_mini_boss_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.morph_moth, LocationName.morph_moth_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.morph_moth, LocationName.morph_moth_clear)

    # Magna Centipede
    add_location_to_region(multiworld, player, active_locations, RegionName.magna_centipede, LocationName.magna_centipede_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.magna_centipede, LocationName.magna_centipede_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.magna_centipede, LocationName.magna_centipede_mini_boss_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.magna_centipede, LocationName.magna_centipede_mini_boss_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.magna_centipede, LocationName.magna_centipede_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.magna_centipede, LocationName.magna_centipede_clear)

    # Crystal Snail
    add_location_to_region(multiworld, player, active_locations, RegionName.crystal_snail, LocationName.crystal_snail_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.crystal_snail, LocationName.crystal_snail_helmet)
    add_location_to_region(multiworld, player, active_locations, RegionName.crystal_snail, LocationName.crystal_snail_mini_boss_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.crystal_snail, LocationName.crystal_snail_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.crystal_snail, LocationName.crystal_snail_clear)

    # Overdrive Ostrich
    add_location_to_region(multiworld, player, active_locations, RegionName.overdrive_ostrich, LocationName.overdrive_ostrich_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.overdrive_ostrich, LocationName.overdrive_ostrich_leg)
    add_location_to_region(multiworld, player, active_locations, RegionName.overdrive_ostrich, LocationName.overdrive_ostrich_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.overdrive_ostrich, LocationName.overdrive_ostrich_clear)

    # Wire Sponge
    add_location_to_region(multiworld, player, active_locations, RegionName.wire_sponge, LocationName.wire_sponge_heart_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.wire_sponge, LocationName.wire_sponge_sub_tank)
    add_location_to_region(multiworld, player, active_locations, RegionName.wire_sponge, LocationName.wire_sponge_boss)
    add_location_to_region(multiworld, player, active_locations, RegionName.wire_sponge, LocationName.wire_sponge_clear)

    # X-Hunter Arena
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_arena, LocationName.agile_defeated)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_arena, LocationName.serges_defeated)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_arena, LocationName.violen_defeated)

    # X-Hunter Stage 1
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_1_boss, LocationName.x_hunter_stage_1_boss)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.x_hunter_stage_1_clear, EventName.x_hunter_stage_1_clear)

    # X-Hunter Stage 2
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_2_boss, LocationName.x_hunter_stage_2_boss)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.x_hunter_stage_2_clear, EventName.x_hunter_stage_2_clear)

    # X-Hunter Stage 3
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_3_boss, LocationName.x_hunter_stage_3_boss)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.x_hunter_stage_3_clear, EventName.x_hunter_stage_3_clear)

    # X-Hunter Stage 4
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby, LocationName.x_hunter_stage_4_wheel_gator)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby, LocationName.x_hunter_stage_4_bubble_crab)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby, LocationName.x_hunter_stage_4_flame_stag)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby, LocationName.x_hunter_stage_4_morph_moth)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby, LocationName.x_hunter_stage_4_magna_centipede)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby, LocationName.x_hunter_stage_4_crystal_snail)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby, LocationName.x_hunter_stage_4_overdrive_ostrich)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_4_lobby, LocationName.x_hunter_stage_4_wire_sponge)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.wheel_gator_rematch, EventName.boss_rematch_clear)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.bubble_crab_rematch, EventName.boss_rematch_clear)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.flame_stag_rematch, EventName.boss_rematch_clear)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.morph_moth_rematch, EventName.boss_rematch_clear)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.magna_centipede_rematch, EventName.boss_rematch_clear)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.crystal_snail_rematch, EventName.boss_rematch_clear)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.overdrive_ostrich_rematch, EventName.boss_rematch_clear)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.wire_sponge_rematch, EventName.boss_rematch_clear)
    add_event_to_region(multiworld, player, RegionName.x_hunter_stage_4_lobby, EventName.x_hunter_stage_4_clear, EventName.x_hunter_stage_4_clear)

    # X-Hunter Stage 5
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_5_zero, LocationName.x_hunter_stage_5_zero)
    add_location_to_region(multiworld, player, active_locations, RegionName.x_hunter_stage_5_sigma, LocationName.victory)


def connect_regions(world: World):
    connect(world, "Menu", RegionName.intro_stage)

    # Connect Hunter Base
    connect(world, RegionName.intro_stage, RegionName.wheel_gator)
    connect(world, RegionName.intro_stage, RegionName.bubble_crab)
    connect(world, RegionName.intro_stage, RegionName.flame_stag)
    connect(world, RegionName.intro_stage, RegionName.morph_moth)
    connect(world, RegionName.intro_stage, RegionName.magna_centipede)
    connect(world, RegionName.intro_stage, RegionName.crystal_snail)
    connect(world, RegionName.intro_stage, RegionName.overdrive_ostrich)
    connect(world, RegionName.intro_stage, RegionName.wire_sponge)
    connect(world, RegionName.intro_stage, RegionName.x_hunter_stage)

    # Connect Wheel Gator
    connect(world, RegionName.wheel_gator, RegionName.wheel_gator_start)
    connect(world, RegionName.wheel_gator_start, RegionName.wheel_gator_mid)
    connect(world, RegionName.wheel_gator_mid, RegionName.wheel_gator_end)
    connect(world, RegionName.wheel_gator_end, RegionName.wheel_gator_boss)

    # Connect Bubble Crab
    connect(world, RegionName.bubble_crab, RegionName.bubble_crab_start)
    connect(world, RegionName.bubble_crab_start, RegionName.bubble_crab_open)
    connect(world, RegionName.bubble_crab_open, RegionName.bubble_crab_inside)
    connect(world, RegionName.bubble_crab_inside, RegionName.bubble_crab_boss)

    # Connect Flame Stag
    connect(world, RegionName.flame_stag, RegionName.flame_stag_start)
    connect(world, RegionName.flame_stag_start, RegionName.flame_stag_volcano)
    connect(world, RegionName.flame_stag_volcano, RegionName.flame_stag_gas)
    connect(world, RegionName.flame_stag_gas, RegionName.flame_stag_boss)

    # Connect Morph Moth
    connect(world, RegionName.morph_moth, RegionName.morph_moth_start)
    connect(world, RegionName.morph_moth_start, RegionName.morph_moth_parasite_1)
    connect(world, RegionName.morph_moth_parasite_1, RegionName.morph_moth_parasite_2)
    connect(world, RegionName.morph_moth_parasite_2, RegionName.morph_moth_boss)

    # Connect Magna Centipede
    connect(world, RegionName.magna_centipede, RegionName.magna_centipede_start)
    connect(world, RegionName.magna_centipede_start, RegionName.magna_centipede_blade)
    connect(world, RegionName.magna_centipede_blade, RegionName.magna_centipede_security)
    connect(world, RegionName.magna_centipede_security, RegionName.magna_centipede_boss)

    # Connect Crystal Snail
    connect(world, RegionName.crystal_snail, RegionName.crystal_snail_start)
    connect(world, RegionName.crystal_snail_start, RegionName.crystal_snail_quartz)
    connect(world, RegionName.crystal_snail_quartz, RegionName.crystal_snail_downhill)
    connect(world, RegionName.crystal_snail_downhill, RegionName.crystal_snail_uphill)
    connect(world, RegionName.crystal_snail_uphill, RegionName.crystal_snail_boss)
    connect(world, RegionName.crystal_snail_start, RegionName.crystal_snail_arena)
    connect(world, RegionName.crystal_snail_arena, RegionName.crystal_snail_after_arena)
    connect(world, RegionName.crystal_snail_after_arena, RegionName.crystal_snail_start)

    # Overdrive Ostrich
    connect(world, RegionName.overdrive_ostrich, RegionName.overdrive_ostrich_start)
    connect(world, RegionName.overdrive_ostrich_start, RegionName.overdrive_ostrich_inside)
    connect(world, RegionName.overdrive_ostrich_start, RegionName.overdrive_ostrich_arena)
    connect(world, RegionName.overdrive_ostrich_inside, RegionName.overdrive_ostrich_boss)

    # Wire Sponge
    connect(world, RegionName.wire_sponge, RegionName.wire_sponge_start)
    connect(world, RegionName.wire_sponge_start, RegionName.wire_sponge_elevator)
    connect(world, RegionName.wire_sponge_elevator, RegionName.wire_sponge_outside)
    connect(world, RegionName.wire_sponge_outside, RegionName.wire_sponge_boss)

    # Connect X-Hunter Arena
    connect(world, RegionName.wheel_gator_mid, RegionName.x_hunter_arena)
    connect(world, RegionName.bubble_crab_open, RegionName.x_hunter_arena)
    connect(world, RegionName.flame_stag_volcano, RegionName.x_hunter_arena)
    connect(world, RegionName.morph_moth_parasite_1, RegionName.x_hunter_arena)
    connect(world, RegionName.magna_centipede_blade, RegionName.x_hunter_arena)
    connect(world, RegionName.crystal_snail_arena, RegionName.x_hunter_arena)
    connect(world, RegionName.overdrive_ostrich_arena, RegionName.x_hunter_arena)
    connect(world, RegionName.wire_sponge_elevator, RegionName.x_hunter_arena)

    # Connect X-Hunter Stage 1
    connect(world, RegionName.x_hunter_stage_1, RegionName.x_hunter_stage_1_start)
    connect(world, RegionName.x_hunter_stage_1_start, RegionName.x_hunter_stage_1_boss)

    # Connect X-Hunter Stage 2
    connect(world, RegionName.x_hunter_stage_2, RegionName.x_hunter_stage_2_start)
    connect(world, RegionName.x_hunter_stage_2_start, RegionName.x_hunter_stage_2_boss)
    
    # Connect X-Hunter Stage 3
    connect(world, RegionName.x_hunter_stage_3, RegionName.x_hunter_stage_3_start)
    connect(world, RegionName.x_hunter_stage_3_start, RegionName.x_hunter_stage_3_boss)

    # Connect X-Hunter Stage 4
    connect(world, RegionName.x_hunter_stage_4, RegionName.x_hunter_stage_4_lobby)
    connect(world, RegionName.x_hunter_stage_4_lobby, RegionName.x_hunter_stage_4_voice)

    # Connect X-Hunter Stage 5
    connect(world, RegionName.x_hunter_stage_5, RegionName.x_hunter_stage_5_zero)
    connect(world, RegionName.x_hunter_stage_5_zero, RegionName.x_hunter_stage_5_sigma)

    # Connect X-Hunter Stages
    if world.options.base_all_levels:
        connect(world, RegionName.x_hunter_stage, RegionName.x_hunter_stage_1)
        connect(world, RegionName.x_hunter_stage, RegionName.x_hunter_stage_2)
        connect(world, RegionName.x_hunter_stage, RegionName.x_hunter_stage_3)
        connect(world, RegionName.x_hunter_stage, RegionName.x_hunter_stage_4)
    else:
        connect(world, RegionName.x_hunter_stage, RegionName.x_hunter_stage_1)
        connect(world, RegionName.x_hunter_stage_1_boss, RegionName.x_hunter_stage_2)
        connect(world, RegionName.x_hunter_stage_2_boss, RegionName.x_hunter_stage_3)
        connect(world, RegionName.x_hunter_stage_3_boss, RegionName.x_hunter_stage_4)
        connect(world, RegionName.x_hunter_stage_4_lobby, RegionName.x_hunter_stage_5)


def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = MMX2Location(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret


def add_event_to_region(multiworld: MultiWorld, player: int, region_name: str, event_name: str, event_item=None):
    region = multiworld.get_region(region_name, player)
    event = MMX2Location(player, event_name, None, region)
    if event_item:
        event.place_locked_item(MMX2Item(event_item, ItemClassification.progression, None, player))
    else:
        event.place_locked_item(MMX2Item(event_name, ItemClassification.progression, None, player))
    region.locations.append(event)


def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str):
    region = multiworld.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = MMX2Location(player, location_name, loc_id, region)
        region.locations.append(location)


def connect(world: World, source: str, target: str):
    source_region: Region = world.multiworld.get_region(source, world.player)
    target_region: Region = world.multiworld.get_region(target, world.player)
    source_region.connect(target_region)
