from typing import List
from BaseClasses import CollectionState, MultiWorld
from .RegionBase import JakAndDaxterRegion
from .. import JakAndDaxterOptions, EnableOrbsanity
from ..Rules import can_reach_orbs
from ..locs import ScoutLocations as Scouts


def build_regions(level_name: str, multiworld: MultiWorld, options: JakAndDaxterOptions, player: int) -> List[JakAndDaxterRegion]:

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 50)
    main_area.add_cell_locations([92, 93])
    main_area.add_fly_locations(Scouts.locGR_scoutTable.keys())  # All Flies here are accessible with blue eco.

    cliff = JakAndDaxterRegion("Cliff", player, multiworld, level_name, 0)
    cliff.add_cell_locations([94])

    main_area.connect(cliff, rule=lambda state:
                      ((state.has("Crouch", player) and state.has("Crouch Jump", player))
                       or (state.has("Crouch", player) and state.has("Crouch Uppercut", player))
                       or state.has("Double Jump", player)))

    cliff.connect(main_area)  # Jump down or ride blue eco elevator.

    multiworld.regions.append(main_area)
    multiworld.regions.append(cliff)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_size = options.level_orbsanity_bundle_size.value
        bundle_count = int(50 / bundle_size)
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(0,
                                   bundle_index,
                                   bundle_size,
                                   access_rule=lambda state, bundle=bundle_index:
                                   can_reach_orbs(state, player, multiworld, options, level_name)
                                   >= (bundle_size * (bundle + 1)))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area]
