from BaseClasses import Location
from .GameID import game_id, game_name, cell_offset, fly_offset
from .locs import CellLocations, ScoutLocations


class JakAndDaxterLocation(Location):
    game: str = game_name


# All Locations
# Because all items in Jak And Daxter are unique and do not regenerate, we can use this same table as our item table.
# Each Item ID == its corresponding Location ID.  And then we only have to do this ugly math once.
location_table = {
    **{game_id + cell_offset + k: CellLocations.locGR_cellTable[k]
       for k in CellLocations.locGR_cellTable},
    **{game_id + cell_offset + k: CellLocations.locSV_cellTable[k]
       for k in CellLocations.locSV_cellTable},
    **{game_id + cell_offset + k: CellLocations.locFJ_cellTable[k]
       for k in CellLocations.locFJ_cellTable},
    **{game_id + cell_offset + k: CellLocations.locSB_cellTable[k]
       for k in CellLocations.locSB_cellTable},
    **{game_id + cell_offset + k: CellLocations.locMI_cellTable[k]
       for k in CellLocations.locMI_cellTable},
    **{game_id + cell_offset + k: CellLocations.locFC_cellTable[k]
       for k in CellLocations.locFC_cellTable},
    **{game_id + cell_offset + k: CellLocations.locRV_cellTable[k]
       for k in CellLocations.locRV_cellTable},
    **{game_id + cell_offset + k: CellLocations.locPB_cellTable[k]
       for k in CellLocations.locPB_cellTable},
    **{game_id + cell_offset + k: CellLocations.locLPC_cellTable[k]
       for k in CellLocations.locLPC_cellTable},
    **{game_id + cell_offset + k: CellLocations.locBS_cellTable[k]
       for k in CellLocations.locBS_cellTable},
    **{game_id + cell_offset + k: CellLocations.locMP_cellTable[k]
       for k in CellLocations.locMP_cellTable},
    **{game_id + cell_offset + k: CellLocations.locVC_cellTable[k]
       for k in CellLocations.locVC_cellTable},
    **{game_id + cell_offset + k: CellLocations.locSC_cellTable[k]
       for k in CellLocations.locSC_cellTable},
    **{game_id + cell_offset + k: CellLocations.locSM_cellTable[k]
       for k in CellLocations.locSM_cellTable},
    **{game_id + cell_offset + k: CellLocations.locLT_cellTable[k]
       for k in CellLocations.locLT_cellTable},
    **{game_id + cell_offset + k: CellLocations.locGMC_cellTable[k]
       for k in CellLocations.locGMC_cellTable},
    **{game_id + fly_offset + k: ScoutLocations.locGR_scoutTable[k]
       for k in ScoutLocations.locGR_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locSV_scoutTable[k]
       for k in ScoutLocations.locSV_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locFJ_scoutTable[k]
       for k in ScoutLocations.locFJ_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locSB_scoutTable[k]
       for k in ScoutLocations.locSB_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locMI_scoutTable[k]
       for k in ScoutLocations.locMI_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locFC_scoutTable[k]
       for k in ScoutLocations.locFC_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locRV_scoutTable[k]
       for k in ScoutLocations.locRV_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locPB_scoutTable[k]
       for k in ScoutLocations.locPB_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locLPC_scoutTable[k]
       for k in ScoutLocations.locLPC_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locBS_scoutTable[k]
       for k in ScoutLocations.locBS_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locMP_scoutTable[k]
       for k in ScoutLocations.locMP_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locVC_scoutTable[k]
       for k in ScoutLocations.locVC_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locSC_scoutTable[k]
       for k in ScoutLocations.locSC_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locSM_scoutTable[k]
       for k in ScoutLocations.locSM_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locLT_scoutTable[k]
       for k in ScoutLocations.locLT_scoutTable},
    **{game_id + fly_offset + k: ScoutLocations.locGMC_scoutTable[k]
       for k in ScoutLocations.locGMC_scoutTable}
}
