from BaseClasses import MultiWorld, CollectionState, Location, Entrance
# from typing import List
from worlds.generic.Rules import set_rule, add_rule
from .Locations import orderedstage_location
from .RoR2Environments import environment_vanilla_orderedstages_table, environment_sotv_orderedstages_table, \
    environment_vanilla_hidden_realm_table, environment_vanilla_special_table


# Does the entrance have the environment?
# Doesn't work with multiple yamls
def has_item_access_rule(multiworld: MultiWorld, entrance, environment: str, player: int):
    region = multiworld.get_region(entrance, player)
    print(entrance, environment)
    entrance = Entrance(player, f"{entrance} to {environment}", region).access_rule = \
        lambda state: state.has(environment, player)
    # multiworld.get_entrance(f"{entrance} to {environment}", player).access_rule = \
    #     lambda state: state.has(environment, player)


# Rule to see if it has access to the previous stage
# Doesn't work with multiple yamls
def has_entrance_access_rule(multiworld: MultiWorld, entrance: str, stage: str, player: int):
    region = multiworld.get_region(entrance, player)
    world = Entrance(player, entrance, region)
    world.access_rule = \
        lambda state: state.has(entrance, player) and state.has(stage, player)


# Checks to see if previous chest/shrine is accessible
def has_location_access_rule(multiworld: MultiWorld, environment: str, player: int, item_number: int, item_type: str):
    multiworld.get_location(f"{environment}: {item_type} {item_number}", player).access_rule = \
        lambda state: state.has(environment, player)


def check_location(state, environment: str, player: int, item_number: int, item_name: str):
    return state.can_reach(f"{environment}: {item_name} {item_number - 1}", "Location", player)


# unlock event to next set of stages
def get_stage_event(multiworld: MultiWorld, stage: str, environment: str, player: int, chests: int):
    multiworld.get_location(stage, player).access_rule = \
        lambda state: state.can_reach(f"{environment}: Chest {chests}", "Location", player)
    multiworld.get_location(f"{environment}: Chest {chests}", player).access_rule = \
        lambda state: state.has(stage, player)


def set_rules(world: MultiWorld, player: int) -> None:

    if (world.goal[player] == "classic"):
        # classic mode
        total_locations = world.total_locations[player].value  # total locations for current player
    else:
        # explore mode
        total_locations = len(
            orderedstage_location.get_locations(
                chests=world.chests_per_stage[player].value,
                shrines=world.shrines_per_stage[player].value,
                scavengers=world.scavengers_per_stage[player].value,
                scanners=world.scanner_per_stage[player].value,
                altars=world.altars_per_stage[player].value,
                dlc_sotv=world.dlc_sotv[player].value
            )
        )

    event_location_step = 25  # set an event location at these locations for "spheres"
    divisions = total_locations // event_location_step
    total_revivals = world.worlds[player].total_revivals  # pulling this info we calculated in generate_basic


    if (world.goal[player] == "classic"):
        # classic mode
        if divisions:
            for i in range(1, divisions):  # since divisions is the floor of total_locations / 25
                event_loc = world.get_location(f"Pickup{i * event_location_step}", player)
                set_rule(event_loc,
                        lambda state, i=i: state.can_reach(f"ItemPickup{i * event_location_step - 1}", "Location", player))
                for n in range(i * event_location_step, (i + 1) * event_location_step):  # we want to create a rule for each of the 25 locations per division
                    if n == i * event_location_step:
                        set_rule(world.get_location(f"ItemPickup{n}", player),
                                lambda state, event_item=event_loc.item.name: state.has(event_item, player))
                    else:
                        set_rule(world.get_location(f"ItemPickup{n}", player),
                                lambda state, n=n: state.can_reach(f"ItemPickup{n - 1}", "Location", player))
            for i in range(divisions * event_location_step, total_locations+1):
                set_rule(world.get_location(f"ItemPickup{i}", player),
                        lambda state, i=i: state.can_reach(f"ItemPickup{i - 1}", "Location", player))
        set_rule(world.get_location("Victory", player),
                lambda state: state.can_reach(f"ItemPickup{total_locations}", "Location", player))
        if total_revivals or world.start_with_revive[player].value:
            add_rule(world.get_location("Victory", player),
                    lambda state: state.has("Dio's Best Friend", player,
                                            total_revivals + world.start_with_revive[player]))

    elif (world.environments_as_items[player].value):
        # When explore_mode and environments_as_items are used,
        #   scavengers need to be locked till after a full loop since that is when they are capable of spawning.
        # (While technically the requirement is just beating 5 stages, this will ensure that the player will have
        #   a long enough run to have enough director credits for scavengers and help prevent being stuck in the same stages until that point.)

        # Logic needs to get added if starting with loop so everything doesn't get dumped into sphere 1
        if world.begin_with_loop[player]:
            print("something needs to go here")
        for location in world.get_locations():
            if location.player != player: continue # ignore all checks that don't belong to this player
            # if ("Scavenger" in location.name):
            #     add_rule(location, lambda state: state.has("OrderedStage_5", player))
    # Regions
        chests = world.chests_per_stage[player]
        shrines = world.shrines_per_stage[player]
        newt = world.altars_per_stage[player]
        scavengers = world.scavengers_per_stage[player]
        scanners = world.scanner_per_stage[player]
        for i in range(len(environment_vanilla_orderedstages_table)):
            for environment_name, _ in environment_vanilla_orderedstages_table[i].items():
                # Make sure to go through each location
                # world.get_location(f"{environment_name}: Chest 1", player).access_rule = \
                #     lambda state: state.has(environment_name, player)
                # world.get_location(f"{environment_name}: Shrine 1", player).access_rule = \
                #     lambda state: state.has(environment_name, player)
                if world.scavengers_per_stage[player]:
                    has_location_access_rule(world, environment_name, player, scavengers, "Scavenger")
                if world.scanner_per_stage[player]:
                    has_location_access_rule(world, environment_name, player, scanners, "Radio Scanner")
                if world.altars_per_stage[player]:
                    world.get_location(f"{environment_name}: Newt Altar 1", player).access_rule = \
                        lambda state: state.has(environment_name, player)
                for chest in range(1, chests + 1):
                    has_location_access_rule(world, environment_name, player, chest, "Chest")
                for shrine in range(1, shrines + 1):
                    has_location_access_rule(world, environment_name, player, shrine, "Shrine")
                if newt > 1:
                    has_location_access_rule(world, environment_name, player, newt, "Newt Altar")
                # if i == 0:
                    # Make sure to have the item to enter environment
                    # print('a')
                    # has_item_access_rule(world, "Menu", environment_name, player)
                # else:
                    # has_item_access_rule(world, f"OrderedStage_{i}", environment_name, player)
                    # Make sure to have the entrance to enter an environment
                    # has_entrance_access_rule(world, f"OrderedStage_{i}", environment_name, player)
                get_stage_event(world, f"OrderedStage_{i + 1}", environment_name, player, chests)
            # world.get_entrance("Sky Meadow to Hidden Realm: Bulwark's Ambry", player).access_rule = \
            #     lambda state: state.has("Hidden Realm: Bulwark's Ambry", player)
            # world.get_entrance("OrderedStage_5 to Hidden Realm: A Moment, Fractured", player).access_rule = \
            #     lambda state: state.has("Hidden Realm: A Moment, Fractured", player)
            # world.get_entrance("Hidden Realm: A Moment, Fractured to Hidden Realm: A Moment, Whole", player).access_rule = \
            #     lambda state: state.has("Hidden Realm: A Moment, Whole", player)
            # world.get_entrance("OrderedStage_1 to Hidden Realm: Gilded Coast", player).access_rule = \
            #     lambda state: state.has("Hidden Realm: Gilded Coast", player)
            # world.get_entrance("OrderedStage_1 to Hidden Realm: Bazaar Between Time", player).access_rule = \
            #     lambda state: state.has("Hidden Realm: Bazaar Between Time", player)
            # world.get_entrance("OrderedStage_5 to Commencement", player).access_rule = \
            #     lambda state: state.has("Commencement", player)
            # world.get_entrance("OrderedStage_5 to Commencement", player).access_rule = \
            #     lambda state: state.has("Sky Meadow", player)
            # world.get_entrance("Hidden Realm: Bulwark's Ambry to Void Fields", player).access_rule = \
            #     lambda state: state.has("Void Fields", player)
            # has_item_access_rule(world, f"OrderedStage_5", "Commencement", player)
            # has_item_access_rule(world, f"OrderedStage_5", "Hidden Realm: A Moment, Fractured", player)
    # Win Condition
    world.completion_condition[player] = lambda state: state.has("Victory", player)
