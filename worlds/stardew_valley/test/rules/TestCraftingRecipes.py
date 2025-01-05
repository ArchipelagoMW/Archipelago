from ... import options
from ...data.craftable_data import all_crafting_recipes_by_name
from ...options import BuildingProgression, ExcludeGingerIsland, Craftsanity, SeasonRandomization
from ...test import SVTestBase


class TestCraftsanityLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        Craftsanity.internal_name: Craftsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_craft_recipe(self):
        location = "Craft Marble Brazier"
        rule = self.world.logic.region.can_reach_location(location)
        self.collect([self.create_item("Progressive Pickaxe")] * 4)
        self.collect([self.create_item("Progressive Fishing Rod")] * 4)
        self.collect([self.create_item("Progressive Sword")] * 4)
        self.collect([self.create_item("Progressive Mine Elevator")] * 24)
        self.collect([self.create_item("Mining Level")] * 10)
        self.collect([self.create_item("Combat Level")] * 10)
        self.collect([self.create_item("Fishing Level")] * 10)
        self.collect_all_the_money()
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Marble Brazier Recipe"))
        self.assert_rule_true(rule, self.multiworld.state)

    def test_can_learn_crafting_recipe(self):
        location = "Marble Brazier Recipe"
        rule = self.world.logic.region.can_reach_location(location)
        self.assert_rule_false(rule, self.multiworld.state)

        self.collect_lots_of_money()
        self.assert_rule_true(rule, self.multiworld.state)

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.create_item("Pumpkin Seeds"))
        self.multiworld.state.collect(self.create_item("Torch Recipe"))
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Fall"))
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Jack-O-Lantern Recipe"))
        self.assert_rule_true(rule, self.multiworld.state)

    def test_require_furnace_recipe_for_smelting_checks(self):
        locations = ["Craft Furnace", "Smelting", "Copper Pickaxe Upgrade", "Gold Trash Can Upgrade"]
        rules = [self.world.logic.region.can_reach_location(location) for location in locations]
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
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_easy,
        Craftsanity.internal_name: Craftsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.create_item("Pumpkin Seeds"))
        self.multiworld.state.collect(self.create_item("Fall"))
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Jack-O-Lantern Recipe"))
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Torch Recipe"))
        self.assert_rule_true(rule, self.multiworld.state)


class TestNoCraftsanityLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        SeasonRandomization.internal_name: SeasonRandomization.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_disabled,
        Craftsanity.internal_name: Craftsanity.option_none,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_craft_recipe(self):
        recipe = all_crafting_recipes_by_name["Wood Floor"]
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_true(rule, self.multiworld.state)

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.create_item("Pumpkin Seeds"))
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        result = rule(self.multiworld.state)
        self.assertFalse(result)

        self.collect([self.create_item("Progressive Season")] * 2)
        self.assert_rule_true(rule, self.multiworld.state)

    def test_requires_mining_levels_for_smelting_checks(self):
        locations = ["Smelting", "Copper Pickaxe Upgrade", "Gold Trash Can Upgrade"]
        rules = [self.world.logic.region.can_reach_location(location) for location in locations]
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
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.FestivalLocations.internal_name: options.FestivalLocations.option_easy,
        Craftsanity.internal_name: Craftsanity.option_none,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_craft_festival_recipe(self):
        recipe = all_crafting_recipes_by_name["Jack-O-Lantern"]
        self.multiworld.state.collect(self.create_item("Pumpkin Seeds"))
        self.multiworld.state.collect(self.create_item("Fall"))
        self.collect_lots_of_money()
        rule = self.world.logic.crafting.can_craft(recipe)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Jack-O-Lantern Recipe"))
        self.assert_rule_true(rule, self.multiworld.state)
