from . import CMTestBase


class MaterialStateTestBase(CMTestBase):
    def setUp(self):
        super().setUp()
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)


class TestSimpleMaterial(MaterialStateTestBase):
    def test_no_options(self):
        self.assertLess(3950, self.multiworld.state.prog_items[self.player]["Material"])


class TestCyclicMaterial(MaterialStateTestBase):
    def test_no_options(self):
        past_material = self.multiworld.state.prog_items[self.player]["Material"]

        self.remove(self.multiworld.itempool)
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)

        self.assertLess(past_material, self.multiworld.state.prog_items[self.player]["Material"])

