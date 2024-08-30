from BaseClasses import Location, CollectionState
from .GameID import jak1_name
from .locs import (OrbLocations as Orbs,
                   CellLocations as Cells,
                   ScoutLocations as Scouts,
                   SpecialLocations as Specials,
                   OrbCacheLocations as Caches)


class JakAndDaxterLocation(Location):
    game: str = jak1_name

    # In AP 0.5.0, the base Location.can_reach function had its two boolean conditions swapped for a faster
    # short-circuit for better performance. However, Jak seeds actually generate faster using the older method,
    # which has been re-implemented below.
    def can_reach(self, state: CollectionState) -> bool:
        assert self.parent_region, "Can't reach location without region"
        return self.parent_region.can_reach(state) and self.access_rule(state)


# Different tables for location groups.
# Each Item ID == its corresponding Location ID. While we're here, do all the ID conversions needed.
cell_location_table = {
    **{Cells.to_ap_id(k): Cells.loc7SF_cellTable[k] for k in Cells.loc7SF_cellTable},
    **{Cells.to_ap_id(k): Cells.locGR_cellTable[k] for k in Cells.locGR_cellTable},
    **{Cells.to_ap_id(k): Cells.locSV_cellTable[k] for k in Cells.locSV_cellTable},
    **{Cells.to_ap_id(k): Cells.locFJ_cellTable[k] for k in Cells.locFJ_cellTable},
    **{Cells.to_ap_id(k): Cells.locSB_cellTable[k] for k in Cells.locSB_cellTable},
    **{Cells.to_ap_id(k): Cells.locMI_cellTable[k] for k in Cells.locMI_cellTable},
    **{Cells.to_ap_id(k): Cells.locFC_cellTable[k] for k in Cells.locFC_cellTable},
    **{Cells.to_ap_id(k): Cells.locRV_cellTable[k] for k in Cells.locRV_cellTable},
    **{Cells.to_ap_id(k): Cells.locPB_cellTable[k] for k in Cells.locPB_cellTable},
    **{Cells.to_ap_id(k): Cells.locLPC_cellTable[k] for k in Cells.locLPC_cellTable},
    **{Cells.to_ap_id(k): Cells.locBS_cellTable[k] for k in Cells.locBS_cellTable},
    **{Cells.to_ap_id(k): Cells.locMP_cellTable[k] for k in Cells.locMP_cellTable},
    **{Cells.to_ap_id(k): Cells.locVC_cellTable[k] for k in Cells.locVC_cellTable},
    **{Cells.to_ap_id(k): Cells.locSC_cellTable[k] for k in Cells.locSC_cellTable},
    **{Cells.to_ap_id(k): Cells.locSM_cellTable[k] for k in Cells.locSM_cellTable},
    **{Cells.to_ap_id(k): Cells.locLT_cellTable[k] for k in Cells.locLT_cellTable},
    **{Cells.to_ap_id(k): Cells.locGMC_cellTable[k] for k in Cells.locGMC_cellTable}
}

scout_location_table = {
    **{Scouts.to_ap_id(k): Scouts.locGR_scoutTable[k] for k in Scouts.locGR_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locSV_scoutTable[k] for k in Scouts.locSV_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locFJ_scoutTable[k] for k in Scouts.locFJ_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locSB_scoutTable[k] for k in Scouts.locSB_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locMI_scoutTable[k] for k in Scouts.locMI_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locFC_scoutTable[k] for k in Scouts.locFC_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locRV_scoutTable[k] for k in Scouts.locRV_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locPB_scoutTable[k] for k in Scouts.locPB_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locLPC_scoutTable[k] for k in Scouts.locLPC_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locBS_scoutTable[k] for k in Scouts.locBS_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locMP_scoutTable[k] for k in Scouts.locMP_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locVC_scoutTable[k] for k in Scouts.locVC_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locSC_scoutTable[k] for k in Scouts.locSC_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locSM_scoutTable[k] for k in Scouts.locSM_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locLT_scoutTable[k] for k in Scouts.locLT_scoutTable},
    **{Scouts.to_ap_id(k): Scouts.locGMC_scoutTable[k] for k in Scouts.locGMC_scoutTable}
}

special_location_table = {Specials.to_ap_id(k): Specials.loc_specialTable[k] for k in Specials.loc_specialTable}
cache_location_table = {Caches.to_ap_id(k): Caches.loc_orbCacheTable[k] for k in Caches.loc_orbCacheTable}
orb_location_table = {Orbs.to_ap_id(k): Orbs.loc_orbBundleTable[k] for k in Orbs.loc_orbBundleTable}

# All Locations
location_table = {
    **cell_location_table,
    **scout_location_table,
    **special_location_table,
    **cache_location_table,
    **orb_location_table
}
