from typing import Dict, List, NamedTuple
from .Names import RegionName

class GatoRobotoRegionData(NamedTuple):
    connecting_regions: List[str] = []
    

region_data_table: Dict[str, GatoRobotoRegionData] = {
    RegionName.region_menu: GatoRobotoRegionData([RegionName.region_landing_site]),
    RegionName.region_landing_site: GatoRobotoRegionData([RegionName.region_nexus]),
    RegionName.region_nexus: GatoRobotoRegionData([RegionName.region_aqueducts,
                                               RegionName.region_heater_core,
                                               RegionName.region_ventilation,
                                               RegionName.region_incubator]),
    RegionName.region_aqueducts: GatoRobotoRegionData(),
    RegionName.region_heater_core: GatoRobotoRegionData(),
    RegionName.region_ventilation: GatoRobotoRegionData(),
    RegionName.region_incubator: GatoRobotoRegionData([RegionName.region_laboratory]),
    RegionName.region_laboratory: GatoRobotoRegionData()
}