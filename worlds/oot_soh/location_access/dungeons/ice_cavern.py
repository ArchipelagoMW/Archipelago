from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld

class EventLocations(StrEnum):
    ICE_CAVERN_BLUE_FIRE_ACCESS = "Ice Cavern Blue Fire Access"


def set_region_rules(world: "SohWorld") -> None:
    ## Ice Cavern Entryway
    # Locations
    add_locations(Regions.ICE_CAVERN_ENTRYWAY, world, [])
    # Connections
    connect_regions(Regions.ICE_CAVERN_ENTRYWAY, world, [
        (Regions.ICE_CAVERN_BEGINNING, lambda bundle: True),
        # Skipping MQ
        (Regions.ZF_LEDGE, lambda bundle: True)
    ])

    ## Ice Cavern Beginning
    # Locations
    add_locations(Regions.ICE_CAVERN_BEGINNING, world, [
        (Locations.ICE_CAVERN_ENTRANCE_SONG_OF_STORMS_FAIRY, lambda bundle: can_use(Items.SONG_OF_STORMS, bundle))
    ])
    # Connections
    connect_regions(Regions.ICE_CAVERN_BEGINNING, world, [
        (Regions.ICE_CAVERN_ENTRYWAY, lambda bundle: True),
        # Skipping MQ
        (Regions.ICE_CAVERN, lambda bundle: can_kill_enemy(bundle, Enemies.FREEZARD, EnemyDistance.CLOSE, True, 4))
    ])

    ## Ice Cavern Main
    # Events
    add_events(Regions.ICE_CAVERN, world, [
        (EventLocations.ICE_CAVERN_BLUE_FIRE_ACCESS, Events.CAN_ACCESS_BLUE_FIRE, lambda bundle: is_adult(bundle) or (can_do_trick(Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle)))
    ])
    # Locations
    add_locations(Regions.ICE_CAVERN, world, [
        (Locations.ICE_CAVERN_MAP_CHEST, lambda bundle: blue_fire(bundle) and (is_adult(bundle) or (can_do_trick(Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle)))),
        (Locations.ICE_CAVERN_COMPASS_CHEST, lambda bundle: blue_fire(bundle)),
        (Locations.ICE_CAVERN_IRON_BOOTS_CHEST, lambda bundle: blue_fire(bundle) and can_kill_enemy(bundle, Enemies.WOLFOS)),
        (Locations.SHEIK_IN_ICE_CAVERN, lambda bundle: blue_fire(bundle) and can_kill_enemy(bundle, Enemies.WOLFOS) and is_adult(bundle)),
        (Locations.ICE_CAVERN_FREESTANDING_POH, lambda bundle: blue_fire(bundle)),
        (Locations.ICE_CAVERN_GS_SPINNING_SCYTHE_ROOM, lambda bundle: hookshot_or_boomerang(bundle)),
        (Locations.ICE_CAVERN_GS_HEART_PIECE_ROOM, lambda bundle: blue_fire(bundle) and hookshot_or_boomerang(bundle)),
        (Locations.ICE_CAVERN_GS_PUSH_BLOCK_ROOM, lambda bundle: blue_fire(bundle) and (hookshot_or_boomerang(bundle) or (can_do_trick(Tricks.ICE_BLOCK_GS, bundle) and can_use(Items.HOVER_BOOTS, bundle)))),
        (Locations.ICE_CAVERN_HALL_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_HALL_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_SPINNING_BLADE_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_SPINNING_BLADE_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_SPINNING_BLADE_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.ICE_CAVERN_NEAR_END_POT1, lambda bundle: can_break_pots(bundle) and blue_fire(bundle)),
        (Locations.ICE_CAVERN_NEAR_END_POT2, lambda bundle: can_break_pots(bundle) and blue_fire(bundle)),
        (Locations.ICE_CAVERN_FROZEN_POT1, lambda bundle: can_break_pots(bundle) and blue_fire(bundle) and (is_adult(bundle) or (can_do_trick(Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle)))),
        (Locations.ICE_CAVERN_LOBBY_RUPEE, lambda bundle: blue_fire(bundle)),
        (Locations.ICE_CAVERN_MAP_ROOM_LEFT_HEART, lambda bundle: is_adult(bundle) or (can_do_trick(Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle))),
        (Locations.ICE_CAVERN_MAP_ROOM_MIDDLE_HEART, lambda bundle: is_adult(bundle) or (can_do_trick(Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle))),
        (Locations.ICE_CAVERN_MAP_ROOM_RIGHT_HEART, lambda bundle: is_adult(bundle) or (can_do_trick(Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle))),
        (Locations.ICE_CAVERN_SLIDING_BLOCK_ROOM_RUPEE1, lambda bundle: blue_fire(bundle) and (can_use(Items.SONG_OF_TIME, bundle) or can_use(Items.BOOMERANG, bundle))),
        (Locations.ICE_CAVERN_SLIDING_BLOCK_ROOM_RUPEE2, lambda bundle: blue_fire(bundle) and (can_use(Items.SONG_OF_TIME, bundle) or can_use(Items.BOOMERANG, bundle))),
        (Locations.ICE_CAVERN_SLIDING_BLOCK_ROOM_RUPEE3, lambda bundle: blue_fire(bundle) and (can_use(Items.SONG_OF_TIME, bundle) or can_use(Items.BOOMERANG, bundle)))
    ])
    # Connections
    ## TODO The SOH logic also doesn't connect back to anything. May need to in Archi
    connect_regions(Regions.ICE_CAVERN, world, [])
