from . import MuseDashTestBase


class TestNoTraps(MuseDashTestBase):
    def test_no_traps(self) -> None:
        md_world = self.get_world()
        md_world.options.chosen_traps.value.clear()
        self.assertEqual(len(md_world.get_available_traps()), 0, "Got an available trap when we expected none.")

    def test_all_traps(self) -> None:
        md_world = self.get_world()
        md_world.options.dlc_packs.value.add(md_world.md_collection.MUSE_PLUS_DLC)

        for trap in md_world.md_collection.trap_items.keys():
            md_world.options.chosen_traps.value.add(trap)

        trap_count = len(md_world.get_available_traps())
        true_count = len(md_world.md_collection.trap_items.keys())

        self.assertEqual(trap_count, true_count, "Got a different amount of traps than what was expected.")

    def test_exclude_sfx_traps(self) -> None:
        md_world = self.get_world()
        if "Muse Plus" in md_world.options.dlc_packs.value:
            md_world.options.dlc_packs.value.remove("Muse Plus")

        for trap in md_world.md_collection.trap_items.keys():
            md_world.options.chosen_traps.value.add(trap)

        trap_count = len(md_world.get_available_traps())
        true_count = len(md_world.md_collection.trap_items.keys()) - len(md_world.md_collection.sfx_trap_items)

        self.assertEqual(trap_count, true_count, "Got a different amount of traps than what was expected.")
