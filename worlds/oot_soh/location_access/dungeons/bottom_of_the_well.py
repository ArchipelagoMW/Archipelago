from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

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
        (Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, lambda s, r, w: True)
    ])
    connect_regions(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, world, [
        (Regions.KOKIRI_FOREST, lambda s, r, w: True)
    ])

    ## Bottom of The Well Entryway
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, world, [])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda s, r, w: is_child(s, r, world) and can_pass_enemy(s, world, Enemies.BIG_SKULLTULA)), # Technically involves an fake wall, but passing it lensless is intended in vanilla and it is well telegraphed
        #[Regions.BOTTOM_OF_THE_WELL_MQ_PERIMETER, lambda s, r, w: is_child(s, w),
        (Regions.KAK_WELL, lambda s, r, w: True)
    ])

    ## Bottom of the Well Perimeter
    # Events
    add_events(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        (EventLocations.BOTTOM_OF_THE_WELL_STICK_POT, Events.STICK_POT, lambda s, r, w: True),
        (EventLocations.BOTTOM_OF_THE_WELL_NUT_POT, Events.NUT_POT, lambda s, r, w: True),
        (EventLocations.BOTTOM_OF_THE_WELL_LOWERED_WATER, LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, lambda s, r, w: can_use(Items.ZELDAS_LULLABY, s, w))
    ])
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        (Locations.BOTTOM_OF_THE_WELL_FRONT_CENTER_BOMBABLE_CHEST, lambda s, r, w: has_explosives(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_UNDERWATER_FRONT_CHEST, lambda s, r, w: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, s, w) or can_open_underwater_chest(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_UNDERWATER_LEFT_CHEST, lambda s, r, w: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, s, w) or can_open_underwater_chest(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT1, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT2, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_UNDERWATER_POT, lambda s, r, w: (can_break_pots(s, w) and has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, s, w)) or can_use(Items.BOOMERANG, s, w))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        (Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, lambda s, r, w: is_child(s, r, world) and can_pass_enemy(s, world, Enemies.BIG_SKULLTULA)),
        (Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w)),
        (Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w)),
        (Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, lambda s, r, w: is_child(s, r, world) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, s, w)),
        (Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, lambda s, r, w: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, s, w) or has_item(Items.BRONZE_SCALE, s, w)),
        (Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, lambda s, r, w: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, s, w) and is_child(s, r, world)),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda s, r, w: True)
    ])

    ## Bottom of the Well Behind Fake Walls
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, world, [
        (Locations.BOTTOM_OF_THE_WELL_FRONT_LEFT_FAKE_WALL_CHEST, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_RIGHT_BOTTOM_FAKE_WALL_CHEST, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_COMPASS_CHEST, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_CENTER_SKULLTULA_CHEST, lambda s, r, w: can_pass_enemy(s, world, Enemies.BIG_SKULLTULA) or take_damage(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BACK_LEFT_BOMBABLE_CHEST, lambda s, r, w: has_explosives(s, w))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w)),
        (Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, lambda s, r, w: small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, s, w)),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda s, r, w: True),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w))
    ])

    ## Bottom of the Well Southwest Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, world, [
        (Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT1, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT2, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT3, lambda s, r, w: can_break_pots(s, w))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w))
    ])

    ## Bottom of the Well Keese-Beamos Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, world, [
        (Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_CHEST, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w)),
        (Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_POT1, lambda s, r, w: can_break_pots(s, w) and can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda s, r, w: is_child(s, r, world) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, s, w) and can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w)),
        (Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w)),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w))
    ])

    ## Bottom of the Well Like-Like Cage
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, world, [
        (Locations.BOTTOM_OF_THE_WELL_LIKE_LIKE_CHEST, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_GS_LIKE_LIKE_CAGE, lambda s, r, w: can_get_enemy_drop(s, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, world, [
        (Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, lambda s, r, w: True)
    ])

    ## Bottom of the Well Inner Rooms 
    # Events
    add_events(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        (EventLocations.BOTTOM_OF_THE_WELL_BABAS_STICKS, Events.DEKU_BABA_STICKS, lambda s, r, w: can_get_deku_baba_sticks(s, w)),
        (EventLocations.BOTTOM_OF_THE_WELL_BABAS_NUTS, Events.DEKU_BABA_NUTS, lambda s, r, w: can_get_deku_baba_nuts(s, w))
    ])
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        (Locations.BOTTOM_OF_THE_WELL_GS_WEST_INNER_ROOM, lambda s, r, w: can_get_enemy_drop(s, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)),
        (Locations.BOTTOM_OF_THE_WELL_GS_EAST_INNER_ROOM, lambda s, r, w: can_get_enemy_drop(s, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        (Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, lambda s, r, w: small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, s, w))
    ])

    ## Bottom of the Well Coffin Room 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, world, [
        (Locations.BOTTOM_OF_THE_WELL_FREESTANDING_KEY, lambda s, r, w: has_fire_source_with_torch(s, w) or can_use(Items.PROGRESSIVE_BOW, s, w)),
        (Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_FRONT_LEFT_HEART, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_MIDDLE_RIGHT_HEART, lambda s, r, w: has_fire_source_with_torch(s, w) or can_use(Items.PROGRESSIVE_BOW, s, w))

    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda s, r, w: has_item(LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, s, w) or has_item(Items.BRONZE_SCALE, s, w))
    ])

    ## Bottom of the Well Dead Hand Room 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, world, [
        (Locations.BOTTOM_OF_THE_WELL_LENS_OF_TRUTH_CHEST, lambda s, r, w: can_kill_enemy(s, world, Enemies.DEAD_HAND)),
        (Locations.BOTTOM_OF_THE_WELL_INVISIBLE_CHEST, lambda s, r, w: can_do_trick("RT LENS BOTW", s, w) or can_use(Items.LENS_OF_TRUTH, s, w))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda s, r, w: is_child(s, r, world) and can_kill_enemy(s, world, Enemies.DEAD_HAND))
    ])

    ## Bottom of the Well Basement 
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT, world, [
        (Locations.BOTTOM_OF_THE_WELL_MAP_CHEST, lambda s, r, w: blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT1, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT2, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT3, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT4, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT5, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT6, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT7, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT8, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT9, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT10, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT11, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT12, lambda s, r, w: can_break_pots(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_MQ_BASEMENT_SUNS_SONG_FAIRY, lambda s, r, w: can_use(Items.SUNS_SONG, s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS1, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS2, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS3, lambda s, r, w: can_cut_shrubs(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS1, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS2, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS3, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS4, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS5, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS6, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS7, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS8, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS9, lambda s, r, w: can_cut_shrubs(s, w) and blast_or_smash(s, w))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT, world, [
        (Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, lambda s, r, w: is_child(s, r, w) and can_pass_enemy(s, w, Enemies.BIG_SKULLTULA)),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, lambda s, r, w: blast_or_smash(s, w) or can_use(Items.DINS_FIRE, s, w) or (can_use(Items.STICKS, s, w) and can_do_trick("RT BOTW Basement", s, w)))
    ])

    ## Bottom of the Well Useful Bomb Flowers
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, world, [
        (Locations.BOTTOM_OF_THE_WELL_MAP_CHEST, lambda s, r, w: has_item(Items.GORONS_BRACELET, s, w))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, world, [
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda s, r, w: can_detonate_upright_bomb_flower(s, w))
    ])

    ## Bottom of the Well Basement Platform
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, world, [
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_LEFT_RUPEE, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_LEFT_RUPEE, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_MIDDLE_RUPEE, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_RIGHT_RUPEE, lambda s, r, w: True),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_RIGHT_RUPEE, lambda s, r, w: True),
        
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, world, [
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda s, r, w: True)
    ])