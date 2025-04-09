from typing import Dict, NamedTuple, Optional, Set

import self

from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, forbid_item

#Party
def party_members_amount(state: CollectionState, player: int):
    state: CollectionState
    num: int = 0
    if state.has("Pinn", player):
        num += 1
    if state.has("Kani", player):
        num += 1
    if state.has("Geo", player):
        num += 1
    return num

def party(amount) -> bool:
    return party_members_amount > amount

#Keys
def has_key(keyname, state: CollectionState, player: int) -> bool:
    return state.has(keyname, player)

#Zones
def red():
    return has_key("yellow", state, player)

def red2(state: CollectionState, player: int):
    return has_key("yellow", state, player)


set_rules = [


]