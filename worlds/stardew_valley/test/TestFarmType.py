from collections import Counter

from . import SVTestBase
from .assertion import WorldAssertMixin
from .. import options


class TestStartInventoryStandardFarm(WorldAssertMixin, SVTestBase):
    options = {
        options.FarmType: options.FarmType.option_standard,
    }

    def test_start_inventory_progressive_coops(self):
        start_items = Counter((i.name for i in self.multiworld.precollected_items[self.player]))
        items = Counter((i.name for i in self.multiworld.itempool))
        
        self.assertIn("Progressive Coop", items)
        self.assertEqual(items["Progressive Coop"], 3)
        self.assertNotIn("Progressive Coop", start_items)

    def test_coop_is_not_logically_available(self):
        self.assert_rule_false(self.world.logic.building.has_building("Coop"))


class TestStartInventoryMeadowLandsProgressiveBuilding(WorldAssertMixin, SVTestBase):
    options = {
        options.FarmType: options.FarmType.option_meadowlands,
        options.BuildingProgression: options.BuildingProgression.option_progressive,
    }

    def test_start_inventory_progressive_coops(self):
        start_items = Counter((i.name for i in self.multiworld.precollected_items[self.player]))
        items = Counter((i.name for i in self.multiworld.itempool))

        self.assertIn("Progressive Coop", items)
        self.assertEqual(items["Progressive Coop"], 2)
        self.assertIn("Progressive Coop", start_items)
        self.assertEqual(start_items["Progressive Coop"], 1)

    def test_coop_is_logically_available(self):
        self.assert_rule_true(self.world.logic.building.has_building("Coop"))


class TestStartInventoryMeadowLandsVanillaBuildings(WorldAssertMixin, SVTestBase):
    options = {
        options.FarmType: options.FarmType.option_meadowlands,
        options.BuildingProgression: options.BuildingProgression.option_vanilla,
    }

    def test_start_inventory_has_no_coop(self):
        start_items = Counter((i.name for i in self.multiworld.precollected_items[self.player]))
        self.assertNotIn("Progressive Coop", start_items)

    def test_coop_is_logically_available(self):
        self.assert_rule_true(self.world.logic.building.has_building("Coop"))
