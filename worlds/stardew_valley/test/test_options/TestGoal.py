from typing import ClassVar

from test.param import classvar_matrix
from ...options import Goal
from ...strings.goal_names import Goal as GoalName
from ...test.bases import SVTestCase, solo_multiworld


@classvar_matrix(goal_and_location=[
    ("community_center", GoalName.community_center),
    ("grandpa_evaluation", GoalName.grandpa_evaluation),
    ("bottom_of_the_mines", GoalName.bottom_of_the_mines),
    ("cryptic_note", GoalName.cryptic_note),
    ("master_angler", GoalName.master_angler),
    ("complete_collection", GoalName.complete_museum),
    ("full_house", GoalName.full_house),
    ("perfection", GoalName.perfection),
])
class TestGoal(SVTestCase):
    goal_and_location: ClassVar[tuple[str, str]]

    def test_given_goal_when_generate_then_victory_is_in_correct_location(self):
        goal, location = self.goal_and_location
        world_options = {Goal.internal_name: goal}
        with solo_multiworld(world_options) as (multi_world, _):
            victory = multi_world.find_item("Victory", 1)
            self.assertEqual(victory.name, location)