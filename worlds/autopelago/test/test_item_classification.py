from BaseClasses import ItemClassification
from test.bases import WorldTestBase
from worlds.autopelago import GAME_NAME, item_name_to_auras, item_name_to_rat_count


class ItemClassificationTestWithOnlyWellFedAuraEnabled(WorldTestBase):
    game = GAME_NAME
    run_default_tests = False
    def setUp(self):
        self.options = {
            "enabled_buffs": frozenset({"Well Fed"}),
            "enabled_traps": frozenset(),
        }
        super().setUp()

    def test_proper_classifications(self) -> None:
        for item in self.multiworld.get_items():
            self.assertNotIn(ItemClassification.trap, item.classification)
            if "well_fed" in item_name_to_auras[item.name]:
                self.assertIn(ItemClassification.useful, item.classification)
            elif item.name not in item_name_to_rat_count:
                self.assertNotIn(ItemClassification.useful, item.classification, item)


class ItemClassificationTestWithOnlyStartledTrapEnabled(WorldTestBase):
    game = GAME_NAME
    run_default_tests = False
    def setUp(self):
        self.options = {
            "enabled_buffs": frozenset(),
            "enabled_traps": frozenset({"Startled"}),
        }
        super().setUp()

    def test_proper_classifications(self) -> None:
        for item in self.multiworld.get_items():
            if item.name not in item_name_to_rat_count:
                self.assertNotIn(ItemClassification.useful, item.classification, item)
            if "startled" in item_name_to_auras[item.name]:
                self.assertIn(ItemClassification.trap, item.classification)
            else:
                self.assertNotIn(ItemClassification.trap, item.classification, item)


class ItemClassificationTestWithNoAurasEnabled(WorldTestBase):
    game = GAME_NAME
    run_default_tests = False
    def setUp(self):
        self.options = {
            "enabled_buffs": frozenset(),
            "enabled_traps": frozenset(),
        }
        super().setUp()

    def test_proper_classifications(self) -> None:
        for item in self.multiworld.get_items():
            if item.name not in item_name_to_rat_count:
                self.assertNotIn(ItemClassification.useful, item.classification, item)
            self.assertNotIn(ItemClassification.trap, item.classification, item)