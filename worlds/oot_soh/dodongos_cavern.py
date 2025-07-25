from typing import TYPE_CHECKING

from BaseClasses import Region
from worlds.generic.Rules import set_rule

from .Items import SohItem
from .Locations import SohLocation, SohLocationData, base_location_table
from .Rules import (can_break_mud_walls, is_adult, has_explosives, can_attack, take_damage, can_shield, can_kill_enemy,
                    has_fire_source_with_torch, can_use, can_do_trick, can_jump_slash)

if TYPE_CHECKING:
    from . import SohWorld


# when python 3.10 and 3.11 are dropped, this should just become a StrEnum to make it easier
dc_region_names: list[str] = [
    "Dodongos Cavern Beginning",
    "Dodongos Cavern Lobby",
    "Dodongos Cavern Lobby Switch",
    "Dodongos Cavern SE Corridor",
    "Dodongos Cavern SE Room",
    "Dodongos Cavern Near Lower Lizalfos",
    "Dodongos Cavern Lower Lizalfos",
    "Dodongos Cavern Dodongo Room",
    "Dodongos Cavern Near Dodongo Room",
    "Dodongos Cavern Stairs Lower",
    "Dodongos Cavern Stairs Upper",
    "Dodongos Cavern Compass Room",
    "Dodongos Cavern Armos Room",
    "Dodongos Cavern Bomb Room Lower",
    "Dodongos Cavern 2F Side Room",
    "Dodongos Cavern First Slingshot Room",
    "Dodongos Cavern Upper Lizalfos",
    "Dodongos Cavern Second Slingshot Room",
    "Dodongos Cavern Bomb Room Upper",
    "Dodongos Cavern Far Bridge",
    "Dodongos Cavern Boss Region",
    "Dodongos Cavern Back Room",
    "Dodongos Cavern Boss Entryway",
]


dc_events: dict[str, SohLocationData] = {
    "Dodongos Cavern Lobby Switch": SohLocationData("Dodongos Cavern Lobby Switch",
                                                    event_item="Dodongos Cavern Lobby Switch Activated"),
    "Dodongos Cavern Far Bridge Switch": SohLocationData("Dodongos Cavern Far Bridge",
                                                         event_item="Dodongos Cavern Far Bridge Switch Activated"),
    "Dodongos Cavern Lower Lizalfos": SohLocationData("Dodongos Cavern Lower Lizalfos",
                                                      event_item="Defeated Dodongos Cavern Lower Lizalfos")
}


def create_dc_regions_and_rules(world: "SohWorld") -> None:
    for region_name in dc_region_names:
        region = Region(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)
        region.add_locations({loc_name: loc_data.address for loc_name, loc_data in base_location_table.items()
                              if loc_data.region == region_name}, SohLocation)

    for event_name, data in dc_events.items():
        region = world.get_region(data.region)
        region.add_event(event_name, data.event_item, location_type=SohLocation, item_type=SohItem)

    set_region_rules_dc(world)
    set_location_rules_dc(world)


# I'm writing this with events in mind, even though the original for this dungeon doesn't use them
# Probably will be easier that way
def set_region_rules_dc(world: "SohWorld") -> None:
    player = world.player

    world.get_region("Dodongos Cavern Entryway").connect(
        world.get_region("Dodongos Cavern Beginning"))

    world.get_region("Dodongos Cavern Beginning").connect(
        world.get_region("Dodongos Cavern Entryway"))

    world.get_region("Dodongos Cavern Beginning").connect(
        world.get_region("Dodongos Cavern Lobby"),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has("Strength Upgrade", player))

    world.get_region("Dodongos Cavern Lobby").connect(
        world.get_region("Dodongos Cavern Beginning"))

    world.get_region("Dodongos Cavern Lobby").connect(
        world.get_region("Dodongos Cavern Lobby Switch"),
        rule=lambda state: is_adult(state, world))

    world.get_region("Dodongos Cavern Lobby").connect(
        world.get_region("Dodongos Cavern SE Corridor"),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has("Strength Upgrade", player))

    world.get_region("Dodongos Cavern Lobby").connect(
        world.get_region("Dodongos Cavern Stairs Lower"),
        rule=lambda state: state.has("Dodongos Cavern Lobby Switch Activated", player))

    world.get_region("Dodongos Cavern Lobby").connect(
        world.get_region("Dodongos Cavern Boss Region"),
        rule=lambda state: state.has("Dodongos Cavern Far Bridge Switch Activated", player)
        and has_explosives(state, world))

    world.get_region("Dodongos Cavern Lobby Switch").connect(
        world.get_region("Dodongos Cavern Lobby"))

    world.get_region("Dodongos Cavern Lobby Switch").connect(
        world.get_region("Dodongos Cavern Dodongo Room"))

    world.get_region("Dodongos Cavern SE Corridor").connect(
        world.get_region("Dodongos Cavern Lobby"))

    world.get_region("Dodongos Cavern SE Corridor").connect(
        world.get_region("Dodongos Cavern SE Room"),
        rule=lambda state: can_break_mud_walls(state, world)
        or can_attack(state, world)
        or (take_damage(state, world) and can_shield(state, world)))

    world.get_region("Dodongos Cavern SE Corridor").connect(
        world.get_region("Dodongos Cavern Near Lower Lizalfos"))

    world.get_region("Dodongos Cavern SE Room").connect(
        world.get_region("Dodongos Cavern SE Corridor"))

    world.get_region("Dodongos Cavern Near Lower Lizalfos").connect(
        world.get_region("Dodongos Cavern SE Corridor"))

    world.get_region("Dodongos Cavern Near Lower Lizalfos").connect(
        world.get_region("Dodongos Cavern Lower Lizalfos"))

    world.get_region("Dodongos Cavern Lower Lizalfos").connect(
        world.get_region("Dodongos Cavern Near Lower Lizalfos"),
        rule=lambda state: can_kill_enemy(state, world, "Lizalfos", 0, quantity=2))

    world.get_region("Dodongos Cavern Lower Lizalfos").connect(
        world.get_region("Dodongos Cavern Dodongo Room"),
        rule=lambda state: can_kill_enemy(state, world, "Lizalfos", 0, quantity=2))

    world.get_region("Dodongos Cavern Dodongo Room").connect(
        world.get_region("Dodongos Cavern Lobby Switch"),
        rule=lambda state: has_fire_source_with_torch(state, world))

    world.get_region("Dodongos Cavern Dodongo Room").connect(
        world.get_region("Dodongos Cavern Lower Lizalfos"))

    world.get_region("Dodongos Cavern Dodongo Room").connect(
        world.get_region("Dodongos Cavern Near Dodongo Room"),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has("Strength Upgrade", player))

    world.get_region("Dodongos Cavern Near Dodongo Room").connect(
        world.get_region("Dodongos Cavern Dodongo Room"))

    world.get_region("Dodongos Cavern Stairs Lower").connect(
        world.get_region("Dodongos Cavern Lobby"))

    world.get_region("Dodongos Cavern Stairs Lower").connect(
        world.get_region("Dodongos Cavern Stairs Upper"),
        rule=lambda state: has_explosives(state, world)
        or state.has("Strength Upgrade", player)
        or can_use("Din's Fire", state, world)
        or (can_do_trick("DC Stairs With Bow", state, world) and can_use("Fairy Bow", state, world)))

    world.get_region("Dodongos Cavern Stairs Lower").connect(
        world.get_region("Dodongos Cavern Compass Room"),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has("Strength Upgrade", player))

    world.get_region("Dodongos Cavern Stairs Upper").connect(
        world.get_region("Dodongos Cavern Stairs Lower"))

    world.get_region("Dodongos Cavern Stairs Upper").connect(
        world.get_region("Dodongos Cavern Armos Room"))

    world.get_region("Dodongos Cavern Compass Room").connect(
        world.get_region("Dodongos Cavern Stairs Lower"),
        rule=lambda state: can_use("Master Sword", state, world)
        or can_use("Biggoron Sword", state, world)
        or can_use("Megaton Hammer", state, world)
        or has_explosives(state, world)
        or state.has("Strength Upgrade", player))

    world.get_region("Dodongos Cavern Armos Room").connect(
        world.get_region("Dodongos Cavern Stairs Upper"))

    world.get_region("Dodongos Cavern Armos Room").connect(
        world.get_region("Dodongos Cavern Bomb Room Lower"))

    world.get_region("Dodongos Cavern Bomb Room Lower").connect(
        world.get_region("Dodongos Cavern Armos Room"))

    world.get_region("Dodongos Cavern Bomb Room Lower").connect(
        world.get_region("Dodongos Cavern 2F Side Room"),
        rule=lambda state: can_break_mud_walls(state, world)
        or (can_do_trick("DC Scrub Room", state, world) and state.has("Strength Upgrade", player)))

    world.get_region("Dodongos Cavern Bomb Room Lower").connect(
        world.get_region("Dodongos Cavern First Slingshot Room"),
        rule=lambda state: can_break_mud_walls(state, world)
        or state.has("Strength Upgrade", player))

    world.get_region("Dodongos Cavern Bomb Room Lower").connect(
        world.get_region("Dodongos Cavern Bomb Room Upper"),
        rule=lambda state: (is_adult(state, world) and can_do_trick("DC Jump", state, world))
        or can_use("Hover Boots", state, world)
        or (is_adult(state, world) and can_use("Longshot", state, world))
        or (can_do_trick("Damage Boost Simple", state, world) and has_explosives(state, world)
            and can_jump_slash(state, world)))

    world.get_region("Dodongos Cavern 2F Side Room").connect(
        world.get_region("Dodongos Cavern Bomb Room Lower"))

    world.get_region("Dodongos Cavern First Slingshot Room").connect(
        world.get_region("Dodongos Cavern Bomb Room Lower"))

    world.get_region("Dodongos Cavern Upper Lizalfos").connect(
        world.get_region("Dodongos Cavern Bomb Room Lower"),
        rule=lambda state: can_use("Fairy Slingshot", state, world)
        or can_use("Fairy Bow", state, world)
        or can_do_trick("DC Slingshot Skip", state, world))

    world.get_region("Dodongos Cavern Upper Lizalfos").connect(
        world.get_region("Dodongos Cavern Lower Lizalfos"))

    world.get_region("Dodongos Cavern Upper Lizalfos").connect(
        world.get_region("Dodongos Cavern First Slingshot Room"),
        rule=lambda state: state.has("Defeated Dodongos Cavern Lower Lizalfos", player))

    world.get_region("Dodongos Cavern Upper Lizalfos").connect(
        world.get_region("Dodongos Cavern Second Slingshot Room"),
        rule=lambda state: state.has("Defeated Dodongos Cavern Lower Lizalfos", player))

    world.get_region("Dodongos Cavern Second Slingshot Room").connect(
        world.get_region("Dodongos Cavern Upper Lizalfos"))

    world.get_region("Dodongos Cavern Second Slingshot Room").connect(
        world.get_region("Dodongos Cavern Bomb Room Upper"),
        rule=lambda state: can_use("Fairy Slingshot", state, world)
        or can_use("Fairy Bow", state, world)
        or can_do_trick("DC Slingshot Skip", state, world))

    world.get_region("Dodongos Cavern Bomb Room Upper").connect(
        world.get_region("Dodongos Cavern Bomb Room Lower"))

    world.get_region("Dodongos Cavern Bomb Room Upper").connect(
        world.get_region("Dodongos Cavern Second Slingshot Room"))

    world.get_region("Dodongos Cavern Bomb Room Upper").connect(
        world.get_region("Dodongos Cavern Far Bridge"))

    world.get_region("Dodongos Cavern Far Bridge").connect(
        world.get_region("Dodongos Cavern Lobby"))

    world.get_region("Dodongos Cavern Far Bridge").connect(
        world.get_region("Dodongos Cavern Bomb Room Upper"))

    world.get_region("Dodongos Cavern Boss Region").connect(
        world.get_region("Dodongos Cavern Lobby"))

    world.get_region("Dodongos Cavern Boss Region").connect(
        world.get_region("Dodongos Cavern Back Room"),
        rule=lambda state: can_break_mud_walls(state, world))

    world.get_region("Dodongos Cavern Boss Region").connect(
        world.get_region("Dodongos Cavern Boss Entryway"))

    world.get_region("Dodongos Cavern Back Room").connect(
        world.get_region("Dodongos Cavern Boss Region"))


def set_location_rules_dc(world: "SohWorld") -> None:
    player = world.player

    set_rule(world.get_location("Dodongos Cavern Map Chest"),
             rule=lambda state: can_break_mud_walls(state, world)
             or state.has("Strength Upgrade", player))

    set_rule(world.get_location("Dodongos Cavern End Of Bridge Chest"),
             rule=lambda state: can_break_mud_walls(state, world))

    set_rule(world.get_location("Dodongos Cavern Lower Lizalfos"),
             rule=lambda state: can_kill_enemy(state, world, "Lizalfos", 0, quantity=2))
