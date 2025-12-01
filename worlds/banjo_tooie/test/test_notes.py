from ..Names import itemName
from ..Options import RandomizeNotes
from .test_logic import EasyTricksLogic, EasyTricksLogicNoBKShuffle, GlitchesLogic, \
    GlitchesLogicNoBKShuffle, HardTricksLogic, HardTricksLogicNoBKShuffle, \
    IntendedLogic, IntendedLogicNoBKShuffle
from .test_fillers_and_traps import ONLY_BIG_O_PANTS_FILLER
from ..Locations import all_location_table
from . import BanjoTooieTestBase


class TestRandomizedNotes(BanjoTooieTestBase):
    options = {
        "randomize_notes": RandomizeNotes.option_true,
        **ONLY_BIG_O_PANTS_FILLER
    }

    def test_item_pool(self) -> None:
        # max jamjars cost is 765. There are 9 trebleclefs by default.
        progression_notes_default = (765 - 9*20) // 5

        notes_in_pool = [item for item in self.multiworld.itempool if item.name == itemName.NOTE]

        progresssion = sum(1 for item in notes_in_pool if item.advancement)
        useful = sum(1 for item in notes_in_pool if item.useful)

        assert progresssion == progression_notes_default
        assert useful == 14  # (144 - progression_notes_default) / 2


class TestVanillaNotes(BanjoTooieTestBase):
    options = {
        "randomize_notes": RandomizeNotes.option_false,
        **ONLY_BIG_O_PANTS_FILLER
    }

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        assert item_pool_names.count(itemName.NOTE) == 0

    def test_prefills(self) -> None:
        vanilla_locations_names = self.world.location_name_groups["Notes"]
        vanilla_locations = [location for location in self.world.get_locations()
                             if location.name in vanilla_locations_names]

        assert len(vanilla_locations) == 144
        for location in vanilla_locations:
            assert location.item.name == itemName.NOTE


class TestRandomizedNotesIntended(TestRandomizedNotes, IntendedLogic):
    options = {
        **TestRandomizedNotes.options,
        **IntendedLogic.options,
    }


class TestRandomizedNotesEasyTricks(TestRandomizedNotes, EasyTricksLogic):
    options = {
        **TestRandomizedNotes.options,
        **EasyTricksLogic.options,
    }


class TestRandomizedNotesHardTricks(TestRandomizedNotes, HardTricksLogic):
    options = {
        **TestRandomizedNotes.options,
        **HardTricksLogic.options,
    }


class TestRandomizedNotesGlitches(TestRandomizedNotes, GlitchesLogic):
    options = {
        **TestRandomizedNotes.options,
        **GlitchesLogic.options,
    }


class TestVanillaNotesIntended(TestVanillaNotes, IntendedLogicNoBKShuffle):
    options = {
        **TestVanillaNotes.options,
        **IntendedLogicNoBKShuffle.options,
    }


class TestVanillaNotesEasyTricks(TestVanillaNotes, EasyTricksLogicNoBKShuffle):
    options = {
        **TestVanillaNotes.options,
        **EasyTricksLogicNoBKShuffle.options,
    }


class TestVanillaNotesHardTricks(TestVanillaNotes, HardTricksLogicNoBKShuffle):
    options = {
        **TestVanillaNotes.options,
        **HardTricksLogicNoBKShuffle.options,
    }


class TestVanillaNotesGlitches(TestVanillaNotes, GlitchesLogicNoBKShuffle):
    options = {
        **TestVanillaNotes.options,
        **GlitchesLogicNoBKShuffle.options,
    }
