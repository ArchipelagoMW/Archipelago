from typing import List
from BaseClasses import CollectionState, MultiWorld
from .RegionBase import JakAndDaxterRegion
from .. import JakAndDaxterOptions, EnableOrbsanity
from ..Rules import can_free_scout_flies, can_trade, can_reach_orbs


def build_regions(level_name: str, multiworld: MultiWorld, options: JakAndDaxterOptions, player: int) -> List[JakAndDaxterRegion]:

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 26)

    # Yakows requires no combat.
    main_area.add_cell_locations([10])
    main_area.add_cell_locations([11], access_rule=lambda state:
                                 can_trade(state, player, multiworld, options, 1530))
    main_area.add_cell_locations([12], access_rule=lambda state:
                                 can_trade(state, player, multiworld, options, 1530))

    # These 4 scout fly boxes can be broken by running with all the blue eco from Sentinel Beach.
    main_area.add_fly_locations([262219, 327755, 131147, 65611])

    # The farmer's scout fly. You can either get the Orb Cache Cliff blue eco, or break it normally.
    main_area.add_fly_locations([196683], access_rule=lambda state:
                                (state.has("Crouch", player) and state.has("Crouch Jump", player))
                                or state.has("Double Jump", player)
                                or can_free_scout_flies(state, player))

    orb_cache_cliff = JakAndDaxterRegion("Orb Cache Cliff", player, multiworld, level_name, 15)
    orb_cache_cliff.add_cache_locations([10344])

    yakow_cliff = JakAndDaxterRegion("Yakow Cliff", player, multiworld, level_name, 3)
    yakow_cliff.add_fly_locations([75], access_rule=lambda state: can_free_scout_flies(state, player))

    oracle_platforms = JakAndDaxterRegion("Oracle Platforms", player, multiworld, level_name, 6)
    oracle_platforms.add_cell_locations([13], access_rule=lambda state:
                                        can_trade(state, player, multiworld, options, 1530))
    oracle_platforms.add_cell_locations([14], access_rule=lambda state:
                                        can_trade(state, player, multiworld, options, 1530, 13))
    oracle_platforms.add_fly_locations([393291], access_rule=lambda state:
                                       can_free_scout_flies(state, player))

    main_area.connect(orb_cache_cliff, rule=lambda state:
                      state.has("Double Jump", player)
                      or (state.has("Crouch", player)
                          and state.has("Crouch Jump", player))
                      or (state.has("Crouch", player)
                          and state.has("Crouch Uppercut", player)
                          and state.has("Jump Kick", player)))

    main_area.connect(yakow_cliff, rule=lambda state:
                      state.has("Double Jump", player)
                      or (state.has("Crouch", player)
                          and state.has("Crouch Jump", player))
                      or (state.has("Crouch", player)
                          and state.has("Crouch Uppercut", player)
                          and state.has("Jump Kick", player)))

    main_area.connect(oracle_platforms, rule=lambda state:
                      (state.has("Roll", player) and state.has("Roll Jump", player))
                      or (state.has("Double Jump", player) and state.has("Jump Kick", player)))

    # All these can go back to main_area immediately.
    orb_cache_cliff.connect(main_area)
    yakow_cliff.connect(main_area)
    oracle_platforms.connect(main_area)

    multiworld.regions.append(main_area)
    multiworld.regions.append(orb_cache_cliff)
    multiworld.regions.append(yakow_cliff)
    multiworld.regions.append(oracle_platforms)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_size = options.level_orbsanity_bundle_size.value
        bundle_count = int(50 / bundle_size)
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(1,
                                   bundle_index,
                                   bundle_size,
                                   access_rule=lambda state, bundle=bundle_index:
                                   can_reach_orbs(state, player, multiworld, options, level_name)
                                   >= (bundle_size * (bundle + 1)))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area]
