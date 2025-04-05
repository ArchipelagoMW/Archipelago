from . import KDL3TestBase
from ..names import location_name
from Options import PlandoConnection
import typing


class TestLocations(KDL3TestBase):
    options = {
        "open_world": True,
        "ow_boss_requirement": 1,
        "strict_bosses": False
        # these ensure we can always reach all stages physically
    }

    def test_simple_heart_stars(self) -> None:
        self.run_location_test(location_name.grass_land_muchi, ["ChuChu"])
        self.run_location_test(location_name.grass_land_chao, ["Stone"])
        self.run_location_test(location_name.grass_land_mine, ["Kine"])
        self.run_location_test(location_name.ripple_field_kamuribana, ["Pitch", "Clean"])
        self.run_location_test(location_name.ripple_field_bakasa, ["Kine", "Parasol"])
        self.run_location_test(location_name.ripple_field_toad, ["Needle"])
        self.run_location_test(location_name.ripple_field_mama_pitch, ["Pitch", "Kine", "Burning", "Stone"])
        self.run_location_test(location_name.sand_canyon_auntie, ["Clean"])
        self.run_location_test(location_name.sand_canyon_nyupun, ["ChuChu", "Cutter"])
        self.run_location_test(location_name.sand_canyon_rob, ["Stone", "Kine", "Coo", "Parasol", "Spark", "Ice"])
        self.run_location_test(location_name.sand_canyon_rob, ["Stone", "Kine", "Coo", "Parasol", "Clean", "Ice"])
        self.run_location_test(location_name.sand_canyon_rob, ["Stone", "Kine", "Coo", "Parasol", "Spark", "Needle"])
        self.run_location_test(location_name.sand_canyon_rob, ["Stone", "Kine", "Coo", "Parasol", "Clean", "Needle"])
        self.run_location_test(location_name.cloudy_park_hibanamodoki, ["Coo", "Clean"])
        self.run_location_test(location_name.cloudy_park_piyokeko, ["Needle"])
        self.run_location_test(location_name.cloudy_park_mikarin, ["Coo"])
        self.run_location_test(location_name.cloudy_park_pick, ["Rick"])
        self.run_location_test(location_name.iceberg_kogoesou, ["Burning"])
        self.run_location_test(location_name.iceberg_samus, ["Ice"])
        self.run_location_test(location_name.iceberg_name, ["Burning", "Coo", "ChuChu"])
        self.run_location_test(location_name.iceberg_angel, ["Cutter", "Burning", "Spark", "Parasol", "Needle", "Clean",
                                                            "Stone", "Ice"])

    def run_location_test(self, location: str, itempool: typing.List[str]) -> None:
        items = itempool.copy()
        while len(itempool) > 0:
            self.assertFalse(self.can_reach_location(location), str(self.multiworld.seed))
            self.collect_by_name(itempool.pop())
        self.assertTrue(self.can_reach_location(location), str(self.multiworld.seed))
        self.remove(self.get_items_by_name(items))


class TestShiro(KDL3TestBase):
    options = {
        "open_world": False,
        "plando_connections": [
                PlandoConnection("Grass Land 1", "Iceberg 5", "both"),
                PlandoConnection("Grass Land 2", "Ripple Field 5", "both"),
                PlandoConnection("Grass Land 3", "Grass Land 1", "both")
            ],
        "stage_shuffle": "shuffled",
        "plando_options": "connections"
    }

    def test_shiro(self) -> None:
        self.assertFalse(self.can_reach_location("Iceberg 5 - Shiro"), str(self.multiworld.seed))
        self.collect_by_name("Nago")
        self.assertFalse(self.can_reach_location("Iceberg 5 - Shiro"), str(self.multiworld.seed))
        # despite Shiro only requiring Nago for logic, it cannot be in logic because our two accessible stages
        # do not actually give the player access to Nago, thus we need Kine to pass 2-5
        self.collect_by_name("Kine")
        self.assertTrue(self.can_reach_location("Iceberg 5 - Shiro"), str(self.multiworld.seed))
