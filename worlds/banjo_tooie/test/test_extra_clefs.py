from ..Names import itemName
from ..Options import BassClefNotes, RandomizeBKMoveList, RandomizeNotes, TrebleclefNotes
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase

class TestClefs(BanjoTooieTestBase):
    def test_clef_count(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.BASS) == self.world.options.bass_clef_amount
        assert item_pool_names.count(itemName.TREBLE) == self.world.options.extra_trebleclefs_count + 9

    def test_filler_count(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]

        expected_fillers = self.world.options.bass_clef_amount + 3 * self.world.options.extra_trebleclefs_count
        if self.world.options.randomize_bk_moves == RandomizeBKMoveList.option_none:
            expected_fillers += 16
        assert item_pool_names.count(itemName.NONE) == expected_fillers

class TestMinClefs(TestClefs):
    options = {
        "randomize_notes": RandomizeNotes.option_true,
        "bass_clef_amount": 0,
        "extra_trebleclefs_count": 0
    }

class TestNoBassSomeTrebles(TestClefs):
    options = {
        "randomize_notes": RandomizeNotes.option_true,
        "bass_clef_amount": 0,
        "extra_trebleclefs_count": 15
    }

class TestSomeBassNoTrebles(TestClefs):
    options = {
        "randomize_notes": RandomizeNotes.option_true,
        "bass_clef_amount": 10,
        "extra_trebleclefs_count": 0
    }

class TestSomeOfEach(TestClefs):
    options = {
        "randomize_notes": RandomizeNotes.option_true,
        "bass_clef_amount": 15,
        "extra_trebleclefs_count": 10
    }

class TestMaxClefs(TestClefs):
    options = {
        "randomize_notes": RandomizeNotes.option_true,
        "bass_clef_amount": BassClefNotes.range_end,
        "extra_trebleclefs_count": TrebleclefNotes.range_end
    }

class TestMinClefsIntended(TestMinClefs, IntendedLogic):
    options = {
        **TestMinClefs.options,
        **IntendedLogic.options
    }

class TestMinClefsEasyTricks(TestMinClefs, EasyTricksLogic):
    options = {
        **TestMinClefs.options,
        **EasyTricksLogic.options
    }

class TestMinClefsHardTricks(TestMinClefs, HardTricksLogic):
    options = {
        **TestMinClefs.options,
        **HardTricksLogic.options
    }

class TestMinClefsGlitches(TestMinClefs, GlitchesLogic):
    options = {
        **TestMinClefs.options,
        **GlitchesLogic.options
    }

class TestNoBassSomeTreblesIntended(TestNoBassSomeTrebles, IntendedLogic):
    options = {
        **TestNoBassSomeTrebles.options,
        **IntendedLogic.options
    }

class TestNoBassSomeTreblesEasyTricks(TestNoBassSomeTrebles, EasyTricksLogic):
    options = {
        **TestNoBassSomeTrebles.options,
        **EasyTricksLogic.options
    }

class TestNoBassSomeTreblesHardTricks(TestNoBassSomeTrebles, HardTricksLogic):
    options = {
        **TestNoBassSomeTrebles.options,
        **HardTricksLogic.options
    }

class TestNoBassSomeTreblesGlitches(TestNoBassSomeTrebles, GlitchesLogic):
    options = {
        **TestNoBassSomeTrebles.options,
        **GlitchesLogic.options
    }

class TestSomeBassNoTreblesIntended(TestSomeBassNoTrebles, IntendedLogic):
    options = {
        **TestSomeBassNoTrebles.options,
        **IntendedLogic.options
    }

class TestSomeBassNoTreblesEasyTricks(TestSomeBassNoTrebles, EasyTricksLogic):
    options = {
        **TestSomeBassNoTrebles.options,
        **EasyTricksLogic.options
    }

class TestSomeBassNoTreblesHardTricks(TestSomeBassNoTrebles, HardTricksLogic):
    options = {
        **TestSomeBassNoTrebles.options,
        **HardTricksLogic.options
    }

class TestSomeBassNoTreblesGlitches(TestSomeBassNoTrebles, GlitchesLogic):
    options = {
        **TestSomeBassNoTrebles.options,
        **GlitchesLogic.options
    }

class TestMaxClefsIntended(TestMaxClefs, IntendedLogic):
    options = {
        **TestMaxClefs.options,
        **IntendedLogic.options
    }

class TestMaxClefsEasyTricks(TestMaxClefs, EasyTricksLogic):
    options = {
        **TestMaxClefs.options,
        **EasyTricksLogic.options
    }

class TestMaxClefsHardTricks(TestMaxClefs, HardTricksLogic):
    options = {
        **TestMaxClefs.options,
        **HardTricksLogic.options
    }

class TestMaxClefsGlitches(TestMaxClefs, GlitchesLogic):
    options = {
        **TestMaxClefs.options,
        **GlitchesLogic.options
    }
