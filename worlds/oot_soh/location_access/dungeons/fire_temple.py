from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    FIRE_TEMPLE_NEAR_BOSS_ROOM_FAIRY_POT = "Fire Temple Near Boss Room Fairy Pot"
    FIRE_TEMPLE_LOOP_HAMMER_SWITCH_ROOM_SWITCH = "Fire Temple Loop Hammer Switch Room Switch"
    FIRE_TEMPLE_FIRE_MAZE_UPPER_PLATFORM = "Fire Temple Fire Maze Upper Platform"
    FIRE_TEMPLE_VOLVAGIA = "Fire Temple Volvagia"
    FIRE_TEMPLE_SHORTCUT_SWITCH = "Fire Temple Shortcut Switch"


class LocalEvents(StrEnum):
    FIRE_TEMPLE_LOOP_HAMMER_SWITCH_HIT = "Fire Temple Loop Hammer Switch Hit"
    FIRE_TEMPLE_FIRE_MAZE_UPPER_PLATFORM_HIT = "Fire Temple Fire Maze Upper Platform Hit"
    FIRE_TEMPLE_SHORTCUT_SWITCH_HIT = "Fire Temple Shortcut Switch Hit"


def set_region_rules(world: "SohWorld") -> None:
    # Fire Temple Entryway
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_ENTRYWAY, world, [
        (Regions.FIRE_TEMPLE_FIRST_ROOM, lambda bundle: True),
        (Regions.DMC_CENTRAL_LOCAL, lambda bundle: True)
    ])

    # Fire Temple First Room
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_FIRST_ROOM, world, [
        (Regions.FIRE_TEMPLE_ENTRYWAY, lambda bundle: True),
        (Regions.FIRE_TEMPLE_NEAR_BOSS_ROOM,
         lambda bundle: fire_timer(bundle) >= 24),
        (Regions.FIRE_TEMPLE_LOOP_ENEMIES, lambda bundle: (can_use(Items.MEGATON_HAMMER, bundle) and (
            small_keys(Items.FIRE_TEMPLE_SMALL_KEY, 8, bundle) or not is_fire_loop_locked(bundle)))),
        (Regions.FIRE_TEMPLE_LOOP_EXIT, lambda bundle: True),
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 2, bundle) and fire_timer(bundle) >= 24)
    ])

    # Fire Temple Near Boss Room
    # Events
    add_events(Regions.FIRE_TEMPLE_NEAR_BOSS_ROOM, world, [
        (EventLocations.FIRE_TEMPLE_NEAR_BOSS_ROOM_FAIRY_POT, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: can_use(Items.HOVER_BOOTS, bundle) or can_use(Items.HOOKSHOT, bundle))
    ])
    # Locations
    add_locations(Regions.FIRE_TEMPLE_NEAR_BOSS_ROOM, world, [
        (Locations.FIRE_TEMPLE_NEAR_BOSS_CHEST, lambda bundle: True),
        (Locations.FIRE_TEMPLE_NEAR_BOSS_POT1, lambda bundle:
            (can_break_pots(bundle) and
             (can_use(Items.HOVER_BOOTS, bundle) or can_use(Items.HOOKSHOT, bundle)))),
        (Locations.FIRE_TEMPLE_NEAR_BOSS_POT2, lambda bundle:
            (can_break_pots(bundle) and
             (can_use(Items.HOVER_BOOTS, bundle) or can_use(Items.HOOKSHOT, bundle)))),
        (Locations.FIRE_TEMPLE_NEAR_BOSS_POT3, lambda bundle:
            (can_break_pots(bundle) and
             (can_use(Items.HOVER_BOOTS, bundle) or can_use(Items.HOOKSHOT, bundle)))),
        (Locations.FIRE_TEMPLE_NEAR_BOSS_POT4, lambda bundle:
            (can_break_pots(bundle) and
             (can_use(Items.HOVER_BOOTS, bundle) or can_use(Items.HOOKSHOT, bundle)))),
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_NEAR_BOSS_ROOM, world, [
        (Regions.FIRE_TEMPLE_FIRST_ROOM, lambda bundle: True),
        (Regions.FIRE_TEMPLE_BOSS_ENTRYWAY, lambda bundle:
            (is_adult(bundle) and
             (can_do_trick(Tricks.FIRE_BOSS_DOOR_JUMP, bundle) or
              has_item(LocalEvents.FIRE_TEMPLE_FIRE_MAZE_UPPER_PLATFORM_HIT, bundle) or
              can_use(Items.HOVER_BOOTS, bundle))))
    ])

    # Fire Temple Loop Enemies
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_LOOP_ENEMIES, world, [
        (Regions.FIRE_TEMPLE_FIRST_ROOM, lambda bundle:
            (small_keys(Items.FIRE_TEMPLE_SMALL_KEY, 8, bundle) or not is_fire_loop_locked(bundle))),
        (Regions.FIRE_TEMPLE_LOOP_TILES, lambda bundle:
            (can_kill_enemy(bundle, Enemies.TORCH_SLUG) and
             can_kill_enemy(bundle, Enemies.FIRE_KEESE)))
    ])

    # Fire Temple Loop Tiles
    # Locations
    add_locations(Regions.FIRE_TEMPLE_LOOP_TILES, world, [
        (Locations.FIRE_TEMPLE_GS_BOSS_KEY_LOOP, lambda bundle: can_attack(bundle))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_LOOP_TILES, world, [
        (Regions.FIRE_TEMPLE_LOOP_ENEMIES, lambda bundle: True),
        (Regions.FIRE_TEMPLE_LOOP_FLARE_DANCER, lambda bundle: True)
    ])

    # Fire Temple Loop Flare Dancer
    # Locations
    add_locations(Regions.FIRE_TEMPLE_LOOP_FLARE_DANCER, world, [
        (Locations.FIRE_TEMPLE_FLARE_DANCER_CHEST, lambda bundle:
            (has_explosives(bundle) or can_use(Items.MEGATON_HAMMER, bundle)) and
            (is_adult(bundle) or can_ground_jump(bundle)))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_LOOP_FLARE_DANCER, world, [
        (Regions.FIRE_TEMPLE_LOOP_TILES, lambda bundle: True),
        (Regions.FIRE_TEMPLE_LOOP_HAMMER_SWITCH, lambda bundle:
            (can_kill_enemy(bundle, Enemies.FLARE_DANCER)))
    ])

    # Fire Temple Loop Hammer Switch
    # Events
    add_events(Regions.FIRE_TEMPLE_LOOP_HAMMER_SWITCH, world, [
        (EventLocations.FIRE_TEMPLE_LOOP_HAMMER_SWITCH_ROOM_SWITCH,
         LocalEvents.FIRE_TEMPLE_LOOP_HAMMER_SWITCH_HIT, lambda bundle: can_use(Items.MEGATON_HAMMER, bundle))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_LOOP_HAMMER_SWITCH, world, [
        (Regions.FIRE_TEMPLE_LOOP_FLARE_DANCER, lambda bundle: True),
        (Regions.FIRE_TEMPLE_LOOP_GORON_ROOM, lambda bundle: has_item(
            LocalEvents.FIRE_TEMPLE_LOOP_HAMMER_SWITCH_HIT, bundle))
    ])

    # Fire Temple Loop Goron Room
    # Locations
    add_locations(Regions.FIRE_TEMPLE_LOOP_GORON_ROOM, world, [
        (Locations.FIRE_TEMPLE_BOSS_KEY_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_LOOP_GORON_ROOM, world, [
        (Regions.FIRE_TEMPLE_LOOP_HAMMER_SWITCH, lambda bundle: has_item(
            LocalEvents.FIRE_TEMPLE_LOOP_HAMMER_SWITCH_HIT, bundle)),
        (Regions.FIRE_TEMPLE_LOOP_EXIT, lambda bundle: has_item(
            LocalEvents.FIRE_TEMPLE_LOOP_HAMMER_SWITCH_HIT, bundle))
    ])

    # Fire Temple Loop Exit
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_LOOP_EXIT, world, [
        (Regions.FIRE_TEMPLE_FIRST_ROOM, lambda bundle: True),
        (Regions.FIRE_TEMPLE_LOOP_GORON_ROOM, lambda bundle: has_item(
            LocalEvents.FIRE_TEMPLE_LOOP_HAMMER_SWITCH_HIT, bundle))
    ])

    # Fire Temple Big Lava Room
    # Locations
    add_locations(Regions.FIRE_TEMPLE_BIG_LAVA_ROOM, world, [
        (Locations.FIRE_TEMPLE_BIG_LAVA_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FIRE_TEMPLE_BIG_LAVA_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FIRE_TEMPLE_BIG_LAVA_POT3,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BIG_LAVA_ROOM, world, [
        (Regions.FIRE_TEMPLE_FIRST_ROOM, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 2, bundle)),
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_NORTH_GORON, lambda bundle: True),
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_NORTH_TILES, lambda bundle:
            (is_adult(bundle) and
             (can_use(Items.SONG_OF_TIME, bundle) or
              can_do_trick(Tricks.FIRE_SOT, bundle)))),
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_SOUTH_GORON,
         lambda bundle: is_adult(bundle) and has_explosives(bundle)),
        (Regions.FIRE_TEMPLE_FIRE_PILLAR_ROOM, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 3, bundle))
    ])

    # Fire Temple Big Lava Room North Goron
    # Locations
    add_locations(Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_NORTH_GORON, world, [
        (Locations.FIRE_TEMPLE_BIG_LAVA_ROOM_LOWER_OPEN_DOOR_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_NORTH_GORON, world, [
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM, lambda bundle: True)
    ])

    # Fire Temple Big Lava Room North Tiles
    # Locations
    add_locations(Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_NORTH_TILES, world, [
        (Locations.FIRE_TEMPLE_GS_SONG_OF_TIME_ROOM, lambda bundle:
            ((is_adult(bundle) and
              can_attack(bundle)) or
             hookshot_or_boomerang(bundle)))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_NORTH_TILES, world, [
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM, lambda bundle: True)
    ])

    # Fire Temple Big Lava Room South Goron
    # Locations
    add_locations(Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_SOUTH_GORON, world, [
        (Locations.FIRE_TEMPLE_BIG_LAVA_ROOM_BLOCKED_DOOR_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BIG_LAVA_ROOM_SOUTH_GORON, world, [
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM, lambda bundle: True)
    ])

    # Fire Temple Fire Pillar Room
    # Locations
    add_locations(Regions.FIRE_TEMPLE_FIRE_PILLAR_ROOM, world, [
        (Locations.FIRE_TEMPLE_FIRE_PILLAR_ROOM_LEFT_HEART,
         lambda bundle: fire_timer(bundle) >= 56),
        (Locations.FIRE_TEMPLE_FIRE_PILLAR_ROOM_RIGHT_HEART,
         lambda bundle: fire_timer(bundle) >= 56),
        (Locations.FIRE_TEMPLE_FIRE_PILLAR_ROOM_BACK_HEART,
         lambda bundle: fire_timer(bundle) >= 56),
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_FIRE_PILLAR_ROOM, world, [
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 3, bundle)),
        (Regions.FIRE_TEMPLE_SHORTCUT_ROOM, lambda bundle:
            (fire_timer(bundle) >= 56 and
             small_keys(Items.FIRE_TEMPLE_SMALL_KEY, 4, bundle)))
    ])

    # Fire Temple Shortcut Room
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_SHORTCUT_ROOM, world, [
        (Regions.FIRE_TEMPLE_FIRE_PILLAR_ROOM, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 4, bundle)),
        (Regions.FIRE_TEMPLE_SHORTCUT_CLIMB, lambda bundle: has_item(
            LocalEvents.FIRE_TEMPLE_SHORTCUT_SWITCH_HIT, bundle)),
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER, lambda bundle:
            is_adult(bundle) and (
                has_item(Items.GORONS_BRACELET, bundle) or can_do_trick(Tricks.FIRE_STRENGTH, bundle) or can_ground_jump(bundle)) and (
                    (has_explosives(bundle) or can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT, Items.FAIRY_SLINGSHOT], bundle))))
    ])

    # Fire Temple Shortcut Climb
    # Events
    add_events(Regions.FIRE_TEMPLE_SHORTCUT_CLIMB, world, [
        (EventLocations.FIRE_TEMPLE_SHORTCUT_SWITCH,
         LocalEvents.FIRE_TEMPLE_SHORTCUT_SWITCH_HIT, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.FIRE_TEMPLE_SHORTCUT_CLIMB, world, [
        (Locations.FIRE_TEMPLE_BOULDER_MAZE_SHORTCUT_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_SHORTCUT_CLIMB, world, [
        (Regions.FIRE_TEMPLE_SHORTCUT_ROOM, lambda bundle: True),
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_UPPER, lambda bundle: True)
    ])

    # Fire Temple Boulder Maze Lower
    # Locations
    add_locations(Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER, world, [
        (Locations.FIRE_TEMPLE_BOULDER_MAZE_LOWER_CHEST, lambda bundle: True),
        (Locations.FIRE_TEMPLE_GS_BOULDER_MAZE, lambda bundle:
            (has_explosives(bundle) and
             (is_adult(bundle) or
              hookshot_or_boomerang(bundle))))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER, world, [
        (Regions.FIRE_TEMPLE_SHORTCUT_ROOM, lambda bundle: True),
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER_SIDE_ROOM, lambda bundle: True),
        (Regions.FIRE_TEMPLE_EAST_CENTRAL_ROOM, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 5, bundle)),
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_UPPER, lambda bundle: False)
    ])

    # Fire Temple Boulder Maze Lower Side Room
    # Locations
    add_locations(Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER_SIDE_ROOM, world, [
        (Locations.FIRE_TEMPLE_BOULDER_MAZE_SIDE_ROOM_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER_SIDE_ROOM, world, [
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER, lambda bundle: True)
    ])

    # Fire Temple East Central Room
    # Locations
    add_locations(Regions.FIRE_TEMPLE_EAST_CENTRAL_ROOM, world, [
        (Locations.FIRE_TEMPLE_EAST_CENTRAL_ROOM_LEFT_HEART, lambda bundle: True),
        (Locations.FIRE_TEMPLE_EAST_CENTRAL_ROOM_RIGHT_HEART, lambda bundle: True),
        (Locations.FIRE_TEMPLE_EAST_CENTRAL_ROOM_MIDDLE_HEART, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_EAST_CENTRAL_ROOM, world, [
        (Regions.FIRE_TEMPLE_BIG_LAVA_ROOM, lambda bundle: take_damage(bundle)),
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 5, bundle)),
        (Regions.FIRE_TEMPLE_FIRE_WALL_CHASE, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 6, bundle)),
        (Regions.FIRE_TEMPLE_MAP_REGION, lambda bundle:
            (can_use(Items.FAIRY_SLINGSHOT, bundle) or
             can_use(Items.FAIRY_BOW, bundle)))
    ])

    # Fire Temple Fire Wall Chase
    # Locations
    add_locations(Regions.FIRE_TEMPLE_FIRE_WALL_CHASE, world, [
        (Locations.FIRE_TEMPLE_FIRE_WALL_CHASE_EAST_PILLAR_HEART, lambda bundle:
            (fire_timer(bundle) >= 24 and
             (is_adult(bundle) or
              can_use(Items.BOOMERANG, bundle)))),
        (Locations.FIRE_TEMPLE_FIRE_WALL_CHASE_WEST_PILLAR_HEART, lambda bundle:
            (fire_timer(bundle) >= 24 and
             (is_adult(bundle) or
              can_use(Items.BOOMERANG, bundle)))),
        (Locations.FIRE_TEMPLE_FIRE_WALL_CHASE_EXIT_PLATFORM_HEART,
         lambda bundle: fire_timer(bundle) >= 24)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_FIRE_WALL_CHASE, world, [
        (Regions.FIRE_TEMPLE_EAST_CENTRAL_ROOM, lambda bundle:
            (fire_timer(bundle) >= 24 and
             small_keys(Items.FIRE_TEMPLE_SMALL_KEY, 6, bundle))),
        (Regions.FIRE_TEMPLE_MAP_REGION, lambda bundle: is_adult(bundle)),
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_UPPER,
         lambda bundle: fire_timer(bundle) >= 24 and is_adult(bundle)),
        (Regions.FIRE_TEMPLE_CORRIDOR, lambda bundle: fire_timer(bundle) >= 24 and is_adult(
            bundle) and small_keys(Items.FIRE_TEMPLE_SMALL_KEY, 7, bundle))
    ])

    # Fire Temple Map Region
    # Locations
    add_locations(Regions.FIRE_TEMPLE_MAP_REGION, world, [
        (Locations.FIRE_TEMPLE_MAP_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_MAP_REGION, world, [
        (Regions.FIRE_TEMPLE_EAST_CENTRAL_ROOM, lambda bundle: True)
    ])

    # Fire Temple Boulder Maze Upper
    # Locations
    add_locations(Regions.FIRE_TEMPLE_BOULDER_MAZE_UPPER, world, [
        (Locations.FIRE_TEMPLE_BOULDER_MAZE_UPPER_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BOULDER_MAZE_UPPER, world, [
        (Regions.FIRE_TEMPLE_SHORTCUT_CLIMB, lambda bundle: has_explosives(bundle)),
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_LOWER, lambda bundle: True),
        (Regions.FIRE_TEMPLE_FIRE_WALL_CHASE, lambda bundle: True),
        (Regions.FIRE_TEMPLE_SCARECROW_ROOM, lambda bundle:
            (can_use(Items.SCARECROW, bundle) or
             (can_do_trick(Tricks.FIRE_SCARECROW, bundle) and
              is_adult(bundle) and
              can_use(Items.LONGSHOT, bundle))))
    ])

    # Fire Temple Scarecrow Room
    # Locations
    add_locations(Regions.FIRE_TEMPLE_SCARECROW_ROOM, world, [
        (Locations.FIRE_TEMPLE_GS_SCARECROW_CLIMB, lambda bundle:
            can_jump_slash_except_hammer(bundle) or
            can_use_any([Items.FAIRY_SLINGSHOT, Items.BOOMERANG, Items.FAIRY_BOW, Items.HOOKSHOT, Items.DINS_FIRE], bundle) or
            has_explosives(bundle))
    ])

    # Connections
    connect_regions(Regions.FIRE_TEMPLE_SCARECROW_ROOM, world, [
        (Regions.FIRE_TEMPLE_BOULDER_MAZE_UPPER, lambda bundle: True),
        (Regions.FIRE_TEMPLE_EAST_PEAK, lambda bundle: True)
    ])

    # Fire Temple East Peak
    # Locations
    add_locations(Regions.FIRE_TEMPLE_EAST_PEAK, world, [
        (Locations.FIRE_TEMPLE_SCARECROW_CHEST, lambda bundle: True),
        (Locations.FIRE_TEMPLE_GS_SCARECROW_TOP,
         lambda bundle: can_use_projectile(bundle))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_EAST_PEAK, world, [
        (Regions.FIRE_TEMPLE_SCARECROW_ROOM, lambda bundle: True),
        (Regions.FIRE_TEMPLE_EAST_CENTRAL_ROOM, lambda bundle: take_damage(bundle))
    ])

    # Fire Temple Corridor
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_CORRIDOR, world, [
        (Regions.FIRE_TEMPLE_FIRE_WALL_CHASE, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 7, bundle)),
        (Regions.FIRE_TEMPLE_FIRE_MAZE_ROOM, lambda bundle: True)
    ])

    # Fire Temple Fire Maze Room
    # Locations
    add_locations(Regions.FIRE_TEMPLE_FIRE_MAZE_ROOM, world, [
        (Locations.FIRE_TEMPLE_FLAME_MAZE_LEFT_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FIRE_TEMPLE_FLAME_MAZE_LEFT_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FIRE_TEMPLE_FLAME_MAZE_LEFT_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FIRE_TEMPLE_FLAME_MAZE_LEFT_POT4,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_FIRE_MAZE_ROOM, world, [
        (Regions.FIRE_TEMPLE_CORRIDOR, lambda bundle: True),
        (Regions.FIRE_TEMPLE_FIRE_MAZE_UPPER, lambda bundle: can_use(
            Items.HOVER_BOOTS, bundle) or can_ground_jump(bundle)),
        (Regions.FIRE_TEMPLE_FIRE_MAZE_SIDE_ROOM, lambda bundle: True),
        (Regions.FIRE_TEMPLE_WEST_CENTRAL_LOWER, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 8, bundle)),
        (Regions.FIRE_TEMPLE_LATE_FIRE_MAZE,
         lambda bundle: can_do_trick(Tricks.FIRE_FLAME_MAZE, bundle))
    ])

    # Fire Temple Fire Maze Upper
    # Events
    add_events(Regions.FIRE_TEMPLE_FIRE_MAZE_UPPER, world, [
        (EventLocations.FIRE_TEMPLE_FIRE_MAZE_UPPER_PLATFORM, LocalEvents.FIRE_TEMPLE_FIRE_MAZE_UPPER_PLATFORM_HIT, lambda bundle:
            (can_use(Items.MEGATON_HAMMER, bundle)))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_FIRE_MAZE_UPPER, world, [
        (Regions.FIRE_TEMPLE_NEAR_BOSS_ROOM,
         lambda bundle: can_use(Items.MEGATON_HAMMER, bundle)),
        (Regions.FIRE_TEMPLE_FIRE_MAZE_ROOM, lambda bundle: True),
        (Regions.FIRE_TEMPLE_WEST_CENTRAL_UPPER,
         lambda bundle: can_use(Items.MEGATON_HAMMER, bundle))
    ])

    # Fire Temple Fire Maze Side Room
    # Locations
    add_locations(Regions.FIRE_TEMPLE_FIRE_MAZE_SIDE_ROOM, world, [
        (Locations.FIRE_TEMPLE_COMPASS_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_FIRE_MAZE_SIDE_ROOM, world, [
        (Regions.FIRE_TEMPLE_FIRE_MAZE_ROOM, lambda bundle: True)
    ])

    # Fire Temple West Central Lower
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_WEST_CENTRAL_LOWER, world, [
        (Regions.FIRE_TEMPLE_FIRE_MAZE_ROOM, lambda bundle: small_keys(
            Items.FIRE_TEMPLE_SMALL_KEY, 8, bundle)),
        (Regions.FIRE_TEMPLE_WEST_CENTRAL_UPPER, lambda bundle:
            (is_adult(bundle) and
             can_use(Items.SONG_OF_TIME, bundle))),
        (Regions.FIRE_TEMPLE_LATE_FIRE_MAZE, lambda bundle: True)
    ])

    # Fire Temple West Central Upper
    # Locations
    add_locations(Regions.FIRE_TEMPLE_WEST_CENTRAL_UPPER, world, [
        (Locations.FIRE_TEMPLE_HIGHEST_GORON_CHEST, lambda bundle:
            ((can_use(Items.SONG_OF_TIME, bundle) or
              can_do_trick(Tricks.RUSTED_SWITCHES, bundle)) and
             can_use(Items.MEGATON_HAMMER, bundle)))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_WEST_CENTRAL_UPPER, world, [
        (Regions.FIRE_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False),
        (Regions.FIRE_TEMPLE_FIRE_MAZE_UPPER, lambda bundle: True),
        (Regions.FIRE_TEMPLE_WEST_CENTRAL_LOWER, lambda bundle: True)
    ])

    # Fire Temple Late Fire Maze
    # Locations
    add_locations(Regions.FIRE_TEMPLE_LATE_FIRE_MAZE, world, [
        (Locations.FIRE_TEMPLE_FLAME_MAZE_RIGHT_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FIRE_TEMPLE_FLAME_MAZE_RIGHT_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FIRE_TEMPLE_FLAME_MAZE_RIGHT_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FIRE_TEMPLE_FLAME_MAZE_RIGHT_POT4,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_LATE_FIRE_MAZE, world, [
        (Regions.FIRE_TEMPLE_FIRE_MAZE_ROOM, lambda bundle: False),
        (Regions.FIRE_TEMPLE_WEST_CENTRAL_LOWER, lambda bundle: True),
        (Regions.FIRE_TEMPLE_UPPER_FLARE_DANCER,
         lambda bundle: has_explosives(bundle))
    ])

    # Fire Temple Upper Flare Dancer
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_UPPER_FLARE_DANCER, world, [
        (Regions.FIRE_TEMPLE_LATE_FIRE_MAZE,
         lambda bundle: can_kill_enemy(bundle, Enemies.FLARE_DANCER)),
        (Regions.FIRE_TEMPLE_WEST_CLIMB,
         lambda bundle: can_kill_enemy(bundle, Enemies.FLARE_DANCER))
    ])

    # Fire Temple West Climb
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_WEST_CLIMB, world, [
        (Regions.FIRE_TEMPLE_UPPER_FLARE_DANCER, lambda bundle: True),
        (Regions.FIRE_TEMPLE_WEST_PEAK, lambda bundle: can_use_projectile(bundle))
    ])

    # Fire Temple West Peak
    # Locations
    add_locations(Regions.FIRE_TEMPLE_WEST_PEAK, world, [
        (Locations.FIRE_TEMPLE_MEGATON_HAMMER_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_WEST_PEAK, world, [
        (Regions.FIRE_TEMPLE_WEST_CENTRAL_UPPER,
         lambda bundle: take_damage(bundle)),
        (Regions.FIRE_TEMPLE_WEST_CLIMB, lambda bundle: True),
        (Regions.FIRE_TEMPLE_HAMMER_RETURN_PATH,
         lambda bundle: can_use(Items.MEGATON_HAMMER, bundle))
    ])

    # Fire Temple Hammer Return Path
    # Locations
    add_locations(Regions.FIRE_TEMPLE_HAMMER_RETURN_PATH, world, [
        (Locations.FIRE_TEMPLE_AFTER_HAMMER_SMALL_CRATE1,
         lambda bundle: can_break_small_crates(bundle)),
        (Locations.FIRE_TEMPLE_AFTER_HAMMER_SMALL_CRATE2,
         lambda bundle: can_break_small_crates(bundle)),
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_HAMMER_RETURN_PATH, world, [
        (Regions.FIRE_TEMPLE_ABOVE_FIRE_MAZE,
         lambda bundle: can_use(Items.MEGATON_HAMMER, bundle))
    ])

    # Fire Temple Above Fire Maze
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_ABOVE_FIRE_MAZE, world, [
        (Regions.FIRE_TEMPLE_HAMMER_RETURN_PATH, lambda bundle: True),
        (Regions.FIRE_TEMPLE_FIRE_MAZE_UPPER,
         lambda bundle: can_use(Items.MEGATON_HAMMER, bundle))
    ])

    # Fire Temple Boss Entryway
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BOSS_ENTRYWAY, world, [
        (Regions.FIRE_TEMPLE_NEAR_BOSS_ROOM, lambda bundle: False),
        (Regions.FIRE_TEMPLE_BOSS_ROOM, lambda bundle: has_item(
            Items.FIRE_TEMPLE_BOSS_KEY, bundle))
    ])

    # Fire Temple Boss Room
    # Events
    add_events(Regions.FIRE_TEMPLE_BOSS_ROOM, world, [
        (EventLocations.FIRE_TEMPLE_VOLVAGIA, Events.FIRE_TEMPLE_COMPLETED, lambda bundle:
            fire_timer(bundle) >= 64 and can_kill_enemy(bundle, Enemies.VOLVAGIA))
    ])
    # Locations
    add_locations(Regions.FIRE_TEMPLE_BOSS_ROOM, world, [
        (Locations.FIRE_TEMPLE_VOLVAGIA_HEART_CONTAINER,
         lambda bundle: has_item(Events.FIRE_TEMPLE_COMPLETED, bundle)),
        (Locations.VOLVAGIA, lambda bundle: has_item(
            Events.FIRE_TEMPLE_COMPLETED, bundle))
    ])
    # Connections
    connect_regions(Regions.FIRE_TEMPLE_BOSS_ROOM, world, [
        (Regions.FIRE_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False),
        (Regions.DMC_CENTRAL_LOCAL, lambda bundle: has_item(
            Events.FIRE_TEMPLE_COMPLETED, bundle))
    ])
