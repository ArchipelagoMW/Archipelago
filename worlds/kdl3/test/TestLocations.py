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

    def testSimpleHeartStars(self):
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
        self.run_location_test(LocationName.cloudy_park_hibanamodoki, ["Coo", "Clean"])
        self.run_location_test(LocationName.cloudy_park_piyokeko, ["Needle"])
        self.run_location_test(LocationName.cloudy_park_mikarin, ["Coo"])
        self.run_location_test(LocationName.cloudy_park_pick, ["Rick"])
        self.run_location_test(LocationName.iceberg_kogoesou, ["Burning"])
        self.run_location_test(LocationName.iceberg_samus, ["Ice"])
        self.run_location_test(LocationName.iceberg_angel, ["Cutter", "Burning", "Spark", "Parasol", "Needle", "Clean", "Stone", "Ice"])

    def run_location_test(self, location: str, itempool: typing.List[str]):
        items = itempool.copy()
        while len(itempool) > 0:
            assert not self.can_reach_location(location)
            self.collect_by_name(itempool.pop())
        assert self.can_reach_location(location)
        self.remove(self.get_items_by_name(items))


class TestName(KDL3TestBase):
    options = {
        "plando_connections": [
            [],
            [
                PlandoConnection("Grass Land 1", "Grass Land 4", "both"),
                PlandoConnection("Grass Land 2", "Iceberg 4", "both"),
                PlandoConnection("Grass Land 3", "Sand Canyon 5", "both"),
                PlandoConnection("Grass Land 4", "Grass Land 3", "both")
            ]],
        "stage_shuffle": "shuffled",
        "plando_options": "connections"
    }

    def testName(self):
        assert not self.can_reach_location("Iceberg 4 - Name")
        self.collect_by_name("Coo")
        self.collect_by_name("ChuChu")
        self.collect_by_name("Burning")
        assert not self.can_reach_location("Iceberg 4 - Name")
        # despite Name only requiring Burning/ChuChu/Coo for logic, it cannot be in logic because our
        # three accessible stages do not actually give the player access to Coo, thus we need Cutter to pass 3-5
        self.collect_by_name("Cutter")
        assert self.can_reach_location("Iceberg 4 - Name")


class TestShiro(KDL3TestBase):
    options = {
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

    def testShiro(self):
        assert not self.can_reach_location("Iceberg 5 - Shiro")
        self.collect_by_name("Nago")
        assert not self.can_reach_location("Iceberg 5 - Shiro")
        # despite Shiro only requiring Nago for logic, it cannot be in logic because our two accessible stages
        # do not actually give the player access to Nago, thus we need Kine to pass 2-5
        self.collect_by_name("Kine")
        assert self.can_reach_location("Iceberg 5 - Shiro")

