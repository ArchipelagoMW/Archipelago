from . import LingoTestBase


class TestPanelHunt(LingoTestBase):
    options = {
        "shuffle_doors": "complex",
        "location_checks": "insanity",
        "victory_condition": "level_2",
        "level_2_requirement": "15"
    }

    def test_another_try(self) -> None:
        self.collect_by_name("The Traveled - Entrance") # idk why this is needed
        self.assertFalse(self.can_reach_location("Second Room - ANOTHER TRY"))
        self.assertFalse(self.can_reach_location("Second Room - Unlock Level 2"))

        self.collect_by_name("Second Room - Exit Door")
        self.assertTrue(self.can_reach_location("Second Room - ANOTHER TRY"))
        self.assertTrue(self.can_reach_location("Second Room - Unlock Level 2"))
