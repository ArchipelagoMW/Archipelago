import typing
from BaseClasses import MultiWorld, CollectionState
from Options import OptionError
from . import JakAndDaxterWorld
from .Options import (EnableOrbsanity,
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
    # Cast all regions upfront to access their unique attributes.
    for region in typing.cast(typing.List[JakAndDaxterRegion], multiworld.get_regions(player)):
        # Rely on short-circuiting to skip region.can_reach whenever possible.
        if region.orb_count > 0 and region.can_reach(state):
            accessible_orbs += region.orb_count
    return accessible_orbs


def count_reachable_orbs_level(state: CollectionState,
                               player: int,
                               multiworld: MultiWorld,
                               level_name: str = "") -> int:

    accessible_orbs = 0
    # Cast all regions upfront to access their unique attributes.
    for region in typing.cast(typing.List[JakAndDaxterRegion], multiworld.get_regions(player)):
        # Rely on short-circuiting to skip region.can_reach whenever possible.
        if region.level_name == level_name and region.orb_count > 0 and region.can_reach(state):
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


def enforce_multiplayer_limits(world: JakAndDaxterWorld):
    options = world.options
    friendly_message = ""

    if (options.enable_orbsanity == EnableOrbsanity.option_global
            and (options.global_orbsanity_bundle_size.value < GlobalOrbsanityBundleSize.multiplayer_minimum
                 or options.global_orbsanity_bundle_size.value > GlobalOrbsanityBundleSize.multiplayer_maximum)):
        friendly_message += (f"  "
                             f"{options.global_orbsanity_bundle_size.display_name} must be no less than "
                             f"{GlobalOrbsanityBundleSize.multiplayer_minimum} and no greater than "
                             f"{GlobalOrbsanityBundleSize.multiplayer_maximum} (currently "
                             f"{options.global_orbsanity_bundle_size.value}).\n")

    if (options.enable_orbsanity == EnableOrbsanity.option_per_level
            and options.level_orbsanity_bundle_size.value < PerLevelOrbsanityBundleSize.multiplayer_minimum):
        friendly_message += (f"  "
                             f"{options.level_orbsanity_bundle_size.display_name} must be no less than "
                             f"{PerLevelOrbsanityBundleSize.multiplayer_minimum} (currently "
                             f"{options.level_orbsanity_bundle_size.value}).\n")

    if options.fire_canyon_cell_count.value > FireCanyonCellCount.multiplayer_maximum:
        friendly_message += (f"  "
                             f"{options.fire_canyon_cell_count.display_name} must be no greater than "
                             f"{FireCanyonCellCount.multiplayer_maximum} (currently "
                             f"{options.fire_canyon_cell_count.value}).\n")

    if options.mountain_pass_cell_count.value > MountainPassCellCount.multiplayer_maximum:
        friendly_message += (f"  "
                             f"{options.mountain_pass_cell_count.display_name} must be no greater than "
                             f"{MountainPassCellCount.multiplayer_maximum} (currently "
                             f"{options.mountain_pass_cell_count.value}).\n")

    if options.lava_tube_cell_count.value > LavaTubeCellCount.multiplayer_maximum:
        friendly_message += (f"  "
                             f"{options.lava_tube_cell_count.display_name} must be no greater than "
                             f"{LavaTubeCellCount.multiplayer_maximum} (currently "
                             f"{options.lava_tube_cell_count.value}).\n")

    if options.citizen_orb_trade_amount.value > CitizenOrbTradeAmount.multiplayer_maximum:
        friendly_message += (f"  "
                             f"{options.citizen_orb_trade_amount.display_name} must be no greater than "
                             f"{CitizenOrbTradeAmount.multiplayer_maximum} (currently "
                             f"{options.citizen_orb_trade_amount.value}).\n")

    if options.oracle_orb_trade_amount.value > OracleOrbTradeAmount.multiplayer_maximum:
        friendly_message += (f"  "
                             f"{options.oracle_orb_trade_amount.display_name} must be no greater than "
                             f"{OracleOrbTradeAmount.multiplayer_maximum} (currently "
                             f"{options.oracle_orb_trade_amount.value}).\n")

    if friendly_message != "":
        raise OptionError(f"{world.player_name}: The options you have chosen may disrupt the multiworld. \n"
                          f"Please adjust the following Options for a multiplayer game. \n"
                          f"{friendly_message}"
                          f"Or use 'random-range-x-y' instead of 'random' in your player yaml.\n"
                          f"Or set 'enforce_friendly_options' in the seed generator's host.yaml to false. "
                          f"(Use at your own risk!)")


def enforce_singleplayer_limits(world: JakAndDaxterWorld):
    options = world.options
    friendly_message = ""

    if options.fire_canyon_cell_count.value > FireCanyonCellCount.singleplayer_maximum:
        friendly_message += (f"  "
                             f"{options.fire_canyon_cell_count.display_name} must be no greater than "
                             f"{FireCanyonCellCount.singleplayer_maximum} (currently "
                             f"{options.fire_canyon_cell_count.value}).\n")

    if options.mountain_pass_cell_count.value > MountainPassCellCount.singleplayer_maximum:
        friendly_message += (f"  "
                             f"{options.mountain_pass_cell_count.display_name} must be no greater than "
                             f"{MountainPassCellCount.singleplayer_maximum} (currently "
                             f"{options.mountain_pass_cell_count.value}).\n")

    if options.lava_tube_cell_count.value > LavaTubeCellCount.singleplayer_maximum:
        friendly_message += (f"  "
                             f"{options.lava_tube_cell_count.display_name} must be no greater than "
                             f"{LavaTubeCellCount.singleplayer_maximum} (currently "
                             f"{options.lava_tube_cell_count.value}).\n")

    if friendly_message != "":
        raise OptionError(f"The options you have chosen may result in seed generation failures. \n"
                          f"Please adjust the following Options for a singleplayer game. \n"
                          f"{friendly_message}"
                          f"Or use 'random-range-x-y' instead of 'random' in your player yaml.\n"
                          f"Or set 'enforce_friendly_options' in your host.yaml to false. "
                          f"(Use at your own risk!)")


def verify_orb_trade_amounts(world: JakAndDaxterWorld):

    if world.total_trade_orbs > 2000:
        raise OptionError(f"{world.player_name}: Required number of orbs for all trades ({world.total_trade_orbs}) "
                          f"is more than all the orbs in the game (2000). Reduce the value of either "
                          f"{world.options.citizen_orb_trade_amount.display_name} "
                          f"or {world.options.oracle_orb_trade_amount.display_name}.")
