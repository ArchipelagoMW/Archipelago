import typing
from BaseClasses import MultiWorld, CollectionState
from .JakAndDaxterOptions import JakAndDaxterOptions
from .locs import CellLocations as Cells
from .Locations import location_table
from .Regions import JakAndDaxterRegion


# TODO - Until we come up with a better progressive system for the traders (that avoids hard-locking if you pay the
#  wrong ones and can't afford the right ones) just make all the traders locked behind the total amount to pay them all.
def can_trade(state: CollectionState,
              player: int,
              multiworld: MultiWorld,
              required_orbs: int,
              required_previous_trade: int = None) -> bool:

    accessible_orbs = 0
    for region in multiworld.get_regions(player):
        if state.can_reach(region, "Region", player):
            accessible_orbs += typing.cast(JakAndDaxterRegion, region).orb_count

    if required_previous_trade:
        name_of_previous_trade = location_table[Cells.to_ap_id(required_previous_trade)]
        return (accessible_orbs >= required_orbs
                and state.can_reach(name_of_previous_trade, "Location", player=player))
    else:
        return accessible_orbs >= required_orbs


def can_free_scout_flies(state: CollectionState, player: int) -> bool:
    return (state.has("Jump Dive", player)
            or (state.has("Crouch", player)
                and state.has("Crouch Uppercut", player)))


def can_fight(state: CollectionState, player: int) -> bool:
    return (state.has("Jump Dive", player)
            or state.has("Jump Kick", player)
            or state.has("Punch", player)
            or state.has("Kick", player))
