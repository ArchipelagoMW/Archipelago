import typing
from BaseClasses import ItemClassification
from ...AutoWorld import call_all
from test.bases import WorldTestBase
from ..Options import HintClarity, RandomizeBKMoveList, RandomizeBTMoveList, RandomizeSignposts, SignpostHints
from . import BanjoTooieTestBase
from ..Items import moves_table, bk_moves_table, progressive_ability_table

class TestSignpostsHints(BanjoTooieTestBase):
    # fill_slot_data needs to be run for these tests to properly run.
    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        super(BanjoTooieTestBase, self).world_setup(seed)
        call_all(self.multiworld, "fill_slot_data")

    def test_hint_count(self) -> None:
        assert len(self.world.hints) == 61

        non_joke_hints = len([hint_data for hint_data in self.world.hints.values() if hint_data.location_id])
        assert non_joke_hints == self.world.options.signpost_hints

    def test_move_hint_count(self) -> None:
        move_names = [
            *[move_name for move_name in moves_table.keys()],
            *[move_name for move_name in bk_moves_table.keys()],
            *[move_name for move_name in progressive_ability_table.keys()],
        ]

        move_hints = 0
        for hint_data in self.world.hints.values():
            hinted_location = [
                    location for location in self.world.get_locations()\
                    if location.address == hint_data.location_id
                ][0]
            if hinted_location.item.name in move_names:
                move_hints += 1

        # There can be more if slow locations are also hinted.
        possible_moves = 0
        if self.world.options.randomize_moves:
            possible_moves += 24
        if self.world.options.randomize_bk_moves == RandomizeBKMoveList.option_all:
            possible_moves += 16


        if move_hints == 0 and min(self.world.options.signpost_move_hints, possible_moves, self.world.options.signpost_hints) != 0:
            print([hint.text for hint in self.world.hints.values()])
        assert move_hints >= min(self.world.options.signpost_move_hints, possible_moves, self.world.options.signpost_hints)


class TestClearSignpostsHints(TestSignpostsHints):
    options = {
        "hint_clarity": HintClarity.option_clear
    }
    def test_accurate_hint_text(self) -> None:
        for hint_data in self.world.hints.values():
            if not hint_data.location_id:
                continue
            hinted_location = [
                location for location in self.world.get_locations()\
                if location.address == hint_data.location_id
            ][0]

            text = hint_data.text

            finder = self.world.player_name[hinted_location.player]
            location = hinted_location.name
            receiver = self.world.player_name[hinted_location.item.player]
            item = hinted_location.item.name

            assert finder in text
            assert location in text
            assert receiver in text
            assert item in text

class TestCrypticSignpostsHints(TestSignpostsHints):
    options = {
        "hint_clarity": HintClarity.option_cryptic
    }
    def test_accurate_hint_text(self) -> None:
        for hint_data in self.world.hints.values():
            if not hint_data.location_id:
                continue
            hinted_location = [
                location for location in self.world.get_locations()\
                if location.address == hint_data.location_id\
                    and location.player == hint_data.location_player_id
            ][0]

            text = hint_data.text[::]

            finder = self.world.player_name[hinted_location.player]
            location = hinted_location.name

            classification_keywords = {
                ItemClassification.progression: "wonderful",
                ItemClassification.useful: "good",
                ItemClassification.filler: "okay",
            }

            assert text.find(finder) != -1
            assert text.find(location) != -1
            assert classification_keywords[hinted_location.item.classification] in text


class TestClearSignpostsNoHints(TestClearSignpostsHints):
    options = {
        **TestClearSignpostsHints.options,
        "signpost_hints": 0,
        "signpost_move_hints": 0
    }

class TestClearSignpostsAllHintsHalfMoves(TestClearSignpostsHints):
    options = {
        **TestClearSignpostsHints.options,
        "randomize_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "signpost_hints": SignpostHints.range_end,
        "signpost_move_hints": 30,
        "randomize_signposts": RandomizeSignposts.option_true
    }

class TestCrypticSignpostsNoHints(TestCrypticSignpostsHints):
    options = {
        **TestCrypticSignpostsHints.options,
        "signpost_hints": 0,
        "signpost_move_hints": 0
    }

class TestCrypticSignpostsAllHintsHalfMoves(TestCrypticSignpostsHints):
    options = {
        **TestCrypticSignpostsHints.options,
        "randomize_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "signpost_hints": SignpostHints.range_end,
        "signpost_move_hints": 30,
        "randomize_signposts": RandomizeSignposts.option_true
    }
