from . import SVTestBase
from .checks.world_checks import basic_checks
from ..options import Goal, QuestLocations


class TestCrypticNoteNoQuests(SVTestBase):
    options = {
        Goal.internal_name: Goal.option_cryptic_note,
        QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        basic_checks(self, self.multiworld)


class TestCompleteCollectionNoQuests(SVTestBase):
    options = {
        Goal.internal_name: Goal.option_complete_collection,
        QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        basic_checks(self, self.multiworld)


class TestProtectorOfTheValleyNoQuests(SVTestBase):
    options = {
        Goal.internal_name: Goal.option_protector_of_the_valley,
        QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        basic_checks(self, self.multiworld)


class TestCraftMasterNoQuests(SVTestBase):
    options = {
        Goal.internal_name: Goal.option_craft_master,
        QuestLocations.internal_name: "none"
    }

    def test_given_option_pair_then_basic_checks(self):
        basic_checks(self, self.multiworld)
