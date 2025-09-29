from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import (add_events, add_locations, connect_regions, can_pass_enemy, has_explosives, can_open_underwater_chest, 
                                         can_cut_shrubs, blast_or_smash, can_break_pots, has_item, take_damage,can_use, small_keys, can_get_enemy_drop, 
                                         can_detonate_upright_bomb_flower, has_fire_source_with_torch, can_kill_enemy, can_do_trick, can_get_deku_baba_nuts, can_get_deku_baba_sticks, is_child)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    BOTTOM_OF_THE_WELL_LOWERED_WATER = "Bottom of the Well Lowered Water"
    BOTTOM_OF_THE_WELL_NUT_POT = "Bottom of the Well Nut Pot"
    BOTTOM_OF_THE_WELL_STICK_POT = "Bottom of the Well Stick Pot"
    BOTTOM_OF_THE_WELL_BABAS_STICKS = "Bottom of the Well Deku Baba Sticks"
    BOTTOM_OF_THE_WELL_BABAS_NUTS = "Bottom of the Well Deku Baba Nuts"


class LocalEvents(str, Enum):
    LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL = "Water was lowered in the Bottom of the Well"


def set_region_rules(world: "SohWorld") -> None:
    player = world.player
    
    # TODO: Temporary to test generation
    connect_regions(Regions.KOKIRI_FOREST, world, [
        [Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, lambda state: True]
    ])
    connect_regions(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, world, [
        [Regions.KOKIRI_FOREST, lambda state: True]
    ])

    ## Bottom of The Well Entryway
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, world, [])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda state: is_child(state, world) and can_pass_enemy(state, world, Enemies.BIG_SKULLTULA)], # Technically involves an fake wall, but passing it lensless is intended in vanilla and it is well telegraphed
        #[Regions.BOTTOM_OF_THE_WELL_MQ_PERIMETER, lambda state: is_child(state, world)],
        [Regions.KAK_WELL, lambda state: True]
    ])

    ## Bottom of the Well Perimeter
    # Events
    add_events(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        [EventLocations.BOTTOM_OF_THE_WELL_STICK_POT, Events.STICK_POT, lambda state: True],
        [EventLocations.BOTTOM_OF_THE_WELL_NUT_POT, Events.NUT_POT, lambda state: True],
        [EventLocations.BOTTOM_OF_THE_WELL_LOWERED_WATER, LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, lambda state: can_use(Items.ZELDAS_LULLABY, state, world)]
    ])
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        [Locations.BOTTOM_OF_THE_WELL_FRONT_CENTER_BOMBABLE_CHEST, lambda state: has_explosives(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_FRONT_CHEST, lambda state: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, state, world) or can_open_underwater_chest(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_LEFT_CHEST, lambda state: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, state, world) or can_open_underwater_chest(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT1, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT2, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_UNDERWATER_POT, lambda state: (can_break_pots(state, world) and has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, state, world)) or can_use(Items.BOOMERANG, state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        [Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, lambda state: is_child(state, world) and can_pass_enemy(state, world, Enemies.BIG_SKULLTULA)],
        [Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, lambda state: is_child(state, world) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, lambda state: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, state, world) or has_item(Items.BRONZE_SCALE, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, lambda state: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, state, world) and is_child(state, world)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda state: True]
    ])

    ## Bottom of the Well Behind Fake Walls
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, world, [
        [Locations.BOTTOM_OF_THE_WELL_FRONT_LEFT_FAKE_WALL_CHEST, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_RIGHT_BOTTOM_FAKE_WALL_CHEST, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_COMPASS_CHEST, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_CENTER_SKULLTULA_CHEST, lambda state: can_pass_enemy(state, world, Enemies.BIG_SKULLTULA) or take_damage(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BACK_LEFT_BOMBABLE_CHEST, lambda state: has_explosives(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, lambda state: small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda state: True],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)]
    ])

    ## Bottom of the Well Southwest Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, world, [
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT1, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT2, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT3, lambda state: can_break_pots(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)]
    ])

    ## Bottom of the Well Keese-Beamos Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, world, [
        [Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_CHEST, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_POT1, lambda state: can_break_pots(state, world) and can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda state: is_child(state, world) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world) and can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)]
    ])

    ## Bottom of the Well Like-Like Cage
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, world, [
        [Locations.BOTTOM_OF_THE_WELL_LIKE_LIKE_CHEST, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_GS_LIKE_LIKE_CAGE, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, world, [
        [Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, lambda state: True]
    ])

    ## Bottom of the Well Inner Rooms 
    # Events
    add_events(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        [EventLocations.BOTTOM_OF_THE_WELL_BABAS_STICKS, Events.DEKU_BABA_STICKS, lambda state: can_get_deku_baba_sticks(state, world)],
        [EventLocations.BOTTOM_OF_THE_WELL_BABAS_NUTS, Events.DEKU_BABA_NUTS, lambda state: can_get_deku_baba_nuts(state, world)]
    ])
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        [Locations.BOTTOM_OF_THE_WELL_GS_WEST_INNER_ROOM, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)],
        [Locations.BOTTOM_OF_THE_WELL_GS_EAST_INNER_ROOM, lambda state: can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        [Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, lambda state: small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, state, world)]
    ])

    ## Bottom of the Well Coffin Room 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, world, [
        [Locations.BOTTOM_OF_THE_WELL_FREESTANDING_KEY, lambda state: has_fire_source_with_torch(state, world) or can_use(Items.PROGRESSIVE_BOW, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_FRONT_LEFT_HEART, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_MIDDLE_RIGHT_HEART, lambda state: has_fire_source_with_torch(state, world) or can_use(Items.PROGRESSIVE_BOW, state, world)]

    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda state: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, state, world) or has_item(Items.BRONZE_SCALE, state, world)]
    ])

    ## Bottom of the Well Dead Hand Room 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, world, [
        [Locations.BOTTOM_OF_THE_WELL_LENS_OF_TRUTH_CHEST, lambda state: can_kill_enemy(state, world, Enemies.DEAD_HAND)],
        [Locations.BOTTOM_OF_THE_WELL_INVISIBLE_CHEST, lambda state: can_do_trick("RT LENS BOTW", state, world) or can_use(Items.LENS_OF_TRUTH, state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, world, [
        [Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda state: is_child(state, world) and can_kill_enemy(state, world, Enemies.DEAD_HAND)]
    ])

    ## Bottom of the Well Basement 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT, world, [
        [Locations.BOTTOM_OF_THE_WELL_MAP_CHEST, lambda state: blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT1, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT2, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT3, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT4, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT5, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT6, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT7, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT8, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT9, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT10, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT11, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT12, lambda state: can_break_pots(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_MQ_BASEMENT_SUNS_SONG_FAIRY, lambda state: can_use(Items.SUNS_SONG, state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS2, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS3, lambda state: can_cut_shrubs(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS1, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS2, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS3, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS4, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS5, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS6, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS7, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS8, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS9, lambda state: can_cut_shrubs(state, world) and blast_or_smash(state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT, world, [
        [Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, lambda state: is_child(state, world) and can_pass_enemy(state, world, Enemies.BIG_SKULLTULA)],
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, lambda state: blast_or_smash(state, world) or can_use(Items.DINS_FIRE, state, world) or (can_use(Items.STICKS, state, world) and can_do_trick("RT BOTW Basement", state, world))]
    ])

    ## Bottom of the Well Useful Bomb Flowers
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, world, [
        [Locations.BOTTOM_OF_THE_WELL_MAP_CHEST, lambda state: has_item(Items.GORONS_BRACELET, state, world)]
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, world, [
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda state: can_detonate_upright_bomb_flower(state, world)]
    ])

    ## Bottom of the Well Basement Platform
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, world, [
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_LEFT_RUPEE, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_LEFT_RUPEE, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_MIDDLE_RUPEE, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_RIGHT_RUPEE, lambda state: True],
        [Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_RIGHT_RUPEE, lambda state: True],
        
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, world, [
        [Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda state: True]
    ])