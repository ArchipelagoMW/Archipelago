from typing import List
from BaseClasses import CollectionState, MultiWorld
from .RegionBase import JakAndDaxterRegion
from .. import JakAndDaxterOptions
from ..Rules import can_reach_orbs
from ..locs import CellLocations as Cells, ScoutLocations as Scouts


def build_regions(level_name: str, multiworld: MultiWorld, options: JakAndDaxterOptions, player: int) -> List[JakAndDaxterRegion]:

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 50)

    # Everything is accessible by making contact with the zoomer.
    main_area.add_cell_locations(Cells.locFC_cellTable.keys())
    main_area.add_fly_locations(Scouts.locFC_scoutTable.keys())

    multiworld.regions.append(main_area)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity.value == 1:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_size = options.level_orbsanity_bundle_size.value
        bundle_count = int(50 / bundle_size)
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(5,
                                   bundle_index,
                                   bundle_size,
                                   access_rule=lambda state, bundle=bundle_index:
                                   can_reach_orbs(state, player, multiworld, options, level_name)
                                   >= (bundle_size * (bundle + 1)))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area]
