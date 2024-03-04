from . import SVTestBase
from .. import BuildingProgression
from ..options import ToolProgression


class TestBitFlagsVanilla(SVTestBase):
    options = {ToolProgression.internal_name: ToolProgression.option_vanilla,
               BuildingProgression.internal_name: BuildingProgression.option_vanilla}

    def test_options_are_not_detected_as_progressive(self):
        world_options = self.world.options
        tool_progressive = world_options.tool_progression & ToolProgression.option_progressive
        building_progressive = world_options.building_progression & BuildingProgression.option_progressive
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_tools_and_buildings_not_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertNotIn("Progressive Coop", item_names)
        self.assertNotIn("Progressive Pickaxe", item_names)


class TestBitFlagsVanillaCheap(SVTestBase):
    options = {ToolProgression.internal_name: ToolProgression.option_vanilla_cheap,
               BuildingProgression.internal_name: BuildingProgression.option_vanilla_cheap}

    def test_options_are_not_detected_as_progressive(self):
        world_options = self.world.options
        tool_progressive = world_options.tool_progression & ToolProgression.option_progressive
        building_progressive = world_options.building_progression & BuildingProgression.option_progressive
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_tools_and_buildings_not_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertNotIn("Progressive Coop", item_names)
        self.assertNotIn("Progressive Pickaxe", item_names)


class TestBitFlagsVanillaVeryCheap(SVTestBase):
    options = {ToolProgression.internal_name: ToolProgression.option_vanilla_very_cheap,
               BuildingProgression.internal_name: BuildingProgression.option_vanilla_very_cheap}

    def test_options_are_not_detected_as_progressive(self):
        world_options = self.world.options
        tool_progressive = world_options.tool_progression & ToolProgression.option_progressive
        building_progressive = world_options.building_progression & BuildingProgression.option_progressive
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_tools_and_buildings_not_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertNotIn("Progressive Coop", item_names)
        self.assertNotIn("Progressive Pickaxe", item_names)


class TestBitFlagsProgressive(SVTestBase):
    options = {ToolProgression.internal_name: ToolProgression.option_progressive,
               BuildingProgression.internal_name: BuildingProgression.option_progressive}

    def test_options_are_detected_as_progressive(self):
        world_options = self.world.options
        tool_progressive = world_options.tool_progression & ToolProgression.option_progressive
        building_progressive = world_options.building_progression & BuildingProgression.option_progressive
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_tools_and_buildings_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn("Progressive Coop", item_names)
        self.assertIn("Progressive Pickaxe", item_names)


class TestBitFlagsProgressiveCheap(SVTestBase):
    options = {ToolProgression.internal_name: ToolProgression.option_progressive_cheap,
               BuildingProgression.internal_name: BuildingProgression.option_progressive_cheap}

    def test_options_are_detected_as_progressive(self):
        world_options = self.world.options
        tool_progressive = world_options.tool_progression & ToolProgression.option_progressive
        building_progressive = world_options.building_progression & BuildingProgression.option_progressive
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_tools_and_buildings_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn("Progressive Coop", item_names)
        self.assertIn("Progressive Pickaxe", item_names)


class TestBitFlagsProgressiveVeryCheap(SVTestBase):
    options = {ToolProgression.internal_name: ToolProgression.option_progressive_very_cheap,
               BuildingProgression.internal_name: BuildingProgression.option_progressive_very_cheap}

    def test_options_are_detected_as_progressive(self):
        world_options = self.world.options
        tool_progressive = world_options.tool_progression & ToolProgression.option_progressive
        building_progressive = world_options.building_progression & BuildingProgression.option_progressive
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_tools_and_buildings_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn("Progressive Coop", item_names)
        self.assertIn("Progressive Pickaxe", item_names)
