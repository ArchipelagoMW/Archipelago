from .RegionBase import JakAndDaxterRegion
from ..Options import EnableOrbsanity
from .. import JakAndDaxterWorld
from ..Rules import can_reach_orbs_level
from ..locs import CellLocations as Cells, ScoutLocations as Scouts


def build_regions(level_name: str, world: JakAndDaxterWorld) -> list[JakAndDaxterRegion]:
    multiworld = world.multiworld
    options = world.options
    player = world.player

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 200)

    # Everything is accessible by making contact with the zoomer.
    main_area.add_cell_locations(Cells.locPB_cellTable.keys())
    main_area.add_fly_locations(Scouts.locPB_scoutTable.keys())

    multiworld.regions.append(main_area)

    # If Per-Level Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Main Area. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_per_level:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld, level_name)

        bundle_count = 200 // world.orb_bundle_size
        for bundle_index in range(bundle_count):
            orbs.add_orb_locations(9,
                                   bundle_index,
                                   access_rule=lambda state, level=level_name, bundle=bundle_index:
                                   can_reach_orbs_level(state, player, world, level, bundle))
        multiworld.regions.append(orbs)
        main_area.connect(orbs)

    return [main_area]
