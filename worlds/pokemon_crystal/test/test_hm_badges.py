from .bases import PokemonCrystalTestBase, verify_region_access

cut_regions = [
    "REGION_LAKE_OF_RAGE:CUT",
    "REGION_ROUTE_42:CENTERFRUIT",
    "REGION_ROUTE_43:FRUITTREE",
    "REGION_ROUTE_2:SOUTHEAST",
    "REGION_CELADON_GYM"
]

fly_regions = [
    "REGION_FLY"
]

surf_regions = [
    "REGION_CIANWOOD_CITY",
    "REGION_ROUTE_34:WATER",
    "REGION_ROUTE_40:WATER",
    "REGION_ROUTE_41",
    "REGION_ROUTE_42:CENTER",
    "REGION_LAKE_OF_RAGE:WATER",
    "REGION_ROUTE_43:FRUITTREE",
    "REGION_CINNABAR_ISLAND",
    "REGION_ROUTE_19",
    "REGION_ROUTE_20",
    "REGION_ROUTE_21",
    "REGION_RUINS_OF_ALPH_HO_OH_ITEM_ROOM"
]

strength_regions = [
    "REGION_RUINS_OF_ALPH_OMANYTE_ITEM_ROOM",
    "REGION_SLOWPOKE_WELL_B2F",
    "REGION_CIANWOOD_GYM:STRENGTH",
    "REGION_BLACKTHORN_GYM_1F:STRENGTH"
]

flash_regions = [
    "REGION_DARK_CAVE_VIOLET_ENTRANCE:WEST",
    "REGION_DARK_CAVE_VIOLET_ENTRANCE:EAST",
    "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_EAST",
    "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTH_EAST",
    "REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTH_WEST",
    "REGION_RUINS_OF_ALPH_AERODACTYL_ITEM_ROOM",
    "REGION_WHIRL_ISLAND_NW",
    "REGION_WHIRL_ISLAND_NE",
    "REGION_WHIRL_ISLAND_SW",
    "REGION_WHIRL_ISLAND_SE",
    "REGION_WHIRL_ISLAND_B1F",
    "REGION_WHIRL_ISLAND_B2F",
    "REGION_ROCK_TUNNEL_1F",
    "REGION_ROCK_TUNNEL_B1F",
    "REGION_SILVER_CAVE_ROOM_1",
    "REGION_SILVER_CAVE_ROOM_2",
    "REGION_SILVER_CAVE_ROOM_3"
]

whirlpool_regions = [
    "REGION_WHIRL_ISLAND_NW",
    "REGION_WHIRL_ISLAND_NE",
    "REGION_WHIRL_ISLAND_SW",
    "REGION_WHIRL_ISLAND_SE",
    "REGION_WHIRL_ISLAND_B1F",
    "REGION_WHIRL_ISLAND_B2F",
    "REGION_DRAGONS_DEN_B1F:WHIRLPOOL",
    "REGION_ROUTE_27:EASTWHIRLPOOL"
]

waterfall_regions = [
    "REGION_MOUNT_MORTAR_2F_OUTSIDE",
    "REGION_MOUNT_MORTAR_1F_INSIDE:BACK"
]


class VanillaHMBadgesTest(PokemonCrystalTestBase):
    options = {
        "hm_badge_requirements": "vanilla"
    }

    def test_cut_access(self):
        verify_region_access(self, ["Hive Badge"], cut_regions)

    def test_fly_access(self):
        verify_region_access(self, ["Storm Badge"], fly_regions)

    def test_surf_access(self):
        verify_region_access(self, ["Fog Badge"], surf_regions)

    def test_strength_access(self):
        verify_region_access(self, ["Plain Badge"], strength_regions)

    def test_flash_access(self):
        verify_region_access(self, ["Zephyr Badge"], flash_regions)

    def test_whirlpool_access(self):
        verify_region_access(self, ["Glacier Badge"], whirlpool_regions)

    def test_waterfall_access(self):
        verify_region_access(self, ["Rising Badge"], waterfall_regions)

    def test_cut_hm_access(self):
        verify_region_access(self, ["HM01 Cut"], cut_regions)

    def test_fly_hm_access(self):
        verify_region_access(self, ["HM02 Fly"], fly_regions)

    def test_surf_hm_access(self):
        verify_region_access(self, ["HM03 Surf"], surf_regions)

    def test_strength_hm_access(self):
        verify_region_access(self, ["HM04 Strength"], strength_regions)

    def test_flash_hm_access(self):
        verify_region_access(self, ["HM05 Flash"], flash_regions)

    def test_whirlpool_hm_access(self):
        verify_region_access(self, ["HM06 Whirlpool"], whirlpool_regions)

    def test_waterfall_hm_access(self):
        verify_region_access(self, ["HM07 Waterfall"], waterfall_regions)


class NoHMBadgesTest(PokemonCrystalTestBase):
    options = {
        "hm_badge_requirements": "no_badges",
        "mt_silver_requirement": "badges",
        "mt_silver_count": "0"
    }

    def test_cut_access(self):
        verify_region_access(self, ["HM01 Cut", "Hive Badge", "Cascade Badge"], cut_regions, ["HM01 Cut"])

    def test_fly_access(self):
        verify_region_access(self, ["HM02 Fly", "Storm Badge", "Thunder Badge"], fly_regions, ["HM02 Fly"])

    def test_surf_access(self):
        verify_region_access(self, ["HM03 Surf", "Fog Badge", "Soul Badge"], surf_regions, ["HM03 Surf"])

    def test_strength_access(self):
        verify_region_access(self, ["HM04 Strength", "Plain Badge", "Rainbow Badge"], strength_regions,
                             ["HM04 Strength"])

    def test_flash_access(self):
        verify_region_access(self, ["HM05 Flash", "Zephyr Badge", "Boulder Badge"], flash_regions, ["HM05 Flash"])

    def test_whirlpool_access(self):
        verify_region_access(self, ["HM06 Whirlpool", "Glacier Badge", "Volcano Badge"], whirlpool_regions,
                             ["HM06 Whirlpool"])

    def test_waterfall_access(self):
        verify_region_access(self, ["HM07 Waterfall", "Rising Badge", "Earth Badge"], waterfall_regions,
                             ["HM07 Waterfall"])


class KantoHMBadgesTest(PokemonCrystalTestBase):
    options = {
        "hm_badge_requirements": "add_kanto",
        "mt_silver_requirement": "badges",
        "mt_silver_count": "0"
    }

    def test_cut_access(self):
        verify_region_access(self, ["Hive Badge", "Cascade Badge"], cut_regions, ["Cascade Badge"])

    def test_fly_access(self):
        verify_region_access(self, ["Storm Badge", "Thunder Badge"], fly_regions, ["Thunder Badge"])

    def test_surf_access(self):
        verify_region_access(self, ["Fog Badge", "Soul Badge"], surf_regions, ["Soul Badge"])

    def test_strength_access(self):
        verify_region_access(self, ["Plain Badge", "Rainbow Badge"], strength_regions, ["Rainbow Badge"])

    def test_flash_access(self):
        verify_region_access(self, ["Zephyr Badge", "Boulder Badge"], flash_regions, ["Boulder Badge"])

    def test_whirlpool_access(self):
        verify_region_access(self, ["Glacier Badge", "Volcano Badge"], whirlpool_regions, ["Volcano Badge"])

    def test_waterfall_access(self):
        verify_region_access(self, ["Rising Badge", "Earth Badge"], waterfall_regions, ["Earth Badge"])

    def test_cut_hm_access(self):
        verify_region_access(self, ["HM01 Cut"], cut_regions)

    def test_fly_hm_access(self):
        verify_region_access(self, ["HM02 Fly"], fly_regions)

    def test_surf_hm_access(self):
        verify_region_access(self, ["HM03 Surf"], surf_regions)

    def test_strength_hm_access(self):
        verify_region_access(self, ["HM04 Strength"], strength_regions)

    def test_flash_hm_access(self):
        verify_region_access(self, ["HM05 Flash"], flash_regions)

    def test_whirlpool_hm_access(self):
        verify_region_access(self, ["HM06 Whirlpool"], whirlpool_regions)

    def test_waterfall_hm_access(self):
        verify_region_access(self, ["HM07 Waterfall"], waterfall_regions)
