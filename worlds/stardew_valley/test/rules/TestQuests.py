from ..bases import SVTestBase
from ...options import ToolProgression, QuestLocations, Secretsanity
from ...strings.ap_names.ap_option_names import SecretsanityOptionName


class TestQuestsLogic(SVTestBase):
    options = {
        QuestLocations.internal_name: 0,
        ToolProgression.internal_name: ToolProgression.option_progressive,
    }

    def test_giant_stump_requires_one_raccoon(self):
        quest_name = "Quest: The Giant Stump"
        quest_location = self.world.get_location(quest_name)

        self.assert_cannot_reach_location(quest_location)

        self.collect("Progressive Axe", 2)
        self.assert_cannot_reach_location(quest_location)

        self.collect("Progressive Raccoon")
        self.assert_can_reach_location(quest_location)


class TestQuestsOverrideBySecretNotesLogic(SVTestBase):
    options = {
        QuestLocations.internal_name: 0,
        Secretsanity.internal_name: frozenset(SecretsanityOptionName.secret_notes),
    }

    def test_giant_stump_requires_one_raccoon(self):
        location_names = [location.name for location in self.multiworld.get_locations()]
        self.assertNotIn("Quest: Strange Note", location_names)
        self.assertIn("Secret Note #23: Strange Note", location_names)
        self.assertEqual(1, len([name for name in location_names if "Strange Note" in name]))