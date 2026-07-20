from BaseClasses import Location
from .game_id import jak1_name
from .locs import (orb_locations as orbs,
                   cell_locations as cells,
                   scout_locations as scouts,
                   special_locations as specials,
                   orb_cache_locations as caches)


class JakAndDaxterLocation(Location):
    game: str = jak1_name


# Different tables for location groups.
# Each Item ID == its corresponding Location ID. While we're here, do all the ID conversions needed.
cell_location_table = {
    **{cells.to_ap_id(k): name for k, name in cells.loc7SF_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locGR_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locSV_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locFJ_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locSB_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locMI_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locFC_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locRV_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locPB_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locLPC_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locBS_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locMP_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locVC_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locSC_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locSM_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locLT_cellTable.items()},
    **{cells.to_ap_id(k): name for k, name in cells.locGMC_cellTable.items()},
}

scout_location_table = {
    **{scouts.to_ap_id(k): name for k, name in scouts.locGR_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locSV_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locFJ_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locSB_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locMI_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locFC_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locRV_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locPB_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locLPC_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locBS_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locMP_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locVC_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locSC_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locSM_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locLT_scoutTable.items()},
    **{scouts.to_ap_id(k): name for k, name in scouts.locGMC_scoutTable.items()},
}

special_location_table = {specials.to_ap_id(k): name for k, name in specials.loc_specialTable.items()}
cache_location_table = {caches.to_ap_id(k): name for k, name in caches.loc_orbCacheTable.items()}
orb_location_table = {orbs.to_ap_id(k): name for k, name in orbs.loc_orbBundleTable.items()}

# All Locations
location_table = {
    **cell_location_table,
    **scout_location_table,
    **special_location_table,
    **cache_location_table,
    **orb_location_table
}
