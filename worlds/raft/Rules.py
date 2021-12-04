from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin

class RaftLogic(LogicMixin):

    def can_access_radio_tower(state, player):
        return state.has("ItemForRadioTower", player)

    def can_access_vasagatan(state, player):
        return state.has("ItemForVasagatan", player)

    def can_access_balboa_island(state, player):
        return state.has("ItemForBalboaIsland", player)

    def can_access_caravan_island(state, player):
        return state.has("ItemForCaravanIsland", player)

    def can_access_tangaroa(state, player):
        return state.has("ItemForTangaroa", player)


def set_rules(world, player):
    # Map region to check to see if we can access it
    regionChecks = {
		"Menu": lambda state: true,
        "Radio Tower": lambda state: state.can_access_radio_tower(player),
        "Vasagatan": lambda state: state.can_access_vasagatan(player),
        "Balboa Island": lambda state: state.can_access_balboa_island(player),
        "Caravan Island": lambda state: state.can_access_caravan_island(player),
        "Tangaroa": lambda state: state.can_access_tangaroa(player)
    }
    # Location rules
    for region in world.regions:
        print(region)
        print(world.get_entrances())
        print(world.get_entrance(region, player))
        print(regionChecks[region])
        # TODO Add item requirements (eg Caravan Island requires zipline for some, but not all, checks)
        set_rule(world.get_entrance(region, player), regionChecks[region])
    
    # Process locations
    for location in location_table:
        set_rule(world.get_location(location.name, player), regionChecks[location.region])

    # Victory location
    world.completion_condition[player] = lambda state: state.has('TangaroaCompletionCondition', player)
