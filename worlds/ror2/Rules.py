from BaseClasses import MultiWorld
from worlds.generic.Rules import set_rule, add_rule


def set_rules(world: MultiWorld, player: int) -> None:
    total_locations = world.total_locations[player].value  # total locations for current player
    event_location_step = 25  # set an event location at these locations for "spheres"
    divisions = total_locations // event_location_step
    total_revivals = world.worlds[player].total_revivals  # pulling this info we calculated in generate_basic

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

    world.completion_condition[player] = lambda state: state.has("Victory", player)
