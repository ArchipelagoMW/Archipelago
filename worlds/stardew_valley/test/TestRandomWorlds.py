from typing import ClassVar

from BaseClasses import MultiWorld, get_seed
from test.param import classvar_matrix

from .. import EntranceRandomizationBehaviorOptionName
from ..options import EntranceRandomizationBehavior
from .assertion import GoalAssertMixin, OptionAssertMixin, WorldAssertMixin
from .bases import SVTestCase, skip_long_tests, solo_multiworld
from .options.option_names import generate_random_world_options


@classvar_matrix(n=range(1000 if skip_long_tests() else 1000))
class TestGenerateManyWorlds(GoalAssertMixin, OptionAssertMixin, WorldAssertMixin, SVTestCase):
    n: ClassVar[int]

    def test_generate_many_worlds_then_check_results(self):
        seed = get_seed()
        world_options = generate_random_world_options(seed + self.n)

        # Currently, these ER Behaviors have a small chance of failing generation. We don't want to fail the pipeline and annoy other people, so we exclude this here.
        er_behaviors = world_options[EntranceRandomizationBehavior.internal_name]
        world_options[EntranceRandomizationBehavior.internal_name] = frozenset({behavior for behavior in er_behaviors
                                                                                if behavior != EntranceRandomizationBehaviorOptionName.same_direction})

        print(f"Generating solo multiworld with seed {seed} for Stardew Valley...")
        with solo_multiworld(world_options, seed=seed, world_caching=False) as (multiworld, _):
            self.assert_multiworld_is_valid(multiworld)

    def assert_multiworld_is_valid(self, multiworld: MultiWorld):
        self.assert_victory_exists(multiworld)
        self.assert_same_number_items_locations(multiworld)
        self.assert_goal_world_is_valid(multiworld)
        self.assert_can_reach_island_if_should(multiworld)
        self.assert_cropsanity_same_number_items_and_locations(multiworld)
        self.assert_festivals_give_access_to_deluxe_scarecrow(multiworld)
        self.assert_has_festival_recipes(multiworld)
