from .region_base import JakAndDaxterRegion
from ..options import EnableOrbsanity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import JakAndDaxterWorld
from ..rules import can_reach_orbs_level
from ..locs import scout_locations as scouts


def build_regions(level_name: str, world: "JakAndDaxterWorld") -> JakAndDaxterRegion:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 48)
    main_area.add_cell_locations([92, 93])
    main_area.add_fly_locations(scouts.locGR_scoutTable.keys())  # All Flies here are accessible with blue eco.

    # The last 2 orbs are barely gettable with the blue eco vent, but it's pushing accessibility. So I moved them here.
    cliff = JakAndDaxterRegion("Cliff", player, multiworld, level_name, 2)
    cliff.add_cell_locations([94])

    main_area.connect(cliff, rule=lambda state:
                      state.has("Double Jump", player)
                      or state.has_all(("Crouch", "Crouch Jump"), player)
                      or state.has_all(("Crouch", "Crouch Uppercut"), player))

    cliff.connect(main_area)  # Jump down or ride blue eco elevator.

    world.level_to_regions[level_name].append(main_area)
    world.level_to_regions[level_name].append(cliff)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 50 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            amount = world.orb_bundle_size * (bundle_index + 1)
            orbs.add_orb_locations(0,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, orb_amount=amount:
                                   can_reach_orbs_level(state, player, world, level, orb_amount))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return main_area
