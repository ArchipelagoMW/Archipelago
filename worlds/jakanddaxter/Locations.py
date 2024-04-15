import typing
from BaseClasses import Location
import locs.CellLocations

class JakAndDaxterLocation(Location):
    game: str = "Jak and Daxter: The Precursor Legacy"

# All Locations
location_table = {
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
    **locGMC_cellTable
}
