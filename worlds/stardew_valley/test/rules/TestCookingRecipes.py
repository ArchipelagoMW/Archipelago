from ..bases import SVTestBase
from ... import options
from ...content.content_packs import ginger_island_content_pack
from ...data.recipe_data import all_cooking_recipes


class TestRecipeContainingGingerIslandIngredientsAreTaggedWithGingerIslandContentPack(SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
        options.Mods: frozenset(options.all_mods_except_invalid_combinations),
    }

    def test_recipe_without_content_pack_contains_only_pure_vanilla_ingredients(self):
        for item in self.multiworld.get_items():
            self.multiworld.state.collect(item, prevent_sweep=True)

        logic = self.world.logic

        for recipe in all_cooking_recipes:
            if recipe.content_pack is ginger_island_content_pack.name or recipe.content_pack not in self.world.options.mods:
                continue

            with self.subTest(recipe.meal):
                for item in recipe.ingredients:
                    rule = logic.has(item)
                    self.assert_rule_true(rule, self.multiworld.state)


class TestRecipeLearnLogic(SVTestBase):
    options = {
        options.BuildingProgression: options.BuildingProgression.option_progressive,
        options.Cropsanity: options.Cropsanity.option_enabled,
        options.Cooksanity: options.Cooksanity.option_all,
        options.Chefsanity: options.Chefsanity.preset_none,
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
    }

    def test_can_learn_qos_recipe(self):
        location = "Cook Radish Salad"
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive House"))
        self.multiworld.state.collect(self.create_item("Radish Seeds"))
        self.multiworld.state.collect(self.create_item("Spring"))
        self.multiworld.state.collect(self.create_item("Summer"))
        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("The Queen of Sauce"))
        self.assert_can_reach_location(location)


class TestRecipeReceiveLogic(SVTestBase):
    options = {
        options.StartWithout: options.StartWithout.preset_none,
        options.BuildingProgression: options.BuildingProgression.option_progressive,
        options.Cropsanity: options.Cropsanity.option_enabled,
        options.Cooksanity: options.Cooksanity.option_all,
        options.Chefsanity: options.Chefsanity.preset_all,
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
    }

    def test_can_learn_qos_recipe(self):
        location = "Cook Radish Salad"
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive House"))
        self.multiworld.state.collect(self.create_item("Radish Seeds"))
        self.multiworld.state.collect(self.create_item("Summer"))
        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        spring = self.create_item("Spring")
        qos = self.create_item("The Queen of Sauce")
        self.multiworld.state.collect(spring)
        self.multiworld.state.collect(qos)
        self.assert_cannot_reach_location(location)
        self.multiworld.state.remove(spring)
        self.multiworld.state.remove(qos)

        self.multiworld.state.collect(self.create_item("Radish Salad Recipe"))
        self.assert_can_reach_location(location)

    def test_get_chefsanity_check_recipe(self):
        location = "Radish Salad Recipe"
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Spring"))
        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        seeds = self.create_item("Radish Seeds")
        summer = self.create_item("Summer")
        house = self.create_item("Progressive House")
        self.multiworld.state.collect(seeds)
        self.multiworld.state.collect(summer)
        self.multiworld.state.collect(house)
        self.assert_cannot_reach_location(location)
        self.multiworld.state.remove(seeds)
        self.multiworld.state.remove(summer)
        self.multiworld.state.remove(house)

        self.multiworld.state.collect(self.create_item("The Queen of Sauce"))
        self.assert_can_reach_location(location)
