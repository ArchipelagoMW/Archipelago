"""
Deku Tree dungeon logic for Ocarina of Time Archipelago randomizer.
"""

from typing import TYPE_CHECKING
from worlds.oot_soh.Rules import *
from worlds.oot_soh.Enums import Regions, Items, Locations
from BaseClasses import Region

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld

def create_regions_and_rules(world: "SohWorld") -> None:
    """Create Deku Tree regions and set all access rules."""
    create_deku_tree_regions(world)
    create_deku_tree_entrances(world)
    set_deku_tree_entrance_rules(world) 
    # Location rules will be set later when locations are created by the main system

def create_deku_tree_regions(world: "SohWorld") -> None:
    """Create all Deku Tree dungeon regions."""

    # Deku Tree Entryway
    deku_tree_entryway = Region(Regions.DEKU_TREE_ENTRYWAY.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_entryway)

    # Deku Tree Lobby
    deku_tree_lobby = Region(Regions.DEKU_TREE_LOBBY.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_lobby)

    # Deku Tree 2F Middle Room
    deku_tree_2f_middle_room = Region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_2f_middle_room)

    # Deku Tree Slingshot Room
    deku_tree_slingshot_room = Region(Regions.DEKU_TREE_SLINGSHOT_ROOM.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_slingshot_room)

    # Deku Tree Compass Room
    deku_tree_compass_room = Region(Regions.DEKU_TREE_COMPASS_ROOM.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_compass_room)

    # Deku Tree Basement Lower
    deku_tree_basement_lower = Region(Regions.DEKU_TREE_BASEMENT_LOWER.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_basement_lower)

    # Deku Tree Basement Scrub Room
    deku_tree_basement_scrub_room = Region(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_basement_scrub_room)

    # Deku Tree Basement Water Room Front
    deku_tree_basement_water_room_front = Region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_basement_water_room_front)

    # Deku Tree Basement Water Room Back
    deku_tree_basement_water_room_back = Region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_basement_water_room_back)

    # Deku Tree Basement Torch Room
    deku_tree_basement_torch_room = Region(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_basement_torch_room)

    # Deku Tree Basement Back Lobby
    deku_tree_basement_back_lobby = Region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_basement_back_lobby)

    # Deku Tree Basement Back Room
    deku_tree_basement_back_room = Region(Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_basement_back_room)

    # Deku Tree Basement Upper
    deku_tree_basement_upper = Region(Regions.DEKU_TREE_BASEMENT_UPPER.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_basement_upper)

    # Deku Tree Outside Boss Room
    deku_tree_outside_boss_room = Region(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_outside_boss_room)

    # Deku Tree Boss Entryway
    deku_tree_boss_entryway = Region(Regions.DEKU_TREE_BOSS_ENTRYWAY.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_boss_entryway)

    # Deku Tree Boss Room
    deku_tree_boss_room = Region(Regions.DEKU_TREE_BOSS_ROOM.value, world.player, world.multiworld)
    world.multiworld.regions.append(deku_tree_boss_room)


def create_deku_tree_locations(world: "SohWorld") -> None:
    """Create all Deku Tree dungeon locations."""
    # Note: For now, we'll skip location creation as this should be handled
    # by the main world initialization based on location tables.
    # This function is kept for future implementation when proper location
    # data is available.
    pass




def set_deku_tree_location_rules(world: "SohWorld") -> None:
    """Set access rules for all Deku Tree locations."""

    # Deku Tree Lobby
    world.multiworld.get_location(Locations.DEKU_TREE_MAP_CHEST.value, world.player).access_rule = \
        lambda state: True  # Always accessible

    world.multiworld.get_location(Locations.DEKU_TREE_LOBBY_LOWER_HEART.value, world.player).access_rule = \
        lambda state: True  # Always accessible

    world.multiworld.get_location(Locations.DEKU_TREE_LOBBY_UPPER_HEART.value, world.player).access_rule = \
        lambda state: can_pass_enemy(state, world, "big_skulltula")

    world.multiworld.get_location(Locations.DEKU_TREE_LOBBY_GRASS1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_LOBBY_GRASS2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_LOBBY_GRASS3.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_LOBBY_GRASS4.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_LOBBY_GRASS5.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    # Deku Tree Slingshot Room
    world.multiworld.get_location(Locations.DEKU_TREE_SLINGSHOT_CHEST.value, world.player).access_rule = \
        lambda state: True  # Always accessible once in room

    world.multiworld.get_location(Locations.DEKU_TREE_SLINGSHOT_ROOM_SIDE_CHEST.value, world.player).access_rule = \
        lambda state: True  # Always accessible once in room

    world.multiworld.get_location(Locations.DEKU_TREE_SLINGSHOT_GRASS_1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_SLINGSHOT_GRASS_2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_SLINGSHOT_GRASS_3.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_SLINGSHOT_GRASS_4.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world) and can_reflect_nuts(state, world)

    # Deku Tree Compass Room
    world.multiworld.get_location(Locations.DEKU_TREE_COMPASS_CHEST.value, world.player).access_rule = \
        lambda state: True  # Always accessible once in room

    world.multiworld.get_location(Locations.DEKU_TREE_COMPASS_ROOM_SIDE_CHEST.value, world.player).access_rule = \
        lambda state: True  # Always accessible once in room

    world.multiworld.get_location(Locations.DEKU_TREE_GSCOMPASS_ROOM.value, world.player).access_rule = \
        lambda state: can_attack(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_COMPASS_GRASS_1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_COMPASS_GRASS_2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    # Deku Tree Basement Lower
    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_CHEST.value, world.player).access_rule = \
        lambda state: True  # Always accessible once in room

    world.multiworld.get_location(Locations.DEKU_TREE_GSBASEMENT_GATE.value, world.player).access_rule = \
        lambda state: can_kill_enemy(state, world, "gold_skulltula", combat_range="short_jumpslash")

    world.multiworld.get_location(Locations.DEKU_TREE_GSBASEMENT_VINES.value, world.player).access_rule = \
        lambda state: can_kill_enemy(state, world, "gold_skulltula", combat_range="bomb_throw")  # Default to bomb throw, tricks could make it shorter

    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_GRASS_1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_GRASS_2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    # Deku Tree Basement Scrub Room
    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_SCRUB_ROOM_GRASS_1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_SCRUB_ROOM_GRASS_2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_SCRUB_ROOM_GRASS_3.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_SCRUB_ROOM_GRASS_4.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    # Deku Tree Basement Water Room Back
    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_SPIKE_ROLLER_GRASS_1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_SPIKE_ROLLER_GRASS_2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    # Deku Tree Basement Torch Room
    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_TORCHES_GRASS_1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_TORCHES_GRASS_2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    # Deku Tree Basement Back Lobby
    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_LARVAE_GRASS_1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BASEMENT_LARVAE_GRASS_2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world)

    # Deku Tree Outside Boss Room
    world.multiworld.get_location(Locations.DEKU_TREE_BEFORE_BOSS_LEFT_HEART.value, world.player).access_rule = \
        lambda state: has_item(state, world, Items.BRONZE_SCALE.value) or can_use(Items.IRON_BOOTS.value, state, world) or can_use(Items.BOOMERANG.value, state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BEFORE_BOSS_MIDDLE_HEART.value, world.player).access_rule = \
        lambda state: has_item(state, world, Items.BRONZE_SCALE.value) or can_use(Items.IRON_BOOTS.value, state, world) or can_use(Items.BOOMERANG.value, state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BEFORE_BOSS_RIGHT_HEART.value, world.player).access_rule = \
        lambda state: has_item(state, world, Items.BRONZE_SCALE.value) or can_use(Items.IRON_BOOTS.value, state, world) or can_use(Items.BOOMERANG.value, state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BEFORE_BOSS_GRASS_1.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world) and has_fire_source_with_torch(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BEFORE_BOSS_GRASS_2.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world) and has_fire_source_with_torch(state, world)

    world.multiworld.get_location(Locations.DEKU_TREE_BEFORE_BOSS_GRASS_3.value, world.player).access_rule = \
        lambda state: can_cut_shrubs(state, world) and has_fire_source_with_torch(state, world)

    # Deku Tree Basement Back Room
    world.multiworld.get_location(Locations.DEKU_TREE_GSBASEMENT_BACK_ROOM.value, world.player).access_rule = \
        lambda state: hookshot_or_boomerang(state, world)

    # Deku Tree Boss Room
    world.multiworld.get_location(Locations.DEKU_TREE_QUEEN_GOHMA_HEART_CONTAINER.value, world.player).access_rule = \
        lambda state: True  # Always accessible once in boss room


def set_deku_tree_entrance_rules(world: "SohWorld") -> None:
    """Set access rules for all Deku Tree entrances."""

    # Deku Tree Entryway to Lobby (always accessible)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_ENTRYWAY.value} -> {Regions.DEKU_TREE_LOBBY.value}", world.player).access_rule = \
        lambda state: True

    # Deku Tree Lobby to 2F Middle Room (always accessible)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_LOBBY.value} -> {Regions.DEKU_TREE_2F_MIDDLE_ROOM.value}", world.player).access_rule = \
        lambda state: True

    # Deku Tree Lobby to Compass Room (always accessible)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_LOBBY.value} -> {Regions.DEKU_TREE_COMPASS_ROOM.value}", world.player).access_rule = \
        lambda state: True

    # Deku Tree Lobby to Basement Lower (need to attack or use nuts)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_LOBBY.value} -> {Regions.DEKU_TREE_BASEMENT_LOWER.value}", world.player).access_rule = \
        lambda state: can_attack(state, world) or can_use(Items.NUTS.value, state, world)

    # Deku Tree 2F Middle Room to Lobby (need to reflect nuts or use hammer)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_2F_MIDDLE_ROOM.value} -> {Regions.DEKU_TREE_LOBBY.value}", world.player).access_rule = \
        lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world)

    # Deku Tree 2F Middle Room to Slingshot Room (need to reflect nuts or use hammer)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_2F_MIDDLE_ROOM.value} -> {Regions.DEKU_TREE_SLINGSHOT_ROOM.value}", world.player).access_rule = \
        lambda state: can_reflect_nuts(state, world) or can_use(Items.MEGATON_HAMMER.value, state, world)

    # Deku Tree Slingshot Room to 2F Middle Room (need slingshot or hover boots)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_SLINGSHOT_ROOM.value} -> {Regions.DEKU_TREE_2F_MIDDLE_ROOM.value}", world.player).access_rule = \
        lambda state: can_use(Items.FAIRY_SLINGSHOT.value, state, world) or can_use(Items.HOVER_BOOTS.value, state, world)

    # Deku Tree Compass Room to Lobby (need fire source with torch or bow)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_COMPASS_ROOM.value} -> {Regions.DEKU_TREE_LOBBY.value}", world.player).access_rule = \
        lambda state: has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)

    # Deku Tree Basement Lower to Scrub Room (need fire source with torch or bow)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_LOWER.value} -> {Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value}", world.player).access_rule = \
        lambda state: has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)

    # Deku Tree Basement Lower to Basement Upper (adult or trick)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_LOWER.value} -> {Regions.DEKU_TREE_BASEMENT_UPPER.value}", world.player).access_rule = \
        lambda state: is_adult(state, world)  # TODO: Add trick logic for RT_DEKU_B1_SKIP

    # Deku Tree Basement Scrub Room to Water Room Front (need to hit eye targets)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value} -> {Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value}", world.player).access_rule = \
        lambda state: can_hit_eye_targets(state, world)

    # Deku Tree Basement Water Room Front to Back (need bronze scale or trick)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value} -> {Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value}", world.player).access_rule = \
        lambda state: has_item(state, world, Items.BRONZE_SCALE.value)  # TODO: Add trick logic for RT_DEKU_B1_BACKFLIP_OVER_SPIKED_LOG

    # Deku Tree Basement Water Room Back to Front (need bronze scale or trick)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value} -> {Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value}", world.player).access_rule = \
        lambda state: has_item(state, world, Items.BRONZE_SCALE.value)  # TODO: Add trick logic for RT_DEKU_B1_BACKFLIP_OVER_SPIKED_LOG

    # Deku Tree Basement Water Room Back to Torch Room (always accessible)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value} -> {Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value}", world.player).access_rule = \
        lambda state: True

    # Deku Tree Basement Torch Room to Back Lobby (need fire source with torch or bow)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value} -> {Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value}", world.player).access_rule = \
        lambda state: has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)

    # Deku Tree Basement Back Lobby to Back Room (need fire source + blast or smash)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value} -> {Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value}", world.player).access_rule = \
        lambda state: (has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)) and blast_or_smash(state, world)

    # Deku Tree Basement Back Lobby to Basement Upper (need fire source + child)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value} -> {Regions.DEKU_TREE_BASEMENT_UPPER.value}", world.player).access_rule = \
        lambda state: (has_fire_source_with_torch(state, world) or can_use(Items.FAIRY_BOW.value, state, world)) and not is_adult(state, world)  # IsChild

    # Deku Tree Basement Upper to Back Lobby (child only)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_UPPER.value} -> {Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value}", world.player).access_rule = \
        lambda state: not is_adult(state, world)  # IsChild

    # Deku Tree Basement Upper to Outside Boss Room (need fire source with torch or adult bow tricks)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BASEMENT_UPPER.value} -> {Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value}", world.player).access_rule = \
        lambda state: has_fire_source_with_torch(state, world)  # TODO: Add trick logic for RT_DEKU_B1_BOW_WEBS

    # Deku Tree Outside Boss Room to Boss Entryway (need bronze scale or iron boots + reflect nuts)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value} -> {Regions.DEKU_TREE_BOSS_ENTRYWAY.value}", world.player).access_rule = \
        lambda state: (has_item(state, world, Items.BRONZE_SCALE.value) or can_use(Items.IRON_BOOTS.value, state, world)) and can_reflect_nuts(state, world)

    # Deku Tree Boss Entryway to Boss Room (always accessible)
    world.multiworld.get_entrance(f"{Regions.DEKU_TREE_BOSS_ENTRYWAY.value} -> {Regions.DEKU_TREE_BOSS_ROOM.value}", world.player).access_rule = \
        lambda state: True


def create_deku_tree_entrances(world: "SohWorld") -> None:
    """Create all Deku Tree entrances."""

    # Connect Entryway to Lobby
    world.multiworld.get_region(Regions.DEKU_TREE_ENTRYWAY.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_LOBBY.value, world.player),
        f"{Regions.DEKU_TREE_ENTRYWAY.value} -> {Regions.DEKU_TREE_LOBBY.value}"
    )

    # Connect Lobby to other rooms
    world.multiworld.get_region(Regions.DEKU_TREE_LOBBY.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_LOBBY.value} -> {Regions.DEKU_TREE_2F_MIDDLE_ROOM.value}"
    )

    world.multiworld.get_region(Regions.DEKU_TREE_LOBBY.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_COMPASS_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_LOBBY.value} -> {Regions.DEKU_TREE_COMPASS_ROOM.value}"
    )

    world.multiworld.get_region(Regions.DEKU_TREE_LOBBY.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value, world.player),
        f"{Regions.DEKU_TREE_LOBBY.value} -> {Regions.DEKU_TREE_BASEMENT_LOWER.value}"
    )

    # Connect 2F Middle Room to Slingshot Room
    world.multiworld.get_region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_LOBBY.value, world.player),
        f"{Regions.DEKU_TREE_2F_MIDDLE_ROOM.value} -> {Regions.DEKU_TREE_LOBBY.value}"
    )

    world.multiworld.get_region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_SLINGSHOT_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_2F_MIDDLE_ROOM.value} -> {Regions.DEKU_TREE_SLINGSHOT_ROOM.value}"
    )

    # Connect Slingshot Room back to 2F Middle Room
    world.multiworld.get_region(Regions.DEKU_TREE_SLINGSHOT_ROOM.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_2F_MIDDLE_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_SLINGSHOT_ROOM.value} -> {Regions.DEKU_TREE_2F_MIDDLE_ROOM.value}"
    )

    # Connect Compass Room back to Lobby
    world.multiworld.get_region(Regions.DEKU_TREE_COMPASS_ROOM.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_LOBBY.value, world.player),
        f"{Regions.DEKU_TREE_COMPASS_ROOM.value} -> {Regions.DEKU_TREE_LOBBY.value}"
    )

    # Connect Basement Lower to other basement rooms
    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_LOWER.value} -> {Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value}"
    )

    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_LOWER.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_LOWER.value} -> {Regions.DEKU_TREE_BASEMENT_UPPER.value}"
    )

    # Connect Basement Scrub Room to Water Room Front
    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_SCRUB_ROOM.value} -> {Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value}"
    )

    # Connect Water Room Front to Back (bidirectional)
    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value} -> {Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value}"
    )

    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value} -> {Regions.DEKU_TREE_BASEMENT_WATER_ROOM_FRONT.value}"
    )

    # Connect Water Room Back to Torch Room
    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_WATER_ROOM_BACK.value} -> {Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value}"
    )

    # Connect Torch Room to Back Lobby
    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_TORCH_ROOM.value} -> {Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value}"
    )

    # Connect Back Lobby to Back Room and Basement Upper
    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value} -> {Regions.DEKU_TREE_BASEMENT_BACK_ROOM.value}"
    )

    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value} -> {Regions.DEKU_TREE_BASEMENT_UPPER.value}"
    )

    # Connect Basement Upper back to Back Lobby
    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_UPPER.value} -> {Regions.DEKU_TREE_BASEMENT_BACK_LOBBY.value}"
    )

    # Connect Basement Upper to Outside Boss Room
    world.multiworld.get_region(Regions.DEKU_TREE_BASEMENT_UPPER.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_BASEMENT_UPPER.value} -> {Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value}"
    )

    # Connect Outside Boss Room to Boss Entryway
    world.multiworld.get_region(Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BOSS_ENTRYWAY.value, world.player),
        f"{Regions.DEKU_TREE_OUTSIDE_BOSS_ROOM.value} -> {Regions.DEKU_TREE_BOSS_ENTRYWAY.value}"
    )

    # Connect Boss Entryway to Boss Room
    world.multiworld.get_region(Regions.DEKU_TREE_BOSS_ENTRYWAY.value, world.player).connect(
        world.multiworld.get_region(Regions.DEKU_TREE_BOSS_ROOM.value, world.player),
        f"{Regions.DEKU_TREE_BOSS_ENTRYWAY.value} -> {Regions.DEKU_TREE_BOSS_ROOM.value}"
    )


def setup_deku_tree(world: "SohWorld") -> None:
    """Setup the complete Deku Tree dungeon."""
    create_deku_tree_regions(world)
    create_deku_tree_locations(world)
    create_deku_tree_entrances(world)
    set_deku_tree_entrance_rules(world)
    set_deku_tree_location_rules(world)
