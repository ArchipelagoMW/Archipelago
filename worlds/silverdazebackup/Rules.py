from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, forbid_item

if TYPE_CHECKING:
    from . import SDWorld
else:
    SDWorld = object


class SDRules:
    player: int
    world: SDWorld
    you = SDWorld.player

    def __init__(self, world: SDWorld) -> None:
        self.player = world.player
        self.world = world
        self.multiworld = world.multiworld

    # Party
    def party_members_amount(self, state: CollectionState):
        num = 0
        if state.has("Pinn", self.player):
            num += 1
        if state.has("Kani", self.player):
            num += 1
        if state.has("Geo", self.player):
            num += 1
        return num


    #Keys
    #def key_red(self, state: CollectionState) -> bool:
    #    return state.has("Red Key", self.player)

    #def key_yellow(self, state: CollectionState) -> bool:
    #    return state.has("Yellow Key", self.player)

    key_red = lambda state: state.has("Red Key", SDWorld.player)
    key_yellow = lambda state: state.has("Yellow Key", SDWorld.player)

    #Zones
    #def zone_red(self, state: CollectionState) -> bool:
    #    return ((state.has("Yellow Key", self.player)) and party(2))
    #def zone_red2(self, state: CollectionState) -> bool:
    #    return ((state.has("Yellow Key", self.player)) and party(2))

    zone_red = lambda state: ((state.has("Yellow Key", SDWorld.player)) and party(2))



def party(amount: int) -> bool:
    num = SDRules.party_members_amount(SDRules, CollectionState)
    return num >= amount



#Keys
def key(key_name) -> bool:
    rules = "SDRules.key_" + key_name
    return rules

#Zones
def zone(zone_name) -> bool:
    rules = "SDRules.zone_" + zone_name
    return rules