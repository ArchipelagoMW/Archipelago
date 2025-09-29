from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    JABU_JABUS_BELLY_WEST_TENTACLE = "Jabu Jabus Belly West Tentacle",
    JABU_JABUS_BELLY_EAST_TENTACLE = "Jabu Jabus Belly East Tentacle", 
    JABU_JABUS_BELLY_NORTH_TENTACLE = "Jabu Jabus Belly North Tentacle",
    JABU_JABUS_BELLY_RUTO_IN_1F = "Jabu Jabus Belly Ruto In 1F",
    JABU_JABUS_BELLY_LOWERED_PATH = "Jabu Jabus Belly Lowered Path",
    JABU_JABUS_BELLY_BOSS = "Jabu Jabu Boss Barinade"


class LocalEvents(str, Enum):
    JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED = "Jabu Jabus Belly West Tentacle Defeated",
    JABU_JABUS_BELLY_EAST_TENTACLE_DEFEATED = "Jabu Jabus Belly East Tentacle Defeated",
    JABU_JABUS_BELLY_NORTH_TENTACLE_DEFEATED = "Jabu Jabus Belly North Tentacle Defeated",
    JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED = "Jabu Jabus Belly Ruto In 1F Rescued",
    JABU_JABUS_BELLY_LOWERED_PATH_ACTIVATED = "Jabu Jabu Belly Lowered Path Activated"


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    ## Jabu Jabu's Belly Entryway
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_ENTRYWAY, world, [
        [Regions.JABU_JABUS_BELLY_BEGINNING, lambda state: True], # TODO: Add vanilla/MQ check
        [Regions.ZORAS_FOUNTAIN, lambda state: True]
    ])

    ## Jabu Jabu's Belly Beginning
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BEGINNING, world, [
        [Regions.JABU_JABUS_BELLY_ENTRYWAY, lambda state: True],
        [Regions.JABU_JABUS_BELLY_MAIN, lambda state: can_use_projectile(state, world)]
    ])

    ## Jabu Jabu's Belly Main
    # Events
    add_events(Regions.JABU_JABUS_BELLY_MAIN, world, [
        [EventLocations.JABU_JABUS_BELLY_WEST_TENTACLE, LocalEvents.JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED, state, world) and can_kill_enemy(state, world, Enemies.TENTACLE, EnemyDistance.BOOMERANG)]
    ])
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_MAIN, world, [
        [Locations.JABU_JABUS_BELLY_DEKU_SCRUB, lambda state: has_item(Items.BRONZE_SCALE, state, world) and (is_child(state, world) or has_item(Items.SILVER_SCALE, state, world) or can_do_trick("Jabu Alcove Jump Dive", state, world) or can_use(Items.IRON_BOOTS, state, world)) and can_stun_deku(state, world)],
        [Locations.JABU_JABUS_BELLY_BOOMERANG_CHEST, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED, state, world)],
        [Locations.JABU_JABUS_BELLY_MAP_CHEST, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED, state, world)],
        [Locations.JABU_JABUS_BELLY_PLATFORM_ROOM_SMALL_CRATE_1, lambda state: can_break_crates(state, world)],
        [Locations.JABU_JABUS_BELLY_PLATFORM_ROOM_SMALL_CRATE_2, lambda state: can_break_crates(state, world)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_MAIN, world, [
        [Regions.JABU_JABUS_BELLY_BEGINNING, lambda state: True],
        [Regions.JABU_JABUS_BELLY_B1_NORTH, lambda state: True],
        [Regions.JABU_JABUS_BELLY_COMPASS_ROOM, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED, state, world)],
        [Regions.JABU_JABUS_BELLY_BLUE_TENTACLE, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_WEST_TENTACLE_DEFEATED, state, world)],
        [Regions.JABU_JABUS_BELLY_GREEN_TENTACLE, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_EAST_TENTACLE_DEFEATED, state, world)],
        [Regions.JABU_JABUS_BELLY_BIGOCTO_LEDGE, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_NORTH_TENTACLE_DEFEATED, state, world)],
        [Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_LOWERED_PATH_ACTIVATED, state, world) or (can_do_trick("Jabu Boss Hover", state, world) and can_use(Items.HOVER_BOOTS, state, world))]
    ])

    ## Jabu Jabu's Belly B1 North
    # Events
    add_events(Regions.JABU_JABUS_BELLY_B1_NORTH, world, [
        [EventLocations.JABU_JABUS_BELLY_RUTO_IN_1F, LocalEvents.JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED, lambda state: is_adult(state, world) or has_item(Items.BRONZE_SCALE, state, world)],
        # TODO: Add FairyPot event: can_use(Items.BOOMERANG, state, world) or (can_use(Items.HOVER_BOOTS, state, world) and can_kill_enemy(state, world, Enemies.OCTOROK))
    ])
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_B1_NORTH, world, [
        [Locations.JABU_JABUS_BELLY_GS_LOBBY_BASEMENT_LOWER, lambda state: hookshot_or_boomerang(state, world)],
        [Locations.JABU_JABUS_BELLY_GS_LOBBY_BASEMENT_UPPER, lambda state: hookshot_or_boomerang(state, world)],
        [Locations.JABU_JABUS_BELLY_GS_WATER_SWITCH_ROOM, lambda state: hookshot_or_boomerang(state, world)],
        [Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT_1, lambda state: can_break_pots(state, world) and (can_use(Items.BOOMERANG, state, world) or (can_use(Items.HOVER_BOOTS, state, world) and can_kill_enemy(state, world, Enemies.OCTOROK, EnemyDistance.BOOMERANG)))],
        [Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT_2, lambda state: can_break_pots(state, world) and (can_use(Items.BOOMERANG, state, world) or (can_use(Items.HOVER_BOOTS, state, world) and can_kill_enemy(state, world, Enemies.OCTOROK, EnemyDistance.BOOMERANG)))],
        [Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT_3, lambda state: can_break_pots(state, world) and (can_use(Items.BOOMERANG, state, world) or (can_use(Items.HOVER_BOOTS, state, world) and can_kill_enemy(state, world, Enemies.OCTOROK, EnemyDistance.BOOMERANG)))],
        [Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT_4, lambda state: can_break_pots(state, world) and (can_use(Items.BOOMERANG, state, world) or (can_use(Items.HOVER_BOOTS, state, world) and can_kill_enemy(state, world, Enemies.OCTOROK, EnemyDistance.BOOMERANG)))],
        [Locations.JABU_JABUS_BELLY_TWO_OCTOROK_POT_5, lambda state: can_break_pots(state, world) and (can_use(Items.BOOMERANG, state, world) or (can_use(Items.HOVER_BOOTS, state, world) and can_kill_enemy(state, world, Enemies.OCTOROK, EnemyDistance.BOOMERANG)))]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_B1_NORTH, world, [
        [Regions.JABU_JABUS_BELLY_MAIN, lambda state: True],
        [Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, lambda state: has_item(Items.BRONZE_SCALE, state, world) or can_use(Items.HOVER_BOOTS, state, world)],
        [Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_SOUTH, lambda state: is_adult(state, world) or has_item(Items.BRONZE_SCALE, state, world)]
    ])

    ## Jabu Jabu's Belly Water Switch Room Ledge
    # Events (TODO: Add FairyPot event)
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, world, [
        [Locations.JABU_JABUS_BELLY_GS_WATER_SWITCH_ROOM, lambda state: has_item(Items.BRONZE_SCALE, state, world) or (is_adult(state, world) and can_use(Items.HOVER_BOOTS, state, world)) or can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOMB_THROW)],
        [Locations.JABU_JABUS_BELLY_BASEMENT_POT_1, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_BASEMENT_POT_2, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_BASEMENT_POT_3, lambda state: can_break_pots(state, world)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, world, [
        [Regions.JABU_JABUS_BELLY_B1_NORTH, lambda state: True],
        [Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_SOUTH, lambda state: True]
    ])

    ## Jabu Jabu's Belly Water Switch Room South
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_SOUTH, world, [
        [Locations.JABU_JABUS_BELLY_GS_WATER_SWITCH_ROOM, lambda state: hookshot_or_boomerang(state, world)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_SOUTH, world, [
        [Regions.JABU_JABUS_BELLY_B1_NORTH, lambda state: is_adult(state, world) or has_item(Items.BRONZE_SCALE, state, world)],
        [Regions.JABU_JABUS_BELLY_WATER_SWITCH_ROOM_LEDGE, lambda state: has_item(Items.BRONZE_SCALE, state, world) or can_use(Items.HOVER_BOOTS, state, world)],
        [Regions.JABU_JABUS_BELLY_MAIN, lambda state: can_use_projectile(state, world)]
    ])

    ## Jabu Jabu's Belly Compass Room
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_COMPASS_ROOM, world, [
        [Locations.JABU_JABUS_BELLY_COMPASS_CHEST, lambda state: can_kill_enemy(state, world, Enemies.SHABOM)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_COMPASS_ROOM, world, [
        [Regions.JABU_JABUS_BELLY_MAIN, lambda state: can_kill_enemy(state, world, Enemies.SHABOM)]
    ])

    ## Jabu Jabu's Belly Blue Tentacle
    # Events
    add_events(Regions.JABU_JABUS_BELLY_BLUE_TENTACLE, world, [
        [EventLocations.JABU_JABUS_BELLY_EAST_TENTACLE, LocalEvents.JABU_JABUS_BELLY_EAST_TENTACLE_DEFEATED, lambda state: can_kill_enemy(state, world, Enemies.TENTACLE, EnemyDistance.BOOMERANG)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BLUE_TENTACLE, world, [
        [Regions.JABU_JABUS_BELLY_MAIN, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_EAST_TENTACLE_DEFEATED, state, world)]
    ])

    ## Jabu Jabu's Belly Green Tentacle
    # Events
    add_events(Regions.JABU_JABUS_BELLY_GREEN_TENTACLE, world, [
        [EventLocations.JABU_JABUS_BELLY_NORTH_TENTACLE, LocalEvents.JABU_JABUS_BELLY_NORTH_TENTACLE_DEFEATED, lambda state: can_kill_enemy(state, world, Enemies.TENTACLE, EnemyDistance.BOOMERANG)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_GREEN_TENTACLE, world, [
        [Regions.JABU_JABUS_BELLY_MAIN, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_NORTH_TENTACLE_DEFEATED, state, world)]
    ])

    ## Jabu Jabu's Belly Bigocto Ledge
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_BIGOCTO_LEDGE, world, [
        [Locations.JABU_JABUS_BELLY_GS_LOBBY_BASEMENT_UPPER, lambda state: is_adult(state, world) and can_get_enemy_drop(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BIGOCTO_LEDGE, world, [
        [Regions.JABU_JABUS_BELLY_B1_NORTH, lambda state: True],
        [Regions.JABU_JABUS_BELLY_ABOVE_BIGOCTO, lambda state: has_item(LocalEvents.JABU_JABUS_BELLY_RUTO_IN_1F_RESCUED, state, world) and can_kill_enemy(state, world, Enemies.BIG_OCTO)]
    ])

    ## Jabu Jabu's Belly Above Bigocto
    # Events (TODO: Add FairyPot and NutPot events)
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_ABOVE_BIGOCTO, world, [
        [Locations.JABU_JABUS_BELLY_ABOVE_BIG_OCTO_POT_1, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_ABOVE_BIG_OCTO_POT_2, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_ABOVE_BIG_OCTO_POT_3, lambda state: can_break_pots(state, world)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_ABOVE_BIGOCTO, world, [
        [Regions.JABU_JABUS_BELLY_LIFT_UPPER, lambda state: can_use(Items.BOOMERANG, state, world)]
    ])

    ## Jabu Jabu's Belly Lift Upper
    # Events
    add_events(Regions.JABU_JABUS_BELLY_LIFT_UPPER, world, [
        [EventLocations.JABU_JABUS_BELLY_LOWERED_PATH, LocalEvents.JABU_JABUS_BELLY_LOWERED_PATH_ACTIVATED, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_LIFT_UPPER, world, [
        [Regions.JABU_JABUS_BELLY_MAIN, lambda state: True]
    ])

    ## Jabu Jabu's Belly Near Boss Room
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, world, [
        [Locations.JABU_JABUS_BELLY_GS_NEAR_BOSS, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.BOMB_THROW)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, world, [
        [Regions.JABU_JABUS_BELLY_MAIN, lambda state: True],
        [Regions.JABU_JABUS_BELLY_BOSS_ENTRYWAY, lambda state: can_use(Items.BOOMERANG, state, world) or (can_do_trick("Jabu Near Boss Ranged", state, world) and (can_use(Items.HOOKSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world) or can_use(Items.FAIRY_SLINGSHOT, state, world))) or (can_do_trick("Jabu Near Boss Explosives", state, world) and (can_use(Items.BOMBCHU_5, state, world) or (can_use(Items.HOVER_BOOTS, state, world) and can_use(Items.BOMB_BAG, state, world))))]
    ])

    # Skipping master quest for now

    ## Jabu Jabu's Belly Boss Entryway
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BOSS_ENTRYWAY, world, [
        [Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, lambda state: True],
        [Regions.JABU_JABUS_BELLY_BOSS_ROOM, lambda state: True]
    ])

    ## Jabu Jabu's Belly Boss Exit
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BOSS_EXIT, world, [
        [Regions.JABU_JABUS_BELLY_NEAR_BOSS_ROOM, lambda state: True]
        # skipping mq connection
    ])

    ## Jabu Jabu's Belly Boss Room
    # Events
    add_events(Regions.JABU_JABUS_BELLY_BOSS_ROOM, world, [
        [EventLocations.JABU_JABUS_BELLY_BOSS, Events.CLEARED_JABU_JABUS_BELLY, lambda state: can_kill_enemy(state, world, Enemies.BARINADE)]
    ])
    # Locations
    add_locations(Regions.JABU_JABUS_BELLY_BOSS_ROOM, world, [
        [Locations.JABU_JABUS_BELLY_BARINADE_POT_1, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_BARINADE_POT_2, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_BARINADE_POT_3, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_BARINADE_POT_4, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_BARINADE_POT_5, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_BARINADE_POT_6, lambda state: can_break_pots(state, world)],
        [Locations.JABU_JABUS_BELLY_BARINADE_HEART, lambda state: has_item(Events.CLEARED_JABU_JABU_BELLY, state, world)],
        [Locations.BARINADE, lambda state: has_item(Events.CLEARED_JABU_JABU_BELLY, state, world)]
    ])
    # Connections
    connect_regions(Regions.JABU_JABUS_BELLY_BOSS_ROOM, world, [
        [Regions.JABU_JABUS_BELLY_BOSS_EXIT, lambda state: True],
        [Regions.ZORAS_FOUNTAIN, lambda state: has_item(Events.CLEARED_JABU_JABU_BELLY, state, world)]
    ])
    
