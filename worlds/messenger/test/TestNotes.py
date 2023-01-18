from . import MessengerTestBase
from .. import NOTES


class TwoNoteGoalTest(MessengerTestBase):
    options = {
        "notes_needed": 2,
    }

    def testPrecollectedNotes(self):
        self.assertEqual(self.multiworld.state.count_group("Notes", 1), 4)


class FourNoteGoalTest(MessengerTestBase):
    options = {
        "notes_needed": 4,
    }

    def testPrecollectedNotes(self):
        self.assertEqual(self.multiworld.state.count_group("Notes", 1), 2)


class DefaultGoalTest(MessengerTestBase):
    def testPrecollectedNotes(self):
        self.assertEqual(self.multiworld.state.count_group("Notes", 1), 0)

    def testGoal(self):
        self.assertBeatable(False)
        self.collect_by_name(NOTES)
        self.assertBeatable(True)
