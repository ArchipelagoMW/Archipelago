from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import *
from worlds.oot_soh.LogicHelpers import *

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


events: dict[str, SohLocationData] = {
    "Deku Tree Lobby Switch": SohLocationData(Regions.DEKU_TREE_LOBBY.value,
                                             event_item="Deku Tree Lobby Switch Activated"),
    "Deku Tree Basement Push Block": SohLocationData(Regions.DEKU_TREE_BASEMENT_LOWER.value,
                                                    event_item="Deku Tree Basement Push Block Moved"),
}


def create_regions_and_rules(world: "SohWorld") -> None:
    for event_name, data in events.items():
        region = world.get_region(data.region)
        region.add_event(event_name, data.event_item, location_type=SohLocation, item_type=SohItem)

    set_region_rules(world)


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    double_link_regions(world, Regions.DEKU_TREE_ENTRYWAY.value, Regions.ROOT.value)

    double_link_regions(world, Regions.DEKU_TREE_ENTRYWAY.value, Regions.DEKU_TREE_LOBBY.value)

    # repeated rules
    normal_grass_rule = lambda state: can_cut_shrubs(state, world)
    requires_reflect_grass_rule = lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)
    #requires_fire_grass_rule = lambda state: can_cut_shrubs(state, world) and has_fire_source_with_torch(state, world)
            # Above commented out because it can't succeed without stick pot event implemented
    requires_fire_grass_rule =lambda state: can_cut_shrubs(state, world)


    ## Deku Lobby
    # Locations
    add_locations(Regions.DEKU_TREE_LOBBY, world, [
        [Locations.DEKU_TREE_MAP_CHEST.value, lambda state: True],
        [Locations.DEKU_TREE_LOBBY_LOWER_HEART.value, lambda state: True],
        [Locations.DEKU_TREE_LOBBY_UPPER_HEART.value, lambda state: can_pass_enemy(state, world, Enemies.BIG_SKULLTULA.value)],
        [Locations.DEKU_TREE_LOBBY_GRASS1, normal_grass_rule],
        [Locations.DEKU_TREE_LOBBY_GRASS2, normal_grass_rule],
        [Locations.DEKU_TREE_LOBBY_GRASS3, normal_grass_rule],
        [Locations.DEKU_TREE_LOBBY_GRASS4, normal_grass_rule],
        [Locations.DEKU_TREE_LOBBY_GRASS5, normal_grass_rule]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_LOBBY.value, world, [
        [Regions.DEKU_TREE_2F_MIDDLE_ROOM.value, lambda state: True],
        [Regions.DEKU_TREE_COMPASS_ROOM, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_LOWER.value, lambda state: can_attack(state, world) or can_use(Items.NUTS.value, state, world)]
    ])
    

    ## Deku F2 middle room
    # Connections
    connect_regions(Regions.DEKU_TREE_2F_MIDDLE_ROOM, world, [
        [Regions.DEKU_TREE_LOBBY, lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world)],
        [Regions.DEKU_TREE_SLINGSHOT_ROOM, lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world)]
    ])
    
    ## Deku slingshot room
    # Locations
    add_locations(Regions.DEKU_TREE_SLINGSHOT_ROOM.value, world, [
        [Locations.DEKU_TREE_SLINGSHOT_CHEST.value, lambda state: True],
        [Locations.DEKU_TREE_SLINGSHOT_ROOM_SIDE_CHEST.value, lambda state: True],
        [Locations.DEKU_TREE_SLINGSHOT_GRASS1, requires_reflect_grass_rule],
        [Locations.DEKU_TREE_SLINGSHOT_GRASS2, requires_reflect_grass_rule],
        [Locations.DEKU_TREE_SLINGSHOT_GRASS3, requires_reflect_grass_rule],
        [Locations.DEKU_TREE_SLINGSHOT_GRASS4, requires_reflect_grass_rule]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_SLINGSHOT_ROOM.value, world, [
        [Regions.DEKU_TREE_2F_MIDDLE_ROOM.value, lambda state: can_use(Items.FAIRY_SLINGSHOT) or can_use(Items.HOVER_BOOTS)]
    ])

    ## Deku compass room
    # Locations
    add_locations(Regions.DEKU_TREE_COMPASS_ROOM.value, world, [
        [Locations.DEKU_TREE_COMPASS_CHEST.value, lambda state: True],
        [Locations.DEKU_TREE_COMPASS_ROOM_SIDE_CHEST.value, lambda state: True],
        [Locations.DEKU_TREE_GS_COMPASS_ROOM.value, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA.value)],
        [Locations.DEKU_TREE_COMPASS_GRASS1, normal_grass_rule],
        [Locations.DEKU_TREE_COMPASS_GRASS2, normal_grass_rule]
    ])      
    # Connections
    connect_regions(Regions.DEKU_TREE_COMPASS_ROOM.value, world, [
        [Regions.DEKU_TREE_LOBBY.value, lambda state: True] # has_fire_source_with_torch(state, world)]
        # Above commented out because it can't succeed without stick pot event implemented
    ])

    ## Deku Basement Lower
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_LOWER.value, world, [
        [Locations.DEKU_TREE_BASEMENT_CHEST.value, lambda state: True],
        [Locations.DEKU_TREE_GS_BASEMENT_GATE.value, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA.value, Combat_Ranges.SHORT_JUMPSLASH.value)],
        #[Locations.DEKU_TREE_GS_BASEMENT_VINES.value, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA.value, Combat_Ranges.SHORT_JUMPSLASH.value if can_do_trick("Deku MQ Compass GS", state, world) else Combat_Ranges.BOMB_THROW.value)],
        # Above commented out because Bomb Throw distance causes fill error
        [Locations.DEKU_TREE_GS_BASEMENT_VINES.value, lambda state: can_kill_enemy(state, world, Enemies.GOLD_SKULLTULA.value, Combat_Ranges.SHORT_JUMPSLASH.value)],
        [Locations.DEKU_TREE_BASEMENT_GRASS1, normal_grass_rule],
        [Locations.DEKU_TREE_BASEMENT_GRASS2, normal_grass_rule]
    ])
        
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_LOWER.value, world, [
        [Regions.DEKU_TREE_LOBBY.value, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value, lambda state: True], # has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)],
        # Above commented out because it can't succeed without stick pot event implemented
        [Regions.DEKU_TREE_BASEMENT_UPPER.value, lambda state: is_adult(state, world) or can_do_trick("Deku B1 Skip") 
            or world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value).can_reach(Regions.DEKU_TREE_BASEMENT_UPPER, state, world)]

    ])

    ## Deku basement shrub room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value, world, [
        [Locations.DEKU_TREE_EYE_SWITCH_GRASS1, normal_grass_rule],
        [Locations.DEKU_TREE_EYE_SWITCH_GRASS2, normal_grass_rule],
        [Locations.DEKU_TREE_EYE_SWITCH_GRASS3, normal_grass_rule],
        [Locations.DEKU_TREE_EYE_SWITCH_GRASS4, normal_grass_rule]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value, world, [
        [Regions.DEKU_TREE_BASEMENT_LOWER.value, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value, lambda state: can_hit_eye_targets(state, world)]
    ])
    
    ## Deku basement water room front
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value, world, [
        [Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value, lambda state: has_item(Items.BRONZE_SCALE.value, state, world) or can_do_trick("Deku B1 backflip over spiked log")]
    ])

    ## Deku basement water room back
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value, world, [
        [Locations.DEKU_TREE_SPIKE_ROLLER_GRASS1, normal_grass_rule],
        [Locations.DEKU_TREE_SPIKE_ROLLER_GRASS2, normal_grass_rule]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value, world, [
        [Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value, lambda state: has_item(Items.BRONZE_SCALE.value, state, world) or can_do_trick("Deku B1 backflip over spiked log")],
        [Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value, lambda state: True]
    ])

    ## Deku tree basement torch room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value, world, [
        [Locations.DEKU_TREE_TORCHES_GRASS1, normal_grass_rule],
        [Locations.DEKU_TREE_TORCHES_GRASS2, normal_grass_rule]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value, world, [
        [Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, lambda state: True] #lambda state: has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)]
        # Above commented out because it can't succeed without stick pot event implemented
    ])

    ## Deku basement back lobby
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, world, [
        [Locations.DEKU_TREE_LARVAE_GRASS1, normal_grass_rule],
        [Locations.DEKU_TREE_LARVAE_GRASS2, normal_grass_rule]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, world, [
        [Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value, lambda state: True], # lambda state: (has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)],
        [Regions.DEKU_TREE_BASEMENT_UPPER.value, lambda state: True] # lambda state: (has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)],
        # Above commented out because it can't succeed without stick pot event implemented
        
    ])

    ## Deku basement back room
    # Locations
    add_locations(Regions.DEKU_TREE_BASEMENT_BACK_ROOM, world, [
        [Locations.DEKU_TREE_GS_BASEMENT_BACK_ROOM.value, lambda state: hookshot_or_boomerang(state, world)],
        
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value, world, [
        [Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, lambda state: True],
        ])

    ## Deku basement upper
    # Connections
    connect_regions(Regions.DEKU_TREE_BASEMENT_UPPER.value, world, [
        [Regions.DEKU_TREE_BASEMENT_LOWER.value, lambda state: True],
        [Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, lambda state: is_child(state, world)],
        [Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value, lambda state: True] # lambda state: has_fire_source_with_torch(state, world) or 
        #    (can_do_trick("Deku B1 bow webs") and is_adult(state, world) and can_use(Items.FAIRY_BOW.value))]
        # Above commented out because it can't succeed without stick pot event implemented
    ])

    ## Deku outside boss room
    # Locations
    outside_boss_freestanding_rule = lambda state: has_item(Items.BRONZE_SCALE, state, world) \
                                            or can_use(Items.IRON_BOOTS, state, world) \
                                            or can_use(Items.IRON_BOOTS, state, world)
    
    add_locations(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value, world, [
        [Locations.DEKU_TREE_FINAL_ROOM_LEFT_FRONT_HEART, outside_boss_freestanding_rule],
        [Locations.DEKU_TREE_FINAL_ROOM_LEFT_BACK_HEART, outside_boss_freestanding_rule],
        [Locations.DEKU_TREE_FINAL_ROOM_RIGHT_HEART, outside_boss_freestanding_rule],
        [Locations.DEKU_TREE_BEFORE_BOSS_GRASS1, requires_fire_grass_rule],
        [Locations.DEKU_TREE_BEFORE_BOSS_GRASS2, requires_fire_grass_rule],
        [Locations.DEKU_TREE_BEFORE_BOSS_GRASS3, requires_fire_grass_rule]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value, world, [
        [Regions.DEKU_TREE_BASEMENT_UPPER.value, lambda state: True],
        [Regions.DEKU_TREE_BOSS_ENTRYWAY.value, lambda state: (has_item(Items.BRONZE_SCALE.value, state, world) or can_use(Items.IRON_BOOTS.value))
            and can_reflect_nuts(state, world)]
    ])
    
    # Skipping master quest for now

    ## Deku Boss room entryway
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ENTRYWAY.value, world, [
        [Regions.DEKU_TREE_BOSS_ROOM.value, lambda state: True]
    ])
    
    ## Deku boss exit
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_EXIT.value, world, [
        [Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value, lambda state: True],
        # skipping mq connection
    ])
    

    ## Deku Tree boss room
    # Deku Boss room
    add_locations(Regions.DEKU_TREE_BOSS_ROOM.value, world, [
        [Locations.QUEEN_GOHMA.value, lambda state: can_kill_enemy(state, world, "gohma")],
        [Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER.value, lambda state: can_kill_enemy(state, world, "gohma")],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS1, normal_grass_rule],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS2, normal_grass_rule],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS3, normal_grass_rule],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS4, normal_grass_rule],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS5, normal_grass_rule],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS6, normal_grass_rule],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS7, normal_grass_rule],
        [Locations.DEKU_TREE_QUEEN_GOHMA_GRASS8, normal_grass_rule]
    ])
    # Connections
    connect_regions(Regions.DEKU_TREE_BOSS_ROOM.value, world, [
        [Regions.DEKU_TREE_BOSS_EXIT.value, lambda state: True],
        [Regions.KF_OUTSIDE_DEKU_TREE.value, lambda state: can_kill_enemy(state, world, "gohma")]   
    ])
