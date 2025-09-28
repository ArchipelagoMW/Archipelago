from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import *
from worlds.oot_soh.LogicHelpers import (add_events, add_locations, connect_regions, can_pass_enemy, has_explosives, lens_or_skip, can_open_underwater_chest, 
                                         can_cut_shrubs, blast_or_smash, can_break_pots, has_item, take_damage,can_use, small_keys, can_get_enemy_drop, 
                                         can_detonate_upright_bomb_flower, has_fire_source_with_torch, can_kill_enemy, can_do_trick)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
    ## Bottom of The Well Entryway
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY.value, world, [])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: is_child(state, world) and can_pass_enemy(state, world, Enemies.BIG_SKULLTULA.value)], # Technically involves an fake wall, but passing it lensless is intended in vanilla and it is well telegraphed
        #[Regions.BOTTOM_OF_THE_WELL_MQ_PERIMETER.value, lambda state: is_child(state, world)],
        [Regions.KAK_WELL.value, lambda state: True]
    ])

    ## Bottom of the Well Perimeter
    # Events
    add_events(Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, world, [
        [EventLocations.BOTTOM_OF_THE_WELL_STICK_POT.value, Events.STICK_POT.value, lambda state: True],
        [EventLocations.BOTTOM_OF_THE_WELL_NUT_POT.value, Events.NUT_POT.value, lambda state: True],
        [EventLocations.BOTTOM_OF_THE_WELL_LOWERED_WATER.value, Events.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL.value, lambda state: can_use(Items.ZELDAS_LULLABY.value, state, world)]
    ])
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_FRONT_CENTER_BOMBABLE_CHEST.value, lambda state: has_explosives(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_FRONT_CHEST.value, lambda state: state.has(Events.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL) or can_open_underwater_chest(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_LEFT_CHEST.value, lambda state: state.has(Events.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL) or can_open_underwater_chest(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT1.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT2.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_POT.value, lambda state: (can_break_pots(state, world) and state.has(Events.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL)) or can_use(Items.BOOMERANG.value, state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_ENTRYWAY.value, lambda state: is_child(state, world) and can_pass_enemy(state, world, Enemies.BIG_SKULLTULA.value)],
        [Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS.value, lambda state: lens_or_skip("RT LENS BOTW", state, world)],
        [Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM.value, lambda state: lens_or_skip("RT LENS BOTW",state, world)],
        [Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM.value, lambda state: is_child(state, world) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM.value, lambda state: state.has(Events.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL) or has_item(Items.BRONZE_SCALE.value, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM.value, lambda state: state.has(Events.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL) and is_child(state, world)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, lambda state: True]
    ])

    ## Bottom of the Well Behind Fake Walls
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_FRONT_LEFT_FAKE_WALL_CHEST.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_RIGHT_BOTTOM_FAKE_WALL_CHEST.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_COMPASS_CHEST.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_CENTER_SKULLTULA_CHEST.value, lambda state: can_pass_enemy(Enemies.BIG_SKULLTULA.value, state, world) or take_damage(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BACK_LEFT_BOMBABLE_CHEST.value, lambda state: has_explosives(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: lens_or_skip("RT LENS BOTW",state, world)],
        [Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS.value, lambda state: small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, lambda state: True],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM.value, lambda state: lens_or_skip("RT LENS BOTW",state, world)]
    ])

    ## Bottom of the Well Southwest Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT1.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT2.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT3.value, lambda state: can_break_pots(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: lens_or_skip("RT LENS BOTW",state, world)]
    ])

    ## Bottom of the Well Keese-Beamos Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_CHEST.value, lambda state: lens_or_skip("RT LENS BOTW",state, world)],
        [Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_POT1.value, lambda state: can_break_pots(state, world) and lens_or_skip("RT LENS BOTW",state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: is_child(state, world) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world) and lens_or_skip("RT LENS BOTW",state, world)],
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: lens_or_skip("RT LENS BOTW",state, world)],
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: lens_or_skip("RT LENS BOTW",state, world)]
    ])

    ## Bottom of the Well Like-Like Cage
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_LIKE_LIKE_CHEST.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_GS_LIKE_LIKE_CAGE.value, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM.value, lambda state: True]
    ])

    ## Bottom of the Well Inner Rooms 
    # Events
    add_events(Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, world, [
        [EventLocations.BOTTOM_OF_THE_WELL_BABAS.value, Events.DEKU_BABA_STICKS.value, lambda state: can_get_deku_baba_sticks(state, world)],
        [EventLocations.BOTTOM_OF_THE_WELL_BABAS.value, Events.DEKU_BABA_NUTS.value, lambda state: can_get_deku_baba_nuts(state, world)]
    ])
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_GS_WEST_INNER_ROOM.value, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)],
        [Locations.BOTTOM_OF_THE_WELL_GS_EAST_INNER_ROOM.value, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS.value, lambda state: small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)]
    ])

    ## Bottom of the Well Coffin Room 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_FREESTANDING_KEY.value, lambda state: has_fire_source_with_torch(state, world) or can_use(Items.PROGRESSIVE_BOW.value, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_FRONT_LEFT_HEART.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_MIDDLE_RIGHT_HEART.value, lambda state: has_fire_source_with_torch(state, world) or can_use(Items.PROGRESSIVE_BOW.value, state, world)]

    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: state.has(Events.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL) or has_item(Items.BRONZE_SCALE.value, state, world)]
    ])

    ## Bottom of the Well Dead Hand Room 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_LENS_OF_TRUTH_CHEST.value, lambda state: can_kill_enemy(Enemies.DEAD_HAND.value, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_INVISIBLE_CHEST.value, lambda state: lens_or_skip("RT LENS BOTW",state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER.value, lambda state: is_child(state, world) and can_kill_enemy(Enemies.DEAD_HAND.value, state, world)]
    ])

    ## Bottom of the Well Basement 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_MAP_CHEST.value, lambda state: blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT1.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT2.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT3.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT4.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT5.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT6.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT7.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT8.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT9.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT10.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT11.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT12.value, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_MQ_BASEMENT_SUNS_SONG_FAIRY.value, lambda state: can_use(Items.SUNS_SONG.value, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS1.value, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS2.value, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS3.value, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS1.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS2.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS3.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS4.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS5.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS6.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS7.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS8.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS9.value, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM.value, lambda state: is_child(state, world) and can_pass_enemy(Enemies.BIG_SKULLTULA.value, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS.value, lambda state: blast_or_smash(state, world) or can_use(Items.DINS_FIRE.value, state, world) or (can_use(Items.STICKS.value) and can_do_trick("RT BOTW Basement", state, world))] # NOT 100% SURE HOW TO TRANSLATE HERE. Has to do with Age: Entrance(RR_BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, []{return Here(RR_BOTTOM_OF_THE_WELL_BASEMENT, []{return logic->BlastOrSmash() || logic->CanUse(RG_DINS_FIRE) || (logic->CanUse(RG_STICKS) && ctx->GetTrickOption(RT_BOTW_BASEMENT));});}),
    ])

    ## Bottom of the Well Useful Bomb Flowers
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_MAP_CHEST.value, lambda state: has_item(Items.GORONS_BRACELET.value, state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, lambda state: can_detonate_upright_bomb_flower(state, world)]
    ])

    ## Bottom of the Well Basement Platform
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM.value, world, [
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_LEFT_RUPEE.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_LEFT_RUPEE.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_MIDDLE_RUPEE.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_RIGHT_RUPEE.value, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_RIGHT_RUPEE.value, lambda state: True],
        
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM.value, world, [
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT.value, lambda state: True]
    ])