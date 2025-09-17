from ..bases import SVTestBase
from ... import options


class TestWizardCatalogueWithoutEndgameLocations(SVTestBase):
    options = {
        options.SeasonRandomization: options.SeasonRandomization.option_disabled,
        options.Cropsanity: options.Cropsanity.option_enabled,
        options.EntranceRandomization: options.EntranceRandomization.option_disabled,
        options.IncludeEndgameLocations: options.IncludeEndgameLocations.option_false,
    }

    def test_doesnt_need_catalogue_to_buy_catalogue(self):
        item = "Ruby Crystal Ball"
        self.collect("Rusty Key")
        self.collect_all_the_money()

        self.assert_rule_true(self.world.logic.has(item))


class TestWizardCatalogueWithEndgameLocations(SVTestBase):
    options = {
        options.SeasonRandomization: options.SeasonRandomization.option_disabled,
        options.Cropsanity: options.Cropsanity.option_enabled,
        options.EntranceRandomization: options.EntranceRandomization.option_disabled,
        options.IncludeEndgameLocations: options.IncludeEndgameLocations.option_true,
    }

    def test_need_catalogue_to_buy_catalogue(self):
        item = "Ruby Crystal Ball"
        self.collect("Rusty Key")
        self.collect_all_the_money()

        self.assert_rule_false(self.world.logic.has(item))
        self.collect("Wizard Catalogue")
        self.assert_rule_true(self.world.logic.has(item))
