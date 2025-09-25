from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import *
from worlds.oot_soh.LogicHelpers import (is_child, is_adult, can_attack, can_kill_enemy,
                                  has_fire_source_with_torch, can_use, can_cut_shrubs, 
                                  can_pass_enemy, can_reflect_nuts, can_do_trick,
                                  can_hit_eye_targets, blast_or_smash, has_item,
                                  hookshot_or_boomerang)

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
    set_location_rules(world)


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    double_link_regions(world, Regions.DEKU_TREE_ENTRYWAY.value, Regions.DEKU_TREE_LOBBY.value)

    # Lobby connections
    # Slingshot Room access requires shield
    world.get_region(Regions.DEKU_TREE_LOBBY.value).connect(
        world.get_region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value))

    # Compass Room - simple access from lobby
    world.get_region(Regions.DEKU_TREE_LOBBY.value).connect(
        world.get_region(Regions.DEKU_TREE_COMPASS_ROOM))
    
    # Basement access requires ability to deal with enemies or adult
    world.get_region(Regions.DEKU_TREE_LOBBY.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value),
        rule=lambda state: can_attack(state, world) or can_use(Items.NUTS.value, state, world))

    # Deku F2 middle room
    world.get_region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_LOBBY),
        rule=lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world))

    world.get_region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_SLINGSHOT_ROOM),
        rule=lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world))
    
    # Deku slingshot room
    world.get_region(Regions.DEKU_TREE_SLINGSHOT_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value),
        rule=lambda state: can_use(Items.FAIRY_SLINGSHOT) or can_use(Items.HOVER_BOOTS))

    # Deku compass room
    world.get_region(Regions.DEKU_TREE_COMPASS_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_LOBBY),
        #rule=lambda state: has_fire_source_with_torch(state, world))
        # Above commented out because it can't succeed without stick pot event implemented
    )

    # Deku Basement Lower
    world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value).connect(
        world.get_region(Regions.DEKU_TREE_LOBBY.value))

    world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value),
        #rule=lambda state: has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world))
        # Above commented out because it can't succeed without stick pot event implemented
    )

    world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value),
        # Todo figure this one out 
        rule=lambda state: is_adult(state, world) or can_do_trick("Deku B1 Skip")
        or world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value).can_reach(Regions.DEKU_TREE_BASEMENT_UPPER, state, world) 
    )

    # Deku basement shrub room
    world.get_region(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value))
    
    world.get_region(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value),
        rule=lambda state: can_hit_eye_targets(state, world))

    # Deku basement water room front
    world.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value))
    
    world.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value),
        rule=lambda state: has_item(Items.BRONZE_SCALE.value) or can_do_trick("Deku B1 backflip over spiked log"))

    # Deku basement water room back
    world.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value),
        rule=lambda state: has_item(Items.BRONZE_SCALE.value) or can_do_trick("Deku B1 backflip over spiked log"))

    world.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value))

    # Deku tree basement torch room
    world.get_region(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value))

    world.get_region(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value),
        #rule=lambda state: has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world))
        # Above commented out because it can't succeed without stick pot event implemented
    )

    # Deku basement back lobby
    world.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value))
    
    world.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value),
        #rule=lambda state: (has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)) 
        #    and blast_or_smash(state, world))
        # Above commented out because it can't succeed without stick pot event implemented
    )

    world.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value),
        #rule=lambda state: (has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world))
        #    and is_child(state, world))
        # Above commented out because it can't succeed without stick pot event implemented
    )

    # Deku basement back room
    world.get_region(Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value))

    # Deku basement upper
    world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value))
    
    world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value),
        rule=lambda state: is_child(state, world))

    world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value).connect(
        world.get_region(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value),
        #rule=lambda state: has_fire_source_with_torch(state, world) or 
        #    (can_do_trick("Deku B1 bow webs") and is_adult(state, world) and can_use(Items.FAIRY_BOW.value)))
        # Above commented out because it can't succeed without stick pot event implemented
    )

    # Deku outside boss room
    world.get_region(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value))

    world.get_region(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_BOSS_ENTRYWAY.value.value),
        rule=lambda state: (has_item(Items.BRONZE_SCALE.value, state, world) or can_use(Items.IRON_BOOTS.value))
            and can_reflect_nuts(state, world))
    
    # Skipping master quest for now

    # Deku Boss room entryway
    world.get_region(Regions.DEKU_TREE_BOSS_ENTRYWAY.value).connect(
        world.get_region(Regions.DEKU_TREE_BOSS_ROOM.value))
    
    # Deku boss exit
    world.get_region(Regions.DEKU_TREE_BOSS_EXIT.value).connect(
        world.get_region(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value))
    # skipping mq connection

    # Deku Tree boss room
    world.get_region(Regions.DEKU_TREE_BOSS_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_BOSS_EXIT.value))
    
    world.get_region(Regions.DEKU_TREE_BOSS_ROOM.value).connect(
        world.get_region(Regions.ROOT.value),
        rule=lambda state: can_kill_enemy(state, world, "gohma"))


def set_location_rules(world: "SohWorld") -> None:
    player = world.player

    # Deku Tree Map Chest
    set_rule(world.get_location(Locations.DEKU_TREE_MAP_CHEST.value),
             rule=lambda state: True)  # Always accessible

    # Deku Tree Slingshot Chest
    set_rule(world.get_location(Locations.DEKU_TREE_SLINGSHOT_CHEST.value),
             rule=lambda state: True)

    # Deku Tree Slingshot Room Side Chest
    set_rule(world.get_location(Locations.DEKU_TREE_SLINGSHOT_ROOM_SIDE_CHEST.value),
             rule=lambda state: True)

    # Deku Tree Compass Chest
    set_rule(world.get_location(Locations.DEKU_TREE_COMPASS_CHEST.value),
             rule=lambda state: True)

    # Deku Tree Compass Room Side Chest
    set_rule(world.get_location(Locations.DEKU_TREE_COMPASS_ROOM_SIDE_CHEST.value),
             rule=lambda state: True)

    # Deku Tree Basement Chest
    set_rule(world.get_location(Locations.DEKU_TREE_BASEMENT_CHEST.value),
             rule=lambda state: True)

    # Queen Gohma Dungeon Reward
    set_rule(world.get_location(Locations.QUEEN_GOHMA.value),
             rule=lambda state: can_kill_enemy(state, world, "gohma"))

    # Queen Gohma Heart Container
    set_rule(world.get_location(Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER.value),
             rule=lambda state: can_kill_enemy(state, world, "gohma"))

    # Only set rule on freestanding items if they are shuffled
    if world.options.shuffle_freestanding_items in ["dungeon", "all"]:
        set_rule(world.get_location(Locations.DEKU_TREE_LOBBY_LOWER_HEART.value),
                    rule=lambda state: True)  # Always accessible
        set_rule(world.get_location(Locations.DEKU_TREE_LOBBY_UPPER_HEART.value),
                    rule=lambda state: can_pass_enemy(state, world, "big_skulltula"))
        for underwater_heart in (Locations.DEKU_TREE_FINAL_ROOM_LEFT_FRONT_HEART, 
                                 Locations.DEKU_TREE_FINAL_ROOM_LEFT_BACK_HEART, 
                                 Locations.DEKU_TREE_FINAL_ROOM_RIGHT_HEART):
            set_rule(world.getLocation(underwater_heart.value),
                rule=lambda state: has_item(Items.BRONZE_SCALE, state, world) 
                    or can_use(Items.IRON_BOOTS, state, world) 
                    or can_use(Items.IRON_BOOTS, state, world))

    # Only set rule on grass items if they are shuffled
    if world.options.shuffle_grass in ["dungeon", "all"]:
        # Normal Grass
        for grass_spot in (Locations.DEKU_TREE_LOBBY_GRASS1,
                Locations.DEKU_TREE_LOBBY_GRASS2,
                Locations.DEKU_TREE_LOBBY_GRASS3,
                Locations.DEKU_TREE_LOBBY_GRASS4,
                Locations.DEKU_TREE_LOBBY_GRASS5,
                Locations.DEKU_TREE_COMPASS_GRASS1,
                Locations.DEKU_TREE_COMPASS_GRASS2,
                Locations.DEKU_TREE_BASEMENT_GRASS1,
                Locations.DEKU_TREE_BASEMENT_GRASS2,
                Locations.DEKU_TREE_EYE_SWITCH_GRASS1,
                Locations.DEKU_TREE_EYE_SWITCH_GRASS2,
                Locations.DEKU_TREE_EYE_SWITCH_GRASS3,
                Locations.DEKU_TREE_EYE_SWITCH_GRASS4,
                Locations.DEKU_TREE_SPIKE_ROLLER_GRASS1,
                Locations.DEKU_TREE_SPIKE_ROLLER_GRASS2,
                Locations.DEKU_TREE_TORCHES_GRASS1,
                Locations.DEKU_TREE_TORCHES_GRASS2,
                Locations.DEKU_TREE_LARVAE_GRASS1,
                Locations.DEKU_TREE_LARVAE_GRASS2,
                Locations.DEKU_TREE_QUEEN_GOHMA_GRASS1,
                Locations.DEKU_TREE_QUEEN_GOHMA_GRASS2,
                Locations.DEKU_TREE_QUEEN_GOHMA_GRASS3,
                Locations.DEKU_TREE_QUEEN_GOHMA_GRASS4,
                Locations.DEKU_TREE_QUEEN_GOHMA_GRASS5,
                Locations.DEKU_TREE_QUEEN_GOHMA_GRASS6,
                Locations.DEKU_TREE_QUEEN_GOHMA_GRASS7,
                Locations.DEKU_TREE_QUEEN_GOHMA_GRASS8):
            set_rule(grass_spot.value, rule=lambda state: can_cut_shrubs(state, world))

        # Scrub reflectable grass
        for grass_spot in (Locations.DEKU_TREE_SLINGSHOT_GRASS1,
                Locations.DEKU_TREE_SLINGSHOT_GRASS2,
                Locations.DEKU_TREE_SLINGSHOT_GRASS3,
                Locations.DEKU_TREE_SLINGSHOT_GRASS4):
            set_rule(grass_spot.value, rule=lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world))  # can reflect is probably a mistake in SoH

        # Requires fire grass
        for grass_spot in (Locations.DEKU_TREE_BEFORE_BOSS_GRASS1,
                Locations.DEKU_TREE_BEFORE_BOSS_GRASS2,
                Locations.DEKU_TREE_BEFORE_BOSS_GRASS3):
            #set_rule(grass_spot.value, rule=lambda state: can_cut_shrubs(state, world) and has_fire_source_with_torch(state, world))
            # Above commented out because it can't succeed without stick pot event implemented
            set_rule(grass_spot.value, rule=lambda state: can_cut_shrubs(state, world))

    # Only set rule on Gold Skulltula tokens if they are shuffled
    if world.options.shuffle_skull_tokens in ["dungeon", "all"]:
        set_rule(world.get_location(Locations.DEKU_TREE_GS_COMPASS_ROOM.value),
                    rule=lambda state: can_kill_enemy(state, world, "gold_skulltula"))
        set_rule(world.get_location(Locations.DEKU_TREE_GS_BASEMENT_GATE.value),
                    rule=lambda state: can_kill_enemy(state, world, "gold_skulltula", "short_jumpslash"))
        set_rule(world.get_location(Locations.DEKU_TREE_GS_BASEMENT_VINES.value),
                    rule=lambda state: can_kill_enemy(state, world, "gold_skulltula", "short_jumpslash" if can_do_trick("Deku MQ Compass GS") else "bomb_throw"))
        set_rule(world.get_location(Locations.DEKU_TREE_GS_BASEMENT_BACK_ROOM.value),
                    rule=lambda state: hookshot_or_boomerang(state, world))
