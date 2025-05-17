from BaseClasses import Location, CollectionState
from .GameID import jak1_name
from .locs import (OrbLocations as Orbs,
                   CellLocations as Cells,
                   ScoutLocations as Scouts,
                   SpecialLocations as Specials,
                   OrbCacheLocations as Caches)


class JakAndDaxterLocation(Location):
    game: str = jak1_name


# Different tables for location groups.
# Each Item ID == its corresponding Location ID. While we're here, do all the ID conversions needed.
cell_location_table = {
    **{Cells.to_ap_id(k): name for k, name in Cells.loc7SF_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locGR_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locSV_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locFJ_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locSB_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locMI_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locFC_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locRV_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locPB_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locLPC_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locBS_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locMP_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locVC_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locSC_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locSM_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locLT_cellTable.items()},
    **{Cells.to_ap_id(k): name for k, name in Cells.locGMC_cellTable.items()},
}

scout_location_table = {
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locGR_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locSV_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locFJ_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locSB_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locMI_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locFC_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locRV_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locPB_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locLPC_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locBS_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locMP_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locVC_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locSC_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locSM_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locLT_scoutTable.items()},
    **{Scouts.to_ap_id(k): name for k, name in Scouts.locGMC_scoutTable.items()},
}

special_location_table = {Specials.to_ap_id(k): name for k, name in Specials.loc_specialTable.items()}
cache_location_table = {Caches.to_ap_id(k): name for k, name in Caches.loc_orbCacheTable.items()}
orb_location_table = {Orbs.to_ap_id(k): name for k, name in Orbs.loc_orbBundleTable.items()}

# All Locations
location_table = {
    **cell_location_table,
    **scout_location_table,
    **special_location_table,
    **cache_location_table,
    **orb_location_table
}
