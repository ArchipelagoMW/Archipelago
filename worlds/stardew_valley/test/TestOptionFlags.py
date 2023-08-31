from . import SVTestBase
from .. import options


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
