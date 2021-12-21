from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin

class RaftLogic(LogicMixin):

    def can_navigate(self, player): # The player can both find locations with the receiver and can change course with the sail
        return self.has("Sail", player) and self.has("Battery", player) and self.has("Receiver", player) and self.has("Antenna", player)

    def can_drive(self, player): # The player can go wherever they want with the engine
        return self.has("Engine", player) and self.has("Steering Wheel", player)

    def can_access_radio_tower(self, player):
        return self.can_navigate(player)

    def can_complete_radio_tower(self, player):
        return self.can_access_radio_tower(player)

    def can_access_vasagatan(self, player):
        return self.can_navigate(player) and self.has("Vasagatan Coordinates", player)

    def can_complete_vasagatan(self, player):
        return self.can_access_vasagatan(player) and self.has("Bomb", player)

    def can_access_balboa_island(self, player):
        return self.can_navigate(player) and self.can_drive(state, player) and self.has("Balboa Coordinates", player)

    def can_complete_balboa_island(self, player):
        return self.can_access_balboa_island(player) and self.has("Machete", player)

    def can_access_caravan_island(self, player):
        return self.can_navigate(player) and self.can_drive(player) and self.has("Caravan Coordinates", player)

    def can_complete_caravan_island(self, player):
        return self.can_access_caravan_island(player) and self.has("Zipline", player)

    def can_access_tangaroa(self, player):
        return self.can_navigate(player) and self.can_drive(player) and self.has("Tangaroa Coordinates", player)

    def can_complete_tangaroa(self, player):
        return self.can_access_tangaroa(player) and self.has("Generator Part", player, 3) and self.has("Tape", 9)


def set_rules(world, player):
    # Map region to check to see if we can access it
    regionChecks = {
        "Raft": lambda state: True,
        "ResearchTable": lambda state: True,
        "RadioTower": lambda state: state.can_access_radio_tower(player), # All can_access functions have state as implicit parameter for function
        "Vasagatan": lambda state: state.can_access_vasagatan(player),
        "BalboaIsland": lambda state: state.can_access_balboa_island(player),
        "CaravanIsland": lambda state: state.can_access_caravan_island(player),
        "Tangaroa": lambda state: state.can_access_tangaroa(player)
    }

    # Location rules
    for region in regionMap:
        if region != "Menu":
            # TODO Add item requirements (eg Caravan Island requires zipline for some, but not all, checks)
            for exitRegion in world.get_region(region, player).exits:
                set_rule(world.get_entrance(exitRegion.name, player), regionChecks[region])
     
    # Process locations
    for location in location_table:
        set_rule(world.get_location(location["name"], player), regionChecks[location["region"]])

    # Victory location
    world.completion_condition[player] = lambda state: state.has('Victory', player)
