from worlds.stardew_valley import options
from ...test.assertion import WorldAssertMixin
from ...test.bases import SVTestBase


class TestCrypticNoteNoQuests(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_cryptic_note,
        options.QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)


class TestCompleteCollectionNoQuests(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_complete_collection,
        options.QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)


class TestProtectorOfTheValleyNoQuests(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_protector_of_the_valley,
        options.QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)


class TestCraftMasterNoQuests(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_craft_master,
        options.QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)


class TestCraftMasterNoSpecialOrder(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: options.Goal.option_craft_master,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.alias_disabled,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.Craftsanity.internal_name: options.Craftsanity.option_none
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)
