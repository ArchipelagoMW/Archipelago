from __future__ import annotations

from typing import TYPE_CHECKING, List

# TODO: Fix reference. Doesn't work with AP Launcher
#from flask_caching import logger

from worlds.generic.Rules import set_rule

from .rezdata.ships import ship_table 
from .apdata.offsets import offsets_table as loc_type_offset
from .logics import possible_regions

if TYPE_CHECKING:
    from .world import EVNWorld

def _ship_id_rule(ship_id: int) -> str:
    # NOTE: WARNING - we can't import the item bank. I don't recall why... Maybe it wasn't created yet?
    #   The result is that we have to recreate the index ID ourselves.
    #   I don't like that. If it changes in items, it could break this!
    # NOTE: This references the item *name*, not ID later.
    ship_data = ship_table[ship_id]
    return ship_data["name"].strip() + ship_data["id"]

def _min_cargo_rule(min_weight: int) -> List[str]:
    ship_offset = loc_type_offset["ship"]
    core_list = []
    for ship_id, ship_data in ship_table.items():
        ship_cargo = ship_data["cargo"]
        if int(ship_cargo) >= min_weight:
            core_list.append(ship_data["name"].strip() + ship_data["id"])
    return core_list

def _min_ship_str_rule(min_str: int) -> List[str]:
    ship_offset = loc_type_offset["ship"]
    core_list = []
    for ship_id, ship_data in ship_table.items():
        ship_stat = ship_data["strength"]
        if int(ship_stat) >= min_str:
            #logger.info(f"Ship str rule, adding {min_str}, {ship_stat}, {ship_data['id']}")
            core_list.append(ship_data["name"].strip() + ship_data["id"])
    return core_list


def set_all_rules(world: EVNWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # NOTE: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: EVNWorld) -> None:
    # Review apquest's rules file for good info on designing this section.

    # Get our story string logic
    # Look at "region_connections". Format: "from_region_id", ["to_region_ids"]
    chosen_route = world.get_chosen_string()
    for from_id, to_regions in chosen_route["region_connections"].items():
        from_region = possible_regions[from_id]
        for to_id in to_regions:
            to_region = possible_regions[to_id]
            # Give ourselves a name we can understand about the objects and relation
            entrance_name = f"{from_region['name']} to {to_region['name']}"
            # Helper method for grabbing entrances
            region_entrance = world.get_entrance(entrance_name)
            # Review the type of entrance rule we described in logics
            # and apply that here.
            # Essentially, our rules will filter for a set of ships / outfits that meet the
            # described rule req in logics, and return that filtered list, where
            # the entrance rule will see if we have any of those filtered qualifying items.
            for rule_type, rule_value in to_region["entrance_rules"].items():
                match rule_type:
                    case "ship":
                        temp_ship_id = _ship_id_rule(rule_value)
                        #logger.info(f"Ship rule for: {temp_ship_id}")
                        # state.has wants name, not id
                        set_rule(region_entrance, lambda state: state.has(temp_ship_id, world.player))
                    case "min_cargo":
                        temp_list = _min_cargo_rule(rule_value)
                        set_rule(region_entrance, lambda state: state.has_any(temp_list, world.player))
                    case "min_ship_str": # Note: Ship str is arbitrary number designers added, but fits our purposes well enough here
                        temp_list = _min_ship_str_rule(rule_value)
                        set_rule(region_entrance, lambda state: state.has_any(temp_list, world.player))
                    #case "min_checks":
                        # apparently this doesn't update how we would expect. Advice was to not use it.
                        # set_rule(region_entrance, lambda state: len(state.locations_checked))
                        # I don't want to recreate a list of all possible checks, but I can't import the item library either due to cross ref imports
                        # set_rule(region_entrance, lambda state: state.has_from_list_unique(temp_list, world.player))
                    #case _:
                        # do nothing


def set_all_location_rules(world: EVNWorld) -> None:
    # NOTE: I'll have to care for missions that can't be repeated. 
    # Ex: the first tutorial mission - if you say "no" to accepting it, you can't get it later without making a new pilot file.

    # Currently, we only have one event that we need to set - the victory event
    # So we do that here.    
    chosen_route = world.get_chosen_string()
    misn_offset = loc_type_offset["misn"]
    loc_name = world.location_id_to_name[chosen_route["final_mission"] + misn_offset] # Do we not have a helper function for this?
    world.multiworld.get_location(loc_name, world.player).place_locked_item(world.create_item("Victory"))

    # We don't really have any other location events or specific rules. Those were handled by the entrances.
    # Again, check exerpts from apquest. It directly discusses what I mean about entrance vs location rules.

    # Possible idea on additional rules that would help us create more spheres of logic in gen'ed APs:
    # ADDING STRING PROGRESS CONDITION for the sake of creating another logic sphere level:
    # the idea being that there would be one or two progress check items that would be given out by story
    # but that we could check against in logic, allowing us to get sphere 3 for example.
    # the item would be invisible to the user.
    # The item would be added to the pool, and then manually place here based on the region entrance rule or something...
    #   looping through here like in the above function.
    # BUT! We don't want to replace the actual check of a mission.
    # I think the way we get around that is to maybe have the mission fire off a chron
    # that completes a hidden mission that awards the item.
    # The hidden mission is what we assign to here. We can't just bit logic give the item because then the 
    # server logic won't know about where the item is assigned and thus wouldn't give a new sphere.


def set_completion_condition(world: EVNWorld) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    #world.multiworld.completion_condition[world.player] = lambda state: state.has_all(("Starbridge"), world.player)

    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets instead set the completion condition to:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)