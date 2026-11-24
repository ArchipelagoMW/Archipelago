from . import GameDevTycoonTestBase


class TestBusinessFeatures(GameDevTycoonTestBase):
    def test_every_feature_is_in_the_pool(self) -> None:
        names = {item.name for item in self.multiworld.itempool}
        for feature in ("Target Audience", "Marketing", "Sequels", "Multi-Genre", "Multi-Platform", "Expansion Packs"):
            self.assertIn(f"Business: {feature}", names)
        self.assertNotIn("Progressive Game Size", names)


class TestShuffleGameSizes(GameDevTycoonTestBase):
    options = {"shuffle_game_sizes": True, "success_level": "tycoon"}

    def test_sizes_gate_the_big_offices(self) -> None:
        self.assertEqual(3, sum(item.name == "Progressive Game Size" for item in self.multiworld.itempool))
        self.collect_by_name("Progressive Office Upgrade")
        self.assertFalse(self.can_reach_region("Studio (Office Tier 4)"))
        self.collect_by_name("Progressive Game Size")
        self.assertTrue(self.can_reach_region("Studio (Office Tier 4)"))
