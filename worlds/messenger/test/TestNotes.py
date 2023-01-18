from . import MessengerTestBase


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
