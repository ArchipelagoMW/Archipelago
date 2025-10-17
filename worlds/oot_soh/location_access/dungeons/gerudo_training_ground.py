from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


def set_region_rules(world: "SohWorld") -> None:
    # Gerudo Training Ground Entryway
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_ENTRYWAY, world, [
        (Regions.GERUDO_TRAINING_GROUND_LOBBY, lambda bundle: True),
        (Regions.GF_EXITING_GTG, lambda bundle: True),
    ])

    # Gerudo Training Ground Lobby
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_LOBBY, world, [
        (Locations.GERUDO_TRAINING_GROUND_LOBBY_LEFT_CHEST,
         lambda bundle: can_hit_eye_targets(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_LOBBY_RIGHT_CHEST,
         lambda bundle: can_hit_eye_targets(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_STALFOS_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2, True)),
        (Locations.GERUDO_TRAINING_GROUND_BEAMOS_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.BEAMOS) and can_kill_enemy(bundle, Enemies.DINOLFOS,
                                                                                  EnemyDistance.CLOSE, True, 2, True)),
        (Locations.GERUDO_TRAINING_GROUND_ENTRANCE_SONG_OF_STORMS_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.GERUDO_TRAINING_GROUND_BEAMOS_EAST_HEART, lambda bundle: True),
        (Locations.GERUDO_TRAINING_GROUND_BEAMOS_SOUTH_HEART, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_LOBBY, world, [
        (Regions.GERUDO_TRAINING_GROUND_ENTRYWAY, lambda bundle: True),
        (Regions.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2, True) and (
             can_use(Items.HOOKSHOT, bundle) or can_do_trick(Tricks.GTG_WITHOUT_HOOKSHOT, bundle))),
        (Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.BEAMOS) and can_kill_enemy(bundle, Enemies.DINOLFOS,
                                                                                  EnemyDistance.CLOSE, True, 2, True)),
        (Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE, lambda bundle: True),
    ])

    # Gerudo Training Ground Central Maze
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE, world, [
        (Locations.GERUDO_TRAINING_GROUND_HIDDEN_CEILING_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 3, bundle) and (
             can_use(Items.LENS_OF_TRUTH, bundle) or can_do_trick(Tricks.LENS_GTG, bundle))),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_FIRST_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 4, bundle)),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_SECOND_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 6, bundle)),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_THIRD_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 7, bundle)),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_FINAL_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 9, bundle)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE, world, [
        (Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE_RIGHT,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 9, bundle)),
    ])

    # Gerudo Training Ground Central Maze Right
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE_RIGHT, world, [
        (Locations.GERUDO_TRAINING_GROUND_FREESTANDING_KEY, lambda bundle: True),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_RIGHT_SIDE_CHEST, lambda bundle: True),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_RIGHT_CENTRAL_CHEST, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE_RIGHT, world, [
        (Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM,
         lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM, lambda bundle: True),
    ])

    # Gerudo Training Ground Lava Room
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM, world, [
        (Locations.GERUDO_TRAINING_GROUND_UNDERWATER_SILVER_RUPEE_CHEST,
         lambda bundle: can_use(Items.HOOKSHOT, bundle) and can_use(Items.SONG_OF_TIME, bundle) and can_use(
             Items.IRON_BOOTS, bundle) and water_timer(bundle) >= 24),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM, world, [
        (Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE_RIGHT,
         lambda bundle: can_use(Items.SONG_OF_TIME, bundle) or is_child(bundle)),
        (Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM, lambda bundle: can_use(Items.LONGSHOT, bundle) or (
            can_use(Items.HOVER_BOOTS, bundle) and can_use(Items.HOOKSHOT, bundle))),
    ])

    # Gerudo Training Ground Hammer Room
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM, world, [
        (Locations.GERUDO_TRAINING_GROUND_HAMMER_ROOM_CLEAR_CHEST,
         lambda bundle: can_attack(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_HAMMER_ROOM_SWITCH_CHEST,
         lambda bundle: can_use(Items.MEGATON_HAMMER, bundle) or (
             take_damage(bundle) and can_do_trick(Tricks.FLAMING_CHESTS, bundle))),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM, world, [
        (Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_LOWER, lambda bundle: can_use(
            Items.MEGATON_HAMMER, bundle) and can_use(Items.FAIRY_BOW, bundle)),
        (Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM, lambda bundle: True),
    ])

    # Gerudo Training Ground Eye Statue Lower
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_LOWER, world, [
        (Locations.GERUDO_TRAINING_GROUND_EYE_STATUE_CHEST,
         lambda bundle: can_use(Items.FAIRY_BOW, bundle)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_LOWER, world, [
        (Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM, lambda bundle: True),
    ])

    # Gerudo Training Ground Eye Statue Upper
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_UPPER, world, [
        (Locations.GERUDO_TRAINING_GROUND_NEAR_SCARECROW_CHEST,
         lambda bundle: can_use(Items.FAIRY_BOW, bundle)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_UPPER, world, [
        (Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_LOWER, lambda bundle: True),
    ])

    # Gerudo Training Ground Heavy Block Room
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_ROOM, world, [
        (Locations.GERUDO_TRAINING_GROUND_BEFORE_HEAVY_BLOCK_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.WOLFOS, EnemyDistance.CLOSE, True, 4, True)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_ROOM, world, [
        (Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_UPPER,
         lambda bundle: (can_do_trick(Tricks.LENS_GTG, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)) and (
             can_use(Items.HOOKSHOT, bundle) or (
                 is_adult(bundle) and (
                     can_do_trick(Tricks.GTG_FAKE_WALL, bundle) and can_use(Items.HOVER_BOOTS, bundle))) or can_ground_jump(bundle))),
        (Regions.GERUDO_TRAINING_GROUND_LIKE_LIKE_ROOM,
         lambda bundle: (can_do_trick(Tricks.LENS_GTG, bundle) or can_use(Items.LENS_OF_TRUTH, bundle)) and (
             can_use(Items.HOOKSHOT, bundle) or (
                 is_adult(bundle) and (
                     can_do_trick(Tricks.GTG_FAKE_WALL, bundle) and can_use(Items.HOVER_BOOTS, bundle)) or can_ground_jump(bundle))) and can_use(Items.SILVER_GAUNTLETS, bundle)),
    ])

    # Gerudo Training Ground Like Like Room
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_LIKE_LIKE_ROOM, world, [
        (Locations.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_FIRST_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_SECOND_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_THIRD_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_FOURTH_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
    ])
