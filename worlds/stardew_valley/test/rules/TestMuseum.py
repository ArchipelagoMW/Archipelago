from BaseClasses import CollectionState
from ...options import Museumsanity
from .. import SVTestBase


class TestMuseumMilestones(SVTestBase):
    options = {
        Museumsanity.internal_name: Museumsanity.option_milestones
    }

    def world_setup(self, *args, **kwargs):
        super().world_setup(*args, **kwargs)
        self.multiworld.precollected_items[self.player] = []
        self.multiworld.state = CollectionState(self.multiworld)

    def test_50_milestone(self):
        milestone_rule = self.world.logic.museum.can_find_museum_items(50)
        self.assert_rule_false(milestone_rule, self.multiworld.state)
