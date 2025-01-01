from collections import Counter

from .. import SVTestBase
from ... import Event, options
from ...options import ToolProgression, SeasonRandomization
from ...strings.entrance_names import Entrance
from ...strings.region_names import Region
from ...strings.tool_names import Tool, ToolMaterial


class TestProgressiveToolsLogic(SVTestBase):
    options = {
        ToolProgression.internal_name: ToolProgression.option_progressive,
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
    }

    def test_sturgeon(self):
        self.multiworld.state.prog_items = {1: Counter()}

        sturgeon_rule = self.world.logic.has("Sturgeon")
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        summer = self.create_item("Summer")
        self.multiworld.state.collect(summer)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        fishing_rod = self.create_item("Progressive Fishing Rod")
        self.multiworld.state.collect(fishing_rod)
        self.multiworld.state.collect(fishing_rod)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        fishing_level = self.create_item("Fishing Level")
        self.multiworld.state.collect(fishing_level)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        self.multiworld.state.collect(fishing_level)
        self.multiworld.state.collect(fishing_level)
        self.multiworld.state.collect(fishing_level)
        self.multiworld.state.collect(fishing_level)
        self.multiworld.state.collect(fishing_level)
        self.assert_rule_true(sturgeon_rule, self.multiworld.state)

        self.remove(summer)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

        winter = self.create_item("Winter")
        self.multiworld.state.collect(winter)
        self.assert_rule_true(sturgeon_rule, self.multiworld.state)

        self.remove(fishing_rod)
        self.assert_rule_false(sturgeon_rule, self.multiworld.state)

    def test_old_master_cannoli(self):
        self.multiworld.state.prog_items = {1: Counter()}

        self.multiworld.state.collect(self.create_item("Progressive Axe"))
        self.multiworld.state.collect(self.create_item("Progressive Axe"))
        self.multiworld.state.collect(self.create_item("Summer"))
        self.collect_lots_of_money()

        rule = self.world.logic.region.can_reach_location("Old Master Cannoli")
        self.assert_rule_false(rule, self.multiworld.state)

        fall = self.create_item("Fall")
        self.multiworld.state.collect(fall)
        self.assert_rule_false(rule, self.multiworld.state)

        tuesday = self.create_item("Traveling Merchant: Tuesday")
        self.multiworld.state.collect(tuesday)
        self.assert_rule_false(rule, self.multiworld.state)

        rare_seed = self.create_item("Rare Seed")
        self.multiworld.state.collect(rare_seed)
        self.assert_rule_true(rule, self.multiworld.state)

        self.remove(fall)
        self.remove(self.create_item(Event.fall_farming))
        self.assert_rule_false(rule, self.multiworld.state)
        self.remove(tuesday)

        green_house = self.create_item("Greenhouse")
        self.collect(self.create_item(Event.fall_farming))
        self.multiworld.state.collect(green_house)
        self.assert_rule_false(rule, self.multiworld.state)

        friday = self.create_item("Traveling Merchant: Friday")
        self.multiworld.state.collect(friday)
        self.assertTrue(self.multiworld.get_location("Old Master Cannoli", 1).access_rule(self.multiworld.state))

        self.remove(green_house)
        self.remove(self.create_item(Event.fall_farming))
        self.assert_rule_false(rule, self.multiworld.state)
        self.remove(friday)


class TestToolVanillaRequiresBlacksmith(SVTestBase):
    options = {
        options.EntranceRandomization: options.EntranceRandomization.option_buildings,
        options.ToolProgression: options.ToolProgression.option_vanilla,
    }
    seed = 4111845104987680262

    # Seed is hardcoded to make sure the ER is a valid roll that actually lock the blacksmith behind the Railroad Boulder Removed.

    def test_cannot_get_any_tool_without_blacksmith_access(self):
        railroad_item = "Railroad Boulder Removed"
        place_region_at_entrance(self.multiworld, self.player, Region.blacksmith, Entrance.enter_bathhouse_entrance)
        self.collect_all_except(railroad_item)

        for tool in [Tool.pickaxe, Tool.axe, Tool.hoe, Tool.trash_can, Tool.watering_can]:
            for material in [ToolMaterial.copper, ToolMaterial.iron, ToolMaterial.gold, ToolMaterial.iridium]:
                self.assert_rule_false(self.world.logic.tool.has_tool(tool, material), self.multiworld.state)

        self.multiworld.state.collect(self.create_item(railroad_item))

        for tool in [Tool.pickaxe, Tool.axe, Tool.hoe, Tool.trash_can, Tool.watering_can]:
            for material in [ToolMaterial.copper, ToolMaterial.iron, ToolMaterial.gold, ToolMaterial.iridium]:
                self.assert_rule_true(self.world.logic.tool.has_tool(tool, material), self.multiworld.state)

    def test_cannot_get_fishing_rod_without_willy_access(self):
        railroad_item = "Railroad Boulder Removed"
        place_region_at_entrance(self.multiworld, self.player, Region.fish_shop, Entrance.enter_bathhouse_entrance)
        self.collect_all_except(railroad_item)

        for fishing_rod_level in [3, 4]:
            self.assert_rule_false(self.world.logic.tool.has_fishing_rod(fishing_rod_level), self.multiworld.state)

        self.multiworld.state.collect(self.create_item(railroad_item))

        for fishing_rod_level in [3, 4]:
            self.assert_rule_true(self.world.logic.tool.has_fishing_rod(fishing_rod_level), self.multiworld.state)


def place_region_at_entrance(multiworld, player, region, entrance):
    region_to_place = multiworld.get_region(region, player)
    entrance_to_place_region = multiworld.get_entrance(entrance, player)

    entrance_to_switch = region_to_place.entrances[0]
    region_to_switch = entrance_to_place_region.connected_region
    entrance_to_switch.connect(region_to_switch)
    entrance_to_place_region.connect(region_to_place)
