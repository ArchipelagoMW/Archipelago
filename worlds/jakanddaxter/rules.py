import typing
from BaseClasses import CollectionState
from Options import OptionError
from .options import (EnableOrbsanity,
                      GlobalOrbsanityBundleSize,
                      PerLevelOrbsanityBundleSize,
                      FireCanyonCellCount,
                      MountainPassCellCount,
                      LavaTubeCellCount,
                      CitizenOrbTradeAmount,
                      OracleOrbTradeAmount)
from .locs import cell_locations as cells
from .locations import location_table
from .levels import level_table

if typing.TYPE_CHECKING:
    from . import JakAndDaxterWorld


def set_orb_trade_rule(world: "JakAndDaxterWorld"):
    options = world.options
    player = world.player

    if options.enable_orbsanity == EnableOrbsanity.option_off:
        world.can_trade = lambda state, required_orbs, required_previous_trade: (
            can_trade_vanilla(state, player, world, required_orbs, required_previous_trade))
    else:
        world.can_trade = lambda state, required_orbs, required_previous_trade: (
            can_trade_orbsanity(state, player, world, required_orbs, required_previous_trade))


def recalculate_reachable_orbs(state: CollectionState, player: int, world: "JakAndDaxterWorld") -> None:

    # Recalculate every level, every time the cache is stale, because you don't know
    # when a specific bundle of orbs in one level may unlock access to another.
    accessible_total_orbs = 0
    for level in level_table:
        accessible_level_orbs = count_reachable_orbs_level(state, world, level)
        accessible_total_orbs += accessible_level_orbs
        state.prog_items[player][f"{level} Reachable Orbs".lstrip()] = accessible_level_orbs

    # Also recalculate the global count, still used even when Orbsanity is Off.
    state.prog_items[player]["Reachable Orbs"] = accessible_total_orbs
    state.prog_items[player]["Reachable Orbs Fresh"] = True


def count_reachable_orbs_global(state: CollectionState,
                                world: "JakAndDaxterWorld") -> int:

    accessible_orbs = 0
    for level_regions in world.level_to_orb_regions.values():
        for region in level_regions:
            if region.can_reach(state):
                accessible_orbs += region.orb_count
    return accessible_orbs


def count_reachable_orbs_level(state: CollectionState,
                               world: "JakAndDaxterWorld",
                               level_name: str = "") -> int:

    accessible_orbs = 0
    for region in world.level_to_orb_regions[level_name]:
        if region.can_reach(state):
            accessible_orbs += region.orb_count
    return accessible_orbs


def can_reach_orbs_global(state: CollectionState,
                          player: int,
                          world: "JakAndDaxterWorld",
                          orb_amount: int) -> bool:

    if not state.prog_items[player]["Reachable Orbs Fresh"]:
        recalculate_reachable_orbs(state, player, world)

    return state.has("Reachable Orbs", player, orb_amount)


def can_reach_orbs_level(state: CollectionState,
                         player: int,
                         world: "JakAndDaxterWorld",
                         level_name: str,
                         orb_amount: int) -> bool:

    if not state.prog_items[player]["Reachable Orbs Fresh"]:
        recalculate_reachable_orbs(state, player, world)

    return state.has(f"{level_name} Reachable Orbs", player, orb_amount)


def can_trade_vanilla(state: CollectionState,
                      player: int,
                      world: "JakAndDaxterWorld",
                      required_orbs: int,
                      required_previous_trade: typing.Optional[int] = None) -> bool:

    # With Orbsanity Off, Reachable Orbs are in fact Tradeable Orbs.
    if not state.prog_items[player]["Reachable Orbs Fresh"]:
        recalculate_reachable_orbs(state, player, world)

    if required_previous_trade:
        name_of_previous_trade = location_table[cells.to_ap_id(required_previous_trade)]
        return (state.has("Reachable Orbs", player, required_orbs)
                and state.can_reach_location(name_of_previous_trade, player=player))
    return state.has("Reachable Orbs", player, required_orbs)


def can_trade_orbsanity(state: CollectionState,
                        player: int,
                        world: "JakAndDaxterWorld",
                        required_orbs: int,
                        required_previous_trade: typing.Optional[int] = None) -> bool:

    # Yes, even Orbsanity trades may unlock access to new Reachable Orbs.
    if not state.prog_items[player]["Reachable Orbs Fresh"]:
        recalculate_reachable_orbs(state, player, world)

    if required_previous_trade:
        name_of_previous_trade = location_table[cells.to_ap_id(required_previous_trade)]
        return (state.has("Tradeable Orbs", player, required_orbs)
                and state.can_reach_location(name_of_previous_trade, player=player))
    return state.has("Tradeable Orbs", player, required_orbs)


def can_free_scout_flies(state: CollectionState, player: int) -> bool:
    return state.has("Jump Dive", player) or state.has_all({"Crouch", "Crouch Uppercut"}, player)


def can_fight(state: CollectionState, player: int) -> bool:
    return state.has_any(("Jump Dive", "Jump Kick", "Punch", "Kick"), player)


def enforce_multiplayer_limits(world: "JakAndDaxterWorld"):
    options = world.options
    friendly_message = ""

    if (options.enable_orbsanity == EnableOrbsanity.option_global
            and (options.global_orbsanity_bundle_size.value < GlobalOrbsanityBundleSize.friendly_minimum
                 or options.global_orbsanity_bundle_size.value > GlobalOrbsanityBundleSize.friendly_maximum)):
        friendly_message += (f"  "
                             f"{options.global_orbsanity_bundle_size.display_name} must be no less than "
                             f"{GlobalOrbsanityBundleSize.friendly_minimum} and no greater than "
                             f"{GlobalOrbsanityBundleSize.friendly_maximum} (currently "
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
        raise OptionError(f"{world.player_name}: The options you have chosen may disrupt the multiworld. \n"
                          f"Please adjust the following Options for a multiplayer game. \n"
                          f"{friendly_message}"
                          f"Or use 'random-range-x-y' instead of 'random' in your player yaml.\n"
                          f"Or set 'enforce_friendly_options' in the seed generator's host.yaml to false. "
                          f"(Use at your own risk!)")


def enforce_singleplayer_limits(world: "JakAndDaxterWorld"):
    options = world.options
    friendly_message = ""

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

    if friendly_message != "":
        raise OptionError(f"The options you have chosen may result in seed generation failures. \n"
                          f"Please adjust the following Options for a singleplayer game. \n"
                          f"{friendly_message}"
                          f"Or use 'random-range-x-y' instead of 'random' in your player yaml.\n"
                          f"Or set 'enforce_friendly_options' in your host.yaml to false. "
                          f"(Use at your own risk!)")


def verify_orb_trade_amounts(world: "JakAndDaxterWorld"):

    if world.total_trade_orbs > 2000:
        raise OptionError(f"{world.player_name}: Required number of orbs for all trades ({world.total_trade_orbs}) "
                          f"is more than all the orbs in the game (2000). Reduce the value of either "
                          f"{world.options.citizen_orb_trade_amount.display_name} "
                          f"or {world.options.oracle_orb_trade_amount.display_name}.")
