import typing
from BaseClasses import Location
from .locs import CellLocations, SpecialLocations

class JakAndDaxterLocation(Location):
    game: str = "Jak and Daxter: The Precursor Legacy"

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
    **SpecialLocations.loc_specialTable
}
