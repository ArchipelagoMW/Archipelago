from . import CMTestBase


class MaterialStateTestBase(CMTestBase):
    def setUp(self):
        super().setUp()
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)


class TestSimpleMaterial(MaterialStateTestBase):
    def test_no_options(self):
        self.assertLess(3950, self.multiworld.state.prog_items[self.player]["Material"])

