from __future__ import annotations

import json
from enum import Enum

from .._resources import resource

with resource('datasets', 'sources', 'unit_projectile_info.json').open() as file:
    # Open projectiles source-file for raw data. Used in `ProjectileInfo.get_unit_projectile(...)`
    _unit_projectile_info: dict = json.load(file)


class ProjectileInfo(Enum):
    """
    This enum class provides information about the projectiles in the game. Information about the following properties
    of a projectile is found in this class:

     - Projectile ID
     - The units that use the projectile

    **Methods**
    >>> ProjectileInfo.from_id()
    >>> ProjectileInfo.get_unit_projectile()

    **Examples**

    >>> ProjectileInfo.SCORPION_FIRE.ID
    >>> 628

    >>> ProjectileInfo.SCORPION_FIRE.USED_BY
    >>> (542,)
    """

    @property
    def ID(self) -> int:
        """
        Returns:
            The ID of the specified projectile unit
        """
        return self.value[0]

    @property
    def USED_BY(self) -> tuple[int]:
        """
        Returns:
            A tuple of unit IDs that use the specified projectile unit
        """
        return self.value[1]

    @classmethod
    def from_id(cls, projectile_id: int) -> ProjectileInfo:
        """
        Get the ProjectileInfo object from its ID

        Args:
            projectile_id: The ID of the projectile to get the ProjectileInfo of

        Returns:
            A ProjectileInfo object of the specified projectile ID
        """
        if type(projectile_id) is not int:
            raise TypeError(f"from_id expected int, got {type(projectile_id)}")
        if projectile_id == -1:
            raise ValueError("-1 is not a valid projectile ID")

        for projectile in cls._member_map_.values():
            if projectile.value[0] == projectile_id:
                return projectile

        raise KeyError(f"A projectile unit with ID '{projectile_id}' was not found in the dataset")

    @staticmethod
    def get_unit_projectile(unit_const: int, has_chemistry: bool = False, secondary: bool = False) -> ProjectileInfo:

        """
        Get the projectile object based on unit const

        Args:
            unit_const: The unit to find the projectile of
            has_chemistry: If you want the fire (chemistry) version (if it exists)
            secondary: If you want the secondary projectile version (if it exists)

        Returns:
            The ProjectileInfo corresponding to the given unit and params or None if nothing was found
        """

        if type(unit_const) is not int:
            raise TypeError(f"unit const expected int, got {type(unit_const)}")
        if unit_const < 0:
            raise ValueError(f"{unit_const} is not a valid unit constant")

        projectile = "secondary" if secondary else "primary"
        fire = "_fire" if has_chemistry else ""
        projectile_id = _unit_projectile_info.get(str(unit_const), {}).get(projectile + fire, -1)

        return ProjectileInfo.from_id(projectile_id) if projectile_id != -1 else None

    ARROW = 9, ()
    VOL = 54, (71, 109, 141, 142, 484, 597, 617, 621, 2275, 2276, 2277)
    ARROW1 = 97, ()
    SLINGER = 187, (185, 1075, 2320, 2463)
    CATST = 242, ()
    CATSF = 244, ()
    BOLTX = 245, ()
    BOLTF = 246, ()
    ARROW2 = 312, ()
    TREBST = 313, ()
    MANGST = 314, ()
    ARROW3 = 315, ()
    ARROW4 = 316, ()
    ARROW5 = 317, ()
    ARROW6 = 318, ()
    ARROW7 = 319, ()
    ARROW8 = 320, ()
    ARROW9 = 321, ()
    ARROW10 = 322, ()
    CATST1 = 323, ()
    CATST2 = 324, ()
    CATST3 = 325, ()
    CATST4 = 326, ()
    CATST5 = 327, ()
    VOL_FIRE = 328, (71, 109, 141, 142, 484, 597, 617, 621, 2275, 2276, 2277)
    ARW_FLM = 360, ()
    ARC = 363, (4, 158, 571, 598, 2415, 2417, 2443)
    CROSSBOWMAN = 364, (24, 493, 866, 868, 926, 930, 1072, 1106, 1166, 1294, 1297, 1759, 1761, 2174, 2175, 2468)
    CRS = 365, (7, 2562, 2564)
    HCS = 366, (6, 583, 596, 1010, 1012, 1036, 1079, 1155, 2328, 2332, 2460, 2470)
    SCORPION = 367, (279,)
    BOMBARD_CANNON = 368, (36, 644, 650, 1709)
    MANGONEL_SECONDARY = 369, (280, 550, 588, 1923, 2138, 2139)
    TREBUCHET = 371, (42, 682, 683, 1690)
    GAL = 372, (21,)
    WAR_GALLEY = 373, (442, 827, 829, 1750, 2339)
    CANNON_GALLEON = 374, (420, 691)
    COM_FIRE = 375, (24, 493, 866, 868, 926, 930, 1072, 1106, 1166, 1294, 1297, 1759, 1761, 2174, 2175, 2468)
    CRS_FIRE = 376, (7, 2562, 2564)
    HCS_FIRE = 377, (6, 583, 596, 1010, 1012, 1036, 1079, 1155, 2328, 2332, 2460, 2470)
    SCORPION_FIRE = 378, (279,)
    GUNPOWDER_PRIMARY = 380, (5, 46, 52, 203, 425, 427, 557, 748, 771, 773, 1068)
    BOLTXF = 381, ()
    BOLTF1 = 385, ()
    MNG_FLM = 462, ()
    ARC_FIRE = 466, (4, 158, 571, 598, 2415, 2417, 2443)
    MANGONEL_SECONDARY_FIRE = 468, (280, 550, 588, 1923, 2138, 2139)
    TREBUCHET_FIRE = 469, (42, 682, 683, 1690)
    GALLEY_FIRE = 470, (21,)
    WAR_GALLEY_FIRE = 471, (442, 827, 829, 1750, 2339)
    HAR_FIRE = 475, (11, 39, 172, 561, 577, 731, 1007, 1009, 1034, 1231, 1233, 1259, 1260, 1261, 1269, 1275, 1276, 1769,
                     1771, 1772, 1952, 2042, 2046, 2485, 2700, 2701)
    HHA_FIRE = 476, (437, 474, 698, 943, 1267, 1303, 2308, 2486)
    HAR = 477, (11, 39, 172, 561, 577, 731, 1007, 1009, 1034, 1231, 1233, 1259, 1260, 1261, 1269, 1275, 1276, 1769,
                1771, 1772, 1952, 2042, 2046, 2485, 2700, 2701)
    HHA = 478, (437, 474, 698, 943, 1267, 1303, 2308, 2486)
    T_ARO = 485, ()
    WTN = 503, (1800, 1802)
    ARROW_GUARD_TOWER = 504, (79, 234, 235, 566, 785, 1665)
    KEP = 505, (79, 234, 235, 684, 685, 785, 1102, 1665)
    BTW = 506, (236,)
    ACA = 507, (492, 642, 686, 1182, 2324, 2474)
    DROMON = 508, (1795,)
    VIL = 509, (122, 216)
    CKN = 510, (73, 559, 1073, 1231, 1233, 1260, 2042)
    LONGBOWMAN = 511, (8, 200, 530, 763, 765, 850, 1069, 1129, 1131, 2326, 2388, 2389, 2419, 2420, 2464, 2473, 2727)
    LBT = 512, (21, 106, 250, 442, 533, 539, 778, 885, 2117, 2118, 2119, 2141, 2142, 2143, 2172, 2728)
    MSU = 513, ()
    MPC = 514, ()
    TAX = 515, (165, 281, 424, 531, 931, 1298)
    WTN_FIRE = 516, (1800, 1802)
    GTW_FIRE = 517, (79, 234, 235, 566, 785, 1665)
    KEP_FIRE = 518, (79, 234, 235, 684, 685, 785, 1102, 1665)
    ACA_FIRE = 519, (492, 642, 686, 1182, 2324, 2474)
    DROMON_FIRE = 520, (1795,)
    VIL_FIRE = 521, (122, 216)
    CKN_FIRE = 522, (73, 559, 1073, 1231, 1233, 1260, 2042)
    LBM_FIRE = 523, (8, 200, 530, 763, 765, 850, 1069, 1129, 1131, 2326, 2388, 2389, 2419, 2420, 2464, 2473, 2727)
    LBT_FIRE = 524, (21, 106, 250, 442, 533, 539, 778, 885, 2117, 2118, 2119, 2141, 2142, 2143, 2172, 2728)
    MPC_FIRE = 525, ()
    MSU_FIRE = 526, ()
    BTW_FIRE = 537, (236,)
    SLINGER_FIRE = 538, (185, 1075, 2320, 2463)
    SGY = 540, (2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2135, 2311)
    SGY_FIRE = 541, (2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2135, 2311)
    ONAGER = 551, ()
    ONAGER_FIRE = 552, ()
    HEAVY_SCORPION = 627, (542,)
    HEAVY_SCORPION_FIRE = 628, (542,)
    MANGONEL_PRIMARY = 656, (280, 550, 588, 2138, 2139)
    GP1 = 657, ()
    MANGONEL_PRIMARY_FIRE = 658, (280, 550, 588, 2138, 2139)
    FIRE_SHIP = 676, (188, 190, 529, 532, 938, 1103, 1302, 2123, 2124, 2125, 2126)
    MLK = 736, (282, 556, 929, 1296)
    CST = 746, (33, 82, 445, 2418, 2600)
    CST_FIRE = 747, (33, 82, 445, 2418, 2600)
    CGX = 767, (831, 832, 844, 1631)
    KREPOST = 786, (1251,)
    KREPOST_FIRE = 787, (1251,)
    KNIFE = 1055, (1013, 1015, 1066)
    CVB = 1057, (1004, 1006)
    CVB_FIRE = 1058, (1004, 1006)
    LBOL = 1111, ()
    LBOL_FIRE = 1112, ()
    HEAVY_SCORPION_UNUSED = 1113, ()
    HEAVY_SCORPION_FIRE_UNUSED = 1114, ()
    HUSSITE_WAGON_SECONDARY = 1119, (203, 1704, 1706)
    BALLISTA_ELEPHANT = 1167, (1120, 1122)
    BALLISTA_ELEPHANT_FIRE = 1168, (1120, 1122)
    ARAMBAI = 1169, (1126, 1128)
    ARAMBAI_FIRE = 1170, (1126, 1128)
    SHCOW = 1223, ()
    LASER = 1595, (1222, 1577)
    HUSSITE_WAGON = 1733, (1704, 1706)
    CHAKRAM = 1756, (1741,)
    THRSD = 1779, (1750,)
    THRSD_FIRE = 1780, (1750,)
    ELEAR = 1781, (873, 875)
    ELEAR_FIRE = 1782, (873, 875)
    ORGAN_GUN = 1789, (1001, 1003)
    DROMON_GREEK_FIRE = 1798, (1795,)
    CITADELS = 1830, (33, 82, 445, 2418, 2600)
    SVT = 1867, (79, 234, 235, 566, 684, 685, 785, 1102, 1665)
    SVT_FIRE = 1868, (79, 234, 235, 566, 684, 685, 785, 1102, 1665)
    LEVIATHAN = 2226, (2140, 2442, 2448)
    GASTRAPHETES = 2307, ()
    POLYCRITUS = 2342, (2319,)
    ELITECHAKRAM = 1783, (1743,)
    LCHUAN_ROCKET = 1879, (1948,)
    ROCKET_CART = 1906, (831, 832, 844, 1904, 1907)
    GRENADIER = 1913, (1911,)
    FIRE_LANCER = 1925, (1901, 1903)
    MOUNTED_TREBUCHET = 1926, (1923,)
    MOUNTED_TREBUCHET_FIRE = 1927, (1923,)
    CROSSBOWMAN_SECONDARY = 1930, (4, 24, 492)
    ZHOUYU = 1931, (2044,)
    TRACTION = 1932, (1942, 2633)
    TRACTION_FIRE = 1933, (1942, 2633)
    TRACTION_SECONDARY = 1934, (1942, 1948)
    TRACTION_SECONDARY_FIRE = 1935, (1942, 1948)
    LCHUAN_CHARGE = 1936, (1948,)
    LCHUAN_FIRE_CHARGE = 1937, (1948,)
    LCHUAN = 1938, (1948,)
    LCHUAN_FIRE = 1939, (1948,)
    WAR_CHARIOT_BARRAGE = 1957, (1980,)
    WAR_CHARIOT_FOCUS_FIRE = 1964, (1962, 2049)
    FIRE_ARCHER = 1971, (1968, 1970)
    FIRE_ARCHER_RED_CLIFFS = 1972, (1968, 1970, 2044)
    XIANBEI = 1982, (1952, 2046)
    LUBU = 2056, (2061,)
    GSTRIKE = 2057, (2065,)
    SUNQUAN = 2062, (2063,)
    XIANBEI_SECONDARY = 1983, (1952,)
    HELEPOLIS = 2445, (2444,)
    CHURCH = 1548, (1806,)
    BOLAS = 2572, (2569,)
    ELITEBOLAS = 2573, (2571,)
    BOLAS_CHARGE = 2574, (2569,)
    ELITEBOLAS_CHARGE = 2575, (2571,)
    BLACKWOOD_ARCHER = 2608, (2579,)
    ELITE_BLACKWOOD_ARCHER = 2609, (2581, 2642)
    FIRE_SHIP_CHARGE = 2629, (529, 532, 938, 1103, 1302)
    DOCK = 2631, (45, 47, 51, 133, 1189)
    DOCK_FIRE = 2632, (45, 47, 51, 133, 1189)
    HOOK = 2636, (2626, 2627, 2628)
    HARALD = 2623, (2721,)
    HEARTH_TROOP = 2702, (2705,)
    ELITE_HEARTH_TROOP = 2707, (2706,)
    GOTHIKON = 2710, ()
    JOMSVIKING = 2713, (2711, 2712)
    JARL = 2719, (426, 2708)
    ELITEJARL = 2720, (2709,)
