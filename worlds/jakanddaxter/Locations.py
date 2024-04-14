import typing
import locs.CellLocations
import locs.ScoutLocations
from BaseClasses import Location

class JakAndDaxterLocation(Location):
    game: str = "Jak and Daxter: The Precursor Legacy"

# All Locations
location_cellTable = {
    **locGR_cellTable, \
    **locSV_cellTable, \
    **locFJ_cellTable, \
    **locSB_cellTable, \
    **locMI_cellTable, \
    **locFC_cellTable, \
    **locRV_cellTable, \
    **locPB_cellTable, \
    **locLPC_cellTable, \
    **locBS_cellTable, \
    **locMP_cellTable, \
    **locVC_cellTable, \
    **locSC_cellTable, \
    **locSM_cellTable, \
    **locLT_cellTable, \
    **locGMC_cellTable, \
    **locGR_scoutTable, \
    **locSV_scoutTable, \
    **locFJ_scoutTable, \
    **locSB_scoutTable, \
    **locMI_scoutTable, \
    **locFC_scoutTable, \
    **locRV_scoutTable, \
    **locPB_scoutTable, \
    **locLPC_scoutTable, \
    **locBS_scoutTable, \
    **locMP_scoutTable, \
    **locVC_scoutTable, \
    **locSC_scoutTable, \
    **locSM_scoutTable, \
    **locLT_scoutTable, \
    **locGMC_scoutTable
}
