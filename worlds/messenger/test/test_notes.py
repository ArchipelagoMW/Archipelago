from . import MessengerTestBase
from ..constants import NOTES


class TwoNoteGoalTest(MessengerTestBase):
    options = {
        "notes_needed": 2,
    }

    def test_precollected_notes(self) -> None:
        self.assertEqual(self.multiworld.state.count_group("Notes", self.player), 4)


class FourNoteGoalTest(MessengerTestBase):
    options = {
        "notes_needed": 4,
    }

    def test_precollected_notes(self) -> None:
        self.assertEqual(self.multiworld.state.count_group("Notes", self.player), 2)


class DefaultGoalTest(MessengerTestBase):
    def test_precollected_notes(self) -> None:
        self.assertEqual(self.multiworld.state.count_group("Notes", self.player), 0)

    def test_goal(self) -> None:
        self.assertBeatable(False)
        self.collect_by_name(NOTES)
        rope_dart = self.get_item_by_name("Rope Dart")
        self.collect(rope_dart)
        self.assertBeatable(True)
        self.remove(rope_dart)
        self.collect_by_name("Wingsuit")
        self.assertBeatable(True)
