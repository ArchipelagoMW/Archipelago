from . import MessengerTestBase
from ..constants import NOTES


class PrecollectedNotesTestBase(MessengerTestBase):
    starting_notes: int = 0

    @property
    def run_default_tests(self) -> bool:
        return False

    def test_precollected_notes(self) -> None:
        self.assertEqual(self.multiworld.state.count_group("Notes", self.player), self.starting_notes)

    def test_goal(self) -> None:
        if self.__class__ is not PrecollectedNotesTestBase:
            return
        self.assertBeatable(False)
        self.collect_by_name(NOTES)
        rope_dart = self.get_item_by_name("Rope Dart")
        self.collect(rope_dart)
        self.assertBeatable(True)
        self.remove(rope_dart)
        self.collect_by_name("Wingsuit")
        self.assertBeatable(True)


class TwoNoteGoalTest(PrecollectedNotesTestBase):
    options = {
        "notes_needed": 2,
    }
    starting_notes = 4


class FourNoteGoalTest(PrecollectedNotesTestBase):
    options = {
        "notes_needed": 4,
    }
    starting_notes = 2
