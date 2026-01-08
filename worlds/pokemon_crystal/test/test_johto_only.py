from .bases import PokemonCrystalTestBase


class JohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on"
    }

    def test_victory_road_access(self):
        self.collect_all_but(["HM07 Waterfall", "EVENT_BEAT_ELITE_FOUR", "Victory"])
        self.assertBeatable(False)
        self.collect_by_name("HM07 Waterfall")
        self.assertBeatable(True)

    def test_victory_road_gate(self):
        self.collect_all_but(["Mineral Badge", "EVENT_BEAT_ELITE_FOUR", "Victory", "Boulder Badge", "Cascade Badge",
                              "Thunder Badge", "Rainbow Badge", "Soul Badge", "Marsh Badge", "Volcano Badge",
                              "Earth Badge"])
        self.assertBeatable(False)
        self.collect_by_name("Mineral Badge")
        self.assertBeatable(True)


class JohtoOnlyExtraBadgesTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on",
        "randomize_badges": "completely_random",
        "elite_four_requirement": "badges",
        "elite_four_count": "16"
    }

    def test_badges_added_to_pool(self):
        for badge in ("Zephyr Badge", "Hive Badge", "Plain Badge", "Fog Badge", "Mineral Badge", "Storm Badge",
                      "Glacier Badge", "Rising Badge", "Boulder Badge", "Cascade Badge", "Thunder Badge",
                      "Rainbow Badge", "Soul Badge", "Marsh Badge", "Volcano Badge", "Earth Badge"):
            self.assertTrue(self.get_item_by_name(badge))

    def test_victory_road_badges(self):
        self.collect_all_but(["Earth Badge", "EVENT_BEAT_ELITE_FOUR", "Victory"])
        self.assertBeatable(False)
        self.collect_by_name("Earth Badge")
        self.assertBeatable(True)


class JohtoOnlyRedTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "include_silver_cave",
        "goal": "red",
        "randomize_badges": "completely_random",
        "red_badges": "16"
    }

    def test_badges_added_to_pool(self):
        for badge in ("Zephyr Badge", "Hive Badge", "Plain Badge", "Fog Badge", "Mineral Badge", "Storm Badge",
                      "Glacier Badge", "Rising Badge", "Boulder Badge", "Cascade Badge", "Thunder Badge",
                      "Rainbow Badge", "Soul Badge", "Marsh Badge", "Volcano Badge", "Earth Badge"):
            self.assertTrue(self.get_item_by_name(badge))

    def test_silver_cave_badges(self):
        self.collect_all_but(["Earth Badge", "EVENT_OPENED_MT_SILVER", "EVENT_BEAT_RED", "Victory"])
        self.assertBeatable(False)
        self.collect_by_name("Earth Badge")
        self.assertBeatable(True)
