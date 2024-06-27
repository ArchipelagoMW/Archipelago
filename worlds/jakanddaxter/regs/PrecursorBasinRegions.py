from typing import List
from BaseClasses import CollectionState, MultiWorld
from .RegionBase import JakAndDaxterRegion
from ..locs import CellLocations as Cells, ScoutLocations as Scouts


def build_regions(level_name: str, player: int, multiworld: MultiWorld) -> List[JakAndDaxterRegion]:

    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 200)

    # Everything is accessible by making contact with the zoomer.
    main_area.add_cell_locations(Cells.locPB_cellTable.keys())
    main_area.add_fly_locations(Scouts.locPB_scoutTable.keys())

    multiworld.regions.append(main_area)

    return [main_area]
