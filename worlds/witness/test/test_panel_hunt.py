from worlds.witness.test import WitnessTestBase


class TestMaxPanelHuntMinChecks(WitnessTestBase):
    options = {
        "victory_condition": "panel_hunt",
        "panel_hunt_total": 100,
        "panel_hunt_required_percentage": 100,
        "panel_hunt_postgame": "disable_anything_locked_by_lasers",
        "disable_non_randomized_puzzles": True,
        "shuffle_discarded_panels": False,
        "shuffle_vault_boxes": False,
    }

    def test_100_panels_were_picked(self):
        self.assertEqual(len(self.multiworld.find_item_locations("+1 Panel Hunt", self.player)), 100)