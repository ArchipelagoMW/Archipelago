from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from .Locations import first_mission_location_table, second_mission_location_table, third_mission_location_table, \
        fourth_mission_location_table, fifth_mission_location_table, cannon_core_location_table, \
        upgrade_location_table, chao_garden_location_table
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


def set_rules(world: MultiWorld, player: int):

    world.completion_condition[player] = lambda state: (state.has(ItemName.sonic_bounce_bracelet, player))

    for (k1, v1), (k2, v2), (k3, v3), (k4, v4), (k5, v5) in \
        zip(sorted(first_mission_location_table.items()), \
            sorted(second_mission_location_table.items()), \
            sorted(third_mission_location_table.items()), \
            sorted(fourth_mission_location_table.items()), \
            sorted(fifth_mission_location_table.items())):
            
        if world.IncludeMission2[player]:
            set_rule(world.get_location(k2, player),
                lambda state: state.can_reach(k1, "Location", player))
                
        if world.IncludeMission3[player]:
            set_rule(world.get_location(k3, player),
                lambda state: state.can_reach(k2, "Location", player))
                
        if world.IncludeMission4[player]:
            set_rule(world.get_location(k4, player),
                lambda state: state.can_reach(k3, "Location", player))
                
        if world.IncludeMission5[player]:
            set_rule(world.get_location(k5, player),
                lambda state: state.can_reach(k4, "Location", player))

    # TODO: Place Upgrade Requirements Here
    #for loc in upgrade_location_table:
    #    world.get_location(loc, player).add_item_rule(loc, lambda item: False)

    # TODO: Place Level Emblem Requirements Here

    # Create some reasonable arbitrary logic for Chao Races to prevent having to grind Chaos Drives in the first level (edge case)
    #for loc in chao_garden_location_table:
    #    world.get_location(loc, player).add_item_rule(loc, lambda item: False)

    world.completion_condition[player] = lambda state: (state.has(ItemName.emblem, player, 30))

