from typing import TYPE_CHECKING

from BaseClasses import Region
from .Rules import access_rules_dict, interpret_rule

from ..generic.Rules import add_rule

if TYPE_CHECKING:

    from . import GrinchWorld

mainareas_list = [
    "Whoville",
    "Who Forest",
    "Who Dump",
    "Who Lake"
]

subareas_list = [
    "Post Office",
    "City Hall",
    "Countdown to X-Mas Tower",
    "Ski Resort",
    "Civic Center",
    "Minefield",
    "Power Plant",
    "Generator Building",
    "Submarine World",
    "Scout's Hut",
    "North Shore",
    "Mayor's Villa",
    "Sleigh Room"
]

supadow_list = [
    "Spin N' Win Supadow",
    "Dankamania Supadow",
    "The Copter Race Contest Supadow",
    "Bike Race"
]

def create_regions(world: "GrinchWorld"):
    for mainarea in mainareas_list:
        #Each area in mainarea, create a region for the given player
        world.multiworld.regions.append(Region(mainarea, world.player, world.multiworld))
    for subarea in subareas_list:
        #Each area in subarea, create a region for the given player
        world.multiworld.regions.append(Region(subarea, world.player, world.multiworld))
    for supadow in supadow_list:
        #Each area in supadow, create a region for the given player
        world.multiworld.regions.append(Region(supadow, world.player, world.multiworld))

# TODO Optimize this function
def grinchconnect(world: "GrinchWorld", current_region_name: str, connected_region_name: str):
    current_region = world.get_region(current_region_name)
    connected_region = world.get_region(connected_region_name)
    required_items: list[list[str]] = access_rules_dict[connected_region.name]
    rule_list = interpret_rule(required_items, world.player)
    # Goes from current to connected
    current_region.connect(connected_region)
    # Goes from connected to current
    connected_region.connect(current_region)
    for access_rule in rule_list:
        for region_entrance in current_region.entrances:
            if region_entrance.connected_region.name == current_region_name and \
                region_entrance.parent_region.name == connected_region_name:
                if rule_list.index(access_rule) == 0:
                    add_rule(region_entrance, access_rule)
                else:
                    add_rule(region_entrance, access_rule, combine="or")
        for region_entrance in connected_region.entrances:
            if region_entrance.connected_region.name == connected_region_name and \
                    region_entrance.parent_region.name == current_region_name:
                if rule_list.index(access_rule) == 0:
                    add_rule(region_entrance, access_rule)
                else:
                    add_rule(region_entrance, access_rule, combine="or")

#What regions are connected to each other
def connect_regions(world: "GrinchWorld"):
    grinchconnect(world, "Mount Crumpit", "Whoville")
    grinchconnect(world, "Mount Crumpit", "Who Forest")
    grinchconnect(world, "Mount Crumpit", "Who Dump")
    grinchconnect(world, "Mount Crumpit", "Who Lake")
    grinchconnect(world, "Mount Crumpit", "Sleigh Room")
    grinchconnect(world, "Mount Crumpit", "Spin N' Win Supadow")
    grinchconnect(world, "Mount Crumpit", "Dankamania Supadow")
    grinchconnect(world, "Mount Crumpit", "The Copter Race Contest Supadow")
    grinchconnect(world, "Whoville", "Post Office")
    grinchconnect(world, "Whoville", "City Hall")
    grinchconnect(world, "Whoville", "Countdown to X-Mas Clock Tower")
    grinchconnect(world, "Who Forest", "Ski Resort")
    grinchconnect(world, "Who Forest", "Civic Center")
    grinchconnect(world, "Who Dump", "Minefield")
    grinchconnect(world, "Who Dump", "Power Plant")
    grinchconnect(world, "Power Plant", "Generator Building")
    grinchconnect(world, "Who Lake", "Submarine World")
    grinchconnect(world, "Who Lake", "Scout's Hut")
    grinchconnect(world, "Who Lake", "North Shore")
    grinchconnect(world, "North Shore", "Mayor's Villa")
    grinchconnect(world, "Sleigh Room", "Bike Race")
