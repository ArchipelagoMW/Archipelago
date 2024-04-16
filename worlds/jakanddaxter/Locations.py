from BaseClasses import Location
from .GameID import game_id, game_name
from .locs import CellLocations, SpecialLocations, ScoutLocations


class JakAndDaxterLocation(Location):
    game: str = game_name


# All Locations
location_table = {
    **CellLocations.locGR_cellTable,
    **CellLocations.locSV_cellTable,
    **CellLocations.locFJ_cellTable,
    **CellLocations.locSB_cellTable,
    **CellLocations.locMI_cellTable,
    **CellLocations.locFC_cellTable,
    **CellLocations.locRV_cellTable,
    **CellLocations.locPB_cellTable,
    **CellLocations.locLPC_cellTable,
    **CellLocations.locBS_cellTable,
    **CellLocations.locMP_cellTable,
    **CellLocations.locVC_cellTable,
    **CellLocations.locSC_cellTable,
    **CellLocations.locSM_cellTable,
    **CellLocations.locLT_cellTable,
    **CellLocations.locGMC_cellTable,
    **SpecialLocations.loc_specialTable,
    **ScoutLocations.locGR_scoutTable,
    **ScoutLocations.locSV_scoutTable,
    **ScoutLocations.locFJ_scoutTable,
    **ScoutLocations.locSB_scoutTable,
    **ScoutLocations.locMI_scoutTable,
    **ScoutLocations.locFC_scoutTable,
    **ScoutLocations.locRV_scoutTable,
    **ScoutLocations.locPB_scoutTable,
    **ScoutLocations.locLPC_scoutTable,
    **ScoutLocations.locBS_scoutTable,
    **ScoutLocations.locMP_scoutTable,
    **ScoutLocations.locVC_scoutTable,
    **ScoutLocations.locSC_scoutTable,
    **ScoutLocations.locSM_scoutTable,
    **ScoutLocations.locLT_scoutTable,
    **ScoutLocations.locGMC_scoutTable
}
