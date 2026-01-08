from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    FOREST_TEMPLE_MEG = "Forest Temple Meg"
    FOREST_TEMPLE_JOELLE = "Forest Temple Joelle"
    FOREST_TEMPLE_AMY = "Forest Temple Amy"
    FOREST_TEMPLE_BETH = "Forest Temple Beth"
    FOREST_TEMPLE_LOWER_STALFOS_FAIRY_POT = "Forest Temple Lower Stalfos Fairy Pot"
    FOREST_TEMPLE_NW_OUTDOORS_LOWER_DEKU_BABA_STICKS = "Forest Temple NW Outdoors Lower Deku Baba Sticks"
    FOREST_TEMPLE_NW_OUTDOORS_LOWER_DEKU_BABA_NUTS = "Forest Temple NW Outdoors Lower Deku Baba Nuts"
    FOREST_TEMPLE_NW_OUTDOORS_UPPER_DEKU_BABA_STICKS = "Forest Temple NW Outdoors Upper Deku Baba Sticks"
    FOREST_TEMPLE_NW_OUTDOORS_UPPER_DEKU_BABA_NUTS = "Forest Temple NW Outdoors Upper Deku Baba Nuts"
    FOREST_TEMPLE_NE_OUTDOORS_UPPER_DEKU_BABA_STICKS = "Forest Temple NE Outdoors Upper Deku Baba Sticks"
    FOREST_TEMPLE_NE_OUTDOORS_UPPER_DEKU_BABA_NUTS = "Forest Temple NE Outdoors Upper Deku Baba Nuts"
    FOREST_TEMPLE_NE_OUTDOORS_LOWER_DEKU_BABA_STICKS = "Forest Temple NE Outdoors Lower Deku Baba Sticks"
    FOREST_TEMPLE_NE_OUTDOORS_LOWER_DEKU_BABA_NUTS = "Forest Temple NE Outdoors Lower Deku Baba Nuts"
    FOREST_TEMPLE_NE_OUTDOORS_UPPER_DRAIN_WELL = "Forest Temple NE Outdoors Upper Drain Well"
    FOREST_TEMPLE_PHANTOM_GANON = "Forest Temple Phantom Ganon"


class LocalEvents(StrEnum):
    DEFEATED_MEG = "Defeated Meg"
    DEFEATED_JOELLE = "Defeated Joelle"
    DEFEATED_AMY = "Defeated Amy"
    DEFEATED_BETH = "Defeated Beth"
    DRAINED_WELL = "Drained the Well"


def set_region_rules(world: "SohWorld") -> None:
    # Forest Temple Entryway
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_ENTRYWAY, world, [
        # Todo: Change this when we have IsVanilla vs. IsMQ
        (Regions.FOREST_TEMPLE_FIRST_ROOM, lambda bundle: True),
        (Regions.SACRED_FOREST_MEADOW, lambda bundle: True)
    ])

    # Forest Temple First Room
    # Locations
    add_locations(Regions.FOREST_TEMPLE_FIRST_ROOM, world, [
        (Locations.FOREST_TEMPLE_FIRST_ROOM_CHEST, lambda bundle: True),
        (Locations.FOREST_TEMPLE_GS_FIRST_ROOM, lambda bundle: ((is_adult(bundle) and can_use(Items.BOMB_BAG, bundle)) or
                                                                can_use(Items.FAIRY_BOW, bundle) or
                                                                can_use(Items.HOOKSHOT, bundle) or
                                                                can_use(Items.BOOMERANG, bundle) or
                                                                can_use(Items.FAIRY_SLINGSHOT, bundle) or
                                                                can_use(Items.BOMBCHUS_5, bundle) or
                                                                can_use(Items.DINS_FIRE, bundle) or
                                                                (can_do_trick(Tricks.FOREST_FIRST_GS, bundle) and (can_jump_slash_except_hammer(bundle) or (is_child(bundle) and can_use(Items.BOMB_BAG, bundle)))))),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_FIRST_ROOM, world, [
        (Regions.FOREST_TEMPLE_ENTRYWAY, lambda bundle: True),
        (Regions.FOREST_TEMPLE_SOUTH_CORRIDOR, lambda bundle: True)
    ])

    # Forest Temple South Corridor
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_SOUTH_CORRIDOR, world, [
        (Regions.FOREST_TEMPLE_FIRST_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: (
            can_pass_enemy(bundle, Enemies.BIG_SKULLTULA)))
    ])

    # Foest Temple Lobby
    # Events
    add_events(Regions.FOREST_TEMPLE_LOBBY, world, [
        (EventLocations.FOREST_TEMPLE_MEG, LocalEvents.DEFEATED_MEG, lambda bundle: (has_item(LocalEvents.DEFEATED_JOELLE, bundle) and
                                                                                     has_item(LocalEvents.DEFEATED_BETH, bundle) and
                                                                                     has_item(LocalEvents.DEFEATED_AMY, bundle) and
                                                                                     can_kill_enemy(bundle, Enemies.MEG)))
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_LOBBY, world, [
        (Locations.FOREST_TEMPLE_GS_LOBBY,
         lambda bundle: hookshot_or_boomerang(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT3, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT4, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT5, lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOBBY_POT6, lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_LOBBY, world, [
        (Regions.FOREST_TEMPLE_SOUTH_CORRIDOR, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NORTH_CORRIDOR, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, lambda bundle: (
            can_use(Items.SONG_OF_TIME, bundle) or is_child(bundle))),
        (Regions.FOREST_TEMPLE_NE_OUTDOORS_LOWER, lambda bundle: (
            can_use(Items.FAIRY_BOW, bundle) or can_use(Items.FAIRY_SLINGSHOT, bundle))),
        (Regions.FOREST_TEMPLE_WEST_CORRIDOR, lambda bundle: (
            small_keys(Items.FOREST_TEMPLE_SMALL_KEY, 1, bundle))),
        (Regions.FOREST_TEMPLE_EAST_CORRIDOR, lambda bundle: False),
        (Regions.FOREST_TEMPLE_BOSS_REGION, lambda bundle: has_item(
            LocalEvents.DEFEATED_MEG, bundle)),
        (Regions.FOREST_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False)
    ])

    # Forest Temple North Corridor
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NORTH_CORRIDOR, world, [
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.FOREST_TEMPLE_LOWER_STALFOS, lambda bundle: True)
    ])

    # Forest Temple Lower Stalfos
    # Events
    add_events(Regions.FOREST_TEMPLE_LOWER_STALFOS, world, [
        (EventLocations.FOREST_TEMPLE_LOWER_STALFOS_FAIRY_POT,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True),
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_LOWER_STALFOS, world, [
        (Locations.FOREST_TEMPLE_FIRST_STALFOS_CHEST, lambda bundle: (
            can_kill_enemy(bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2))),
        (Locations.FOREST_TEMPLE_LOWER_STALFOS_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_LOWER_STALFOS_POT2,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_LOWER_STALFOS, world, [
        (Regions.FOREST_TEMPLE_NORTH_CORRIDOR, lambda bundle: True)
    ])

    # Forest Temple NW Outdoors Lower
    # Events
    add_events(Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, world, [
        (EventLocations.FOREST_TEMPLE_NW_OUTDOORS_LOWER_DEKU_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.FOREST_TEMPLE_NW_OUTDOORS_LOWER_DEKU_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, world, [
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: can_use(
            Items.SONG_OF_TIME, bundle)),
        (Regions.FOREST_TEMPLE_NW_COURTYARD_SKULLTULA_ISLAND,
         lambda bundle: can_use(Items.LONGSHOT, bundle)),
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_UPPER, lambda bundle: (
            can_use(Items.HOVER_BOOTS, bundle) and (
                (can_do_trick(Tricks.HOVER_BOOST_SIMPLE, bundle) and can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and has_explosives(bundle)) or
                (can_do_trick(Tricks.GROUND_JUMP_HARD, bundle) and can_ground_jump(bundle))))),
        (Regions.FOREST_TEMPLE_MAP_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_WELL, lambda bundle:
            ((has_item(Items.GOLDEN_SCALE, bundle) or
              can_use(Items.IRON_BOOTS, bundle)) or
             has_item(LocalEvents.DRAINED_WELL, bundle))),
        (Regions.FOREST_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False),
        (Regions.FOREST_TEMPLE_NW_COURTYARD_HEARTS, lambda bundle: (can_use(Items.BOOMERANG, bundle) and
                                                                    can_do_trick(Tricks.FOREST_OUTDOORS_HEARTS_BOOMERANG, bundle)))
    ])

    # Forest Temple NW Outdoors Upper
    # Events
    add_events(Regions.FOREST_TEMPLE_NW_OUTDOORS_UPPER, world, [
        (EventLocations.FOREST_TEMPLE_NW_OUTDOORS_UPPER_DEKU_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.FOREST_TEMPLE_NW_OUTDOORS_UPPER_DEKU_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle)),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NW_OUTDOORS_UPPER, world, [
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NW_COURTYARD_SKULLTULA_ISLAND,
         lambda bundle: hookshot_or_boomerang(bundle)),
        (Regions.FOREST_TEMPLE_BELOW_BOSS_KEY_CHEST, lambda bundle: True),
        (Regions.FOREST_TEMPLE_FLOORMASTER_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_BLOCK_PUSH_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NW_COURTYARD_HEARTS, lambda bundle: True)
    ])

    # Forest Temple NW Courtyard Hearts
    # Locations
    add_locations(Regions.FOREST_TEMPLE_NW_COURTYARD_HEARTS, world, [
        (Locations.FOREST_TEMPLE_WEST_COURTYARD_RIGHT_HEART, lambda bundle: True),
        (Locations.FOREST_TEMPLE_WEST_COURTYARD_LEFT_HEART, lambda bundle: True)
    ])

    # Forest Temple Courtyard Skulltula Island
    # Locations
    add_locations(Regions.FOREST_TEMPLE_NW_COURTYARD_SKULLTULA_ISLAND, world, [
        (Locations.FOREST_TEMPLE_GS_LEVEL_ISLAND_COURTYARD, lambda bundle: True)
    ])

    # Forest Temple NE Outdoors Lower
    # Events
    add_events(Regions.FOREST_TEMPLE_NE_OUTDOORS_LOWER, world, [
        (EventLocations.FOREST_TEMPLE_NE_OUTDOORS_LOWER_DEKU_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.FOREST_TEMPLE_NE_OUTDOORS_LOWER_DEKU_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NE_OUTDOORS_LOWER, world, [
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NE_OUTDOORS_UPPER, lambda bundle: (can_use(Items.LONGSHOT, bundle) or
                                                                  (can_do_trick(Tricks.FOREST_VINES, bundle) and can_use(Items.HOOKSHOT, bundle)))),
        (Regions.FOREST_TEMPLE_WELL, lambda bundle:
            ((has_item(Items.GOLDEN_SCALE, bundle) or
              can_use(Items.IRON_BOOTS, bundle)) or
             has_item(LocalEvents.DRAINED_WELL, bundle))),
        (Regions.FOREST_TEMPLE_FALLING_ROOM, lambda bundle: False),
        (Regions.FOREST_TEMPLE_NE_COURTYARD_SKULLTULA_ISLAND,
         lambda bundle: (can_use(Items.HOOKSHOT, bundle))),
        (Regions.FOREST_TEMPLE_NE_COURTYARD_SKULLTULA_ISLAND_GS, lambda bundle: (can_use(Items.HOOKSHOT, bundle) or
                                                                                 (can_do_trick(Tricks.FOREST_OUTDOORS_EAST_GS, bundle) and can_use(Items.BOOMERANG, bundle))))
    ])

    # Forest Temple NE Outdoors Upper
    # Events
    add_events(Regions.FOREST_TEMPLE_NE_OUTDOORS_UPPER, world, [
        (EventLocations.FOREST_TEMPLE_NE_OUTDOORS_UPPER_DRAIN_WELL,
         LocalEvents.DRAINED_WELL, lambda bundle: True),
        (EventLocations.FOREST_TEMPLE_NE_OUTDOORS_UPPER_DEKU_BABA_STICKS,
         Events.CAN_FARM_STICKS, lambda bundle: can_get_deku_baba_sticks(bundle)),
        (EventLocations.FOREST_TEMPLE_NE_OUTDOORS_UPPER_DEKU_BABA_NUTS,
         Events.CAN_FARM_NUTS, lambda bundle: can_get_deku_baba_nuts(bundle)),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NE_OUTDOORS_UPPER, world, [
        (Regions.FOREST_TEMPLE_NE_OUTDOORS_LOWER, lambda bundle: True),
        (Regions.FOREST_TEMPLE_MAP_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_FALLING_ROOM, lambda bundle: (can_do_trick(Tricks.FOREST_DOORFRAME, bundle) and
                                                             can_jump_slash_except_hammer(bundle) and
                                                             can_use(Items.HOVER_BOOTS, bundle) and
                                                             can_use(Items.SCARECROW, bundle))),
        (Regions.FOREST_TEMPLE_NE_COURTYARD_SKULLTULA_ISLAND, lambda bundle: (is_adult(bundle) and
                                                                              can_do_trick(Tricks.FOREST_OUTDOORS_LEDGE, bundle) and
                                                                              can_use(Items.HOVER_BOOTS, bundle)))
    ])

    # Forest Temple NE Courtyard Skulltula Island
    # Locations
    add_locations(Regions.FOREST_TEMPLE_NE_COURTYARD_SKULLTULA_ISLAND, world, [
        (Locations.FOREST_TEMPLE_RAISED_ISLAND_COURTYARD_CHEST, lambda bundle: True)
    ])

    # Forest Temple NE Courtyard Skulltula Island GS
    # Locations
    add_locations(Regions.FOREST_TEMPLE_NE_COURTYARD_SKULLTULA_ISLAND_GS, world, [
        (Locations.FOREST_TEMPLE_GS_RAISED_ISLAND_COURTYARD, lambda bundle: True)
    ])

    # Forest Temple Map Room
    # Locations
    add_locations(Regions.FOREST_TEMPLE_MAP_ROOM, world, [
        (Locations.FOREST_TEMPLE_MAP_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.BLUE_BUBBLE))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_MAP_ROOM, world, [
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER,
         lambda bundle: can_kill_enemy(bundle, Enemies.BLUE_BUBBLE)),
        (Regions.FOREST_TEMPLE_NE_OUTDOORS_UPPER,
         lambda bundle: can_kill_enemy(bundle, Enemies.BLUE_BUBBLE)),
    ])

    # Forest Temple Well
    # Locations
    add_locations(Regions.FOREST_TEMPLE_WELL, world, [
        (Locations.FOREST_TEMPLE_WELL_CHEST, lambda bundle:
            ((can_open_underwater_chest(bundle) and
              water_timer(bundle) >= 8) or
             has_item(LocalEvents.DRAINED_WELL, bundle))),
        (Locations.FOREST_TEMPLE_WELL_WEST_HEART, lambda bundle:
            ((can_use(Items.IRON_BOOTS, bundle) and
              water_timer(bundle) >= 8) or
             has_item(LocalEvents.DRAINED_WELL, bundle))),
        (Locations.FOREST_TEMPLE_WELL_EAST_HEART, lambda bundle:
            ((can_use(Items.IRON_BOOTS, bundle) and
              water_timer(bundle) >= 8) or
             has_item(LocalEvents.DRAINED_WELL, bundle)))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_WELL, world, [
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_LOWER, lambda bundle:
            has_item(Items.BRONZE_SCALE, bundle) or
            has_item(LocalEvents.DRAINED_WELL, bundle)),
        (Regions.FOREST_TEMPLE_NE_OUTDOORS_LOWER, lambda bundle:
            has_item(Items.BRONZE_SCALE, bundle) or
            has_item(LocalEvents.DRAINED_WELL, bundle))
    ])

    # Forest Temple Below Boss Key Chest
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_BELOW_BOSS_KEY_CHEST, world, [
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_UPPER,
         lambda bundle: can_kill_enemy(bundle, Enemies.BLUE_BUBBLE))
    ])

    # Forest Temple Floormaster Room
    # Locations
    add_locations(Regions.FOREST_TEMPLE_FLOORMASTER_ROOM, world, [
        (Locations.FOREST_TEMPLE_FLOORMASTER_CHEST,
         lambda bundle: can_damage(bundle))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_FLOORMASTER_ROOM, world, [
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_UPPER, lambda bundle: True)
    ])

    # Forest Temple West Corridor
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_WEST_CORRIDOR, world, [
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: small_keys(
            Items.FOREST_TEMPLE_SMALL_KEY, 1, bundle)),
        (Regions.FOREST_TEMPLE_BLOCK_PUSH_ROOM, lambda bundle: (
            can_attack(bundle) or can_use(Items.NUTS, bundle)))
    ])

    # Forest Temple Block Push Room
    # Locations
    add_locations(Regions.FOREST_TEMPLE_BLOCK_PUSH_ROOM, world, [
        (Locations.FOREST_TEMPLE_EYE_SWITCH_CHEST, lambda bundle: (has_item(Items.GORONS_BRACELET, bundle) and
                                                                   (can_use(Items.FAIRY_BOW, bundle) or can_use(Items.FAIRY_SLINGSHOT, bundle))))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_BLOCK_PUSH_ROOM, world, [
        (Regions.FOREST_TEMPLE_WEST_CORRIDOR, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NW_OUTDOORS_UPPER, lambda bundle: (can_use(Items.HOVER_BOOTS, bundle) or
                                                                  (can_do_trick(Tricks.FOREST_OUTSIDE_BACKDOOR, bundle) and
                                                                   can_jump_slash_except_hammer(bundle) and
                                                                   has_item(Items.GORONS_BRACELET, bundle)))),
        (Regions.FOREST_TEMPLE_NW_CORRIDOR_TWISTED, lambda bundle: (is_adult(bundle) and
                                                                    has_item(Items.GORONS_BRACELET, bundle) and
                                                                    small_keys(Items.FOREST_TEMPLE_SMALL_KEY, 2, bundle))),
        (Regions.FOREST_TEMPLE_NW_CORRIDOR_STRAIGHTENED, lambda bundle: (is_adult(bundle) and
                                                                         (can_use(Items.FAIRY_BOW, bundle) or
                                                                          can_use(Items.FAIRY_SLINGSHOT, bundle)) and
                                                                         has_item(Items.GORONS_BRACELET, bundle) and
                                                                         small_keys(Items.FOREST_TEMPLE_SMALL_KEY, 2, bundle)))
    ])

    # Forest Temple NW Corridor Twisted
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NW_CORRIDOR_TWISTED, world, [
        (Regions.FOREST_TEMPLE_BLOCK_PUSH_ROOM, lambda bundle: small_keys(
            Items.FOREST_TEMPLE_SMALL_KEY, 2, bundle)),
        (Regions.FOREST_TEMPLE_RED_POE_ROOM, lambda bundle: small_keys(
            Items.FOREST_TEMPLE_SMALL_KEY, 3, bundle))
    ])

    # Forest Temple NW Corridor Straightened
    # Locations
    add_locations(Regions.FOREST_TEMPLE_NW_CORRIDOR_STRAIGHTENED, world, [
        (Locations.FOREST_TEMPLE_BOSS_KEY_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NW_CORRIDOR_STRAIGHTENED, world, [
        (Regions.FOREST_TEMPLE_BELOW_BOSS_KEY_CHEST, lambda bundle: True),
        (Regions.FOREST_TEMPLE_BLOCK_PUSH_ROOM, lambda bundle: small_keys(
            Items.FOREST_TEMPLE_SMALL_KEY, 2, bundle))
    ])

    # Forest Temple Red Poe Room
    # Events
    add_events(Regions.FOREST_TEMPLE_RED_POE_ROOM, world, [
        (EventLocations.FOREST_TEMPLE_JOELLE, LocalEvents.DEFEATED_JOELLE,
         lambda bundle: can_use(Items.FAIRY_BOW, bundle))
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_RED_POE_ROOM, world, [
        (Locations.FOREST_TEMPLE_RED_POE_CHEST,
         lambda bundle: has_item(LocalEvents.DEFEATED_JOELLE, bundle))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_RED_POE_ROOM, world, [
        (Regions.FOREST_TEMPLE_NW_CORRIDOR_TWISTED, lambda bundle: small_keys(
            Items.FOREST_TEMPLE_SMALL_KEY, 3, bundle)),
        (Regions.FOREST_TEMPLE_UPPER_STALFOS, lambda bundle: True)
    ])

    # Forest Temple Upper Stalfos
    # Locations
    add_locations(Regions.FOREST_TEMPLE_UPPER_STALFOS, world, [
        (Locations.FOREST_TEMPLE_BOW_CHEST, lambda bundle: can_kill_enemy(
            bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 3)),
        (Locations.FOREST_TEMPLE_UPPER_STALFOS_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_UPPER_STALFOS_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_UPPER_STALFOS_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_UPPER_STALFOS_POT4,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_UPPER_STALFOS, world, [
        (Regions.FOREST_TEMPLE_RED_POE_ROOM, lambda bundle: can_kill_enemy(
            bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 3)),
        (Regions.FOREST_TEMPLE_BLUE_POE_ROOM, lambda bundle: can_kill_enemy(
            bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 3))
    ])

    # Forest Temple Blue Poe Room
    # Events
    add_events(Regions.FOREST_TEMPLE_BLUE_POE_ROOM, world, [
        (EventLocations.FOREST_TEMPLE_BETH, LocalEvents.DEFEATED_BETH,
         lambda bundle: can_use(Items.FAIRY_BOW, bundle))
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_BLUE_POE_ROOM, world, [
        (Locations.FOREST_TEMPLE_BLUE_POE_CHEST,
         lambda bundle: has_item(LocalEvents.DEFEATED_BETH, bundle)),
        (Locations.FOREST_TEMPLE_BLUE_POE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_BLUE_POE_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_BLUE_POE_POT3,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_BLUE_POE_ROOM, world, [
        (Regions.FOREST_TEMPLE_UPPER_STALFOS, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NE_CORRIDOR_STRAIGHTENED,
         lambda bundle: small_keys(Items.FOREST_TEMPLE_SMALL_KEY, 4, bundle))
    ])

    # Forest Temple NE Corridor Straightened
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NE_CORRIDOR_STRAIGHTENED, world, [
        (Regions.FOREST_TEMPLE_BLUE_POE_ROOM, lambda bundle: small_keys(
            Items.FOREST_TEMPLE_SMALL_KEY, 4, bundle)),
        (Regions.FOREST_TEMPLE_FROZEN_EYE_ROOM, lambda bundle: small_keys(
            Items.FOREST_TEMPLE_SMALL_KEY, 5, bundle))
    ])

    # Forest Temple NE Corridor Twisted
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_NE_CORRIDOR_TWISTED, world, [
        (Regions.FOREST_TEMPLE_FROZEN_EYE_ROOM, lambda bundle: small_keys(
            Items.FOREST_TEMPLE_SMALL_KEY, 5, bundle)),
        (Regions.FOREST_TEMPLE_FALLING_ROOM, lambda bundle: True)
    ])

    # Forest Temple Frozen Eye Room
    # Locations
    add_locations(Regions.FOREST_TEMPLE_FROZEN_EYE_ROOM, world, [
        (Locations.FOREST_TEMPLE_FROZEN_EYE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_FROZEN_EYE_POT2,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_FROZEN_EYE_ROOM, world, [
        (Regions.FOREST_TEMPLE_NE_CORRIDOR_STRAIGHTENED,
         lambda bundle: small_keys(Items.FOREST_TEMPLE_SMALL_KEY, 5, bundle)),
        (Regions.FOREST_TEMPLE_NE_CORRIDOR_TWISTED, lambda bundle: (small_keys(Items.FOREST_TEMPLE_SMALL_KEY, 5, bundle) and
                                                                    (can_use(Items.FAIRY_BOW, bundle) or can_use(Items.DINS_FIRE, bundle))))
    ])

    # Forest Temple Falling Room
    # Locations
    add_locations(Regions.FOREST_TEMPLE_FALLING_ROOM, world, [
        (Locations.FOREST_TEMPLE_FALLING_CEILING_ROOM_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_FALLING_ROOM, world, [
        (Regions.FOREST_TEMPLE_NE_OUTDOORS_LOWER, lambda bundle: True),
        (Regions.FOREST_TEMPLE_GREEN_POE_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NE_COURTYARD_SKULLTULA_ISLAND, lambda bundle: True),
        (Regions.FOREST_TEMPLE_NE_COURTYARD_SKULLTULA_ISLAND_GS, lambda bundle: (can_use(Items.FAIRY_BOW, bundle) or
                                                                                 can_use(Items.FAIRY_SLINGSHOT, bundle) or
                                                                                 can_use(Items.DINS_FIRE, bundle) or
                                                                                 has_explosives(bundle)))
    ])

    # Forest Temple Green Poe Room
    # Events
    add_events(Regions.FOREST_TEMPLE_GREEN_POE_ROOM, world, [
        (EventLocations.FOREST_TEMPLE_AMY, LocalEvents.DEFEATED_AMY,
         lambda bundle: can_use(Items.FAIRY_BOW, bundle))
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_GREEN_POE_ROOM, world, [
        (Locations.FOREST_TEMPLE_GREEN_POE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.FOREST_TEMPLE_GREEN_POE_POT2,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_GREEN_POE_ROOM, world, [
        (Regions.FOREST_TEMPLE_FALLING_ROOM, lambda bundle: True),
        (Regions.FOREST_TEMPLE_EAST_CORRIDOR,
         lambda bundle: has_item(LocalEvents.DEFEATED_AMY, bundle))
    ])

    # Foest Temple East Corridor
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_EAST_CORRIDOR, world, [
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: (
            can_attack(bundle) or can_use(Items.NUTS, bundle))),
        (Regions.FOREST_TEMPLE_GREEN_POE_ROOM, lambda bundle: (
            can_attack(bundle) or can_use(Items.NUTS, bundle)))
    ])

    # Forest Temple Boss Region
    # Locations
    add_locations(Regions.FOREST_TEMPLE_BOSS_REGION, world, [
        (Locations.FOREST_TEMPLE_BASEMENT_CHEST, lambda bundle: True),
        (Locations.FOREST_TEMPLE_GS_BASEMENT,
         lambda bundle: hookshot_or_boomerang(bundle))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_BOSS_REGION, world, [
        (Regions.FOREST_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.FOREST_TEMPLE_BOSS_ENTRYWAY, lambda bundle: True)
    ])

    # Forest Temple Boss Entryway
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_BOSS_ENTRYWAY, world, [
        (Regions.FOREST_TEMPLE_BOSS_REGION, lambda bundle: False),
        # Todo: Connect to MQ_BOSS_REGION
        (Regions.FOREST_TEMPLE_BOSS_ROOM, lambda bundle: has_item(
            Items.FOREST_TEMPLE_BOSS_KEY, bundle))
    ])

    # Forest Temple Boss Room
    # Events
    add_events(Regions.FOREST_TEMPLE_BOSS_ROOM, world, [
        (EventLocations.FOREST_TEMPLE_PHANTOM_GANON, Events.FOREST_TEMPLE_COMPLETED,
         lambda bundle: can_kill_enemy(bundle, Enemies.PHANTOM_GANON))
    ])
    # Locations
    add_locations(Regions.FOREST_TEMPLE_BOSS_ROOM, world, [
        (Locations.FOREST_TEMPLE_PHANTOM_GANON_HEART_CONTAINER,
         lambda bundle: has_item(Events.FOREST_TEMPLE_COMPLETED, bundle)),
        (Locations.PHANTOM_GANON, lambda bundle: has_item(
            Events.FOREST_TEMPLE_COMPLETED, bundle))
    ])
    # Connections
    connect_regions(Regions.FOREST_TEMPLE_BOSS_ROOM, world, [
        (Regions.FOREST_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False),
        (Regions.SACRED_FOREST_MEADOW, lambda bundle: has_item(
            Events.FOREST_TEMPLE_COMPLETED, bundle))
    ])
