from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    WATER_TEMPLE_EAST_LOWER_WATER_LOW_FROM_HIGH = "Water Temple East Lower Water Low From High"
    WATER_TEMPLE_CENTRAL_PILLAR_UPPER_WATER_MIDDLE = "Water Temple Central Pillar Upper Water Middle"
    WATER_TEMPLE_HIGH_WATER_WATER_HIGH = "Water Temple High Water Water High"
    WATER_TEMPLE_BOSS_KEY_ROOM_FAIRY_POT = "Water Temple Boss Key Room Fairy Pot"
    WATER_TEMPLE_PRE_BOSS_ROOM_FAIRY_POT = "Water Temple Pre Boss Room Fairy Pot"
    WATER_TEMPLE_MORPHA = "Water Temple Morpha"


class LocalEvents(StrEnum):
    WATER_LEVEL_LOW = "Water Level Low"
    WATER_LEVEL_MIDDLE = "Water Level Middle"
    WATER_LEVEL_HIGH = "Water Level High"


def set_region_rules(world: "SohWorld") -> None:
    # Water Temple Entryway
    # Connections
    connect_regions(Regions.WATER_TEMPLE_ENTRYWAY, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: (
            has_item(Items.BRONZE_SCALE, bundle))),
        (Regions.LH_FROM_WATER_TEMPLE, lambda bundle: True)
    ])

    # Water Temple Lobby
    # Locations
    add_locations(Regions.WATER_TEMPLE_LOBBY, world, [
        (Locations.WATER_TEMPLE_MAIN_LEVEL2_POT1, lambda bundle: (can_break_pots(bundle) and
                                                                  (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                                   has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle) or
                                                                   (can_use(Items.IRON_BOOTS, bundle) and
                                                                    can_use(Items.HOOKSHOT, bundle))))),
        (Locations.WATER_TEMPLE_MAIN_LEVEL2_POT2, lambda bundle: (can_break_pots(bundle) and
                                                                  (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                                   has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle) or
                                                                   (can_use(Items.IRON_BOOTS, bundle) and
                                                                    can_use(Items.HOOKSHOT, bundle))))),
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_LOBBY, world, [
        (Regions.WATER_TEMPLE_ENTRYWAY, lambda bundle: True),
        (Regions.WATER_TEMPLE_EAST_LOWER, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                          ((can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) or
                                                            can_use(Items.ZORA_TUNIC, bundle)) and
                                                           (can_use(Items.IRON_BOOTS, bundle) or
                                                            (can_use(Items.LONGSHOT, bundle) and
                                                             can_do_trick(Tricks.WATER_LONGSHOT_TORCH, bundle)))))),
        (Regions.WATER_TEMPLE_NORTH_LOWER, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                           ((can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) or
                                                             can_use(Items.ZORA_TUNIC, bundle)) and
                                                            can_use(Items.IRON_BOOTS, bundle)))),
        (Regions.WATER_TEMPLE_SOUTH_LOWER, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) and
                                                           has_explosives(bundle) and
                                                           (has_item(Items.SILVER_SCALE, bundle) or
                                                            can_use(Items.IRON_BOOTS, bundle)) and
                                                           (can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) or
                                                            can_use(Items.ZORA_TUNIC, bundle)))),
        (Regions.WATER_TEMPLE_WEST_LOWER, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) and
                                                          has_item(Items.GORONS_BRACELET, bundle) and
                                                          (is_child(bundle) or
                                                           has_item(Items.SILVER_SCALE, bundle) or
                                                           can_use(Items.IRON_BOOTS, bundle)) and
                                                          (can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) or
                                                           can_use(Items.ZORA_TUNIC, bundle)))),
        (Regions.WATER_TEMPLE_CENTRAL_PILLAR_LOWER, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) and
                                                                    small_keys(Items.WATER_TEMPLE_SMALL_KEY, 5, bundle))),
        (Regions.WATER_TEMPLE_CENTRAL_PILLAR_UPPER, lambda bundle: ((has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                                    has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle)) and
                                                                    (has_fire_source_with_torch(bundle) or
                                                                     can_use(Items.FAIRY_BOW, bundle)))),
        (Regions.WATER_TEMPLE_EAST_MIDDLE, lambda bundle: ((has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                            has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle) or
                                                            (can_use(Items.IRON_BOOTS, bundle) and
                                                             water_timer(bundle) >= 16)) and
                                                           can_use(Items.LONGSHOT, bundle))),
        (Regions.WATER_TEMPLE_WEST_MIDDLE, lambda bundle: (
            has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle))),
        (Regions.WATER_TEMPLE_HIGH_WATER, lambda bundle: (is_adult(bundle) and
                                                          (can_use(Items.HOVER_BOOTS, bundle) or
                                                           can_do_trick(Tricks.DAMAGE_BOOST, bundle) and
                                                           can_use(Items.BOMB_BAG, bundle) and
                                                           take_damage(bundle)))),
        (Regions.WATER_TEMPLE_BLOCK_CORRIDOR, lambda bundle: ((has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                               has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle)) and
                                                              (can_use(Items.FAIRY_SLINGSHOT, bundle) or
                                                               can_use(Items.FAIRY_BOW, bundle)) and
                                                              (can_use(Items.LONGSHOT, bundle) or
                                                               can_use(Items.HOVER_BOOTS, bundle) or
                                                               (can_do_trick(Tricks.WATER_CENTRAL_BOW, bundle) and
                                                                (is_adult(bundle) or
                                                                 has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle)))))),
        (Regions.WATER_TEMPLE_FALLING_PLATFORM_ROOM, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_HIGH, bundle) and
                                                                     small_keys(Items.WATER_TEMPLE_SMALL_KEY, 4, bundle))),
        (Regions.WATER_TEMPLE_PRE_BOSS_ROOM, lambda bundle: ((has_item(LocalEvents.WATER_LEVEL_HIGH, bundle) and
                                                              can_use(Items.LONGSHOT, bundle)) or
                                                             (can_do_trick(Tricks.HOVER_BOOST_SIMPLE, bundle) and
                                                              can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and
                                                              has_explosives(bundle) and
                                                              can_use(Items.HOVER_BOOTS, bundle))))
    ])

    # Water Temple East Lower
    # Events
    add_events(Regions.WATER_TEMPLE_EAST_LOWER, world, [
        (EventLocations.WATER_TEMPLE_EAST_LOWER_WATER_LOW_FROM_HIGH,
         LocalEvents.WATER_LEVEL_LOW, lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Locations
    add_locations(Regions.WATER_TEMPLE_EAST_LOWER, world, [
        (Locations.WATER_TEMPLE_TORCH_POT1, lambda bundle: (can_break_pots(bundle) and
                                                            (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                             (can_use(Items.HOOKSHOT, bundle) and
                                                              can_use(Items.IRON_BOOTS, bundle))))),
        (Locations.WATER_TEMPLE_TORCH_POT2, lambda bundle: (can_break_pots(bundle) and
                                                            (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                             (can_use(Items.HOOKSHOT, bundle) and
                                                              can_use(Items.IRON_BOOTS, bundle)))))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_EAST_LOWER, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                     ((can_do_trick(Tricks.FEWER_TUNIC_REQUIREMENTS, bundle) or
                                                       can_use(Items.ZORA_TUNIC, bundle)) and
                                                      can_use(Items.IRON_BOOTS, bundle)))),
        (Regions.WATER_TEMPLE_MAP_ROOM, lambda bundle: has_item(
            LocalEvents.WATER_LEVEL_HIGH, bundle)),
        (Regions.WATER_TEMPLE_CRACKED_WALL, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle) or
                                                            (has_item(LocalEvents.WATER_LEVEL_HIGH, bundle) and
                                                             has_item(LocalEvents.WATER_LEVEL_LOW, bundle) and
                                                             ((can_use(Items.HOVER_BOOTS, bundle) and
                                                               can_do_trick(Tricks.WATER_CRACKED_WALL_HOVERS, bundle)) or
                                                              can_do_trick(Tricks.WATER_CRACKED_WALL, bundle))))),
        (Regions.WATER_TEMPLE_TORCH_ROOM, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) and
                                                          (has_fire_source_with_torch(bundle) or
                                                           can_use(Items.FAIRY_BOW, bundle))))
    ])

    # Water Temple Map Room
    # Locations
    add_locations(Regions.WATER_TEMPLE_MAP_ROOM, world, [
        (Locations.WATER_TEMPLE_MAP_CHEST, lambda bundle: can_kill_enemy(
            bundle, Enemies.SPIKE, EnemyDistance.CLOSE, True, 3))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_MAP_ROOM, world, [
        (Regions.WATER_TEMPLE_EAST_LOWER, lambda bundle: can_kill_enemy(
            bundle, Enemies.SPIKE, EnemyDistance.CLOSE, True, 3))
    ])

    # Water Temple Cracked Wall
    # Locations
    add_locations(Regions.WATER_TEMPLE_CRACKED_WALL, world, [
        (Locations.WATER_TEMPLE_CRACKED_WALL_CHEST,
         lambda bundle: has_explosives(bundle))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_CRACKED_WALL, world, [
        (Regions.WATER_TEMPLE_EAST_LOWER, lambda bundle: True)
    ])

    # Water Temple Torch Room
    # Locations
    add_locations(Regions.WATER_TEMPLE_TORCH_ROOM, world, [
        (Locations.WATER_TEMPLE_TORCHES_CHEST, lambda bundle: can_kill_enemy(
            bundle, Enemies.SHELL_BLADE, EnemyDistance.CLOSE, True, 3))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_TORCH_ROOM, world, [
        (Regions.WATER_TEMPLE_EAST_LOWER, lambda bundle: can_kill_enemy(
            bundle, Enemies.SHELL_BLADE, EnemyDistance.CLOSE, True, 3))
    ])

    # Water Temple North Lower
    # Connections
    connect_regions(Regions.WATER_TEMPLE_NORTH_LOWER, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.WATER_TEMPLE_BOULDERS_LOWER, lambda bundle: ((can_use(Items.LONGSHOT, bundle) or
                                                               (can_do_trick(Tricks.WATER_BK_REGION, bundle) and
                                                                can_use(Items.HOVER_BOOTS, bundle))) and
                                                              small_keys(Items.WATER_TEMPLE_SMALL_KEY, 4, bundle)))
    ])

    # Water Temple Boulders Lower
    # Connections
    connect_regions(Regions.WATER_TEMPLE_BOULDERS_LOWER, world, [
        (Regions.WATER_TEMPLE_NORTH_LOWER, lambda bundle: small_keys(
            Items.WATER_TEMPLE_SMALL_KEY, 4, bundle)),
        (Regions.WATER_TEMPLE_BLOCK_ROOM, lambda bundle: True),
        (Regions.WATER_TEMPLE_BOULDERS_UPPER, lambda bundle: ((is_adult(bundle) and
                                                               (can_use(Items.HOVER_BOOTS, bundle) or
                                                                can_do_trick(Tricks.WATER_NORTH_BASEMENT_LEDGE_JUMP, bundle))) or
                                                              (can_use(Items.HOVER_BOOTS, bundle) and
                                                               can_use(Items.IRON_BOOTS, bundle)))),
        (Regions.WATER_TEMPLE_NEAR_BOSS_KEY_CHEST_GS,
         lambda bundle: can_use(Items.LONGSHOT, bundle))
    ])

    # Water Temple Block Room
    # Locations
    add_locations(Regions.WATER_TEMPLE_BLOCK_ROOM, world, [
        (Locations.WATER_TEMPLE_BASEMENT_BLOCK_PUZZLE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.WATER_TEMPLE_BASEMENT_BLOCK_PUZZLE_POT2,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_BLOCK_ROOM, world, [
        (Regions.WATER_TEMPLE_BOULDERS_LOWER, lambda bundle: ((has_item(Items.GORONS_BRACELET, bundle) and
                                                               has_explosives(bundle)) or
                                                              can_use(Items.HOOKSHOT, bundle))),
        (Regions.WATER_TEMPLE_JETS_ROOM, lambda bundle: ((has_item(Items.GORONS_BRACELET, bundle) and
                                                          has_explosives(bundle)) or
                                                         (can_use(Items.HOOKSHOT, bundle) and
                                                          can_use(Items.HOVER_BOOTS, bundle))))
    ])

    # Water Temple Jets Room
    # Connections
    connect_regions(Regions.WATER_TEMPLE_JETS_ROOM, world, [
        (Regions.WATER_TEMPLE_BLOCK_ROOM,
         lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.WATER_TEMPLE_BOULDERS_UPPER, lambda bundle: True)
    ])

    # Water Temple Boulders Upper
    # Connections
    connect_regions(Regions.WATER_TEMPLE_BOULDERS_UPPER, world, [
        (Regions.WATER_TEMPLE_BOULDERS_LOWER, lambda bundle: True),
        (Regions.WATER_TEMPLE_JETS_ROOM, lambda bundle: is_adult(bundle)),
        (Regions.WATER_TEMPLE_BOSS_KEY_ROOM, lambda bundle: ((can_use(Items.IRON_BOOTS, bundle) or
                                                              (is_adult(bundle) and
                                                               can_do_trick(Tricks.WATER_BK_JUMP_DIVE, bundle))) and
                                                             small_keys(Items.WATER_TEMPLE_SMALL_KEY, 5, bundle))),
        (Regions.WATER_TEMPLE_NEAR_BOSS_KEY_CHEST_GS, lambda bundle: ((is_adult(bundle) and
                                                                       hookshot_or_boomerang(bundle)) or
                                                                      (can_use(Items.IRON_BOOTS, bundle) and
                                                                       can_use(Items.HOOKSHOT, bundle))))
    ])

    # Water Temple Near Boss Key Chest GS
    # Locations
    add_locations(Regions.WATER_TEMPLE_NEAR_BOSS_KEY_CHEST_GS, world, [
        (Locations.WATER_TEMPLE_GS_NEAR_BOSS_KEY_CHEST, lambda bundle: True)
    ])

    # Water Temple Boss Key Room
    # Events
    add_events(Regions.WATER_TEMPLE_BOSS_KEY_ROOM, world, [
        (EventLocations.WATER_TEMPLE_BOSS_KEY_ROOM_FAIRY_POT,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.WATER_TEMPLE_BOSS_KEY_ROOM, world, [
        (Locations.WATER_TEMPLE_BOSS_KEY_CHEST, lambda bundle: True),
        (Locations.WATER_TEMPLE_BOSS_KEY_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.WATER_TEMPLE_BOSS_KEY_POT2,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_BOSS_KEY_ROOM, world, [
        (Regions.WATER_TEMPLE_BOULDERS_UPPER, lambda bundle: ((can_use(Items.IRON_BOOTS, bundle) or
                                                               (is_adult(bundle) and
                                                                can_do_trick(Tricks.WATER_BK_JUMP_DIVE, bundle)) or
                                                               is_child(bundle) or
                                                               has_item(Items.SILVER_SCALE, bundle)) and
                                                              small_keys(Items.WATER_TEMPLE_SMALL_KEY, 5, bundle)))
    ])

    # Water Temple South Lower
    # Locations
    add_locations(Regions.WATER_TEMPLE_SOUTH_LOWER, world, [
        (Locations.WATER_TEMPLE_GS_BEHIND_GATE, lambda bundle: (can_jump_slash(bundle) and
                                                                (can_use(Items.HOOKSHOT, bundle) or
                                                                 (is_adult(bundle) and
                                                                  can_use(Items.HOVER_BOOTS, bundle))))),
        (Locations.WATER_TEMPLE_BEHIND_GATE_POT1, lambda bundle: (can_jump_slash(bundle) and
                                                                  (can_use(Items.HOOKSHOT, bundle) or
                                                                   (is_adult(bundle) and
                                                                      can_use(Items.HOVER_BOOTS, bundle))))),
        (Locations.WATER_TEMPLE_BEHIND_GATE_POT2, lambda bundle: (can_jump_slash(bundle) and
                                                                  (can_use(Items.HOOKSHOT, bundle) or
                                                                   (is_adult(bundle) and
                                                                      can_use(Items.HOVER_BOOTS, bundle))))),
        (Locations.WATER_TEMPLE_BEHIND_GATE_POT3, lambda bundle: (can_jump_slash(bundle) and
                                                                  (can_use(Items.HOOKSHOT, bundle) or
                                                                   (is_adult(bundle) and
                                                                      can_use(Items.HOVER_BOOTS, bundle))))),
        (Locations.WATER_TEMPLE_BEHIND_GATE_POT4, lambda bundle: (can_jump_slash(bundle) and
                                                                  (can_use(Items.HOOKSHOT, bundle) or
                                                                   (is_adult(bundle) and
                                                                      can_use(Items.HOVER_BOOTS, bundle))))),
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_SOUTH_LOWER, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: can_use(Items.IRON_BOOTS, bundle))
    ])

    # Water Temple West Lower
    # Connections
    connect_regions(Regions.WATER_TEMPLE_WEST_LOWER, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: (can_use(Items.HOOKSHOT, bundle) and
                                                     can_use(Items.IRON_BOOTS, bundle) and
                                                     has_item(Items.GORONS_BRACELET, bundle))),
        (Regions.WATER_TEMPLE_DRAGON_ROOM, lambda bundle: (can_jump_slash_except_hammer(bundle) or
                                                           can_use_projectile(bundle)))
    ])

    # Water Temple Dragon Room
    # Connections
    connect_regions(Regions.WATER_TEMPLE_DRAGON_ROOM, world, [
        (Regions.WATER_TEMPLE_WEST_LOWER, lambda bundle: True),
        (Regions.WATER_TEMPLE_DRAGON_ROOM_CHEST, lambda bundle: ((can_use(Items.HOOKSHOT, bundle) and
                                                                  can_use(Items.IRON_BOOTS, bundle)) or
                                                                 (((is_adult(bundle) and
                                                                    can_do_trick(Tricks.WATER_ADULT_DRAGON, bundle) and
                                                                    (can_use(Items.HOOKSHOT, bundle) or
                                                                  can_use(Items.FAIRY_BOW, bundle) or
                                                                  can_use(Items.BOMBCHUS_5, bundle))) or
                                                                     (is_child(bundle) and
                                                                      can_do_trick(Tricks.WATER_CHILD_DRAGON, bundle) and
                                                                      (can_use(Items.FAIRY_SLINGSHOT, bundle) or
                                                                      can_use(Items.BOOMERANG, bundle) or
                                                                      can_use(Items.BOMBCHUS_5, bundle)))) and
                                                                  (has_item(Items.SILVER_SCALE, bundle) or
                                                                     can_use(Items.IRON_BOOTS, bundle))))),
    ])

    # Water Temple Central Pillar Lower
    # Connections
    connect_regions(Regions.WATER_TEMPLE_CENTRAL_PILLAR_LOWER, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: small_keys(
            Items.WATER_TEMPLE_SMALL_KEY, 5, bundle)),
        (Regions.WATER_TEMPLE_CENTRAL_PILLAR_UPPER,
         lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.WATER_TEMPLE_CENTRAL_PILLAR_BASEMENT, lambda bundle: (has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle) and
                                                                       can_use(Items.IRON_BOOTS, bundle) and
                                                                       water_timer(bundle) >= 40))
    ])

    # Water Temple Central Pillar Upper
    # Events
    add_events(Regions.WATER_TEMPLE_CENTRAL_PILLAR_UPPER, world, [
        (EventLocations.WATER_TEMPLE_CENTRAL_PILLAR_UPPER_WATER_MIDDLE,
         LocalEvents.WATER_LEVEL_MIDDLE, lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Locations
    add_locations(Regions.WATER_TEMPLE_CENTRAL_PILLAR_UPPER, world, [
        (Locations.WATER_TEMPLE_GS_CENTRAL_PILLAR, lambda bundle: (can_use(Items.LONGSHOT, bundle) or
                                                                   (((can_do_trick(Tricks.WATER_FW_CENTRAL_GS, bundle) and
                                                                      can_use(Items.FARORES_WIND, bundle) and
                                                                      (can_use(Items.FAIRY_BOW, bundle) or
                                                                       can_use(Items.DINS_FIRE, bundle) or
                                                                       small_keys(Items.WATER_TEMPLE_SMALL_KEY, 5, bundle))) or
                                                                     (can_do_trick(Tricks.WATER_IRONS_CENTRAL_GS, bundle) and
                                                                      can_use(Items.IRON_BOOTS, bundle) and
                                                                      ((can_use(Items.HOOKSHOT, bundle) and
                                                                        can_use(Items.FAIRY_BOW, bundle)) or
                                                                       (can_use(Items.DINS_FIRE, bundle))))) and
                                                                    has_item(LocalEvents.WATER_LEVEL_HIGH, bundle) and
                                                                    hookshot_or_boomerang(bundle))))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_CENTRAL_PILLAR_UPPER, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.WATER_TEMPLE_CENTRAL_PILLAR_LOWER, lambda bundle: True)
    ])

    # Water Temple Central Pillar Basement
    # Locations
    add_locations(Regions.WATER_TEMPLE_CENTRAL_PILLAR_BASEMENT, world, [
        (Locations.WATER_TEMPLE_CENTRAL_PILLAR_CHEST, lambda bundle: (can_use(Items.HOOKSHOT, bundle) and
                                                                      can_use(Items.IRON_BOOTS, bundle) and
                                                                      water_timer(bundle) >= 40))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_CENTRAL_PILLAR_BASEMENT, world, [
        (Regions.WATER_TEMPLE_CENTRAL_PILLAR_LOWER, lambda bundle: (can_use(Items.IRON_BOOTS, bundle) and
                                                                    water_timer(bundle) >= 16))
    ])

    # Water Temple East Middle
    # Locations
    add_locations(Regions.WATER_TEMPLE_EAST_MIDDLE, world, [
        (Locations.WATER_TEMPLE_COMPASS_CHEST,
         lambda bundle: can_use_projectile(bundle)),
        (Locations.WATER_TEMPLE_NEAR_COMPASS_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.WATER_TEMPLE_NEAR_COMPASS_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.WATER_TEMPLE_NEAR_COMPASS_POT3,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_EAST_MIDDLE, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: can_use(Items.IRON_BOOTS, bundle))
    ])

    # Water Temple West Middle
    # Connections
    connect_regions(Regions.WATER_TEMPLE_WEST_MIDDLE, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.WATER_TEMPLE_HIGH_WATER, lambda bundle: can_use_projectile(bundle))
    ])

    # Water Temple High Water
    # Events
    add_events(Regions.WATER_TEMPLE_HIGH_WATER, world, [
        (EventLocations.WATER_TEMPLE_HIGH_WATER_WATER_HIGH, LocalEvents.WATER_LEVEL_HIGH,
         lambda bundle: can_use(Items.ZELDAS_LULLABY, bundle))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_HIGH_WATER, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: True)
    ])

    # Water Temple Block Corridor
    # Locations
    add_locations(Regions.WATER_TEMPLE_BLOCK_CORRIDOR, world, [
        (Locations.WATER_TEMPLE_CENTRAL_BOW_TARGET_CHEST, lambda bundle: (has_item(Items.GORONS_BRACELET, bundle) and
                                                                          (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                                           has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle)))),
        (Locations.WATER_TEMPLE_CENTRAL_BOW_POT1, lambda bundle: (can_break_pots(bundle) and
                                                                  has_item(Items.GORONS_BRACELET, bundle) and
                                                                  (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                                   has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle)))),
        (Locations.WATER_TEMPLE_CENTRAL_BOW_POT2, lambda bundle: (can_break_pots(bundle) and
                                                                  has_item(Items.GORONS_BRACELET, bundle) and
                                                                  (has_item(LocalEvents.WATER_LEVEL_LOW, bundle) or
                                                                   has_item(LocalEvents.WATER_LEVEL_MIDDLE, bundle))))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_BLOCK_CORRIDOR, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: can_use(Items.HOOKSHOT, bundle))
    ])

    # Water Temple Falling Platform Room
    # Locations
    add_locations(Regions.WATER_TEMPLE_FALLING_PLATFORM_ROOM, world, [
        (Locations.WATER_TEMPLE_GS_FALLING_PLATFORM_ROOM, lambda bundle: (can_use(Items.LONGSHOT, bundle) or
                                                                          (can_do_trick(Tricks.WATER_RANG_FALLING_PLATFORM_GS, bundle) and
                                                                           is_child(bundle) and
                                                                           can_use(Items.BOOMERANG, bundle)) or
                                                                          (can_do_trick(Tricks.WATER_HOOKSHOT_FALLING_PLATFORM_GS, bundle) and
                                                                           is_adult(bundle) and
                                                                           can_use(Items.HOOKSHOT, bundle))))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_FALLING_PLATFORM_ROOM, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: (can_use(Items.HOOKSHOT, bundle) and
                                                     small_keys(Items.WATER_TEMPLE_SMALL_KEY, 4, bundle))),
        (Regions.WATER_TEMPLE_DRAGON_PILLARS_ROOM, lambda bundle: (can_use(Items.HOOKSHOT, bundle) and
                                                                   small_keys(Items.WATER_TEMPLE_SMALL_KEY, 5, bundle))),
    ])

    # Water Temple Dragon Pillars Room
    # Locations
    add_locations(Regions.WATER_TEMPLE_DRAGON_PILLARS_ROOM, world, [
        (Locations.WATER_TEMPLE_LIKE_LIKE_POT1,
         lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Locations.WATER_TEMPLE_LIKE_LIKE_POT2,
         lambda bundle: can_use(Items.HOOKSHOT, bundle))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_DRAGON_PILLARS_ROOM, world, [
        (Regions.WATER_TEMPLE_FALLING_PLATFORM_ROOM,
         lambda bundle: can_use_projectile(bundle)),
        (Regions.WATER_TEMPLE_DARK_LINK_ROOM,
         lambda bundle: can_use(Items.HOOKSHOT, bundle))
    ])

    # Water Temple Dark Link Room
    # Connections
    connect_regions(Regions.WATER_TEMPLE_DARK_LINK_ROOM, world, [
        (Regions.WATER_TEMPLE_DRAGON_PILLARS_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.DARK_LINK)),
        (Regions.WATER_TEMPLE_LONGSHOT_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.DARK_LINK)),
    ])

    # Water Temple Longshot Room
    # Locations
    add_locations(Regions.WATER_TEMPLE_LONGSHOT_ROOM, world, [
        (Locations.WATER_TEMPLE_LONGSHOT_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_LONGSHOT_ROOM, world, [
        (Regions.WATER_TEMPLE_DARK_LINK_ROOM, lambda bundle: True),
        (Regions.WATER_TEMPLE_RIVER, lambda bundle: (is_child(bundle) or
                                                     can_use(Items.SONG_OF_TIME, bundle)))
    ])

    # Water Temple River
    # Locations
    add_locations(Regions.WATER_TEMPLE_RIVER, world, [
        (Locations.WATER_TEMPLE_RIVER_CHEST, lambda bundle: ((can_use(Items.FAIRY_SLINGSHOT, bundle) or
                                                              can_use(Items.FAIRY_BOW, bundle)) and
                                                             (is_adult(bundle) or
                                                              can_use(Items.HOVER_BOOTS, bundle) or
                                                              can_use(Items.HOOKSHOT, bundle)))),
        (Locations.WATER_TEMPLE_GS_RIVER, lambda bundle: ((can_use(Items.IRON_BOOTS, bundle) and
                                                           can_use(Items.HOOKSHOT, bundle)) or
                                                          (can_do_trick(Tricks.WATER_RIVER_GS, bundle) and
                                                           can_use(Items.LONGSHOT, bundle)))),
        (Locations.WATER_TEMPLE_RIVER_POT1, lambda bundle: can_break_pots(bundle)),
        (Locations.WATER_TEMPLE_RIVER_POT2, lambda bundle: can_break_pots(bundle)),
        (Locations.WATER_TEMPLE_RIVER_HEART1, lambda bundle: ((can_use(Items.IRON_BOOTS, bundle) and
                                                               water_timer(bundle) >= 16) or
                                                              has_item(Items.BRONZE_SCALE, bundle))),
        (Locations.WATER_TEMPLE_RIVER_HEART2, lambda bundle: ((can_use(Items.IRON_BOOTS, bundle) and
                                                               water_timer(bundle) >= 16) or
                                                              has_item(Items.BRONZE_SCALE, bundle))),
        (Locations.WATER_TEMPLE_RIVER_HEART3, lambda bundle: ((can_use(Items.IRON_BOOTS, bundle) and
                                                               water_timer(bundle) >= 16) or
                                                              has_item(Items.BRONZE_SCALE, bundle))),
        (Locations.WATER_TEMPLE_RIVER_HEART4, lambda bundle: ((can_use(Items.IRON_BOOTS, bundle) and
                                                               water_timer(bundle) >= 16) or
                                                              has_item(Items.BRONZE_SCALE, bundle)))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_RIVER, world, [
        (Regions.WATER_TEMPLE_DRAGON_ROOM, lambda bundle: ((can_use(Items.FAIRY_SLINGSHOT, bundle) or
                                                            can_use(Items.FAIRY_BOW, bundle)) and
                                                           (is_adult(bundle) or
                                                            can_use(Items.HOVER_BOOTS, bundle) or
                                                            can_use(Items.HOOKSHOT, bundle)))),
        (Regions.WATER_TEMPLE_DRAGON_ROOM_CHEST, lambda bundle: (is_adult(bundle) and
                                                                 can_use(Items.FAIRY_BOW, bundle) and
                                                                 ((can_do_trick(Tricks.WATER_ADULT_DRAGON, bundle) and
                                                                   (has_item(Items.SILVER_SCALE, bundle) or
                                                                    can_use(Items.IRON_BOOTS, bundle))) or
                                                                  can_do_trick(Tricks.WATER_DRAGON_JUMP_DIVE, bundle))))
    ])

    # Water Temple Dragon Chest
    add_locations(Regions.WATER_TEMPLE_DRAGON_ROOM_CHEST, world, [
        (Locations.WATER_TEMPLE_DRAGON_CHEST, lambda bundle: True)
    ])

    # Water Temple Pre Boss Room
    # Events
    add_events(Regions.WATER_TEMPLE_PRE_BOSS_ROOM, world, [
        (EventLocations.WATER_TEMPLE_PRE_BOSS_ROOM_FAIRY_POT,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True)
    ])
    # Locations
    add_locations(Regions.WATER_TEMPLE_PRE_BOSS_ROOM, world, [
        (Locations.WATER_TEMPLE_MAIN_LEVEL1_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.WATER_TEMPLE_MAIN_LEVEL1_POT2,
         lambda bundle: can_break_pots(bundle))
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_PRE_BOSS_ROOM, world, [
        (Regions.WATER_TEMPLE_LOBBY, lambda bundle: True),
        (Regions.WATER_TEMPLE_BOSS_ENTRYWAY, lambda bundle: True)
    ])

    # Water Temple Boss Entryway
    # Connections
    connect_regions(Regions.WATER_TEMPLE_BOSS_ENTRYWAY, world, [
        (Regions.WATER_TEMPLE_PRE_BOSS_ROOM, lambda bundle: False),
        (Regions.WATER_TEMPLE_BOSS_ROOM, lambda bundle: has_item(
            Items.WATER_TEMPLE_BOSS_KEY, bundle))
    ])

    # Water Temple Boss Room
    # Events
    add_events(Regions.WATER_TEMPLE_BOSS_ROOM, world, [
        (EventLocations.WATER_TEMPLE_MORPHA, Events.WATER_TEMPLE_COMPLETED,
         lambda bundle: can_kill_enemy(bundle, Enemies.MORPHA))
    ])
    # Locations
    add_locations(Regions.WATER_TEMPLE_BOSS_ROOM, world, [
        (Locations.WATER_TEMPLE_MORPHA_HEART_CONTAINER,
         lambda bundle: has_item(Events.WATER_TEMPLE_COMPLETED, bundle)),
        (Locations.MORPHA, lambda bundle: has_item(
            Events.WATER_TEMPLE_COMPLETED, bundle)),
    ])
    # Connections
    connect_regions(Regions.WATER_TEMPLE_BOSS_ROOM, world, [
        (Regions.WATER_TEMPLE_BOSS_ENTRYWAY, lambda bundle: False),
        (Regions.LAKE_HYLIA, lambda bundle: has_item(
            Events.WATER_TEMPLE_COMPLETED, bundle))
    ])
