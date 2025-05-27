from .bases import JakAndDaxterTestBase


class TradesCostNothingTest(JakAndDaxterTestBase):
    options = {
        "enable_orbsanity": 2,
        "global_orbsanity_bundle_size": 5,
        "citizen_orb_trade_amount": 0,
        "oracle_orb_trade_amount": 0
    }

    def test_orb_items_are_filler(self):
        self.collect_all_but("")
        self.assertNotIn("5 Precursor Orbs", self.multiworld.state.prog_items)

    def test_trades_are_accessible(self):
        self.assertTrue(self.multiworld
                        .get_location("SV: Bring 90 Orbs To The Mayor", self.player)
                        .can_reach(self.multiworld.state))


class TradesCostEverythingTest(JakAndDaxterTestBase):
    options = {
        "enable_orbsanity": 2,
        "global_orbsanity_bundle_size": 5,
        "citizen_orb_trade_amount": 120,
        "oracle_orb_trade_amount": 150
    }

    def test_orb_items_are_progression(self):
        self.collect_all_but("")
        self.assertIn("5 Precursor Orbs", self.multiworld.state.prog_items[self.player])
        self.assertEqual(396, self.multiworld.state.prog_items[self.player]["5 Precursor Orbs"])

    def test_trades_are_accessible(self):
        self.collect_all_but("")
        self.assertTrue(self.multiworld
                        .get_location("SV: Bring 90 Orbs To The Mayor", self.player)
                        .can_reach(self.multiworld.state))
