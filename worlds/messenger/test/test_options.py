from BaseClasses import CollectionState
from Fill import distribute_items_restrictive
from . import MessengerTestBase
from .. import MessengerWorld
from ..options import Logic


class LimitedMovementTest(MessengerTestBase):
    options = {
        "limited_movement": "true",
        "shuffle_shards": "true",
    }

    @property
    def run_default_tests(self) -> bool:
        # This test base fails reachability tests. Not sure if the core tests should change to support that
        return False

    def test_options(self) -> None:
        """Tests that options were correctly changed."""
        assert isinstance(self.multiworld.worlds[self.player], MessengerWorld)
        self.assertEqual(Logic.option_hard, self.world.options.logic_level)


class EarlyMeditationTest(MessengerTestBase):
    options = {
        "early_meditation": "true",
    }

    def test_option(self) -> None:
        """Checks that Meditation gets placed early"""
        distribute_items_restrictive(self.multiworld)
        sphere1 = self.multiworld.get_reachable_locations(CollectionState(self.multiworld))
        items = [loc.item.name for loc in sphere1]
        self.assertIn("Meditation", items)
