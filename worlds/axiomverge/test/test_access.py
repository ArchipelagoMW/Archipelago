from . import AVTestBase

class TestAccessCases(AVTestBase):
    options = {
        "start_location": 2,
    }
    def test_false_roof_alcove_reachable(self):
        location = "Zi - False Ceiling Alcove"
        self.assertFalse(self.can_reach_location(location))

        self.collect_by_name(("Axiom Disruptor", "Field Disruptor", "Power Node"))
        self.assertTrue(self.can_reach_location(location))
