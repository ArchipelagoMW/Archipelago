from typing import Dict, NamedTuple, Optional, Set

import self

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

    def __init__(self, world: SDWorld) -> None:
        self.player = world.player
        self.world = world
        self.multiworld = world.multiworld

    # Party
    def party_members_amount(self, state: CollectionState):
        state: CollectionState
        num: int = 0
        if state.has("Pinn", self.player):
            num += 1
        if state.has("Kani", self.player):
            num += 1
        if state.has("Geo", self.player):
            num += 1
        return num

    #Keys
    def key_red(self, state: CollectionState) -> bool:
        return state.has("Red Key", self.player)

    def key_yellow(self, state: CollectionState) -> bool:
        return state.has("Yellow Key", self.player)

    #Zones
    def zone_red(self, state: CollectionState) -> bool:
        return ((state.has("Yellow Key", self.player)) and party(2))

    def zone_red2(self, state: CollectionState) -> bool:
        return ((state.has("Yellow Key", self.player)) and party(2))









def party(amount) -> bool:
    return SDRules.party_members_amount > amount

#Keys
def key(key_name) -> bool:
    rules = "SDRules.key_" + key_name
    return rules

#Zones
def zone(zone_name) -> bool:
    rules = "SDRules.zone_" + zone_name
    return rules