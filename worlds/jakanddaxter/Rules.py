import typing
from BaseClasses import MultiWorld, CollectionState
from Options import OptionError
from . import JakAndDaxterWorld
from .JakAndDaxterOptions import (JakAndDaxterOptions,
                                  EnableOrbsanity,
                                  GlobalOrbsanityBundleSize,
                                  PerLevelOrbsanityBundleSize,
                                  FireCanyonCellCount,
                                  MountainPassCellCount,
                                  LavaTubeCellCount,
                                  CitizenOrbTradeAmount,
                                  OracleOrbTradeAmount)
from .locs import CellLocations as Cells
from .Locations import location_table
from .Levels import level_table
from .regs.RegionBase import JakAndDaxterRegion


def set_orb_trade_rule(world: JakAndDaxterWorld):
    options = world.options
    player = world.player

    if options.enable_orbsanity == EnableOrbsanity.option_off:
        world.can_trade = lambda state, required_orbs, required_previous_trade: (
            can_trade_vanilla(state, player, required_orbs, required_previous_trade))
    else:
        world.can_trade = lambda state, required_orbs, required_previous_trade: (
            can_trade_orbsanity(state, player, required_orbs, required_previous_trade))


def recalculate_reachable_orbs(state: CollectionState, player: int) -> None:

    if not state.prog_items[player]["Reachable Orbs Fresh"]:

        # Recalculate every level, every time the cache is stale, because you don't know
        # when a specific bundle of orbs in one level may unlock access to another.
        for level in level_table:
            state.prog_items[player][f"{level} Reachable Orbs".strip()] = (
                count_reachable_orbs_level(state, player, state.multiworld, level))

        # Also recalculate the global count, still used even when Orbsanity is Off.
        state.prog_items[player]["Reachable Orbs"] = count_reachable_orbs_global(state, player, state.multiworld)
        state.prog_items[player]["Reachable Orbs Fresh"] = True


def count_reachable_orbs_global(state: CollectionState,
                                player: int,
                                multiworld: MultiWorld) -> int:

    accessible_orbs = 0
    for region in multiworld.get_regions(player):
        if region.can_reach(state):
            # Only cast the region when we need to.
            accessible_orbs += typing.cast(JakAndDaxterRegion, region).orb_count
    return accessible_orbs


def count_reachable_orbs_level(state: CollectionState,
                               player: int,
                               multiworld: MultiWorld,
                               level_name: str = "") -> int:

    accessible_orbs = 0
    # Need to cast all regions upfront.
    for region in typing.cast(typing.List[JakAndDaxterRegion], multiworld.get_regions(player)):
        if region.level_name == level_name and region.can_reach(state):
            accessible_orbs += region.orb_count
    return accessible_orbs


def can_reach_orbs_global(state: CollectionState,
                          player: int,
                          world: JakAndDaxterWorld,
                          bundle: int) -> bool:

    recalculate_reachable_orbs(state, player)
    return state.has("Reachable Orbs", player, world.orb_bundle_size * (bundle + 1))


def can_reach_orbs_level(state: CollectionState,
                         player: int,
                         world: JakAndDaxterWorld,
                         level_name: str,
                         bundle: int) -> bool:

    recalculate_reachable_orbs(state, player)
    return state.has(f"{level_name} Reachable Orbs", player, world.orb_bundle_size * (bundle + 1))


def can_trade_vanilla(state: CollectionState,
                      player: int,
                      required_orbs: int,
                      required_previous_trade: typing.Optional[int] = None) -> bool:

    recalculate_reachable_orbs(state, player)  # With Orbsanity Off, Reachable Orbs are in fact Tradeable Orbs.
    if required_previous_trade:
        name_of_previous_trade = location_table[Cells.to_ap_id(required_previous_trade)]
        return (state.has("Reachable Orbs", player, required_orbs)
                and state.can_reach_location(name_of_previous_trade, player=player))
    return state.has("Reachable Orbs", player, required_orbs)


def can_trade_orbsanity(state: CollectionState,
                        player: int,
                        required_orbs: int,
                        required_previous_trade: typing.Optional[int] = None) -> bool:

    recalculate_reachable_orbs(state, player)  # Yes, even Orbsanity trades may unlock access to new Reachable Orbs.
    if required_previous_trade:
        name_of_previous_trade = location_table[Cells.to_ap_id(required_previous_trade)]
        return (state.has("Tradeable Orbs", player, required_orbs)
                and state.can_reach_location(name_of_previous_trade, player=player))
    return state.has("Tradeable Orbs", player, required_orbs)


def can_free_scout_flies(state: CollectionState, player: int) -> bool:
    return state.has("Jump Dive", player) or state.has_all({"Crouch", "Crouch Uppercut"}, player)


def can_fight(state: CollectionState, player: int) -> bool:
    return state.has_any({"Jump Dive", "Jump Kick", "Punch", "Kick"}, player)


def enforce_multiplayer_limits(options: JakAndDaxterOptions):
    friendly_message = ""

    if (options.enable_orbsanity == EnableOrbsanity.option_global
            and options.global_orbsanity_bundle_size.value < GlobalOrbsanityBundleSize.friendly_minimum):
        friendly_message += (f"  "
                             f"{options.global_orbsanity_bundle_size.display_name} must be no less than "
                             f"{GlobalOrbsanityBundleSize.friendly_minimum} (currently "
                             f"{options.global_orbsanity_bundle_size.value}).\n")

    if (options.enable_orbsanity == EnableOrbsanity.option_per_level
            and options.level_orbsanity_bundle_size.value < PerLevelOrbsanityBundleSize.friendly_minimum):
        friendly_message += (f"  "
                             f"{options.level_orbsanity_bundle_size.display_name} must be no less than "
                             f"{PerLevelOrbsanityBundleSize.friendly_minimum} (currently "
                             f"{options.level_orbsanity_bundle_size.value}).\n")

    if options.fire_canyon_cell_count.value > FireCanyonCellCount.friendly_maximum:
        friendly_message += (f"  "
                             f"{options.fire_canyon_cell_count.display_name} must be no greater than "
                             f"{FireCanyonCellCount.friendly_maximum} (currently "
                             f"{options.fire_canyon_cell_count.value}).\n")

    if options.mountain_pass_cell_count.value > MountainPassCellCount.friendly_maximum:
        friendly_message += (f"  "
                             f"{options.mountain_pass_cell_count.display_name} must be no greater than "
                             f"{MountainPassCellCount.friendly_maximum} (currently "
                             f"{options.mountain_pass_cell_count.value}).\n")

    if options.lava_tube_cell_count.value > LavaTubeCellCount.friendly_maximum:
        friendly_message += (f"  "
                             f"{options.lava_tube_cell_count.display_name} must be no greater than "
                             f"{LavaTubeCellCount.friendly_maximum} (currently "
                             f"{options.lava_tube_cell_count.value}).\n")

    if options.citizen_orb_trade_amount.value > CitizenOrbTradeAmount.friendly_maximum:
        friendly_message += (f"  "
                             f"{options.citizen_orb_trade_amount.display_name} must be no greater than "
                             f"{CitizenOrbTradeAmount.friendly_maximum} (currently "
                             f"{options.citizen_orb_trade_amount.value}).\n")

    if options.oracle_orb_trade_amount.value > OracleOrbTradeAmount.friendly_maximum:
        friendly_message += (f"  "
                             f"{options.oracle_orb_trade_amount.display_name} must be no greater than "
                             f"{OracleOrbTradeAmount.friendly_maximum} (currently "
                             f"{options.oracle_orb_trade_amount.value}).\n")

    if friendly_message != "":
        raise OptionError(f"Please adjust the following Options for a multiplayer game.\n"
                          f"{friendly_message}")


def verify_orb_trade_amounts(options: JakAndDaxterOptions):

    total_trade_orbs = (9 * options.citizen_orb_trade_amount) + (6 * options.oracle_orb_trade_amount)
    if total_trade_orbs > 2000:
        raise OptionError(f"Required number of orbs for all trades ({total_trade_orbs}) "
                          f"is more than all the orbs in the game (2000). "
                          f"Reduce the value of either {options.citizen_orb_trade_amount.display_name} "
                          f"or {options.oracle_orb_trade_amount.display_name}.")
