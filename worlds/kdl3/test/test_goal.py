from . import KDL3TestBase


class TestFastGoal(KDL3TestBase):
    options = {
        "open_world": False,
        "goal_speed": "fast",
        "max_heart_stars": 30,
        "heart_stars_required": 50,
        "filler_percentage": 0,
    }

    def test_goal(self) -> None:
        self.assertBeatable(False)
        heart_stars = self.get_items_by_name("Heart Star")
        self.collect(heart_stars[0:14])
        self.assertEqual(self.count("Heart Star"), 14, str(self.multiworld.seed))
        self.assertBeatable(False)
        self.collect(heart_stars[14:15])
        self.assertEqual(self.count("Heart Star"), 15, str(self.multiworld.seed))
        self.assertBeatable(True)
        self.remove([self.get_item_by_name("Love-Love Rod")])
        self.collect_by_name("Kine")  # Ensure a little more progress, but leave out cutter and burning
        self.collect(heart_stars[15:])
        self.assertBeatable(True)


class TestNormalGoal(KDL3TestBase):
    # TODO: open world tests
    options = {
        "open_world": False,
        "goal_speed": "normal",
        "max_heart_stars": 30,
        "heart_stars_required": 50,
        "filler_percentage": 0,
    }

    def test_goal(self) -> None:
        self.assertBeatable(False)
        heart_stars = self.get_items_by_name("Heart Star")
        self.collect(heart_stars[0:14])
        self.assertEqual(self.count("Heart Star"), 14, str(self.multiworld.seed))
        self.assertBeatable(False)
        self.collect(heart_stars[14:15])
        self.assertEqual(self.count("Heart Star"), 15, str(self.multiworld.seed))
        self.assertBeatable(False)
        self.collect_by_name(["Burning", "Cutter", "Kine"])
        self.assertBeatable(True)
        self.remove([self.get_item_by_name("Love-Love Rod")])
        self.collect(heart_stars)
        self.assertEqual(self.count("Heart Star"), 30, str(self.multiworld.seed))
        self.assertBeatable(True)

    def test_kine(self) -> None:
        self.collect_by_name(["Cutter", "Burning", "Heart Star"])
        self.assertBeatable(False)

    def test_cutter(self) -> None:
        self.collect_by_name(["Kine", "Burning", "Heart Star"])
        self.assertBeatable(False)

    def test_burning(self) -> None:
        self.collect_by_name(["Cutter", "Kine", "Heart Star"])
        self.assertBeatable(False)
