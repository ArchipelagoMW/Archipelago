from enum import StrEnum


AP_ID_BASE = 2 ** 50


class AVItemType(StrEnum):
    COAT = "Coats"
    DRILL = "Drills"
    DRONE = "Drones"
    GLITCH = "Glitches"
    HEALTH_NODE = "Health Nodes"
    HEALTH_NODE_FRAGMENT = "Health Node Fragments"
    KEY = "Keys"
    MOVEMENT = "Movement"
    # NOTE = "Note"
    POWER_NODE = "Power Nodes"
    POWER_NODE_FRAGMENT = "Power Node Fragments"
    RANGE_NODE = "Range Nodes"
    SIZE_NODE = "Size Nodes"
    TENDRILS = "Tendrils"
    WEAPON = "Weapons"

class AVArea(StrEnum):
    ERIBU = 'Eribu'
    ABSU = 'Absu'
    ZI = 'Zi'
    KUR = 'Kur'
    INDI = 'Indi'
    UKKIN_NA = 'Ukkin-Na'
    EDIN = 'Edin'
    E_KUR_MAH = 'E-Kur-Mah'
    MAR_URU = 'Mar-Uru'


class AVRegions(StrEnum):
    # Eribu
    WEST_ERIBU = "West Eribu"
    DINGER_GISBAR = "Dinger-Gisbar"
    UPPER_ERIBU = "Upper Eribu"
    LABORATORY = "Laboratory"
    XEDUR = "Xedur"
    LOWER_ERIBU = "Lower Eribu"
    ERIBU_UKKIN_NA = "Eribu-Ukkin-Na"
    ERIBU_INDI = "Eribu-Indi"

    # Absu
    WEST_ABSU = "West Absu"
    WEST_ATTIC = "West Attic"
    EAST_ATTIC = "East Attic"
    ELSENOVA = "Elsenova"
    LOWER_ABSU = "Lower Absu"
    ABSU_BASEMENT = "Absu Basement"
    TELAL = "Telal"
    LOWER_CORRIDOR = "Lower Corridor"
    EAST_ABSU = "East Absu"
    EAST_ABSU_DRONE = "East Absu Drone"
    INDI_TUNNEL = "Indi Tunnel"

    # Absu microregions (Thanks Drone)
    EA_LEDGE = "East Absu Ledge"
    EA_BEHIND_TELAL = "Behind Telal"
    EA_ALCOVE = "East Absu Alcove"
    EA_HIDDEN_SHRINE = "Hidden Shrine"
    EA_CHASM_TUNNEL = "Chasm Tunnel"
    EA_ZI_ENTRANCE = "Zi Entrance"

    # Zi
    ABSU_ZI = "Absu-Zi"
    LOWER_ZI = "Lower Zi"
    EAST_ZI = "East Zi"
    UPPER_ZI = "Upper Zi"
    PREVIEW_ROOM = "Preview Room"
    ZI_INDI = "Zi-Indi"
    URUKU = "Uruku"
    URUKU_TOP = "Uruku Top"
    URUKU_BOTTOM = "Uruku Bottom"
    URUKU_BACK_LEDGE = "Uruku Back Ledge"

    # Kur
    LOWER_CAVES = "Lower Caves"
    UPPER_CAVES = "Upper Caves"

    GAUNTLET_ENTRANCE = "Gauntlet Entrance"
    GAUNTLET_ROOF = "Gauntlet Roof"
    GAUNTLET_REWARD = "Gauntlet Reward"

    MOUNTAIN_BASE = "Mountain Base"
    MOUNTAIN_TOP = "Mountain Top"
    MOUNTAIN_PEAK = "Mountain Peak"

    GIR_TAB_LOWER_ENTRANCE = "Gir-Tab Lower Entrance"
    GIR_TAB_UPPER_ENTRANCE = "Gir-Tab Upper Entrance"
    ABOVE_GIR_TAB = "Above Gir-Tab"
    GRAPPLE_CLIFFS = "Grapple Cliffs"

    DRONE_ODYSSEY = "Drone Odyssey"

    KUR_INDI = "Kur-Indi"
    KUR_EDIN = "Kur-Edin"

    # Indi
    INDI = "Indi"
    WEST_INDI = "West Indi"
    EAST_INDI = "East Indi"

    # Ukkin-Na
    WEST_UKKIN_NA_EXIT = "West Ukkin-Na Exit"
    UKKIN_NA_BASE = "Ukkin-Na Base"
    SOUTH_UKKIN_NA_EXIT = "South Ukkin-Na Exit"
    VISION = "Vision"
    OPHELIA = "Ophelia"
    EAST_UKKIN_NA_EXIT = "East Ukkin-Na Exit"

    # Edin
    LOWER_EDIN = "Lower Edin"
    UKHU = "Ukhu"
    CLONE = "Clone"
    HANGAR = "Hangar"
    EAST_EDIN = "East Edin"

    # E-Kur-Mah
    KEY_CHAMBER = "Key Chamber"
    UPPER_E_KUR_MAH = "Upper E-Kur-Mah"
    MID_E_KUR_MAH = "Middle E-Kur-Mah"
    LOWER_E_KUR_MAH = "Lower E-Kur-Mah"

    # Mar-Uru
    MAR_URU_ENTRANCE = "Mar-Uru Entrance"
    POST_SENTINEL = "Post Sentinel"
    SENTRY_BOT_ROOM = "Sentry Bot Room"
    ATHETOS = "Athetos"

    MENU = "Menu"
    BLURST = "Blurst"
    


START_OPTION_MAP = [
    (AVRegions.WEST_ERIBU, "Area1", "SaveRoom1"),
    (AVRegions.ELSENOVA, "Area2", "SaveRoom2"),
    (AVRegions.EAST_ABSU, "Area2", "SaveRoom4"),
    (AVRegions.LOWER_CAVES, "Area4", "SaveRoom1"),
]
