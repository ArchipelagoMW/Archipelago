from . import SVTestBase
from .assertion import WorldAssertMixin
from .. import options
from ..options import Goal, QuestLocations


class TestCrypticNoteNoQuests(WorldAssertMixin, SVTestBase):
    options = {
        Goal.internal_name: Goal.option_cryptic_note,
        QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)


class TestCompleteCollectionNoQuests(WorldAssertMixin, SVTestBase):
    options = {
        Goal.internal_name: Goal.option_complete_collection,
        QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)


class TestProtectorOfTheValleyNoQuests(WorldAssertMixin, SVTestBase):
    options = {
        Goal.internal_name: Goal.option_protector_of_the_valley,
        QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)


class TestCraftMasterNoQuests(WorldAssertMixin, SVTestBase):
    options = {
        Goal.internal_name: Goal.option_craft_master,
        QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)


class TestCraftMasterNoSpecialOrder(WorldAssertMixin, SVTestBase):
    options = {
        options.Goal.internal_name: Goal.option_craft_master,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_disabled,
        options.ExcludeGingerIsland.internal_name: options.ExcludeGingerIsland.option_true,
        options.Craftsanity.internal_name: options.Craftsanity.option_none
    }

    def test_given_option_pair_then_basic_checks(self):
        self.assert_basic_checks(self.multiworld)
