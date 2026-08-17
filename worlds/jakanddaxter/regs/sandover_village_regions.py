from .region_base import JakAndDaxterRegion
from ..options import EnableOrbsanity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import JakAndDaxterWorld
from ..rules import can_free_scout_flies, can_reach_orbs_level


def build_regions(level_name: str, world: "JakAndDaxterWorld") -> JakAndDaxterRegion:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 26)

    # Yakows requires no combat.
    main_area.add_cell_locations([10])
    main_area.add_cell_locations([11], access_rule=lambda state: world.can_trade(state, world.total_trade_orbs, None))
    main_area.add_cell_locations([12], access_rule=lambda state: world.can_trade(state, world.total_trade_orbs, None))

    # These 4 scout fly boxes can be broken by running with all the blue eco from Sentinel Beach.
    main_area.add_fly_locations([262219, 327755, 131147, 65611])

    # The farmer's scout fly. You can either get the Orb Cache Cliff blue eco, or break it normally.
    main_area.add_fly_locations([196683], access_rule=lambda state:
                                state.has("Double Jump", player)
                                or state.has_all(("Crouch", "Crouch Jump"), player)
                                or can_free_scout_flies(state, player))

    orb_cache_cliff = JakAndDaxterRegion("Orb Cache Cliff", player, multiworld, level_name, 15)
    orb_cache_cliff.add_cache_locations([10344])

    yakow_cliff = JakAndDaxterRegion("Yakow Cliff", player, multiworld, level_name, 3)
    yakow_cliff.add_fly_locations([75], access_rule=lambda state: can_free_scout_flies(state, player))

    oracle_platforms = JakAndDaxterRegion("Oracle Platforms", player, multiworld, level_name, 6)
    oracle_platforms.add_cell_locations([13], access_rule=lambda state:
                                        world.can_trade(state, world.total_trade_orbs, None))
    oracle_platforms.add_cell_locations([14], access_rule=lambda state:
                                        world.can_trade(state, world.total_trade_orbs, 13))
    oracle_platforms.add_fly_locations([393291], access_rule=lambda state:
                                       can_free_scout_flies(state, player))

    main_area.connect(orb_cache_cliff, rule=lambda state:
                      state.has("Double Jump", player)
                      or state.has_all(("Crouch", "Crouch Jump"), player)
                      or state.has_all(("Crouch", "Crouch Uppercut", "Jump Kick"), player))

    main_area.connect(yakow_cliff, rule=lambda state:
                      state.has("Double Jump", player)
                      or state.has_all(("Crouch", "Crouch Jump"), player)
                      or state.has_all(("Crouch", "Crouch Uppercut", "Jump Kick"), player))

    main_area.connect(oracle_platforms, rule=lambda state:
                      state.has_all(("Roll", "Roll Jump"), player)
                      or state.has_all(("Double Jump", "Jump Kick"), player))

    # All these can go back to main_area immediately.
    orb_cache_cliff.connect(main_area)
    yakow_cliff.connect(main_area)
    oracle_platforms.connect(main_area)

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(orb_cache_cliff)
    world.level_to_regions[level_name].append(yakow_cliff)
    world.level_to_regions[level_name].append(oracle_platforms)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 50 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(1,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return main_area
