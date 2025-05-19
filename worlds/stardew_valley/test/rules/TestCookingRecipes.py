from ..bases import SVTestBase
from ... import options
from ...options import BuildingProgression, ExcludeGingerIsland, Chefsanity


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
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        Chefsanity.internal_name: Chefsanity.option_all,
        ExcludeGingerIsland.internal_name: ExcludeGingerIsland.option_true,
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
