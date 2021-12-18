from ..generic.Rules import set_rule
from .Locations import location_table
from .Regions import regionMap
from ..AutoWorld import LogicMixin

class RaftLogic(LogicMixin):

    def can_navigate(state, player): # The player can both find locations with the receiver and can change course with the sail
        return state.has("Sail", player) and state.has("Battery", player) and state.has("Receiver", player) and state.has("Antenna", player)

    def can_drive(state, player): # The player can go wherever they want with the engine
        return state.has("Engine", player) and state.has("Steering Wheel", player)

    def can_access_radio_tower(state, player):
        state.can_navigate(state, player)

    def can_complete_radio_tower(state, player):
        return state.can_access_radio_tower(state, player)

    def can_access_vasagatan(state, player):
        return state.can_navigate(state, player) and state.has("Vastagatan Coordinates", player)

    def can_complete_vasagatan(state, player):
        return state.can_access_vasagatan(state, player) and state.has("Bomb", player)

    def can_access_balboa_island(state, player):
        return state.can_navigate(state, player) and state.can_drive(state, player) and state.has("Balboa Coordinates", player)

    def can_complete_balboa_island(state, player):
        return state.can_access_balboa_island(state, player) and state.has("Machete", player)

    def can_access_caravan_island(state, player):
        return state.can_navigate(state, player) and state.can_drive(state, player) and state.has("Caravan Coordinates", player)

    def can_complete_caravan_island(state, player):
        return state.can_access_caravan_island(state, player) and state.has("Zipline", player)

    def can_access_tangaroa(state, player):
        return state.can_navigate(state, player) and state.can_drive(state, player) and state.has("Tangaroa Coordinates", player)

    def can_complete_tangaroa(state, player):
        return state.can_access_tangaroa(state, player) and state.has("Generator Part", player, 3) and state.has("Tape", 9)


def set_rules(world, player):
    # Map region to check to see if we can access it
    regionChecks = {
        "Radio Tower": lambda state: state.can_access_radio_tower(player),
        "Vasagatan": lambda state: state.can_access_vasagatan(player),
        "Balboa Island": lambda state: state.can_access_balboa_island(player),
        "Caravan Island": lambda state: state.can_access_caravan_island(player),
        "Tangaroa": lambda state: state.can_access_tangaroa(player)
    }
    # Location rules
    
    # Process locations

    # Victory location
    world.completion_condition[player] = lambda state: state.has('RadioTowerRadioTranscription', player) #TODO: Add actual victory condition
