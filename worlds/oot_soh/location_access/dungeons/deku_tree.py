from typing import TYPE_CHECKING

from ...Enums import *
from ...LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


class EventLocations(str, Enum):
    DEKU_TREE_LOBBY_BABA_STICKS = "Deku Tree Lobby Baba Sticks",
    DEKU_TREE_LOBBY_BABA_NUTS = "Deku Tree Lobby Baba Nuts",
    DEKU_TREE_COMPASS_BABA_STICKS = "Deku Tree Compass Room Baba Sticks",
    DEKU_TREE_COMPASS_BABA_NUTS = "Deku Tree Compass Room Baba Nuts",
    DEKU_TREE_BASEMENT_LOWER_BABA_STICKS = "Deku Tree Basement Lower Baba Sticks",
    DEKU_TREE_BASEMENT_LOWER_BABA_NUTS = "Deku Tree Basement Lower Baba Nuts",
    DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_STICKS = "Deku Tree Basement Torch Room Baba Sticks",
    DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_NUTS = "Deku Tree Torch Room Baba Nuts",
    DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_STICKS = "Deku Tree Basement Back Lobby Baba Sticks",
    DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_NUTS = "Deku Tree Basement Back Lobby Baba Nuts",
    DEKU_TREE_BASEMENT_UPPER_BABA_STICKS = "Deku Tree Basement Upper Baba Sticks",
    DEKU_TREE_BASEMENT_UPPER_BABA_NUTS = "Deku Tree Basement Upper Baba Nuts",
    DEKU_TREE_BASEMENT_UPPER_BLOCK = "Deku Tree Basement Upper Push Block",
    DEKU_TREE_BOSS = "Deku Tree Queen Gohma"


class LocalEvents(str, Enum):
    DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED = "Deku Tree Basement Upper Block Pushed"


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    ## Deku Tree Entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_ENTRYWAY, world, [
        [Regions.DEKU_TREE_LOBBY, lambda state: True],
        [Regions.KF_OUTSIDE_DEKU_TREE, lambda state: True]
    ])

    ## Deku Lobby
    # Events
    add_events(Regions.DEKU_TREE_LOBBY, world, [
        [EventLocations.DEKU_TREE_LOBBY_BABA_STICKS, Events.DEKU_BABA_STICKS, lambda state: can_get_deku_baba_sticks(state, world)],
        [EventLocations.DEKU_TREE_LOBBY_BABA_NUTS, Events.DEKU_BABA_NUTS, lambda state: can_get_deku_baba_nuts(state, world)]
    ])

    # Locations
    add_locations(Regions.DEKU_TREE_LOBBY, world, [
        [Locations.DEKU_TREE_MAP_CHEST, lambda state: True],
        [Locations.DEKU_TREE_LOBBY_LOWER_HEART, lambda state: True],
        [Locations.DEKU_TREE_LOBBY_UPPER_HEART, lambda state: can_pass_enemy(state, world, Enemies.BIG_SKULLTULA)],
        [Locations.DEKU_TREE_LOBBY_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_LOBBY_GRASS2, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_LOBBY_GRASS3, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_LOBBY_GRASS4, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_LOBBY_GRASS5, lambda state: can_cut_shrubs(state, world)]
    ])
    
    # Connections
    connect_regions(Regions.DEKU_TREE_LOBBY, world, [
        [Regions.DEKU_TREE_2F_MIDDLE_ROOM, lambda state: True],
        [Regions.DEKU_TREE_COMPASS_ROOM, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_LOWER, lambda state: can_attack(state, world) or can_use(Items.NUTS, state, world)]
    ])
    

    ## Deku F2 middle room
    # Connections
    connect_regions(Regions.DEKU_TREE_2F_MIDDLE_ROOM, world, [
        [Regions.DEKU_TREE_LOBBY, lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER, state, world)],
        [Regions.DEKU_TREE_SLINGSHOT_ROOM, lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER, state, world)]
    ])
    
    ## Deku slingshot room
    # Locations
    add_locations(Regions.DEKU_TREE_SLINGSHOT_ROOM, world, [
        [Locations.DEKU_TREE_SLINGSHOT_CHEST, lambda state: True],
        [Locations.DEKU_TREE_SLINGSHOT_ROOM_SIDE_CHEST, lambda state: True],
        [Locations.DEKU_TREE_SLINGSHOT_GRASS1, lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)],
        [Locations.DEKU_TREE_SLINGSHOT_GRASS2, lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)],
        [Locations.DEKU_TREE_SLINGSHOT_GRASS3, lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)],
        [Locations.DEKU_TREE_SLINGSHOT_GRASS4, lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_SLINGSHOT_ROOM, world, [
        [Regions.DEKU_TREE_2F_MIDDLE_ROOM, lambda state: can_use(Items.FAIRY_SLINGSHOT, state, world) or can_use(Items.HOVER_BOOTS, state, world)]
    ])

    ## Deku compass room
    # Events
    add_events(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        [EventLocations.DEKU_TREE_COMPASS_BABA_STICKS, Events.DEKU_BABA_STICKS, lambda state: can_get_deku_baba_sticks(state, world)],
        [EventLocations.DEKU_TREE_COMPASS_BABA_NUTS, Events.DEKU_BABA_NUTS, lambda state: can_get_deku_baba_nuts(state, world)]
    ])

    # Locations
    add_locations(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        [Locations.DEKU_TREE_COMPASS_CHEST, lambda state: True],
        [Locations.DEKU_TREE_COMPASS_ROOM_SIDE_CHEST, lambda state: True],
        [Locations.DEKU_TREE_GS_COMPASS_ROOM, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA)],
        [Locations.DEKU_TREE_COMPASS_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_COMPASS_GRASS2, lambda state: can_cut_shrubs(state, world)]
    ])      
    # Connections
    connect_regions(Regions.DEKU_TREE_COMPASS_ROOM, world, [
        [Regions.DEKU_TREE_LOBBY, lambda state: True] # has_fire_source_with_torch(state, world)]
        # Above commented out because it can't succeed without stick pot event implemented
    ])

    ## Deku Basement Lower
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        [EventLocations.DEKU_TREE_BASEMENT_LOWER_BABA_STICKS, Events.DEKU_BABA_STICKS, lambda state: can_get_deku_baba_sticks(state, world)],
        [EventLocations.DEKU_TREE_BASEMENT_LOWER_BABA_NUTS, Events.DEKU_BABA_NUTS, lambda state: can_get_deku_baba_nuts(state, world)]
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        [Locations.DEKU_TREE_BASEMENT_CHEST, lambda state: True],
        [Locations.DEKU_TREE_GS_BASEMENT_GATE, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH)],
        #[Locations.DEKU_TREE_GS_BASEMENT_VINES, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH if can_do_trick("Deku MQ Compass GS", state, world) else EnemyDistance.BOMB_THROW)],
        # Above commented out because Bomb Throw distance causes fill error
        [Locations.DEKU_TREE_GS_BASEMENT_VINES, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA, EnemyDistance.SHORT_JUMPSLASH)],
        [Locations.DEKU_TREE_BASEMENT_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_BASEMENT_GRASS2, lambda state: can_cut_shrubs(state, world)]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_LOWER, world, [
        [Regions.DEKU_TREE_LOBBY, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, lambda state: True], # has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW, state, world)],
        # Above commented out because it can't succeed without stick pot event implemented
        [Regions.DEKU_TREE_BASEMENT_UPPER, lambda state: is_adult(state, world) or can_do_trick("Deku B1 Skip", state, world)
            or has_item(LocalEvents.DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED, state, world)]
    ])

    ## Deku basement shrub room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, world, [
        [Locations.DEKU_TREE_EYE_SWITCH_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_EYE_SWITCH_GRASS2, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_EYE_SWITCH_GRASS3, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_EYE_SWITCH_GRASS4, lambda state: can_cut_shrubs(state, world)]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, world, [
        [Regions.DEKU_TREE_BASEMENT_LOWER, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT, lambda state: can_hit_eye_targets(state, world)]
    ])
    
    ## Deku basement water room front
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT, world, [
        [Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, lambda state: has_item(Items.BRONZE_SCALE, state, world) or can_do_trick("Deku B1 backflip over spiked log", state, world)]
    ])

    ## Deku basement water room back
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, world, [
        [Locations.DEKU_TREE_SPIKE_ROLLER_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_SPIKE_ROLLER_GRASS2, lambda state: can_cut_shrubs(state, world)]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, world, [
        [Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT, lambda state: has_item(Items.BRONZE_SCALE, state, world) or can_do_trick("Deku B1 backflip over spiked log", state, world)],
        [Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, lambda state: True]
    ])

    ## Deku tree basement torch room
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        [EventLocations.DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_STICKS, Events.DEKU_BABA_STICKS, lambda state: can_get_deku_baba_sticks(state, world)],
        [EventLocations.DEKU_TREE_BASEMENT_TORCH_ROOM_BABA_NUTS, Events.DEKU_BABA_NUTS, lambda state: can_get_deku_baba_nuts(state, world)]
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        [Locations.DEKU_TREE_TORCHES_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_TORCHES_GRASS2, lambda state: can_cut_shrubs(state, world)]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, world, [
        [Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda state: True] #lambda state: has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW, state, world)]
        # Above commented out because it can't succeed without stick pot event implemented
    ])

    ## Deku basement back lobby
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        [EventLocations.DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_STICKS, Events.DEKU_BABA_STICKS, lambda state: can_get_deku_baba_sticks(state, world)],
        [EventLocations.DEKU_TREE_BASEMENT_BACK_LOBBY_BABA_NUTS, Events.DEKU_BABA_NUTS, lambda state: can_get_deku_baba_nuts(state, world)]
    ])
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        [Locations.DEKU_TREE_LARVAE_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_LARVAE_GRASS2, lambda state: can_cut_shrubs(state, world)]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, world, [
        [Regions.DEKU_TREE_BASEMENT_TORCH_ROOM, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_BACK_ROOM, lambda state: True], # lambda state: (has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW, state, world)],
        [Regions.DEKU_TREE_BASEMENT_UPPER, lambda state: True] # lambda state: (has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW, state, world)],
        # Above commented out because it can't succeed without stick pot event implemented
        
    ])

    ## Deku basement back room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_BACK_ROOM, world, [
        [Locations.DEKU_TREE_GS_BASEMENT_BACK_ROOM, lambda state: hookshot_or_boomerang(state, world)],
        
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_BACK_ROOM, world, [
        [Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda state: True],
        ])

    ## Deku basement upper
    # Events
    add_events(Regions.DEKU_TREE_BASEMENT_UPPER, world, [
        [EventLocations.DEKU_TREE_BASEMENT_UPPER_BABA_STICKS, Events.DEKU_BABA_STICKS, lambda state: can_get_deku_baba_sticks(state, world)],
        [EventLocations.DEKU_TREE_BASEMENT_UPPER_BABA_NUTS, Events.DEKU_BABA_NUTS, lambda state: can_get_deku_baba_nuts(state, world)],
        [EventLocations.DEKU_TREE_BASEMENT_UPPER_BLOCK, LocalEvents.DEKU_TREE_BASEMENT_UPPER_BLOCK_PUSHED, lambda state: True]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_UPPER, world, [
        [Regions.DEKU_TREE_BASEMENT_LOWER, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_BACK_LOBBY, lambda state: is_child(state, world)],
        [Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, lambda state: True] # lambda state: has_fire_source_with_torch(state, world) or 
        #    (can_do_trick("Deku B1 bow webs") and is_adult(state, world) and can_use(Items.FAIRY_BOW))]
        # Above commented out because it can't succeed without stick pot event implemented
    ])

    ## Deku outside boss room
    # Locations
    add_locations(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, world, [
        [Locations.DEKU_TREE_FINAL_ROOM_LEFT_FRONT_HEART, lambda state: has_item(Items.BRONZE_SCALE, state, world) or can_use(Items.IRON_BOOTS, state, world) or can_use(Items.IRON_BOOTS, state, world)],
        [Locations.DEKU_TREE_FINAL_ROOM_LEFT_BACK_HEART, lambda state: has_item(Items.BRONZE_SCALE, state, world) or can_use(Items.IRON_BOOTS, state, world) or can_use(Items.IRON_BOOTS, state, world)],
        [Locations.DEKU_TREE_FINAL_ROOM_RIGHT_HEART, lambda state: has_item(Items.BRONZE_SCALE, state, world) or can_use(Items.IRON_BOOTS, state, world) or can_use(Items.IRON_BOOTS, state, world)],
        [Locations.DEKU_TREE_BEFORE_BOSS_GRASS1, lambda state: can_cut_shrubs(state, world)], # lambda state: can_cut_shrubs(state, world) and has_fire_source_with_torch(state, world)
            # Above commented out because it can't succeed without stick pot event implemented],
        [Locations.DEKU_TREE_BEFORE_BOSS_GRASS2, lambda state: can_cut_shrubs(state, world)], # lambda state: can_cut_shrubs(state, world) and has_fire_source_with_torch(state, world)
            # Above commented out because it can't succeed without stick pot event implemented],
        [Locations.DEKU_TREE_BEFORE_BOSS_GRASS3, lambda state: can_cut_shrubs(state, world)] # lambda state: can_cut_shrubs(state, world) and has_fire_source_with_torch(state, world)
            # Above commented out because it can't succeed without stick pot event implemented]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, world, [
        [Regions.DEKU_TREE_BASEMENT_UPPER, lambda state: True],
        [Regions.DEKU_TREE_BOSS_ENTRYWAY, lambda state: (has_item(Items.BRONZE_SCALE, state, world) or can_use(Items.IRON_BOOTS, state, world))
            and can_reflect_nuts(state, world)]
    ])
    
    # Skipping master quest for now

    ## Deku Boss room entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ENTRYWAY, world, [
        [Regions.DEKU_TREE_BOSS_ROOM, lambda state: True]
    ])
    
    ## Deku boss exit
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_EXIT, world, [
        [Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM, lambda state: True],
        # skipping mq connection
    ])
    

    ## Deku Tree boss room
    # Events
    add_events(Regions.DEKU_TREE_BOSS_ROOM, world, [
        [EventLocations.DEKU_TREE_BOSS, Events.CLEARED_DEKU_TREE, lambda state: can_kill_enemy(state, world, Enemies.GOHMA)]
    ])

    # Locations
    add_locations(Regions.DEKU_TREE_BOSS_ROOM, world, [
        [Locations.QUEEN_GOHMA, lambda state: has_item(Events.CLEARED_DEKU_TREE, state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER, lambda state: has_item(Events.CLEARED_DEKU_TREE, state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS1, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS2, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS3, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS4, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS5, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS6, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS7, lambda state: can_cut_shrubs(state, world)],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS8, lambda state: can_cut_shrubs(state, world)]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ROOM, world, [
        [Regions.DEKU_TREE_BOSS_EXIT, lambda state: True],
        [Regions.KF_OUTSIDE_DEKU_TREE, lambda state: has_item(Events.CLEARED_DEKU_TREE, state, world)]   
    ])
