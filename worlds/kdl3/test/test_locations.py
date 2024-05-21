from . import KDL3TestBase
from worlds.generic import PlandoConnection
from ..Names import LocationName
import typing


class TestLocations(KDL3TestBase):
    options = {
        "open_world": True,
        "ow_boss_requirement": 1,
        "strict_bosses": False
        # these ensure we can always reach all stages physically
    }

    def test_simple_heart_stars(self):
        self.run_location_test(LocationName.grass_land_muchi, ["ChuChu"])
        self.run_location_test(LocationName.grass_land_chao, ["Stone"])
        self.run_location_test(LocationName.grass_land_mine, ["Kine"])
        self.run_location_test(LocationName.ripple_field_kamuribana, ["Pitch", "Clean"])
        self.run_location_test(LocationName.ripple_field_bakasa, ["Kine", "Parasol"])
        self.run_location_test(LocationName.ripple_field_toad, ["Needle"])
        self.run_location_test(LocationName.ripple_field_mama_pitch, ["Pitch", "Kine", "Burning", "Stone"])
        self.run_location_test(LocationName.sand_canyon_auntie, ["Clean"])
        self.run_location_test(LocationName.sand_canyon_nyupun, ["ChuChu", "Cutter"])
        self.run_location_test(LocationName.sand_canyon_rob, ["Stone", "Kine", "Coo", "Parasol", "Spark", "Ice"])
        self.run_location_test(LocationName.sand_canyon_rob, ["Stone", "Kine", "Coo", "Parasol", "Clean", "Ice"]),
        self.run_location_test(LocationName.sand_canyon_rob, ["Stone", "Kine", "Coo", "Parasol", "Spark", "Needle"]),
        self.run_location_test(LocationName.sand_canyon_rob, ["Stone", "Kine", "Coo", "Parasol", "Clean", "Needle"]),
        self.run_location_test(LocationName.cloudy_park_hibanamodoki, ["Coo", "Clean"])
        self.run_location_test(LocationName.cloudy_park_piyokeko, ["Needle"])
        self.run_location_test(LocationName.cloudy_park_mikarin, ["Coo"])
        self.run_location_test(LocationName.cloudy_park_pick, ["Rick"])
        self.run_location_test(LocationName.iceberg_kogoesou, ["Burning"])
        self.run_location_test(LocationName.iceberg_samus, ["Ice"])
        self.run_location_test(LocationName.iceberg_name, ["Burning", "Coo", "ChuChu"])
        self.run_location_test(LocationName.iceberg_angel, ["Cutter", "Burning", "Spark", "Parasol", "Needle", "Clean",
                                                            "Stone", "Ice"])

    def run_location_test(self, location: str, itempool: typing.List[str]):
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
            [],
            [
                PlandoConnection("Grass Land 1", "Iceberg 5", "both"),
                PlandoConnection("Grass Land 2", "Ripple Field 5", "both"),
                PlandoConnection("Grass Land 3", "Grass Land 1", "both")
            ]],
        "stage_shuffle": "shuffled",
        "plando_options": "connections"
    }

    def test_shiro(self):
        self.assertFalse(self.can_reach_location("Iceberg 5 - Shiro"), str(self.multiworld.seed))
        self.collect_by_name("Nago")
        self.assertFalse(self.can_reach_location("Iceberg 5 - Shiro"), str(self.multiworld.seed))
        # despite Shiro only requiring Nago for logic, it cannot be in logic because our two accessible stages
        # do not actually give the player access to Nago, thus we need Kine to pass 2-5
        self.collect_by_name("Kine")
        self.assertTrue(self.can_reach_location("Iceberg 5 - Shiro"), str(self.multiworld.seed))
