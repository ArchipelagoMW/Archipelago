from BaseClasses import MultiWorld, CollectionState
from worlds.generic.Rules import set_rule, add_rule
from .Locations import orderedstage_location
from .RoR2Environments import environment_vanilla_orderedstages_table, environment_sotv_orderedstages_table, \
    environment_orderedstages_table


# Rule to see if it has access to the previous stage
def has_entrance_access_rule(multiworld: MultiWorld, stage: str, entrance: str, player: int):
    multiworld.get_entrance(entrance, player).access_rule = \
        lambda state: state.has(entrance, player) and state.has(stage, player)


# Checks to see if chest/shrine are accessible
def has_location_access_rule(multiworld: MultiWorld, environment: str, player: int, item_number: int, item_type: str):
    if item_number == 1:
        multiworld.get_location(f"{environment}: {item_type} {item_number}", player).access_rule = \
            lambda state: state.has(environment, player)
        if item_type == "Scavenger":
            multiworld.get_location(f"{environment}: {item_type} {item_number}", player).access_rule = \
                lambda state: state.has(environment, player) and state.has("Stage_4", player)
    else:
        multiworld.get_location(f"{environment}: {item_type} {item_number}", player).access_rule = \
            lambda state: check_location(state, environment, player, item_number, item_type)


def check_location(state, environment: str, player: int, item_number: int, item_name: str):
    return state.can_reach(f"{environment}: {item_name} {item_number - 1}", "Location", player)


# unlock event to next set of stages
def get_stage_event(multiworld: MultiWorld, player: int, stage_number: int):
    if not multiworld.dlc_sotv[player]:
        environment_name = multiworld.random.choices(list(environment_vanilla_orderedstages_table[stage_number].keys()),
                                                     k=1)
    else:
        environment_name = multiworld.random.choices(list(environment_orderedstages_table[stage_number].keys()), k=1)
    multiworld.get_location(f"Stage_{stage_number + 1}", player).access_rule = \
        lambda state: get_one_of_the_stages(state, environment_name[0], player)


def get_one_of_the_stages(state: CollectionState, stage: str, player: int):
    return state.has(stage, player)


def set_rules(multiworld: MultiWorld, player: int) -> None:
    if multiworld.goal[player] == "classic":
        # classic mode
        total_locations = multiworld.total_locations[player].value  # total locations for current player
    else:
        # explore mode
        total_locations = len(
            orderedstage_location.get_locations(
                chests=multiworld.chests_per_stage[player].value,
                shrines=multiworld.shrines_per_stage[player].value,
                scavengers=multiworld.scavengers_per_stage[player].value,
                scanners=multiworld.scanner_per_stage[player].value,
                altars=multiworld.altars_per_stage[player].value,
                dlc_sotv=multiworld.dlc_sotv[player].value
            )
        )

    event_location_step = 25  # set an event location at these locations for "spheres"
    divisions = total_locations // event_location_step
    total_revivals = multiworld.worlds[player].total_revivals  # pulling this info we calculated in generate_basic

    if multiworld.goal[player] == "classic":
        # classic mode
        if divisions:
            for i in range(1, divisions + 1):  # since divisions is the floor of total_locations / 25
                if i * event_location_step != total_locations:
                    event_loc = multiworld.get_location(f"Pickup{i * event_location_step}", player)
                    set_rule(event_loc,
                            lambda state, i=i: state.can_reach(f"ItemPickup{i * event_location_step - 1}", "Location", player))
                    # we want to create a rule for each of the 25 locations per division
                for n in range(i * event_location_step, (i + 1) * event_location_step + 1):
                    if n > total_locations:
                        break
                    if n == i * event_location_step:
                        set_rule(multiworld.get_location(f"ItemPickup{n}", player),
                                 lambda state, event_item=event_loc.item.name: state.has(event_item, player))
                    else:
                        set_rule(multiworld.get_location(f"ItemPickup{n}", player),
                                 lambda state, n=n: state.can_reach(f"ItemPickup{n - 1}", "Location", player))
        set_rule(multiworld.get_location("Victory", player),
                 lambda state: state.can_reach(f"ItemPickup{total_locations}", "Location", player))
        if total_revivals or multiworld.start_with_revive[player].value:
            add_rule(multiworld.get_location("Victory", player),
                     lambda state: state.has("Dio's Best Friend", player,
                                             total_revivals + multiworld.start_with_revive[player]))

    elif multiworld.goal[player] == "explore":
        # When explore_mode is used,
        #   scavengers need to be locked till after a full loop since that is when they are capable of spawning.
        # (While technically the requirement is just beating 5 stages, this will ensure that the player will have
        #   a long enough run to have enough director credits for scavengers and
        #   help prevent being stuck in the same stages until that point.)

        for location in multiworld.get_locations(player):
            if "Scavenger" in location.name:
                add_rule(location, lambda state: state.has("Stage_5", player))
        # Regions
        chests = multiworld.chests_per_stage[player]
        shrines = multiworld.shrines_per_stage[player]
        newts = multiworld.altars_per_stage[player]
        scavengers = multiworld.scavengers_per_stage[player]
        scanners = multiworld.scanner_per_stage[player]
        for i in range(len(environment_vanilla_orderedstages_table)):
            for environment_name, _ in environment_vanilla_orderedstages_table[i].items():
                # Make sure to go through each location
                if scavengers == 1:
                    has_location_access_rule(multiworld, environment_name, player, scavengers, "Scavenger")
                if scanners == 1:
                    has_location_access_rule(multiworld, environment_name, player, scanners, "Radio Scanner")
                for chest in range(1, chests + 1):
                    has_location_access_rule(multiworld, environment_name, player, chest, "Chest")
                for shrine in range(1, shrines + 1):
                    has_location_access_rule(multiworld, environment_name, player, shrine, "Shrine")
                if newts > 0:
                    for newt in range(1, newts + 1):
                        has_location_access_rule(multiworld, environment_name, player, newt, "Newt Altar")
                if i > 0:
                    has_entrance_access_rule(multiworld, f"Stage_{i}", environment_name, player)
            get_stage_event(multiworld, player, i)

        if multiworld.dlc_sotv[player]:
            for i in range(len(environment_sotv_orderedstages_table)):
                for environment_name, _ in environment_sotv_orderedstages_table[i].items():
                    # Make sure to go through each location
                    if scavengers == 1:
                        has_location_access_rule(multiworld, environment_name, player, scavengers, "Scavenger")
                    if scanners == 1:
                        has_location_access_rule(multiworld, environment_name, player, scanners, "Radio Scanner")
                    for chest in range(1, chests + 1):
                        has_location_access_rule(multiworld, environment_name, player, chest, "Chest")
                    for shrine in range(1, shrines + 1):
                        has_location_access_rule(multiworld, environment_name, player, shrine, "Shrine")
                    if newts > 0:
                        for newt in range(1, newts + 1):
                            has_location_access_rule(multiworld, environment_name, player, newt, "Newt Altar")
                    if i > 0:
                        has_entrance_access_rule(multiworld, f"Stage_{i}", environment_name, player)
        has_entrance_access_rule(multiworld, f"Hidden Realm: A Moment, Fractured", "Hidden Realm: A Moment, Whole",
                                 player)
        has_entrance_access_rule(multiworld, f"Stage_1", "Hidden Realm: Bazaar Between Time", player)
        has_entrance_access_rule(multiworld, f"Hidden Realm: Bazaar Between Time", "Void Fields", player)
        has_entrance_access_rule(multiworld, f"Stage_5", "Commencement", player)
        has_entrance_access_rule(multiworld, f"Stage_5", "Hidden Realm: A Moment, Fractured", player)
        has_entrance_access_rule(multiworld, "Beads of Fealty", "Hidden Realm: A Moment, Whole", player)
        if multiworld.dlc_sotv[player]:
            has_entrance_access_rule(multiworld, f"Stage_5", "Void Locus", player)
            has_entrance_access_rule(multiworld, f"Void Locus", "The Planetarium", player)
    # Win Condition
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
