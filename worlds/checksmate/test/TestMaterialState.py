from . import CMTestBase


class MaterialStateTestBase(CMTestBase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


class TestSimpleMaterial(MaterialStateTestBase):
    def test_no_options(self):
        self.assertEqual(3900, self.multiworld.state.prog_items[self.player]["Material"])

