from typing import TYPE_CHECKING

from worlds.generic.Rules import set_rule
from worlds.oot_soh.Regions import double_link_regions
from worlds.oot_soh.Items import SohItem
from worlds.oot_soh.Locations import SohLocation, SohLocationData
from worlds.oot_soh.Enums import Regions, Items, Locations, Enemies, Combat_Ranges
from worlds.oot_soh.LogicHelpers import (can_break_mud_walls, is_adult, has_explosives, can_attack, take_damage, can_shield, can_kill_enemy,
                                  has_fire_source_with_torch, can_use, can_do_trick, can_jump_slash, blast_or_smash)

if TYPE_CHECKING:
    from worlds.oot_soh import SohWorld


events: dict[str, SohLocationData] = {
    "Dodongos Cavern Lobby Switch": SohLocationData(Regions.DODONGOS_CAVERN_LOBBY_SWITCH.value,
                                                    event_item="Dodongos Cavern Lobby Switch Activated"),
    "Dodongos Cavern Far Bridge Switch": SohLocationData(Regions.DODONGOS_CAVERN_FAR_BRIDGE.value,
                                                         event_item="Dodongos Cavern Far Bridge Switch Activated"),
    "Dodongos Cavern Lower Lizalfos": SohLocationData(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS.value,
                                                      event_item="Defeated Dodongos Cavern Lower Lizalfos")
}


def create_regions_and_rules(world: "SohWorld") -> None:
    for event_name, data in events.items():
        region = world.get_region(data.region)
        region.add_event(event_name, data.event_item, location_type=SohLocation, item_type=SohItem)

    set_region_rules(world)
    set_location_rules(world)


# I'm writing this with events in mind, even though the original for this dungeon doesn't use them
# Probably will be easier that way
def set_region_rules(world: "SohWorld") -> None:
    player = world.player

    double_link_regions(world, Regions.DODONGOS_CAVERN_ENTRYWAY.value, Regions.ROOT.value)

    double_link_regions(world, Regions.DODONGOS_CAVERN_ENTRYWAY.value, Regions.DODONGOS_CAVERN_BEGINNING.value)

    # Entry to main lobby requires breaking mud walls or strength upgrade
    world.get_region(Regions.DODONGOS_CAVERN_BEGINNING.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value),
        rule=lambda state: blast_or_smash(state, world) or state.has(Items.STRENGTH_UPGRADE.value, player))

    world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BEGINNING.value))

    world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOBBY_SWITCH.value),
        rule=lambda state: is_adult(state, world))

    world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_SE_CORRIDOR.value),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has(Items.STRENGTH_UPGRADE.value, player))

    world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_STAIRS_LOWER.value),
        rule=lambda state: state.has("Dodongos Cavern Lobby Switch Activated", player))

    world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOSS_REGION.value),
        rule=lambda state: True)  # Simplified for early access

    world.get_region(Regions.DODONGOS_CAVERN_LOBBY_SWITCH.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value))

    world.get_region(Regions.DODONGOS_CAVERN_LOBBY_SWITCH.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_DODONGO_ROOM.value))

    world.get_region(Regions.DODONGOS_CAVERN_SE_CORRIDOR.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value))

    world.get_region(Regions.DODONGOS_CAVERN_SE_CORRIDOR.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_SE_ROOM.value),
        rule=lambda state: can_break_mud_walls(state, world)
        or can_attack(state, world)
        or (take_damage(state, world) and can_shield(state, world)))

    double_link_regions(world, Regions.DODONGOS_CAVERN_SE_CORRIDOR.value, Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS.value)

    world.get_region(Regions.DODONGOS_CAVERN_SE_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_SE_CORRIDOR.value))

    world.get_region(Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS.value))

    world.get_region(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_NEAR_LOWER_LIZALFOS.value),
        rule=lambda state: can_kill_enemy(state, world, Enemies.LIZALFOS.value, Combat_Ranges.CLOSE.value, quantity=2))

    world.get_region(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_DODONGO_ROOM.value),
        rule=lambda state: can_kill_enemy(state, world, Enemies.LIZALFOS.value, Combat_Ranges.CLOSE.value, quantity=2))

    world.get_region(Regions.DODONGOS_CAVERN_DODONGO_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOBBY_SWITCH.value),
        rule=lambda state: has_fire_source_with_torch(state, world))

    world.get_region(Regions.DODONGOS_CAVERN_DODONGO_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS.value))

    world.get_region(Regions.DODONGOS_CAVERN_DODONGO_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM.value),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has(Items.STRENGTH_UPGRADE.value, player))

    world.get_region(Regions.DODONGOS_CAVERN_NEAR_DODONGO_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_DODONGO_ROOM.value))

    world.get_region(Regions.DODONGOS_CAVERN_STAIRS_LOWER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value))

    world.get_region(Regions.DODONGOS_CAVERN_STAIRS_LOWER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_STAIRS_UPPER.value),
        rule=lambda state: has_explosives(state, world)
        or state.has(Items.STRENGTH_UPGRADE.value, player)
        or can_use(Items.DINS_FIRE.value, state, world)
        or (can_do_trick("DC Stairs With Bow", state, world) and can_use(Items.PROGRESSIVE_BOW.value, state, world)))

    world.get_region(Regions.DODONGOS_CAVERN_STAIRS_LOWER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_COMPASS_ROOM.value),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has(Items.STRENGTH_UPGRADE.value, player))

    world.get_region(Regions.DODONGOS_CAVERN_STAIRS_UPPER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_STAIRS_LOWER.value))

    world.get_region(Regions.DODONGOS_CAVERN_STAIRS_UPPER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_ARMOS_ROOM.value))

    world.get_region(Regions.DODONGOS_CAVERN_COMPASS_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_STAIRS_LOWER.value),
        rule=lambda state: can_use(Items.MASTER_SWORD.value, state, world)
        or can_use(Items.BIGGORONS_SWORD.value, state, world)
        or can_use(Items.MEGATON_HAMMER.value, state, world)
        or has_explosives(state, world)
        or state.has(Items.STRENGTH_UPGRADE.value, player))

    world.get_region(Regions.DODONGOS_CAVERN_ARMOS_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_STAIRS_UPPER.value))

    world.get_region(Regions.DODONGOS_CAVERN_ARMOS_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_ARMOS_ROOM.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_2F_SIDE_ROOM.value),
        rule=lambda state: can_break_mud_walls(state, world)
        or (can_do_trick("DC Scrub Room", state, world) and state.has(Items.STRENGTH_UPGRADE.value, player)))

    world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM.value),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has(Items.STRENGTH_UPGRADE.value, player))

    world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER.value),
        rule=lambda state: (is_adult(state, world) and can_do_trick("DC Jump", state, world))
        or can_use(Items.HOVER_BOOTS.value, state, world)
        or (is_adult(state, world) and can_use(Items.PROGRESSIVE_HOOKSHOT.value, state, world))
        or (can_do_trick("Damage Boost Simple", state, world) and has_explosives(state, world)
            and can_jump_slash(state, world)))

    world.get_region(Regions.DODONGOS_CAVERN_2F_SIDE_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value))

    world.get_region(Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value))

    world.get_region(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value),
        rule=lambda state: can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world)
        or can_use(Items.PROGRESSIVE_BOW.value, state, world)
        or can_do_trick("DC Slingshot Skip", state, world))

    world.get_region(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOWER_LIZALFOS.value))

    world.get_region(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_FIRST_SLINGSHOT_ROOM.value),
        rule=lambda state: state.has("Defeated Dodongos Cavern Lower Lizalfos", player))

    world.get_region(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM.value),
        rule=lambda state: state.has("Defeated Dodongos Cavern Lower Lizalfos", player))

    world.get_region(Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_UPPER_LIZALFOS.value))

    world.get_region(Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER.value),
        rule=lambda state: can_use(Items.PROGRESSIVE_SLINGSHOT.value, state, world)
        or can_use(Items.PROGRESSIVE_BOW.value, state, world)
        or can_do_trick("DC Slingshot Skip", state, world))

    world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_LOWER.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_SECOND_SLINGSHOT_ROOM.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_FAR_BRIDGE.value))

    world.get_region(Regions.DODONGOS_CAVERN_FAR_BRIDGE.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOMB_ROOM_UPPER.value))

    world.get_region(Regions.DODONGOS_CAVERN_FAR_BRIDGE.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOSS_REGION.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_LOBBY.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOSS_REGION.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BACK_ROOM.value),
        rule=lambda state: can_break_mud_walls(state, world))

    world.get_region(Regions.DODONGOS_CAVERN_BOSS_REGION.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOSS_REGION.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOSS_ROOM.value))

    world.get_region(Regions.DODONGOS_CAVERN_BOSS_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOSS_ENTRYWAY.value))

    world.get_region(Regions.DODONGOS_CAVERN_BACK_ROOM.value).connect(
        world.get_region(Regions.DODONGOS_CAVERN_BOSS_REGION.value))


def set_location_rules(world: "SohWorld") -> None:
    player = world.player

    set_rule(world.get_location(Locations.DODONGOS_CAVERN_MAP_CHEST.value),
             rule=lambda state: can_break_mud_walls(state, world)
             or state.has(Items.STRENGTH_UPGRADE.value, player))

    set_rule(world.get_location(Locations.DODONGOS_CAVERN_END_OF_BRIDGE_CHEST.value),
             rule=lambda state: can_break_mud_walls(state, world))

    set_rule(world.get_location("Dodongos Cavern Lower Lizalfos"),
             rule=lambda state: can_kill_enemy(state, world, Enemies.LIZALFOS.value, Combat_Ranges.CLOSE.value, quantity=2))
