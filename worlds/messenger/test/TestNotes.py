from . import MessengerTestBase
from ..Constants import NOTES


class TwoNoteGoalTest(MessengerTestBase):
    options = {
        "notes_needed": 2,
    }

    def testPrecollectedNotes(self) -> None:
        self.assertEqual(self.multiworld.state.count_group("Notes", self.player), 4)


class FourNoteGoalTest(MessengerTestBase):
    options = {
        "notes_needed": 4,
    }

    def testPrecollectedNotes(self) -> None:
        self.assertEqual(self.multiworld.state.count_group("Notes", self.player), 2)


class DefaultGoalTest(MessengerTestBase):
    def testPrecollectedNotes(self) -> None:
        self.assertEqual(self.multiworld.state.count_group("Notes", self.player), 0)

    def testGoal(self) -> None:
        self.assertBeatable(False)
        self.collect_by_name(NOTES)
        self.assertBeatable(True)
