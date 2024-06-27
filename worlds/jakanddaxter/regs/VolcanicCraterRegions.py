from typing import List
from BaseClasses import CollectionState, MultiWorld
from .RegionBase import JakAndDaxterRegion
from ..Rules import can_free_scout_flies, can_trade
from ..locs import CellLocations as Cells, ScoutLocations as Scouts


def build_regions(level_name: str, player: int, multiworld: MultiWorld) -> List[JakAndDaxterRegion]:

    # No area is inaccessible in VC even with only running and jumping.
    main_area = JakAndDaxterRegion("Main Area", player, multiworld, level_name, 50)
    main_area.add_cell_locations([96], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530))
    main_area.add_cell_locations([97], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530, 96))
    main_area.add_cell_locations([98], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530, 97))
    main_area.add_cell_locations([99], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530, 98))
    main_area.add_cell_locations([100], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530))
    main_area.add_cell_locations([101], access_rule=lambda state:
                                 can_trade(state, player, multiworld, 1530, 100))

    # Hidden Power Cell: you can carry yellow eco from Spider Cave just by running and jumping
    # and using your Goggles to shoot the box (you do not need Punch to shoot from FP mode).
    main_area.add_cell_locations([74])

    # No blue eco sources in this area, all boxes must be broken by hand (yellow eco can't be carried far enough).
    main_area.add_fly_locations(Scouts.locVC_scoutTable.keys(), access_rule=lambda state:
                                can_free_scout_flies(state, player))

    # Approach the gondola to get this check.
    main_area.add_special_locations([105])

    multiworld.regions.append(main_area)

    return [main_area]
