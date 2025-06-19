from ..bases import SVTestBase
from ...options import ToolProgression, QuestLocations


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