from .bases import CMTestBase

class TestWorldGeneration(CMTestBase):
    def test_full_generation(self):
        """Test that a complete world generates successfully"""
        pass

    def test_fairy_chess_pawn_upgrades_in_slot_data_default(self):
        """Default off (0) should appear in fill_slot_data output."""
        slot_data = self.world.fill_slot_data()
        self.assertIn("fairy_chess_pawn_upgrades", slot_data)
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 0)


class TestWorldGenerationPawnUpgradesPool(CMTestBase):
    options = {"fairy_chess_pawn_upgrades": 1}

    def test_fairy_chess_pawn_upgrades_round_trip(self):
        """Setting option to pool (1) should round-trip through fill_slot_data."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 1)


class TestWorldGenerationPawnUpgradesMax(CMTestBase):
    options = {"fairy_chess_pawn_upgrades": 2}

    def test_fairy_chess_pawn_upgrades_round_trip(self):
        """Setting option to max (2) should round-trip through fill_slot_data."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 2)


class TestWorldGenerationPawnUpgradesSuperMax(CMTestBase):
    options = {"fairy_chess_pawn_upgrades": "super_max"}

    def test_fairy_chess_pawn_upgrades_round_trip(self):
        """Setting option to super_max (3) should round-trip through fill_slot_data."""
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["fairy_chess_pawn_upgrades"], 3)
