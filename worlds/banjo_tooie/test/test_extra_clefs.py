from ..Names import itemName
from ..Options import BassClefNotes, RandomizeNotes, TrebleclefNotes
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from .test_fillers_and_traps import ONLY_BIG_O_PANTS_FILLER
from . import BanjoTooieTestBase


class TestClefs(BanjoTooieTestBase):
    options = {
        "randomize_notes": RandomizeNotes.option_true,
        **ONLY_BIG_O_PANTS_FILLER
    }

    def test_clef_count(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool if item.advancement]
        assert item_pool_names.count(itemName.BASS) == self.world.options.bass_clef_amount.value
        assert item_pool_names.count(itemName.TREBLE) == self.world.options.extra_trebleclefs_count.value + 9

    def test_notes_count(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool if item.advancement]

        # max jamjars cost is 765. There are 9 trebleclefs by default.
        progression_notes_default = (765 - 9*20) // 5

        assert item_pool_names.count(itemName.NOTE)\
            == max(progression_notes_default
                   - 2 * self.world.options.bass_clef_amount.value
                   - 4 * self.world.options.extra_trebleclefs_count.value,
                   0)


class TestMinClefs(TestClefs):
    options = {
        **TestClefs.options,
        "bass_clef_amount": 0,
        "extra_trebleclefs_count": 0
    }


class TestNoBassSomeTrebles(TestClefs):
    options = {
        **TestClefs.options,
        "bass_clef_amount": 0,
        "extra_trebleclefs_count": 15
    }


class TestSomeBassNoTrebles(TestClefs):
    options = {
        **TestClefs.options,
        "bass_clef_amount": 10,
        "extra_trebleclefs_count": 0
    }


class TestSomeOfEach(TestClefs):
    options = {
        **TestClefs.options,
        "bass_clef_amount": 15,
        "extra_trebleclefs_count": 10
    }


class TestMaxClefs(TestClefs):
    options = {
        **TestClefs.options,
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
