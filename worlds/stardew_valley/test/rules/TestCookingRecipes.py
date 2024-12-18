from ... import options
from ...options import BuildingProgression, ExcludeGingerIsland, Chefsanity
from ...test import SVTestBase


class TestRecipeLearnLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        Chefsanity.internal_name: Chefsanity.option_none,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_learn_qos_recipe(self):
        location = "Cook Radish Salad"
        rule = self.world.logic.region.can_reach_location(location)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Progressive House"), prevent_sweep=False)
        self.multiworld.state.collect(self.create_item("Radish Seeds"), prevent_sweep=False)
        self.multiworld.state.collect(self.create_item("Spring"), prevent_sweep=False)
        self.multiworld.state.collect(self.create_item("Summer"), prevent_sweep=False)
        self.collect_lots_of_money()
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("The Queen of Sauce"), prevent_sweep=False)
        self.assert_rule_true(rule, self.multiworld.state)


class TestRecipeReceiveLogic(SVTestBase):
    options = {
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        Chefsanity.internal_name: Chefsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
    }

    def test_can_learn_qos_recipe(self):
        location = "Cook Radish Salad"
        rule = self.world.logic.region.can_reach_location(location)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Progressive House"), prevent_sweep=False)
        self.multiworld.state.collect(self.create_item("Radish Seeds"), prevent_sweep=False)
        self.multiworld.state.collect(self.create_item("Summer"), prevent_sweep=False)
        self.collect_lots_of_money()
        self.assert_rule_false(rule, self.multiworld.state)

        spring = self.create_item("Spring")
        qos = self.create_item("The Queen of Sauce")
        self.multiworld.state.collect(spring, prevent_sweep=False)
        self.multiworld.state.collect(qos, prevent_sweep=False)
        self.assert_rule_false(rule, self.multiworld.state)
        self.multiworld.state.remove(spring)
        self.multiworld.state.remove(qos)

        self.multiworld.state.collect(self.create_item("Radish Salad Recipe"), prevent_sweep=False)
        self.assert_rule_true(rule, self.multiworld.state)

    def test_get_chefsanity_check_recipe(self):
        location = "Radish Salad Recipe"
        rule = self.world.logic.region.can_reach_location(location)
        self.assert_rule_false(rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Spring"), prevent_sweep=False)
        self.collect_lots_of_money()
        self.assert_rule_false(rule, self.multiworld.state)

        seeds = self.create_item("Radish Seeds")
        summer = self.create_item("Summer")
        house = self.create_item("Progressive House")
        self.multiworld.state.collect(seeds, prevent_sweep=False)
        self.multiworld.state.collect(summer, prevent_sweep=False)
        self.multiworld.state.collect(house, prevent_sweep=False)
        self.assert_rule_false(rule, self.multiworld.state)
        self.multiworld.state.remove(seeds)
        self.multiworld.state.remove(summer)
        self.multiworld.state.remove(house)

        self.multiworld.state.collect(self.create_item("The Queen of Sauce"), prevent_sweep=False)
        self.assert_rule_true(rule, self.multiworld.state)
