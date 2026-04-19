from .bases import CMTestBase

class TestWorldGeneration(CMTestBase):
    def test_full_generation(self):
        """Test that a complete world generates successfully"""
        pass

    def test_fairy_chess_pawn_sergeants_in_slot_data_default(self):
        """Default off (0) should appear in fill_slot_data output."""
        slot_data = self.world.fill_slot_data()
        self.assertIn("fairy_chess_pawn_sergeants", slot_data)
        self.assertEqual(slot_data["fairy_chess_pawn_sergeants"], 0)


class TestWorldGenerationSergeantsReplace(CMTestBase):
    options = {"fairy_chess_pawn_sergeants": 2}

    def test_fairy_chess_pawn_sergeants_round_trip(self):
        """Setting option to replace (2) should round-trip through fill_slot_data."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_sergeants"], 2)
