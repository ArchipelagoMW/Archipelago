from ..bases import SVTestBase
from ... import options, StartWithoutOptionName
from ...data.craftable_data import all_crafting_recipes_by_name
from ...options import StartWithout


class TestCraftsanityLogic(SVTestBase):
    options = {
        StartWithout.internal_name: frozenset({StartWithoutOptionName.buildings}),
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_disabled,
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
    }

    def test_can_craft_recipe(self):
        location = "Craft Marble Brazier"
        self.collect(self.create_item("Landslide Removed"))
        self.collect([self.create_item("Progressive Pickaxe")] * 4)
        self.collect([self.create_item("Progressive Fishing Rod")] * 4)
        self.collect([self.create_item("Progressive Sword")] * 4)
        self.collect([self.create_item("Progressive Mine Elevator")] * 24)
        self.collect([self.create_item("Progressive Pan")] * 4)
        self.collect([self.create_item("Mining Level")] * 10)
        self.collect([self.create_item("Combat Level")] * 10)
        self.collect([self.create_item("Fishing Level")] * 10)
        self.collect_all_the_money()
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Marble Brazier Recipe"))
        self.assert_can_reach_location(location)

    def test_can_learn_crafting_recipe(self):
        location = "Marble Brazier Recipe"
        self.assert_cannot_reach_location(location)

        self.collect_lots_of_money()
        self.assert_can_reach_location(location)

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.create_item("Pumpkin Seeds"))
        self.multiworld.state.collect(self.create_item("Torch Recipe"))
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule)

        self.multiworld.state.collect(self.create_item("Fall"))
        self.assert_rule_false(rule)

        self.multiworld.state.collect(self.create_item("Jack-O-Lantern Recipe"))
        self.assert_rule_true(rule)

    def test_require_furnace_recipe_for_smelting_checks(self):
        locations = ["Craft Furnace", "Quest: Smelting", "Copper Pickaxe Upgrade", "Gold Trash Can Upgrade"]
        rules = [self.world.logic.region.can_reach_location(location) for location in locations]
        self.collect(self.create_item("Landslide Removed"))
        self.collect([self.create_item("Progressive Pickaxe")] * 4)
        self.collect([self.create_item("Progressive Fishing Rod")] * 4)
        self.collect([self.create_item("Progressive Sword")] * 4)
        self.collect([self.create_item("Progressive Mine Elevator")] * 24)
        self.collect([self.create_item("Progressive Trash Can")] * 2)
        self.collect([self.create_item("Mining Level")] * 10)
        self.collect([self.create_item("Combat Level")] * 10)
        self.collect([self.create_item("Fishing Level")] * 10)
        self.collect_all_the_money()
        self.assert_rules_false(rules, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Furnace Recipe"))
        self.assert_rules_true(rules, self.multiworld.state)


class TestCraftsanityWithFestivalsLogic(SVTestBase):
    options = {
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_easy,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
    }

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.create_item("Pumpkin Seeds"))
        self.multiworld.state.collect(self.create_item("Fall"))
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule)

        self.multiworld.state.collect(self.create_item("Jack-O-Lantern Recipe"))
        self.assert_rule_false(rule)

        self.multiworld.state.collect(self.create_item("Torch Recipe"))
        self.assert_rule_true(rule)


class TestNoCraftsanityLogic(SVTestBase):
    options = {
        options.SkillProgression.internal_name: options.SkillProgression.option_progressive,
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.SeasonRandomization.internal_name: options.SeasonRandomization.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_disabled,
        options.Craftsanity.internal_name: options.Craftsanity.option_none,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
    }

    def test_can_craft_recipe(self):
        recipe = all_crafting_recipes_by_name["Wood Floor"]
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_true(rule)

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.create_item("Pumpkin Seeds"))
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        result = rule(self.multiworld.state)
        self.assertFalse(result)

        self.collect([self.create_item("Progressive Season")] * 2)
        self.assert_rule_true(rule)

    def test_requires_mining_levels_for_smelting_checks(self):
        locations = ["Quest: Smelting", "Copper Pickaxe Upgrade", "Gold Trash Can Upgrade"]
        rules = [self.world.logic.region.can_reach_location(location) for location in locations]
        self.collect(self.create_item("Landslide Removed"))
        self.collect([self.create_item("Progressive Pickaxe")] * 4)
        self.collect([self.create_item("Progressive Fishing Rod")] * 4)
        self.collect([self.create_item("Progressive Sword")] * 4)
        self.collect([self.create_item("Progressive Mine Elevator")] * 24)
        self.collect([self.create_item("Progressive Trash Can")] * 2)
        self.multiworld.state.collect(self.create_item("Furnace Recipe"))
        self.collect([self.create_item("Combat Level")] * 10)
        self.collect([self.create_item("Fishing Level")] * 10)
        self.collect_all_the_money()
        self.assert_rules_false(rules, self.multiworld.state)

        self.collect([self.create_item("Mining Level")] * 10)
        self.assert_rules_true(rules, self.multiworld.state)


class TestNoCraftsanityWithFestivalsLogic(SVTestBase):
    options = {
        options.BuildingProgression.internal_name: options.BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_easy,
        options.Craftsanity.internal_name: options.Craftsanity.option_none,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
    }

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.create_item("Pumpkin Seeds"))
        self.multiworld.state.collect(self.create_item("Fall"))
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule)

        self.multiworld.state.collect(self.create_item("Jack-O-Lantern Recipe"))
        self.assert_rule_true(rule)
