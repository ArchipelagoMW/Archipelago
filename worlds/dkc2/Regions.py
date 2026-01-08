from BaseClasses import MultiWorld, Region, ItemClassification
from .Locations import DKC2Location
from .Items import DKC2Item
from .Names import LocationName, RegionName, EventName
from .Options import Goal
from .Levels import level_map, regional_events, boss_connections
from worlds.AutoWorld import World

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import DKC2World

def create_regions(world: "DKC2World", active_locations):
    multiworld = world.multiworld
    player = world.player

    menu = create_region(multiworld, player, active_locations, 'Menu')

    # Worlds
    crocodile_isle = create_region(multiworld, player, active_locations, RegionName.crocodile_isle)
    gangplank_galleon = create_region(multiworld, player, active_locations, RegionName.gangplank_galleon)
    crocodile_cauldron = create_region(multiworld, player, active_locations, RegionName.crocodile_cauldron)
    krem_quay = create_region(multiworld, player, active_locations, RegionName.krem_quay)
    krazy_kremland = create_region(multiworld, player, active_locations, RegionName.krazy_kremland)
    gloomy_gulch = create_region(multiworld, player, active_locations, RegionName.gloomy_gulch)
    krools_keep = create_region(multiworld, player, active_locations, RegionName.krools_keep)
    the_flying_krock = create_region(multiworld, player, active_locations, RegionName.the_flying_krock)
    lost_world_cauldron = create_region(multiworld, player, active_locations, RegionName.lost_world_cauldron)
    lost_world_quay = create_region(multiworld, player, active_locations, RegionName.lost_world_quay)
    lost_world_kremland = create_region(multiworld, player, active_locations, RegionName.lost_world_kremland)
    lost_world_gulch = create_region(multiworld, player, active_locations, RegionName.lost_world_gulch)
    lost_world_keep = create_region(multiworld, player, active_locations, RegionName.lost_world_keep)

    # Map levels
    pirate_panic_map = create_region(multiworld, player, active_locations, RegionName.pirate_panic_map)
    mainbrace_mayhem_map = create_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_map)
    gangplank_galley_map = create_region(multiworld, player, active_locations, RegionName.gangplank_galley_map)
    lockjaws_locker_map = create_region(multiworld, player, active_locations, RegionName.lockjaws_locker_map)
    topsail_trouble_map = create_region(multiworld, player, active_locations, RegionName.topsail_trouble_map)
    krows_nest_map = create_region(multiworld, player, active_locations, RegionName.krows_nest_map)

    hot_head_hop_map = create_region(multiworld, player, active_locations, RegionName.hot_head_hop_map)
    kannons_klaim_map = create_region(multiworld, player, active_locations, RegionName.kannons_klaim_map)
    lava_lagoon_map = create_region(multiworld, player, active_locations, RegionName.lava_lagoon_map)
    red_hot_ride_map = create_region(multiworld, player, active_locations, RegionName.red_hot_ride_map)
    squawks_shaft_map = create_region(multiworld, player, active_locations, RegionName.squawks_shaft_map)
    kleevers_kiln_map = create_region(multiworld, player, active_locations, RegionName.kleevers_kiln_map)

    barrel_bayou_map = create_region(multiworld, player, active_locations, RegionName.barrel_bayou_map)
    glimmers_galleon_map = create_region(multiworld, player, active_locations, RegionName.glimmers_galleon_map)
    krockhead_klamber_map = create_region(multiworld, player, active_locations, RegionName.krockhead_klamber_map)
    rattle_battle_map = create_region(multiworld, player, active_locations, RegionName.rattle_battle_map)
    slime_climb_map = create_region(multiworld, player, active_locations, RegionName.slime_climb_map)
    bramble_blast_map = create_region(multiworld, player, active_locations, RegionName.bramble_blast_map)
    kudgels_kontest_map = create_region(multiworld, player, active_locations, RegionName.kudgels_kontest_map)

    hornet_hole_map = create_region(multiworld, player, active_locations, RegionName.hornet_hole_map)
    target_terror_map = create_region(multiworld, player, active_locations, RegionName.target_terror_map)
    bramble_scramble_map = create_region(multiworld, player, active_locations, RegionName.bramble_scramble_map)
    rickety_race_map = create_region(multiworld, player, active_locations, RegionName.rickety_race_map)
    mudhole_marsh_map = create_region(multiworld, player, active_locations, RegionName.mudhole_marsh_map)
    rambi_rumble_map = create_region(multiworld, player, active_locations, RegionName.rambi_rumble_map)
    king_zing_sting_map = create_region(multiworld, player, active_locations, RegionName.king_zing_sting_map)

    ghostly_grove_map = create_region(multiworld, player, active_locations, RegionName.ghostly_grove_map)
    haunted_hall_map = create_region(multiworld, player, active_locations, RegionName.haunted_hall_map)
    gusty_glade_map = create_region(multiworld, player, active_locations, RegionName.gusty_glade_map)
    parrot_chute_panic_map = create_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_map)
    web_woods_map = create_region(multiworld, player, active_locations, RegionName.web_woods_map)
    kreepy_krow_map = create_region(multiworld, player, active_locations, RegionName.kreepy_krow_map)

    arctic_abyss_map = create_region(multiworld, player, active_locations, RegionName.arctic_abyss_map)
    windy_well_map = create_region(multiworld, player, active_locations, RegionName.windy_well_map)
    castle_crush_map = create_region(multiworld, player, active_locations, RegionName.castle_crush_map)
    clappers_cavern_map = create_region(multiworld, player, active_locations, RegionName.clappers_cavern_map)
    chain_link_chamber_map = create_region(multiworld, player, active_locations, RegionName.chain_link_chamber_map)
    toxic_tower_map = create_region(multiworld, player, active_locations, RegionName.toxic_tower_map)
    stronghold_showdown_map = create_region(multiworld, player, active_locations, RegionName.stronghold_showdown_map)

    screechs_sprint_map = create_region(multiworld, player, active_locations, RegionName.screechs_sprint_map)

    jungle_jinx_map = create_region(multiworld, player, active_locations, RegionName.jungle_jinx_map)
    black_ice_battle_map = create_region(multiworld, player, active_locations, RegionName.black_ice_battle_map)
    klobber_karnage_map = create_region(multiworld, player, active_locations, RegionName.klobber_karnage_map)
    fiery_furnace_map = create_region(multiworld, player, active_locations, RegionName.fiery_furnace_map)
    animal_antics_map = create_region(multiworld, player, active_locations, RegionName.animal_antics_map)

    # Level regions
    pirate_panic_level = create_region(multiworld, player, active_locations, RegionName.pirate_panic_level)
    mainbrace_mayhem_level = create_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level)
    gangplank_galley_level = create_region(multiworld, player, active_locations, RegionName.gangplank_galley_level)
    lockjaws_locker_level = create_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level)
    topsail_trouble_level = create_region(multiworld, player, active_locations, RegionName.topsail_trouble_level)
    krows_nest_level = create_region(multiworld, player, active_locations, RegionName.krows_nest_level)

    hot_head_hop_level = create_region(multiworld, player, active_locations, RegionName.hot_head_hop_level)
    kannons_klaim_level = create_region(multiworld, player, active_locations, RegionName.kannons_klaim_level)
    lava_lagoon_level = create_region(multiworld, player, active_locations, RegionName.lava_lagoon_level)
    red_hot_ride_level = create_region(multiworld, player, active_locations, RegionName.red_hot_ride_level)
    squawks_shaft_level = create_region(multiworld, player, active_locations, RegionName.squawks_shaft_level)
    kleevers_kiln_level = create_region(multiworld, player, active_locations, RegionName.kleevers_kiln_level)

    barrel_bayou_level = create_region(multiworld, player, active_locations, RegionName.barrel_bayou_level)
    glimmers_galleon_level = create_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level)
    krockhead_klamber_level = create_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level)
    rattle_battle_level = create_region(multiworld, player, active_locations, RegionName.rattle_battle_level)
    slime_climb_level = create_region(multiworld, player, active_locations, RegionName.slime_climb_level)
    bramble_blast_level = create_region(multiworld, player, active_locations, RegionName.bramble_blast_level)
    kudgels_kontest_level = create_region(multiworld, player, active_locations, RegionName.kudgels_kontest_level)

    hornet_hole_level = create_region(multiworld, player, active_locations, RegionName.hornet_hole_level)
    target_terror_level = create_region(multiworld, player, active_locations, RegionName.target_terror_level)
    bramble_scramble_level = create_region(multiworld, player, active_locations, RegionName.bramble_scramble_level)
    rickety_race_level = create_region(multiworld, player, active_locations, RegionName.rickety_race_level)
    mudhole_marsh_level = create_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level)
    rambi_rumble_level = create_region(multiworld, player, active_locations, RegionName.rambi_rumble_level)
    king_zing_sting_level = create_region(multiworld, player, active_locations, RegionName.king_zing_sting_level)

    ghostly_grove_level = create_region(multiworld, player, active_locations, RegionName.ghostly_grove_level)
    haunted_hall_level = create_region(multiworld, player, active_locations, RegionName.haunted_hall_level)
    gusty_glade_level = create_region(multiworld, player, active_locations, RegionName.gusty_glade_level)
    parrot_chute_panic_level = create_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level)
    web_woods_level = create_region(multiworld, player, active_locations, RegionName.web_woods_level)
    kreepy_krow_level = create_region(multiworld, player, active_locations, RegionName.kreepy_krow_level)

    arctic_abyss_level = create_region(multiworld, player, active_locations, RegionName.arctic_abyss_level)
    windy_well_level = create_region(multiworld, player, active_locations, RegionName.windy_well_level)
    castle_crush_level = create_region(multiworld, player, active_locations, RegionName.castle_crush_level)
    clappers_cavern_level = create_region(multiworld, player, active_locations, RegionName.clappers_cavern_level)
    chain_link_chamber_level = create_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level)
    toxic_tower_level = create_region(multiworld, player, active_locations, RegionName.toxic_tower_level)
    stronghold_showdown_level = create_region(multiworld, player, active_locations, RegionName.stronghold_showdown_level)

    screechs_sprint_level = create_region(multiworld, player, active_locations, RegionName.screechs_sprint_level)

    jungle_jinx_level = create_region(multiworld, player, active_locations, RegionName.jungle_jinx_level)
    black_ice_battle_level = create_region(multiworld, player, active_locations, RegionName.black_ice_battle_level)
    klobber_karnage_level = create_region(multiworld, player, active_locations, RegionName.klobber_karnage_level)
    fiery_furnace_level = create_region(multiworld, player, active_locations, RegionName.fiery_furnace_level)
    animal_antics_level = create_region(multiworld, player, active_locations, RegionName.animal_antics_level)


    multiworld.regions += [
        menu,
        crocodile_isle,
        gangplank_galleon,
        crocodile_cauldron,
        krem_quay,
        krazy_kremland,
        gloomy_gulch,
        krools_keep,
        the_flying_krock,
        lost_world_cauldron,
        lost_world_quay,
        lost_world_kremland,
        lost_world_gulch,
        lost_world_keep,
        pirate_panic_map,
        mainbrace_mayhem_map,
        gangplank_galley_map,
        lockjaws_locker_map,
        topsail_trouble_map,
        krows_nest_map,
        hot_head_hop_map,
        kannons_klaim_map,
        lava_lagoon_map,
        red_hot_ride_map,
        squawks_shaft_map,
        kleevers_kiln_map,
        barrel_bayou_map,
        glimmers_galleon_map,
        krockhead_klamber_map,
        rattle_battle_map,
        slime_climb_map,
        bramble_blast_map,
        kudgels_kontest_map,
        hornet_hole_map,
        target_terror_map,
        bramble_scramble_map,
        rickety_race_map,
        mudhole_marsh_map,
        rambi_rumble_map,
        king_zing_sting_map,
        ghostly_grove_map,
        haunted_hall_map,
        gusty_glade_map,
        parrot_chute_panic_map,
        web_woods_map,
        kreepy_krow_map,
        arctic_abyss_map,
        windy_well_map,
        castle_crush_map,
        clappers_cavern_map,
        chain_link_chamber_map,
        toxic_tower_map,
        stronghold_showdown_map,
        screechs_sprint_map,
        jungle_jinx_map,
        black_ice_battle_map,
        klobber_karnage_map,
        fiery_furnace_map,
        animal_antics_map,
        pirate_panic_level,
        mainbrace_mayhem_level,
        gangplank_galley_level,
        lockjaws_locker_level,
        topsail_trouble_level,
        krows_nest_level,
        hot_head_hop_level,
        kannons_klaim_level,
        lava_lagoon_level,
        red_hot_ride_level,
        squawks_shaft_level,
        kleevers_kiln_level,
        barrel_bayou_level,
        glimmers_galleon_level,
        krockhead_klamber_level,
        rattle_battle_level,
        slime_climb_level,
        bramble_blast_level,
        kudgels_kontest_level,
        hornet_hole_level,
        target_terror_level,
        bramble_scramble_level,
        rickety_race_level,
        mudhole_marsh_level,
        rambi_rumble_level,
        king_zing_sting_level,
        ghostly_grove_level,
        haunted_hall_level,
        gusty_glade_level,
        parrot_chute_panic_level,
        web_woods_level,
        kreepy_krow_level,
        arctic_abyss_level,
        windy_well_level,
        castle_crush_level,
        clappers_cavern_level,
        chain_link_chamber_level,
        toxic_tower_level,
        stronghold_showdown_level,
        screechs_sprint_level,
        jungle_jinx_level,
        black_ice_battle_level,
        klobber_karnage_level,
        fiery_furnace_level,
        animal_antics_level,
    ]

    if world.options.goal != Goal.option_lost_world:
        k_rool_duel_level = create_region(multiworld, player, active_locations, RegionName.k_rool_duel_level)
        k_rool_duel_map = create_region(multiworld, player, active_locations, RegionName.k_rool_duel_map)
        multiworld.regions.append(k_rool_duel_level)
        multiworld.regions.append(k_rool_duel_map)
    
    if world.options.goal != Goal.option_flying_krock:
        krocodile_core_level = create_region(multiworld, player, active_locations, RegionName.krocodile_core_level)
        krocodile_core_map = create_region(multiworld, player, active_locations, RegionName.krocodile_core_map)
        multiworld.regions.append(krocodile_core_level)
        multiworld.regions.append(krocodile_core_map)

    # Level clears
    add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.krows_nest_level, LocationName.krows_nest_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.kleevers_kiln_level, LocationName.kleevers_kiln_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.kudgels_kontest_level, LocationName.kudgels_kontest_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.target_terror_level, LocationName.target_terror_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.rickety_race_level, LocationName.rickety_race_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.king_zing_sting_level, LocationName.king_zing_sting_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.kreepy_krow_level, LocationName.kreepy_krow_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.stronghold_showdown_level, LocationName.stronghold_showdown_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_clear)
    add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_clear)

    # Level clears (Events)
    for map_level, level in world.level_connections.items():
        current_world = level_map[map_level]
        if "Lost World" in current_world or map_level in boss_connections.keys():
            continue
        event_name = level.replace(": Level", " - Clear (Map Event)")
        event_item = regional_events[current_world]
        add_event_to_region(multiworld, player, level, event_name, event_item)

    add_location_to_region(multiworld, player, active_locations, RegionName.krows_nest_level, LocationName.krow_defeated)
    add_location_to_region(multiworld, player, active_locations, RegionName.kleevers_kiln_level, LocationName.kleever_defeated)
    add_location_to_region(multiworld, player, active_locations, RegionName.kudgels_kontest_level, LocationName.kudgel_defeated)
    add_location_to_region(multiworld, player, active_locations, RegionName.king_zing_sting_level, LocationName.king_zing_defeated)
    add_location_to_region(multiworld, player, active_locations, RegionName.kreepy_krow_level, LocationName.kreepy_krow_defeated)

    if world.options.goal != Goal.option_lost_world:
        add_event_to_region(multiworld, player, RegionName.k_rool_duel_level, LocationName.k_rool_duel_clear, EventName.k_rool_duel_clear)

    if world.options.goal != Goal.option_flying_krock:
        add_event_to_region(multiworld, player, RegionName.krocodile_core_level, LocationName.krocodile_core_clear, EventName.krocodile_core_clear)
    
    # Bonuses
    add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.target_terror_level, LocationName.target_terror_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.target_terror_level, LocationName.target_terror_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.rickety_race_level, LocationName.rickety_race_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_bonus_3)
    add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_bonus_2)
    add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_bonus_1)
    add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_bonus_1)

    # KONG
    if world.options.kong_checks:
        add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.target_terror_level, LocationName.target_terror_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.rickety_race_level, LocationName.rickety_race_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_kong)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_kong)

    # DK Coin
    if world.options.dk_coin_checks:
        add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.target_terror_level, LocationName.target_terror_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.rickety_race_level, LocationName.rickety_race_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_dk_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_dk_coin)

    if world.options.swanky_checks:
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galleon, LocationName.swanky_galleon_game_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galleon, LocationName.swanky_galleon_game_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galleon, LocationName.swanky_galleon_game_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.crocodile_cauldron, LocationName.swanky_cauldron_game_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.crocodile_cauldron, LocationName.swanky_cauldron_game_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.crocodile_cauldron, LocationName.swanky_cauldron_game_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.krem_quay, LocationName.swanky_quay_game_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.krem_quay, LocationName.swanky_quay_game_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.krem_quay, LocationName.swanky_quay_game_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.krazy_kremland, LocationName.swanky_kremland_game_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.krazy_kremland, LocationName.swanky_kremland_game_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.krazy_kremland, LocationName.swanky_kremland_game_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.gloomy_gulch, LocationName.swanky_gulch_game_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.gloomy_gulch, LocationName.swanky_gulch_game_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.gloomy_gulch, LocationName.swanky_gulch_game_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.krools_keep, LocationName.swanky_keep_game_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.krools_keep, LocationName.swanky_keep_game_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.krools_keep, LocationName.swanky_keep_game_3)

    if world.options.balloonsanity:
        add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_green_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_green_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_red_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_red_balloon_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_red_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_red_balloon_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_blue_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_green_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_red_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_red_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_green_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_red_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_red_balloon_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_green_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_red_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.target_terror_level, LocationName.target_terror_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_blue_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_blue_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_green_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_green_balloon_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_red_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_red_balloon_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_green_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.stronghold_showdown_level, LocationName.stronghold_showdown_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_red_balloon_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_red_balloon_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_red_balloon_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_red_balloon)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_red_balloon)

    if world.options.coinsanity:
        add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_coin_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_coin_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_coin_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.krows_nest_level, LocationName.krows_nest_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.krows_nest_level, LocationName.krows_nest_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_coin_10)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_coin_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_coin_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_coin_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.kleevers_kiln_level, LocationName.kleevers_kiln_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.kleevers_kiln_level, LocationName.kleevers_kiln_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_coin_10)
        add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.krockhead_klamber_level, LocationName.krockhead_klamber_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_coin_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_coin_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_coin_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.rickety_race_level, LocationName.rickety_race_banana_coin)
        add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.king_zing_sting_level, LocationName.king_zing_sting_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.king_zing_sting_level, LocationName.king_zing_sting_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.gusty_glade_level, LocationName.gusty_glade_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.kreepy_krow_level, LocationName.kreepy_krow_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.kreepy_krow_level, LocationName.kreepy_krow_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.stronghold_showdown_level, LocationName.stronghold_showdown_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.stronghold_showdown_level, LocationName.stronghold_showdown_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_coin_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_coin_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_coin_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_banana_coin_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_coin_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_coin_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_coin_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_coin_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_coin_5)

    if world.options.bananasanity:
        add_location_to_region(multiworld, player, active_locations, RegionName.pirate_panic_level, LocationName.pirate_panic_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.mainbrace_mayhem_level, LocationName.mainbrace_mayhem_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.gangplank_galley_level, LocationName.gangplank_galley_banana_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.lockjaws_locker_level, LocationName.lockjaws_locker_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.topsail_trouble_level, LocationName.topsail_trouble_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.hot_head_hop_level, LocationName.hot_head_hop_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.kannons_klaim_level, LocationName.kannons_klaim_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.lava_lagoon_level, LocationName.lava_lagoon_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.red_hot_ride_level, LocationName.red_hot_ride_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.squawks_shaft_level, LocationName.squawks_shaft_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.barrel_bayou_level, LocationName.barrel_bayou_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_10)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_11)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_12)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_13)
        add_location_to_region(multiworld, player, active_locations, RegionName.glimmers_galleon_level, LocationName.glimmers_galleon_banana_bunch_14)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.rattle_battle_level, LocationName.rattle_battle_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.slime_climb_level, LocationName.slime_climb_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_blast_level, LocationName.bramble_blast_banana_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.hornet_hole_level, LocationName.hornet_hole_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.target_terror_level, LocationName.target_terror_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.target_terror_level, LocationName.target_terror_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.bramble_scramble_level, LocationName.bramble_scramble_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.mudhole_marsh_level, LocationName.mudhole_marsh_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.rambi_rumble_level, LocationName.rambi_rumble_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.ghostly_grove_level, LocationName.ghostly_grove_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.haunted_hall_level, LocationName.haunted_hall_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.parrot_chute_panic_level, LocationName.parrot_chute_panic_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.web_woods_level, LocationName.web_woods_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.arctic_abyss_level, LocationName.arctic_abyss_banana_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.windy_well_level, LocationName.windy_well_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.castle_crush_level, LocationName.castle_crush_banana_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.clappers_cavern_level, LocationName.clappers_cavern_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.chain_link_chamber_level, LocationName.chain_link_chamber_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_8)
        add_location_to_region(multiworld, player, active_locations, RegionName.toxic_tower_level, LocationName.toxic_tower_banana_bunch_9)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.screechs_sprint_level, LocationName.screechs_sprint_banana_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.jungle_jinx_level, LocationName.jungle_jinx_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.black_ice_battle_level, LocationName.black_ice_battle_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_bunch_6)
        add_location_to_region(multiworld, player, active_locations, RegionName.klobber_karnage_level, LocationName.klobber_karnage_banana_bunch_7)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_banana_bunch_4)
        add_location_to_region(multiworld, player, active_locations, RegionName.fiery_furnace_level, LocationName.fiery_furnace_banana_bunch_5)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_bunch_1)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_bunch_2)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_bunch_3)
        add_location_to_region(multiworld, player, active_locations, RegionName.animal_antics_level, LocationName.animal_antics_banana_bunch_4)


def connect_regions(world: "DKC2World"):
    connect(world, "Menu", RegionName.crocodile_isle)

    connect(world, RegionName.crocodile_isle, RegionName.gangplank_galleon)
    connect(world, RegionName.crocodile_isle, RegionName.crocodile_cauldron)
    connect(world, RegionName.crocodile_isle, RegionName.krem_quay)
    connect(world, RegionName.crocodile_isle, RegionName.krazy_kremland)
    connect(world, RegionName.crocodile_isle, RegionName.gloomy_gulch)
    connect(world, RegionName.crocodile_isle, RegionName.krools_keep)
    connect(world, RegionName.crocodile_isle, RegionName.the_flying_krock)

    connect(world, RegionName.crocodile_cauldron, RegionName.lost_world_cauldron)
    connect(world, RegionName.krem_quay, RegionName.lost_world_quay)
    connect(world, RegionName.krazy_kremland, RegionName.lost_world_kremland)
    connect(world, RegionName.gloomy_gulch, RegionName.lost_world_gulch)
    connect(world, RegionName.krools_keep, RegionName.lost_world_keep)

    connect(world, RegionName.gangplank_galleon, RegionName.pirate_panic_map)
    connect(world, RegionName.gangplank_galleon, RegionName.mainbrace_mayhem_map)
    connect(world, RegionName.gangplank_galleon, RegionName.gangplank_galley_map)
    connect(world, RegionName.gangplank_galleon, RegionName.lockjaws_locker_map)
    connect(world, RegionName.gangplank_galleon, RegionName.topsail_trouble_map)
    connect(world, RegionName.gangplank_galleon, RegionName.krows_nest_map)

    connect(world, RegionName.crocodile_cauldron, RegionName.hot_head_hop_map)
    connect(world, RegionName.crocodile_cauldron, RegionName.kannons_klaim_map)
    connect(world, RegionName.crocodile_cauldron, RegionName.lava_lagoon_map)
    connect(world, RegionName.crocodile_cauldron, RegionName.red_hot_ride_map)
    connect(world, RegionName.crocodile_cauldron, RegionName.squawks_shaft_map)
    connect(world, RegionName.crocodile_cauldron, RegionName.kleevers_kiln_map)

    connect(world, RegionName.krem_quay, RegionName.barrel_bayou_map)
    connect(world, RegionName.krem_quay, RegionName.glimmers_galleon_map)
    connect(world, RegionName.krem_quay, RegionName.krockhead_klamber_map)
    connect(world, RegionName.krem_quay, RegionName.rattle_battle_map)
    connect(world, RegionName.krem_quay, RegionName.slime_climb_map)
    connect(world, RegionName.krem_quay, RegionName.bramble_blast_map)
    connect(world, RegionName.krem_quay, RegionName.kudgels_kontest_map)

    connect(world, RegionName.krazy_kremland, RegionName.hornet_hole_map)
    connect(world, RegionName.krazy_kremland, RegionName.target_terror_map)
    connect(world, RegionName.krazy_kremland, RegionName.bramble_scramble_map)
    connect(world, RegionName.krazy_kremland, RegionName.rickety_race_map)
    connect(world, RegionName.krazy_kremland, RegionName.mudhole_marsh_map)
    connect(world, RegionName.krazy_kremland, RegionName.rambi_rumble_map)
    connect(world, RegionName.krazy_kremland, RegionName.king_zing_sting_map)
    
    connect(world, RegionName.gloomy_gulch, RegionName.ghostly_grove_map)
    connect(world, RegionName.gloomy_gulch, RegionName.haunted_hall_map)
    connect(world, RegionName.gloomy_gulch, RegionName.gusty_glade_map)
    connect(world, RegionName.gloomy_gulch, RegionName.parrot_chute_panic_map)
    connect(world, RegionName.gloomy_gulch, RegionName.web_woods_map)
    connect(world, RegionName.gloomy_gulch, RegionName.kreepy_krow_map)
    
    connect(world, RegionName.krools_keep, RegionName.arctic_abyss_map)
    connect(world, RegionName.krools_keep, RegionName.windy_well_map)
    connect(world, RegionName.krools_keep, RegionName.castle_crush_map)
    connect(world, RegionName.krools_keep, RegionName.clappers_cavern_map)
    connect(world, RegionName.krools_keep, RegionName.chain_link_chamber_map)
    connect(world, RegionName.krools_keep, RegionName.toxic_tower_map)
    connect(world, RegionName.krools_keep, RegionName.stronghold_showdown_map)
    
    connect(world, RegionName.the_flying_krock, RegionName.screechs_sprint_map)
    if world.options.goal != Goal.option_lost_world:
        connect(world, RegionName.the_flying_krock, RegionName.k_rool_duel_map)
        connect(world, RegionName.k_rool_duel_map, RegionName.k_rool_duel_level)
    
    connect(world, RegionName.lost_world_cauldron, RegionName.jungle_jinx_map)
    connect(world, RegionName.lost_world_quay, RegionName.black_ice_battle_map)
    connect(world, RegionName.lost_world_kremland, RegionName.klobber_karnage_map)
    connect(world, RegionName.lost_world_gulch, RegionName.fiery_furnace_map)
    connect(world, RegionName.lost_world_keep, RegionName.animal_antics_map)
    
    if world.options.goal != Goal.option_flying_krock:
        connect(world, RegionName.lost_world_cauldron, RegionName.krocodile_core_map)
        connect(world, RegionName.lost_world_quay, RegionName.krocodile_core_map)
        connect(world, RegionName.lost_world_kremland, RegionName.krocodile_core_map)
        connect(world, RegionName.lost_world_gulch, RegionName.krocodile_core_map)
        connect(world, RegionName.lost_world_keep, RegionName.krocodile_core_map)
        connect(world, RegionName.krocodile_core_map, RegionName.krocodile_core_level)

    for map_level, level in world.level_connections.items():
        connect(world, map_level, level)


def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = DKC2Location(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret


def add_event_to_region(multiworld: MultiWorld, player: int, region_name: str, event_name: str, event_item=None):
    region = multiworld.get_region(region_name, player)
    event = DKC2Location(player, event_name, None, region)
    if event_item:
        event.place_locked_item(DKC2Item(event_item, ItemClassification.progression, None, player))
    else:
        event.place_locked_item(DKC2Item(event_name, ItemClassification.progression, None, player))
    region.locations.append(event)


def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str):
    region = multiworld.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = DKC2Location(player, location_name, loc_id, region)
        region.locations.append(location)


def connect(world: World, source: str, target: str):
    source_region: Region = world.multiworld.get_region(source, world.player)
    target_region: Region = world.multiworld.get_region(target, world.player)
    source_region.connect(target_region)
