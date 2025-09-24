from typing import TYPE_CHECKING

from BaseClasses import Region
from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData, base_location_table
from worlds.oot_soh.Enums import Regions, Items, Locations
from worlds.oot_soh.Rules import (can_break_mud_walls, is_adult, has_explosives, can_attack, take_damage, can_shield, can_kill_enemy,
                                  has_fire_source_with_torch, can_use, can_do_trick, can_jump_slash, can_cut_shrubs, 
                                  can_pass_enemy, has_item, can_reflect_nuts, hookshot_or_boomerang,
                                  can_hit_eye_targets, blast_or_smash)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


events: dict[str, SohLocationData] = {
    "Deku Tree Lobby Switch": SohLocationData(Regions.DEKU_TREE_LOBBY.value,
                                             event_item="Deku Tree Lobby Switch Activated"),
    "Deku Tree Basement Push Block": SohLocationData(Regions.DEKU_TREE_BASEMENT_LOWER.value,
                                                    event_item="Deku Tree Basement Push Block Moved"),
}


def create_regions_and_rules(world: "SohWorld") -> None:
    # Regions are now created in the main region_data_table system
    # Just add events and set up rules
    
    for event_name, data in events.items():
        region = world.get_region(data.region)
        region.add_event(event_name, data.event_item, location_type=SohLocation, item_type=SohItem)

    set_region_rules(world)
    set_location_rules(world)


def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    double_link_regions(world, Regions.DEKU_TREE_ENTRYWAY.value, Regions.DEKU_TREE_LOBBY.value)

    # Slingshot Room access requires shield
    world.get_region(Regions.DEKU_TREE_LOBBY.value).connect(
        world.get_region(Regions.DEKU_TREE_SLINGSHOT_ROOM.value),
        rule=lambda state: can_shield(state, world))

    world.get_region(Regions.DEKU_TREE_SLINGSHOT_ROOM.value).connect(
        world.get_region(Regions.DEKU_TREE_LOBBY.value))

    # Compass Room - simple access from lobby
    double_link_regions(world, Regions.DEKU_TREE_LOBBY.value, Regions.DEKU_TREE_COMPASS_ROOM.value)

    # Basement access requires ability to deal with enemies or adult
    world.get_region(Regions.DEKU_TREE_LOBBY.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value),
        rule=lambda state: is_adult(state, world) or can_attack(state, world) or can_use(Items.NUTS.value, state, world))

    world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value).connect(
        world.get_region(Regions.DEKU_TREE_LOBBY.value))

    # Basement Upper access requires adult or specific logic
    world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value),
        rule=lambda state: is_adult(state, world))

    world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value).connect(
        world.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value))

    # Boss room access requires fire source or bow
    world.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value).connect(
        world.get_region(Regions.DEKU_TREE_BOSS_ROOM.value),
        rule=lambda state: has_fire_source_with_torch(state, world) or can_use(Items.PROGRESSIVE_BOW.value, state, world))



def set_location_rules(world: "SohWorld") -> None:
    player = world.player

    # Deku Tree Map Chest
    set_rule(world.get_location(Locations.DEKU_TREE_MAP_CHEST.value),
             rule=lambda state: True)  # Always accessible

    # Deku Tree Slingshot Chest
    set_rule(world.get_location(Locations.DEKU_TREE_SLINGSHOT_CHEST.value),
             rule=lambda state: can_attack(state, world))

    # Deku Tree Slingshot Room Side Chest
    set_rule(world.get_location(Locations.DEKU_TREE_SLINGSHOT_ROOM_SIDE_CHEST.value),
             rule=lambda state: can_attack(state, world))

    # Deku Tree Compass Chest
    set_rule(world.get_location(Locations.DEKU_TREE_COMPASS_CHEST.value),
             rule=lambda state: can_attack(state, world))

    # Deku Tree Compass Room Side Chest
    set_rule(world.get_location(Locations.DEKU_TREE_COMPASS_ROOM_SIDE_CHEST.value),
             rule=lambda state: can_attack(state, world))

    # Deku Tree Basement Chest
    set_rule(world.get_location(Locations.DEKU_TREE_BASEMENT_CHEST.value),
             rule=lambda state: can_attack(state, world))

    # Queen Gohma Heart Container
    set_rule(world.get_location(Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER.value),
             rule=lambda state: can_attack(state, world))

    # Only set rule on freestanding items if they are shuffled
    if world.options.shuffle_freestanding_items in ["dungeon", "all"]:
        try:
            set_rule(world.get_location(Locations.DEKU_TREE_LOBBY_LOWER_HEART.value),
                     rule=lambda state: True)  # Always accessible
        except KeyError:
            pass

        try:
            set_rule(world.get_location(Locations.DEKU_TREE_LOBBY_UPPER_HEART.value),
                     rule=lambda state: can_pass_enemy(state, world, "big_skulltula"))
        except KeyError:
            pass

    # Only set rule on grass items if they are shuffled
    if world.options.shuffle_grass in ["dungeon", "all"]:
        try:
            set_rule(world.get_location(Locations.DEKU_TREE_LOBBY_GRASS1.value),
                     rule=lambda state: can_cut_shrubs(state, world))
        except KeyError:
            pass

        try:
            set_rule(world.get_location(Locations.DEKU_TREE_LOBBY_GRASS2.value),
                     rule=lambda state: can_cut_shrubs(state, world))
        except KeyError:
            pass

        try:
            set_rule(world.get_location(Locations.DEKU_TREE_LOBBY_GRASS3.value),
                     rule=lambda state: can_cut_shrubs(state, world))
        except KeyError:
            pass

    # Only set rule on Gold Skulltula tokens if they are shuffled
    if world.options.shuffle_skull_tokens in ["dungeon", "all"]:
        try:
            set_rule(world.get_location(Locations.DEKU_TREE_GSCOMPASS_ROOM.value),
                     rule=lambda state: can_kill_enemy(state, world, "gold_skulltula"))
        except KeyError:
            pass

        try:
            set_rule(world.get_location(Locations.DEKU_TREE_GSBASEMENT_GATE.value),
                     rule=lambda state: can_kill_enemy(state, world, "gold_skulltula"))
        except KeyError:
            pass

        try:
            set_rule(world.get_location(Locations.DEKU_TREE_GSBASEMENT_VINES.value),
                     rule=lambda state: can_kill_enemy(state, world, "gold_skulltula"))
        except KeyError:
            pass

        try:
            set_rule(world.get_location(Locations.DEKU_TREE_GSBASEMENT_BACK_ROOM.value),
                     rule=lambda state: can_kill_enemy(state, world, "gold_skulltula"))
        except KeyError:
            pass

    # Only set rule on scrubs if they are shuffled - no regular scrubs in vanilla Deku Tree
    if world.options.shuffle_scrubs:
        try:
            # Only MQ has scrubs in Deku Tree
            set_rule(world.get_location(Locations.DEKU_TREE_MQDEKU_SCRUB.value),
                     rule=lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world))
        except KeyError:
            pass
