from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    JABU_JABUS_BELLY_WEST_TENTACLE = "Jabu Jabus Belly West Tentacle"
    JABU_JABUS_BELLY_EAST_TENTACLE = "Jabu Jabus Belly East Tentacle"
    JABU_JABUS_BELLY_NORTH_TENTACLE = "Jabu Jabus Belly North Tentacle"
    JABU_JABUS_BELLY_RUTO_IN_1F = "Jabu Jabus Belly Ruto In 1F"
    JABU_JABUS_BELLY_LOWERED_PATH = "Jabu Jabus Belly Lowered Path"
    JABU_JABUS_BELLY_B1_NORTH_FAIRY_POT = "Jabu Jabus Belly B1 North Fairy Pot"
    JABU_JABUS_BELLY_WATER_SWITCH_ROOM_FAIRY_POT = "Jabu Jabus Belly Water Switch Room Fairy Pot"
    JABU_JABUS_BELLY_ABOVE_BIGOCTO_FAIRY_POT = "Jabu Jabus Belly Above Bigocto Fairy Pot"
    JABU_JABUS_BELLY_ABOVE_BIGOCTO_NUT_POT = "Jabu Jabus Belly Above Bigocto Nut Pot"
    JABU_JABUS_BELLY_BARINADE = "Jabu Jabus Belly Barinade"


class LocalEvents(StrEnum):
    JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED = "Jabu Jabus Belly West Tentacle Defeated"
    JABU_JABUS_BELLY_EAST_TENTACLE_DEFEATED = "Jabu Jabus Belly East Tentacle Defeated"
    JABU_JABUS_BELLY_NORTH_TENTACLE_DEFEATED = "Jabu Jabus Belly North Tentacle Defeated"
    JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED = "Jabu Jabus Belly Ruto In 1F Rescued"
    JABU_JABUS_BELLY_LOWERED_PATH_ACTIVATED = "Jabu Jabu Belly Lowered Path Activated"


def set_region_rules(world: "SohWorld") -> None:
    # Jabu Jabu's Belly Entryway
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_ENTRYWAY, world, [
        # TODO: Add vanilla/MQ check
        (Regions.JABU_JABUS_BELLY_BEGINNING, lambda bundle: True),
        (Regions.ZORAS_FOUNTAIN, lambda bundle: True)
    ])

    # Jabu Jabu's Belly Beginning
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BEGINNING, world, [
        (Regions.JABU_JABUS_BELLY_ENTRYWAY, lambda bundle: True),
        (Regions.JABU_JABUS_BELLY_MAIN, lambda bundle: can_use_projectile(bundle))
    ])

    # Jabu Jabu's Belly Main
    # Events
    add_events(Regions.JABU_JABUS_BELLY_MAIN, world, [
        (EventLocations.JABU_JABUS_BELLY_WEST_TENTACLE, LocalEvents.JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED, bundle) and can_kill_enemy(bundle, Enemies.TENTACLE, EnemyDistance.BOOMERANG))
    ])
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_MAIN, world, [
        (Locations.JABU_JABUS_BELLY_DEKU_SCRUB, lambda bundle: has_item(Items.BRONZE_SCALE, bundle) and (is_child(bundle) or has_item(
            Items.SILVER_SCALE, bundle) or can_do_trick(Tricks.JABU_ALCOVE_JUMP_DIVE, bundle) or can_use(Items.IRON_BOOTS, bundle)) and can_stun_deku(bundle)),
        (Locations.JABU_JABUS_BELLY_BOOMERANG_CHEST, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED, bundle)),
        (Locations.JABU_JABUS_BELLY_MAP_CHEST, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED, bundle)),
        (Locations.JABU_JABUS_BELLY_PLATFORM_ROOM_SMALL_CRATE1,
         lambda bundle: can_break_small_crates(bundle)),
        (Locations.JABU_JABUS_BELLY_PLATFORM_ROOM_SMALL_CRATE2,
         lambda bundle: can_break_small_crates(bundle))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_MAIN, world, [
        (Regions.JABU_JABUS_BELLY_BEGINNING, lambda bundle: True),
        (Regions.JABU_JABUS_BELLY_B1_NORTH, lambda bundle: True),
        (Regions.JABU_JABUS_BELLY_COMPASS_ROOM, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED, bundle)),
        (Regions.JABU_JABUS_BELLY_BLUE_TENTACLE, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED, bundle)),
        (Regions.JABU_JABUS_BELLY_GREEN_TENTACLE, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_EAST_TENTACLE_DEFEATED, bundle)),
        (Regions.JABU_JABUS_BELLY_BIGOCTO_LEDGE, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_NORTH_TENTACLE_DEFEATED, bundle)),
        (Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, lambda bundle: has_item(LocalEvents.JABU_JABUS_BELLY_LOWERED_PATH_ACTIVATED,
         bundle) or (can_do_trick(Tricks.JABU_BOSS_HOVER, bundle) and can_use(Items.HOVER_BOOTS, bundle)))
    ])

    # Jabu Jabu's Belly B1 North
    # Events
    add_events(Regions.JABU_JABUS_BELLY_B1_NORTH, world, [
        (EventLocations.JABU_JABUS_BELLY_RUTO_IN_1F, LocalEvents.JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED,
         lambda bundle: is_adult(bundle) or has_item(Items.BRONZE_SCALE, bundle)),
        (EventLocations.JABU_JABUS_BELLY_B1_NORTH_FAIRY_POT, Events.CAN_ACCESS_FAIRIES, lambda bundle: can_use(
            Items.BOOMERANG, bundle) or (can_use(Items.HOVER_BOOTS, bundle) and can_kill_enemy(bundle, Enemies.OCTOROK)))
    ])
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_B1_NORTH, world, [
        (Locations.JABU_JABUS_BELLY_GS_LOBBY_BASEMENT_LOWER,
         lambda bundle: hookshot_or_boomerang(bundle)),
        (Locations.JABU_JABUS_BELLY_GS_WATER_SWITCH_ROOM,
         lambda bundle: hookshot_or_boomerang(bundle)),
        (Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT1, lambda bundle: can_break_pots(bundle) and (can_use(Items.BOOMERANG, bundle) or (
            can_use(Items.HOVER_BOOTS, bundle) and can_kill_enemy(bundle, Enemies.OCTOROK, EnemyDistance.BOOMERANG, False)))),
        (Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT2, lambda bundle: can_break_pots(bundle) and (can_use(Items.BOOMERANG, bundle) or (
            can_use(Items.HOVER_BOOTS, bundle) and can_kill_enemy(bundle, Enemies.OCTOROK, EnemyDistance.BOOMERANG, False)))),
        (Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT3, lambda bundle: can_break_pots(bundle) and (can_use(Items.BOOMERANG, bundle) or (
            can_use(Items.HOVER_BOOTS, bundle) and can_kill_enemy(bundle, Enemies.OCTOROK, EnemyDistance.BOOMERANG, False)))),
        (Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT4, lambda bundle: can_break_pots(bundle) and (can_use(Items.BOOMERANG, bundle) or (
            can_use(Items.HOVER_BOOTS, bundle) and can_kill_enemy(bundle, Enemies.OCTOROK, EnemyDistance.BOOMERANG, False)))),
        (Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT5, lambda bundle: can_break_pots(bundle) and (can_use(Items.BOOMERANG, bundle) or (
            can_use(Items.HOVER_BOOTS, bundle) and can_kill_enemy(bundle, Enemies.OCTOROK, EnemyDistance.BOOMERANG, False))))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_B1_NORTH, world, [
        (Regions.JABU_JABUS_BELLY_MAIN, lambda bundle: True),
        (Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, lambda bundle: has_item(
            Items.BRONZE_SCALE, bundle) or can_use(Items.HOVER_BOOTS, bundle)),
        (Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_SOUTH, lambda bundle: is_adult(
            bundle) or has_item(Items.BRONZE_SCALE, bundle)),
        (Regions.JABU_JABUS_BELLY_LOBBY_BASEMENT_UPPER_GS,
         lambda bundle: hookshot_or_boomerang(bundle)),
    ])

    # Jabu Jabu's Belly Water Switch Room Ledge
    # Events
    add_events(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, world, [
        (EventLocations.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_FAIRY_POT,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, world, [
        (Locations.JABU_JABUS_BELLY_GS_WATER_SWITCH_ROOM, lambda bundle: has_item(Items.BRONZE_SCALE, bundle) or (is_adult(
            bundle) and can_use(Items.HOVER_BOOTS, bundle)) or can_kill_enemy(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOMB_THROW)),
        (Locations.JABU_JABUS_BELLY_BASEMENT_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_BASEMENT_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_BASEMENT_POT3,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, world, [
        (Regions.JABU_JABUS_BELLY_B1_NORTH, lambda bundle: True),
        (Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_SOUTH, lambda bundle: True)
    ])

    # Jabu Jabu's Belly Water Switch Room South
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_SOUTH, world, [
        (Locations.JABU_JABUS_BELLY_GS_WATER_SWITCH_ROOM,
         lambda bundle: hookshot_or_boomerang(bundle))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_SOUTH, world, [
        (Regions.JABU_JABUS_BELLY_B1_NORTH, lambda bundle: is_adult(
            bundle) or has_item(Items.BRONZE_SCALE, bundle)),
        (Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, lambda bundle: has_item(
            Items.BRONZE_SCALE, bundle) or can_use(Items.HOVER_BOOTS, bundle)),
        (Regions.JABU_JABUS_BELLY_MAIN, lambda bundle: can_use_projectile(bundle))
    ])

    # Jabu Jabu's Belly Compass Room
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_COMPASS_ROOM, world, [
        (Locations.JABU_JABUS_BELLY_COMPASS_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.SHABOM))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_COMPASS_ROOM, world, [
        (Regions.JABU_JABUS_BELLY_MAIN,
         lambda bundle: can_kill_enemy(bundle, Enemies.SHABOM))
    ])

    # Jabu Jabu's Belly Blue Tentacle
    # Events
    add_events(Regions.JABU_JABUS_BELLY_BLUE_TENTACLE, world, [
        (EventLocations.JABU_JABUS_BELLY_EAST_TENTACLE, LocalEvents.JABU_JABUS_BELLY_EAST_TENTACLE_DEFEATED,
         lambda bundle: can_kill_enemy(bundle, Enemies.TENTACLE, EnemyDistance.BOOMERANG))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BLUE_TENTACLE, world, [
        (Regions.JABU_JABUS_BELLY_MAIN, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_EAST_TENTACLE_DEFEATED, bundle))
    ])

    # Jabu Jabu's Belly Green Tentacle
    # Events
    add_events(Regions.JABU_JABUS_BELLY_GREEN_TENTACLE, world, [
        (EventLocations.JABU_JABUS_BELLY_NORTH_TENTACLE, LocalEvents.JABU_JABUS_BELLY_NORTH_TENTACLE_DEFEATED,
         lambda bundle: can_kill_enemy(bundle, Enemies.TENTACLE, EnemyDistance.BOOMERANG))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_GREEN_TENTACLE, world, [
        (Regions.JABU_JABUS_BELLY_MAIN, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_NORTH_TENTACLE_DEFEATED, bundle))
    ])

    # Jabu Jabu's Belly Bigocto Room
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BIGOCTO_LEDGE, world, [
        (Regions.JABU_JABUS_BELLY_B1_NORTH, lambda bundle: True),
        (Regions.JABU_JABUS_BELLY_ABOVE_BIGOCTO, lambda bundle: has_item(
            LocalEvents.JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED, bundle) and can_kill_enemy(bundle, Enemies.BIG_OCTO)),
        (Regions.JABU_JABUS_BELLY_LOBBY_BASEMENT_UPPER_GS, lambda bundle: is_adult(bundle)
         and can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH))
    ])

    # Jabu Jabu's Belly GS Lobby Basement Upper
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_LOBBY_BASEMENT_UPPER_GS, world, [
        (Locations.JABU_JABUS_BELLY_GS_LOBBY_BASEMENT_UPPER, lambda bundle: True)
    ])

    # Jabu Jabu's Belly Above Bigocto
    add_events(Regions.JABU_JABUS_BELLY_ABOVE_BIGOCTO, world, [
        (EventLocations.JABU_JABUS_BELLY_ABOVE_BIGOCTO_FAIRY_POT,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True),
        (EventLocations.JABU_JABUS_BELLY_ABOVE_BIGOCTO_NUT_POT,
         Events.CAN_FARM_NUTS, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_ABOVE_BIGOCTO, world, [
        (Locations.JABU_JABUS_BELLY_ABOVE_BIG_OCTO_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_ABOVE_BIG_OCTO_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_ABOVE_BIG_OCTO_POT3,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_ABOVE_BIGOCTO, world, [
        (Regions.JABU_JABUS_BELLY_LIFT_UPPER,
         lambda bundle: can_use(Items.BOOMERANG, bundle))
    ])

    # Jabu Jabu's Belly Lift Upper
    # Events
    add_events(Regions.JABU_JABUS_BELLY_LIFT_UPPER, world, [
        (EventLocations.JABU_JABUS_BELLY_LOWERED_PATH,
         LocalEvents.JABU_JABUS_BELLY_LOWERED_PATH_ACTIVATED, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_LIFT_UPPER, world, [
        (Regions.JABU_JABUS_BELLY_MAIN, lambda bundle: True)
    ])

    # Jabu Jabu's Belly Near Boss Room
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, world, [
        (Locations.JABU_JABUS_BELLY_GS_NEAR_BOSS, lambda bundle: can_kill_enemy(
            bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.BOMB_THROW))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, world, [
        (Regions.JABU_JABUS_BELLY_MAIN, lambda bundle: True),
        (Regions.JABU_JABUS_BELLY_BOSS_ENTRYWAY, lambda bundle: can_use(Items.BOOMERANG, bundle) or (can_do_trick(Tricks.JABU_NEAR_BOSS_RANGED, bundle) and can_use_any([Items.HOOKSHOT, Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)) or (
            can_do_trick(Tricks.JABU_NEAR_BOSS_EXPLOSIVES, bundle) and (can_use(Items.BOMBCHUS_5, bundle) or (can_use(Items.HOVER_BOOTS, bundle) and can_use(Items.BOMB_BAG, bundle)))))
    ])

    # Skipping master quest for now

    # Jabu Jabu's Belly Boss Entryway
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BOSS_ENTRYWAY, world, [
        (Regions.JABU_JABUS_BELLY_BOSS_ROOM, lambda bundle: True)
    ])

    # # Jabu Jabu's Belly Boss Exit
    # # Connections
    # connect_regions(Regions.JABU_JABUS_BELLY_BOSS_EXIT, world, [
    #     (Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, lambda bundle: True)
    #     # skipping mq connection
    # ])

    # Jabu Jabu's Belly Boss Room
    # Events
    add_events(Regions.JABU_JABUS_BELLY_BOSS_ROOM, world, [
        (EventLocations.JABU_JABUS_BELLY_BARINADE, Events.JABU_JABUS_BELLY_COMPLETED,
         lambda bundle: can_kill_enemy(bundle, Enemies.BARINADE))
    ])
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_BOSS_ROOM, world, [
        (Locations.JABU_JABUS_BELLY_BARINADE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_BARINADE_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_BARINADE_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_BARINADE_POT4,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_BARINADE_POT5,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_BARINADE_POT6,
         lambda bundle: can_break_pots(bundle)),
        (Locations.JABU_JABUS_BELLY_BARINADE_HEART_CONTAINER,
         lambda bundle: has_item(Events.JABU_JABUS_BELLY_COMPLETED, bundle)),
        (Locations.BARINADE, lambda bundle: has_item(
            Events.JABU_JABUS_BELLY_COMPLETED, bundle))
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BOSS_ROOM, world, [
        # (Regions.JABU_JABUS_BELLY_BOSS_EXIT, lambda bundle: False),  # readd for MQ stuff
        (Regions.ZORAS_FOUNTAIN, lambda bundle: has_item(
            Events.JABU_JABUS_BELLY_COMPLETED, bundle))
    ])
