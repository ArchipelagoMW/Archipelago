from typing import Dict, NamedTuple, Optional

from BaseClasses import Location
from .Names import LocationName
from .Names import RegionName

gatoroboto_base_id: int = 10000

class GatoRobotoLocation(Location):
    game = "Gato Roboto"

class GatoRobotoLocationData(NamedTuple):
    region: str
    address: Optional[int] = None

healthkit_location_data_table: Dict[str, GatoRobotoLocationData] = {
    LocationName.loc_healthkit_landing_site_west:
        GatoRobotoLocationData(RegionName.region_landing_site, gatoroboto_base_id + 408),
    LocationName.loc_healthkit_landing_site_east:
        GatoRobotoLocationData(RegionName.region_landing_site, gatoroboto_base_id + 1812),
    LocationName.loc_healthkit_nexus_west:
        GatoRobotoLocationData(RegionName.region_nexus, gatoroboto_base_id + 1014),
    LocationName.loc_healthkit_nexus_east:
        GatoRobotoLocationData(RegionName.region_nexus, gatoroboto_base_id + 2314),
    LocationName.loc_healthkit_aqueducts_west:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 406),
    LocationName.loc_healthkit_aqueducts_east:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 1606),
    LocationName.loc_healthkit_heater_core_west:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 417),
    LocationName.loc_healthkit_heater_core_east:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 1713),
    LocationName.loc_healthkit_ventilation:
        GatoRobotoLocationData(RegionName.region_ventilation, gatoroboto_base_id + 815),
    LocationName.loc_healthkit_incubator:
        GatoRobotoLocationData(RegionName.region_incubator, gatoroboto_base_id + 2413),
}

cartridge_location_data_table: Dict[str, GatoRobotoLocationData] = {
    LocationName.loc_cartridge_bark:
        GatoRobotoLocationData(RegionName.region_landing_site, gatoroboto_base_id + 710),
    LocationName.loc_cartridge_nicotine:
        GatoRobotoLocationData(RegionName.region_landing_site, gatoroboto_base_id + 1810),
    LocationName.loc_cartridge_coffee_stain:
        GatoRobotoLocationData(RegionName.region_nexus, gatoroboto_base_id + 914),
    LocationName.loc_cartridge_urine:
        GatoRobotoLocationData(RegionName.region_nexus, gatoroboto_base_id + 1413),
    LocationName.loc_cartridge_swamp_matcha:
        GatoRobotoLocationData(RegionName.region_nexus, gatoroboto_base_id + 2113),
    LocationName.loc_cartridge_port:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 1106),
    LocationName.loc_cartridge_goop:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 707),
    LocationName.loc_cartridge_starboard:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 2106),
    LocationName.loc_cartridge_virtual_cat:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 1318),
    LocationName.loc_cartridge_meowtrix:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 414),
    LocationName.loc_cartridge_chewed_gum:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 1916),
    LocationName.loc_cartridge_gris:
        GatoRobotoLocationData(RegionName.region_ventilation, gatoroboto_base_id + 1613),
    LocationName.loc_cartridge_grape:
        GatoRobotoLocationData(RegionName.region_ventilation, gatoroboto_base_id + 517),
    LocationName.loc_cartridge_tamagato:
        GatoRobotoLocationData(RegionName.region_incubator, gatoroboto_base_id + 1513),
}

module_location_data_table: Dict[str, GatoRobotoLocationData] = {
    LocationName.loc_module_missile:
        GatoRobotoLocationData(RegionName.region_landing_site, gatoroboto_base_id + 814),
    LocationName.loc_module_decoder:
        GatoRobotoLocationData(RegionName.region_landing_site, gatoroboto_base_id + 807),
    LocationName.loc_module_repeater:
        GatoRobotoLocationData(RegionName.region_nexus, gatoroboto_base_id + 1716),
    LocationName.loc_module_hopper:
        GatoRobotoLocationData(RegionName.region_nexus, gatoroboto_base_id + 11716),
    LocationName.loc_module_spinjump:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 2410),
    LocationName.loc_module_coolant:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 113),
    LocationName.loc_module_phase:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 1114),
    LocationName.loc_module_bigshot:
        GatoRobotoLocationData(RegionName.region_ventilation, gatoroboto_base_id + 1718),
}

event_location_data_table: Dict[str, GatoRobotoLocationData] = {
    LocationName.loc_progressive_aqueducts_1:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 204),
    LocationName.loc_progressive_aqueducts_2:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 1603),
    LocationName.loc_progressive_aqueducts_3:
        GatoRobotoLocationData(RegionName.region_aqueducts, gatoroboto_base_id + 1908),
    LocationName.loc_progressive_heater_core_1:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 19),
    LocationName.loc_progressive_heater_core_2:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 313),
    LocationName.loc_progressive_heater_core_3:
        GatoRobotoLocationData(RegionName.region_heater_core, gatoroboto_base_id + 15),
    LocationName.loc_progressive_ventilation_1:
        GatoRobotoLocationData(RegionName.region_ventilation, gatoroboto_base_id + 1113),
    LocationName.loc_progressive_ventilation_2:
        GatoRobotoLocationData(RegionName.region_ventilation, gatoroboto_base_id + 1122),
    LocationName.loc_progressive_ventilation_3:
        GatoRobotoLocationData(RegionName.region_ventilation, gatoroboto_base_id + 521)
}

victory_location_data_table: Dict[str, GatoRobotoLocationData] = {
    LocationName.loc_victory:
        GatoRobotoLocationData(RegionName.region_laboratory, gatoroboto_base_id + 1319)
}

location_data_table: Dict[str, GatoRobotoLocationData] = {
    **healthkit_location_data_table,
    **cartridge_location_data_table,
    **module_location_data_table,
    **event_location_data_table,
    **victory_location_data_table
}

location_table = {name: data.address for name, data in location_data_table.items()}