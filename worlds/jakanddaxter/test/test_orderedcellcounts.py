from .bases import JakAndDaxterTestBase


class ReorderedCellCountsTest(JakAndDaxterTestBase):
    options = {
        "enable_ordered_cell_counts": True,
        "fire_canyon_cell_count": 20,
        "mountain_pass_cell_count": 15,
        "lava_tube_cell_count": 10,
    }

    def test_reordered_cell_counts(self):
        self.world.generate_early()
        self.assertLessEqual(self.world.options.fire_canyon_cell_count, self.world.options.mountain_pass_cell_count)
        self.assertLessEqual(self.world.options.mountain_pass_cell_count, self.world.options.lava_tube_cell_count)


class UnorderedCellCountsTest(JakAndDaxterTestBase):
    options = {
        "enable_ordered_cell_counts": False,
        "fire_canyon_cell_count": 20,
        "mountain_pass_cell_count": 15,
        "lava_tube_cell_count": 10,
    }

    def test_unordered_cell_counts(self):
        self.world.generate_early()
        self.assertGreaterEqual(self.world.options.fire_canyon_cell_count, self.world.options.mountain_pass_cell_count)
        self.assertGreaterEqual(self.world.options.mountain_pass_cell_count, self.world.options.lava_tube_cell_count)
