from collections import Counter

from ..bases import SVTestBase
from ...options import Museumsanity


class TestMuseumMilestones(SVTestBase):
    options = {
        Museumsanity.internal_name: Museumsanity.option_milestones
    }

    def test_50_milestone(self):
        self.multiworld.state.prog_items = {1: Counter()}

        milestone_rule = self.world.logic.museum.can_find_museum_items(50)
        self.assert_rule_false(milestone_rule, self.multiworld.state)
