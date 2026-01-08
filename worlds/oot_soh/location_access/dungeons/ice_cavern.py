from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    ICE_CAVERN_MAP_ROOM_BLUE_FIRE_ACCESS = "Ice Cavern Map Room Blue Fire Access"
    ICE_CAVERN_COMPASS_ROOM_BLUE_FIRE_ACCESS = "Ice Cavern Compass Room Blue Fire Access"
    ICE_CAVERN_BLOCK_ROOM_BLUE_FIRE_ACCESS = "Ice Cavern Block Room Blue Fire Access"


def set_region_rules(world: "SohWorld") -> None:
    # Ice Cavern Entryway
    # Locations
    add_locations(Regions.ICE_CAVERN_ENTRYWAY, world, [])
    # Connections
    connect_regions(Regions.ICE_CAVERN_ENTRYWAY, world, [
        (Regions.ICE_CAVERN_BEGINNING, lambda bundle: True),
        # Skipping MQ
        (Regions.ZF_LEDGE, lambda bundle: True)
    ])

    # Ice Cavern Beginning
    # Locations
    add_locations(Regions.ICE_CAVERN_BEGINNING, world, [
        (Locations.ICE_CAVERN_ENTRANCE_SONG_OF_STORMS_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.ICE_CAVERN_LOBBY_RUPEE, lambda bundle: blue_fire(bundle))
    ])
    # Connections
    connect_regions(Regions.ICE_CAVERN_BEGINNING, world, [
        (Regions.ICE_CAVERN_ENTRYWAY, lambda bundle: True),
        (Regions.ICE_CAVERN_HUB, lambda bundle: can_kill_enemy(
            bundle, Enemies.FREEZARD, EnemyDistance.CLOSE, True, 4)),
        (Regions.ICE_CAVERN_ABOVE_BEGINNING, lambda bundle: False)
    ])

    # Ice Cavern Hub
    # Locations
    add_locations(Regions.ICE_CAVERN_HUB, world, [
        (Locations.ICE_CAVERN_GS_SPINNING_SCYTHE_ROOM,
         lambda bundle: hookshot_or_boomerang(bundle)),
        (Locations.ICE_CAVERN_HALL_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_HALL_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_SPINNING_BLADE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_SPINNING_BLADE_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_SPINNING_BLADE_POT3,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.ICE_CAVERN_HUB, world, [
        (Regions.ICE_CAVERN_BEGINNING, lambda bundle: True),
        (Regions.ICE_CAVERN_MAP_ROOM, lambda bundle: (is_adult(bundle) or (can_do_trick(
            Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle))) and can_clear_stalagmite(bundle)),
        (Regions.ICE_CAVERN_COMPASS_ROOM, lambda bundle: blue_fire(bundle)),
        (Regions.ICE_CAVERN_BLOCK_ROOM, lambda bundle: blue_fire(
            bundle) and can_clear_stalagmite(bundle))
    ])

    # Ice Cavern Map Room
    # Events
    add_events(Regions.ICE_CAVERN_MAP_ROOM, world, [
        (EventLocations.ICE_CAVERN_MAP_ROOM_BLUE_FIRE_ACCESS,
         Events.CAN_ACCESS_BLUE_FIRE, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.ICE_CAVERN_MAP_ROOM, world, [
        (Locations.ICE_CAVERN_MAP_CHEST, lambda bundle: blue_fire(bundle)),
        (Locations.ICE_CAVERN_FROZEN_POT1, lambda bundle: (can_break_pots(bundle) and blue_fire(bundle)) or has_explosives(bundle) or (can_do_trick(Tricks.RUSTED_SWITCHES, bundle) and ((can_standing_shield(bundle) and can_use(
            Items.DEKU_SHIELD, bundle)) or can_use_any([Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.MEGATON_HAMMER], bundle))) or (can_do_trick(Tricks.HOOKSHOT_EXTENSION, bundle) and can_use(Items.HOOKSHOT, bundle))),
        (Locations.ICE_CAVERN_MAP_ROOM_LEFT_HEART, lambda bundle: True),
        (Locations.ICE_CAVERN_MAP_ROOM_MIDDLE_HEART, lambda bundle: True),
        (Locations.ICE_CAVERN_MAP_ROOM_RIGHT_HEART, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.ICE_CAVERN_MAP_ROOM, world, [
        (Regions.ICE_CAVERN_HUB, lambda bundle: True)
    ])

    # Ice Cavern Compass Room
    # Events
    add_events(Regions.ICE_CAVERN_COMPASS_ROOM, world, [
        (EventLocations.ICE_CAVERN_COMPASS_ROOM_BLUE_FIRE_ACCESS,
         Events.CAN_ACCESS_BLUE_FIRE, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.ICE_CAVERN_COMPASS_ROOM, world, [
        (Locations.ICE_CAVERN_COMPASS_CHEST,
         lambda bundle: can_clear_stalagmite(bundle) and blue_fire(bundle)),
        (Locations.ICE_CAVERN_FREESTANDING_POH,
         lambda bundle: can_clear_stalagmite(bundle) and blue_fire(bundle)),
        (Locations.ICE_CAVERN_GS_HEART_PIECE_ROOM,
         lambda bundle: hookshot_or_boomerang(bundle))
    ])
    # Connections
    connect_regions(Regions.ICE_CAVERN_COMPASS_ROOM, world, [
        (Regions.ICE_CAVERN_HUB, lambda bundle: True)
    ])

    # Ice Cavern Main
    # Events
    add_events(Regions.ICE_CAVERN_BLOCK_ROOM, world, [
        (EventLocations.ICE_CAVERN_BLOCK_ROOM_BLUE_FIRE_ACCESS,
         Events.CAN_ACCESS_BLUE_FIRE, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.ICE_CAVERN_BLOCK_ROOM, world, [
        (Locations.ICE_CAVERN_GS_PUSH_BLOCK_ROOM, lambda bundle: hookshot_or_boomerang(bundle) or (can_do_trick(Tricks.ICE_BLOCK_GS, bundle) and is_adult(
            bundle) and can_use(Items.HOVER_BOOTS, bundle) and can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH))),
        (Locations.ICE_CAVERN_SLIDING_BLOCK_ROOM_RUPEE1, lambda bundle: can_use(
            Items.SONG_OF_TIME, bundle) or can_use(Items.BOOMERANG, bundle)),
        (Locations.ICE_CAVERN_SLIDING_BLOCK_ROOM_RUPEE2, lambda bundle: can_use(
            Items.SONG_OF_TIME, bundle) or can_use(Items.BOOMERANG, bundle)),
        (Locations.ICE_CAVERN_SLIDING_BLOCK_ROOM_RUPEE3, lambda bundle: can_use(
            Items.SONG_OF_TIME, bundle) or can_use(Items.BOOMERANG, bundle))
    ])
    # Connections
    connect_regions(Regions.ICE_CAVERN_BLOCK_ROOM, world, [
        (Regions.ICE_CAVERN_HUB, lambda bundle: can_clear_stalagmite(bundle)),
        (Regions.ICE_CAVERN_BEFORE_FINAL_ROOM, lambda bundle: blue_fire(bundle))
    ])

    # Ice Cavern Before Final Room
    # Locations
    add_locations(Regions.ICE_CAVERN_BEFORE_FINAL_ROOM, world, [
        (Locations.ICE_CAVERN_NEAR_END_POT1,
         lambda bundle: can_break_pots(bundle) and blue_fire(bundle)),
        (Locations.ICE_CAVERN_NEAR_END_POT2,
         lambda bundle: can_break_pots(bundle) and blue_fire(bundle))
    ])
    # Connections
    connect_regions(Regions.ICE_CAVERN_BEFORE_FINAL_ROOM, world, [
        (Regions.ICE_CAVERN_BLOCK_ROOM, lambda bundle: blue_fire(bundle)),
        (Regions.ICE_CAVERN_FINAL_ROOM, lambda bundle: True)
    ])

    # Ice Cavern Final Room
    # Locations
    add_locations(Regions.ICE_CAVERN_FINAL_ROOM, world, [
        (Locations.ICE_CAVERN_IRON_BOOTS_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.WOLFOS)),
        (Locations.SHEIK_IN_ICE_CAVERN, lambda bundle: can_kill_enemy(
            bundle, Enemies.WOLFOS))  # Rando enables this for child
    ])
    # Connections
    connect_regions(Regions.ICE_CAVERN_FINAL_ROOM, world, [
        (Regions.ICE_CAVERN_BEFORE_FINAL_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.WOLFOS)),
        (Regions.ICE_CAVERN_FINAL_ROOM_UNDERWATER, lambda bundle: can_kill_enemy(
            bundle, Enemies.WOLFOS) and can_use(Items.IRON_BOOTS, bundle))
    ])

    # Ice Cavern Final Room Underwater
    # Connections
    connect_regions(Regions.ICE_CAVERN_FINAL_ROOM_UNDERWATER, world, [
        (Regions.ICE_CAVERN_FINAL_ROOM,
         lambda bundle: can_use(Items.BRONZE_SCALE, bundle)),
        (Regions.ICE_CAVERN_ABOVE_BEGINNING,
         lambda bundle: can_use(Items.IRON_BOOTS, bundle))
    ])

    # Ice Cavern Above Beginning
    # Connections
    connect_regions(Regions.ICE_CAVERN_ABOVE_BEGINNING, world, [
        (Regions.ICE_CAVERN_FINAL_ROOM_UNDERWATER,
         lambda bundle: can_use(Items.IRON_BOOTS, bundle)),
        (Regions.ICE_CAVERN_BEGINNING, lambda bundle: True)
    ])
