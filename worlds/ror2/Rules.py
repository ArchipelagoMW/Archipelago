from BaseClasses import MultiWorld
from worlds.generic.Rules import set_rule, add_rule
from .Locations import orderedstage_location


def set_rules(world: MultiWorld, player: int) -> None:

    if (world.classic_mode[player].value):
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


    if (world.classic_mode[player].value):
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
        for location in world.get_locations():
            if location.player != player: continue # ignore all checks that don't belong to this player
            if ("Scavenger" in location.name):
                add_rule(location, lambda state: state.has("OrderedStage_5", player))

    world.completion_condition[player] = lambda state: state.has("Victory", player)
