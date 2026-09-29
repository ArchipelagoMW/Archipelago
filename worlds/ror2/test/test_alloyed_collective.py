from . import RoR2TestBase


class AlloyedCollectiveTest(RoR2TestBase):
    options = {
        "dlc_alloyed": "true",
        "progressive_stages": "false",
    }

    ac_stages = ["Pretender's Precipice", "Iron Alluvium", "Iron Auroras",
                 "Conduit Canyon", "Repurposed Crater"]

    def test_ac_stages_in_item_pool(self) -> None:
        pool = [item.name for item in self.multiworld.itempool if item.player == self.player]
        precollected = [item.name for item in self.multiworld.precollected_items.get(self.player, [])]
        for stage in self.ac_stages:
            self.assertEqual(pool.count(stage) + precollected.count(stage), 1)

    def test_ac_regions_exist(self) -> None:
        for stage in self.ac_stages:
            self.assertIsNotNone(self.multiworld.get_region(stage, self.player))

    def test_conduit_canyon_has_no_newt_altars(self) -> None:
        locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertNotIn("Conduit Canyon: Newt Altar 1", locations)
        self.assertIn("Conduit Canyon: Chest 1", locations)
        self.assertIn("Verdant Falls: Newt Altar 1", locations)

    def test_ac_stage_progression(self) -> None:
        self.collect_by_name("Pretender's Precipice")
        self.assertFalse(self.can_reach_region("Pretender's Precipice"))
        self.collect_by_name("Stage 1")
        self.assertTrue(self.can_reach_region("Pretender's Precipice"))

        self.collect_by_name("Iron Alluvium")
        self.assertFalse(self.can_reach_region("Iron Alluvium"))
        self.collect_by_name("Stage 2")
        self.assertTrue(self.can_reach_region("Iron Alluvium"))

    def test_slot_data(self) -> None:
        slot_data = self.multiworld.worlds[self.player].fill_slot_data()
        self.assertIs(slot_data["dlcAlloyed"], True)
        self.assertIs(slot_data["dlcSots"], False)
        self.assertIs(slot_data["dlcSotv"], False)


class AlloyedCollectiveDisabledTest(RoR2TestBase):
    options = {
        "dlc_alloyed": "false",
    }

    def test_no_ac_stages_in_pool(self) -> None:
        pool = [item.name for item in self.multiworld.itempool if item.player == self.player]
        for stage in AlloyedCollectiveTest.ac_stages:
            self.assertNotIn(stage, pool)

    def test_slot_data(self) -> None:
        slot_data = self.multiworld.worlds[self.player].fill_slot_data()
        self.assertIs(slot_data["dlcAlloyed"], False)
