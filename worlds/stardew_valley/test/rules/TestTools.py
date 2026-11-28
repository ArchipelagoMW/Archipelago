from collections import Counter

from Options import PlandoConnection

from ... import options
from ...options import SeasonRandomization, Secretsanity, ToolProgression
from ...strings.entrance_names import Entrance
from ...strings.tool_names import FishingRod, Tool, ToolMaterial
from ..bases import SVTestBase


class TestProgressiveToolsLogic(SVTestBase):
    options = {  # noqa: RUF012
        ToolProgression.internal_name: ToolProgression.option_progressive,
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Secretsanity.internal_name: Secretsanity.preset_simple,
    }

    def test_sturgeon(self):
        self.multiworld.state.prog_items = {1: Counter()}

        sturgeon_rule = self.world.logic.has("Sturgeon")
        self.assert_rule_false(sturgeon_rule)

        summer = self.create_item("Summer")
        self.multiworld.state.collect(summer)
        self.assert_rule_false(sturgeon_rule)

        fishing_rod = self.create_item("Progressive Fishing Rod")
        self.multiworld.state.collect(fishing_rod)
        self.multiworld.state.collect(fishing_rod)
        self.assert_rule_false(sturgeon_rule)

        fishing_level = self.create_item("Fishing Level")
        self.multiworld.state.collect(fishing_level)
        self.assert_rule_false(sturgeon_rule)

        self.multiworld.state.collect(fishing_level)
        self.multiworld.state.collect(fishing_level)
        self.multiworld.state.collect(fishing_level)
        self.multiworld.state.collect(fishing_level)
        self.multiworld.state.collect(fishing_level)
        self.assert_rule_true(sturgeon_rule)

        self.remove(summer)
        self.assert_rule_false(sturgeon_rule)

        winter = self.create_item("Winter")
        self.multiworld.state.collect(winter)
        self.assert_rule_true(sturgeon_rule)

        self.remove(fishing_rod)
        self.assert_rule_false(sturgeon_rule)

    def test_old_master_cannoli(self):
        self.multiworld.state.prog_items = {1: Counter()}

        self.collect("Progressive Axe")
        self.collect("Progressive Axe")
        self.collect("Summer")
        self.collect_lots_of_money()

        location = "Secret: Old Master Cannoli"
        self.assert_cannot_reach_location(location)

        fall = self.create_item("Fall")
        self.multiworld.state.collect(fall)
        self.assert_cannot_reach_location(location)

        tuesday = self.create_item("Traveling Merchant: Tuesday")
        self.multiworld.state.collect(tuesday)
        self.assert_cannot_reach_location(location)

        rare_seed = self.create_item("Rare Seed")
        self.multiworld.state.collect(rare_seed)
        self.assert_can_reach_location(location)

        self.remove(fall)
        self.assert_cannot_reach_location(location)
        self.remove(tuesday)

        green_house = self.create_item("Greenhouse")
        self.multiworld.state.collect(green_house)
        self.assert_cannot_reach_location(location)

        friday = self.create_item("Traveling Merchant: Friday")
        self.multiworld.state.collect(friday)
        self.assert_can_reach_location(location)

        self.remove(green_house)
        self.assert_cannot_reach_location(location)
        self.remove(friday)


class TestToolVanillaRequiresBlacksmith(SVTestBase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_buildings,
        options.EntranceRandomizationBehavior: {},
        options.ToolProgression: options.ToolProgression.option_vanilla,
        options.EntrancePlando: [
            PlandoConnection(Entrance.enter_mens_locker_room, Entrance.town_to_blacksmith, "both", 100),
            PlandoConnection(Entrance.enter_womens_locker_room, Entrance.beach_to_willy_fish_cabin, "both", 100),
            PlandoConnection(Entrance.fish_cabin_to_boat_tunnel, Entrance.enter_sunroom, "both", 100),
        ],
    }

    def test_cannot_get_any_tool_without_blacksmith_access(self):
        mens_locker_item = "Men's Locker Key"
        self.collect_all_except(mens_locker_item)

        for tool in [Tool.pickaxe, Tool.axe, Tool.hoe, Tool.trash_can, Tool.watering_can]:
            for material in [ToolMaterial.copper, ToolMaterial.iron, ToolMaterial.gold, ToolMaterial.iridium]:
                self.assert_rule_false(self.world.logic.tool.has_tool(tool, material))

        self.collect(mens_locker_item)

        for tool in [Tool.pickaxe, Tool.axe, Tool.hoe, Tool.trash_can, Tool.watering_can]:
            for material in [ToolMaterial.copper, ToolMaterial.iron, ToolMaterial.gold, ToolMaterial.iridium]:
                self.assert_rule_true(self.world.logic.tool.has_tool(tool, material))

    def test_cannot_get_fishing_rod_without_willy_access(self):
        mens_locker_item = "Women's Locker Key"
        self.collect_all_except(mens_locker_item)
        self.collect("Fishing Level", 10)
        self.collect("Fishing Mastery")

        for fishing_rod in [FishingRod.training, FishingRod.bamboo, FishingRod.fiberglass, FishingRod.iridium, FishingRod.advanced_iridium]:
            self.assert_rule_false(self.world.logic.tool.has_fishing_rod(fishing_rod))

        self.collect(mens_locker_item)

        for fishing_rod in [FishingRod.training, FishingRod.bamboo, FishingRod.fiberglass, FishingRod.iridium, FishingRod.advanced_iridium]:
            self.assert_rule_true(self.world.logic.tool.has_fishing_rod(fishing_rod))


class TestVanillaFishingRodsRequiresLevelsAndMasteries(SVTestBase):
    options = {  # noqa: RUF012
        options.SeasonRandomization: options.SeasonRandomization.option_disabled,
        options.Cropsanity: options.Cropsanity.option_disabled,
        options.SkillProgression: options.SkillProgression.option_progressive_with_masteries,
        options.ToolProgression: options.ToolProgression.option_vanilla,
    }

    def test_cannot_get_fishing_rods_without_their_unlock_conditions(self):
        self.collect_lots_of_money()

        rods = [FishingRod.training, FishingRod.bamboo, FishingRod.fiberglass, FishingRod.iridium, FishingRod.advanced_iridium]
        reachable = 2
        for i in range(len(rods)):
            if i < reachable:
                self.assert_rule_true(self.world.logic.tool.has_fishing_rod(rods[i]))
            else:
                self.assert_rule_false(self.world.logic.tool.has_fishing_rod(rods[i]))

        self.collect("Fishing Level", 2)
        reachable = 3
        for i in range(len(rods)):
            if i < reachable:
                self.assert_rule_true(self.world.logic.tool.has_fishing_rod(rods[i]))
            else:
                self.assert_rule_false(self.world.logic.tool.has_fishing_rod(rods[i]))

        self.collect("Fishing Level", 4)
        reachable = 4
        for i in range(len(rods)):
            if i < reachable:
                self.assert_rule_true(self.world.logic.tool.has_fishing_rod(rods[i]))
            else:
                self.assert_rule_false(self.world.logic.tool.has_fishing_rod(rods[i]))

        self.collect("Fishing Level", 4)
        reachable = 4
        for i in range(len(rods)):
            if i < reachable:
                self.assert_rule_true(self.world.logic.tool.has_fishing_rod(rods[i]))
            else:
                self.assert_rule_false(self.world.logic.tool.has_fishing_rod(rods[i]))

        self.collect("Fishing Mastery")
        for rod in rods:
            self.assert_rule_true(self.world.logic.tool.has_fishing_rod(rod))
