import math
import typing
from BaseClasses import MultiWorld, CollectionState
from .JakAndDaxterOptions import JakAndDaxterOptions
from .Items import orb_item_table
from .locs import CellLocations as Cells
from .Locations import location_table
from .regs.RegionBase import JakAndDaxterRegion


def can_reach_orbs(state: CollectionState,
                   player: int,
                   multiworld: MultiWorld,
                   options: JakAndDaxterOptions,
                   level_name: str = None) -> int:

    # Global Orbsanity and No Orbsanity both treat orbs as completely interchangeable.
    # Per Level Orbsanity needs to know if you can reach orbs *in a particular level.*
    if options.enable_orbsanity.value in [0, 2]:
        return can_reach_orbs_global(state, player, multiworld)
    else:
        return can_reach_orbs_level(state, player, multiworld, level_name)


def can_reach_orbs_global(state: CollectionState,
                          player: int,
                          multiworld: MultiWorld) -> int:

    accessible_orbs = 0
    for region in multiworld.get_regions(player):
        if state.can_reach(region, "Region", player):
            accessible_orbs += typing.cast(JakAndDaxterRegion, region).orb_count

    return accessible_orbs


def can_reach_orbs_level(state: CollectionState,
                         player: int,
                         multiworld: MultiWorld,
                         level_name: str) -> int:

    accessible_orbs = 0
    regions = [typing.cast(JakAndDaxterRegion, reg) for reg in multiworld.get_regions(player)]
    for region in regions:
        if region.level_name == level_name and state.can_reach(region, "Region", player):
            accessible_orbs += region.orb_count

    return accessible_orbs


# TODO - Until we come up with a better progressive system for the traders (that avoids hard-locking if you pay the
#  wrong ones and can't afford the right ones) just make all the traders locked behind the total amount to pay them all.
def can_trade(state: CollectionState,
              player: int,
              multiworld: MultiWorld,
              options: JakAndDaxterOptions,
              required_orbs: int,
              required_previous_trade: int = None) -> bool:

    if options.enable_orbsanity.value == 1:
        bundle_size = options.level_orbsanity_bundle_size.value
        return can_trade_orbsanity(state, player, bundle_size, required_orbs, required_previous_trade)
    elif options.enable_orbsanity.value == 2:
        bundle_size = options.global_orbsanity_bundle_size.value
        return can_trade_orbsanity(state, player, bundle_size, required_orbs, required_previous_trade)
    else:
        return can_trade_regular(state, player, multiworld, required_orbs, required_previous_trade)


def can_trade_regular(state: CollectionState,
                      player: int,
                      multiworld: MultiWorld,
                      required_orbs: int,
                      required_previous_trade: int = None) -> bool:

    # We know that Orbsanity is off, so count orbs globally.
    accessible_orbs = can_reach_orbs_global(state, player, multiworld)
    if required_previous_trade:
        name_of_previous_trade = location_table[Cells.to_ap_id(required_previous_trade)]
        return (accessible_orbs >= required_orbs
                and state.can_reach(name_of_previous_trade, "Location", player=player))
    else:
        return accessible_orbs >= required_orbs


def can_trade_orbsanity(state: CollectionState,
                        player: int,
                        orb_bundle_size: int,
                        required_orbs: int,
                        required_previous_trade: int = None) -> bool:

    required_count = math.ceil(required_orbs / orb_bundle_size)
    orb_bundle_name = orb_item_table[orb_bundle_size]
    if required_previous_trade:
        name_of_previous_trade = location_table[Cells.to_ap_id(required_previous_trade)]
        return (state.has(orb_bundle_name, player, required_count)
                and state.can_reach(name_of_previous_trade, "Location", player=player))
    else:
        return state.has(orb_bundle_name, player, required_count)


def can_free_scout_flies(state: CollectionState, player: int) -> bool:
    return (state.has("Jump Dive", player)
            or (state.has("Crouch", player)
                and state.has("Crouch Uppercut", player)))


def can_fight(state: CollectionState, player: int) -> bool:
    return (state.has("Jump Dive", player)
            or state.has("Jump Kick", player)
            or state.has("Punch", player)
            or state.has("Kick", player))
