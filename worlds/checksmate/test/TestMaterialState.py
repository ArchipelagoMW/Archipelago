from . import CMTestBase


class MaterialStateTestBase(CMTestBase):
    def setUp(self):
        super().setUp()
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)


class TestSimpleMaterial(MaterialStateTestBase):
    """
    Checks that goal can be reached based on the math performed by collect()

    If this fails, it's not necessarily the fault of collect(), it might be that the generator isn't adding enough items
    """
    def test_no_options(self):
        self.assertLess(3950, self.multiworld.state.prog_items[self.player]["Material"])


class TestCyclicMaterial(MaterialStateTestBase):
    """Removes all material, then adds it back again. This tests remove() via sledgehammer method"""
    def test_no_options(self):
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])

        self.remove(self.multiworld.itempool)
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)

        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])

