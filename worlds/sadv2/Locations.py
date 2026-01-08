from BaseClasses import Location
from . import Names

class SADV2Location(Location):
    game: str = "Sonic Advance 2"

leaf_forest_locations = {
    Names.lf_sonic_1: 0x10000,
    Names.lf_sonic_2: 0x10010,
    Names.lf_sonic_boss: 0x10020,
    Names.lf_cream_1: 0x11000,
    Names.lf_cream_2: 0x11010,
    Names.lf_cream_boss: 0x11020,
    Names.lf_tails_1: 0x12000,
    Names.lf_tails_2: 0x12010,
    Names.lf_tails_boss: 0x12020,
    Names.lf_knuckles_1: 0x13000,
    Names.lf_knuckles_2: 0x13010,
    Names.lf_knuckles_boss: 0x13020,
    Names.lf_amy_1: 0x14000,
    Names.lf_amy_2: 0x14010,
    Names.lf_amy_boss: 0x14020
}

hot_crater_locations = {
    Names.hc_sonic_1: 0x10040,
    Names.hc_sonic_2: 0x10050,
    Names.hc_sonic_boss: 0x10060,
    Names.hc_cream_1: 0x11040,
    Names.hc_cream_2: 0x11050,
    Names.hc_cream_boss: 0x11060,
    Names.hc_tails_1: 0x12040,
    Names.hc_tails_2: 0x12050,
    Names.hc_tails_boss: 0x12060,
    Names.hc_knuckles_1: 0x13040,
    Names.hc_knuckles_2: 0x13050,
    Names.hc_knuckles_boss: 0x13060,
    Names.hc_amy_1: 0x14040,
    Names.hc_amy_2: 0x14050,
    Names.hc_amy_boss: 0x14060
}

music_plant_locations = {
    Names.mp_sonic_1: 0x10080,
    Names.mp_sonic_2: 0x10090,
    Names.mp_sonic_boss: 0x100a0,
    Names.mp_cream_1: 0x11080,
    Names.mp_cream_2: 0x11090,
    Names.mp_cream_boss: 0x110a0,
    Names.mp_tails_1: 0x12080,
    Names.mp_tails_2: 0x12090,
    Names.mp_tails_boss: 0x120a0,
    Names.mp_knuckles_1: 0x13080,
    Names.mp_knuckles_2: 0x13090,
    Names.mp_knuckles_boss: 0x130a0,
    Names.mp_amy_1: 0x14080,
    Names.mp_amy_2: 0x14090,
    Names.mp_amy_boss: 0x140a0
}

ice_paradise_locations = {
    Names.ip_sonic_1: 0x100c0,
    Names.ip_sonic_2: 0x100d0,
    Names.ip_sonic_boss: 0x100e0,
    Names.ip_cream_1: 0x110c0,
    Names.ip_cream_2: 0x110d0,
    Names.ip_cream_boss: 0x110e0,
    Names.ip_tails_1: 0x120c0,
    Names.ip_tails_2: 0x120d0,
    Names.ip_tails_boss: 0x120e0,
    Names.ip_knuckles_1: 0x130c0,
    Names.ip_knuckles_2: 0x130d0,
    Names.ip_knuckles_boss: 0x130e0,
    Names.ip_amy_1: 0x140c0,
    Names.ip_amy_2: 0x140d0,
    Names.ip_amy_boss: 0x140e0
}

sky_canyon_locations = {
    Names.sc_sonic_1: 0x10100,
    Names.sc_sonic_2: 0x10110,
    Names.sc_sonic_boss: 0x10120,
    Names.sc_cream_1: 0x11100,
    Names.sc_cream_2: 0x11110,
    Names.sc_cream_boss: 0x11120,
    Names.sc_tails_1: 0x12100,
    Names.sc_tails_2: 0x12110,
    Names.sc_tails_boss: 0x12120,
    Names.sc_knuckles_1: 0x13100,
    Names.sc_knuckles_2: 0x13110,
    Names.sc_knuckles_boss: 0x13120,
    Names.sc_amy_1: 0x14100,
    Names.sc_amy_2: 0x14110,
    Names.sc_amy_boss: 0x14120
}

techno_base_locations = {
    Names.tb_sonic_1: 0x10140,
    Names.tb_sonic_2: 0x10150,
    Names.tb_sonic_boss: 0x10160,
    Names.tb_cream_1: 0x11140,
    Names.tb_cream_2: 0x11150,
    Names.tb_cream_boss: 0x11160,
    Names.tb_tails_1: 0x12140,
    Names.tb_tails_2: 0x12150,
    Names.tb_tails_boss: 0x12160,
    Names.tb_knuckles_1: 0x13140,
    Names.tb_knuckles_2: 0x13150,
    Names.tb_knuckles_boss: 0x13160,
    Names.tb_amy_1: 0x14140,
    Names.tb_amy_2: 0x14150,
    Names.tb_amy_boss: 0x14160
}

egg_utopia_locations = {
    Names.eu_sonic_1: 0x10180,
    Names.eu_sonic_2: 0x10190,
    Names.eu_sonic_boss: 0x101a0,
    Names.eu_cream_1: 0x11180,
    Names.eu_cream_2: 0x11190,
    Names.eu_cream_boss: 0x111a0,
    Names.eu_tails_1: 0x12180,
    Names.eu_tails_2: 0x12190,
    Names.eu_tails_boss: 0x121a0,
    Names.eu_knuckles_1: 0x13180,
    Names.eu_knuckles_2: 0x13190,
    Names.eu_knuckles_boss: 0x131a0,
    Names.eu_amy_1: 0x14180,
    Names.eu_amy_2: 0x14190,
    Names.eu_amy_boss: 0x141a0
}

xx_locations = {
    Names.xx_sonic: 0x101c0,
    Names.xx_cream: 0x111c0,
    Names.xx_tails: 0x121c0,
    Names.xx_knuckles: 0x131c0,
    Names.xx_amy: 0x141c0
}

event_locations = {
    "True Area 53": None
}

all_locations = {
    **leaf_forest_locations,
    **hot_crater_locations,
    **music_plant_locations,
    **ice_paradise_locations,
    **sky_canyon_locations,
    **techno_base_locations,
    **egg_utopia_locations,
    **xx_locations
}