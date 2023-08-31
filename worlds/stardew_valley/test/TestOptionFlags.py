from . import SVTestBase
from .. import options


class TestBitFlagsVanilla(SVTestBase):
    options = {options.ToolProgression.internal_name: options.ToolProgression.option_vanilla,
               options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla}

    def test_options_are_not_detected_as_progressive(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_progressive
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_progressive
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_options_are_detected_as_vanilla(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_vanilla
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_vanilla
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_tools_and_buildings_not_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertNotIn("Progressive Coop", item_names)
        self.assertNotIn("Progressive Pickaxe", item_names)


class TestBitFlagsVanillaCheap(SVTestBase):
    options = {options.ToolProgression.internal_name: options.ToolProgression.option_vanilla_cheap,
               options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla_cheap}

    def test_options_are_not_detected_as_progressive(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_progressive
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_progressive
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_options_are_detected_as_vanilla(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_vanilla
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_vanilla
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_tools_and_buildings_not_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertNotIn("Progressive Coop", item_names)
        self.assertNotIn("Progressive Pickaxe", item_names)


class TestBitFlagsVanillaVeryCheap(SVTestBase):
    options = {options.ToolProgression.internal_name: options.ToolProgression.option_vanilla_very_cheap,
               options.BuildingProgression.internal_name: options.BuildingProgression.option_vanilla_very_cheap}

    def test_options_are_not_detected_as_progressive(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_progressive
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_progressive
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_options_are_detected_as_vanilla(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_vanilla
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_vanilla
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_tools_and_buildings_not_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertNotIn("Progressive Coop", item_names)
        self.assertNotIn("Progressive Pickaxe", item_names)


class TestBitFlagsProgressive(SVTestBase):
    options = {options.ToolProgression.internal_name: options.ToolProgression.option_progressive,
               options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive}

    def test_options_are_detected_as_progressive(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_progressive
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_progressive
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_options_are_not_detected_as_vanilla(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_vanilla
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_vanilla
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_tools_and_buildings_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn("Progressive Coop", item_names)
        self.assertIn("Progressive Pickaxe", item_names)


class TestBitFlagsProgressiveCheap(SVTestBase):
    options = {options.ToolProgression.internal_name: options.ToolProgression.option_progressive_cheap,
               options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive_cheap}

    def test_options_are_detected_as_progressive(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_progressive
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_progressive
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_options_are_not_detected_as_vanilla(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_vanilla
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_vanilla
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_tools_and_buildings_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn("Progressive Coop", item_names)
        self.assertIn("Progressive Pickaxe", item_names)


class TestBitFlagsProgressiveVeryCheap(SVTestBase):
    options = {options.ToolProgression.internal_name: options.ToolProgression.option_progressive_very_cheap,
               options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive_very_cheap}

    def test_options_are_detected_as_progressive(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_progressive
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_progressive
        self.assertTrue(tool_progressive)
        self.assertTrue(building_progressive)

    def test_options_are_not_detected_as_vanilla(self):
        world_options = self.multiworld.worlds[self.player].options
        tool_progressive = world_options[options.ToolProgression] & options.ToolProgression.option_vanilla
        building_progressive = world_options[options.BuildingProgression] & options.BuildingProgression.option_vanilla
        self.assertFalse(tool_progressive)
        self.assertFalse(building_progressive)

    def test_tools_and_buildings_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn("Progressive Coop", item_names)
        self.assertIn("Progressive Pickaxe", item_names)
