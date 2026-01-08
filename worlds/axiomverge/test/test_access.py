from . import AVTestBase

class TestAccessCases(AVTestBase):
    options = {
        "start_location": 2,
    }
    def test_false_roof_alcove_reachable(self):
        location = "Zi - False Roof Alcove"
        self.assertFalse(self.can_reach_location(location))

        self.collect_by_name(("Kilver", "Field Disruptor"))
        self.assertTrue(self.can_reach_location(location))