from . import SVTestBase
from .assertion import WorldAssertMixin
from .. import options


class TestStartInventoryStandardFarm(WorldAssertMixin, SVTestBase):
    options = {
        options.FarmType.internal_name: options.FarmType.option_standard,
    }

    def test_start_inventory_progressive_coops(self):
        start_items = dict(map(lambda x: (x.name, self.multiworld.precollected_items[self.player].count(x)), self.multiworld.precollected_items[self.player]))
        items = dict(map(lambda x: (x.name, self.multiworld.itempool.count(x)), self.multiworld.itempool))
        self.assertIn("Progressive Coop", items)
        self.assertEqual(items["Progressive Coop"], 3)
        self.assertNotIn("Progressive Coop", start_items)


class TestStartInventoryMeadowLands(WorldAssertMixin, SVTestBase):
    options = {
        options.FarmType.internal_name: options.FarmType.option_meadowlands,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
    }

    def test_start_inventory_progressive_coops(self):
        start_items = dict(map(lambda x: (x.name, self.multiworld.precollected_items[self.player].count(x)), self.multiworld.precollected_items[self.player]))
        items = dict(map(lambda x: (x.name, self.multiworld.itempool.count(x)), self.multiworld.itempool))
        self.assertIn("Progressive Coop", items)
        self.assertEqual(items["Progressive Coop"], 2)
        self.assertIn("Progressive Coop", start_items)
        self.assertEqual(start_items["Progressive Coop"], 1)
