from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    BOTTOM_OF_THE_WELL_LOWERED_WATER = "Bottom of the Well Lowered Water"
    BOTTOM_OF_THE_WELL_NUT_POT = "Bottom of the Well Nut Pot"
    BOTTOM_OF_THE_WELL_STICK_POT = "Bottom of the Well Stick Pot"
    BOTTOM_OF_THE_WELL_BABAS_STICKS = "Bottom of the Well Deku Baba Sticks"
    BOTTOM_OF_THE_WELL_BABAS_NUTS = "Bottom of the Well Deku Baba Nuts"


class LocalEvents(StrEnum):
    LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL = "Water was lowered in the Bottom of the Well"


def set_region_rules(world: "SohWorld") -> None:
    # Bottom of The Well Entryway
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, world, [])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, world, [
        # Technically involves an fake wall, but passing it lensless is intended in vanilla and it is well telegraphed
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda bundle: is_child(
            bundle) and can_pass_enemy(bundle, Enemies.BIG_SKULLTULA)),
        # [Regions.BOTTOM_OF_THE_WELL_MQ_PERIMETER, lambda bundle: is_child(bundle),
        (Regions.KAK_WELL, lambda bundle: True)
    ])

    # Bottom of the Well Perimeter
    # Events
    add_events(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        (EventLocations.BOTTOM_OF_THE_WELL_STICK_POT,
         Events.CAN_FARM_STICKS, lambda bundle: True),
        (EventLocations.BOTTOM_OF_THE_WELL_NUT_POT,
         Events.CAN_FARM_NUTS, lambda bundle: True),
        (EventLocations.BOTTOM_OF_THE_WELL_LOWERED_WATER, LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        (Locations.BOTTOM_OF_THE_WELL_FRONT_CENTER_BOMBABLE_CHEST,
         lambda bundle: has_explosives(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_UNDERWATER_FRONT_CHEST, lambda bundle: has_item(
            LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, bundle) or can_open_underwater_chest(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_UNDERWATER_LEFT_CHEST, lambda bundle: has_item(
            LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, bundle) or can_open_underwater_chest(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_NEAR_ENTRANCE_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_UNDERWATER_POT, lambda bundle: (can_break_pots(bundle) and has_item(
            LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, bundle)) or can_use(Items.BOOMERANG, bundle))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_PERIMETER, world, [
        (Regions.BOTTOM_OF_THE_WELL_ENTRYWAY, lambda bundle: is_child(
            bundle) and can_pass_enemy(bundle, Enemies.BIG_SKULLTULA)),
        (Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)),
        (Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)),
        (Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, lambda bundle: is_child(
            bundle) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, bundle)),
        (Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, lambda bundle: has_item(
            LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, bundle) or has_item(Items.BRONZE_SCALE, bundle)),
        (Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, lambda bundle: has_item(
            LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, bundle) and is_child(bundle)),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda bundle: True)
    ])

    # Bottom of the Well Behind Fake Walls
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, world, [
        (Locations.BOTTOM_OF_THE_WELL_FRONT_LEFT_FAKE_WALL_CHEST, lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_RIGHT_BOTTOM_FAKE_WALL_CHEST, lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_COMPASS_CHEST, lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_CENTER_SKULLTULA_CHEST, lambda bundle: can_pass_enemy(
            bundle, Enemies.BIG_SKULLTULA) or take_damage(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BACK_LEFT_BOMBABLE_CHEST,
         lambda bundle: has_explosives(bundle))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)),
        (Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, lambda bundle: small_keys(
            Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, bundle)),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda bundle: True),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle))
    ])

    # Bottom of the Well Southwest Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, world, [
        (Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_LEFT_SIDE_POT3,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle))
    ])

    # Bottom of the Well Keese-Beamos Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, world, [
        (Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_CHEST, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)),
        (Locations.BOTTOM_OF_THE_WELL_FIRE_KEESE_POT1, lambda bundle: can_break_pots(bundle)
         and can_do_trick(Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda bundle: is_child(bundle) and small_keys(Items.BOTTOM_OF_THE_WELL_SMALL_KEY,
         3, bundle) and can_do_trick(Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)),
        (Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle))
    ])

    # Bottom of the Well Like-Like Cage
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, world, [
        (Locations.BOTTOM_OF_THE_WELL_LIKE_LIKE_CHEST, lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_GS_LIKE_LIKE_CAGE, lambda bundle: can_get_enemy_drop(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_LIKE_LIKE_CAGE, world, [
        (Regions.BOTTOM_OF_THE_WELL_KEESE_BEAMOS_ROOM, lambda bundle: True)
    ])

    # Bottom of the Well Inner Rooms
    # Events
    add_events(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        (EventLocations.BOTTOM_OF_THE_WELL_BABAS_STICKS, Events.CAN_FARM_STICKS,
         lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.BOTTOM_OF_THE_WELL_BABAS_NUTS, Events.CAN_FARM_NUTS,
         lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        (Locations.BOTTOM_OF_THE_WELL_GS_WEST_INNER_ROOM, lambda bundle: can_get_enemy_drop(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG)),
        (Locations.BOTTOM_OF_THE_WELL_GS_EAST_INNER_ROOM, lambda bundle: can_get_enemy_drop(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOOMERANG))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_INNER_ROOMS, world, [
        (Regions.BOTTOM_OF_THE_WELL_BEHIND_FAKE_WALLS, lambda bundle: small_keys(
            Items.BOTTOM_OF_THE_WELL_SMALL_KEY, 3, bundle))
    ])

    # Bottom of the Well Coffin Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, world, [
        (Locations.BOTTOM_OF_THE_WELL_FREESTANDING_KEY, lambda bundle: has_fire_source_with_torch(
            bundle) or can_use(Items.FAIRY_BOW, bundle)),
        (Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_FRONT_LEFT_HEART, lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_COFFIN_ROOM_MIDDLE_RIGHT_HEART,
         lambda bundle: has_fire_source_with_torch(bundle) or can_use(Items.FAIRY_BOW, bundle))

    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_COFFIN_ROOM, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda bundle: has_item(
            LocalEvents.LOWERED_WATER_INSIDE_BOTTOM_OF_THE_WELL, bundle) or has_item(Items.BRONZE_SCALE, bundle))
    ])

    # Bottom of the Well Dead Hand Room
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, world, [
        (Locations.BOTTOM_OF_THE_WELL_LENS_OF_TRUTH_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.DEAD_HAND)),
        (Locations.BOTTOM_OF_THE_WELL_INVISIBLE_CHEST, lambda bundle: can_do_trick(
            Tricks.LENS_BOTW, bundle) or can_use(Items.LENS_OF_TRUTH, bundle))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_DEAD_HAND_ROOM, world, [
        (Regions.BOTTOM_OF_THE_WELL_PERIMETER, lambda bundle: is_child(
            bundle) and can_kill_enemy(bundle, Enemies.DEAD_HAND))
    ])

    # Bottom of the Well Basement
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT, world, [
        (Locations.BOTTOM_OF_THE_WELL_MAP_CHEST,
         lambda bundle: blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT4,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT5,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT6,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT7,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT8,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT9,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT10,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT11,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_POT12,
         lambda bundle: can_break_pots(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_SUNS_SONG_FAIRY,
         lambda bundle: can_use(Items.SUNS_SONG, bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS1,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS2,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_GRASS3,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS1,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS2,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS3,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS4,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS5,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS6,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS7,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS8,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle)),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_BEHIND_ROCKS_GRASS9,
         lambda bundle: can_cut_shrubs(bundle) and blast_or_smash(bundle))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT, world, [
        (Regions.BOTTOM_OF_THE_WELL_SOUTHWEST_ROOM, lambda bundle: is_child(
            bundle) and can_pass_enemy(bundle, Enemies.BIG_SKULLTULA)),
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, lambda bundle: blast_or_smash(bundle) or can_use(
            Items.DINS_FIRE, bundle) or (can_use(Items.STICKS, bundle) and can_do_trick(Tricks.BOTW_BASEMENT, bundle)))
    ])

    # Bottom of the Well Useful Bomb Flowers
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, world, [
        (Locations.BOTTOM_OF_THE_WELL_MAP_CHEST,
         lambda bundle: has_item(Items.GORONS_BRACELET, bundle))
    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_USEFUL_BOMB_FLOWERS, world, [
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT,
         lambda bundle: can_detonate_upright_bomb_flower(bundle))
    ])

    # Bottom of the Well Basement Platform
    # Locations
    add_locations(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, world, [
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_LEFT_RUPEE, lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_LEFT_RUPEE,
         lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_MIDDLE_RUPEE, lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_BACK_RIGHT_RUPEE,
         lambda bundle: True),
        (Locations.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM_RIGHT_RUPEE, lambda bundle: True),

    ])
    # Connections
    connect_regions(Regions.BOTTOM_OF_THE_WELL_BASEMENT_PLATFORM, world, [
        (Regions.BOTTOM_OF_THE_WELL_BASEMENT, lambda bundle: True)
    ])
