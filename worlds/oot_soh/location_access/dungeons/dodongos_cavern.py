from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    DODONGOS_CAVERN_GOSSIP_STONE_SONG_FAIRY = "Dodongos Cavern Gossip Stone Song Fairy"
    DODONGOS_CAVERN_LOBBY_SWITCH = "Dodongos Cavern Lobby Switch"
    DODONGOS_CAVERN_LOWER_LIZALFOS_FIGHT = "Dodongos Cavern Lower Lizalfos Fight"
    DODONGOS_CAVERN_LIFT_SWITCH = "Dodongos Cavern Lift Switch"
    DODONGOS_CAVERN_EYES = "Dodongos Cavern Eyes"
    DODONGOS_CAVERN_FAIRY_POT = "Dodongos Cavern Fairy Pot"
    DODONGOS_CAVERN_KING_DODONGO = "Dodongos Cavern King Dodongo"


class LocalEvents(StrEnum):
    DODONGOS_CAVERN_STAIRS_ROOM_DOOR = "Dodongos Cavern Stairs Room Door"
    DODONGOS_CAVERN_LIFT_PLATFORM = "Dodongos Cavern Lift Platform"
    DODONGOS_CAVERN_EYES_LIT = "Dodongos Cavern Eyes Lit"
    DODONGOS_CAVERN_LOWER_LIZALFOS_DEFEATED = "Dodongos Cavern Lower Lizalfos Defeated"


def set_region_rules(world: "SohWorld") -> None:
    # Dodongos Cavern Entryway
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_ENTRYWAY, world, [
        (Regions.DODONGOS_CAVERN_BEGINNING, lambda bundle: True),
        (Regions.DEATH_MOUNTAIN_TRAIL, lambda bundle: True),
    ])

    # Dodongos Cavern Beginning
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BEGINNING, world, [
        (Regions.DODONGOS_CAVERN_ENTRYWAY, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_LOBBY,
         lambda bundle: blast_or_smash(bundle) or has_item(Items.GORONS_BRACELET, bundle))
    ])

    # Dodongos Cavern Lobby
    # Events
    add_events(Regions.DODONGOS_CAVERN_LOBBY, world, [
        (EventLocations.DODONGOS_CAVERN_GOSSIP_STONE_SONG_FAIRY, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: (can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle)) and call_gossip_fairy(
             bundle)),
    ])
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_LOBBY, world, [
        (Locations.DODONGOS_CAVERN_MAP_CHEST,
         lambda bundle: can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Locations.DODONGOS_CAVERN_DEKU_SCRUB_LOBBY,
         lambda bundle: can_stun_deku(bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Locations.DODONGOS_CAVERN_GOSSIP_STONE_FAIRY,
         lambda bundle: (can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle)) and call_gossip_fairy(
             bundle)),
        (Locations.DODONGOS_CAVERN_GOSSIP_STONE_BIG_FAIRY,
         lambda bundle: (can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle)) and can_use(
             Items.SONG_OF_STORMS, bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_LOBBY, world, [
        (Regions.DODONGOS_CAVERN_BEGINNING, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_LOBBY_SWITCH,
         lambda bundle: is_adult(bundle) or can_ground_jump(bundle)),
        (Regions.DODONGOS_CAVERN_SE_CORRIDOR,
         lambda bundle: can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Regions.DODONGOS_CAVERN_STAIRS_LOWER,
         lambda bundle: has_item(LocalEvents.DODONGOS_CAVERN_STAIRS_ROOM_DOOR, bundle)),
        (Regions.DODONGOS_CAVERN_FAR_BRIDGE,
         lambda bundle: has_item(LocalEvents.DODONGOS_CAVERN_LIFT_PLATFORM, bundle)),
        (Regions.DODONGOS_CAVERN_BOSS_REGION, lambda bundle: has_item(
            LocalEvents.DODONGOS_CAVERN_EYES_LIT, bundle)),
        (Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY, lambda bundle: False),
    ])

    # Dodongos Cavern Lobby Switch
    # Events
    add_events(Regions.DODONGOS_CAVERN_LOBBY_SWITCH, world, [
        (EventLocations.DODONGOS_CAVERN_LOBBY_SWITCH,
         LocalEvents.DODONGOS_CAVERN_STAIRS_ROOM_DOOR, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_LOBBY_SWITCH, world, [
        (Regions.DODONGOS_CAVERN_LOBBY, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_DODONGO_ROOM, lambda bundle: True),
    ])

    # Dodongos Cavern SE Corridor
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_SE_CORRIDOR, world, [
        (Locations.DODONGOS_CAVERN_GS_SCARECROW,
         lambda bundle: can_use(Items.SCARECROW, bundle) or (is_adult(bundle) and can_use(Items.LONGSHOT, bundle)) or (
             can_do_trick(Tricks.DC_SCARECROW_GS, bundle) and can_attack(bundle))),
        (Locations.DODONGOS_CAVERN_SIDE_ROOM_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_SIDE_ROOM_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_SIDE_ROOM_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_SIDE_ROOM_POT4,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_SIDE_ROOM_POT5,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_SIDE_ROOM_POT6,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_SE_CORRIDOR, world, [
        (Regions.DODONGOS_CAVERN_LOBBY, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_SE_ROOM, lambda bundle: can_break_mud_walls(bundle) or can_attack(bundle) or (
            take_damage(bundle) and can_shield(bundle))),
        (Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS, lambda bundle: True),
    ])

    # Dodongos Cavern SE Room
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_SE_ROOM, world, [
        (Locations.DODONGOS_CAVERN_GS_SIDE_ROOM_NEAR_LOWER_LIZALFOS,
         lambda bundle: can_attack(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_SE_ROOM, world, [
        (Regions.DODONGOS_CAVERN_SE_CORRIDOR, lambda bundle: True),
    ])

    # Dodongos Cavern Near Lower Lizalfos
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS, world, [
        (Regions.DODONGOS_CAVERN_SE_CORRIDOR, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, lambda bundle: True),
    ])

    # Dodongos Cavern Lower Lizalfos
    # Events
    add_events(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, world, [
        (EventLocations.DODONGOS_CAVERN_LOWER_LIZALFOS_FIGHT, LocalEvents.DODONGOS_CAVERN_LOWER_LIZALFOS_DEFEATED,
         lambda bundle: can_kill_enemy(bundle, Enemies.LIZALFOS, EnemyDistance.CLOSE, quantity=2))
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, world, [
        (Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS,
         lambda bundle: has_item(LocalEvents.DODONGOS_CAVERN_LOWER_LIZALFOS_DEFEATED, bundle)),
        (Regions.DODONGOS_CAVERN_DODONGO_ROOM,
         lambda bundle: has_item(LocalEvents.DODONGOS_CAVERN_LOWER_LIZALFOS_DEFEATED, bundle)),
        (Regions.DODONGOS_CAVERN_LOWER_LIZALFOS_LOCATIONS, lambda bundle: True),
    ])

    # Dodongos Cavern Lower Lizalfos Locations
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS_LOCATIONS, world, [
        (Locations.DODONGOS_CAVERN_LIZALFOS_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_LIZALFOS_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_LIZALFOS_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_LIZALFOS_POT4,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_LOWER_LIZALFOS_ROOM_LAVAFALL_HEART, lambda bundle: True),
    ])

    # Dodongos Cavern Dodongo Room
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_DODONGO_ROOM, world, [
        (Locations.DODONGOS_CAVERN_TORCH_ROOM_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_TORCH_ROOM_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_TORCH_ROOM_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_TORCH_ROOM_POT4,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_DODONGO_ROOM, world, [
        (Regions.DODONGOS_CAVERN_LOBBY_SWITCH,
         lambda bundle: has_fire_source_with_torch(bundle)),
        (Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM,
         lambda bundle: can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle)),
    ])

    # Dodongos Cavern Near Dodongo Room
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM, world, [
        (Locations.DODONGOS_CAVERN_DEKU_SCRUB_SIDE_ROOM_NEAR_DODONGOS,
         lambda bundle: can_stun_deku(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM, world, [
        (Regions.DODONGOS_CAVERN_DODONGO_ROOM, lambda bundle: True),
    ])

    # Dodongos Cavern Stairs Lower
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_STAIRS_LOWER, world, [
        (Regions.DODONGOS_CAVERN_LOBBY, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_STAIRS_UPPER,
         lambda bundle: has_explosives(bundle) or has_item(Items.GORONS_BRACELET, bundle) or can_use(Items.DINS_FIRE,
                                                                                                     bundle) or (
             can_do_trick(Tricks.DC_STAIRS_WITH_BOW, bundle) and can_use(Items.FAIRY_BOW,
                                                                         bundle))),
        (Regions.DODONGOS_CAVERN_COMPASS_ROOM,
         lambda bundle: can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Regions.DODONGOS_CAVERN_VINES_ABOVE_STAIRS_GS,
         lambda bundle: can_do_trick(Tricks.DC_VINES_GS, bundle) and can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA,
                                                                                        EnemyDistance.LONGSHOT)),
    ])

    # Dodongos Cavern Stairs Upper
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_STAIRS_UPPER, world, [
        (Locations.DODONGOS_CAVERN_GS_ALCOVE_ABOVE_STAIRS,
         lambda bundle: can_get_enemy_drop(bundle, Enemies.GOLD_SKULLTULA, EnemyDistance.LONGSHOT) or (
             has_item(LocalEvents.DODONGOS_CAVERN_LIFT_PLATFORM, bundle) and can_get_enemy_drop(bundle,
                                                                                                Enemies.GOLD_SKULLTULA,
                                                                                                EnemyDistance.BOOMERANG))),
        (Locations.DODONGOS_CAVERN_STAIRCASE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_STAIRCASE_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_STAIRCASE_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_STAIRCASE_POT4,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_STAIRS_UPPER, world, [
        (Regions.DODONGOS_CAVERN_STAIRS_LOWER, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_ARMOS_ROOM, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_VINES_ABOVE_STAIRS_GS,
         lambda bundle: is_adult(bundle) or can_attack(bundle)),
    ])

    # Dodongos Cavern Vines Above Stairs
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_VINES_ABOVE_STAIRS_GS, world, [
        (Locations.DODONGOS_CAVERN_GS_VINES_ABOVE_STAIRS, lambda bundle: True),
    ])

    # Dodongos Cavern Compass Room
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_COMPASS_ROOM, world, [
        (Locations.DODONGOS_CAVERN_COMPASS_CHEST, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_COMPASS_ROOM, world, [
        (Regions.DODONGOS_CAVERN_STAIRS_LOWER,
         lambda bundle: can_use_any(
             [Items.MASTER_SWORD, Items.BIGGORONS_SWORD,
                 Items.MEGATON_HAMMER, Items.GORONS_BRACELET],
             bundle) or has_explosives(bundle)),
    ])

    # Dodongos Cavern Armos Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_ARMOS_ROOM, world, [
        (Regions.DODONGOS_CAVERN_STAIRS_UPPER, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, lambda bundle: True),
    ])

    # Dodongos Cavern Bomb Room Lower
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, world, [
        (Locations.DODONGOS_CAVERN_BOMB_FLOWER_PLATFORM_CHEST, lambda bundle: True),
        (Locations.DODONGOS_CAVERN_BLADE_ROOM_HEART, lambda bundle: True),
        (Locations.DODONGOS_CAVERN_FIRST_BRIDGE_GRASS,
         lambda bundle: can_cut_shrubs(bundle)),
        (Locations.DODONGOS_CAVERN_BLADE_ROOM_GRASS,
         lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, world, [
        (Regions.DODONGOS_CAVERN_ARMOS_ROOM, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_2F_SIDE_ROOM, lambda bundle: can_break_mud_walls(bundle) or (
            can_do_trick(Tricks.DC_SCRUB_ROOM, bundle) and has_item(Items.GORONS_BRACELET, bundle))),
        (Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM,
         lambda bundle: can_break_mud_walls(bundle) or has_item(Items.GORONS_BRACELET, bundle)),
        (Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER,
         lambda bundle: (is_adult(bundle) and (
             can_do_trick(Tricks.DC_JUMP, bundle) or can_ground_jump(bundle))) or can_use(Items.HOVER_BOOTS,
                                                                                          bundle) or (
             can_use(Items.LONGSHOT, bundle)) or (
             can_do_trick(Tricks.DAMAGE_BOOST_SIMPLE, bundle) and has_explosives(
                 bundle) and can_jump_slash(bundle))),
    ])

    # Dodongos Cavern 2F Side Room
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_2F_SIDE_ROOM, world, [
        (Locations.DODONGOS_CAVERN_DEKU_SCRUB_NEAR_BOMB_BAG_LEFT,
         lambda bundle: can_stun_deku(bundle)),
        (Locations.DODONGOS_CAVERN_DEKU_SCRUB_NEAR_BOMB_BAG_RIGHT,
         lambda bundle: can_stun_deku(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_2F_SIDE_ROOM, world, [
        (Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, lambda bundle: True)
    ])

    # Dodongos Cavern First Slingshot Room
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM, world, [
        (Locations.DODONGOS_CAVERN_SINGLE_EYE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_SINGLE_EYE_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_SINGLE_EYE_GRASS,
         lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM, world, [
        (Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_UPPER_LIZALFOS,
         lambda bundle: can_use(Items.FAIRY_SLINGSHOT, bundle) or can_use(Items.FAIRY_BOW, bundle) or can_do_trick(
             Tricks.DC_SLINGSHOT_SKIP, bundle) or (is_adult(bundle) and can_ground_jump(bundle))),
    ])

    # Dodongos Cavern Upper Lizalfos
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS, world, [
        (Locations.DODONGOS_CAVERN_UPPER_LIZALFOS_ROOM_LEFT_HEART, lambda bundle: True),
        (Locations.DODONGOS_CAVERN_UPPER_LIZALFOS_ROOM_RIGHT_HEART, lambda bundle: True),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS, world, [
        (Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.LIZALFOS, EnemyDistance.CLOSE, quantity=2)),
        (Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.LIZALFOS, EnemyDistance.CLOSE, quantity=2)),
        (Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS,
         lambda bundle: has_item(LocalEvents.DODONGOS_CAVERN_LOWER_LIZALFOS_DEFEATED, bundle)),
        (Regions.DODONGOS_CAVERN_DODONGO_ROOM,
         lambda bundle: has_item(LocalEvents.DODONGOS_CAVERN_LOWER_LIZALFOS_DEFEATED, bundle)),
        (Regions.DODONGOS_CAVERN_LOWER_LIZALFOS_LOCATIONS, lambda bundle: True),
    ])

    # Dodongos Cavern Second Slingshot Room
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM, world, [
        (Locations.DODONGOS_CAVERN_DOUBLE_EYE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_DOUBLE_EYE_POT2,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM, world, [
        (Regions.DODONGOS_CAVERN_UPPER_LIZALFOS, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER,
         lambda bundle: can_use_any([Items.FAIRY_SLINGSHOT, Items.FAIRY_BOW], bundle) or can_do_trick(
             Tricks.DC_SLINGSHOT_SKIP, bundle)),
    ])

    # Dodongos Cavern Bomb Room Upper
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER, world, [
        (Locations.DODONGOS_CAVERN_BOMB_BAG_CHEST, lambda bundle: True),
        (Locations.DODONGOS_CAVERN_BLADE_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_BLADE_POT2,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER, world, [
        (Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_FAR_BRIDGE, lambda bundle: True),
    ])

    # Dodongos Cavern Far Bridge
    # Events
    add_events(Regions.DODONGOS_CAVERN_FAR_BRIDGE, world, [
        (EventLocations.DODONGOS_CAVERN_EYES, LocalEvents.DODONGOS_CAVERN_EYES_LIT,
         lambda bundle: has_explosives(bundle)),
        (EventLocations.DODONGOS_CAVERN_LIFT_SWITCH,
         LocalEvents.DODONGOS_CAVERN_LIFT_PLATFORM, lambda bundle: True),
    ])
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_FAR_BRIDGE, world, [
        (Locations.DODONGOS_CAVERN_END_OF_BRIDGE_CHEST,
         lambda bundle: can_break_mud_walls(bundle))
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_FAR_BRIDGE, world, [
        (Regions.DODONGOS_CAVERN_LOBBY, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER, lambda bundle: True),
    ])

    # Dodongos Cavern Boss Region
    # Events
    add_events(Regions.DODONGOS_CAVERN_BOSS_REGION, world, [
        (EventLocations.DODONGOS_CAVERN_FAIRY_POT,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True),
    ])
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BOSS_REGION, world, [
        (Locations.DODONGOS_CAVERN_BEFORE_BOSS_GRASS,
         lambda bundle: can_cut_shrubs(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOSS_REGION, world, [
        (Regions.DODONGOS_CAVERN_LOBBY, lambda bundle: True),
        (Regions.DODONGOS_CAVERN_BACK_ROOM,
         lambda bundle: can_break_mud_walls(bundle)),
        (Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY, lambda bundle: True),
    ])

    # Dodongos Cavern Back Room
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BACK_ROOM, world, [
        (Locations.DODONGOS_CAVERN_GS_BACK_ROOM, lambda bundle: can_attack(bundle)),
        (Locations.DODONGOS_CAVERN_BACK_ROOM_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_BACK_ROOM_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_BACK_ROOM_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.DODONGOS_CAVERN_BACK_ROOM_POT4,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BACK_ROOM, world, [
        (Regions.DODONGOS_CAVERN_BOSS_REGION, lambda bundle: True),
    ])

    # Dodongos Cavern Boss Entryway
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY, world, [
        (Regions.DODONGOS_CAVERN_BOSS_ROOM, lambda bundle: True),
    ])

    # Dodongos Cavern Boss Exit
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOSS_EXIT, world, [
        (Regions.DODONGOS_CAVERN_BOSS_REGION, lambda bundle: True),
    ])

    # Dodongos Cavern Boss Room
    # Events
    add_events(Regions.DODONGOS_CAVERN_BOSS_ROOM, world, [
        (EventLocations.DODONGOS_CAVERN_KING_DODONGO, Events.DODONGOS_CAVERN_COMPLETED,
         lambda bundle: (has_explosives(bundle) or (can_use(Items.MEGATON_HAMMER, bundle) or (can_do_trick(Tricks.BLUE_FIRE_MUD_WALLS, bundle) and blue_fire(bundle)) if can_do_trick(Tricks.DC_HAMMER_FLOOR, bundle) else can_do_trick(Tricks.BLUE_FIRE_MUD_WALLS, bundle) and can_use(Items.BOTTLE_WITH_BLUE_FIRE, bundle))) and can_kill_enemy(bundle, Enemies.KING_DODONGO))
    ])
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BOSS_ROOM, world, [
        (Locations.DODONGOS_CAVERN_BOSS_ROOM_CHEST, lambda bundle: True),
        (Locations.DODONGOS_CAVERN_KING_DODONGO_HEART_CONTAINER,
         lambda bundle: has_item(Events.DODONGOS_CAVERN_COMPLETED, bundle)),
        (Locations.KING_DODONGO, lambda bundle: has_item(
            Events.DODONGOS_CAVERN_COMPLETED, bundle)),
    ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOSS_ROOM, world, [
        (Regions.DODONGOS_CAVERN_BOSS_EXIT, lambda bundle: True),
        (Regions.DEATH_MOUNTAIN_TRAIL, lambda bundle: has_item(
            Events.DODONGOS_CAVERN_COMPLETED, bundle)),
    ])
