from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld

#TODO: Events
class EventLocations(str, Enum):
    DODONGOS_CAVERN_LOBBY_SWITCH = "Dodongos Cavern Lobby Switch",
    DODONGOS_CAVERN_LOWER_LIZALFOS = "Dodongos Cavern Lower Lizalfos Defeated"


class LocalEvents(str, Enum):
    DODONGOS_CAVERN_LOBBY_SWITCH_ACTIVATED = "Dodongos Cavern Lobby Switch Activated",
    DODONGOS_CAVERN_LOWER_LIZALFOS_DEFEATED = "Dodongos Cavern Lower Lizalfos Defeated"

def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    ## Dodongos Cavern Beginning
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BEGINNING, world, [
        [Regions.DODONGOS_CAVERN_LOBBY, lambda state: blast_or_smash(state, world) or has_item(Items.STRENGTH_UPGRADE, state, world)]
    ])

    ## Dodongos Cavern Lobby
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_LOBBY, world, [
        [Regions.DODONGOS_CAVERN_BEGINNING, lambda state: True],
        [Regions.DODONGOS_CAVERN_LOBBY_SWITCH, lambda state: is_adult(state, world)], # I don't think this is right.
        [Regions.DODONGOS_CAVERN_SE_CORRIDOR, lambda state: can_break_mud_walls(state, world) or has_item(Items.STRENGTH_UPGRADE, state, world)],
        [Regions.DODONGOS_CAVERN_STAIRS_LOWER, lambda state: True], # TODO: Add lobby switch event requirement
        [Regions.DODONGOS_CAVERN_BOSS_REGION, lambda state: True], # Simplified for early access
        [Regions.DODONGOS_CAVERN_FAR_BRIDGE, lambda state: True]
    ])

    # Events
    #TODO
    #  areaTable[RR_DODONGOS_CAVERN_LOBBY] = Region("Dodongos Cavern Lobby", SCENE_DODONGOS_CAVERN, {
    #         //Events
    #         EventAccess(&logic->GossipStoneFairy, []{return (Here(RR_DODONGOS_CAVERN_LOBBY, []{return logic->CanBreakMudWalls();}) || logic->HasItem(RG_GORONS_BRACELET)) && logic->CallGossipFairy();}),
    #     },

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_LOBBY, world, [
        [Locations.DODONGOS_CAVERN_MAP_CHEST, lambda state: can_break_mud_walls(state, world) or has_item(Items.GORONS_BRACELET, state, world)],
        [Locations.DODONGOS_CAVERN_DEKU_SCRUB_LOBBY, lambda state: can_stun_deku(state, world) or has_item(Items.GORONS_BRACELET, state, world)],
        [Locations.DODONGOS_CAVERN_GOSSIP_STONE_FAIRY, lambda state: (can_break_mud_walls(state, world) or has_item(Items.GORONS_BRACELET, state, world)) and call_gossip_fairy(state, world)],
        [Locations.DODONGOS_CAVERN_GOSSIP_STONE_BIG_FAIRY, lambda state: (can_break_mud_walls(state, world) or has_item(Items.GORONS_BRACELET, state, world)) and can_use(Items.SONG_OF_STORMS, state, world)],
        [Locations.DODONGOS_CAVERN_GOSSIP_STONE, lambda state: can_break_mud_walls(state, world) or has_item(Items.GORONS_BRACELET, state, world)]
    ])


    ## Dodongos Cavern Lobby Switch
    # # Events
    # add_events(Regions.DODONGOS_CAVERN_LOBBY_SWITCH, world, [
    #     [EventLocations.DODONGOS_CAVERN_LOBBY_SWITCH, LocalEvents.DODONGOS_CAVERN_LOBBY_SWITCH_ACTIVATED, lambda state: True]
    # ])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_LOBBY_SWITCH, world, [
        [Regions.DODONGOS_CAVERN_LOBBY, lambda state: True],
        [Regions.DODONGOS_CAVERN_DODONGO_ROOM, lambda state: True]
    ])

    ## Dodongos Cavern SE Corridor
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_SE_CORRIDOR, world, [
        [Regions.DODONGOS_CAVERN_LOBBY, lambda state: True],
        [Regions.DODONGOS_CAVERN_SE_ROOM, lambda state: can_break_mud_walls(state, world) or can_attack(state, world) or (take_damage(state, world) and can_shield(state, world))]
    ])

    ## Dodongos Cavern SE Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_SE_ROOM, world, [
        [Regions.DODONGOS_CAVERN_SE_CORRIDOR, lambda state: True]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_SE_ROOM, world, [
        [Locations.DODONGOS_CAVERN_GS_SIDE_ROOM_NEAR_LOWER_LIZALFOS, lambda state: can_attack(state, world)]
    ])

    ## Dodongos Cavern Near Lower Lizalfos
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS, world, [
        [Regions.DODONGOS_CAVERN_SE_CORRIDOR, lambda state: True],
        [Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, lambda state: True]
    ])

    ## Dodongos Cavern Lower Lizalfos
    # Events
    #add_events(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, world, [
    #    [EventLocations.DODONGOS_CAVERN_LOWER_LIZALFOS, LocalEvents.DODONGOS_CAVERN_LOWER_LIZALFOS_DEFEATED, lambda state: can_kill_enemy(state, world, Enemies.LIZALFOS, EnemyDistance.CLOSE, quantity=2)]
    #])
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, world, [
        [Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS, lambda state: can_kill_enemy(state, world, Enemies.LIZALFOS, EnemyDistance.CLOSE, quantity=2)],
        [Regions.DODONGOS_CAVERN_DODONGO_ROOM, lambda state: can_kill_enemy(state, world, Enemies.LIZALFOS, EnemyDistance.CLOSE, quantity=2)],
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, world, [
        [Locations.DODONGOS_CAVERN_LIZALFOS_POT1, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_LIZALFOS_POT2, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_LIZALFOS_POT3, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_LIZALFOS_POT4, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_LOWER_LIZALFOS_ROOM_LAVAFALL_HEART, lambda state: True],
        ])

    ## Dodongos Cavern Dodongo Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_DODONGO_ROOM, world, [
        [Regions.DODONGOS_CAVERN_LOBBY_SWITCH, lambda state: has_fire_source_with_torch(state, world)],
        [Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, lambda state: True],
        [Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM, lambda state: can_break_mud_walls(state, world) or has_item(Items.GORONS_BRACELET, state, world)]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_DODONGO_ROOM, world, [
        [Locations.DODONGOS_CAVERN_TORCH_ROOM_POT1, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_TORCH_ROOM_POT2, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_TORCH_ROOM_POT3, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_TORCH_ROOM_POT4, lambda state: can_break_pots(state, world)],
        ])

    ## Dodongos Cavern Near Dodongo Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM, world, [
        [Regions.DODONGOS_CAVERN_DODONGO_ROOM, lambda state: True]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM, world, [
        [Locations.DODONGOS_CAVERN_DEKU_SCRUB_SIDE_ROOM_NEAR_DODONGOS, lambda state: can_stun_deku(state, world)]
    ])


    ## Dodongos Cavern Stairs Lower
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_STAIRS_LOWER, world, [
        [Regions.DODONGOS_CAVERN_LOBBY, lambda state: True],
        [Regions.DODONGOS_CAVERN_STAIRS_UPPER, lambda state: has_explosives(state, world) or has_item(Items.GORONS_BRACELET, state, world) or can_use(Items.DINS_FIRE, state, world) or (can_do_trick("DC Stairs With Bow", state, world) and can_use(Items.FAIRY_BOW, state, world))],
        [Regions.DODONGOS_CAVERN_COMPASS_ROOM, lambda state: can_break_mud_walls(state, world) or has_item(Items.GORONS_BRACELET, state, world)]
    ])


    ## Dodongos Cavern Stairs Upper
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_STAIRS_UPPER, world, [
        [Regions.DODONGOS_CAVERN_STAIRS_LOWER, lambda state: True],
        [Regions.DODONGOS_CAVERN_ARMOS_ROOM, lambda state: True]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_STAIRS_UPPER, world, [
        [Locations.DODONGOS_CAVERN_GS_ALCOVE_ABOVE_STAIRS, lambda state: hookshot_or_boomerang(state, world) or can_use(Items.LONGSHOT, state, world)],
        [Locations.DODONGOS_CAVERN_GS_VINES_ABOVE_STAIRS, lambda state: is_adult(state, world) or can_attack(state, world) or  hookshot_or_boomerang(state, world)], #c++; HasAccessTo(RR_DODONGOS_CAVERN_STAIRS_LOWER) what do we do here?
        [Locations.DODONGOS_CAVERN_STAIRCASE_POT1, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_STAIRCASE_POT2, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_STAIRCASE_POT3, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_STAIRCASE_POT4, lambda state: can_break_pots(state, world)],
    ])

    ## Dodongos Cavern Compass Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_COMPASS_ROOM, world, [
        [Regions.DODONGOS_CAVERN_STAIRS_LOWER, lambda state: can_use(Items.MASTER_SWORD, state, world) or can_use(Items.BIGGORONS_SWORD, state, world) or can_use(Items.MEGATON_HAMMER, state, world) or has_explosives(state, world) or has_item(Items.GORONS_BRACELET, state, world)]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_COMPASS_ROOM, world, [
        [Locations.DODONGOS_CAVERN_COMPASS_CHEST, lambda state: True]
    ])

    ## Dodongos Cavern Armos Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_ARMOS_ROOM, world, [
        [Regions.DODONGOS_CAVERN_STAIRS_UPPER, lambda state: True],
        [Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, lambda state: True]
    ])

    ## Dodongos Cavern Bomb Room Lower
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, world, [
        [Regions.DODONGOS_CAVERN_ARMOS_ROOM, lambda state: True],
        [Regions.DODONGOS_CAVERN_2F_SIDE_ROOM, lambda state: can_break_mud_walls(state, world) or (can_do_trick("DC Scrub Room", state, world) and has_item(Items.GORONS_BRACELET, state, world))],
        [Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM, lambda state: can_break_mud_walls(state, world) or has_item(Items.GORONS_BRACELET, state, world)],
        [Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER, lambda state: (is_adult(state, world) and can_do_trick("DC Jump", state, world)) or can_use(Items.HOVER_BOOTS, state, world) or (is_adult(state, world) and can_use(Items.LONGSHOT, state, world)) or (can_do_trick("Damage Boost Simple", state, world) and has_explosives(state, world) and can_jump_slash(state, world))]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, world, [
        [Locations.DODONGOS_CAVERN_BOMB_FLOWER_PLATFORM_CHEST, lambda state: True],
        [Locations.DODONGOS_CAVERN_BLADE_ROOM_HEART, lambda state: True],
        [Locations.DODONGOS_CAVERN_FIRST_BRIDGE_GRASS, lambda state: can_cut_shrubs(state, world)],
        [Locations.DODONGOS_CAVERN_BLADE_ROOM_GRASS, lambda state: can_cut_shrubs(state, world)], # RC_DODONGOS_CAVERN_BLADE_GRASS == DODONGOS_CAVERN_BLADE_ROOM_GRASS  ??

    ])

    ## Dodongos Cavern 2F Side Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_2F_SIDE_ROOM, world, [
        [Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, lambda state: True]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_2F_SIDE_ROOM, world, [
        [Locations.DODONGOS_CAVERN_DEKU_SCRUB_NEAR_BOMB_BAG_LEFT, lambda state: can_stun_deku(state, world)],
        [Locations.DODONGOS_CAVERN_DEKU_SCRUB_NEAR_BOMB_BAG_RIGHT, lambda state: can_stun_deku(state, world)]
    ])

    ## Dodongos Cavern First Slingshot Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM, world, [
        [Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, lambda state: True],
        [Regions.DODONGOS_CAVERN_UPPER_LIZALFOS, lambda state: can_use(Items.FAIRY_SLINGSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world) or can_do_trick("DC Slingshot Skip", state, world)]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM, world, [
        [Locations.DODONGOS_CAVERN_SINGLE_EYE_POT1, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_SINGLE_EYE_POT2, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_SINGLE_EYE_GRASS, lambda state: can_cut_shrubs(state, world)]
    ])

    ## Dodongos Cavern Upper Lizalfos
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS, world, [
        [Regions.DODONGOS_CAVERN_LOWER_LIZALFOS, lambda state: True],
        [Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM, lambda state: can_kill_enemy(state, world, Enemies.LIZALFOS, EnemyDistance.CLOSE, quantity=2)],
        [Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM, lambda state: can_kill_enemy(state, world, Enemies.LIZALFOS, EnemyDistance.CLOSE, quantity=2)]
    ])
    # Locations
    add_locations(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS, world, [
        #[Locations.DODONGOS_CAVERN_UPPER_LIZALFOS_ROOM_HEART, lambda state: True], # TODO: This doesn't exist? # C++ name: RC_DODONGOS_CAVERN_LOWER_LIZALFOS_HEART
        [Locations.DODONGOS_CAVERN_UPPER_LIZALFOS_ROOM_LEFT_HEART, lambda state: True],
        [Locations.DODONGOS_CAVERN_UPPER_LIZALFOS_ROOM_RIGHT_HEART, lambda state: True],
    ])

    ## Dodongos Cavern Second Slingshot Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM, world, [
        [Regions.DODONGOS_CAVERN_UPPER_LIZALFOS, lambda state: True],
        [Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER, lambda state: can_use(Items.FAIRY_SLINGSHOT, state, world) or can_use(Items.FAIRY_BOW, state, world) or can_do_trick("DC Slingshot Skip", state, world)]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM, world, [
        [Locations.DODONGOS_CAVERN_DOUBLE_EYE_POT1, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_DOUBLE_EYE_POT2, lambda state: can_break_pots(state, world)]
    ])

    ## Dodongos Cavern Bomb Room Upper
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER, world, [
        [Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER, lambda state: True],
        [Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM, lambda state: True],
        [Regions.DODONGOS_CAVERN_FAR_BRIDGE, lambda state: True]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER, world, [
        [Locations.DODONGOS_CAVERN_BOMB_BAG_CHEST, lambda state: True],
        [Locations.DODONGOS_CAVERN_BLADE_POT1, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_BLADE_POT2, lambda state: can_break_pots(state, world)]
    ])

    ## Dodongos Cavern Far Bridge
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_FAR_BRIDGE, world, [
        [Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER, lambda state: True],
        [Regions.DODONGOS_CAVERN_LOBBY, lambda state: True]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_FAR_BRIDGE, world, [
        [Locations.DODONGOS_CAVERN_END_OF_BRIDGE_CHEST, lambda state: can_break_mud_walls(state, world)]
    ])

    ## Dodongos Cavern Boss Region
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOSS_REGION, world, [
        [Regions.DODONGOS_CAVERN_LOBBY, lambda state: True],
        [Regions.DODONGOS_CAVERN_BACK_ROOM, lambda state: can_break_mud_walls(state, world)],
        [Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY, lambda state: True]
    ])

    # EVENTS
    # TODO: EventAccess(&logic->FairyPot, []{return true;}),

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BOSS_REGION, world, [
        [Locations.DODONGOS_CAVERN_BEFORE_BOSS_GRASS, lambda state: can_cut_shrubs(state, world)]
    ])

    ## Dodongos Cavern Boss Entryway
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY, world, [
        [Regions.DODONGOS_CAVERN_BOSS_REGION, lambda state: True],
        [Regions.DODONGOS_CAVERN_BOSS_ROOM, lambda state: True]
    ])

    ## Dodongos Cavern Boss Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BOSS_ROOM, world, [
        [Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY, lambda state: True]
    ])

    ## Dodongos Cavern Back Room
    # Connections
    connect_regions(Regions.DODONGOS_CAVERN_BACK_ROOM, world, [
        [Regions.DODONGOS_CAVERN_BOSS_REGION, lambda state: True]
    ])

    # Locations
    add_locations(Regions.DODONGOS_CAVERN_BACK_ROOM, world, [
        [Locations.DODONGOS_CAVERN_GS_BACK_ROOM, lambda state: can_attack(state, world)],
        [Locations.DODONGOS_CAVERN_BACK_ROOM_POT1, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_BACK_ROOM_POT2, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_BACK_ROOM_POT3, lambda state: can_break_pots(state, world)],
        [Locations.DODONGOS_CAVERN_BACK_ROOM_POT4, lambda state: can_break_pots(state, world)]
    ])